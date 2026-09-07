# Robotic Coronary Bypass at Columbia

A two-audience microsite for the robotic and minimally invasive coronary bypass program at NewYork-Presbyterian/Columbia (Sameer Singh, MD): one version for patients and families, one for referring physicians and interventional cardiologists. Static HTML, CSS and vanilla JS in `docs/`; no build step.

## Run it

```bash
python3 -m http.server 8761 --directory docs
```

Then open http://localhost:8761. In Claude Code, `/run` uses the same server (`.claude/launch.json`, name `site`). Opening `docs/index.html` straight from Finder also works.

Routes: `#patients`, `#patients/candidates`, `#patients/hybrid`, `#patients/recovery`, `#patients/questions`, `#physicians`, `#physicians/selection`, `#physicians/hybrid`, `#physicians/refer`, `#physicians/technology`, `#physicians/landscape`.

## Test it

```bash
python3 -m unittest discover -s tests -v
```

Static checks: token contrast in both themes, no colour literals outside the token blocks, every `var()` defined and every token used, tab labels within the bottom-bar budget, every route link resolves, no em dashes or register words, every numeric claim carries a source chip, and the New York State figures on the page match `tools/nys_volumes.py`. Layout checks drive the page in headless Chromium (Playwright) at phone and desktop widths and skip, visibly, if the browser is missing.

Prose and design gates from the base rulebook:

```bash
python3 ~/Projects/coding-best-practices/tools/slopcheck.py --fail-on WARN .
python3 ~/Projects/coding-best-practices/tools/designcheck.py --fail-on WARN .
```

HTML validity, once per change:

```bash
curl -s -H "Content-Type: text/html; charset=utf-8" --data-binary @docs/index.html "https://validator.w3.org/nu/?out=json"
```

## Where the brief landed

| From the 2026-09-07 conversation | On the site |
|---|---|
| Market to patients: what they search for, faster recovery, who qualifies | Patients: Overview, Candidates, Recovery, Questions |
| Market to cardiologists; interventional cardiology buy-in for the hybrid program | Physicians: Hybrid (the shared pathway), Refer |
| Indications: isolated LAD, multi-arterial, hybrid with staged PCI | Physicians: Selection; Patients: Candidates |
| Da Vinci today, Medtronic stabilizer, Intuitive's expected robotic stabilizer, TECAB in one to two years with outside training | Physicians: Technology |
| Market opportunity in New York City; other programs in New York and New Jersey; partnership criteria | Physicians: Landscape |
| Offering robotic grows the whole program, including traditional CABG | Physicians: Refer; Patients: Candidates |

## Data

`data/nys_doh_jtip-2ccj_2019.json` is the New York State Department of Health "Cardiac Surgery and PCI by Hospital" export for 2019 discharges, the latest year in the dataset when it was updated on 2025-03-07. `python3 tools/nys_volumes.py` prints the figures the page quotes. To refresh, re-run the `curl` in that file's docstring and check whether a newer year has appeared.

## Before publishing

- Confirm with Dr. Singh the two statements attributed to him or the program without an external source: the robotic stabilizer expected within one to two years, and the TECAB training timeline.
- Confirm the referral commitments on the Physicians > Refer tab (written recommendation, sequence proposal, follow-up returning to the referring cardiologist). They are proposed defaults, not verified office workflow.
- Confirm the phone numbers: program line (212) 305-8312 and Dr. Singh's office 212-305-5156 were read from columbiasurgery.org on 2026-09-07.
- The footer credits the site builder; remove that line if the program prefers.
- Deploy: GitHub Pages serving `docs/` works as-is. The project is not yet a git repository.

## Layout

```
docs/          the site (index.html, styles.css, app.js)
site/design.md the visual identity and copy rules for this project
tests/         static and Playwright gates
tools/         nys_volumes.py derives the state figures from data/
data/          raw NYS DOH export
```

Base rulebooks (`CLAUDE.md`, `DESIGN.md`, `TESTING.md` and companions) are seeded from `~/Projects/coding-best-practices`; the project section at the end of `CLAUDE.md` holds what is specific here.
