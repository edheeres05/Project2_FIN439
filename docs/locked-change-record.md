# SOXX changed-input experiment — evidence and reproduction

The student committed the prediction before personally running the application on November 25, 2026. The changed input was a 10-percentage-point reduction in SOXX's annual expected return. See the [validation record](validation-and-ai-use.md#5-locked-changed-input-record--november-25-2026) for exact inputs, the chronology, before/after results, discrepancy diagnosis and AI-use disclosure.

- [Frozen baseline commit](https://github.com/edheeres05/Project2_FIN439/commit/4442c05594191d47a292a040d9ef974502b396de)
- [Original prediction commit](https://github.com/edheeres05/Project2_FIN439/commit/e6329aea9b34afa81649ae3ba40990d8e068c11f)
- [Original prediction](../ai-off-prediction.md)
- [Original baseline output](../outputs/baseline.json)
- [Original student UI export](../locked-change-result.json)

For optional post-experiment reproduction from a clean Git clone, install dependencies following the README and run:

```powershell
py run_locked_change.py --baseline-commit 4442c05594191d47a292a040d9ef974502b396de --prediction-commit e6329aea9b34afa81649ae3ba40990d8e068c11f
```

The helper was updated after the original experiment to match the actual root-level file paths. It checks Git order and unchanged calculation inputs and writes `outputs/locked-change-reproduction.json` separately; it does not overwrite or replace the original student export or attest AI-off authorship.
