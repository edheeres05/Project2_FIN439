# Video 2 — Code and validation (maximum 5:00)

**Recording guide, not a transcript.** Screen recording with webcam on and clear audio. Explain in your own words. Opening: disclose ChatGPT (GPT-6 family) assistance, affirm ownership and say educational analysis, not investment advice.

| Planned time | Show and explain |
|---|---|
| 0:00–0:25 | Opening and repository layout. `app.py` is UI; `engine.py` is finance; bundled frozen data and requirements make execution reproducible. |
| 0:25–1:10 | Show monthly returns CSV, source audit and FRED reference. Explain arithmetic mean ×12, covariance ×12, annualized volatility and estimated excess-return score. Distinguish nominal first-year net estimate from CAGR. |
| 1:10–2:00 | Explain the discrete 5% grid, 53,130 combinations, 1,082 qualifying baseline candidates. Show both objective functions, the benchmark, one-way turnover versus both-side costs, and how each candidate gets an exact pass/fail verdict. |
| 2:00–2:50 | Show Portfolio construction tab and actual weights; demonstrate why maximum estimated Sharpe accepts more risk. Show historical and chronological diagnostic limitations: revised history, not untouched holdout, no actual policy enforcement in those paths. |
| 2:50–3:30 | Show actual 22-test run, data-audit checks, independent direct monthly-return calculation, and failure demonstration: set current drawdown 15% or volatility cap 5%, observe stop, then reset. |
| 3:30–4:30 | Show actual locked prediction commit followed by actual output and explain the discrepancy and decision effect. Show actual second-machine cold-run evidence (OS, version, elapsed time and any first error). Do not claim either before completed. |
| 4:30–4:55 | Explain why high in-sample means, sector overlap, costs, stale/missing data and no prospective validation matter. |

After recording, correct actual transcript and add actual timestamps. This guide is not evidence of a recorded video.
