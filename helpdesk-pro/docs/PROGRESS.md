# Checkpoint progress

Last updated: 13 October 2026 (Asia/Riyadh). A–F are reviewed/approved; G automated verification is complete: genuine fresh installation, 149 tests, 39 Chrome checks and 14 live HTTP/server checks. Stop after G. Human acceptance/rehearsal and instructor scope/access/duration remain open; no full approval/submission or grade guarantee. HD-10013/working data are unchanged.

| Checkpoint | Estimate | Completion condition | Status |
| --- | --- | --- | --- |
| A: design/foundation | 1h | Approved amendments, ERD/contracts/wireframes, safe scaffold inside helpdesk-pro, compatibility before install, actual checks and coherent commit | Reviewed/approved |
| B: data/accounts | 2h | Models/constraints/migrations, guarded admin, roles/seed and integrity/provisioning tests | Reviewed/approved |
| C: support workflow | 4h | Complete persisted role journey, usable forms/pages and focused security/state tests | Reviewed/approved; user-observed HD-10013 journey recorded |
| D: CRUD/reports | 2h | Category CRUD, list queries/pagination, known aggregate/annotation counts | Reviewed/approved |
| E: reliability/UX | 3h | Audit/fix/test and actual browser checks where available; truthful remaining manual instructions | Reviewed/approved; 149 tests + 39 Chrome checks; human limitations documented |
| F: final evidence | 2h | Final README/design/matrix/actual verification/demo documents | Reviewed/approved; complete source-linked documentation/evidence/demo/checklist |
| G: readiness | 3h | Separate fresh checkout, seed twice, checks/tests/server/browser, truthful remaining human acceptance/rehearsal/access and candidate revision | Automated verification complete; 149 tests/39 Chrome/14 HTTP; human/external approval still open |
| Contingency | 2h | Mandatory blockers fixed; affected checks repeated | Reserved |

## Completed work

- Full six-page guide and specification audit; user-approved corrections.
- Environment inspected: Python 3.14.7, SQLite 3.53.4; initially no Django for that interpreter.
- Original root environment created in the previous checkpoint attempt; pinned Django 5.2.18, asgiref 3.12.1 and sqlparse 0.6.0. Initial sandbox PyPI access failed; installation succeeded after network approval. That ignored environment is retained locally and is no longer the application's environment.
- Foundation source and runtime configuration prepared; no custom models/migrations or database created intentionally.
- Final target architecture, ERD, route/role contracts, wireframes and sample-count contracts documented.
- Requirement/evidence, acceptance and demo records established with planned versus executed status.
- Django system check and dependency check passed. Configuration rejection, source syntax, ASGI/WSGI, shared-template escaping/landmarks, static lookup and anonymous admin HTTP checks passed. No database queries, database creation or migrations were required.
- Latest user amendments incorporated before relocation. The existing empty `helpdesk-pro/` directory was inspected and reused; tracked application files/docs moved there without replacing unrelated data. Root guide/specification retained.
- Official supported-release/Python compatibility and existing package metadata checked before installing the same pinned dependencies into a freshly created `helpdesk-pro/.venv`. Relocated integration checks are recorded independently of the historical checks.
- Amended R01–R08 checks passed: environment/pins, both invocation directories, configuration rejection, resource paths, entry points, template/static integration, unauthenticated HTTP/CSRF behavior and repository/link hygiene. No migrations or business/browser tests run. An initial debug-root HTTP assertion was corrected and rerun as documented.

## Remaining work and blockers

- Remaining user human acceptance/rehearsal and instructor scope/access/duration confirmation. G's delivery identifies the local candidate commit; the student records the ultimately submitted/demonstrated revision after any further verified acceptance updates. Historical A–F reports stay unchanged; no push/submission is performed.
- Human review of local HD-10013's final detail/controls, complete keyboard/zoom/device/screen-reader usability, admin observations and rehearsal remain. G completed automated fresh checkout/server/browser verification; a human setup repeat is not reported. Disposable checks do not upgrade unobserved human rows to PASS.
- External facts unresolved: instructor scope agreement, presentation duration, instructor repository access and available focused development hours. No claim of confirmation is made.
- No deployment is required. Credentials/secret key are runtime-only; the local ignored database now contains the five fictitious demo accounts. Verification used a generated undisclosed password; choose known local credentials with Django changepassword as documented.

## Checkpoint B delivered and verified

