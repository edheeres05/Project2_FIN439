# Project 2 submission manifest — working record

Edition A/B and research-evolution PDF: not required for Project 2. Attach the two matching Markdown reports and three plain-text transcripts to Brightspace. The recordings have been produced and the transcript files are present; YouTube publication and instructional-team access confirmation remain pending.

| Evidence | Location / status |
|---|---|
| Repository | [Project2_FIN439](https://github.com/edheeres05/Project2_FIN439); private; instructional-team access not yet confirmed |
| README | [README.md](https://github.com/edheeres05/Project2_FIN439/blob/main/README.md) |
| Runnable application | [app.py](https://github.com/edheeres05/Project2_FIN439/blob/main/app.py), [engine.py](https://github.com/edheeres05/Project2_FIN439/blob/main/engine.py), [requirements.txt](https://github.com/edheeres05/Project2_FIN439/blob/main/requirements.txt), [test_engine.py](https://github.com/edheeres05/Project2_FIN439/blob/main/test_engine.py) |
| Data and signal | [data/monthly_returns_pct.csv](https://github.com/edheeres05/Project2_FIN439/blob/main/data/monthly_returns_pct.csv), [data/risk_free.json](https://github.com/edheeres05/Project2_FIN439/blob/main/data/risk_free.json), [docs/data-provenance.md](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/data-provenance.md), [docs/signal-data-card.md](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/signal-data-card.md) |
| Visible executed output | [outputs/visible-summary.txt](https://github.com/edheeres05/Project2_FIN439/blob/main/outputs/visible-summary.txt), [outputs/baseline.json](https://github.com/edheeres05/Project2_FIN439/blob/main/outputs/baseline.json), [outputs/stress_summary.json](https://github.com/edheeres05/Project2_FIN439/blob/main/outputs/stress_summary.json), [outputs/data-audit.json](https://github.com/edheeres05/Project2_FIN439/blob/main/outputs/data-audit.json), [outputs/test-results.txt](https://github.com/edheeres05/Project2_FIN439/blob/main/outputs/test-results.txt), [outputs/historical_diagnostics.json](https://github.com/edheeres05/Project2_FIN439/blob/main/outputs/historical_diagnostics.json), [outputs/chronological_check.json](https://github.com/edheeres05/Project2_FIN439/blob/main/outputs/chronological_check.json) |
| Decision memo | [docs/decision-memo.md](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/decision-memo.md); attach matching .md |
| Validation and named AI use | [docs/validation-and-ai-use.md](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/validation-and-ai-use.md); attach matching .md |
| Locked experiment | [Baseline](https://github.com/edheeres05/Project2_FIN439/commit/4442c05594191d47a292a040d9ef974502b396de), [prediction commit](https://github.com/edheeres05/Project2_FIN439/commit/e6329aea9b34afa81649ae3ba40990d8e068c11f), [ai-off-prediction.md](https://github.com/edheeres05/Project2_FIN439/blob/main/ai-off-prediction.md), [locked-change-result.json](https://github.com/edheeres05/Project2_FIN439/blob/main/locked-change-result.json); see validation for AI assistance and chronology |
| Student AI-output check | BND source comparison in Section 6 of the validation record |
| Second-machine run / independent cold run | Student-reported successful second-computer README run by father (November 25), approximately 8–9 minutes, no errors. Latest clarification and evidence limits documented in validation. See [validation record](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/validation-and-ai-use.md). |
| Video 1: Research evolution and AI-output check | FIN 439 Project 2 — Video 1: Research Evolution and AI Verification; 2:27; YouTube link pending (Unlisted or Public) |
| Transcript 1 | [Timestamped transcript](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/transcript-video-1.txt) · [Timed captions for upload](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/captions-video-1.vtt) |
| Video 2: Codebase and validation | FIN 439 Project 2 — Video 2: Technical Walkthrough and Validation; 4:29; YouTube link pending (Unlisted or Public) |
| Transcript 2 | [Timestamped transcript](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/transcript-video-2.txt) · [Timed captions for upload](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/captions-video-2.vtt) |
| Video 3: Investment committee (opens with live app) | FIN 439 Project 2 — Video 3: Investment Committee Presentation; 4:20; YouTube link pending (Unlisted or Public) |
| Transcript 3 | [Timestamped transcript](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/transcript-video-3.txt) · [Timed captions for upload](https://github.com/edheeres05/Project2_FIN439/blob/main/docs/captions-video-3.vtt) |
| Research evolution document | Not required (Project 2 ruling) |
| Optional deployment | Not submitted |

## Timestamped video evidence index

Timestamps are taken from the supplied recordings' captions, rounded down to the nearest second. Video durations are rounded to the nearest second. The index refers to actual recorded narration, not the original scripts.

| Video | Timestamp | Evidence |
|---|---|---|
| 1 | 00:00–00:14 | AI announcement, student ownership, educational disclaimer |
| 1 | 00:15–00:47 | Intended investor, mandate and evolution to two optimizers |
| 1 | 00:49–01:04 | Changed data methodology and consistent 60-month return sample |
| 1 | 01:06–01:49 | Personally checked BND result: PortfoliosLab 2.37%, Digrin 2.74%, third source 2.37%; accepted supported total return |
| 1 | 01:51–02:25 | Comparison of both portfolios and final pilot decision |
| 2 | 00:00–00:20 | Required opening statements and app/engine architecture |
| 2 | 00:23–01:41 | Source dataset, estimate_from, metrics, optimize, constraints and estimated Sharpe |
| 2 | 01:43–02:10 | app.py, data flow into review, frontier and allocations |
| 2 | 02:12–02:34 | 22 tests and second-machine README run |
| 2 | 02:36–02:56 | Original precommitted prediction and predicted direction |
| 2 | 03:00–03:56 | Live SOXX change, actual before/after, discrepancy and decision effect |
| 2 | 04:00–04:26 | Drawdown stop demonstration and historical-estimate limitation |
| 3 | 00:00–00:20 | Live app, required disclosure and committee recommendation |
| 3 | 00:22–00:46 | Intended investor, five-year horizon and mandate |
| 3 | 00:48–01:59 | Benchmark, portfolio estimates, allocation range and trade-off |
| 3 | 02:00–02:49 | Stress scenarios and SOXX assumption sensitivity |
| 3 | 02:49–03:23 | Historical drawdown risk and limitations |
| 3 | 03:27–03:56 | 12-month pilot, monitoring and reversal triggers |
| 3 | 03:58–04:18 | Committee ask and zero real capital |

## Frozen-package checklist

- [x] Repository source, README and dependencies.
- [x] Visible executed output, dated input data, signal card and stress results.
- [x] Decision memo and validation record, including original prediction and changed-input output.
- [x] Three recorded videos within the time limits and three timestamped transcript files.
- [ ] Speaker review of apparent numerical caption errors against the actual audio; publish corrected captions on each YouTube video.
- [ ] Add the actual three stable YouTube links; verify playback and captions while logged out.
- [ ] Confirm instructional-team access to the private repository.
- [ ] Freeze final repository revision and submit this manifest, matching two Markdown reports and three plain-text transcripts in Brightspace.

No public redistribution of frozen source data without verified rights. No credentials or private data in repository.
