# Point-in-time signal data card

| Field | Specification |
|---|---|
| Signal | Trailing 12 completed months of VOO total return |
| Source | PortfoliosLab VOO Monthly Returns History, https://portfolioslab.com/symbol/VOO |
| Observation span | November 2025–October 2026; last trading session October 30, 2026 |
| Availability boundary | Source capture November 24, 2026; permitted only for the end-of-day review on/after that date |
| Transformation | Product of (1 + monthly decimal total return) minus 1; not the sum of monthly returns |
| Result | +12.09497%, rounded to +12.09% |
| Rule | Nonpositive value pauses new risk-taking; positive value permits further policy checks, never guarantees returns or authorizes capital |
| Missing/stale | No imputation; corrupt or missing source stops the app; after 45 calendar days from last trading session the snapshot is stale |
| Revisions | Historical return tables may be revised; actual vintage at earlier dates has not been established |
| Validation status | Timing and transformation checked; synthetic negative-signal stop tested. No demonstrated forecasting value or prospective validation. |

The Treasury input is a separately sourced 3-month annualized CMT yield, not the VOO signal and not a forecast of the BIL return. FRED's 4.37% observation dated Nov 23 was published on Nov 24 at 3:16 p.m. CST. The app rejects a review date before the frozen capture date. It does not use the Nov 24 vintage to claim an implementable historical strategy. The chronological check is an estimation diagnostic on revised data and does not apply this signal retroactively. See `data-provenance.md` for source URLs, definitions and risk-free metadata.
