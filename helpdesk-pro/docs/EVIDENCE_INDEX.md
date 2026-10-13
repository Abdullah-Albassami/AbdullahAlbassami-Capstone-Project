# Testing evidence

## Verified automated checks

| Check | Result | Source |
|---|---|---|
| Fresh environment, migration and repeatable seed | Pass | [Final verification report](CHECKPOINT_G_REPORT.md) |
| Django test suite | **149 passed** | [Tests](../tickets/tests/) |
| Real Chrome browser checks | **39 passed** | [Browser results](evidence/checkpoint-g/results.json) |
| HTTP/server checks | **14 passed** | [Final verification report](CHECKPOINT_G_REPORT.md) |
| Documentation link checks | Passed at final documentation audit | Historical local audit report |

The browser runner uses a separate temporary database and does not alter the working demo data.

## Human-observed checks

On **13 October 2026**, the project owner reported **M01–M09 PASS within the specific actions observed**, covering ticket lifecycle, validation, search, filtering, pagination, permissions, category management and reporting. See [acceptance details](ACCEPTANCE_TESTS.md).

M10–M12 and unreported subchecks have not been marked complete. Automated checks and human observations are distinct sources of evidence.
