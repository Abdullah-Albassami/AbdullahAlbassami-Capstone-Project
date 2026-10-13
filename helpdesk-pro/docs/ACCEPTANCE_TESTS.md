# Verification record

Only executed or explicitly user-observed checks may be marked PASS, with their source named. NOT RUN means planned/unobserved. Command-level HTTP/template checks are not real browser walkthroughs. Historical A–E records remain separate from F's documentation audit; [EVIDENCE_INDEX](EVIDENCE_INDEX.md) consolidates evidence without rewriting its provenance.

## Historical Checkpoint A checks before the structure amendment

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| A01 | Local package installation | Exact selected Django and valid dependencies | Django 5.2.18, asgiref 3.12.1, sqlparse 0.6.0 installed | PASS | Initial sandbox network failure; approved retry succeeded |
| A02 | Django system check | No issues with temporary runtime key | System check identified no issues (0 silenced) | PASS | Python source syntax also parsed successfully; no schema created |
| A03 | Missing/example secret | Useful configuration failure, no tracked secret | Both subprocess checks rejected configuration with the intended message | PASS | Fresh random key existed in process environment only |
| A04 | Invalid debug/wildcard host | Configuration rejected | Invalid debug, wildcard and empty hosts all rejected | PASS | Explicit local host configuration |
| A05 | ASGI/WSGI and shared template/static lookup | Entry points load; inherited layout and stylesheet resolve | Both entry points callable; landmarks, escaped message and CSS lookup confirmed | PASS | Django template rendering, not browser verification |
| A06 | Anonymous admin login HTTP | GET renders login without database queries | Login GET 200; admin index redirects to login; zero queries and no db.sqlite3 | PASS | Django test client; not an authenticated/database test |
| A07 | Repository hygiene | No key/password/environment/database tracked; clean whitespace | Reviewed 23 source/design files; ignored runtime files verified; dependency pins match; diff whitespace clean | PASS | No database created; tracked example contains no real credential |

Executed on 12 October 2026 using the local virtual environment. Ad hoc command assertions checked source syntax, configuration rejection, entry-point/template/static integration and unauthenticated admin HTTP behavior. `pip check` returned “No broken requirements found.” The first `git diff --check` detected trailing whitespace on three edited Markdown lines; those lines were corrected before final verification. No test-suite PASS, migrations, browser walkthrough or final fresh-checkout result is claimed.

These results apply to the earlier repository-root foundation. The latest user amendment requires the application inside `helpdesk-pro/`. The new environment/path checks below are separate; historic PASS results are not presented as revalidation.

## Amended Checkpoint A revalidation

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| R01 | Compatibility before new install | Supported Django and Python 3.14.7; compatible pinned metadata | Official Django 5.2 support starts for Python 3.14 at 5.2.8; 5.2.18 supported through April 2028; package metadata requires >=3.10 | PASS | Official docs and existing package metadata read before new install |
| R02 | Fresh environment in helpdesk-pro | Exact pins installed; interpreter/activation point to new path | Python 3.14.7; Django/asgiref/sqlparse match pins; activation/prefix use helpdesk-pro/.venv; pip check found no broken requirements | PASS | Old virtual environment not relocated |
| R03 | Django check in corrected directory | Zero system-check issues | Both application-cwd and root-cwd subprocesses reported no issues | PASS | Runtime-only random key |
| R04 | Config rejection and local defaults | Missing/example keys, invalid debug/hosts rejected; valid local/debug-false settings accepted | Missing/example/blank key, invalid debug, wildcard/empty hosts rejected; debug-false/default-host check passed | PASS | All subprocess outcomes asserted |
| R05 | App path independence | BASE_DIR/database/template/static paths under helpdesk-pro, even invoked from root | All paths point under helpdesk-pro; built-in User and one custom app confirmed | PASS | No database created |
| R06 | Entry points, template and static integration | ASGI/WSGI load; layout/escaping/CSS resolve | Entry points callable, inherited blocks/landmarks/message escaping correct, CSS resolves at new path | PASS | Template checks, not browser |
| R07 | Foundation HTTP behavior | Admin login 200, anonymous admin redirect, no database queries; app routes still absent | Login 200, redirect 302, CSRF rejection 403; future routes unresolved; debug-false 404s; zero queries/no DB files | PASS | Debug-true root displays Django's own welcome page, not a dashboard |
| R08 | Repository/doc hygiene and file inventory | Root guide intact; no tracked runtime secrets/DB; local links resolve; clean whitespace | Exact 25-file source inventory; guide and 15 relocated files byte-preserved; all local links resolve; ignore rules and diff check passed | PASS | Root contains source documents/entry point/ignore only; no duplicate application or DB |

See CHECKPOINT_A_REPORT.md for the amended file inventory, commands and results. The relocation preflight initially stopped safely because the target directory already existed; inspection showed it was empty, so it was reused without overwriting data.

