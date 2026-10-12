# Verification record

Only executed or explicitly user-observed checks may be marked PASS, with their source named. NOT RUN means planned/unobserved. Command-level HTTP/template checks are not real browser walkthroughs. Historical A–C results remain separate from D checks and user-observed evidence.

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

## Required final manual scenarios

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| M01 | Employee submit → admin assign → technician start/comment/resolve → employee read | Saved New/Assigned/In Progress/Resolved states; note/thread visible | User observed HD-10013 lifecycle and employee dashboard Resolved (UC01–UC07); final employee detail/thread not reported | PARTIAL (user-observed) | Complete reported steps passed; remaining detail checks unobserved |
| M02 | Missing/blank title, description, note, comment; invalid values | Helpful errors; no invalid mutation | Not executed | NOT RUN | Required/value/business checks |
| M03 | Matching search and combined filters | Correct scoped results | Not executed | NOT RUN | Include category relationship query |
| M04 | No matches; empty queues; invalid parameters | Useful empty state; no crash | Not executed | NOT RUN | Preserve valid parameters |
| M05 | Priority/date ordering and pagination | Intentional stable order and filters preserved | Not executed | NOT RUN | More than ten results |
| M06 | Edit own New; reject assigned/other-user edits | Valid edits persisted; forbidden edits rejected | Not executed | NOT RUN | GET and POST bypass attempts |
| M07 | Cancel ticket with comments/assignee | Confirmation; terminal record and dependencies retained | Not executed | NOT RUN | Employee New versus admin active |
| M08 | Category create/read/edit/delete | Unused category deleted; used category protected with explanation | Not executed | NOT RUN | No uncaught dependency error |
| M09 | Initial reports and changed live counts | Pristine seed 12/8/2/2; current persisted values and annotations correct | No browser report check reported | NOT RUN | Local read-only HTTP render D06 is 13/8/3/2; not a browser PASS |
| M10 | Cross-user/role access, reassignment and terminal actions | No leaks; old technician loses access; terminal read-only | Not executed | NOT RUN | List/detail/dashboard/actions |
| M11 | Guarded admin and account changes | Ticket/comment mutation blocked; active technician cannot be stranded | Not executed | NOT RUN | Includes role groups/deletion |
| M12 | Desktop/mobile/keyboard/errors | Usable at 1280px and 375px; focus/labels/feedback | Not executed | NOT RUN | Real browser, not template inspection |
| M13 | Separate fresh checkout setup | Configure/install/migrate/seed twice/check/test/run succeeds | Not executed | NOT RUN | No dependency on original DB/environment |
| M14 | Guide-ordered demonstration and student explanation | Workflow/failure/reports/relationships/value explained | Not executed | NOT RUN | Final submitted revision; duration confirmed |

## Automated coverage delivered and remaining

Authentication/no-role/conflicting-role/inactive/staff-only/superuser behavior; session-derived identity and field whitelists; object GET/POST restrictions; all transitions and terminal operations; reassignment/current-state checks; trimmed/choice/FK/name validations; inactive/invalid assignees; database state checks; PROTECT and retained dependencies; guarded admin/provisioning; search/order/pagination/malformed input; known aggregate/annotation and zero/multi-row results; seed idempotency/collisions/change/password preservation; fresh migrations and system checks. Use Django's test tools; no arbitrary coverage quota.

B delivered 60 database/auth/admin/seed tests; C added 41 service/HTTP tests. D adds 32 Category/query/report tests (133 total), covering advanced filters/order/pagination, integrated aggregate/annotation values, zero/empty/multi-related data, report isolation and workflow count updates. Automated HTTP outcomes do not substitute for unobserved manual cases. UC01–UC07 are separately attributed to the user.

## Current limitations

Checkpoint D completes Category CRUD, scoped queries/pagination and full aggregate/annotated reporting while preserving the ticket workflow. UC01–UC07 record reported C browser observations; M01 is partial for final detail/thread, and M02–M14 remain NOT RUN. D browser/terminal-control checks, desktop/mobile/keyboard, student rehearsal and full fresh checkout remain pending E–G. Instructor scope/access/duration remain unconfirmed. Privileged bulk ORM/raw SQL can bypass validation; supported admin/services enforce approved rules. No enterprise concurrency assurance or grade guarantee is made.
