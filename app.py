"""The Care Gap: who will care for Americans aged 80 and over?

Shows the published fall in the helper ratio (people aged 45-64 per person
aged 80+) and lets you test how the gap could be handled: immigration, a
bigger paid care workforce, healthier aging, and robots and AI. The math is
in model.py; every fixed number is from a published source.

Run: streamlit run app.py
"""

import plotly.graph_objects as go
import streamlit as st

import dougalien_brand as brand
from model import (DECLINING_TO_2050, FASTEST_TO_2050, GREW_FASTEST_2025, LOST_2025, PLACES, POP_2025,
                   POP_2100, POP_PEAK, PRESETS, PROJECTED, RATIO, run)

PLOT_CFG = {"displaylogo": False, "toImageButtonOptions": {"format": "png", "scale": 3}}
COLORS = {"imm": brand.SLATE, "care": brand.RUST, "health": brand.SAND, "tech": brand.CAPTION}
NAMES = {"imm": "Immigration", "care": "Paid care workforce", "health": "Healthier aging", "tech": "Robots and AI"}

SLIDERS = [
    ("imm", "More helpers through immigration (%)", 30, 1,
     "Share more people aged 45–64 than projected.",
     "For scale: the foreign born are 19.2% of the labor force "
     "([BLS](https://www.bls.gov/news.release/archives/forbrn_05202025.htm)). Penn Wharton estimates about 3.5 times "
     "today's immigration would be needed to restore the worker-to-retiree ratio "
     "([PWBM](https://budgetmodel.wharton.upenn.edu/issues/2024/3/22/us-demographic-projections-with-and-without-immigration))."),
    ("care", "Bigger paid care workforce (%)", 100, 1,
     "Share more of each helper group's work goes to care.",
     "For scale: BLS projects home health and personal care aides growing 18% by 2035 against 3.5% for all jobs, "
     "a 14% rise in their share ([OOH](https://www.bls.gov/ooh/healthcare/home-health-aides-and-personal-care-aides.htm), "
     "[projections](https://www.bls.gov/news.release/archives/ecopro_08272026.htm)). Every care worker added leaves another sector."),
    ("health", "Healthier aging (%)", 40, 1,
     "Share fewer people aged 80+ need daily help.",
     "For scale: 52% of Americans turning 65 will need long-term care, for about two years on average "
     "([ASPE](https://aspe.hhs.gov/basic-report/long-term-services-and-supports-older-americans-risks-and-financing-research-brief))."),
    ("tech", "Robots and AI: what they can do (%)", 60, 1,
     "Share of care tasks machines can do.",
     "Long-term care need is defined by hands-on help with bathing, dressing and moving "
     "([ASPE](https://aspe.hhs.gov/basic-report/long-term-services-and-supports-older-americans-risks-and-financing-research-brief)). "
     "Robots are least developed for this work."),
    ("trust", "Robots and AI: how much is safe to use (%)", 100, 5,
     "Share of that capability usable without close supervision.",
     "NIST, WHO and OWASP document confabulation, privacy and security risks that keep nominal AI capability "
     "from counting as usable capacity ([NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1))."),
]

FACTS = [
    ("1.60", "births per woman in 2024, a record low. Replacement is about 2.1.",
     "[NCHS, Births: Final Data for 2024](https://www.cdc.gov/nchs/data/nvsr/nvsr75/nvsr75-02.pdf)"),
    ("−53.8%", "drop in net international migration, to 1.3 million, in the year to July 2025.",
     "[U.S. Census Bureau, Jan 2026](https://www.census.gov/newsroom/press-releases/2026/population-growth-slows.html)"),
    ("2031", "the year deaths are projected to start exceeding births.",
     "[CBO, Sept 2025](https://www.cbo.gov/publication/61735)"),
    ("83.6%", "of people aged 25–54 were in the labor force in 2025, close to the record. There is little room left to rise.",
     "[BLS LNS11300060](https://fred.stlouisfed.org/series/LNS11300060)"),
    ("37%", "of all new jobs projected for 2025–2035 are in health care and social assistance, which has about 14% of jobs today.",
     "[BLS Employment Projections](https://www.bls.gov/news.release/archives/ecopro_08272026.htm)"),
    ("48.6%", "of labor-force growth from 1996 to 2000 came from foreign-born workers.",
     "[BLS Monthly Labor Review, 2002](https://www.bls.gov/opub/mlr/2002/05/art1full.pdf)"),
]

