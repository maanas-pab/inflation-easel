# Data

`cpi_groceries.csv` — one row per year, 1970-2026.

- `cpi_u` — BLS Consumer Price Index for All Urban Consumers (CPI-U),
  annual average, 1982-84 = 100. 1970-2024 are BLS published annual
  averages; 2025 is the BLS year-to-date average at time of writing;
  2026 is a ~2.5% projection, clearly marked in code as `projected=True`.
- `food_at_home_index` — BLS Food-at-home CPI, same base. Same sourcing notes.
- `apple_per_lb`, `bread_per_loaf`, `eggs_per_dozen`, `milk_per_gallon` —
  BLS Average Price Data (AP.data) national averages in nominal dollars.
  Early-70s loaf/dozen/gallon figures are from BLS bulletins; modern years
  track AP.series APU0000701112 (apples), APU0000702111 (bread),
  APU0000701112-adjacent egg series, and APU0000701113 (milk).

All values are nominal contemporaneous dollars — that is the point:
the painting shows what a fixed 1970 basket costs over time.
