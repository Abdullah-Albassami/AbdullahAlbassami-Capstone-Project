# Checkpoint C delivery report

Date: 12 October 2026. A/B were reviewed/approved and the user authorized C only. The Django application remains inside `helpdesk-pro/`; the official guide and specification remain at the root. **C is implemented and verified. Stop before D pending explicit approval.**

## Delivered behavior

- Django login and POST-only logout, role navigation and Employee/Technician/IT Admin dashboards. Active superusers retain the explicit IT Admin override; staff alone grants no application role.
- Scoped newest-first ticket list, related detail/thread, Employee/Admin submission, allowed five-field edits and confirmation-based cancellation. Cancellation retains the ticket, assignee and comments.
- Admin assignment to an active single-role Technician; reassignment preserves Assigned/In progress and immediately revokes the old technician's scope. Assignee/Admin start only Assigned; resolution only In progress with a trimmed meaningful note and server timestamp saved together.
- Session-derived requester/comment author and server-derived workflow metadata. All web mutations use shared atomic services that fetch current state/scope, recheck authorization/eligibility and run complete validation. No form.save bypass, hard deletion, reopening or comment editing/deletion.
- Terminal tickets remain view-only. Form errors render bound fields/non-field feedback; success redirects with messages. Anonymous requests redirect to login; missing/out-of-scope IDs return safe 404, disallowed roles/actions 403, invalid state 409, unsupported methods 405. CSRF failures provide refresh guidance; the server-error template does not resolve a database-backed user.
- Inherited responsive local templates/CSS with labels/help/error associations, semantic landmarks, keyboard focus styling, textual status/priority, scrollable tables, empty states and clear destructive consequences.

Dashboard's basic four summary cards use the final scoped aggregate Count query, avoiding a foreseeable replacement of that query. This does **not** implement the full reporting interface: five-status breakdown and annotated category/technician tables remain D. Category CRUD, search/filter controls, selectable ordering and pagination are also unimplemented at C.

## All created/modified files

Created (16):

| Path (relative to repository root) | Responsibility |
| --- | --- |
| helpdesk-pro/tickets/services.py | Shared current-state authorization and validated atomic mutations |
| helpdesk-pro/tickets/forms.py | Explicit business/action fields and validation-error mapping |
| helpdesk-pro/tickets/views.py | HTTP binding, role summaries, scoped pages, feedback/error handling |
| helpdesk-pro/tickets/urls.py | Named application workflow routes |
| helpdesk-pro/tickets/tests/test_services.py | 12 direct workflow/security/integrity tests |
| helpdesk-pro/tickets/tests/test_views.py | 29 HTTP/auth/scope/CSRF/journey/error tests |
| helpdesk-pro/templates/registration/login.html | Labeled built-in authentication form |
| helpdesk-pro/templates/errors/error.html | Friendly error/navigation page |
| helpdesk-pro/templates/tickets/dashboard.html | Role-scoped summary/recent requests |
| helpdesk-pro/templates/tickets/ticket_list.html | Scoped queue and useful empty state |
| helpdesk-pro/templates/tickets/ticket_detail.html | Related details, discussion and permitted action forms |
| helpdesk-pro/templates/tickets/ticket_form.html | Five-field submission/edit interface |
| helpdesk-pro/templates/tickets/ticket_cancel_confirm.html | Cancellation consequences and POST confirmation |
| helpdesk-pro/templates/tickets/includes/form_fields.html | Consistent labels/help/field and non-field errors |
| helpdesk-pro/templates/tickets/includes/ticket_table.html | Reusable related ticket rows and empty queues |
| helpdesk-pro/docs/CHECKPOINT_C_REPORT.md | This inventory/results/limitations report |

Modified (13):

| Path | Change |
| --- | --- |
| HELPDESK_PRO_CODEX_SPEC_FINAL.md | Actual C status, gate before D and next checkpoint prompt |
| README.md | Current repository delivery summary/report link |
| helpdesk-pro/README.md | Executable web workflow, access, setup, tests/evidence and truthful scope |
| helpdesk-pro/config/settings.py | Custom CSRF rejection handler |
| helpdesk-pro/config/urls.py | Login/logout/application routes and error handlers |
| helpdesk-pro/templates/base.html | Role navigation and CSRF-protected sign-out |
| helpdesk-pro/static/css/style.css | Integrated responsive workflow/dashboard/form/status styles |
| helpdesk-pro/docs/DESIGN.md | Implemented service/form/view/HTTP contracts and C/D boundary |
| helpdesk-pro/docs/WIREFRAMES.md | Implemented versus planned interface status |
| helpdesk-pro/docs/REQUIREMENTS_MATRIX.md | All guide rows updated; actual C URL/code/check/document links |
| helpdesk-pro/docs/ACCEPTANCE_TESTS.md | C01–C08 actual verification; manual checks remain NOT RUN |
| helpdesk-pro/docs/PROGRESS.md | B approved, C delivered, remaining tasks/blockers and gate |
| helpdesk-pro/docs/DEMO_SCRIPT.md | Executable C review journey, final reports/rehearsal pending |