- Four final models with approved types/defaults/relationships/deletion rules; four database checks; trimmed meaningful text and business validation.
- Generated/applied initial migration plus Django auth/admin/session migrations; schema matched to ERD and independently migrated into a fresh temporary SQLite file.
- Three post-migration role groups, scoped-query/action/eligibility helpers, guarded built-in provisioning, auth mutation hooks and read-only ticket/comment admin. No custom user/profile/history/integration subsystem.
- Deterministic, collision-safe transactional seed with runtime-only hashed credentials; initial 12/8/2/2 totals and category 3/2/2/1/0, technician 3/2 counts verified. Working and fresh SQLite databases seeded twice without resets.
- 60 automated tests passed, including model/database/relationship/deletion/role/account/admin-HTTP/seed checks. The first 53-test run found the blank-enabled/null-text validation gap; it was fixed and verified before two recovery checks were added. Final review reproduced an unsaved Group-name deletion bypass; the guard now checks persisted identity and its regression passes in the final suite.
- System/database checks, migration consistency and dependency checks passed. Final Git/link/secret hygiene is recorded in ACCEPTANCE_TESTS and CHECKPOINT_B_REPORT. No browser workflow/mobile acceptance or rendered ORM-feature evidence is claimed at B.

## Acceptance discipline

Record changes, commands/checks and actual outcomes for each checkpoint in ACCEPTANCE_TESTS.md. Maintain traceability in REQUIREMENTS_MATRIX.md. Never turn a planned case into PASS without execution. Commit real validated milestones; do not manufacture development history. Before submission record the final demo commit and verify instructor access. Optional polish cannot replace mandatory reliability or evidence.

## Checkpoint C delivered and verified

- Built-in login/POST logout; server-enforced role dashboards, scoped ticket queues/details and related discussion. Basic summary cards use the final scoped aggregate query; full reports remain D.
- Explicit business/action forms and shared atomic services for submission, editing, cancellation, assignment/reassignment, progress, resolution and comments. Current role/scope/state and technician eligibility are rechecked; requester/author/metadata are server-derived. Terminal records remain read-only.
- Inherited local templates/CSS supply role navigation, confirmations, labels/help/errors, status text, responsive grids, scrollable tables, empty states, success messages and friendly 403/404/409/CSRF/500 pages. GET cannot mutate; all mutation forms include CSRF.
- 41 new service/HTTP tests plus the 60 foundation tests: final 101 tests passed. Includes full persisted role journey, forged fields, scoped GET/POST, CSRF-enforced requests, safe login redirects, invalid/stale account/state handling and reassignment revoking access.
- Separate fresh temporary SQLite file migrated/seeded twice with normal password hashing. CSRF-enforced seeded resolution plus create/edit/comment/cancel passed; connection reopened and final 13/7/3/3 totals confirmed. Working demo data untouched.
- Checks/dependency consistency passed; no model changes or pending migrations. The initial targeted run found/fixed nullable-assignee template rendering. Redirect-message consumption assumptions in two tests were corrected. Final tests pass; real browser/mobile/keyboard acceptance, full checkout and student rehearsal remain NOT RUN.

## Checkpoint D delivered and verified

- IT Admin Category create/list/detail/edit/delete through explicit forms, shared role-checked services and confirmation; PROTECT retains categories referenced by active or terminal tickets with helpful feedback.
- Scoped Q title/description search, combined status/priority/category filters through category__name, whitelist ordering with business priority rank and stable tie-breakers, validated URL preservation and ten-ticket pagination. Malformed filters are ignored independently; zero/negative/nonnumeric pages select first, positive out-of-range last.
- One aggregate query supplies four cards and all five status counts. Separate filtered distinct Count annotations show all categories and eligible technicians, including zero rows. Organization reports require IT Admin at the query and view boundaries.
- 32 new category/query/report tests plus the previous 101: 133 tests pass. Cases include known seed arithmetic, no-result/empty states, malformed/repeated parameters, related filtering, ordering/page boundaries, permissions/CSRF, multiple comments/groups, eligibility and live workflow report updates. Existing lifecycle tests remain passing; one former C assertion for absent category routes now checks Employee denial on the implemented routes.
- Fresh temporary migrated/seeded database, normal hashing and CSRF-enforced Category CRUD/PROTECT/report/filter/page/role checks passed. Parsed HTML labels/IDs/landmarks/forms passed. Local database rendered read-only at actual 13/8/3/2 totals, preserving HD-10013 and all working data.
- User-observed browser entries UC01–UC07 are recorded exactly as reported; final terminal controls, new D browser checks, mobile/keyboard and full fresh checkout remain unverified. Models/migrations/ERD, dependency pins, seed and ticket mutation rules are unchanged.

## Checkpoint E delivered and verified