The first relocated verification harness passed R02–R06, then failed an assertion expecting `/` to return 404 with DEBUG=true. Inspection confirmed Django's normal development welcome response when only admin is configured. The corrected R07 check asserts absence of business URL patterns, the debug welcome page, and 404s with DEBUG=false; that rerun passed. This was a corrected check assumption, not an implemented dashboard. No business suite, migration or browser acceptance PASS is claimed.

## Checkpoint B executed verification

Executed on 12 October 2026 in helpdesk-pro using Python 3.14.7 / Django 5.2.18. Runtime keys/passwords were generated in process memory, never printed or committed.

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| B01 | Runtime/dependency consistency | Verified pinned environment, no new packages | Python/Django/asgiref/sqlparse unchanged; pip check reports no broken requirements | PASS | No dependency installation needed |
| B02 | Generate/apply migrations | Four final custom tables and auth prerequisites | makemigrations tickets generated 0001_initial; migrate --noinput applied all migrations successfully | PASS | Working ignored SQLite database |
| B03 | System/schema consistency | No checks, migration drift or pending migrations | check --database default: zero issues; makemigrations --check --dry-run: no changes; migrate --check: exit 0 | PASS | Final schema unchanged after validation fix |
| B04 | Automated foundation suite | Model/constraint/relationship/role/account/seed behavior correct | Final 60 tests passed, no failures, fresh migrated test DB created/destroyed | PASS | Fast hashing only in test overrides |
| B05 | Guarded admin server requests | View-only ticket/comment even for superuser; safe provisioning/protected deletion | AdminTests pass: change/add/delete bypasses 403, valid provisioning persists hashed credentials, invalid account changes return form errors/no mutation | PASS | Django test client; real browser M11 remains NOT RUN |
| B06 | Repeated actual seed and known metrics | Same records/passwords/timestamps on repeat; 12/8/2/2 totals | First seed 12 new, second 0 without password; exact snapshots preserved; category 3/2/2/1/0 and technicians 3/2 | PASS | Normal runtime hasher; local DB; CLI math is not rendered report evidence |
| B07 | Independent fresh SQLite reproducibility | Migrations/role bootstrap/seed/integrity work without original DB | New temporary file migrated; three groups/four IT permissions; seeded twice; constraints/system check passed; file removed | PASS | Not a complete fresh checkout/environment/browser setup |
| B08 | Source/Git/link/secret hygiene | Guide/dependency pins unchanged; runtime DB/credentials ignored; docs links/whitespace valid | 45 source files checked; guide/config/pins unchanged; local links/Python syntax valid; runtime ignored; no literal credentials; diff whitespace clean | PASS | Final staged check repeated before commit |

Initial results were not hidden: a first ad hoc migration wrapper omitted DJANGO_SETTINGS_MODULE and stopped before executing migrations; the corrected wrapper invoked manage.py properly and succeeded. The first 53-test run had one failure: optional non-null text could contain None because Django skips blank-enabled fields. Explicit model rejection fixed that defect; 53 tests passed on rerun, then two meaningful seed recovery cases were added and an interim 55-test run passed. No unexecuted UI check is marked PASS.

Code review also reproduced a deletion bypass when a reserved Group's name was changed only in memory before delete. Its targeted regression initially failed. The pre-delete guard now checks the persisted database name; its regression brought the intermediate suite to 56 passing tests.

The same review reproduced two unsaved-user-flag bypasses in role resolution and forward membership validation. Both targeted checks failed before fixes. Roles and membership guards now read current persisted flags, including stale deactivation and unsaved-user cases; that 58-test run passed. Admin superuser permissions also check persisted state, and valid multi-role superuser demotion reduces memberships before saving flags inside the existing admin transaction. The final suite has 60 passing tests; migration/system checks passed again. Smaller totals above describe intermediate results.

Exact principal commands, all from helpdesk-pro with a private runtime DJANGO_SECRET_KEY:

```sh
.venv/bin/python -B manage.py makemigrations tickets
.venv/bin/python -B manage.py migrate --noinput
.venv/bin/python -B manage.py check
.venv/bin/python -B manage.py test tickets.tests --verbosity 2
.venv/bin/python -B manage.py test tickets.tests --verbosity 1
.venv/bin/python -B manage.py makemigrations --check --dry-run
.venv/bin/python -B manage.py migrate --check
.venv/bin/python -B manage.py check --database default
.venv/bin/python -B manage.py seed_demo
.venv/bin/python -B manage.py seed_demo
.venv/bin/python -m pip --no-cache-dir check
```