No models, migration files, role helpers, account guards, seed files, dependency pins or official guide were changed. The ERD still matches the schema; the existing schema/relationship/deletion tests pass. No new packages or migrations were needed.

## Commands and actual results

Commands ran from `helpdesk-pro/` through stdin wrappers supplying a generated private runtime key. This is the exact final verification wrapper (no key printed):

```sh
.venv/bin/python -B - <<'PY'
import os, secrets, subprocess, sys
os.environ['DJANGO_SECRET_KEY'] = secrets.token_urlsafe(64)
for args in [('check', '--database', 'default'),
             ('makemigrations', '--check', '--dry-run'),
             ('migrate', '--check'),
             ('test', 'tickets.tests', '--verbosity', '1')]:
    print('manage.py ' + ' '.join(args), flush=True)
    subprocess.run([sys.executable, '-B', 'manage.py', *args], check=True)
PY
.venv/bin/python -m pip --no-cache-dir check
```

| Check | Actual result |
| --- | --- |
| check --database default | No issues (0 silenced) |
| makemigrations --check --dry-run | No changes detected |
| migrate --check | Exit 0; no pending migrations |
| test tickets.tests --verbosity 1 | **101 tests passed**, 2.076s; fresh migrated test DB created/destroyed |
| pip --no-cache-dir check | No broken requirements found |

Earlier commands included check; targeted test_services/test_views with verbosity 2 and 1; and test --verbosity 1. The first targeted run had 37 tests with four nullable-assignee rendering errors and one success-message assertion failure. Explicit assignee conditionals fixed the template defect. Following the assignment redirect corrected the role-switch test setup. A subsequent check assertion fetched a success page twice; fetch_redirect_response=False corrected it. An interim 100-test full suite passed; the final query-free server-error check makes 101. The final aggregate query and regression were tested together. No outstanding test failure is known.

An additional `.venv/bin/python -B -` harness configured a separate temporary SQLite file before Django setup; called migrate, seed_demo twice, check and migrate --check; and used Client(enforce_csrf_checks=True) against the actual seeded accounts with normal runtime password hashing. Runtime credentials stayed in memory. The second seed ran without DEMO_PASSWORD and preserved exact ticket/password snapshots.

The harness exercised login/logout, seeded ticket assignment/start/comment/resolution, terminal comment rejection, cross-user 404, and new-ticket creation/edit/comment/confirmation/cancellation. Parsed renders verified header/main/footer, unique IDs, associated labels and POST/CSRF forms. The stylesheet resolved. After closing/reopening the database connection, saved outcomes/thread remained and totals were 13 total, 7 active, 3 resolved, 3 cancelled (initial 12/8/2/2). The temporary database was removed; the working demo database was untouched. This is executed HTTP/database integration evidence, not real browser acceptance or a full fresh checkout.

Repository commands used for review include git status --short, git diff --stat, git diff --check and git diff --cached --check. Source/HTML/Markdown and approved documents were inspected with rg/cat/sed. A final stdin hygiene harness checks Python syntax, local Markdown links, unchanged protected baseline files and exclusion of runtime/generated/credential files; commit staging is limited to the 29-file inventory above. The user-facing completion response supplies the exact final commit hash and working-tree status; the report avoids a self-referential commit hash.

Hygiene result: 61 source/document files, 43 valid local links, exactly 13 modified and 16 created files; Python syntax, 12/29 new test-method counts, unchanged protected files, runtime ignore rules and diff whitespace all passed. The staged diff received the same whitespace/runtime/inventory review before commit.

## Grading evidence and remaining limitations

C supplies persisted ticket CRUD, role journey, authentication/object/action enforcement, explicit ModelForms/shared Python logic, named routing/inherited templates, relationship display, scoped aggregate summaries, helpful errors/confirmations and meaningful automated/integration verification. REQUIREMENTS_MATRIX maps these to code/URLs/checks/documentation across the guide's criteria. This supports grading evidence; it does not establish a grade or complete the remaining criteria.

All manual M01–M14 rows remain NOT RUN: browser viewport/keyboard/accessibility, the final demonstration, full fresh checkout and student rehearsal have not been executed. No browser tool is available in this session. Responsive CSS/parsed HTML checks are not substitutes for a real browser assessment.

SQLite transactions validate cohesive writes and current state but provide no row-locking guarantee through select_for_update; enterprise concurrent-user behavior is outside this local capstone scope. Privileged bulk ORM/raw SQL can bypass parts of validation, as documented in B. Instructor scope agreement, access, presentation duration and focused time remain externally unconfirmed.

Next after explicit approval: **D only** — category CRUD/protected deletion, validated combined list filters/relationship filtering/ordering/pagination, five-status breakdown and category/technician annotated reports with known/zero-row/edge-case verification. Do not begin D before review.