- Full application/security/schema/query/interface audit with narrow corrections: cleared feedback on logout and successful account login, helpful 405/Allow pages, named technician choices retaining IDs/eligibility, requester queue information, long-text wrapping, readable locally scrollable tables and stronger control borders.
- Added 16 meaningful audit tests; all 149 tests pass. Regressions reproduced feedback leakage on app/admin logout and login switch, blank 405 output, requested dropdown-label omission and absent private/no-store headers. Corrections pass alongside stale eligibility, changed roles, forged report parameters, terminal mutations, malformed queries and CSRF rotation.
- Found real installed Chrome despite no browser connector/Playwright/Puppeteer. Sandboxed Chrome/local-port launches failed; approved isolated runs succeeded with existing Node/Chrome. No packages installed. Browser stress reproduced maximum-length category overflow; mobile table containment correction and fully specified key events were verified.
- Final 39 real Chrome checks pass: 34 page/viewport/label/error/contrast cases, three basic keyboard cases, the role/action journey and guarded admin. Screenshots/result JSON are retained, and new fixtures/normal-hasher server/Chrome profile were removed. Working database never used by that server.
- Django/system/database/migration/dependency checks passed; logical snapshot of all app/user/role data matched E's baseline exactly, with PRAGMA integrity/foreign-key checks clean. Models/migrations/ERD and pins are unchanged; HD-10013 remains intact.
- UC01–UC07 remain attributed to the user. MANUAL_BROWSER_CHECKS supplies exact remaining actions; human/device/screen-reader/zoom/full-keyboard, fresh checkout and final rehearsal remain pending. E is not a final submission readiness claim.

## Checkpoint F delivered

- Re-read all six guide pages and audit all eight assessment criteria (100 marks). REQUIREMENTS_MATRIX now maps every normative requirement through a source-linked feature catalogue to actual URLs/views/models/forms/services/queries/templates, executed checks and remaining human evidence.
- Complete README covers problem/users, comparison/internal adoption assumptions, stack/pins, four models/six relationships, safe installation/configuration/migrate/seed twice/test/run, ORM metric meaning, limitations/future improvement and assistance/resources. Full fresh-checkout execution is still G.
- Final ERD/architecture/role/action/lifecycle documents reviewed against unchanged application source. Wireframes corrected to actual role navigation, names, columns, labels and scroll behavior; screenshots remain separate genuine browser artifacts.
- EVIDENCE_INDEX consolidates A–E results without rewriting history: latest E 149 Django tests and 39 Chrome checks, UC01–UC07 user observations, M01 partial and M02–M14 NOT RUN. F is documentation-only and does not invent a new test/browser run.
- DEMO_SCRIPT follows the exact six guide steps, gives source-linked request traces and likely instructor answers, distinguishes market assumptions and prepares live metric arithmetic. Student rehearsal is not executed by writing the script.
- SUBMISSION_CHECKLIST lists delivered artifacts, outstanding manual/G checks, external instructor scope/access/duration/deadline confirmations and how to capture the exact final submitted commit after verified changes. No remote delivery/access or final readiness is claimed.
- Actual F verification commands/results and inventory are recorded in CHECKPOINT_F_REPORT/ACCEPTANCE_TESTS. Working database/HD-10013, application source, migrations, pins and E artifacts remain unchanged. Stop before G.

## Checkpoint G delivered and verified

- Genuine `git clone --no-local` of F's committed repository into a new temporary directory; independent Python 3.14.7 venv and isolated uncached pin downloads. No working venv/database/local config copied. Initial sandbox PyPI DNS failure corrected by approved retry; no dependency change.
- New private runtime key/password, 19 migrations from scratch, known 12/8/2/2 seed totals, seed repeated without password. All-table snapshots/password hashes/timestamps identical; schema integrity/foreign keys clean. Fresh environment activation/pins verified.
- Full 149-test suite passed in 3.130s with all schema/security/lifecycle/category/query/report/seed tests. System/database/migration/dependency checks clean; no drift/pending migration.
- Actual Chrome from the clone passed 39 checks with disposable fixtures/profile (34 pages, 3 basic keyboard, guarded admin and combined journey). Another actual Django runserver passed 14 real HTTP/server/CSRF/workflow/live report checks. Corrected the harness's DEBUG=false/static assumption and raw regex warnings; documented default DEBUG=true works. No application defect or code rewrite.
- Genuine JSON/screenshots retained under evidence/checkpoint-g; full file/command/result details in CHECKPOINT_G_REPORT. Original database file bytes/logical rows and HD-10013 unchanged. Historical A–F reports and UC01–UC07 remain intact.
- Final all-100-mark audit/source/docs cross-check distinguishes automated readiness from human acceptance/understanding/instructor facts. M13 automated setup PASS; M01 partial and M02–M12/M14 human checks open. Student rehearsal/duration/scope/access/submission are not claimed completed.
- Stop after G. Deliver a local candidate commit/hash/clean-tree result; remaining human/external outcomes must be supplied by the student before full approval/submission. No remote push or messaging occurs.
