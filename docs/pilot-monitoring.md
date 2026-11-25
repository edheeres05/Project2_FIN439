# Paper-trading governance protocol

## Committee scope

Proposed research protocol, no live money: run minimum-volatility and maximum-estimated-Sharpe candidates as separate simulated accounts, plus a 50/40/10 benchmark. Initial simulated targets are in `outputs/baseline.json`. Use the same starting hypothetical value and pre-trade portfolio for all; no claim of actual account balances. The proposed 12 monthly reviews are for operational evidence and do not prove five-year performance.

At each review, preserve the prior model/data hash, newly available source observations, decision date, benchmark level, paper fills, realized costs, drifted weights, actual simulated turnover ledger over trailing 12 months, net account value and peak, drawdown, signal, and every constraint verdict. Use the dated data actually available then. Compare net cumulative performance, realized monthly volatility and drawdown relative to benchmark; report uncertainty and missed fills. Monthly data cannot establish intra-month stop execution: use a daily account-value monitoring source for a real deployment or restrict pilot claims to observed dates.

| Trigger | Required response |
|---|---|
| Missing/corrupted data, availability or definition problem | Stop; reconcile and freeze new validated snapshot |
| Source older than 45 calendar days | Stop; do not reuse stale estimates as current |
| Nonpositive trailing 12-month VOO return | Pause new risk; do not interpret as a proven sell signal |
| Measured drawdown ≥15% | Pause new risk; committee reviews exposure and liquidity; no automated forced sale |
| No feasible allocation / reserve, return estimate, volatility or turnover breach | Record failed rules; no new allocation until resolved and approved |
| Material concentration or cost-assumption concern | Challenge SOXX return, overlap and trade execution; review both candidates |
| Investor has firm liability or needs funds earlier | Reassess suitability and liquidity; do not rely on forecast liquidation value |

At 12 months, consider whether the app is operationally reproducible, controls stop correctly, the benchmark comparisons are credible, net performance and realized risk justify continuing, and the observed data are suitable and permitted for use. No live allocation merely because 12 months elapsed or an estimated Sharpe is high. Require separate written committee approval. If insufficient evidence, extend the pilot, revise or reject. No actual prospective records are asserted in this package.
