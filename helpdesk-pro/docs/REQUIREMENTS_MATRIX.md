# Official guide and evidence matrix

Primary authority: [root CapstoneProjectGuide.pdf](../../CapstoneProjectGuide.pdf), pp.1–6. Total assessment: 100 marks. **Checkpoint B database/auth foundation is implemented inside `helpdesk-pro/`; frontend workflows/reports remain C/D.** Application paths are relative to `helpdesk-pro/`. PASS requires an executed check recorded in ACCEPTANCE_TESTS.md. Every official requirement must ultimately map to implemented UI/code, executed verification and documentation. Planned URLs, shell math and data tests alone do not establish integrated frontend ORM evidence. No score is guaranteed.

## Assessment coverage

| Criterion | Marks | Deliverable / intended feature | Current evidence |
| --- | --- | --- | --- |
| Problem and market potential | 10 | README audience/problem/comparison/adoption; authentic evidence separated from assumptions | Written rationale; market benefits unvalidated |
| Core functionality | 20 | Employee → admin → technician → employee; ticket/category CRUD; comments; safe errors | Planned in DESIGN and WIREFRAMES, not implemented |
| Database and ORM | 20 | Matching ERD/schema, constraints/deletion, all five ORM capabilities | B models/migration/schema/integrity verified; integrated UI queries/reports pending C/D |
| Django and Python | 15 | Routing, readable reusable logic, ModelForms, inherited templates | B reusable role/account/model/admin logic verified; application views/forms pending C |
| Interface and usability | 10 | Responsive accessible role pages, confirmations and feedback | Wireframes/shared CSS; browser acceptance pending |
| Verification and reproducibility | 10 | Manual record, focused tests, known fixtures, fresh checkout | 60 tests, local/fresh SQLite migrations and repeated seed passed; manual/browser/fresh-checkout pending |
| Git and documentation | 5 | Meaningful validated history and usable README | Original/A milestones committed; verified B milestone/report delivered |
| Demonstration and understanding | 10 | Guide-ordered demo, personal request/constraint/query explanation | Rehearsal script written; browser demo/student rehearsal pending |
| Total | 100 | Working evidence and individual explanation | Not graded |

## Every guide requirement

