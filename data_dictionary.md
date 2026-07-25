# Data dictionary

All files are deterministic synthetic data created by `scripts/build_experiment_pack.py`.

| Table | Grain | Selected fields | Purpose |
|---|---|---|---|
| `store_attributes.csv` | store | region, format, baseline index | matching context |
| `customer_attributes.csv` | customer | segment, tier, prior spend | segmentation context |
| `test_assignments.csv` | store assignment | treatment group, match cell | assignment audit |
| `transactions.csv` | transaction | net sales, margin, conversion | outcome analysis |
| `data_feed_validation.csv` | store-week-feed | expected/received rows, null rate | IT/vendor feed health |
| `experiment_summary.csv` | treatment × segment | AOV, conversion, margin | outcome rollup |

`net_sales` and `gross_margin` are synthetic USD-like amounts. `baseline_index` is a synthetic relative index. `converted` is an illustrative transaction-level outcome flag.