The subprocess commands above were launched by stdin Python wrappers that generated keys/passwords without printing them. The second real seed ran with DEMO_PASSWORD removed. An additional stdin harness pointed settings at a temporary fresh SQLite file before Django setup, invoked migrate/seed twice/check, asserted exact snapshots/groups/counts and removed the file. Root commands git diff --check and git diff --cached --check plus source/link/ignore assertions establish B08; full command/file detail is in CHECKPOINT_B_REPORT.md.

## Historical Checkpoint C executed verification

Executed 12 October 2026 under Python 3.14.7 / Django 5.2.18. No new packages, schema changes or real credentials. Runtime secrets stayed in process memory.

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| C01 | System/database/dependency checks | No system/dependency issues | check --database default: zero issues; pip check: no broken requirements | PASS | Same verified dependency pins |
| C02 | Migration/ERD consistency | No model drift or pending migrations | makemigrations --check --dry-run: no changes; migrate --check: exit 0; B schema/deletion tests still pass | PASS | Model/migration/ERD files unchanged |
| C03 | Full automated suite | Existing foundation plus complete workflow/security behavior | 101 tests passed in 2.076s; fresh migrated test DB created/destroyed | PASS | 60 B + 41 C; not a coverage-percentage claim |
| C04 | HTTP security/error semantics | Authentication/scope/action/state/method/CSRF enforced server-side | WorkflowViewTests pass for 302/403/404/405/409; invalid forms 200; success redirects; CSRF enforced client verifies rejection/success | PASS | Role/ownership/forged identity and metadata; logout POST only; state re-fetch |
| C05 | Related display, role dashboard and workflow persistence | Own/assigned/all summaries and related thread; saved outcomes | Service/HTTP tests verify role counts, related objects, complete journey, retained cancellation and reassignment revocation | PASS | Dashboard summary aggregate is integrated; complete reports/annotation remain D |
| C06 | Fresh seeded HTTP integration using normal hashing | Seed twice unchanged; CSRF-protected journey; persisted terminal outcomes | Temporary SQLite migrated, seed repeated with exact snapshots; initial 12/8/2/2; resolved seeded ticket and created/edited/commented/cancelled another; after connection reopen total 13/active 7/resolved 3/cancelled 3 | PASS | Django HTTP client; not browser; working demo DB untouched; temporary file removed |
| C07 | Rendered HTML/form/static integration | Labels target unique IDs, semantic landmarks, POST/CSRF forms, CSS resolves | Parsed login/dashboard/list/detail/create/edit/cancel renders meet all assertions; stylesheet lookup succeeds | PASS | No browser viewport/keyboard/rendering claim |
| C08 | Source/Git/document hygiene | Unchanged schema/pins/guide; no secrets/generated files; valid links/syntax/whitespace | 61 files, 43 local links, Python syntax, exact 13 modified/16 created inventory, protected baseline and runtime exclusion checked; diff whitespace clean | PASS | Final staged hygiene also checked before commit |

The first 37-test targeted run reported four errors from dereferencing a null assignee in a template filter argument and one assertion failure from an unconsumed prior success message when the test changed roles with force_login. Explicit assignee conditionals fixed the template defect; following the assignment redirect corrected that test setup. The next targeted run found one assertion that fetched the success page twice (assertRedirects already consumed the message); fetch_redirect_response=False corrected it. Then 100 tests passed. The final aggregate summary query was verified in the full suite; a query-free server-error regression raised the final total to 101 passing tests. Earlier failures are not presented as passes.

Exact principal commands (from helpdesk-pro; private runtime DJANGO_SECRET_KEY):

```sh
.venv/bin/python -B manage.py check
.venv/bin/python -B manage.py test tickets.tests.test_services tickets.tests.test_views --verbosity 2
.venv/bin/python -B manage.py test tickets.tests.test_services tickets.tests.test_views --verbosity 1
.venv/bin/python -B manage.py test --verbosity 1
.venv/bin/python -B manage.py check --database default
.venv/bin/python -B manage.py makemigrations --check --dry-run
.venv/bin/python -B manage.py migrate --check
.venv/bin/python -B manage.py test tickets.tests --verbosity 1
.venv/bin/python -m pip --no-cache-dir check
```

Management commands ran through stdin subprocess wrappers generating the secret privately. An additional `.venv/bin/python -B -` harness configured a temporary SQLite path before Django setup, invoked migrate/seed twice, asserted exact data/password snapshots, and used Client(enforce_csrf_checks=True) for login, assignment, start, comment, resolution, submission/edit/cancellation/logout. It parsed the rendered HTML, reopened the connection to verify persisted state, ran database checks and removed the temporary file. Test classes reproduce the security/workflow behaviors; CHECKPOINT_C_REPORT records command and file detail. This is HTTP/database integration evidence, not final fresh-checkout or manual/browser evidence.

## User-observed Checkpoint C browser verification: HD-10013