st.set_page_config(page_title="The Care Gap", layout="wide", page_icon=brand.page_icon("🪨"))
brand.apply_branding()

# Sliders start at "Do nothing"; picking a scenario moves them, moving a slider marks the scenario "Custom"
for key, value in PRESETS["Do nothing"].items():
    st.session_state.setdefault(key, value)
st.session_state.setdefault("scenario", "Do nothing")


def _apply_scenario():
    if st.session_state.scenario in PRESETS:
        st.session_state.update(PRESETS[st.session_state.scenario])


def _mark_custom():
    s = {k: st.session_state[k] for k in PRESETS["Do nothing"]}
    st.session_state.scenario = next((n for n, p in PRESETS.items() if p == s), "Custom")


with st.sidebar:
    st.header("1 · Place and year")
    place = st.selectbox("Place", list(PLACES), help="Every state's ratio is from the same AARP report.")
    year = st.radio("Year", list(RATIO), index=3, horizontal=True, label_visibility="collapsed",
                    format_func=lambda y: f"{y} (proj.)" if y in PROJECTED else str(y))
    st.header("2 · How the gap is handled")
    st.selectbox("Scenario", [*PRESETS, "Custom"], key="scenario", on_change=_apply_scenario)
    for key, label, top, step, help_text, anchor in SLIDERS:
        st.slider(label, 0, top, step=step, key=key, help=help_text, on_change=_mark_custom)
        st.caption(anchor)

s = {k: st.session_state[k] for k in PRESETS["Do nothing"]}
r = run(s, year, place)
ratio = PLACES[place]
where = "" if place == "United States" else f" in {'the ' if place.startswith('District') else ''}{place}"

st.title("The Care Gap")
st.markdown(
    "Fewer births and longer lives mean fewer people of working age for each American who needs daily care. "
    "This app shows the published fall in potential family helpers and lets you test the ways the gap could be handled."
)

tab_gap, tab_pop, tab_why, tab_method = st.tabs(
    ["The gap", "Isn't the population still growing?", "Why the old answers are running out", "Method and sources"])

