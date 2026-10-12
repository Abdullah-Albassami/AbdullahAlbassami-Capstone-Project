# Official guide and evidence matrix

Primary authority: [root CapstoneProjectGuide.pdf](../../CapstoneProjectGuide.pdf), pp.1–6. Total assessment: 100 marks. **C implements the ticket web workflow and basic role summaries inside `helpdesk-pro/`; category CRUD, advanced list controls and full reports remain D.** Application paths are relative to `helpdesk-pro/`. PASS requires an executed check recorded in ACCEPTANCE_TESTS.md. Every official requirement must ultimately map to implemented UI/code, executed verification and documentation. Planned URLs, shell math and data tests alone do not establish integrated frontend ORM evidence. No score is guaranteed.

## Assessment coverage

| Criterion | Marks | Deliverable / intended feature | Current evidence |
| --- | --- | --- | --- |
| Problem and market potential | 10 | README audience/problem/comparison/adoption; authentic evidence separated from assumptions | Written rationale; market benefits unvalidated |
| Core functionality | 20 | Employee → admin → technician → employee; ticket/category CRUD; comments; safe errors | C ticket journey/CRUD/comments verified; category CRUD pending D |
| Database and ORM | 20 | Matching ERD/schema, constraints/deletion, all five ORM capabilities | B schema + C integrated ticket CRUD/related display/summary aggregate verified; advanced queries/annotation pending D |
| Django and Python | 15 | Routing, readable reusable logic, ModelForms, inherited templates | C namespaced routes, shared services, explicit forms/views and inherited templates verified |
| Interface and usability | 10 | Responsive accessible role pages, confirmations and feedback | C usable role pages and rendered form/landmark checks; real browser acceptance pending |
| Verification and reproducibility | 10 | Manual record, focused tests, known fixtures, fresh checkout | 101 tests + CSRF-enforced fresh seeded HTTP workflow passed; manual/browser/full-checkout pending |
| Git and documentation | 5 | Meaningful validated history and usable README | Original/A/B milestones committed; C evidence/report and README updated |
| Demonstration and understanding | 10 | Guide-ordered demo, personal request/constraint/query explanation | Rehearsal script written; browser demo/student rehearsal pending |
| Total | 100 | Working evidence and individual explanation | Not graded |

## Every guide requirement

