# Validation, sensitivity and AI use | November 24, 2026

## 1. Evidence boundary and source correction

The previous package's 60 price observations produced 59 returns and combined an older snapshot with an October price-ratio update. It was adequate for exploratory work only. The revised snapshot uses 60 directly reported dividend-adjusted monthly total returns from one provider (PortfoliosLab), Nov 2021–Oct 2026; rounded at source to 0.01 pp. Captured Nov 24. No November partial return, fabricated observation, fill, or old-price splice. Exact data and FRED metadata checksums, source links, alternate-source comparisons, units, privacy and licensing limits are in `data-provenance.md`. The dated 4.37% risk-free proxy is from FRED DGS3MO (observation Nov 23, publication Nov 24, 3:16 p.m. CST), not a historical BIL estimate or guaranteed five-year yield.

Data check: 24/24 2022–25 calendar-year compounding reconciliations agree within 0.10 pp; maximum absolute deviation 0.0273 pp. Five Digrin October adjusted-price ratios agree within 0.10 pp; BND ratio +2.74% conflicts with primary +2.37%. A separate published one-month reinvested BND return supports +2.37%; SOXX cross-check -17.1% versus -17.08%. Retain one source and reject splicing. Source-vintage revisions and redistribution rights remain unresolved for deployment. `outputs/data-audit.json` records checks; annual reconciliation is a transcription check, not an independent source audit. No historical point-in-time claim before the frozen source date.

## 2. Finance and independent implementation checks

Monthly arithmetic mean × 12; annualized sample covariance = monthly covariance × 12; variance = w'Σw. One-way turnover = half sum of absolute pre/post trade weight differences; costs apply to both sides. A 10-bps charge × 50% of value traded = 0.05% estimated initial cost. Estimated first-year net return = (1 − cost)(1 + gross estimate) − 1. Fund fees reflected in observed returns are not double counted. Tax effects excluded. The risk-adjusted score uses (estimated net return − annual Treasury proxy) / annual volatility. This is an estimated forward Sharpe-type score, not an achieved Sharpe or a statistical forecast. No leverage, shorting, or derivatives; fully invested 5%-increment grid. No continuous optimum claimed. Return floor is a constraint on an estimate, not achieved performance. Risk-free proxy is a short-term reference, not a guaranteed five-year rate.

Independent known answer: two assets, 60/40 new weights, 50/50 old, means 8%/4%, diagonal annual variance 0.04/0.01. Gross 6.40%, one-way turnover 10%, cost 0.02%, net 6.37872%, volatility 12.6491%. The test calculates these without relying on the engine's optimization.

A second implementation constructs portfolio monthly returns for every one of the 53,130 weight vectors, directly calculates means and sample standard deviations, separately charges costs, and recomputes feasibility. It verifies 1,082 feasible allocations, minimum-volatility selection and global maximum of estimated Sharpe on the grid. `tests/test_engine.py` also checks both reported estimates directly on monthly portfolio returns, frontier monotonicity/non-domination, sample size and sources, exact snapshot reconstruction, checksum rejection, duplicate/missing/nonfinite data, invalid holdings, infeasibility, stale boundary, drawdown boundary, nonpositive signal, already-used turnover and historical weight drift. All 22 tests passed in the available Python 3.13.5 / NumPy 2.3.5 / pandas 2.2.3 Linux calculation environment (see `outputs/test-results.txt`). The revised Streamlit code passed Python syntax compilation; Streamlit/Altair were not installed in that environment, so this is not a UI runtime or second-machine cold run. Prior version launched on the student's Windows machine, but its evidence does not validate the revised app.

## 3. Baseline, stress and decision evidence

| Candidate | Net estimate | Annual volatility | Estimated Sharpe | Turnover | Numerical verdict |
|---|---:|---:|---:|---:|---|
| Equal weight | 11.87% | 13.83% | 0.542 | 56.67% | FAIL turnover |
| Inverse volatility | 4.21% | 1.85% | -0.086 | 80.98% | FAIL return, turnover |
| Benchmark | 6.68% | 9.58% | 0.242 | 0% | PASS |
| Minimum volatility | 6.28% | 7.35% | 0.260 | 25% | PASS |
| Maximum estimated Sharpe | 12.24% | 14.18% | 0.555 | 25% | PASS |

The minimum-volatility weights are 40% VOO, 35% BIL, 25% BND. Maximum estimated Sharpe is 50% VOO, 15% SOXX, 10% SCHD, 10% BIL, 15% BND. The latter uses 75% equity exposure and approaches the volatility ceiling. Compare the historical semiconductor arithmetic estimate of 29.92% with its 38.76% annualized volatility; this load-bearing estimate is not a long-horizon fundamental forecast. BND's near-zero historical arithmetic mean is also sample-dependent, not a current yield forecast. Both candidates are sensitive to the estimation window.

