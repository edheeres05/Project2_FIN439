# Validation, sensitivity and AI use | November 25, 2026

## 1. Evidence boundary and source correction

The previous package's 60 price observations produced 59 returns and combined an older snapshot with an October price-ratio update. It was adequate for exploratory work only. The revised snapshot uses 60 directly reported dividend-adjusted monthly total returns from one provider (PortfoliosLab), Nov 2021–Oct 2026; rounded at source to 0.01 pp. Captured Nov 24. No November partial return, fabricated observation, fill, or old-price splice. Exact data and FRED metadata checksums, source links, alternate-source comparisons, units, privacy and licensing limits are in `data-provenance.md`. The dated 4.37% risk-free proxy is from FRED DGS3MO (observation Nov 23, publication Nov 24, 3:16 p.m. CST), not a historical BIL estimate or guaranteed five-year yield.

Data check: 24/24 2022–25 calendar-year compounding reconciliations agree within 0.10 pp; maximum absolute deviation 0.0273 pp. Five Digrin October adjusted-price ratios agree within 0.10 pp; BND ratio +2.74% conflicts with primary +2.37%. A separate published one-month reinvested BND return supports +2.37%; SOXX cross-check -17.1% versus -17.08%. Retain one source and reject splicing. Source-vintage revisions and redistribution rights remain unresolved for deployment. `outputs/data-audit.json` records checks; annual reconciliation is a transcription check, not an independent source audit. No historical point-in-time claim before the frozen source date.

## 2. Finance and independent implementation checks

Monthly arithmetic mean × 12; annualized sample covariance = monthly covariance × 12; variance = w'Σw. One-way turnover = half sum of absolute pre/post trade weight differences; costs apply to both sides. A 10-bps charge × 50% of value traded = 0.05% estimated initial cost. Estimated first-year net return = (1 − cost)(1 + gross estimate) − 1. Fund fees reflected in observed returns are not double counted. Tax effects excluded. The risk-adjusted score uses (estimated net return − annual Treasury proxy) / annual volatility. This is an estimated forward Sharpe-type score, not an achieved Sharpe or a statistical forecast. No leverage, shorting, or derivatives; fully invested 5%-increment grid. No continuous optimum claimed. Return floor is a constraint on an estimate, not achieved performance. Risk-free proxy is a short-term reference, not a guaranteed five-year rate.

Independent known answer: two assets, 60/40 new weights, 50/50 old, means 8%/4%, diagonal annual variance 0.04/0.01. Gross 6.40%, one-way turnover 10%, cost 0.02%, net 6.37872%, volatility 12.6491%. The test calculates these without relying on the engine's optimization.

A second implementation constructs portfolio monthly returns for every one of the 53,130 weight vectors, directly calculates means and sample standard deviations, separately charges costs, and recomputes feasibility. It verifies 1,082 feasible allocations, minimum-volatility selection and global maximum of estimated Sharpe on the grid. `test_engine.py` (repository root; originally `tests/test_engine.py`) also checks both reported estimates directly on monthly portfolio returns, frontier monotonicity/non-domination, sample size and sources, exact snapshot reconstruction, checksum rejection, duplicate/missing/nonfinite data, invalid holdings, infeasibility, stale boundary, drawdown boundary, nonpositive signal, already-used turnover and historical weight drift. All 22 tests passed in the available Python 3.13.5 / NumPy 2.3.5 / pandas 2.2.3 Linux calculation environment (see `outputs/test-results.txt`). The revised Streamlit code passed Python syntax compilation; Streamlit/Altair were not installed in that environment, so this is not a UI runtime or second-machine cold run. The student subsequently launched the revised Streamlit app on Windows and showed all 22 tests passing (0.524 seconds, Python 3.14 series). The initial test-discovery failure occurred in the outer download directory and was resolved by entering the inner project directory. This is a first-machine run, not an independent cold run. In the current repository the unchanged test file sits at the root; run `py -m unittest discover -s . -p test_engine.py -v` there. The README and Windows launcher use the repository-root test command.

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

## 5. Locked changed-input record — November 25, 2026

