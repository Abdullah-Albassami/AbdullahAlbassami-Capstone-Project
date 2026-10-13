# Verification evidence index

Updated after Checkpoint G, 13 October 2026 (Asia/Riyadh), with owner-observed M01–M09 results. This index distinguishes executed evidence and its limits; [ACCEPTANCE_TESTS](ACCEPTANCE_TESTS.md) preserves actual outcomes. F's documentation-only checks remain historical; G genuinely reran fresh-installation/tests/browser/server verification. This reconciliation did not rerun application checks. Executable source, migrations and pins remain unchanged.

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
| G | Genuine clone/new venv/uncached pinned install/migrations/seed twice; **149 tests**, **39 Chrome checks**, **14 live HTTP/server checks** | [G report](CHECKPOINT_G_REPORT.md); G01–G07; automated readiness passed, human/external confirmation outstanding |
| Owner report after G | **M01–M09 PASS (user-observed), within reported scopes**, performed 13 October 2026 in local HelpDesk Pro | [Dated scenario outcomes](ACCEPTANCE_TESTS.md#required-final-manual-scenarios); final HD-10013 detail, whitespace errors, queries/pages, HD-10014/15 edits/cancellations, Category CRUD/access and live reports; no supplied browser metadata/screenshots |

A–E reports are historical records of their stages, including defects found and recovery checks. Their older feature states and test counts are not overwritten with today's totals. The most recent executable application change is **d207e0e0c31450d03fbaf1a24eaec8311f26dced** (E). G freshly cloned/tested **d89f8748a9de33050eeb20ee7720df1eb2c253a1** (F), whose app source is identical. G's candidate hash is delivered after commit; none is represented as an already-submitted revision.

## Historical E Django regression evidence (G rerun below)

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

At F, manual status was **M01 PARTIAL (user-observed), M02–M14 NOT RUN**. G subsequently executed automated setup M13; the later owner report adds M01–M09 observations as below. Use [human instructions](MANUAL_BROWSER_CHECKS.md) for remaining checks and record actual scope/date/references, adding browser/viewport metadata only when supplied. M13 has automated fresh-setup PASS, human repeat NOT RUN; M14 requires the student's own demonstration/technical explanation. Instructor scope/access/duration remain unconfirmed.

## Latest G evidence: genuine fresh checkout

G01 cloned committed source with `git clone --no-local` into a new temporary directory and created a new Python 3.14.7 venv. `pip --isolated install --no-cache-dir -r requirements.txt` downloaded pins; no original packages/DB/local configuration were copied. New runtime secret/passwords stayed private. The first sandbox DNS failure was corrected by approved network execution; installation succeeded.

[Fresh-checkout JSON](evidence/checkpoint-g/fresh-checkout.json) records eight successful commands, 19 applied migrations, exact seed-repeat snapshots including password hashes/timestamps, zero check/drift/pending/dependency errors and **149 tests PASS in 3.130s**. An activation assertion confirms the independent prefix. The additional no-cache pip check also passes. G02 reruns every test module counted above unchanged, rather than claiming the older E run as new evidence.

[Chrome G JSON](evidence/checkpoint-g/results.json) records **39 PASS** on Chrome/155.0.8059.40 using the fresh clone's .venv and separate disposable fixture/profile. [G desktop](evidence/checkpoint-g/dashboard-desktop.png), [G mobile](evidence/checkpoint-g/dashboard-mobile.png), [login](evidence/checkpoint-g/login-mobile.png), [long category](evidence/checkpoint-g/long-category-confirmation.png), [long ticket](evidence/checkpoint-g/long-ticket-confirmation.png) are actual captures. Coverage breakdown remains 34 page audits + 3 basic keyboard + guarded admin + combined journey. E artifacts remain historical and unchanged.

[Server G JSON](evidence/checkpoint-g/server-access.json) records **14 PASS** using an actual Django runserver, new secret, normal password hashing/CSRF and only the clone's disposable database. It covers reachable login/CSS, authentication/logout, role denial, creation/edit/comment/cancel/retention, 403/404/405/409, and report totals changing **12/8/2/2 → 13/8/2/3** after creation/cancellation. G's browser journey separately verifies **12/8/2/2 → 13/7/3/3** before stress fixtures. Report tests cover assignment/reassignment/resolution and per-row annotation changes, zeros and multiple related rows.

The first ad hoc server probe used DEBUG=false, so ordinary runserver returned 404 for CSS; the README's local DEBUG=true setting passed the corrected probe. Non-raw regex warnings in that discarded harness were corrected to raw strings, and the pip cache advisory was avoided in the no-cache check. No application defect or code change was needed. Disposable HTTP credentials were privately rotated after the seed-idempotency assertion; the working accounts were never touched. The server/browser fixture/profile stopped/removed on completion; the separately created clone/evidence workspace is disposed after retained evidence/parity checks.

G06 verifies the original database bytes and eight-table logical digest unchanged, with HD-10013 still resolved and **13/8/3/2** original counts. Numeric ticket 10013 created in a clone is independent of the preserved original HD-10013. G05 checks final documents, unchanged app source/pins/historical reports, ignored runtime files and tracked history for credential indicators. The local candidate commit is identified by Git at delivery; instructor remote access/submission is not inferred.

## Owner-observed acceptance after G — 13 October 2026

Current manual status: **M01–M09 PASS (user-observed, within reported scopes)**; **M10–M12/M14 pending human acceptance**; **M13 PASS (automated setup), human repeat NOT RUN**. Final HD-10013 note/time/thread and absence of modification controls were observed by employee1, technician1 and itadmin. Whitespace resolution validation used HD-10007; edit/assigned cancellation used HD-10014; New comment/cancellation used HD-10015. Full per-scenario expected/actual/status/date/limits are recorded in [ACCEPTANCE_TESTS](ACCEPTANCE_TESTS.md#required-final-manual-scenarios), without invented browser metadata or captures.

Dataset chronology: pristine seed **12/8/2/2**; G working snapshot **13/8/3/2**; later owner observation **15/8/3/4**. Before HD-10001 → technician2: statuses New/Assigned/In Progress/Resolved/Cancelled **3/3/2/3/4**, categories Hardware/Software/Network/Accounts/Unused **3/2/2/1/0**, Lina/Sami **3/2**. After assignment: New **2**, Assigned **4**, Sami **3**, overall active/category counts unchanged. These are historical observations, not a fixed live baseline; the earlier preservation digest remains evidence for its stage only.

Unreported facets remain unverified: additional invalid-value variants, completely empty queue, date/Low/tie ordering and detailed filter-preserving pagination, remaining edit fields/crafted requests, cancellation confirmation GET/Keep ticket back-out and separate In Progress cancellation. Broader M10/M11 role/reassignment/admin and M12 full human keyboard/zoom/device checks remain pending. Instructor scope/access/duration and M14 student understanding/rehearsal still require confirmation. Historical reports and UC01–UC07 remain unchanged; no executable or working-data mutations are authorized in this reconciliation.