with tab_gap:
    left, right = st.columns([1, 1.15], gap="large")

    with left:
        st.subheader("The helper ratio")
        st.metric(f"People aged 45–64 per person aged 80+{where}, {year}", f"{ratio[year]:.1f}",
                  delta=None if year == 2010 else f"{ratio[year] - ratio[2010]:+.1f} vs 2010", delta_color="normal")
        years = list(RATIO)
        fig = go.Figure()
        if place != "United States":
            fig.add_scatter(x=years, y=[RATIO[y] for y in years], mode="lines", name="United States",
                            line=dict(color=brand.MUTED, width=1.5, dash="dot"),
                            hovertemplate="United States %{x}: %{y}<extra></extra>")
        fig.add_scatter(x=years[:2], y=[ratio[y] for y in years[:2]], mode="lines",
                        line=dict(color=brand.SLATE, width=3), name="Estimated", hoverinfo="skip")
        fig.add_scatter(x=years[1:], y=[ratio[y] for y in years[1:]], mode="lines",
                        line=dict(color=brand.SLATE, width=3, dash="dash"), name="Projected", hoverinfo="skip")
        fig.add_scatter(x=years, y=[ratio[y] for y in years], mode="markers+text", showlegend=False,
                        text=[f"{ratio[y]}" for y in years], textposition="top center",
                        marker=dict(size=[16 if y == year else 9 for y in years],
                                    color=[brand.RUST if y == year else brand.SLATE for y in years],
                                    line=dict(color=brand.SHEET, width=2)),
                        hovertemplate="%{x}: %{y} helpers<extra></extra>")
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor=brand.SHEET,
                          paper_bgcolor=brand.PAPER, legend=dict(orientation="h", y=-0.15))
        fig.update_xaxes(tickvals=years, showgrid=False)
        fig.update_yaxes(range=[0, max(8.5, max(ratio.values()) * 1.15)], gridcolor=brand.RULE,
                         title="Helpers per person aged 80+")
        st.plotly_chart(fig, width="stretch", config=PLOT_CFG)
        if year == 2010:
            st.caption("2010 is the baseline year.")
        else:
            st.caption(f"Each potential helper would need to give {r['pressure']:.2f} times the 2010 effort "
                       f"for the same care per person aged 80+{where}.")
        st.caption("Source: Redfoot, Feinberg & Houser, *The Aging of the Baby Boom and the Growing Care Gap*, "
                   "AARP Public Policy Institute, 2013 ([PDF](https://www.caregiver.org/uploads/2023/02/"
                   "baby-boom-and-the-growing-care-gap-insight-AARP-ppi-ltc.pdf)). Only these four years are published.")
        if place != "United States":
            st.caption("State figures are from the report's Appendix B. AARP advises against comparing states "
                       "for 2030 or 2050, so each state is measured against its own 2010 level.")

    with right:
        st.subheader("How could the gap be handled?")
        if year <= 2010:
            st.info("No gap to close yet. Choose 2030 or 2050 in the sidebar.")
        else:
            closed = r["coverage"] >= 0.995
            st.metric(f"Care per person aged 80+{where} in {year}, compared with 2010",
                      f"{min(r['coverage'], 9.99):.0%}",
                      delta="Gap closed" if closed else f"-{r['unmet']:.0%}: short of the 2010 level",
                      delta_color="normal")

            # Each choice's share of the gap, stacked to 100%
            bar = go.Figure()
            used = 0.0
            for k in ("imm", "care", "health", "tech"):
                share = max(0.0, min(r["shares"][k], 1 - used))
                used += share
                bar.add_bar(x=[share], y=[""], orientation="h", name=f"{NAMES[k]} {r['shares'][k]:.0%}",
                            marker_color=COLORS[k], hovertemplate=f"{NAMES[k]}: %{{x:.0%}}<extra></extra>")
            bar.add_bar(x=[max(0.0, 1 - used)], y=[""], orientation="h", name=f"Still open {max(0.0, 1 - used):.0%}",
                        marker=dict(color=brand.SAND_TINT, line=dict(color=brand.RUST, width=1.5)),
                        hovertemplate="Still open: %{x:.0%}<extra></extra>")
            bar.update_layout(barmode="stack", height=190, margin=dict(l=10, r=10, t=30, b=10),
                              paper_bgcolor=brand.PAPER, plot_bgcolor=brand.PAPER,
                              title=dict(text="Share of the gap each choice closes", font=dict(size=14)),
                              legend=dict(orientation="h", y=-0.05, traceorder="normal"))
            bar.update_xaxes(range=[0, 1], visible=False)
            bar.update_yaxes(visible=False)
            st.plotly_chart(bar, width="stretch", config=PLOT_CFG)

            c1, c2 = st.columns(2)
            if closed:
                st.success("Nothing left: no extra load falls on families and no care goes undone.")
            else:
                c1.metric("Effort from each helper", f"{r['effort']:.2f}×",
                          help="Times the 2010 effort, if families make up the difference.")
                c2.metric("Care that goes undone", f"{r['unmet']:.0%}", help="If nobody makes up the difference.")

            st.markdown("#### What robots and AI would have to do")
            if r["ai_needed"] == 0:
                st.write("The other choices close the gap without them.")
            else:
                st.metric(f"Share of all care work in {year} machines would have to do", f"{r['ai_needed']:.0%}")
                st.write(
                    "That is the share machines would have to do, safely and without close supervision, to close "
                    "what the other choices leave open. The two technology sliders set how much they actually do. "
                    "Today that capacity has not been shown: most of the need is hands-on help with bathing, "
                    "dressing and moving, and the AI risk standards linked under the sliders say nominal capability "
                    "should not be counted as usable capacity. Whether that changes is open."
                )
    st.caption("Slider positions and scenarios are assumptions to test. They are not forecasts.")

