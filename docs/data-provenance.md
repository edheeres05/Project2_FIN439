# Data provenance and source reconciliation

## Frozen research date and definitions

Review date: **November 24, 2026, end of day**. Source capture date: November 24, 2026. The observation horizon is November 2021–October 2026 inclusive: **60 complete monthly return observations × 6 ETFs = 360 observations**. October 30 is the last October trading session; the file uses calendar month-end labels, including October 31. Partial November 2026 performance is excluded. This is a current-vintage historical research snapshot, not an archive of the values originally visible at each historic date.

The raw model input is `data/monthly_returns_pct.csv`. Each cell is the published **monthly dividend-adjusted total return**, in percentage points, displayed to two decimal places; the engine divides by 100 exactly once. The provider describes its history as based on dividend-adjusted daily data. No raw price-level splicing, manual split corrections, interpolation, gap filling, or separate dividend addition occurs. USD nominal returns; no currency conversion, inflation adjustment, personal data, or future forecasts imported. Fund expenses are reflected in market performance, not deducted a second time. Taxes and investor-specific fees other than the modeled trade charge are excluded.

## Source register

| Input | Source and location | Observation / availability | Use |
|---|---|---|---|
| VOO | https://portfolioslab.com/symbol/VOO — VOO Monthly Returns History | Nov 2021–Oct 2026; captured Nov 24, 2026 | Large-cap equity exposure |
| QQQ | https://portfolioslab.com/symbol/QQQ — QQQ Monthly Returns History | Same | Nasdaq-100 growth tilt |
| SOXX | https://portfolioslab.com/symbol/SOXX — SOXX Monthly Returns History | Same | Semiconductor equity exposure |
| SCHD | https://portfolioslab.com/symbol/SCHD — SCHD Monthly Returns History | Same | Dividend equity exposure |
| BIL | https://portfolioslab.com/symbol/BIL — BIL Monthly Returns History | Same | Short-term Treasury bill reserve |
| BND | https://portfolioslab.com/symbol/BND — BND Monthly Returns History | Same | Broad U.S. investment-grade bond exposure |
| Annual Treasury reference | https://fred.stlouisfed.org/series/DGS3MO/history — Board of Governors, via FRED | Observation Nov 23, 2026 = **4.37%**; source page reports publication Nov 24, 2026, 3:16 p.m. CST | Short-term annual risk-free proxy for estimated Sharpe score |
| Historical diagnostic Treasury reference | https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202410&type=daily_treasury_yield_curve — 3 Mo column | Oct 30, 2024 = **4.67%**; historical Treasury quote preceding evaluation period; retrieved Nov 24, 2026 | Training-only risk-free proxy for chronological check |
| 10 bps per bought/sold dollar | Analyst scenario assumption, not a broker quote | Approved model assumption | Base estimated trading cost; 30/50 bps stresses |
| 6% net return, 15% vol, BIL 5%, 25% turnover | Student-selected mandate | Project development | Numerical constraints |

## Lineage and integrity

Source tables were manually transcribed by the AI-assisted project workflow on Nov 24, 2026; `build_data.py` preserves the transcribed source percentages by year and symbol and reproduces the chronological CSV deterministically. Source cells and frozen CSV are rounded as displayed, not presented as higher-precision observations. The engine refuses a different checksum, wrong shape, incorrect dates, missing values, invalid return units or non-finite inputs. The code checks both source files and uses immutable SHA256 values:

- Monthly returns: `33294b3122e0990303672b4cca389a1462930a160a214662875bf4361ead4378`
- FRED data card: `a21726cfad77a51aec46c7ffedf9121175efee453c687e14aaa5e6ffbef1ebc5`

`python audit_data.py` compares compounded 2022–2025 monthly returns to the corresponding reported calendar-year totals for each ticker, checks October against a second price table, and records two cross-publisher definition checks. `outputs/data-audit.json` is the reproducible audit output. All 24 annual totals reconcile within 0.10 percentage point; maximum difference **0.0273 pp**. These same-provider annual checks detect transcription problems but are not independently sourced observations. The display rounding and underlying provider revisions remain limitations.

## Cross-source discrepancy and disposition

Digrin monthly adjusted-price tables were examined for all six tickers: `https://www.digrin.com/stocks/detail/{TICKER}/price`. Five October return ratios agree with the primary total-return table within 0.10 pp. BND does not: the displayed September and October adjusted prices, $69.65 and $71.56, imply +2.7423%, versus +2.37% in the primary monthly total-return table. We do not splice that ratio into the series or assume which adjustment convention caused the mismatch. An independently published BND one-month reinvested nominal return ending October 31 is +2.37% (https://www.lazyportfolioetf.com/etf/vanguard-total-bond-market-bnd/, investment returns as of Oct 31, USD, dividend reinvestment). This supports use of the explicitly defined primary total-return series rather than a mixed price basis. SOXX October total return is -17.08%; ChartRow reports -17.1% at one-decimal display precision (https://chartrow.com/quote/soxx/monthly-returns). It must not be confused with a split-related fall in unadjusted price. Providers may share upstream data; these checks are limited, not a vendor audit.

The older package contained 60 price levels, yielding only 59 returns, and combined snapshots. It is retired. The new source has 60 actual monthly return observations, so old 6.44% estimates must not appear as the final baseline. `outputs/baseline.json` is the new calculation source of record.

## Licensing, revisions and privacy

Public visibility does not establish unrestricted redistribution rights. PortfoliosLab source tables are used for restricted educational evaluation; permission to republish a full dataset commercially or publicly has not been verified. Use a private repository with the instructional team granted access unless permission is verified; confirm course access requirements. Cite the publishers and do not describe the data as open-licensed. FRED series notes identify the original Board of Governors source and request citation. No passwords, keys, credentials, user account balances, or actual holdings are collected or committed. A later refresh requires a new dated snapshot, checksum, documented source differences, rerun and separate commit; never silently overwrite the frozen evidence.