Recorded 12 October 2026 from the user's Checkpoint D authorization request. These are **user-observed browser checks**, not Codex-executed browser tests. The browser execution date/viewport were not specified. Codex's separate read-only database check confirms HD-10013 is resolved with requester 9001, assignee 9003 and resolution note/timestamp present; that corroboration does not establish additional browser observations.

| ID | Scenario | Expected | Actual reported by user | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| UC01 | Employee login and ticket creation | Employee can sign in and persist a support request | HD-10013 created through browser | PASS (user-observed) | No credentials recorded |
| UC02 | Employee comment creation | Employee can comment on own active request | Employee comment created on HD-10013 | PASS (user-observed) | No claim about final thread visibility |
| UC03 | IT Admin assignment | Assign an eligible technician; status Assigned | HD-10013 assigned to technician1 | PASS (user-observed) | User-reported admin action |
| UC04 | Technician login and ticket visibility | Assigned technician can sign in and see assigned request | Technician signed in and saw HD-10013 | PASS (user-observed) | No claim about unrelated-ticket restrictions |
| UC05 | Start progress | Assigned → In progress | HD-10013 moved to In progress | PASS (user-observed) | User-reported browser transition |
| UC06 | Resolution | In progress → Resolved | HD-10013 resolved through browser | PASS (user-observed) | Database separately confirms note/timestamp presence |
| UC07 | Employee dashboard outcome | Employee sees saved Resolved status | Employee dashboard showed HD-10013 as Resolved | PASS (user-observed) | Final detail/thread/read-only controls unobserved |

Final terminal control visibility, employee resolution/thread detail, new D browser cases, mobile/keyboard and fresh checkout are **not** covered by these reported observations.

## Checkpoint D executed verification

Executed 12 October 2026 with existing Python 3.14.7 / Django 5.2.18. No new dependencies, schema/migration changes or resets of the working database.

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| D01 | Category CRUD, validation, permissions, CSRF and PROTECT | Valid CRUD persists; unused delete only; safe errors; role enforcement | CategoryTests pass create/list/detail/update/confirm/delete, trimming/duplicates, GET/POST/CSRF, service guards and active/terminal reference protection | PASS | HTTP integration, not manual browser |
| D02 | Scoped search/filter/order/pagination | Q title/description search, AND filters, category relationship, priority rank, stable pages and sanitized links | TicketQueryTests pass 12 scenarios covering all orders, tie-breakers, ten/page, malformed/repeated/huge/nonpositive/out-of-range params, no results and cross-role isolation | PASS | Only cleaned parameters preserved |
| D03 | Aggregation/annotation and correctness | Live zero-safe counts, no inflated joins or report leakage | ReportingTests pass known 12/8/2/2 and 3/3/2/2/2 statuses; categories 3/2/2/1/0, technicians 3/2; zeros/empty/multi-comment/group/eligibility/state-update cases | PASS | Actual rendered dashboard/category features, not shell-only evidence |
| D04 | Complete regression suite | Foundation and lifecycle remain correct with D | 133 tests passed; fresh migrated test DB created/destroyed; no failures | PASS | 101 existing + 32 D tests; C absent-route assertion updated to Employee denial |
| D05 | Fresh seeded HTTP/HTML integration | Normal hashing, CSRF-protected CRUD, live reports, query controls and valid markup | Temporary SQLite migrated/seeded twice; Category CRUD/PROTECT, aggregate/annotation/zero workload, filter/page/role assertions and HTML landmarks/IDs/labels/forms passed | PASS | Temporary file removed; working data untouched; not full fresh checkout |
| D06 | Actual local database/report verification | Counts reflect additional resolved HD-10013; preserve all working data | Read-only SQL and dashboard render: 13 total/8 active/3 resolved/2 cancelled, status 3/3/2/3/2; category active sum 8, technician workloads 3/2; HD-10013 preserved | PASS | No seeding, login/session updates or writes |
| D07 | Django/migration/dependency checks | Clean system, no drift/pending migrations, compatible existing pins | check --database default: no issues; makemigrations --check --dry-run: no changes; migrate --check: exit 0; dependency check recorded in D report | PASS | Models/migrations/ERD and pins unchanged |
| D08 | Git/source/doc/runtime hygiene | Exact inventory, valid links/syntax/whitespace, no tracked credentials/generated data | 71 source/document files, 57 valid local links, 18 modified/10 created, Python syntax and 9/12/11 new test counts checked; protected files/runtime ignore/diff whitespace passed | PASS | Staged whitespace/inventory reviewed before commit |

No failing D suite result has been observed. Exact commands and integration details are in CHECKPOINT_D_REPORT. The complete suite includes all earlier model/account/permission/seed/admin/ticket lifecycle regressions. Django's expected debug 404 log lines in targeted missing-ticket checks do not indicate failures.

## Checkpoint E executed audit and verification