with tab_pop:
    st.subheader("Isn't the population still growing?")
    st.markdown(
        "Yes, and that is what makes the care gap easy to miss. The gap is about the **age mix**, not the headcount. "
        "In the Census Bureau's middle projection the U.S. keeps growing until about 2080, yet the number of "
        "potential helpers per person aged 80+ falls from 7.2 in 2010 to 2.9 in 2050. From 2010 to 2030 the "
        "45–64 group grows 1% while the 80+ group grows 79% (AARP)."
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("U.S. population, July 2025", f"{POP_2025} million")
    c2.metric("Projected peak (middle series)", f"{POP_PEAK['Middle series'][1]} million",
              delta=f"in {POP_PEAK['Middle series'][0]}", delta_color="off")
    c3.metric("People 65+ outnumber children", "2029", help="Middle series: the 65+ group passes the under-18 group.")

    pop = go.Figure()
    names = list(POP_2100)
    pop.add_bar(x=[POP_2100[n] for n in names], y=names, orientation="h",
                marker_color=[brand.SLATE if n == "Middle series" else brand.SAND for n in names],
                text=[f"{POP_2100[n]} million" for n in names], textposition="outside",
                hovertemplate="%{y}: %{x} million in 2100<extra></extra>")
    pop.add_vline(x=POP_2025, line=dict(color=brand.RUST, width=2, dash="dash"),
                  annotation_text=f"2025: {POP_2025} million", annotation_position="top")
    pop.update_layout(height=280, margin=dict(l=10, r=40, t=40, b=10), paper_bgcolor=brand.PAPER,
                      plot_bgcolor=brand.SHEET,
                      title=dict(text="U.S. population in 2100 by immigration scenario", font=dict(size=14)))
    pop.update_xaxes(range=[0, 500], title="Millions", gridcolor=brand.RULE)
    pop.update_yaxes(autorange="reversed")
    st.plotly_chart(pop, width="stretch", config=PLOT_CFG)
    st.caption("Low immigration peaks at about 346 million in 2043. With zero immigration the population "
               "falls from 2024 on. Every path gets older: even with high immigration the median age rises from 38.9 "
               "(2022) to 46.5 in 2100.")
    st.caption("Sources: [Census Bureau 2023 National Population Projections]"
               "(https://www.census.gov/newsroom/press-releases/2023/population-projections.html); "
               "[Census Bureau Vintage 2025 estimates, Jan 2026]"
               "(https://www.census.gov/newsroom/press-releases/2026/population-growth-slows.html).")

    st.markdown("#### People moving between states")
    st.markdown(
        "A state that gains people can still lose helpers, because moves change the age mix as well as the "
        "headcount. Retirees who move in add to a state's 80+ group later. In the AARP table the lowest 2050 ratios "
        "are Arizona (1.8) and Nevada (2.0), both of which had 7.0 or more in 2010."
    )
    if place != "United States":
        notes = []
        if place in GREW_FASTEST_2025:
            notes.append(f"{place} was among the five fastest-growing states in 2025 (+{GREW_FASTEST_2025[place]}).")
        if place in LOST_2025:
            notes.append(f"{place} was one of five states that lost population in 2025.")
        if place in FASTEST_TO_2050:
            notes.append(f"{place} is projected to be among the fastest-growing states through 2050.")
        if place in DECLINING_TO_2050:
            notes.append(f"{place} is projected to keep losing population through 2050.")
        notes.append(f"The helper ratio there goes from {ratio[2010]} in 2010 to {ratio[2050]} in 2050.")
        st.info(" ".join(notes))
    st.caption("Sources: Census Bureau Vintage 2025 estimates (fastest-growing states and the five that lost people "
               "in 2025); [Weldon Cooper Center, July 2024]"
               "(https://coopercenter.org/research/national-50-state-population-projections-2030-2040-2050) "
               "(Utah, Idaho and Texas fastest-growing; West Virginia, Mississippi and Illinois declining through 2050).")

with tab_why:
    st.subheader("Why the old answers are running out")
    cols = st.columns(3)
    for i, (big, text, src) in enumerate(FACTS):
        with cols[i % 3].container(border=True):
            st.markdown(f"### {big}")
            st.write(text)
            st.caption(src)

with tab_method:
    st.subheader("How the simulator works")
    st.markdown(
        f"""
The published helper ratio sets the pressure: each potential helper would need to give `2010 ratio / ratio` times
the 2010 effort to provide the same care per person aged 80+ (1.76 times in 2030, 2.48 times in 2050).

Each slider is a multiplier on that, and the effects multiply:

| Slider | Effect |
| --- | --- |
| Immigration | more helpers: `× (1 + imm)` |
| Paid care workforce | more of each helper group's work goes to care: `× (1 + care)` |
| Healthier aging | fewer people aged 80+ need daily help: `÷ (1 − health)` |
| Robots and AI | machines do a share of care tasks, scaled by how much is safe to use unsupervised: `÷ (1 − capability × trust)` |

Coverage is care per person aged 80+ as a share of the 2010 level. For a state, the baseline is that state's own 2010 ratio. The bar shows each choice's share of the gap,
measured in log terms so the multiplied effects add up. The robots and AI panel shows what share of all care work
machines would have to do, safely, to close what the other choices leave open.

Scenario settings: immigration 20%; paid care 14% (BLS aides +18% against all jobs +3.5%); healthier aging 20%;
technology 40% capability at 30% safe use; "All of the above" combines them.
"""
    )
    st.subheader("Sources")
    st.markdown(
        """
- Helper ratio, national and by state (Appendix B): Redfoot, Feinberg & Houser, *The Aging of the Baby Boom and the Growing Care Gap*, AARP Public Policy Institute, 2013.
- U.S. population 341.8 million (July 2025) and the five fastest-growing and five shrinking states in 2025: U.S. Census Bureau, release CB26-20, January 2026.
- Population by immigration scenario (peak 370 million in 2080; 435, 366, 319 and 226 million in 2100; 65+ outnumber under-18s in 2029): U.S. Census Bureau, 2023 National Population Projections, November 2023.
- State growth through 2050: Weldon Cooper Center for Public Service, *National 50-state population projections: 2030, 2040, 2050*, July 2024.
- Final 2024 total fertility rate, 1,599.5 per 1,000 women: NCHS, *Births: Final Data for 2024*, NVSR 75(2), 2026.
- Net international migration down 53.8% to 1.3 million: U.S. Census Bureau, release CB26-20, January 2026.
- Deaths exceed births from 2031: CBO, *An Update to the Demographic Outlook, 2025 to 2055*, September 2025.
- Prime-age participation 83.6%: BLS series LNS11300060.
- Foreign born 19.2% of the labor force (2024): BLS, *Foreign-Born Workers*, May 2025. 48.6% of labor-force growth 1996–2000: Mosisa, *Monthly Labor Review*, May 2002.
- Health care and social assistance 37% of new jobs 2025–2035: BLS Employment Projections, August 2026. Home health and personal care aides +18%: BLS *Occupational Outlook Handbook*.
- 52% of people turning 65 will need long-term care: Favreault & Dey, ASPE, 2016.
- Immigration about 3.5 times the current rate to restore the worker-to-retiree ratio: Gokhale, Penn Wharton Budget Model, 2024.
- AI risk categories: NIST AI 600-1 (2024), WHO guidance on large multimodal models (2024), OWASP Top 10 for LLM Applications 2025.
"""
    )
    st.caption("Accompanies *When the Supports Run Out* (Douglas E. Allen). A [Dougalien Systems](https://dougalien.com) app.")
