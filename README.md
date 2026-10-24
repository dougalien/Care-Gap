# The Care Gap

An interactive page about the U.S. care maintenance gap. It shows how many people aged 45 to 64 there are for each person aged 80 and over, and lets you test ways the gap could be handled: immigration, a bigger paid care workforce, healthier aging, and robots and AI.

It accompanies the manuscript *When the Supports Run Out: Below-Replacement Fertility, the Falling Helper Ratio, and the U.S. Care Maintenance Gap* (Douglas E. Allen).

## Run it

Open `index.html` in any browser. It is one file of plain HTML, CSS and JavaScript, with no build step and no dependencies apart from Google Fonts. It also works as a GitHub Pages site.

## How the simulator works

The published helper ratio sets the pressure: each potential helper would need to give `7.2 / ratio` times the 2010 effort to provide the same care per person aged 80+ (1.76 times in 2030, 2.48 times in 2050).

Each slider is a multiplier on that, and the effects multiply:

| Slider | Effect |
| --- | --- |
| Immigration | more helpers: `× (1 + imm)` |
| Paid care workforce | more of each helper group's work goes to care: `× (1 + care)` |
| Healthier aging | fewer people aged 80+ need daily help: `÷ (1 − health)` |
| Robots and AI | machines do a share of care tasks, scaled by how much is safe to use unsupervised: `÷ (1 − capability × trust)` |

The result is care per person aged 80+ as a share of the 2010 level. The bar shows each choice's share of the gap, measured in log terms so the multiplied effects add up. The AI panel shows what share of all care work machines would have to do, safely, to close what the other choices leave open.

Slider positions and scenarios are assumptions to test. They are not forecasts.

## Sources

Every fixed number on the page comes from a published source:

- Helper ratio (6.6 in 1990, 7.2 in 2010, 4.1 in 2030, 2.9 in 2050): Redfoot, Feinberg & Houser, *The Aging of the Baby Boom and the Growing Care Gap*, AARP Public Policy Institute, 2013.
- Final 2024 total fertility rate, 1,599.5 per 1,000 women: NCHS, *Births: Final Data for 2024*, NVSR 75(2), 2026.
- Net international migration down 53.8% to 1.3 million: U.S. Census Bureau, release CB26-20, January 2026.
- Deaths exceed births from 2031: CBO, *An Update to the Demographic Outlook, 2025 to 2055*, September 2025.
- Prime-age participation 83.6%: BLS series LNS11300060.
- Foreign born 19.2% of the labor force (2024): BLS, *Foreign-Born Workers*, May 2025. 48.6% of labor-force growth 1996–2000: Mosisa, *Monthly Labor Review*, May 2002.
- Health care and social assistance 37% of new jobs 2025–2035: BLS Employment Projections, August 2026. Home health and personal care aides +18%: BLS *Occupational Outlook Handbook*.
- 52% of people turning 65 will need long-term care: Favreault & Dey, ASPE, 2016.
- Immigration about 3.5 times the current rate to restore the worker-to-retiree ratio: Gokhale, Penn Wharton Budget Model, 2024.
- AI risk categories: NIST AI 600-1 (2024), WHO guidance on large multimodal models (2024), OWASP Top 10 for LLM Applications 2025.

Links to each source are on the page.
