**AI use:** ChatGPT (GPT-6 family) assisted with financial research, code, calculations, testing and drafting; the investment mandate, ETF selection and decision to pilot are my choices, and I own the analysis and decision.

**Educational analysis only; not investment advice.**

# Investment committee memo | November 24, 2026

**Decision requested: PILOT — paper trading only; live capital allocation range 0–0%.** Evaluate two competing, mandate-constrained allocation processes in parallel against the benchmark. Do not execute real trades or approve live allocation from historical estimates.

## Intended investor and mandate

My intended user is a college student or young adult with a flexible five-year financial goal. Five years is a horizon people my age can picture, with possible major expenses after graduation. It is not a guarantee that invested funds can be recovered in full on a particular date. Emergency reserves must be held separately; capital needed at a firm date or that cannot tolerate a loss is not suitable for this allocation process. The policy should be reviewed as the goal approaches.

I chose a 6% estimated nominal net annual return target to make room for BIL and BND instead of relying entirely on stocks. The 15% estimated annual volatility ceiling reflects my preference for controlled risk and steady growth rather than speculation. It is a statistical estimate, not a cap on loss. No leverage, shorting or derivatives. Minimum BIL 5%; rolling one-way annual turnover at most 25%; review monthly and normally rebalance annually. A 15% actual drawdown pauses new risk-taking. VOO covers large U.S. companies, QQQ growth exposure, SOXX the semiconductor growth thesis, SCHD dividend equity, BND broad bonds and BIL short Treasury bills. SOXX potential is a thesis, not a promise. The benchmark is 50% VOO, 40% BND, 10% BIL, also the hypothetical starting holdings.

I want a reasonable trade-off between return and risk rather than mechanically minimizing either risk or maximizing return. The app therefore retains minimum volatility and maximum estimated Sharpe as competing optimizers, using the same return floor, reserve, volatility and turnover constraints.

## Evidence and allocation comparison

Sixty completed monthly total returns (Nov 2021–Oct 2026) from a single provider, captured Nov 24, replace the earlier mixed price series. The annual risk-free proxy is 4.37%, observed Nov 23 and published by FRED Nov 24. Estimated net annual return charges 10 bps on each dollar bought or sold; no taxes. Risk uses annualized monthly sample covariance. Estimated Sharpe is net excess return divided by annualized volatility, not realized performance. The 5% grid screens 53,130 fully invested allocations; 1,082 qualify numerically.

| Portfolio | Estimated net return | Volatility | Est. Sharpe | One-way turnover | Verdict |
|---|---:|---:|---:|---:|---|
| Equal weight | 11.87% | 13.83% | 0.542 | 56.67% | Fail: turnover |
| Inverse volatility | 4.21% | 1.85% | -0.086 | 80.98% | Fail: return, turnover |
| Benchmark | 6.68% | 9.58% | 0.242 | 0% | Pass |
| Minimum volatility | 6.28% | 7.35% | 0.260 | 25% | Pass |
| Max estimated Sharpe | 12.24% | 14.18% | 0.555 | 25% | Pass |

Minimum volatility: **40% VOO / 35% BIL / 25% BND**. Max estimated Sharpe: **50% VOO / 15% SOXX / 10% SCHD / 10% BIL / 15% BND**. QQQ is eligible but receives zero; no need to force an allocation to each ETF. These are two alternative 100%-invested simulated targets, not real orders or independent weight bands. Both spend the entire turnover budget. The latter adds 5.95 pp expected net return for 6.83 pp additional annual volatility relative to minimum volatility, with just 0.82 pp volatility headroom and 75% equities versus 40%. Its higher estimated Sharpe depends on the historical SOXX arithmetic mean (29.92%), which may not persist.

## Challenge and committee action

A 30-bps cost scenario leaves both allocations unchanged (net estimates 6.18% and 12.13%); at 50 bps the minimum-volatility estimate is only 6.07%. Cutting equity estimates by 2 pp pushes both candidates toward the constraint boundary; shorter windows change their composition materially. A 5% volatility ceiling eliminates feasible allocations. Both the 15% drawdown stop and stale-source gate override numerical passes. The VOO trailing 12-month signal is +12.09%; its predictive edge is not established.

The November 25 changed-input experiment reduced the SOXX expected annual return by 10 percentage points: minimum volatility remained unchanged; maximum estimated Sharpe shifted 10 points from SOXX to QQQ and SCHD, with net return declining to 10.03%, volatility to 12.44%, and estimated Sharpe to 0.455. Both passed; the pilot recommendation remained unchanged. The student personally checked the BND October return and retained the 2.37% reported total return. See [validation and named AI-use record](validation-and-ai-use.md) for source checks, the precommitted prediction, results and disclosed procedural assistance.

In a hindsight fixed-target annual-rebalance diagnostic, the maximum-Sharpe candidate experienced a 22.15% month-end peak-to-trough loss, exceeding the 15% policy pause threshold; minimum volatility experienced 13.15%, benchmark 17.81%. This is not a simulated mandate-enforced strategy or prospective result. A 36-month-estimation / 24-month-later-evaluation diagnostic shows 10.91%, 17.41% and 9.92% CAGR for minimum-volatility, maximum-Sharpe and benchmark respectively, with later drawdowns of 3.56%, 6.03% and 3.16%. It is informative but was examined after the fact with revised data. These results make minimum volatility a conservative reference, not necessarily the winner; both merit paper evaluation, not a live allocation.

**Proposed pilot governance:** maintain two separately tracked simulated portfolios and the benchmark for 12 monthly reviews, record actual paper fills, costs, drift, turnover, return and drawdown, compare against the contemporaneous benchmark, and avoid automatic rebalancing on a breach. Pause for ≥15% account drawdown, nonpositive VOO signal, stale/corrupt inputs or infeasibility; escalate material policy changes to the committee. Before live approval require a documented independent cold run and AI-off challenge, prospective evidence and verified data rights, a suitable actual investor, reproducible results, realistic costs and committee authorization. A one-year pilot is not proof of a five-year return target. Reject or revise the process if these requirements fail; never silently relax a constraint. The portfolio may lose value, and technology overlap, sector concentration, rate duration, reinvestment risk and uncertain mean/covariance estimates remain material.
