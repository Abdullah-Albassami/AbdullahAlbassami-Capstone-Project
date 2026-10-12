# Verification evidence index

Consolidated in Checkpoint F, 13 October 2026 (Asia/Riyadh). This index describes executed evidence and its limits; [ACCEPTANCE_TESTS](ACCEPTANCE_TESTS.md) preserves scenario/expected/actual/status records. F modifies Markdown only, retaining executable source, migrations, pins and E artifacts. It does not rerun or relabel historical tests as new results.

## Checkpoint history and evidence types

| Stage | Executed evidence | Scope / reference |
| --- | --- | --- |
| A | Installed verified Python 3.14.7/Django 5.2.18 pins; system/config/template/static/HTTP/dependency/path checks | [A report](CHECKPOINT_A_REPORT.md); A01–A07 and amended R01–R08; foundation only, no business schema/browser claim |
| B | **60 Django tests**; migrations applied; seed twice and known math; independent temporary SQLite migration/seed | [B report](CHECKPOINT_B_REPORT.md); B01–B08; database/auth/admin/seed foundation |
| C | **101 Django tests** (60 + 41); normal-hasher/CSRF HTTP persisted journey in temporary SQLite | [C report](CHECKPOINT_C_REPORT.md); C01–C08; server/HTTP/HTML evidence, not real-browser observation |
| User report at D | **UC01–UC07 PASS (user-observed)**: HD-10013 employee login/create/comment, admin assignment, technician login/visibility/start/resolve, employee dashboard Resolved | [Original recorded observations](ACCEPTANCE_TESTS.md#user-observed-checkpoint-c-browser-verification-hd-10013); recorded 12 October, browser execution date/viewport unspecified; final employee thread/detail/controls not reported |
| D | **133 Django tests** (101 + 32); normal-hasher/CSRF Category/query/report HTTP integration; live read-only 13/8/3/2 counts | [D report](CHECKPOINT_D_REPORT.md); D01–D08; related filtering, aggregation/annotation and edge cases integrated in pages |
| E | **149 Django tests** (133 + 16), passing in **3.127s**; **39 real headless Chrome checks**; system/database/migration/dependency/hygiene checks | [E report](CHECKPOINT_E_REPORT.md); E01–E08; fixed actual audit defects, preserved working database |
| F | Guide/source/document audit, links/paths/setup contract/evidence validation, read-only preservation and hygiene | [F report](CHECKPOINT_F_REPORT.md); F01–F05; documentation only; G not started |

A–E reports are historical records of their stages, including defects found and recovery checks. Their older feature states and test counts are not overwritten with today's totals. The latest verified application commit is **d207e0e0c31450d03fbaf1a24eaec8311f26dced** (E); F's documentation commit is identified in delivery/Git history, not treated as a final submitted revision.

## Latest Django regression evidence

The final E suite executed all **149 test methods**, with no failures and a fresh migrated test database created/destroyed. The following source modules remain unchanged in F:

| Module | Methods | Behavior covered |
| --- | ---: | --- |
| [test_models.py](../tickets/tests/test_models.py) | 19 | ERD/schema/FKs/checks, text validation, state invariants, relationships and all deletion choices |
| [test_permissions.py](../tickets/tests/test_permissions.py) | 17 | PermissionTests (8), AccountSafeguardTests (9): roles/current flags, object scope, eligible targets, membership/account guards |
| [test_admin.py](../tickets/tests/test_admin.py) | 11 | Read-only Ticket/Comment, Department-only staff setup, protected deletion and guarded account/group provisioning |
| [test_seed.py](../tickets/tests/test_seed.py) | 13 | Determinism/idempotency, password/edit preservation, known math, reserved collisions, atomic rollback and terminal history |
| [test_services.py](../tickets/tests/test_services.py) | 12 | Complete ticket mutations, current-state validation, terminal restrictions, reassignment, actor/field protection |
| [test_views.py](../tickets/tests/test_views.py) | 29 | Login/logout, CSRF, scoped GET/POST, forged fields, errors/feedback and complete persisted role journey |
| [test_categories.py](../tickets/tests/test_categories.py) | 9 | CRUD/service/role/method/CSRF/value checks and active/terminal PROTECT behavior |
| [test_queries.py](../tickets/tests/test_queries.py) | 12 | Q search, combined related filters, stable ordering, page boundaries, sanitized query links, empty/invalid/scope cases |
| [test_reports.py](../tickets/tests/test_reports.py) | 11 | Aggregate/annotation integration, known/zero/empty/live math, join inflation and role/eligibility guards |
| [test_reliability.py](../tickets/tests/test_reliability.py) | 16 | Account-message privacy, readable names, 405/cache headers, stale eligibility/roles, extreme inputs, CSRF rotation and terminal regressions |
| **Total** | **149** | Meaningful rules/calculations; no coverage-percentage claim |

E's principal commands, from `helpdesk-pro/` with a privately generated runtime DJANGO_SECRET_KEY:

```sh
.venv/bin/python -B manage.py check --database default
.venv/bin/python -B manage.py makemigrations --check --dry-run
.venv/bin/python -B manage.py migrate --check
.venv/bin/python -B manage.py test tickets.tests --verbosity 1
.venv/bin/python -m pip --no-cache-dir check
```

Results: zero system issues; no model changes; no unapplied migrations; 149 tests PASS; no broken requirements. These ran through private-environment stdin wrappers, not with a committed key. Fast hashing is confined to Django test overrides; production settings and seeded/browser HTTP integration use Django's normal password hashing. Tests create separate data and do not mutate the working demo database.

## Actual Chrome evidence

[results.json](evidence/checkpoint-e/results.json) records **Chrome/155.0.8059.40** and **39 results**. Earlier E runs used Chrome 154.0.8037.99; the final artifact is the version above. Existing Node 21.7.2/installed Chrome and CDP were used, with no new packages.

- **34 page/viewport audits:** actual renders at 1280px/375px; page width, unique IDs, form labels/error associations, landmarks, loaded CSS and selected computed text/control contrast. Checked contrast failures: zero.
- **3 keyboard checks:** skip link/visible focus/Enter, native technician selection and ArrowRight table scrolling.
- **1 guarded-admin check:** Ticket/Comment read-only and active-technician deactivation rejected.
- **1 combined role journey:** login/assignment/start/comment/resolution/read-only outcome, authorization/validation/cancellation, Category CRUD/PROTECT and query edge states.

Actual captures: [login mobile](evidence/checkpoint-e/login-mobile.png), [dashboard desktop](evidence/checkpoint-e/dashboard-desktop.png), [dashboard mobile](evidence/checkpoint-e/dashboard-mobile.png), [long category confirmation](evidence/checkpoint-e/long-category-confirmation.png), [long ticket confirmation](evidence/checkpoint-e/long-ticket-confirmation.png).

Executed from the repository root:

```sh
HELPDESK_BROWSER_EVIDENCE=/private/tmp/helpdesk-e-evidence node helpdesk-pro/scripts/verify_browser.mjs
```

The [fixture](../scripts/browser_fixture.py) rejects an existing database; the [runner](../scripts/verify_browser.mjs) creates its own temporary SQLite database and Chrome profile, uses runtime-only credentials/normal hashing/CSRF, and removes server/database/profile on completion. It retains screenshots/JSON separately. Browser-only setup superuser exists solely in that temporary database. Images depict fictional disposable fixtures, not the working HD-10013 data.

This is real-browser automation, not physical mobile testing, a full keyboard-only human journey, 200% zoom/screen-reader review, WCAG certification or Checkpoint G fresh-checkout verification. F validates the retained artifacts and unchanged relevant source without rerunning Chrome or inventing new browser observations.

## Working data and human evidence

E and F read-only checks preserve 4 Departments, 5 Categories, **13 tickets**, **5 comments**, 5 users, 5 memberships, 3 groups and 4 group permissions. HD-10013 remains Resolved with requester 9001, technician 9003 and a resolution note/timestamp. Logical snapshot SHA-256 across those eight tables at both checks:

`8d55195964b920600d6f5d015d8ed07629155211deb4a68a0f3b0f62ff781fbf`

No account login, seeding, migrations application or reset is performed against the working database in F. The digest is a preservation check, not a submitted database or disclosure of rows/password hashes. Fresh seed expectations (12/8/2/2) differ from the preserved working values (13/8/3/2); later valid actions will change them.

Manual status remains **M01 PARTIAL (user-observed), M02–M14 NOT RUN**. Use [human instructions](MANUAL_BROWSER_CHECKS.md) and record actual observations, browser/version/viewport/date and failures. M13 is G's full fresh checkout; M14 requires the student's own demonstration/technical explanation. Instructor scope/access/duration remain unconfirmed. Documentary completeness in F does not close those readiness gaps.
