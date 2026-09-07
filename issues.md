# issues.md

| Date | Area | Description | Root cause | Status |
|---|---|---|---|---|
| 2026-09-07 | HTML validity | First W3C Nu run: favicon data URI contained raw spaces (invalid `href`); three `<div aria-label>` without a role, which assistive tech ignores. | Code bug (authoring). | Fixed: URI percent-encoded; `role="group"` added to the stat strips. Three remaining "role is unnecessary" notes are informational and kept on purpose (DESIGN.md §9). |
| 2026-09-07 | Copy | slopcheck first run: 6 sentences over 30 words, a colon-setup heading, a comma-tail heading, a vague "studies show" heading, one comparative-superlative. | Authoring. | Fixed by rewriting; no allowlist entries. |