Executed 13 October 2026 (Asia/Riyadh). A–D approved; E only authorized. User-observed UC01–UC07 above are preserved without adding observations of local HD-10013. No application dependencies/schema/seed/live records changed.

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| E01 | Full auth/workflow/category/query/model/interface audit | Reuse correct behavior; fix genuine defects | Models/migration/ERD, role/account/admin helpers, services/forms/views/URLs, queries, seed and all custom templates/CSS reviewed; corrections and traceability in E report | PASS | No stylistic backend rewrite or scope expansion |
| E02 | Audit regressions and complete suite | Existing 133 + meaningful new security/interface checks | **149 tests passed in 3.127s**, fresh migrated test DB created/destroyed; 16 new ReliabilityTests | PASS | Role/ownership/forged fields/terminal/eligibility/queries/reports/CSRF regressions retained |
| E03 | Feedback isolation and HTTP/labels | No prior-identity messages; helpful 405/Allow; readable options with unchanged IDs | Login/logout/admin logout message regressions pass; cookie/session storage covered; 405 navigation and full-name/username/fallback/escaping/eligibility checks pass | PASS | Initial failures reproduced and fixed, not hidden |
| E04 | Real Chrome page/interface checks | Fixed-width desktop/mobile layouts, labels/errors/contrast, readable tables and max text | **34 page/viewport audits passed** at 1280px/375px, including login, all custom page types, bound errors, 405 and long confirmations; measured contrast failures zero for checked elements | PASS (browser automated) | Emulated widths, computed checks and screenshots; not certification/human/device review |
| E05 | Real Chrome keyboard/workflows/admin | Actual key input and persisted flows/permissions | **5 additional checks passed**: skip link/focus/Enter; native technician selection; table ArrowRight scroll; role/action lifecycle/category/query/denial journey; guarded admin read-only ticket/comment and active-technician deactivation rejection | PASS (browser automated) | Total 39 Chrome checks; fixture-only superuser; normal hashing/CSRF; live DB untouched |
| E06 | Schema/environment/data consistency | No drift/pending migrations/dependency issues; live data preserved | System/database check clean; makemigrations no changes; migrate --check exit 0; pip check clean; logical snapshot of eight app/user/role tables exactly equals pre-E; PRAGMA integrity ok and foreign_key_check empty | PASS | 13 tickets/5 comments/5 accounts unchanged; HD-10013 retained |
| E07 | Source/evidence/Git hygiene | Exact inventory, valid links/syntax/whitespace, no runtime credentials/DB tracked | 82 source/doc/artifact files, 80 local links, 16 modified/11 created, Python/Node syntax, 16 new test methods, actual 39-check JSON/PNG signatures, protected files/runtime exclusion/diff checks passed | PASS | Staged whitespace/inventory also checked before commit |
| E08 | Remaining acceptance preparation | Reproducible actions and honest coverage limits | MANUAL_BROWSER_CHECKS maps remaining M01–M14 actions/expected outcomes; F/G remain gated | PASS (preparation) | Instructions are not observed outcomes |

The first three targeted checks failed on username-only options, pending logout feedback and blank 405 output. Corrections passed. Additional single-test runs reproduced feedback on successful account-switch login and admin logout, then missing no-store/private response headers; all corrections passed. Interim totals 136/147/148 preceded the final 149-test suite.

Installed Chrome and Node 21.7.2 were available, without Playwright/Puppeteer/Selenium or a browser connector. Earlier runs reported Chrome 154.0.8037.99; the final run reported Chrome 155.0.8059.40. CDP made genuine automation possible. Initial sandbox/local-port failures needed approved isolated execution. Stress reproduced valid 100-character category overflow; wrap/scroll containment corrections passed. Keyboard scrolling needed explicit virtual key codes in the harness. The final 39-check run passed; [results](evidence/checkpoint-e/results.json) and screenshots are actual disposable-fixture evidence.

Exact final principal commands from helpdesk-pro with a generated private runtime key:

```sh
.venv/bin/python -B manage.py check --database default
.venv/bin/python -B manage.py makemigrations --check --dry-run
.venv/bin/python -B manage.py migrate --check
.venv/bin/python -B manage.py test tickets.tests --verbosity 1
.venv/bin/python -m pip --no-cache-dir check
```

Those management commands ran via stdin subprocess wrappers setting a random DJANGO_SECRET_KEY without printing it. Targeted test_reliability/test_views runs were used after corrections. From the repository root the executed browser command was:

```sh
HELPDESK_BROWSER_EVIDENCE=/private/tmp/helpdesk-e-evidence node helpdesk-pro/scripts/verify_browser.mjs
```

