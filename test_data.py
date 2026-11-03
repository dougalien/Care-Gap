"""Checks that the copied BLS tables agree with each other. Run: python test_data.py"""

import csv
from pathlib import Path

DATA = Path(__file__).parent / "data"


def rows(name):
    with open(DATA / name, newline="") as f:
        return {r["soc"] if "soc" in r else r["age"]: r for r in csv.DictReader(f)}


t11 = rows("bls_ep_table_1_1.csv")
total = t11.pop("00-0000")
assert len(t11) == 22
for year in ("emp_2025", "emp_2035"):
    groups = sum(float(r[year]) for r in t11.values())
    assert abs(groups - float(total[year])) < 1.0, (year, groups)   # BLS rounds each row
for r in t11.values():
    assert abs(float(r["emp_2035"]) - float(r["emp_2025"]) - float(r["change"])) < 0.15, r["soc"]

# Table 1.10 employment must match Table 1.1 for every group it has
t110 = rows("bls_ep_table_1_10.csv")
for soc, r in t110.items():
    ref = total if soc == "00-0000" else t11[soc]
    assert r["emp_2025"] == ref["emp_2025"] and r["emp_2035"] == ref["emp_2035"], soc

# Labor force age groups add to the total
t31 = rows("bls_ep_table_3_1.csv")
lf_total = t31.pop("16 and older")
for year in ("lf_2015", "lf_2025", "lf_2035"):
    assert sum(int(r[year]) for r in t31.values()) == int(lf_total[year]), year

print("data checks passed")