| Guide | Requirement | Location / intended evidence | Current state at C |
| --- | --- | --- | --- |
| p.1 | Defined users, real recognizable problem | README product rationale | Documented; demand unvalidated |
| p.1 | Clear reason to choose product and adoption model | README email/spreadsheet comparison/internal adoption | Documented hypothesis |
| p.1 | Complete manageable scope; persisted realistic workflow | DESIGN workflow; DEMO_SCRIPT; services/views | C03/C05/C06 persisted ticket journey PASS; final scope completion pending |
| p.1 | Evidence versus assumptions; no commercial launch required | README | Documented |
| p.1 | Instructor-discussed idea; individual project | PROGRESS external facts; attribution/rehearsal | Instructor agreement unverified |
| p.2 | Python/Django relational backend and migrations | config; tickets/models.py and migrations/0001_initial.py | Implemented; B02/B03/B04/B07 PASS |
| p.2 | Clear apps/URLs/templates/static, namespaces/inheritance | config/urls.py, tickets/urls.py, base.html, CSS | C routes/inherited templates verified C03/C07 |
| p.2 | Readable views and repeated logic extracted | tickets/permissions.py, accounts.py, views.py, services.py | Shared service/form/permission boundary verified C03/C04 |
| p.2 | Discoverable approved UI workflow and persisted records | WIREFRAMES; role pages and forms | HTTP journey PASS C05/C06; browser walkthrough pending |
| p.2 | Relevant CRUD; cancellation/restricted deletion acceptable | Ticket create/detail/edit/cancel; tests/test_views.py | C ticket CRUD PASS C03/C05/C06; category CRUD D |
| p.2 | Useful search/filter, intentional ordering, pagination | /tickets/; query tests | Basic newest-first implemented; advanced controls/pagination D |
| p.2 | Server field/value/business validation and feedback | models/admin_forms/forms/services; messages | B validation and C form/action/forged-field tests PASS C03/C04 |
| p.2 | Missing records, invalid requests, empty lists | views HTTP gate; error template; list/dashboard empty states | 403/404/405/409, bound errors and empty queues PASS C03/C04/C07 |
| p.2 | Semantic HTML, associated labels, appropriate alt text | base/form/table templates; CSS | Rendered landmarks/labels/unique IDs PASS C07; no content images; browser pending |
| p.2 | Responsive consistent interface/navigation/actions | CSS/WIREFRAMES; desktop/mobile browser checks | Responsive templates delivered; actual viewport/keyboard checks NOT RUN |
| p.2 | Empty/error/success states; destructive confirmation | Cancellation confirmation, bound forms/messages | C HTTP/template checks PASS; category confirmation D |
| p.2 | Django auth, server-enforced roles, safe demo information | Login/LogoutView; permissions/services/admin; tests | B guards + C login/logout/CSRF/ownership/state checks PASS C03/C04 |
| p.2 | Integrations/deployment optional, core independent | DESIGN exclusions | Explicitly excluded |
| p.3 | ERD entities/keys/cardinality/optionality matching models | ERD; models.py and schema test | B schema/columns/FKs/constraints verified; final G recheck pending |
| p.3 | Suitable types/lengths/defaults/requiredness | models.py; test_models.py | Implemented/verified B04 |
| p.3 | Normalization and justified FK/other relationships | ERD rationale; no profile/custom M2M | Documented |
| p.3 | Uniqueness/constraints/deletion integrity | models.py, initial migration, model/account tests | Implemented/verified B04; admin checks B05 |
| p.3 | Repository migrations create fresh schema | initial migration; test DB and temporary file | B02/B07 PASS; full G fresh-checkout still pending |
| p.3 | Integrated CRUD | /tickets/ and /categories/ | C ticket CRUD verified; category CRUD D |
| p.3 | Integrated filtering/ordering | /tickets/ query controls | Newest-first scoped list implemented; query controls D |
| p.3 | Integrated relationship queries | Category name traversal/detail related objects | C detail select_related + comment authors verified C05/C07; explicit category filter D |
| p.3 | At least one queryset aggregate | / role summaries via aggregate Count | C dashboard integrated and scoped counts tested C03/C05; complete reports D |
| p.3 | At least one per-result annotation | / and /categories/ filtered per-row Counts | Planned |
| p.3 | Useful displayed summaries/decision explanation | Basic role summary; category backlog and technician assignments | C own/all active/outcome summaries verified; backlog/workload D |
| p.3 | Realistic multi-row/edge data; correct totals and empty metrics | demo_data.py/seed_demo; test_seed.py | B04/B06/B07 PASS; rendered reports pending D |
| p.4 | Design/first workflow/completion/readiness checkpoints | PROGRESS | Established |
| p.4 | Prioritized tasks, completion conditions, remaining/blockers | PROGRESS | Established |
| p.4 | Required manual expected/actual/status record; honest limitations | ACCEPTANCE_TESTS | Established; feature checks not run |
| p.4 | Workflow/input/filter/dependency/report/access/mobile/fresh checks | Acceptance rows and tests | B foundation/dependency/access/math checks PASS; full UI/manual checks pending |
| p.4 | Important automated tests encouraged, no coverage quota | tickets/tests/ | 101 B/C tests PASS; D/E remaining feature tests pending |
| p.4 | Resource/AI acknowledgement and student understanding | README; DEMO_SCRIPT technical rehearsal | Attribution written; rehearsal pending |
| p.4 | Fictional/anonymized data, no secrets, safe config examples | .gitignore/.env.example/settings/demo_data/seed | Implemented; runtime-only passwords, ignored local DB; hygiene verified in B08 |
| p.5 | Source/dependencies/design/verification/demo package | Repository/requirements/docs | B/C delivered; D–G remaining features/evidence pending |
| p.5 | Instructor repository access | PROGRESS/G final checklist | Unverified |
| p.5 | Setup: environment/install/config/migrate/sample/server; versions | README, B/C reports; G fresh checkout | Fresh SQLite seed/CSRF workflow PASS C06; full fresh environment/browser setup pending |
| p.5 | Concise six-step demo and confirmed duration | DEMO_SCRIPT | Script target; duration unconfirmed |
| p.5 | URL→view→ORM→template, constraint/calculation explanation | DEMO_SCRIPT personal rehearsal | Pending |
| p.5 | Submitted revision matches demo; cleanup/access/setup/core recheck | G final checklist | Pending |
| p.6 | Complete focused dependable product and final checklist | C–G completion/acceptance gates | C delivered; D–G and final manual checklist remain pending |

## Implemented B evidence links