It creates a new temporary database/Chrome profile and a browser-only setup superuser, serves loopback, exercises the real app, retains images/result JSON and removes server/database/profile. A separate read-only SQL snapshot comparison included Department/Category/Ticket/Comment/User/membership/Group/GroupPermission values, revealing no change to the working records. This is not Checkpoint G fresh-checkout evidence. Model/migration/ERD and pins remain unchanged.

## Checkpoint F documentation verification

Executed 13 October 2026 (Asia/Riyadh), documentation only. A–E are reviewed/approved; G is not started. Existing automated evidence is preserved, not reported as a new run. All historical checkpoint reports and UC01–UC07/manual scenario entries remain unchanged.

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| F01 | Official grading/design/source audit | Every normative guide requirement and all 100 marks map to actual features/source/evidence/gaps | All six guide pages re-read; eight criteria total 100; 14 source-linked feature entries plus exhaustive guide mapping; ERD/role/lifecycle/wireframes reviewed and README/demo/checklist finalized | PASS (document audit) | No market research, manual acceptance or final-readiness result invented |
| F02 | Latest evidence remains applicable | E source/artifacts unchanged; historical/user/manual provenance preserved | 66 non-Markdown tracked files byte-identical to E, A–E reports and UC/M sections unchanged; AST confirms 149 methods and documented symbols; JSON validates 34 page + 5 other checks, final Chrome 155.0.8059.40 | PASS (retained evidence audit) | 149-test/39-browser results are E executions, not new F runs |
| F03 | Current configuration/dependency/schema consistency | Documented versions/pins match; no check/drift/pending/dependency issues | Python 3.14.7/Django 5.2.18/asgiref 3.12.1/sqlparse 0.6.0/SQLite 3.53.4; check --database default zero issues, makemigrations no changes, migrate --check exit 0, pip check clean | PASS | Private runtime key; no install/migration application/seed/fresh checkout |
| F04 | Markdown/path/setup/rubric/Git hygiene | Links and commands resolve, intended docs only, no tracked runtime files | 85 repository files/19 Markdown documents; 207 local links/targets/fragments valid; 8 shell blocks parse in bash/zsh; 15 app routes and 3 auth/admin logout reversals correct; eight criteria total 100 and 14 feature entries; 11 modified/3 created Markdown only; ignore rules and diff whitespace clean | PASS (document/command audit) | Shell parsing/source consistency is not clean-checkout execution; final staged paths/whitespace reviewed before commit |
| F05 | Working database and HD-10013 preservation | Existing app/user/role records and file bytes untouched | Eight-table logical digest matches E; 13 tickets/5 comments/5 users retained; HD-10013 resolved with requester 9001/assignee 9003/note/timestamp; PRAGMA integrity ok, foreign_key_check empty; DB bytes unchanged before/after F checks | PASS (read-only) | No login/seed/reset or saved mutation; counts remain 13/8/3/2 |

Commands and full inventory: [CHECKPOINT_F_REPORT](CHECKPOINT_F_REPORT.md). [EVIDENCE_INDEX](EVIDENCE_INDEX.md) consolidates historical totals/commands/limits; [SUBMISSION_CHECKLIST](SUBMISSION_CHECKLIST.md) lists unresolved human, G and external actions. Writing the six-step demo/Q&A is preparation, not M14 rehearsal.

## Checkpoint G final automated verification

