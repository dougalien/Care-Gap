"""Where the workers come from: a ledger of new workers by sector, 2025-2035.

Every number is read from the published BLS and Census tables in data/ (see
data/SOURCES.md). The only model step is accounting: each sector needs new
workers to cover its growth and the workers who leave the labor force, and
extra care workers have to come from new supply or out of other sectors.
Occupational transfers are moves inside the pool, so they are not counted.
All figures are in thousands of workers.
"""

import csv
from pathlib import Path

DATA = Path(__file__).parent / "data"
YEARS = 10  # 2025 to 2035

# App sector -> BLS major occupation groups (SOC)
SECTORS = {
    "aides": ("Care: aides and support", ["31-0000"]),
    "clinical": ("Care: nurses and clinicians", ["29-0000"]),
    "construction": ("Construction and infrastructure", ["47-0000"]),
    "repair": ("Repair and utilities", ["49-0000"]),
    "transport": ("Transportation", ["53-0000"]),
    "manufacturing": ("Manufacturing", ["51-0000"]),
    "agriculture": ("Agriculture", ["45-0000"]),
    "education": ("Education", ["25-0000"]),
    "safety": ("Public safety", ["33-0000"]),
    "other": ("Everything else", None),  # every group not named above
}
CARE = ("aides", "clinical")


def _read(name):
    with open(DATA / name, newline="") as f:
        return list(csv.DictReader(f))


def load():
    """Sector totals from BLS Table 1.10 and the Census 80+ projection."""
    groups = {r["soc"]: r for r in _read("bls_ep_table_1_10.csv") if r["soc"] != "00-0000"}
    named = {soc for _, socs in SECTORS.values() if socs for soc in socs}
    out = {}
    for key, (label, socs) in SECTORS.items():
        rows = [groups[s] for s in (socs or [s for s in groups if s not in named])]
        emp_2025 = sum(float(r["emp_2025"]) for r in rows)
        emp_2035 = sum(float(r["emp_2035"]) for r in rows)
        exits = sum(float(r["exits_per_year"]) for r in rows)
        out[key] = {
            "label": label,
            "emp_2025": emp_2025,
            "emp_2035": emp_2035,
            "exits_per_year": exits,
            "openings_per_year": sum(float(r["openings_per_year"]) for r in rows),
            # New workers the sector needs over the decade: its growth plus replacing those who leave
            "entrants": (emp_2035 - emp_2025) + YEARS * exits,
        }
    pop80 = {int(r["year"]): int(r["age_80_plus"]) for r in _read("census_np2023_t3_80plus.csv")}
    return out, pop80


SECTOR_DATA, POP80 = load()
LABOR_FORCE_2035 = next(float(r["lf_2035"]) for r in _read("bls_ep_table_3_1.csv") if r["age"] == "16 and older")
GROWTH_80 = POP80[2035] / POP80[2025]
DONORS = [k for k in SECTORS if k not in CARE]


def default_weights():
    """Proportional draw: each other sector gives up workers in line with its share of new workers needed."""
    total = sum(SECTOR_DATA[k]["entrants"] for k in DONORS)
    return {k: SECTOR_DATA[k]["entrants"] / total for k in DONORS}


def extra_care(include_clinical=False):
    """Care workers needed in 2035 above the BLS projection, if care keeps pace with the 80+ population."""
    keys = CARE if include_clinical else ("aides",)
    return sum(max(0.0, SECTOR_DATA[k]["emp_2025"] * GROWTH_80 - SECTOR_DATA[k]["emp_2035"]) for k in keys)


def run(keep_pace=True, include_clinical=False, new_supply=0.0, weights=None):
    """Gaps by sector in 2035.

    keep_pace: False uses the BLS care projection (no extra need, no gaps).
    new_supply: share (0-1) of the extra care workers who come from added labor supply.
    weights: share of the draw each non-care sector gives up; defaults to proportional.
    """
    extra = extra_care(include_clinical) if keep_pace else 0.0
    supply = extra * new_supply
    draw = extra - supply
    w = weights or default_weights()
    total_w = sum(max(0.0, w.get(k, 0.0)) for k in DONORS)
    gaps = {}
    for k in DONORS:
        taken = draw * max(0.0, w.get(k, 0.0)) / total_w if total_w > 0 else 0.0
        d = SECTOR_DATA[k]
        gaps[k] = {"taken": taken, "share_of_jobs": taken / d["emp_2035"], "share_of_entrants": taken / d["entrants"]}
    worst = max(gaps, key=lambda k: gaps[k]["share_of_jobs"]) if draw > 0 else None
    return {
        "extra": extra,
        "supply": supply,
        "supply_share_of_lf": supply / LABOR_FORCE_2035,
        "draw": draw,
        "gaps": gaps,
        "worst": worst,
    }
