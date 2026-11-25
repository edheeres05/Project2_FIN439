**AI use:** ChatGPT (GPT-6 family) assisted with research, implementation, calculations, validation and drafting. The investment mandate, ETF selection and paper-trading pilot decision are the student's; the student owns the analysis and decision.

**Educational analysis only; not investment advice.** This app places no trades.

# FIN 439 Project 2 | Five-year investment committee application

**Committee action: PILOT, paper trading only. Live allocation: 0%.** Compare minimum-volatility and maximum-estimated-Sharpe portfolios under the same mandate, alongside equal weight, inverse volatility and a 50/40/10 benchmark. The intended user is a college-aged or early-career investor with a flexible five-year financial goal, separate emergency savings, and no scheduled withdrawals during the research period. Do not use this process for money that must be available at a firm date regardless of losses.

## Run from a clean folder (Windows, VS Code)

Extract all contents, open the directory containing `app.py` in VS Code, and run these commands separately in the integrated PowerShell terminal:

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m unittest discover -s . -p test_engine.py -v
.\.venv\Scripts\python audit_data.py
.\.venv\Scripts\python generate_outputs.py
.\.venv\Scripts\python -m streamlit run app.py
```

Or double-click `RUN_WINDOWS.bat`. On macOS/Linux use `python3 -m venv .venv`, then `.venv/bin/python` in place of `.\.venv\Scripts\python`. Use Python 3.12 or 3.13; calculation environment verified on 3.13.5. Open http://localhost:8501 if Streamlit does not open a browser; stop with Ctrl+C. Dependency installation requires internet; app calculations use the bundled snapshot, no API keys or network data requests. If dependencies fail, preserve the exact error and Python version. Do not upload `.venv` or secrets.

## Investment mandate

- Five-year flexible goal; return objective estimated nominal annual net return ≥6%; estimated annualized volatility ≤15%; minimum BIL 5%; rolling annual one-way turnover ≤25%; no shorting, leverage or derivatives.
- Monthly review; planned annual rebalance. A 15% measured account drawdown or nonpositive trailing 12-month VOO return pauses new risk. Missing/corrupted data, no feasible allocation or >45-day-old source stops review; no automatic forced sale or relaxation.
- VOO large-cap U.S. equity, QQQ growth tilt, SOXX semiconductor thesis, SCHD dividend equity, BND broad investment-grade bonds, BIL short Treasury bills. The universe is student-selected, not forced weights. Benchmark / default hypothetical pre-trade holdings: 50% VOO, 40% BND, 10% BIL.
- Base 10 bps per dollar bought or sold (assumption, not actual broker quote). Model first-year return net of estimated transition cost; taxes excluded.

## Frozen baseline, November 24, 2026

Sixty completed monthly total returns, Nov 2021–Oct 2026, transcribed from PortfoliosLab single-provider tables. Rounded source percentages; historical vintages are not available. Source and annual-reconciliation checks in `docs/data-provenance.md`. FRED DGS3MO annual reference 4.37%, Nov 23 observation published Nov 24 3:16 p.m. CST. The app rejects dates earlier than capture. Latest complete October observation, final session October 30. Positive VOO trailing 12-month signal 12.09%, not validated alpha. 1,082 of 53,130 5%-step grid allocations meet numerical rules.

| Candidate | Net estimate | Annual vol | Est. Sharpe | Turnover | Verdict |
|---|---:|---:|---:|---:|---|
| Equal weight | 11.87% | 13.83% | 0.542 | 56.67% | Fail |
| Inverse volatility | 4.21% | 1.85% | -0.086 | 80.98% | Fail |
| Benchmark | 6.68% | 9.58% | 0.242 | 0% | Pass |
| Minimum volatility | 6.28% | 7.35% | 0.260 | 25% | Pass |
| Maximum estimated Sharpe | 12.24% | 14.18% | 0.555 | 25% | Pass |

Minimum volatility = 40% VOO / 35% BIL / 25% BND. Maximum estimated Sharpe = 50% VOO / 15% SOXX / 10% SCHD / 10% BIL / 15% BND. Both use the same policy. The additional estimated return of the latter comes with higher volatility, 75% equities, historical mean sensitivity and narrow volatility headroom; a hindsight fixed-target diagnostic shows a 22.15% drawdown (above the stop threshold). Compare both in a paper pilot; no live allocation approved. The expected returns are estimates derived from historical monthly total returns, not forecasts of guaranteed future performance. In particular, SOXX's 29.92% annualized historical arithmetic mean should not be interpreted as an expected realized return over the next five years. The app's retrospective and chronological charts are diagnostics, not demonstrated prospective skill.

## Use the five tabs

1. **Committee decision:** compare portfolio weights, estimates, risk-adjusted scores and exact failed rules. Sidebar holds current policy/holdings, scenario inputs and decision date; invalid or stale inputs stop the process.
2. **Portfolio construction:** feasible risk-return cloud, nondominated frontier, allocation chart and table. Grid search is discrete, not a continuous optimum.
3. **Stress tests:** explicit estimate, window, trading-cost, reserve, turnover, volatility, drawdown and Treasury-rate scenarios. The student-locked SOXX-specific change is not auto-run.
4. **Historical diagnostics:** fixed-target hindsight returns/drawdown; separate chronological 36/24 estimation challenge with historical Treasury reference. No policy-enforced or vintage historical backtest.
5. **Data & methods:** source/date, asset estimates, cost conventions and JSON export.

## Code, evidence, and reproducibility

`engine.py` is the calculation layer; `app.py` the UI. `build_data.py` rebuilds the frozen CSV from transcribed rounded source values; `audit_data.py` independently reconciles annual totals and cross-source differences. `generate_outputs.py` writes visible results without running Streamlit. Tests check both optimizers using a separate direct-monthly-return implementation, known answers, source integrity, stops, feasibility and path calculation. `outputs/` contains the executed baseline, stress results, diagnostics, data audit and calculation-test log. 22 calculation tests passed in the Linux calculation environment and on the student's Windows machine (0.524 seconds); the student also launched the revised UI. The student's father followed the README setup instructions with the student's guidance on November 25, 2026. The application launched successfully on the second computer in approximately 8–9 minutes, with no reported errors. This was a guided README run; see the validation record for limitations.

- [Decision memo](docs/decision-memo.md)
- [Validation and AI use](docs/validation-and-ai-use.md)
- [Provenance](docs/data-provenance.md) and [signal card](docs/signal-data-card.md)
- [Pilot monitoring](docs/pilot-monitoring.md)
- [Visible baseline](outputs/visible-summary.txt)
- [Original pre-run prediction](ai-off-prediction.md) and [executed changed-input result](locked-change-result.json)
- [Student evidence steps](docs/student-evidence-steps.md) and [submission checklist](docs/submission-manifest.md)

Source: PortfoliosLab monthly tables for six tickers; FRED series DGS3MO; historical U.S. Treasury yield table. Exact URLs, date boundaries, definitions and discrepancies are in provenance. Source redistribution permission has not been established; restrict course-evaluation access rather than assuming open licensing. No private account or credentials.

The earlier AI-assisted 10→30 bps experiment is exploratory, not the formal AI-off precommit. The student wrote his own SOXX prediction and committed it before personally executing the experiment on November 25; explanatory AI interactions are disclosed in the validation record. The student also checked BND's October total return across three sources. The reported second-device run is documented; independent cold-run details, recordings, actual transcripts and final manifest remain outstanding. Project instructions: https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/project-2-investment-management-application.md.
