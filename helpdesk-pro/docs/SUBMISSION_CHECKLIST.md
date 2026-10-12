# Submission checklist and remaining confirmations

Finalized in G against the official [guide](../../CapstoneProjectGuide.pdf), pp.4–6. Checked entries mean the artifact or specifically labelled verification exists; they do not imply human acceptance, instructor access or submission. G stops after its verified milestone. Outstanding human/external actions require actual confirmation.

## Delivered artifacts

- [x] Source inside `helpdesk-pro/`: config, tickets app, templates, local CSS, four models, guarded admin, seed and tests. Root guide/specification retained.
- [x] Committed [initial migration](../tickets/migrations/0001_initial.py) and matching [ERD](ERD.md), including six FK deletion choices and four checks; schema test passed in G's fresh 149-test suite.
- [x] [Pinned dependencies](../requirements.txt): Django 5.2.18, asgiref 3.12.1, sqlparse 0.6.0; Python 3.14.7 verified. No extra frontend/application dependencies.
- [x] [Application README](../README.md) documents audience/value/roles, install/configure/migrate/seed/test/run, runtime-only passwords, ORM reports, limitations and AI/resources. [Root README](../../README.md) links the package.
- [x] Safe [.env.example](../.env.example), ignored secrets/environments/databases; actual credentials absent from tracked source. `.env` is not loaded automatically.
- [x] Final [architecture/permissions/lifecycle](DESIGN.md), [wireframes](WIREFRAMES.md), [100-mark matrix](REQUIREMENTS_MATRIX.md) and maintained [progress](PROGRESS.md).
- [x] [Acceptance record](ACCEPTANCE_TESTS.md), [evidence index](EVIDENCE_INDEX.md), E/G browser results/screenshots and meaningful test source; historical results and HD-10013 attribution preserved.
- [x] [Six-step demo and instructor questions](DEMO_SCRIPT.md), [remaining manual actions](MANUAL_BROWSER_CHECKS.md) and checkpoint delivery reports.

## Automated setup completed; human acceptance still open

- [ ] Execute M01 remaining employee/technician/admin final HD-10013 detail/thread/read-only checks without changing that record.
- [ ] Execute M02–M11 input/search/ordering/pagination/edit/cancel/Category/report/access/admin scenarios on fictional temporary records. Record expected/actual/status and notes in ACCEPTANCE_TESTS; counts will change after valid actions.
- [ ] Execute M12 desktop/mobile and full human keyboard/zoom/error usability. Record actual browser/device/viewport; explicitly list unavailable physical-device/other-browser/screen-reader checks as limitations rather than PASS.
- [x] M13 automated fresh setup: G cloned committed source, created a new venv, installed pins without cache, configured a new runtime key, migrated/seeded twice and passed checks/149 tests/server/39 Chrome checks. [Actual G results](CHECKPOINT_G_REPORT.md); no original environment/database/configuration copied.
- [ ] Independent human setup repeat, if requested by instructor: follow README in another checkout and record actual results; no human installation PASS has been reported.
- [x] Executed G checks pass with no known unresolved application defect; harness/configuration issues and recovery are documented. If human checks find a defect, fix it and rerun impacted checks before submission.
- [ ] Execute M14: student rehearses all six guide steps and personally traces a request, explains FK/constraints and calculates a report. Preparation by Codex is not student-understanding evidence.

## External confirmations

| Confirmation | Current status | Action / owner |
| --- | --- | --- |
| Instructor accepted this idea/workflow | Unconfirmed | Student asks instructor; record response/date, without claiming approval from repository evidence |
| Presentation duration and slot | Unconfirmed | Student obtains allotted duration; adjust pacing of the six-step script without changing order |
| Instructor repository access | Unconfirmed | Student supplies repository URL/access as required and asks instructor to open the submitted commit; never send credentials in source |
| Time available / final deadline | Unconfirmed | Student confirms actual deadline and remaining focused hours; original plan estimated 20 hours over two days, not an observed timesheet |
| Student explanation/rehearsal | NOT RUN | Student executes M14 and records actual rehearsal gaps/outcome |

## Candidate revision and remaining submission/access actions

- [ ] Confirm the intended repository/branch/remote through `git remote -v` and `git branch --show-current` privately; no repository URL is invented here.
- [ ] After all verified changes are committed, run these from the repository root:

```sh
git status --short
git log --oneline -8
git rev-parse HEAD
```

- [ ] Record the **full 40-character submitted commit hash** and repository URL in the submission form/release note as required by the instructor. G's delivery message identifies the full candidate commit. If later human evidence/corrections change the repository, obtain the new final hash from Git after committing; do not submit a placeholder or assume an earlier checkpoint is still HEAD.
- [ ] Demonstrate that exact commit. Check `git rev-parse HEAD` against the submission record, confirm a clean working tree and recheck the core journey. Use fictional data/private credentials and record the actual demo ticket reference and live metric baseline.
- [ ] Confirm instructor access to that revision. Pushing/publishing or sending messages is a separate user action unless specifically authorized; a local commit does not prove remote delivery/access.
- [x] G checks tracked source/history/runtime exclusion and retained screenshots/evidence for credentials/private data; no review flags found.
- [ ] Student rechecks final submitted revision hygiene after any further human evidence/corrections; historical reports stay.
- [ ] Supply source/design/evidence/demo package; include deployment URL only if actually deployed (deployment is outside this scope).

G records automated fresh-checkout results and delivers a local candidate hash. Remaining submission fields are **not confirmed**: instructor access/scope, presentation duration, final demo reference, student rehearsal, outstanding human observations and actual submitted revision. No remote publication, instructor approval or submission is performed by G.