| Official requirement | Implemented location / interface | Executed verification | Documentation |
| --- | --- | --- | --- |
| ERD, fields, relationships, integrity | [models.py](../tickets/models.py); [initial migration](../tickets/migrations/0001_initial.py) | ModelTests including schema/SQL FK/constraint introspection; B02–B04/B07 | ERD, DESIGN |
| Django authentication and role restrictions | [permissions.py](../tickets/permissions.py): get_role, visible_tickets, ticket_permissions, eligible_technicians | PermissionTests; B04 | DESIGN/README; application URLs pending C |
| Account safeguards and provisioning | [accounts.py](../tickets/accounts.py), [signals.py](../tickets/signals.py), [admin forms](../tickets/admin_forms.py) | AccountSafeguardTests and admin form/POST tests; B04/B05 | DESIGN/README |
| Secure administration / helpful protected deletion | [admin.py](../tickets/admin.py); /admin/ Department/User/Group/Ticket/Comment routes | AdminTests: forged POST 403, guarded forms, protected deletion 200/no mutation; B05 | README/B report |
| Realistic related sample data, known metric math | [fixtures](../tickets/demo_data.py), [seed command](../tickets/management/commands/seed_demo.py) | SeedTests; local/fresh seed twice; B04/B06/B07 | README/DEMO_SCRIPT; UI reports pending D |
| Reproducible schema and honest testing | migrations, seed, [tests](../tickets/tests/test_seed.py) | 60 tests; no migration drift/pending migrations; fresh SQLite | ACCEPTANCE_TESTS/B report; full checkout pending G |

## Feature evidence references to complete during implementation

| Capability | Final UI | Intended code | Required check |
| --- | --- | --- | --- |
| CRUD | Ticket create/detail/edit/cancel; category list/create/edit/delete | models, forms, views, services | Persist/update/retire; unused deletion and PROTECT |
| Filtering/ordering | /tickets/ | Filter form and list query | Combined filters, related category, stable priority ordering/page links |
| Relationship query | /tickets/ and ticket detail | category__name; select_related and comment authors | Correct filtered result, related display, no scope leak |
| Aggregation | / IT Admin | aggregate filtered Count | Initial 12 total / 8 active / 2 resolved / 2 cancelled |
| Annotation | / and /categories/ | Category/technician annotate filtered Count | Categories 3/2/2/1/0; technicians 3/2; zero-workload fixture |
| Access/validation | All actions | permissions/forms/services; guarded admin | GET/POST bypasses, stale states, inactive/conflicting roles |
| Reproducibility | README/seed/migrations | management command and committed schema | New checkout, seed twice, checks/tests and browser journey |

Add actual source line references and executed-check IDs as each feature is delivered. Isolated shell query examples, planned URLs and unexecuted tests do not establish integration.

## Implemented C evidence links

| Official requirement | Implemented URL/code | Executed verification | Documentation |
| --- | --- | --- | --- |
| Django authentication/POST logout/CSRF | /accounts/login/; /accounts/logout/; [project URLs](../config/urls.py); [settings](../config/settings.py) | WorkflowViewTests login/logout/inactive/safe-next/CSRF tests; C03/C04 | README; DESIGN |
| Persisted relevant ticket CRUD and full role journey | /tickets/new/; /tickets/&lt;id&gt;/; /edit/; /cancel/; [services](../tickets/services.py); [views](../tickets/views.py) | WorkflowServiceTests and complete persisted HTTP journey; C03/C05/C06 | DESIGN; C report; DEMO_SCRIPT |
| Assignment/progress/resolution/comments and server permissions | /assign/; /start/; /resolve/; /comment/ under ticket reference; [forms](../tickets/forms.py) | [service tests](../tickets/tests/test_services.py), [HTTP tests](../tickets/tests/test_views.py): forged fields, scope, all transitions, reassignment, terminal restrictions | README; C03/C04/C05 |
| Related retrieval and useful role summary | /tickets/&lt;id&gt;/ related fields/authors; / aggregate cards and recent tickets | role_scoped_lists_dashboards_and_related_detail; complete role journey; C05/C07 | DESIGN; ERD; full relationship filter/annotation D |
| Validation/helpful failures/confirmation/semantic interface | [templates](../templates/tickets/ticket_detail.html), [field include](../templates/tickets/includes/form_fields.html), [confirmation](../templates/tickets/ticket_cancel_confirm.html), [CSS](../static/css/style.css) | C03/C04/C07 HTTP errors, field/non-field errors, escaping, labels/landmarks/POST/CSRF | ACCEPTANCE_TESTS; browser M01/M02/M06/M07/M10/M12 still NOT RUN |
| Reproducible integrated fictional data | Existing seed/models reused without schema change | C06 fresh seeded database/normal hashing/CSRF journey/connection reopen; C01/C02 checks | README; C report; full checkout G |

The five-status breakdown, per-category and per-technician annotations, category CRUD and validated list queries/pagination are explicitly unimplemented until D. Their matrix entries are targets, not satisfied criteria.
