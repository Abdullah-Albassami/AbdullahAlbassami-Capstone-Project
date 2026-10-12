# Verification record

Only executed checks may be marked PASS. NOT RUN means planned or unavailable in the current checkpoint. Command-level HTTP/template checks are not a real browser walkthrough. No custom migrations or database workflow checks have been performed at Checkpoint A.

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

## Required final manual scenarios

| ID | Scenario | Expected | Actual | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| M01 | Employee submit → admin assign → technician start/comment/resolve → employee read | Saved New/Assigned/In Progress/Resolved states; note/thread visible | Not executed | NOT RUN | Real browser; persistence/reload |
| M02 | Missing/blank title, description, note, comment; invalid values | Helpful errors; no invalid mutation | Not executed | NOT RUN | Required/value/business checks |
| M03 | Matching search and combined filters | Correct scoped results | Not executed | NOT RUN | Include category relationship query |
| M04 | No matches; empty queues; invalid parameters | Useful empty state; no crash | Not executed | NOT RUN | Preserve valid parameters |
| M05 | Priority/date ordering and pagination | Intentional stable order and filters preserved | Not executed | NOT RUN | More than ten results |
| M06 | Edit own New; reject assigned/other-user edits | Valid edits persisted; forbidden edits rejected | Not executed | NOT RUN | GET and POST bypass attempts |
| M07 | Cancel ticket with comments/assignee | Confirmation; terminal record and dependencies retained | Not executed | NOT RUN | Employee New versus admin active |
| M08 | Category create/read/edit/delete | Unused category deleted; used category protected with explanation | Not executed | NOT RUN | No uncaught dependency error |
| M09 | Initial reports and changed live counts | Total 12/active 8/resolved 2/cancelled 2; annotations correct | Not executed | NOT RUN | Category 3/2/2/1/0; technicians 3/2 |
| M10 | Cross-user/role access, reassignment and terminal actions | No leaks; old technician loses access; terminal read-only | Not executed | NOT RUN | List/detail/dashboard/actions |
| M11 | Guarded admin and account changes | Ticket/comment mutation blocked; active technician cannot be stranded | Not executed | NOT RUN | Includes role groups/deletion |
| M12 | Desktop/mobile/keyboard/errors | Usable at 1280px and 375px; focus/labels/feedback | Not executed | NOT RUN | Real browser, not template inspection |
| M13 | Separate fresh checkout setup | Configure/install/migrate/seed twice/check/test/run succeeds | Not executed | NOT RUN | No dependency on original DB/environment |
| M14 | Guide-ordered demonstration and student explanation | Workflow/failure/reports/relationships/value explained | Not executed | NOT RUN | Final submitted revision; duration confirmed |

## Automated coverage to implement

Authentication/no-role/conflicting-role/inactive/staff-only/superuser behavior; session-derived identity and field whitelists; object GET/POST restrictions; all transitions and terminal operations; reassignment/current-state checks; trimmed/choice/FK/name validations; inactive/invalid assignees; database state checks; PROTECT and retained dependencies; guarded admin/provisioning; search/order/pagination/malformed input; known aggregate/annotation and zero/multi-row results; seed idempotency/collisions/change/password preservation; fresh migrations and system checks. Use Django's test tools; no arbitrary coverage quota.

## Current limitations

Checkpoint A contains the foundation and design only. No custom schema, seeded accounts, application routes, business tests, browser workflow or full fresh-checkout verification exists yet. Instructor scope approval, access and presentation duration remain unconfirmed. No production deployment/concurrency assurance or grade guarantee is made.
