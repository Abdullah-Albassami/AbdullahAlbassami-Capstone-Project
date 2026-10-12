# Checkpoint progress

Last updated: 12 October 2026 (Asia/Riyadh). A–C are reviewed/approved; the user authorized D only and reported HD-10013's browser lifecycle. D is complete; stop before E pending explicit approval. The helpdesk-pro structure and two-day priorities remain. Approximately 20 focused hours were estimated; actual completion speed is not guaranteed.

| Checkpoint | Estimate | Completion condition | Status |
| --- | --- | --- | --- |
| A: design/foundation | 1h | Approved amendments, ERD/contracts/wireframes, safe scaffold inside helpdesk-pro, compatibility before install, actual checks and coherent commit | Reviewed/approved |
| B: data/accounts | 2h | Models/constraints/migrations, guarded admin, roles/seed and integrity/provisioning tests | Reviewed/approved |
| C: support workflow | 4h | Complete persisted role journey, usable forms/pages and focused security/state tests | Reviewed/approved; user-observed HD-10013 journey recorded |
| D: CRUD/reports | 2h | Category CRUD, list queries/pagination, known aggregate/annotation counts | Complete; awaiting review/approval before E |
| E: reliability/UX | 3h | Complete important tests and mobile/accessibility/error-state verification | Not started |
| F: final evidence | 2h | Final README/design/matrix/actual verification/demo documents | Not started |
| G: readiness | 3h | Separate fresh checkout, seed twice, all checks, real browser acceptance, rehearsal and submission revision | Not started |
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

- User review/approval of D before E. Verified D changes/report form a coherent milestone commit; Git history supplies its hash without a self-referential report hash. Historical A–C checks remain separate.
- E–G reliability/manual usability, evidence completion, full fresh checkout and student rehearsal remain. New D browser checks and final read-only-control visibility are unobserved; do not mark them passed.
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
