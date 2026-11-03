# Data for the sector view

Published numbers only, copied from the pages and spreadsheets below on 3 Nov 2026. Employment and labor force are in thousands; openings are thousands a year (2025 to 2035 annual average); rates are percent a year. Nothing here is used by the app yet.

| File | Source | Status |
| --- | --- | --- |
| `bls_ep_table_1_1.csv` | BLS Employment Projections 2025-35, [Table 1.1, Employment by major occupational group](https://www.bls.gov/emp/tables/emp-by-major-occupational-group.htm) | Complete (all 22 major groups and the total) |
| `bls_ep_table_1_10.csv` | BLS Employment Projections 2025-35, [Table 1.10, Occupational separations and openings](https://www.bls.gov/emp/tables/occupational-separations-and-openings.htm) | Complete (all 22 major groups and the total), read from the BLS spreadsheet [occupation.xlsx](https://www.bls.gov/emp/ind-occ-matrix/occupation.xlsx), sheet "Table 1.10". Columns: exit and transfer rates, and annual averages of labor force exits, occupational transfers and openings. |
| `bls_ep_table_3_1.csv` | BLS Employment Projections 2025-35, [Table 3.1, Civilian labor force by age](https://www.bls.gov/emp/tables/civilian-labor-force-summary.htm) | Complete for these age groups. The 65 and older row is the sum of BLS's 65 to 74 and 75 and older rows. |
| `census_np2023_t3_80plus.csv` | U.S. Census Bureau, *Projected Population by Five-Year Age Group and Sex for the United States, Main Series: 2022-2100*, [Table 3](https://www2.census.gov/programs-surveys/popproj/tables/2023/2023-summary-tables/np2023-t3.xlsx), released November 2023. Resident population on July 1, thousands, both sexes. | Complete. The five bands from 80 to 84 up to 100 and over are copied as published; `age_80_plus` is their sum. |

Release: BLS [Employment Projections 2025 to 2035](https://www.bls.gov/news.release/archives/ecopro_08272026.htm), 27 Aug 2026.