| Guide | Requirement | Location / intended evidence | Current state at B |
| --- | --- | --- | --- |
| p.1 | Defined users, real recognizable problem | README product rationale | Documented; demand unvalidated |
| p.1 | Clear reason to choose product and adoption model | README email/spreadsheet comparison/internal adoption | Documented hypothesis |
| p.1 | Complete manageable scope; persisted realistic workflow | DESIGN workflow; DEMO_SCRIPT | Planned |
| p.1 | Evidence versus assumptions; no commercial launch required | README | Documented |
| p.1 | Instructor-discussed idea; individual project | PROGRESS external facts; attribution/rehearsal | Instructor agreement unverified |
| p.2 | Python/Django relational backend and migrations | config; tickets/models.py and migrations/0001_initial.py | Implemented; B02/B03/B04/B07 PASS |
| p.2 | Clear apps/URLs/templates/static, namespaces/inheritance | config/urls.py, base.html, CSS; C namespaces | Partial foundation |
| p.2 | Readable views and repeated logic extracted | tickets/permissions.py and accounts.py; C views/services | Shared B helpers implemented/tested; views/services pending |
| p.2 | Discoverable approved UI workflow and persisted records | WIREFRAMES; C role journey | Planned |
| p.2 | Relevant CRUD; cancellation/restricted deletion acceptable | Ticket/category routes pending; tests/test_models.py | Retention/deletion foundation verified; frontend CRUD pending |
| p.2 | Useful search/filter, intentional ordering, pagination | /tickets/; query tests | Planned |
| p.2 | Server field/value/business validation and feedback | models.py/admin_forms.py; upcoming service/forms | B model/admin validation PASS; workflow feedback pending |
| p.2 | Missing records, invalid requests, empty lists | DESIGN HTTP contracts; error/no-result cases | Planned |
| p.2 | Semantic HTML, associated labels, appropriate alt text | base.html; form templates/browser checks | Shared landmarks only |
| p.2 | Responsive consistent interface/navigation/actions | CSS/WIREFRAMES; desktop/mobile browser checks | Browser checks pending |
| p.2 | Empty/error/success states; destructive confirmation | Cancellation/category deletion and bound forms | Planned |
| p.2 | Django auth, server-enforced roles, safe demo information | permissions/accounts/signals/admin and tests | B password/roles/admin/mutation checks PASS; frontend enforcement pending C |
| p.2 | Integrations/deployment optional, core independent | DESIGN exclusions | Explicitly excluded |
| p.3 | ERD entities/keys/cardinality/optionality matching models | ERD; models.py and schema test | B schema/columns/FKs/constraints verified; final G recheck pending |
| p.3 | Suitable types/lengths/defaults/requiredness | models.py; test_models.py | Implemented/verified B04 |
| p.3 | Normalization and justified FK/other relationships | ERD rationale; no profile/custom M2M | Documented |
| p.3 | Uniqueness/constraints/deletion integrity | models.py, initial migration, model/account tests | Implemented/verified B04; admin checks B05 |
| p.3 | Repository migrations create fresh schema | initial migration; test DB and temporary file | B02/B07 PASS; full G fresh-checkout still pending |
| p.3 | Integrated CRUD | /tickets/ and /categories/ | Planned |
| p.3 | Integrated filtering/ordering | /tickets/ query controls | Planned |
| p.3 | Integrated relationship queries | Category name traversal/detail related objects | Planned |
| p.3 | At least one queryset aggregate | / admin totals via aggregate Count | Planned |
| p.3 | At least one per-result annotation | / and /categories/ filtered per-row Counts | Planned |
| p.3 | Useful displayed summaries/decision explanation | Category backlog and technician assignments | Planned |
| p.3 | Realistic multi-row/edge data; correct totals and empty metrics | demo_data.py/seed_demo; test_seed.py | B04/B06/B07 PASS; rendered reports pending D |
| p.4 | Design/first workflow/completion/readiness checkpoints | PROGRESS | Established |
| p.4 | Prioritized tasks, completion conditions, remaining/blockers | PROGRESS | Established |
| p.4 | Required manual expected/actual/status record; honest limitations | ACCEPTANCE_TESTS | Established; feature checks not run |
| p.4 | Workflow/input/filter/dependency/report/access/mobile/fresh checks | Acceptance rows and tests | B foundation/dependency/access/math checks PASS; full UI/manual checks pending |
| p.4 | Important automated tests encouraged, no coverage quota | tickets/tests/ | 60 B tests PASS; C–E feature tests pending |
| p.4 | Resource/AI acknowledgement and student understanding | README; DEMO_SCRIPT technical rehearsal | Attribution written; rehearsal pending |
| p.4 | Fictional/anonymized data, no secrets, safe config examples | .gitignore/.env.example/settings/demo_data/seed | Implemented; runtime-only passwords, ignored local DB; hygiene verified in B08 |
| p.5 | Source/dependencies/design/verification/demo package | Repository/requirements/docs | B database/auth package delivered; complete application/evidence pending |
| p.5 | Instructor repository access | PROGRESS/G final checklist | Unverified |
| p.5 | Setup: environment/install/config/migrate/sample/server; versions | README, B report; G fresh checkout | B migrations/seed/tests/fresh SQLite PASS; full fresh environment/browser setup pending |
| p.5 | Concise six-step demo and confirmed duration | DEMO_SCRIPT | Script target; duration unconfirmed |
| p.5 | URL→view→ORM→template, constraint/calculation explanation | DEMO_SCRIPT personal rehearsal | Pending |
| p.5 | Submitted revision matches demo; cleanup/access/setup/core recheck | G final checklist | Pending |
| p.6 | Complete focused dependable product and final checklist | C–G completion/acceptance gates | B delivered; complete product remains pending |

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
