"""The Care Gap model: published helper ratio plus four multiplying choices.

Coverage is care per person aged 80+ as a share of the 2010 level. The fall
in the helper ratio sets the pressure (7.2 / ratio); each choice is a
multiplier that pushes back against it. Slider values are assumptions to
test, not forecasts. Only the helper ratios and the population figures are data.
"""

import math

# Potential family caregivers aged 45-64 per person aged 80+.
# Redfoot, Feinberg & Houser, AARP Public Policy Institute, 2013. Only these years are published.
RATIO = {1990: 6.6, 2010: 7.2, 2030: 4.1, 2050: 2.9}
PROJECTED = {2030, 2050}
BASE = RATIO[2010]

# The same ratio by state: AARP PPI 2013, Appendix B, "Caregiver Support Ratios by State, 1990-2050"
# (columns 1990, 2010, 2030, 2050). AARP advises against comparing states for 2030 or 2050.
_STATE_TABLE = {
    "Alabama": (6.8, 7.8, 3.9, 3.2),
    "Alaska": (26.2, 18.3, 5.3, 3.1),
    "Arizona": (6.8, 7.0, 2.6, 1.8),
    "Arkansas": (5.6, 7.0, 3.9, 3.2),
    "California": (7.6, 7.7, 4.4, 2.7),
    "Colorado": (8.0, 9.3, 4.5, 2.7),
    "Connecticut": (6.4, 6.3, 3.9, 2.8),
    "Delaware": (7.9, 7.4, 3.5, 2.8),
    "District of Columbia": (6.6, 7.0, 6.4, 4.0),
    "Florida": (4.9, 5.5, 2.9, 2.3),
    "Georgia": (8.5, 10.1, 4.8, 3.1),
    "Hawaii": (8.7, 6.1, 2.9, 2.1),
    "Idaho": (6.5, 7.6, 4.0, 3.0),
    "Illinois": (6.5, 7.1, 4.9, 3.3),
    "Indiana": (6.6, 7.2, 4.3, 3.2),
    "Iowa": (4.6, 5.6, 3.3, 2.3),
    "Kansas": (4.9, 6.3, 3.8, 2.7),
    "Kentucky": (6.7, 8.0, 4.1, 3.1),
    "Louisiana": (7.4, 8.3, 4.4, 3.4),
    "Maine": (5.9, 6.9, 3.4, 3.0),
    "Maryland": (8.6, 8.1, 4.2, 2.8),
    "Massachusetts": (5.6, 6.4, 4.4, 3.2),
    "Michigan": (7.3, 7.0, 4.1, 3.3),
    "Minnesota": (5.4, 6.9, 4.3, 2.7),
    "Mississippi": (6.2, 8.0, 4.1, 3.3),
    "Missouri": (5.4, 6.9, 3.8, 2.9),
    "Montana": (6.2, 7.1, 3.5, 2.9),
    "Nebraska": (4.6, 6.1, 4.1, 2.8),
    "Nevada": (12.4, 10.0, 3.4, 2.0),
    "New Hampshire": (6.8, 8.1, 3.8, 2.9),
    "New Jersey": (7.1, 6.8, 4.3, 2.9),
    "New Mexico": (8.0, 8.0, 3.2, 2.5),
    "New York": (6.5, 6.6, 4.8, 3.5),
    "North Carolina": (7.7, 8.0, 3.9, 2.7),
    "North Dakota": (4.5, 5.5, 4.2, 3.0),
    "Ohio": (6.8, 6.7, 4.0, 3.3),
    "Oklahoma": (5.8, 7.4, 3.8, 3.1),
    "Oregon": (6.0, 6.9, 3.9, 2.8),
    "Pennsylvania": (6.0, 5.8, 3.9, 3.3),
    "Rhode Island": (5.3, 5.7, 3.9, 3.0),
    "South Carolina": (8.6, 8.3, 3.6, 2.9),
    "South Dakota": (4.4, 5.8, 3.9, 2.9),
    "Tennessee": (6.9, 8.1, 4.1, 3.2),
    "Texas": (7.6, 9.2, 4.8, 3.0),
    "Utah": (7.6, 8.3, 5.8, 3.4),
    "Vermont": (6.3, 7.5, 3.4, 2.9),
    "Virginia": (8.4, 8.5, 4.2, 2.8),
    "Washington": (6.9, 7.9, 4.4, 2.8),
    "West Virginia": (6.2, 6.8, 3.4, 3.1),
    "Wisconsin": (5.5, 6.7, 4.0, 2.9),
    "Wyoming": (7.8, 8.7, 3.9, 2.6),
}
PLACES = {"United States": RATIO,
          **{name: dict(zip(RATIO, values)) for name, values in _STATE_TABLE.items()}}

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


def run(s, year, place="United States"):
    """Coverage, each choice's share of the gap, and what machines would have to do.

    The baseline is the place's own 2010 ratio, so a state is measured against itself.
    """
    ratio = PLACES[place]
    pressure = ratio[2010] / ratio[year]
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


# U.S. total population, millions. Estimate: Census Bureau, Vintage 2025 (release CB26-20, Jan 2026).
# Projections: Census Bureau 2023 National Population Projections (release, Nov 2023), by immigration scenario.
POP_2025 = 341.8
POP_2100 = {"High immigration": 435, "Middle series": 366, "Low immigration": 319, "Zero immigration": 226}
POP_PEAK = {"Middle series": (2080, 370), "Low immigration": (2043, 346)}

# State population shifts, as published (no state figures beyond these are used)
GREW_FASTEST_2025 = {"South Carolina": "1.5%", "Idaho": "1.4%", "North Carolina": "1.3%", "Texas": "1.2%", "Utah": "1.0%"}
LOST_2025 = {"California", "Hawaii", "New Mexico", "Vermont", "West Virginia"}
FASTEST_TO_2050 = {"Utah", "Idaho", "Texas"}                      # Weldon Cooper Center, 2024 vintage
DECLINING_TO_2050 = {"West Virginia", "Mississippi", "Illinois"}  # Weldon Cooper Center, 2024 vintage
