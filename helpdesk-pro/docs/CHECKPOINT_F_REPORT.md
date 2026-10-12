# Checkpoint F delivery report

13 October 2026 (Asia/Riyadh). Authorized scope: final documentation, grading evidence and demonstration preparation only. A–E reviewed/approved. The six-page official guide remains primary. No application feature, executable source, schema, migration, dependency or working record is changed. Stop before G; this milestone does not establish final submission readiness.

## Documentation completed and corrections

- Source-linked requirements matrix covers all eight assessment criteria totaling 100 marks and every normative guide requirement. Each feature points to actual files/symbols/routes/templates, executed verification and remaining human evidence.
- Complete application README documents problem/users/value/adoption assumptions, installed versions/pins, models/relationships, safe shell configuration, migration/seed twice/run/test, ORM reports, limitations and assistance/resources. Root README is a concise entry point.
- ERD/architecture/permission matrix/lifecycle reviewed against the unchanged models/migration and implemented behavior. Wireframes now reflect actual headings, role navigation, requester/created columns, named technicians, confirmations and scrollable tables.
- Evidence index consolidates A–E without rewriting historical reports. Latest regression remains E's 149 passing Django tests and 39 Chrome checks. UC01–UC07 retain user attribution; M01 remains partial and M02–M14 NOT RUN.
- Demo script follows the guide's exact six-step order, with source-linked request traces, metric arithmetic and likely instructor questions. It labels market benefits as assumptions and student rehearsal as unexecuted.
- Submission checklist separates delivered artifacts from outstanding human/G/external actions, including recording the exact submitted commit after final verified work. No remote access/submission or instructor agreement is implied by a local commit.
- Removed stale live-document “F awaiting approval” statements and a misleading matrix reproducibility row that implied completed fresh-checkout evidence. Historical checkpoint statements are preserved as historical results.

## Complete file inventory

**Created (3):**

- [EVIDENCE_INDEX.md](EVIDENCE_INDEX.md)
- [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)
- [CHECKPOINT_F_REPORT.md](CHECKPOINT_F_REPORT.md)

**Modified (11):**

- [Root README](../../README.md)
- [Root specification](../../HELPDESK_PRO_CODEX_SPEC_FINAL.md)
- [Application README](../README.md)
- [DESIGN.md](DESIGN.md)
- [ERD.md](ERD.md)
- [WIREFRAMES.md](WIREFRAMES.md)
- [REQUIREMENTS_MATRIX.md](REQUIREMENTS_MATRIX.md)
- [ACCEPTANCE_TESTS.md](ACCEPTANCE_TESTS.md)
- [PROGRESS.md](PROGRESS.md)
- [DEMO_SCRIPT.md](DEMO_SCRIPT.md)
- [MANUAL_BROWSER_CHECKS.md](MANUAL_BROWSER_CHECKS.md)

All 14 changes are Markdown. A–E checkpoint reports, Chrome JSON/PNG artifacts, all non-Markdown tracked files and the root PDF are byte-preserved from E. No package installation, seed execution, migration application, database reset, new browser run or full fresh checkout is performed in F.

## Actual verification

F01–F05 results are recorded in [ACCEPTANCE_TESTS](ACCEPTANCE_TESTS.md#checkpoint-f-documentation-verification). The full inventory above is checked before commit; the delivery message/Git history supplies the milestone hash. A hash of this file's own containing commit cannot be embedded in it without creating a different commit.

Executed environment/system/migration/dependency commands from `helpdesk-pro/`, with DJANGO_SECRET_KEY generated privately by an stdin Python wrapper:

```sh
.venv/bin/python -B manage.py check --database default
.venv/bin/python -B manage.py makemigrations --check --dry-run
.venv/bin/python -B manage.py migrate --check
.venv/bin/python -m pip --no-cache-dir check
```

Actual results: **zero system/database-check issues**, **no model changes**, **no pending migrations** (exit 0), **no broken requirements**. Installed Python 3.14.7, Django 5.2.18, asgiref 3.12.1, sqlparse 0.6.0 and SQLite 3.53.4 match the README/pins. No key is printed or stored.

Source/evidence review ran through `helpdesk-pro/.venv/bin/python -B -` stdin assertions and read-only Git inspection:

- `git status --short`, `git log -3 --oneline`, `git ls-files -z`, `git show d207e0e0c31450d03fbaf1a24eaec8311f26dced:<path>` and final `git diff --check` / `git diff --stat`.
- All **66 non-Markdown tracked files** compare byte-for-byte with E, including app/tests/migrations/config/pins/browser artifacts/PDF. A–E historical reports also compare unchanged.
- Python AST verifies the documented feature symbols and **149 test methods**. Existing test-count evidence is confirmed, not newly executed. No full regression/browser rerun is necessary for Markdown-only edits.
- Retained JSON validates **34 page audits + 5 other passing checks** on Chrome/155.0.8059.40: page widths, labels/error associations, unique IDs, landmarks, loaded CSS, zero measured contrast failures and explicit pass results for keyboard/admin/journey entries.
- UC01–UC07 and the entire M01–M14 manual-scenario section compare unchanged against E. No manual status is silently promoted.

An stdin read-only SQLite check (`sqlite3.connect('file:db.sqlite3?mode=ro', uri=True)`) verifies PRAGMA integrity `ok`, no foreign-key violations and HD-10013's resolved/requester/assignee/note/timestamp. All eight app/user/role tables match E's logical digest; database file bytes remain identical before/after F's Django checks. Counts: 4 departments, 5 categories, **13 tickets**, **5 comments**, 5 users, 5 memberships, 3 groups, 4 group permissions. Digest is in [EVIDENCE_INDEX](EVIDENCE_INDEX.md); no rows/password hashes are disclosed.

Markdown/link/path/setup/rubric hygiene passed by stdin inspection: **85 repository files, 19 Markdown documents, 207 local links/targets/fragments**, **8 shell blocks** parsed in bash/zsh, **15 application routes and 3 auth/admin logout reversals**, all eight rubric values totaling **100**, all 14 feature entries, exact 11 modified/3 created Markdown inventory, runtime exclusion and clean diff whitespace. These validate documentation and current configuration, not an executed install/server/fresh-checkout journey. Before committing, review `git diff`, stage only this inventory, check staged whitespace and inspect staged paths. After commit, report `git rev-parse HEAD` and `git status --short`.

## Remaining grading gaps and limitations

- Human M01 final HD-10013 detail/thread/terminal controls and M02–M12 browser/input/query/report/access/admin/full keyboard/zoom/device usability remain unexecuted as recorded. E automation supplies strong but bounded evidence; it does not replace required manual acceptance or certify accessibility.
- M13 full fresh checkout/environment is reserved for G after explicit approval. README instructions are source/command-consistent, but full clean-checkout execution cannot yet be claimed passed.
- M14 guide-ordered student rehearsal and personal technical explanation remain NOT RUN. The prepared script/Q&A are documentation, not proof of understanding.
- Instructor scope agreement, repository access, presentation duration/slot and actual remaining time/deadline remain externally unconfirmed. Final submitted commit and demo reference are captured after G, not fabricated in F.
- No known unresolved functional defect from the executed E checks. SQLite concurrency and privileged bulk/raw SQL validation bypass remain documented scope limits; no deployment/integrations or guaranteed grade.

Next proposed checkpoint is **G: separate fresh checkout, actual acceptance/readiness and rehearsal evidence**, after the user approves F. F does not start those actions or claim final submission readiness.
