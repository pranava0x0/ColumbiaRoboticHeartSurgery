"""Gates for docs/ (the static site).

Static checks parse the shipped files directly; the layout checks drive the
page in headless Chromium and skip, loudly, when Playwright or its browser is
missing. Run: python3 -m unittest discover -s tests -v
"""
from __future__ import annotations

import functools
import http.server
import importlib.util
import json
import re
import subprocess
import sys
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
HTML = (DOCS / "index.html").read_text(encoding="utf-8")
CSS = (DOCS / "styles.css").read_text(encoding="utf-8")
JS = (DOCS / "app.js").read_text(encoding="utf-8")

MAIN = HTML[HTML.index("<main"):HTML.index("</main>")]
ROLES = {"patients", "physicians"}
MAX_TAB_LABEL = 11  # six tabs across a 375px bottom bar at 11px type
TOUCH_FLOOR = 44 - 0.5  # DESIGN 7; half-pixel tolerance for device scaling

SECTION_RE = re.compile(
    r'<section id="(?P<id>[\w-]+)" class="panel" data-role="(?P<role>\w+)" '
    r'data-section="(?P<section>[\w-]+)" data-label="(?P<label>[^"]+)">'
)

# DESIGN 11.1 register words that must not appear in shipped copy.
BANNED_WORDS = [
    "delve", "leverage", "robust", "seamless", "seamlessly", "elevate", "unlock", "empower",
    "harness", "tapestry", "testament", "underscore", "underscores", "pivotal", "crucial",
    "comprehensive", "cutting-edge", "game-changer", "ever-evolving", "realm",
    "state-of-the-art", "world-class", "at your fingertips", "next level", "it's worth noting",
    "in conclusion", "not only", "rather than",
]

NUMERIC_CLAIM = re.compile(
    r"\b\d[\d,.]*[-\s]*(%|days?|weeks?|hours?|years?|patients|procedures|operations|cases|"
    r"hospitals|inch|cm|mm)\b|\b\d{1,3}(,\d{3})+\b|\b(19|20)\d\d\b"
)


def visible_text(html: str) -> str:
    text = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text)


def token_block(css: str, opener: str) -> dict[str, str]:
    start = css.index(opener)
    body = css[css.index("{", start) + 1: css.index("}", start)]
    tokens = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body))
    if not tokens:
        raise AssertionError(f"no tokens found under {opener!r}")
    return tokens


LIGHT = token_block(CSS, ":root {")
DARK_MEDIA = token_block(CSS, ':root:not([data-theme="light"])')
DARK_ATTR = token_block(CSS, ':root[data-theme="dark"]')


