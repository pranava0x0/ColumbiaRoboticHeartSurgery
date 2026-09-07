# design.md: Robotic Coronary Bypass at Columbia

Extends the base [DESIGN.md](../DESIGN.md). This file carries the specific identity; the base carries the rules it must respect. Project wins on conflict.

## Identity in one line

A program microsite in the visual language of its parent, columbiasurgery.org: Columbia blue on white, Libre Franklin, hairline rules. One memorable move: the deep-blue masthead with a segmented audience switch (Patients | Physicians), and the three-chest incision diagram on the landing page that shows in one glance what "robotic" changes.

## Palette (from the parent site's CSS, checked 2026-09-07)

| Token | Light | Dark | Where it came from |
|---|---|---|---|
| `--accent` | `#13407b` | `#8ec2ee` | the most-used colour in columbiasurgery.org's theme CSS (39 uses) |
| `--accent-hover` | `#072143` | `#b9dcf8` | the parent's button hover colour |
| `--link` | `#0071b3` | `#9dcbf3` | the parent's `a { color }` |
| `--bg` / `--surface` | white / `#f4f6f9` | `#0b1829` / `#132539` | dark ground derived from the parent's `#072143` navy |

Every text/background pair the page renders is asserted at 4.5:1 or better in both themes by `tests/test_site.py`. The bright brand blue `#0077c8` from the parent site measures 4.4:1 on the light surface, so it is not used for text.

## Type

Libre Franklin 400 / 600 / 800, the parent site's face, loaded from Google Fonts with `display=swap` and a Franklin Gothic / Helvetica fallback stack. This is the one sanctioned web font in the project; the brief asked for Columbia's own type. The parent also uses ITC Giovanni Bold for a few headings; it is a commercial face and is not loaded.

Headings and display numbers: 800. Sub-headings, buttons, tab labels: 600. Body: 400 at 16px / 1.55. Tabular numerals on `:root`.

## Structure

- Two audiences, one page. The landing shows the two doors and the diagram; the masthead switch moves between versions from anywhere.
- Hash routes (`#patients/recovery`, `#physicians/refer`). Each `<section data-role data-section data-label>` in `docs/index.html` becomes a tab, in document order; `app.js` builds the tablists from those attributes, so adding a section is one edit.
- One panel per screen. Depth goes behind `<details>`; must-read facts stay in the open (the stay, the recovery time, the phone number).
- Tabs sit under the masthead on desktop and become a fixed bottom bar on phones. Labels are capped at 11 characters so six fit across 375px; the test enforces the cap.
- Radii 4 to 6px, hairline borders, no shadows on cards. The page should read as a hospital's own publication, not a start-up landing page.

## Copy rules specific to this site

- Every number carries a source chip (`<a class="src">`) naming the destination it links to. The test fails on a numeric claim without one.
- Columbia's own patient guide gives two hospital-stay figures ("3-4 days" in the body, "2 or 3 days" in the FAQ). The page says "2 to 4 days" so it contradicts neither.
- New York State volumes derive from `data/nys_doh_jtip-2ccj_2019.json` through `tools/nys_volumes.py`; the test asserts the page shows what the script computes.
- The named surgeon is Sameer Singh, MD, verified against columbiasurgery.org/sameer-singh-md on 2026-09-07. Surgeons at other centres are not named.
- Program plans that have no external source (the stabilizer expected within one to two years, the TECAB timeline, the referral-workflow commitments) are attributed to the program or to Dr. Singh in the text, never stated as external fact.
- No em dashes, no register words, no eyebrow labels, no emoji.

## Not in this design, on purpose

No logo image (trademark; the wordmark is text), no photographs yet, no icon set, no analytics, no backend, no form of its own (Columbia's Qualtrics request form is linked instead).