Executed 13 October 2026 (Asia/Riyadh). A–F reviewed/approved. G uses a genuine local Git clone (no hardlinks), a new venv, isolated uncached package download and new SQLite data/configuration. Original working data/HD-10013 are never used for state-changing checks. [G report](CHECKPOINT_G_REPORT.md) records exact commands, failed probes/corrections and inventory.

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| G01 | Genuine clean-checkout installation | Committed source alone creates environment/schema/related data; seed idempotent | Cloned F commit d89f8748a9de33050eeb20ee7720df1eb2c253a1 in a new /private/tmp directory; Python 3.14.7 venv; pins downloaded/installed; new private key; 19 migrations applied; seed 12 then 0 new tickets; exact all-table snapshots/passwords/timestamps unchanged | PASS (automated fresh checkout) | First sandbox PyPI DNS attempt failed; approved retry succeeded; no original venv/DB/config reused |
| G02 | Complete suite/versions/schema/dependencies | Full security/workflow/ORM tests, no drift/pending/check/dependency issues | 149 tests passed in 3.130s, fresh migrated test DB created/destroyed; system/database zero issues, makemigrations no changes, migrate --check exit 0, pip check clean; pins match | PASS | Includes all role/admin/forged-state/transition/reassignment/query/report/ERD tests; expected Not Found logging is not failure |
| G03 | Fresh-clone real Chrome | Actual pages/actions/admin/key checks work on isolated fixtures | 39 checks PASS on Chrome/155.0.8059.40: 34 page audits, 3 basic keyboard checks, combined role/Category/query journey and guarded admin; cards 12/8/2/2 then validated 13/7/3/3 before stress fixtures | PASS (browser automated) | 1280px/375px emulation; no physical device, zoom/screen-reader/full human keyboard or original HD-10013 observation |
| G04 | Real Django server and HTTP mutations | Documented local server serves CSS/login and persists protected workflow/report changes | 14 checks PASS: login/static/anonymous redirect, role denial, create/edit/comment/cancel/retention, CSRF rejection, terminal 409, object 404/method 405, POST logout and current report 13/8/2/3 | PASS (HTTP automated) | Initial probe wrongly set DEBUG=false and CSS returned 404; rerun with documented DEBUG=true passed; private passwords rotated only in disposable clone |
| G05 | Repository/source/link/pin/security hygiene | Only evidence/docs changes; valid links, no tracked runtime/private credentials; historical reports intact | 94 repository files/20 Markdown docs; 268 local links/fragments valid; 16 shell blocks parse in bash/zsh; 66 baseline non-Markdown files and A–F reports/UC unchanged; 149 test methods/artifact counts validated; 100-mark matrix correct; 13 modified/9 created intended docs/artifacts; history scan no credential flags, runtime ignored and whitespace clean | PASS (source/document/security audit) | Source/pin/history review is not remote instructor-access confirmation; staged/final candidate parity checked at delivery |
| G06 | Existing working DB/HD-10013 preservation | File bytes and all app/user/role rows intact | Database SHA-256 unchanged; eight-table logical digest equals F/E; PRAGMA integrity ok/no FK violations; HD-10013 still resolved with requester 9001/assignee 9003/note/time; counts 13/8/3/2 | PASS (read-only) | Disposable clone may reuse numeric ID 10013 independently; original record never mutated |
| G07 | Final guide/grading/demo/manual preparation | All 100 marks map to exact source/checks/gaps; human instructions truthful | Eight rubric criteria and final guide checklist audited; README/design/ERD/wireframes/matrix/evidence/demo/checklist cross-checked; M01 user partial preserved, remaining human steps explicit | PASS (audit/preparation) | Personal rehearsal/understanding and instructor scope/access/duration remain unconfirmed; no submission/full approval/grade guarantee |

[Fresh JSON](evidence/checkpoint-g/fresh-checkout.json), [server JSON](evidence/checkpoint-g/server-access.json), [browser JSON](evidence/checkpoint-g/results.json) and five actual screenshots retain measured evidence. The full suite covers all required supported workflows; G's HTTP/server checks add actual network/request/stylesheet evidence. Historical A–F reports and user UC01–UC07 remain unchanged. Failure history also includes an initial pip cache advisory and non-raw regex SyntaxWarnings in the discarded HTTP probe; the corrected raw-regex probe and no-cache dependency check passed. These were harness/environment issues, not application defects.

## Required final manual scenarios