def luminance(hex6: str) -> float:
    hex6 = hex6.lstrip("#")
    rgb = [int(hex6[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


class Tokens(unittest.TestCase):
    PAIRS = [
        ("--text", "--bg"), ("--text", "--surface"), ("--text", "--surface-2"),
        ("--text-muted", "--bg"), ("--text-muted", "--surface"), ("--text-muted", "--surface-2"),
        ("--link", "--bg"), ("--link", "--surface"),
        ("--on-accent", "--accent"), ("--accent", "--bg"), ("--accent", "--surface"),
        ("--accent", "--accent-soft"), ("--accent-hover", "--bg"),
    ]

    def test_dark_blocks_are_one_source_of_truth(self):
        self.assertEqual(DARK_MEDIA, DARK_ATTR)

    def test_every_rendered_pair_clears_aa_in_both_themes(self):
        for name, theme in (("light", LIGHT), ("dark", {**LIGHT, **DARK_ATTR})):
            for fg, bg in self.PAIRS:
                ratio = contrast(theme[fg], theme[bg])
                self.assertGreaterEqual(ratio, 4.5, f"{name}: {fg} on {bg} = {ratio:.2f}:1")

    def test_theme_color_meta_is_the_accent_token(self):
        meta = re.search(r'name="theme-color" content="([^"]+)"', HTML).group(1)
        self.assertEqual(meta, LIGHT["--accent"])

    def test_no_colour_literal_outside_the_token_blocks(self):
        rest = CSS
        for opener in (":root {", ':root:not([data-theme="light"])', ':root[data-theme="dark"]'):
            start = rest.index(opener)
            rest = rest[:start] + rest[rest.index("}", start) + 1:]
        self.assertFalse(re.search(r"#[0-9a-fA-F]{3,8}\b", rest), "hex colour outside :root")
        self.assertFalse(re.search(r"\brgba?\(", rest), "rgb() outside :root")
        markup = re.sub(r'<link rel="icon"[^>]*>', "", HTML)
        self.assertFalse(re.search(r'(fill|stroke|color)="#', markup), "colour attribute in markup")
        self.assertFalse(re.search(r'style="[^"]*#[0-9a-fA-F]{3,8}', markup), "hex in style attribute")

    def test_every_var_is_defined_and_every_token_is_used(self):
        used = set(re.findall(r"var\((--[\w-]+)\)", CSS))
        defined = set(LIGHT)
        self.assertEqual(used - defined, set(), "var() with no definition")
        unused = defined - used
        self.assertEqual(unused, set(), "defined but never referenced")
        for token in DARK_ATTR:
            self.assertIn(token, LIGHT, f"{token} only exists in dark")


class Markup(unittest.TestCase):
    def sections(self):
        return [m.groupdict() for m in SECTION_RE.finditer(HTML)]

    def test_sections_form_two_role_menus(self):
        secs = self.sections()
        self.assertGreaterEqual(len(secs), 10)
        self.assertEqual({s["role"] for s in secs}, ROLES)
        keys = [(s["role"], s["section"]) for s in secs]
        self.assertEqual(len(keys), len(set(keys)), "duplicate role/section")
        ids = [s["id"] for s in secs]
        self.assertEqual(len(ids), len(set(ids)))
        for s in secs:
            self.assertLessEqual(len(s["label"]), MAX_TAB_LABEL, s["label"])
            body = HTML[HTML.index(f'id="{s["id"]}"'):]
            body = body[:body.index("</section>")]
            self.assertEqual(body.count("<h2>"), 1, f'{s["id"]} needs exactly one h2')

    def test_js_roles_match_the_markup(self):
        js_roles = set(re.findall(r"(\w+): 'For ", JS))
        self.assertEqual(js_roles, ROLES)

    def test_internal_route_links_resolve(self):
        routes = {(s["role"], s["section"]) for s in self.sections()}
        for href in re.findall(r'href="#([\w-]+)(?:/([\w-]+))?"', HTML):
            role, section = href
            if role in ("", "main"):
                continue
            self.assertIn(role, ROLES, href)
            if section:
                self.assertIn((role, section), routes, href)

    def test_landmarks_and_skip_link(self):
        self.assertEqual(HTML.count("<h1>"), 1)
        self.assertLess(HTML.index('class="skip-link"'), HTML.index("<header"))
        for needle in ('role="banner"', 'role="main"', 'role="contentinfo"', 'aria-live="polite"'):
            self.assertIn(needle, HTML)

    def test_tabs_bar_and_hidden_rules_exist(self):
        self.assertIn('<div id="tabs"></div>', HTML)
        self.assertIn("[hidden] { display: none !important; }", CSS)
        self.assertIn("details.acc:not([open]) > :not(summary) { display: none; }", CSS)
        self.assertIn("@media (pointer: coarse)", CSS)
        self.assertIn("prefers-reduced-motion", CSS)

    def test_one_external_stylesheet_and_it_is_the_brand_font(self):
        links = re.findall(r'<link rel="stylesheet" href="(https?://[^"]+)"', HTML)
        self.assertEqual(len(links), 1)
        self.assertIn("Libre+Franklin", links[0])
        self.assertIn("display=swap", links[0])
        self.assertIn('rel="preconnect" href="https://fonts.gstatic.com"', HTML)
        self.assertIn('"Libre Franklin"', LIGHT["--font-sans"])

    def test_cache_busted_assets(self):
        self.assertRegex(HTML, r'href="styles\.css\?v=\d{8}"')
        self.assertRegex(HTML, r'src="app\.js\?v=\d{8}"')


class Copy(unittest.TestCase):
    def test_no_dashes_of_the_model_kind(self):
        for name, text in (("index.html", HTML), ("app.js", JS)):
            self.assertNotIn("—", text, f"em dash in {name}")
            self.assertNotIn("–", text, f"en dash in {name}; write 'to'")

    def test_no_register_words_in_shipped_text(self):
        text = visible_text(HTML).lower()
        for word in BANNED_WORDS:
            self.assertIsNone(re.search(r"\b" + re.escape(word) + r"\b", text), word)

    def test_no_emoji(self):
        self.assertIsNone(re.search(r"[\U0001F300-\U0001FAFF☀-➿]", HTML))

    def test_every_numeric_claim_carries_a_source_chip(self):
        blocks = re.findall(r"<(p|li|dd|td|figcaption)\b[^>]*>(.*?)</\1>", MAIN, flags=re.S)
        blocks += [("stat", b) for b in re.findall(r'<div class="stat">(.*?)</div>', MAIN, flags=re.S)]
        self.assertGreater(len(blocks), 60, "extractor found too little to check")
        checked = 0
        for tag, body in blocks:
            text = visible_text(body)
            if not NUMERIC_CLAIM.search(text):
                continue
            checked += 1
            self.assertIn('class="src"', body, f"<{tag}> has a number and no source: {text[:120]}")
        self.assertGreater(checked, 40, "the numeric-claim scan checked too few blocks")

    def test_source_chips_are_real_links(self):
        chips = re.findall(r'<a class="src" href="([^"]+)">([^<]*)</a>', HTML)
        self.assertGreater(len(chips), 50)
        for href, label in chips:
            self.assertRegex(href, r"^https://", href)
            self.assertTrue(label.strip(), href)


class Volumes(unittest.TestCase):
    def test_state_figures_on_the_page_come_from_the_data(self):
        spec = importlib.util.spec_from_file_location("nys_volumes", ROOT / "tools" / "nys_volumes.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        v = mod.volumes(json.loads(mod.DATA.read_text()))
        self.assertEqual(v["top_nyc_cabg_hospital"], mod.COLUMBIA_ROW)
        for key in ("statewide_cabg", "nyc_cabg", "columbia_cabg", "columbia_pci", "statewide_pci"):
            self.assertIn(f"<b>{v[key]:,}</b>", HTML, key)
        self.assertIn(f"across {v['nyc_cabg_hospitals']} hospitals", HTML)
        self.assertIn(f"{v['year']} discharges", HTML)


ROUTES = ["", "#patients", "#patients/candidates", "#patients/hybrid", "#patients/recovery",
          "#patients/questions", "#physicians", "#physicians/selection", "#physicians/hybrid",
          "#physicians/refer", "#physicians/technology", "#physicians/landscape"]


def _serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DOCS))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


class Layout(unittest.TestCase):
    """Drives the real page. Skips itself, visibly, when the browser is missing."""

    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as e:  # pragma: no cover
            raise unittest.SkipTest(f"playwright not importable: {e}")
        cls.pw = sync_playwright().start()
        try:
            cls.browser = cls.pw.chromium.launch()
        except Exception as e:  # pragma: no cover
            cls.pw.stop()
            raise unittest.SkipTest(f"chromium not launchable: {e}")
        cls.server = _serve()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}/"

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.shutdown()

    def _context(self, mobile: bool):
        if mobile:
            return self.browser.new_context(**self.pw.devices["iPhone 12"])
        return self.browser.new_context(viewport={"width": 1280, "height": 800})

    def _each_route(self, page):
        for i, route in enumerate(ROUTES):
            page.goto(f"{self.base}?i={i}{route}", wait_until="load")
            page.wait_for_function("document.documentElement.classList.contains('js')")
            yield route

    def test_no_horizontal_overflow_and_tabs_fit_at_every_width_and_route(self):
        for mobile in (True, False):
            ctx = self._context(mobile)
            page = ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            for route in self._each_route(page):
                m = page.evaluate("""() => {
                    const d = document.documentElement;
                    const list = document.querySelector('.tabs:not([hidden])');
                    const tabs = list ? [...list.querySelectorAll('.tab')] : [];
                    const last = tabs.length ? tabs[tabs.length - 1].getBoundingClientRect() : null;
                    const lr = list ? list.getBoundingClientRect() : null;
                    const panel = document.querySelector('section:not([hidden])');
                    return {cw: d.clientWidth, sw: d.scrollWidth,
                            listOverflow: list ? list.scrollWidth - list.clientWidth : 0,
                            lastFits: last ? (last.right <= lr.right + 0.5) : true,
                            tabs: tabs.length, panel: panel ? panel.id : null,
                            title: document.title};
                }""")
                self.assertGreater(m["cw"], 300, "viewport collapsed; measurement is garbage")
                self.assertLessEqual(m["sw"], m["cw"] + 1, f"{route} {'mobile' if mobile else 'desktop'} scrolls sideways")
                self.assertLessEqual(m["listOverflow"], 1, f"{route}: tab strip overflows")
                self.assertTrue(m["lastFits"], f"{route}: last tab clipped")
                if route:
                    self.assertGreaterEqual(m["tabs"], 5)
                    self.assertIsNotNone(m["panel"])
                    self.assertIn("·", m["title"])
                else:
                    self.assertEqual(m["panel"], "home")
            self.assertEqual(errors, [])
            ctx.close()

    def test_touch_targets_on_a_coarse_pointer(self):
        ctx = self._context(True)
        page = ctx.new_page()
        for route in self._each_route(page):
            if not route:
                continue
            heights = page.evaluate("""() => {
                const sel = '.tabs:not([hidden]) .tab, section:not([hidden]) .button, section:not([hidden]) details.acc > summary, .role-switch a';
                return [...document.querySelectorAll(sel)].map(el => {
                    const r = el.getBoundingClientRect();
                    return {h: r.height, w: r.width, what: el.className || el.tagName, text: el.textContent.trim().slice(0, 30)};
                });
            }""")
            self.assertGreater(len(heights), 4)
            for h in heights:
                self.assertGreaterEqual(h["h"], TOUCH_FLOOR, f"{route}: {h}")
        ctx.close()

    def test_desktop_button_is_not_bloated_by_the_touch_floor(self):
        """The coarse-pointer rule must be doing real work: on a fine pointer the summary row stays compact."""
        ctx = self._context(False)
        page = ctx.new_page()
        page.goto(f"{self.base}?i=fine#patients/questions", wait_until="load")
        h = page.evaluate("document.querySelector('section:not([hidden]) details.acc > summary').getBoundingClientRect().height")
        self.assertLess(h, TOUCH_FLOOR, "summary rows should be compact on desktop")
        ctx.close()

    def test_dark_theme_renders_tokens_from_the_dark_block(self):
        ctx = self.browser.new_context(viewport={"width": 1280, "height": 800}, color_scheme="dark")
        page = ctx.new_page()
        page.goto(f"{self.base}?i=dark#physicians", wait_until="load")
        bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
        r, g, b = (int(DARK_ATTR["--bg"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        self.assertEqual(bg, f"rgb({r}, {g}, {b})")
        ctx.close()


if __name__ == "__main__":
    unittest.main()
