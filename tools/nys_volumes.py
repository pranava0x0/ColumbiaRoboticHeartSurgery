#!/usr/bin/env python3
"""Derive the New York State coronary volumes the site quotes from the raw DOH export.

Source: NYS Department of Health, "Cardiac Surgery and Percutaneous Coronary
Interventions by Hospital: Beginning 2008" (dataset jtip-2ccj on
health.data.ny.gov, updated 2025-03-07). data/nys_doh_jtip-2ccj_2019.json is the
API response for year_of_hospital_discharge=2019, the latest year in the dataset
on 2026-09-07. Fetch a fresh copy with:

    curl -s 'https://health.data.ny.gov/resource/jtip-2ccj.json?year_of_hospital_discharge=2019&$limit=5000'

The test suite runs this module and asserts the figures it prints appear in
docs/index.html, so the page cannot drift from the data without failing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "nys_doh_jtip-2ccj_2019.json"
STATEWIDE_ROW = "NYS - All Hospitals"
COLUMBIA_ROW = "NYP Columbia Presby."
NYC_REGION = "NY Metro - NYC"


def volumes(rows: list[dict]) -> dict:
    """Return the figures the page quotes, derived from the raw rows."""
    year = {r["year_of_hospital_discharge"] for r in rows}
    if year != {"2019"}:
        raise SystemExit(f"expected only 2019 rows, got {sorted(year)}")
    hospitals = [r for r in rows if r["hospital_name"] != STATEWIDE_ROW]
    cabg = [r for r in hospitals if r["procedure"] == "CABG"]
    nyc_cabg = [r for r in cabg if r["region"] == NYC_REGION]
    if not nyc_cabg:
        raise SystemExit("no NYC CABG rows: region label changed?")

    def one(name: str, procedure: str) -> int:
        hits = [r for r in rows if r["hospital_name"] == name and r["procedure"] == procedure]
        if len(hits) != 1:
            raise SystemExit(f"expected exactly one {procedure} row for {name!r}, got {len(hits)}")
        return int(hits[0]["number_of_cases"])

    top_nyc = max(nyc_cabg, key=lambda r: int(r["number_of_cases"]))
    return {
        "year": 2019,
        "statewide_cabg": one(STATEWIDE_ROW, "CABG"),
        "statewide_pci": one(STATEWIDE_ROW, "All PCI"),
        "nyc_cabg": sum(int(r["number_of_cases"]) for r in nyc_cabg),
        "nyc_cabg_hospitals": len(nyc_cabg),
        "columbia_cabg": one(COLUMBIA_ROW, "CABG"),
        "columbia_pci": one(COLUMBIA_ROW, "All PCI"),
        "top_nyc_cabg_hospital": top_nyc["hospital_name"],
    }


def main() -> int:
    rows = json.loads(DATA.read_text())
    v = volumes(rows)
    for key, value in v.items():
        print(f"{key}: {value:,}" if isinstance(value, int) else f"{key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