M01–M09 below record observations supplied by the **project owner**, performed manually on **13 October 2026** in the local application. They are **PASS (user-observed)** only within the reported scope, not Codex-executed browser checks. Browser/version, viewport and screenshots were not supplied; none are inferred. UC01–UC07 and historical A–G records above retain their original attribution and stage-specific results.

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| M01 | Resolved detail and terminal controls | Resolution note/time/discussion readable; no modification controls | HD-10013 inspected as employee1, technician1 and itadmin; all three saw note, timestamp and retained discussion, with no modification controls | PASS (user-observed) | 13 October 2026; complements original UC01–UC07 without rewriting them; crafted terminal POSTs are separate automated evidence |
| M02 | Whitespace validation | Helpful errors; rejected whitespace input | Creation rejected whitespace-only title/description; active-ticket comment rejected whitespace; resolution on HD-10007 rejected whitespace note; errors displayed, no successful mutation indicated | PASS (user-observed, observed scenarios) | 13 October 2026; comment ticket reference unspecified; empty-value/invalid-choice/FK variants and independent persistence inspection not reported |
| M03 | Matching search and combined filters | Correct results, case-insensitive search and related category filtering | printer → HD-10001/HD-10013; printer + New + High + Hardware → HD-10001 only; pRiNtEr with other filters cleared → both; Category detail → View tickets applied Hardware | PASS (user-observed) | 13 October 2026; actual reported query combinations |
| M04 | No matches and invalid parameters | Helpful no-results/errors; valid filter retained; no crash | Nonexistent term displayed useful no-results; invalid status/order displayed feedback while preserving valid High priority; no traceback | PASS (user-observed, observed scenarios) | 13 October 2026; a completely empty initial queue was not reported |
| M05 | Priority ordering and pagination | High before Medium; invalid/nonpositive pages first, positive overflow last; no errors | High before Medium observed; owner confirmed pagination and page=abc, 0, -1, 999 followed documented expectations without errors | PASS (user-observed, user-reported pagination) | 13 October 2026; detailed clicks/filter preservation, all date orders, Low ordering and tie behavior not independently reported |
| M06 | Own New edit and object access | Own New edits persist; assigned owner edit 403; other employee detail/edit 404 | employee1 created HD-10014, edited title/priority while New; after admin assignment to technician1, employee1 edit URL 403; employee2 detail/edit URLs 404 | PASS (user-observed) | 13 October 2026; remaining business fields/forged POSTs not manually reported |
| M07 | Cancellation and retained dependencies | Cancelled records retain details/comment/assignee and become read-only | employee2 created/commented/cancelled HD-10015; details/comment retained, read-only. Admin cancelled assigned HD-10014; requester/assignee/details retained, read-only | PASS (user-observed, observed scenarios) | 13 October 2026; confirmation GET/Keep ticket back-out and separate In Progress cancellation not explicitly evidenced, remain unverified |
| M08 | Category CRUD, validation and access | Unused deletion succeeds; referenced deletion protected; unauthorized access rejected | Admin created/viewed/edited/deleted unused category; Hardware deletion prevented; employee1/technician1 listing/edit URLs 403; duplicate Hardware/whitespace name rejected | PASS (user-observed) | 13 October 2026; unused category name/reference not supplied |
| M09 | Live aggregate and annotated counts | Active = New + Assigned + In Progress; assignment changes state/workload, retaining overall active/category counts | Before HD-10001 assignment: total/active/resolved/cancelled 15/8/3/4; statuses 3/3/2/3/4; categories Hardware/Software/Network/Accounts/Unused 3/2/2/1/0; Lina/Sami 3/2. Assign HD-10001 to technician2 → New 2, Assigned 4, Sami 3; active/category counts unchanged | PASS (user-observed, observed reporting checks) | 13 October 2026; historical observations, not future constants; seed is 12 tickets, G working snapshot was 13 |
| M10 | Cross-user/role access, reassignment and terminal actions | No leaks; old technician loses access; terminal read-only | Not executed | NOT RUN | List/detail/dashboard/actions |
| M11 | Guarded admin and account changes | Ticket/comment mutation blocked; active technician cannot be stranded | Not executed | NOT RUN | Includes role groups/deletion |
| M12 | Desktop/mobile/keyboard/errors | Usable at 1280px and 375px; focus/labels/feedback | Not executed | NOT RUN | Real browser, not template inspection |
| M13 | Separate fresh checkout setup | Configure/install/migrate/seed twice/check/test/run succeeds | G01–G04 genuine automated fresh installation/server/browser checks passed; independent human repeat not reported | PASS (automated setup); human NOT RUN | Original DB/environment/config not reused; no human installation claim |
| M14 | Guide-ordered demonstration and student explanation | Workflow/failure/reports/relationships/value explained | Not executed | NOT RUN | Final submitted revision; duration confirmed |

## Automated coverage delivered and remaining

Authentication/no-role/conflicting-role/inactive/staff-only/superuser behavior; session-derived identity and field whitelists; object GET/POST restrictions; all transitions and terminal operations; reassignment/current-state checks; trimmed/choice/FK/name validations; inactive/invalid assignees; database state checks; PROTECT and retained dependencies; guarded admin/provisioning; search/order/pagination/malformed input; known aggregate/annotation and zero/multi-row results; seed idempotency/collisions/change/password preservation; fresh migrations and system checks. Use Django's test tools; no arbitrary coverage quota.

B delivered 60 tests; C added 41 and D added 32. E adds 16 ReliabilityTests (149 total). Existing lifecycle/schema/role/seed/report tests remain, with new account-message isolation, stale eligibility, changed roles, forged report params, all-role terminal controls, extreme query values, safe redirects, CSRF rotation and readable requester/technician output. E also passed 39 real Chrome checks with actual rendered screenshots. These automate part of M01–M12; the later M01–M09 owner observations above are separate evidence, and UC01–UC07 remain user-attributed. This documentation reconciliation did not rerun tests or browser automation.

## Current limitations

M01–M09 now have owner-reported PASS results within the scopes above. Unreported facets remain unverified, especially cancellation confirmation/back-out; these results do not close the broader M10–M12 or M14 scenarios. M10–M12/M14 remain human NOT RUN; M13 automated setup PASS/human repeat NOT RUN. Follow [MANUAL_BROWSER_CHECKS](MANUAL_BROWSER_CHECKS.md) for remaining role/reassignment/admin/full keyboard/zoom/device checks and unreported facets. G supplies the latest automated evidence; this pass changes documentation only. Instructor facts, student rehearsal and actual submission remain outstanding. No unresolved defect is known from the executed checks. Privileged bulk/raw SQL and SQLite concurrent-write limits remain documented; no certification or grade guarantee is claimed.