| Exploratory scenario | Min-vol net / vol | Max-Sharpe net / vol | Decision |
|---|---:|---:|---|
| 10 bps baseline | 6.28% / 7.35% | 12.24% / 14.18% | Pilot |
| 30 bps | 6.18% / 7.35% | 12.13% / 14.18% | Pilot |
| 50 bps | 6.07% / 7.35% | 12.01% / 14.18% | Pilot |
| Equity means -2 pp | 6.01% / 7.88% | 11.14% / 14.94% | Pilot, narrow headroom |
| 36-month window | 9.11% / 4.52% | 18.50% / 9.49% | Pilot; materially different estimates |
| 48-month window | 7.95% / 4.96% | 18.66% / 12.34% | Pilot |
| 10% BIL reserve | 6.28% / 7.35% | 12.24% / 14.18% | Pilot |
| 10% turnover | 6.40% / 8.59% | 9.65% / 12.20% | Pilot |
| 5% volatility cap | No feasible | No feasible | STOP |
| Actual drawdown reaches 15% | Numeric targets still calculate | Numeric targets still calculate | STOP |
| Treasury proxy +1 pp | Same target weights | Same target weights | Pilot; score falls |

See `outputs/stress_summary.json` for actual weights, counts and full precision. The original 10→30 bps prediction was discussed with AI and was not precommitted AI-off. On this revised model both candidates retain their baseline weights; higher cost lowers net return but not gross mean/covariance or weights. This exploratory stress is not the formal locked record. The 15% drawdown test was also executed on the earlier app by the student; the current automated risk boundary confirms the revised engine behavior, not a revised human UI run.

## 4. Chronological challenge and limitations

Fixed-target annual rebalancing with drift, initial transition and both-side transaction costs on the full sample is a hindsight diagnostic. It does not apply rolling policy checks or stops. Month-end max drawdown: benchmark -17.81%; min volatility -13.15%; max estimated Sharpe -22.15%. A policy estimate below 15% volatility clearly does not guarantee a loss below 15%: the historical path of the higher-return candidate exceeds the drawdown threshold. In a separate chronological research diagnostic, estimate using only the first 36 returns (through October 2024) with Oct 30 2024 3-month Treasury quote 4.67%; select constrained targets; evaluate the next 24 monthly returns without re-estimation, with annual drift/rebalancing and modeled costs. Results: benchmark CAGR 9.92% and max month-end drawdown -3.16%; min-vol CAGR 10.91%, drawdown -3.56%; max-Sharpe CAGR 17.41%, drawdown -6.03%. The training period uses revised historical data and this split has been examined during development. No untouched holdout, vintage reconstruction, out-of-sample signal validation, actual trade log or prospective track record is claimed. These challenges support paper evaluation, not live approval. The app is an allocation review tool, not a broker or account ledger.

## 5. Formal locked changed-input record

The final-model locked experiment must be authored independently before execution. A separate SOXX-specific annual expected-return haircut is specified in `locked-change-record.md`; its changed-input result has not been executed or revealed. The existing exploratory stresses are not passed off as the required experiment. Add the real baseline and prediction commit links/timestamps, original student prediction, actual result and diagnosis here after execution. The student must state the actual decision effect even if the app remains PILOT.

## 6. Material AI uses and verification

ChatGPT (GPT-6 family, exposed model label; interactions Nov 23–24, 2026): source retrieval and comparison; design and code; portfolio estimates; data reconstruction; testing; document drafting. The student selected the investor audience, five-year goal, 6% return target, 15% volatility cap, ETF universe, benchmark, risk/return preference and pilot decision. The student asked for both optimizers; estimated Sharpe and the FRED reference operationalize that preference. The AI-assisted source reconciliation corrected the previous mixed price basis and 59-return sample. AI-produced claims about return definitions and timing must be checked by the student personally; the BND source conflict and FRED publication boundary are material candidates. No personal verification is claimed until the student supplies actual evidence/disposition. No AI assistance is permitted for the independent pre-run prediction.

## 7. Reproducibility and acceptance

`outputs/visible-summary.txt`, `baseline.json`, `stress_summary.json`, `historical_diagnostics.json`, `chronological_check.json`, `data-audit.json`, and `test-results.txt` expose material evidence without running the application. A second-machine cold run on the frozen revision still requires an actual independent user, OS/Python/package versions, start/end or elapsed time, commands, outcome and first failure/resolution. No invented logs, personal cold run, transcript or commit. The decision remains a paper-only PILOT (0% real capital). Data provenance, prospective evidence, independent verification, access and committee approval must precede consideration of live allocation. See `pilot-monitoring.md` for specific monitor and stop triggers.
