"""Quick checks on the Care Gap model. Run: python test_model.py"""

from model import PRESETS, run

nothing = run(PRESETS["Do nothing"], 2050)
assert abs(nothing["pressure"] - 7.2 / 2.9) < 1e-9
assert abs(nothing["coverage"] - 2.9 / 7.2) < 1e-9          # 40%
assert abs(nothing["ai_needed"] - (1 - 2.9 / 7.2)) < 1e-9   # 60%
assert abs(nothing["still_open"] - 1) < 1e-9

all_of = run(PRESETS["All of the above"], 2050)
assert round(all_of["coverage"], 2) == 0.78
assert round(all_of["ai_needed"], 2) == 0.31
assert abs(sum(all_of["shares"].values()) + all_of["still_open"] - 1) < 1e-9

assert run(PRESETS["Do nothing"], 2010)["coverage"] == 1
assert round(run(PRESETS["Do nothing"], 2030)["pressure"], 2) == 1.76

print("model checks passed")
