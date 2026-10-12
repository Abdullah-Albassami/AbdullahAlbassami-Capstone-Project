# Official guide and evidence matrix

Primary authority: `CapstoneProjectGuide.pdf`, pp.1–6. Total assessment: 100 marks. **Checkpoint A is design/foundation only.** Proposed URLs and future source locations below are not implemented evidence. PASS requires an executed check recorded in ACCEPTANCE_TESTS.md. No score is guaranteed.

## Assessment coverage

| Criterion | Marks | Deliverable / intended feature | Current evidence |
| --- | --- | --- | --- |
| Problem and market potential | 10 | README audience/problem/comparison/adoption; authentic evidence separated from assumptions | Written rationale; market benefits unvalidated |
| Core functionality | 20 | Employee → admin → technician → employee; ticket/category CRUD; comments; safe errors | Planned in DESIGN and WIREFRAMES, not implemented |
| Database and ORM | 20 | Matching ERD/schema, constraints/deletion, all five ORM capabilities | Approved target ERD; actual schema/queries not implemented |
| Django and Python | 15 | Routing, readable reusable logic, ModelForms, inherited templates | Scaffold/settings/shared template; feature evidence pending |
| Interface and usability | 10 | Responsive accessible role pages, confirmations and feedback | Wireframes/shared CSS; browser acceptance pending |
| Verification and reproducibility | 10 | Manual record, focused tests, known fixtures, fresh checkout | Record established; foundation checks tracked separately |
| Git and documentation | 5 | Meaningful validated history and usable README | Original documentation milestone; A milestone prepared |
| Demonstration and understanding | 10 | Guide-ordered demo, personal request/constraint/query explanation | Rehearsal script written; browser demo/student rehearsal pending |
| Total | 100 | Working evidence and individual explanation | Not graded |

## Every guide requirement

| Guide | Requirement | Location / intended evidence | State at A |
| --- | --- | --- | --- |
| p.1 | Defined users, real recognizable problem | README product rationale | Documented; demand unvalidated |
| p.1 | Clear reason to choose product and adoption model | README email/spreadsheet comparison/internal adoption | Documented hypothesis |
| p.1 | Complete manageable scope; persisted realistic workflow | DESIGN workflow; DEMO_SCRIPT | Planned |
| p.1 | Evidence versus assumptions; no commercial launch required | README | Documented |
| p.1 | Instructor-discussed idea; individual project | PROGRESS external facts; attribution/rehearsal | Instructor agreement unverified |
| p.2 | Python/Django relational backend and migrations | config, tickets app; B models/migrations | Scaffold only |
| p.2 | Clear apps/URLs/templates/static, namespaces/inheritance | config/urls.py, base.html, CSS; C namespaces | Partial foundation |
| p.2 | Readable views and repeated logic extracted | C views/services/permissions contracts | Planned |
| p.2 | Discoverable approved UI workflow and persisted records | WIREFRAMES; C role journey | Planned |
| p.2 | Relevant CRUD; cancellation/restricted deletion acceptable | Ticket and category routes; protected deletion tests | Planned |
| p.2 | Useful search/filter, intentional ordering, pagination | /tickets/; query tests | Planned |
| p.2 | Server field/value/business validation and feedback | Model/forms/service; messages | Planned |
| p.2 | Missing records, invalid requests, empty lists | DESIGN HTTP contracts; error/no-result cases | Planned |
| p.2 | Semantic HTML, associated labels, appropriate alt text | base.html; form templates/browser checks | Shared landmarks only |
| p.2 | Responsive consistent interface/navigation/actions | CSS/WIREFRAMES; desktop/mobile browser checks | Browser checks pending |
| p.2 | Empty/error/success states; destructive confirmation | Cancellation/category deletion and bound forms | Planned |
| p.2 | Django auth, server-enforced roles, safe demo information | Middleware/settings; B/C auth/access/admin tests | Foundation only |
| p.2 | Integrations/deployment optional, core independent | DESIGN exclusions | Explicitly excluded |
| p.3 | ERD entities/keys/cardinality/optionality matching models | ERD; B/G schema comparison | Target documented |
| p.3 | Suitable types/lengths/defaults/requiredness | DESIGN exact fields; B models | Target documented |
| p.3 | Normalization and justified FK/other relationships | ERD rationale; no profile/custom M2M | Documented |
| p.3 | Uniqueness/constraints/deletion integrity | DESIGN state checks and PROTECT/CASCADE | Planned |
| p.3 | Repository migrations create fresh schema | B/G migrations and clean checkout | Not run |
| p.3 | Integrated CRUD | /tickets/ and /categories/ | Planned |
| p.3 | Integrated filtering/ordering | /tickets/ query controls | Planned |
| p.3 | Integrated relationship queries | Category name traversal/detail related objects | Planned |
| p.3 | At least one queryset aggregate | / admin totals via aggregate Count | Planned |
| p.3 | At least one per-result annotation | / and /categories/ filtered per-row Counts | Planned |
| p.3 | Useful displayed summaries/decision explanation | Category backlog and technician assignments | Planned |
| p.3 | Realistic multi-row/edge data; correct totals and empty metrics | Seed 12/8/2/2; zero-row/multi-join tests | Planned |
| p.4 | Design/first workflow/completion/readiness checkpoints | PROGRESS | Established |
| p.4 | Prioritized tasks, completion conditions, remaining/blockers | PROGRESS | Established |
| p.4 | Required manual expected/actual/status record; honest limitations | ACCEPTANCE_TESTS | Established; feature checks not run |
| p.4 | Workflow/input/filter/dependency/report/access/mobile/fresh checks | Acceptance rows and B–G tests | Planned |
| p.4 | Important automated tests encouraged, no coverage quota | Django test suite B–E | Not implemented |
| p.4 | Resource/AI acknowledgement and student understanding | README; DEMO_SCRIPT technical rehearsal | Attribution written; rehearsal pending |
| p.4 | Fictional/anonymized data, no secrets, safe config examples | .gitignore/.env.example/runtime settings/seed contract | Config implemented; seed pending |
| p.5 | Source/dependencies/design/verification/demo package | Repository/requirements/docs | Foundation package only |
| p.5 | Instructor repository access | PROGRESS/G final checklist | Unverified |
| p.5 | Setup: environment/install/config/migrate/sample/server; versions | README; G separate fresh checkout | Foundation setup only verified separately |
| p.5 | Concise six-step demo and confirmed duration | DEMO_SCRIPT | Script target; duration unconfirmed |
| p.5 | URL→view→ORM→template, constraint/calculation explanation | DEMO_SCRIPT personal rehearsal | Pending |
| p.5 | Submitted revision matches demo; cleanup/access/setup/core recheck | G final checklist | Pending |
| p.6 | Complete focused dependable product and final checklist | B–G completion/acceptance gates | Product implementation pending |

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
