"""The Care Gap model: published helper ratio plus four multiplying choices.

Coverage is care per person aged 80+ as a share of the 2010 level. The fall
in the helper ratio sets the pressure (7.2 / ratio); each choice is a
multiplier that pushes back against it. Slider values are assumptions to
test, not forecasts. Only the helper ratio is data.
"""

import math

# Potential family caregivers aged 45-64 per person aged 80+.
# Redfoot, Feinberg & Houser, AARP Public Policy Institute, 2013. Only these years are published.
RATIO = {1990: 6.6, 2010: 7.2, 2030: 4.1, 2050: 2.9}
PROJECTED = {2030, 2050}
BASE = RATIO[2010]

LEVERS = ("imm", "care", "health", "tech", "trust")

PRESETS = {
    "Do nothing": dict(imm=0, care=0, health=0, tech=0, trust=0),
    "Lean on immigration": dict(imm=20, care=0, health=0, tech=0, trust=0),
    "Grow paid care": dict(imm=0, care=14, health=0, tech=0, trust=0),
    "Healthier aging": dict(imm=0, care=0, health=20, tech=0, trust=0),
    "Bet on technology": dict(imm=0, care=0, health=0, tech=40, trust=30),
    "All of the above": dict(imm=20, care=14, health=20, tech=40, trust=30),
}


def multipliers(s):
    """Each choice's multiplier on care per person aged 80+ (slider values in percent)."""
    return {
        "imm": 1 + s["imm"] / 100,
        "care": 1 + s["care"] / 100,
        "health": 1 / (1 - s["health"] / 100),
        "tech": 1 / (1 - (s["tech"] / 100) * (s["trust"] / 100)),
    }


def run(s, year):
    """Coverage, each choice's share of the gap, and what machines would have to do."""
    pressure = BASE / RATIO[year]
    f = multipliers(s)
    coverage = f["imm"] * f["care"] * f["health"] * f["tech"] / pressure
    gap = math.log(pressure)
    # Shares in log terms, so the multiplied effects add up to the whole gap
    shares = {k: (math.log(v) / gap if gap > 0 else 0.0) for k, v in f.items()}
    without_tech = f["imm"] * f["care"] * f["health"] / pressure
    return {
        "pressure": pressure,
        "coverage": coverage,
        "shares": shares,
        "still_open": max(0.0, 1 - sum(shares.values())) if gap > 0 else 0.0,
        "ai_needed": max(0.0, 1 - without_tech),
        "effort": 1 / coverage,
        "unmet": max(0.0, 1 - coverage),
    }