**Baseline:** [GitHub commit 4442c05594191d47a292a040d9ef974502b396de](https://github.com/edheeres05/Project2_FIN439/commit/4442c05594191d47a292a040d9ef974502b396de), committed November 25 at 1:51:18 p.m. CST (19:51:18 UTC). Original executed output: [`outputs/baseline.json`](../outputs/baseline.json).

**Pre-run prediction:** [original student prediction](../ai-off-prediction.md), preserved in [commit e6329aea9b34afa81649ae3ba40990d8e068c11f](https://github.com/edheeres05/Project2_FIN439/commit/e6329aea9b34afa81649ae3ba40990d8e068c11f), November 25 at 2:58:36 p.m. CST (20:58:36 UTC). The GitHub commit adds only the prediction file; the model and data are unchanged relative to the baseline commit. The student's original wording is retained, including the unfilled local-time label; the actual commit timestamp above establishes the recorded order. The original is in the repository root, not the `docs/` directory.

**Single changed input:** additional SOXX annual expected-return reduction from 0 to 10 percentage points (29.916% to 19.916% estimated annual arithmetic return). The student executed the test through the Streamlit UI on November 25 after committing the prediction and exported the actual review JSON. The exported decision date remains November 24 (the frozen research date), not the execution date. Exact execution time is not embedded in the export. The separate CLI was not used; no CLI verification or exact local Git revision is claimed. The preserved inputs match the frozen baseline, including data SHA-256, 60 months, 4.37% Treasury proxy, 10-bps cost, 6% net return floor, 5% BIL minimum, 15% volatility ceiling, 25% turnover ceiling, zero prior turnover/drawdown, 50/40/10 starting weights, and unchanged individual asset volatilities. This is a return-assumption stress, not a change to historical returns or covariance.

Actual executed evidence: [`locked-change-result.json`](../locked-change-result.json), the student's unmodified UI export. The student reports using his own wording, financial reasoning, and application navigation to complete the prediction and execute the experiment. The original student-authored prediction was committed before the observed changed result. ChatGPT answered separate questions about financial concepts, required prediction fields, and where to find application controls, but did not write or edit the prediction, operate the application for the student, or reveal the changed results before execution. These interactions are disclosed; the student's own execution and prediction authorship are distinct from the explanatory assistance. Strict AI-off compliance is for the instructor to determine. The earlier AI-assisted cost experiment is not substituted for this record.

### Before/after results

| ETF | Min-vol before | Min-vol after | Max-Sharpe before | Max-Sharpe after |
|---|---:|---:|---:|---:|
| VOO | 40% | 40% | 50% | 50% |
| QQQ | 0% | 0% | 0% | 5% |
| SOXX | 0% | 0% | 15% | 5% |
| SCHD | 0% | 0% | 10% | 15% |
| BIL | 35% | 35% | 10% | 10% |
| BND | 25% | 25% | 15% | 15% |

| Metric | Min-vol before | Min-vol after | Max-Sharpe before | Max-Sharpe after |
|---|---:|---:|---:|---:|
| Estimated net return | 6.2838% | 6.2838% | 12.2374% | 10.0342% |
| Annual volatility | 7.3525% | 7.3525% | 14.1822% | 12.4423% |
| Estimated Sharpe | 0.260297 | 0.260297 | 0.554736 | 0.455234 |
| One-way turnover | 25% | 25% | 25% | 25% |
| BIL reserve | 35% | 35% | 10% | 10% |
| Mandate verdict | PASS | PASS | PASS | PASS |

Eligible grid allocations fell from 1,082 to 1,060 of 53,130. Equal weight still fails turnover; inverse volatility still fails return and turnover; benchmark still passes. The app remains PILOT: paper trading only, with 0% live allocation and no new stop reason.

### Predicted versus actual and discrepancy diagnosis (post-run, AI-assisted analysis)

| Student expectation (summarized; original preserved above) | Actual result | Reconciliation |
|---|---|---|
| Min-vol SOXX down, VOO and QQQ up | All weights unchanged | Miss: original SOXX weight already zero |
| Min-vol return approximately unchanged | 6.2838% unchanged | Match; 6% is a floor, not an exact target |
| Min-vol volatility slightly down | 7.3525% unchanged | Miss |
| Min-vol Sharpe about the same; requirements pass | 0.260297 unchanged; PASS | Match |
| Max-Sharpe SOXX down; VOO and QQQ up | SOXX -10 pp, QQQ +5 pp, SCHD +5 pp; VOO unchanged | Partial match |
| Max-Sharpe net return and volatility down | Net -2.2032 pp; volatility -1.7399 pp | Match in direction |
| Max-Sharpe Sharpe about the same | Down 0.099502 | Miss |
| Max-Sharpe requirements pass; paper pilot remains | PASS; PILOT | Match |

The minimum-volatility optimizer minimizes annualized variance subject to the constraints. Its previous optimal weights have no SOXX; reducing only SOXX's mean does not change its return or covariance risk. The feasible set shrinks, but this existing minimum remains feasible, so no better lower-volatility allocation can emerge from the smaller set. This explains why the expected allocation and volatility reductions did not occur.

The maximum-Sharpe optimizer reassigns 10 pp from SOXX, split equally between QQQ and SCHD. VOO remains at 50%; the optimizer is free to choose SCHD rather than raise VOO. Risk depends on the entire covariance matrix and the risk-free rate is held fixed. Net excess return falls from 7.8674% to 5.6642%, proportionally more than volatility falls. Therefore estimated Sharpe drops even though the new allocation is the best feasible ratio under the revised assumptions. Both portfolios continue to satisfy the 6% return floor and other constraints. The higher-return strategy still depends on uncertain historical return estimates and retains 75% equity exposure. The 29.92% baseline SOXX estimate is the annualized arithmetic mean of the 60 historical monthly total returns, not a prediction that SOXX will earn 29.92% annually over the next five years. This is a key reason for testing lower return assumptions and restricting the recommendation to paper trading. The student's pre-run recommendation was to retain paper trading; the application result also remains PILOT, 0% real capital. The unchanged action is supported by the numerical passes and material sensitivity, not by a promise of future returns.

## 6. Material AI uses and verification

ChatGPT (GPT-6 family, exposed model label; interactions Nov 23–25, 2026): source retrieval and comparison; design and code; portfolio estimates; data reconstruction; testing; document drafting. The student selected the investor audience, five-year goal, 6% return target, 15% volatility cap, ETF universe, benchmark, risk/return preference and pilot decision. The student asked for both optimizers; estimated Sharpe and the FRED reference operationalize that preference. The AI-assisted source reconciliation corrected the previous mixed price basis and 59-return sample. **Student-performed AI-output check, November 25, 2026:** The student opened and inspected three source pages and supplied screenshots: [PortfoliosLab BND monthly returns](https://portfolioslab.com/symbol/BND) (October 2026 +2.37%); [Digrin BND adjusted monthly prices](https://www.digrin.com/stocks/detail/BND/price) (September $69.65, October $71.56, implying +2.7423%); and [Lazy Portfolio ETF BND](https://www.lazyportfolioetf.com/etf/vanguard-total-bond-market-bnd/) (October total return +2.37%). The assistant explained the adjusted-price calculation and differences in return definitions; the student selected 2.37%, stating: “i'd use the 2.37 because we aren't looking at the adjusted price, also I like to use more conservative numbers”. The retained value is supported by two directly reported monthly total-return series; conservatism alone is not a valid reason to change a historical observation. The model uses dividend-adjusted total returns, not unadjusted price changes. Digrin's exact adjustment discrepancy remains unresolved; no price-ratio splice is made. Disposition: accept the existing 2.37% input and reject substitution of the 2.74% price-derived estimate. The student personally inspected the sources with AI guidance; this is not an AI-off check or proof of fully independent vendor data. The pre-run prediction and subsequent UI execution chronology and actual procedural AI assistance are disclosed in Section 5. AI also assisted the post-run comparison and discrepancy analysis; the original prediction remains unedited.

## 7. Reproducibility and acceptance

`outputs/visible-summary.txt`, `baseline.json`, `stress_summary.json`, `historical_diagnostics.json`, `chronological_check.json`, `data-audit.json`, and `test-results.txt` expose material evidence without running the application. The locked UI export is additionally preserved in `locked-change-result.json`. On November 25, 2026, the student reported a successful second-device application run on his father's computer. His father followed the repository README setup instructions and successfully launched the application in approximately 8–9 minutes, with no reported errors. The student's latest clarification is that his father read the README without guidance; the earlier account described student guidance. This is a student-reported second-machine README run, not an independently observed setup. Fresh-environment status, exact repository revision, operating system, Python/package versions, exact commands and automated test count were not reported. A subsequent AI-assisted calculation check on November 25 used source files from the original enhanced package whose Git blob hashes matched the repository's engine, UI, input data, dependencies and test file. All 22 calculation tests passed again (0.445 seconds; Linux, Python 3.13.5, NumPy 2.3.5, pandas 2.2.3). The SOXX scenario reproduced 1,060 feasible allocations and both optimizer results. This is additional calculation evidence, not another human cold run or UI test.

The decision remains a paper-only PILOT (0% real capital). Data rights, prospective evidence, operational verification, access and committee approval must precede consideration of live allocation. See `pilot-monitoring.md` for specific monitor and stop triggers.


## 8. Recorded presentation evidence

The supplied recordings have measured durations of 146.826 seconds (Video 1), 269.254 seconds (Video 2), and 259.517 seconds (Video 3); each is within the applicable 3/5/5-minute limit. The timestamped transcripts and timed caption files in `docs/` were prepared from the supplied auto-caption files, not from the earlier scripts. ChatGPT corrected apparent recognition errors in finance terminology, ticker names and material figures using the corresponding script and visible project results; the precise spoken audio was not independently verified for each correction. The student must review the uncertain numerical corrections and publish the matching captions. See [submission manifest](submission-manifest.md) for actual timestamp indices and publication/access status. No YouTube publication or grading-access confirmation is claimed until the links and access have been checked.
