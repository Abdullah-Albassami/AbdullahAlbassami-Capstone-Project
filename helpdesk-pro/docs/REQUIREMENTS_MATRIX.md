# Official guide and evidence matrix

Primary authority: [root CapstoneProjectGuide.pdf](../../CapstoneProjectGuide.pdf), pp.1–6. Total assessment: 100 marks. **A–D implements ticket/category CRUD, scoped queries/pagination and full reports inside helpdesk-pro. All five ORM capabilities are integrated in rendered features.** Application paths are relative to helpdesk-pro. PASS requires executed or explicitly user-observed evidence in ACCEPTANCE_TESTS. UC01–UC07 are user-observed; other manual/readiness cases remain pending. No score is guaranteed.

## Assessment coverage

| Criterion | Marks | Deliverable / intended feature | Current evidence |
| --- | --- | --- | --- |
| Problem and market potential | 10 | README audience/problem/comparison/adoption; authentic evidence separated from assumptions | Written rationale; market benefits unvalidated |
| Core functionality | 20 | Employee → admin → technician → employee; ticket/category CRUD; comments; safe errors | C workflow + D Category CRUD/PROTECT tested; UC01–UC07 user-observed lifecycle |
| Database and ORM | 20 | Matching ERD/schema, constraints/deletion, all five ORM capabilities | Unchanged tested schema; rendered CRUD/filter/order/relationship/aggregate/annotation PASS D01–D06 |
| Django and Python | 15 | Routing, readable reusable logic, ModelForms, inherited templates | Named routes, explicit forms/shared services and queries, inherited pages verified |
| Interface and usability | 10 | Responsive accessible role pages, confirmations and feedback | D rendered pages/forms/empty/error/report explanations checked; viewport/keyboard/manual acceptance pending |
| Verification and reproducibility | 10 | Manual record, focused tests, known fixtures, fresh checkout | 133 tests + CSRF fresh seeded integration PASS; user-observed C record; D browser/full-checkout pending |
| Git and documentation | 5 | Meaningful validated history and usable README | Original/A–C milestones committed; D evidence/report/README updated |
| Demonstration and understanding | 10 | Guide-ordered demo, personal request/constraint/query explanation | Rehearsal script written; browser demo/student rehearsal pending |
| Total | 100 | Working evidence and individual explanation | Not graded |

## Every guide requirement

| Guide | Requirement | Location / evidence | Current state at D |
| --- | --- | --- | --- |
| p.1 | Defined users, real recognizable problem | README product rationale | Documented; demand unvalidated |
| p.1 | Clear reason to choose product and adoption model | README email/spreadsheet comparison/internal adoption | Documented hypothesis |
| p.1 | Complete manageable scope; persisted realistic workflow | DESIGN; DEMO_SCRIPT; services/views | C03/C05/C06 and UC01–UC07 lifecycle; D features implemented; readiness pending |
| p.1 | Evidence versus assumptions; no commercial launch required | README | Documented |
| p.1 | Instructor-discussed idea; individual project | PROGRESS external facts; attribution/rehearsal | Instructor agreement unverified |
| p.2 | Python/Django relational backend and migrations | config; tickets/models.py and migrations/0001_initial.py | Implemented; B02/B03/B04/B07 PASS |
| p.2 | Clear apps/URLs/templates/static, namespaces/inheritance | config/urls.py, tickets/urls.py, base.html, CSS | C routes/inherited templates verified C03/C07 |
| p.2 | Readable views and repeated logic extracted | tickets/permissions.py, accounts.py, views.py, services.py | Shared service/form/permission boundary verified C03/C04 |
| p.2 | Discoverable approved UI workflow and persisted records | WIREFRAMES; role pages/forms; category navigation | C/D HTTP journey PASS; user-observed UC01–UC07; remaining browser checks pending |
| p.2 | Relevant CRUD; cancellation/restricted deletion acceptable | Ticket/category named routes and services | C ticket CRUD + D01 Category CRUD and PROTECT PASS |
| p.2 | Useful search/filter, intentional ordering, pagination | /tickets/; queries.ticket_list_page; filter form | D02/D05 PASS: combined search/filter, four orders, ten/page, safe parameters |
| p.2 | Server field/value/business validation and feedback | models/admin_forms/forms/services; messages | B validation and C form/action/forged-field tests PASS C03/C04 |
| p.2 | Missing records, invalid requests, empty lists | views HTTP gate; error template; list/dashboard empty states | 403/404/405/409, bound errors and empty queues PASS C03/C04/C07 |
| p.2 | Semantic HTML, associated labels, appropriate alt text | base/form/table templates; CSS | Rendered landmarks/labels/unique IDs PASS C07; no content images; browser pending |
| p.2 | Responsive consistent interface/navigation/actions | CSS/WIREFRAMES; desktop/mobile browser checks | Responsive templates delivered; actual viewport/keyboard checks NOT RUN |
| p.2 | Empty/error/success states; destructive confirmation | Ticket/category confirmations, filters/forms/messages | C/D01/D02/D05 PASS: empty/no-match, field/non-field errors, safe delete feedback |
| p.2 | Django auth, server-enforced roles, safe demo information | Login/LogoutView; permissions/services/admin; tests | B guards + C login/logout/CSRF/ownership/state checks PASS C03/C04 |
| p.2 | Integrations/deployment optional, core independent | DESIGN exclusions | Explicitly excluded |
| p.3 | ERD entities/keys/cardinality/optionality matching models | ERD; models.py and schema test | B schema/columns/FKs/constraints verified; final G recheck pending |
| p.3 | Suitable types/lengths/defaults/requiredness | models.py; test_models.py | Implemented/verified B04 |
| p.3 | Normalization and justified FK/other relationships | ERD rationale; no profile/custom M2M | Documented |
| p.3 | Uniqueness/constraints/deletion integrity | models.py, initial migration, model/account tests | Implemented/verified B04; admin checks B05 |
| p.3 | Repository migrations create fresh schema | initial migration; test DB and temporary file | B02/B07 PASS; full G fresh-checkout still pending |
| p.3 | Integrated CRUD | /tickets/ and /categories/ | C ticket + D01 category interface/services verified |
| p.3 | Integrated filtering/ordering | /tickets/ query controls | D02/D05 scoped Q/AND/Case/order/page behavior PASS |
| p.3 | Integrated relationship queries | category__name; detail related fields/comment authors | C05/C07 + D02 combined_related_name_query/D05 PASS |
| p.3 | At least one queryset aggregate | / cards and status breakdown; queries.ticket_summary | D03/D05/D06 integrated filtered aggregate, zero-safe/live/role scope PASS |
| p.3 | At least one per-result annotation | / and /categories/ filtered distinct Count | D03/D05 category_backlog and technician_workload rendered/verified |
| p.3 | Useful displayed summaries/decision explanation | dashboard/category descriptions and tables | Category backlog prioritization; workload assignment count/availability distinction; D03/D05 PASS |
| p.3 | Realistic multi-row/edge data; correct totals and empty metrics | seed fixtures; ReportingTests | D03 known/zero/empty/multi-comment/group/state-change arithmetic PASS; D06 local actual data |
| p.4 | Design/first workflow/completion/readiness checkpoints | PROGRESS | Established |
| p.4 | Prioritized tasks, completion conditions, remaining/blockers | PROGRESS | Established |
| p.4 | Required manual expected/actual/status record; honest limitations | ACCEPTANCE_TESTS | UC01–UC07 user-observed PASS; M01 partial; remaining manual cases NOT RUN |
| p.4 | Workflow/input/filter/dependency/report/access/mobile/fresh checks | Acceptance rows and tests | B foundation/dependency/access/math checks PASS; full UI/manual checks pending |
| p.4 | Important automated tests encouraged, no coverage quota | tickets/tests/ | 133 B–D tests PASS; remaining E verification not claimed |
| p.4 | Resource/AI acknowledgement and student understanding | README; DEMO_SCRIPT technical rehearsal | Attribution written; rehearsal pending |
| p.4 | Fictional/anonymized data, no secrets, safe config examples | .gitignore/.env.example/settings/demo_data/seed | Implemented; runtime-only passwords, ignored local DB; hygiene verified in B08 |
| p.5 | Source/dependencies/design/verification/demo package | Repository/requirements/docs | A–D code/design/evidence delivered; final E–G evidence/rehearsal pending |
| p.5 | Instructor repository access | PROGRESS/G final checklist | Unverified |
| p.5 | Setup: environment/install/config/migrate/sample/server; versions | README, B–D reports; G fresh checkout | D05 fresh SQLite/normal hashing/seed/HTTP PASS; full checkout/environment pending |
| p.5 | Concise six-step demo and confirmed duration | DEMO_SCRIPT | Script target; duration unconfirmed |
| p.5 | URL→view→ORM→template, constraint/calculation explanation | DEMO_SCRIPT personal rehearsal | Pending |
| p.5 | Submitted revision matches demo; cleanup/access/setup/core recheck | G final checklist | Pending |
| p.6 | Complete focused dependable product and final checklist | C–G completion/acceptance gates | D features delivered; E–G and remaining manual/readiness checklist pending |

## Implemented B evidence links

| Official requirement | Implemented location / interface | Executed verification | Documentation |
| --- | --- | --- | --- |
| ERD, fields, relationships, integrity | [models.py](../tickets/models.py); [initial migration](../tickets/migrations/0001_initial.py) | ModelTests including schema/SQL FK/constraint introspection; B02–B04/B07 | ERD, DESIGN |
| Django authentication and role restrictions | [permissions.py](../tickets/permissions.py): get_role, visible_tickets, ticket_permissions, eligible_technicians | PermissionTests; B04 | DESIGN/README; implemented application URLs below |
| Account safeguards and provisioning | [accounts.py](../tickets/accounts.py), [signals.py](../tickets/signals.py), [admin forms](../tickets/admin_forms.py) | AccountSafeguardTests and admin form/POST tests; B04/B05 | DESIGN/README |
| Secure administration / helpful protected deletion | [admin.py](../tickets/admin.py); /admin/ Department/User/Group/Ticket/Comment routes | AdminTests: forged POST 403, guarded forms, protected deletion 200/no mutation; B05 | README/B report |
| Realistic related sample data, known metric math | [fixtures](../tickets/demo_data.py), [seed command](../tickets/management/commands/seed_demo.py) | SeedTests; local/fresh seed twice; B04/B06/B07 | README/DEMO_SCRIPT; integrated D reports below |
| Reproducible schema and honest testing | migrations, seed, [tests](../tickets/tests/test_seed.py) | 60 tests; no migration drift/pending migrations; fresh SQLite | ACCEPTANCE_TESTS/B report; full checkout pending G |

## Feature evidence summary

| Capability | Implemented UI | Code | Executed/remaining evidence |
| --- | --- | --- | --- |
| CRUD | Ticket create/detail/edit/cancel; category list/create/detail/edit/delete | models/forms/views/services | C05, D01/D05; browser C subset UC01–UC07; category manual pending |
| Filtering/ordering | /tickets/ | TicketFilterForm; ticket_list_page | D02/D05 combined filters/business priority/order/page links; manual pending |
| Relationship query | /tickets/ and ticket detail | category__name; select_related/comments authors | C05/D02/D05 correct related/scoped results |
| Aggregation | / dashboard | ticket_summary aggregate filtered Count | D03/D05 pristine 12/8/2/2; D06 live 13/8/3/2; zero/state-change scope verified |
| Annotation | / and /categories/ | category_backlog; technician_workload | D03/D05 categories 3/2/2/1/0; technicians 3/2/zero; no inflation |
| Access/validation | All actions | permissions/forms/services; guarded admin | GET/POST bypasses, stale states, inactive/conflicting roles |
| Reproducibility | README/seed/migrations | management command and committed schema | New checkout, seed twice, checks/tests and browser journey |

Add actual source line references and executed-check IDs as each feature is delivered. Isolated shell query examples, planned URLs and unexecuted tests do not establish integration.

## Implemented C evidence links

| Official requirement | Implemented URL/code | Executed verification | Documentation |
| --- | --- | --- | --- |
| Django authentication/POST logout/CSRF | /accounts/login/; /accounts/logout/; [project URLs](../config/urls.py); [settings](../config/settings.py) | WorkflowViewTests login/logout/inactive/safe-next/CSRF tests; C03/C04 | README; DESIGN |
| Persisted relevant ticket CRUD and full role journey | /tickets/new/; /tickets/&lt;id&gt;/; /edit/; /cancel/; [services](../tickets/services.py); [views](../tickets/views.py) | WorkflowServiceTests and complete persisted HTTP journey; C03/C05/C06 | DESIGN; C report; DEMO_SCRIPT |
| Assignment/progress/resolution/comments and server permissions | /assign/; /start/; /resolve/; /comment/ under ticket reference; [forms](../tickets/forms.py) | [service tests](../tickets/tests/test_services.py), [HTTP tests](../tickets/tests/test_views.py): forged fields, scope, all transitions, reassignment, terminal restrictions | README; C03/C04/C05 |
| Related retrieval and useful role summary | /tickets/&lt;id&gt;/ related fields/authors; / aggregate cards and recent tickets | role_scoped_lists_dashboards_and_related_detail; complete role journey; C05/C07 | DESIGN; ERD; D relationship/annotation evidence below |
| Validation/helpful failures/confirmation/semantic interface | [templates](../templates/tickets/ticket_detail.html), [field include](../templates/tickets/includes/form_fields.html), [confirmation](../templates/tickets/ticket_cancel_confirm.html), [CSS](../static/css/style.css) | C03/C04/C07 HTTP errors, field/non-field errors, escaping, labels/landmarks/POST/CSRF | ACCEPTANCE_TESTS; M01 partial (user-observed); other listed manual cases NOT RUN |
| Reproducible integrated fictional data | Existing seed/models reused without schema change | C06 fresh seeded database/normal hashing/CSRF journey/connection reopen; C01/C02 checks | README; C report; full checkout G |

## Exact integrated ORM evidence at D

The routes are defined in [urls.py](../tickets/urls.py); query helpers in [queries.py](../tickets/queries.py). Each row names the actual view, query and rendered page. Values are computed from authorized persisted records, never from fixture constants.

| Capability | View and URL | Actual ORM query | Rendered template | Executed evidence |
| --- | --- | --- | --- | --- |
| CRUD | views.category_create/list/detail/update/delete; /categories/, /categories/new/, /categories/&lt;id&gt;/, /edit/, /delete/ | services.create_category/update_category use full_clean/save; get_admin_category retrieves; delete_category invokes model.delete with PROTECT | [category list](../templates/tickets/category_list.html), [detail](../templates/tickets/category_detail.html), [form](../templates/tickets/category_form.html), [confirmation](../templates/tickets/category_confirm_delete.html) | [CategoryTests](../tickets/tests/test_categories.py); D01/D05; ticket CRUD regressions D04 |
| Filtering and ordering | views.ticket_list; /tickets/?q=...&status=...&priority=...&category=...&order=... | ticket_list_page: visible_tickets first; Q(title__icontains) OR Q(description__icontains); AND filters; order_by whitelist; Case priority rank; Paginator ten/page | [ticket_list](../templates/tickets/ticket_list.html); TicketFilterForm; shared ticket table | [TicketQueryTests](../tickets/tests/test_queries.py); D02/D05 scope/search/empty/malformed/ties/page/preservation |
| Relationship queries | views.ticket_list; category detail links to /tickets/?category=&lt;id&gt;; ticket_detail | ticket_list_page.filter(category__name=selected_category.name); list/detail.select_related; ticket.comments.select_related('author') | ticket_list, category_detail, ticket_detail | combined_and_filters_and_explicit_related_name_query verifies join/name predicate and result; C05/D02/D05 |
| Aggregation | views.dashboard; / | ticket_summary: visible_tickets.aggregate(total=Count, active=Count(filter=Q(status__in=ACTIVE_STATUSES)), conditional Count for each Status); one query reused by cards/breakdown | [dashboard](../templates/tickets/dashboard.html) | [ReportingTests](../tickets/tests/test_reports.py); D03/D05/D06 known/live/zero/state-change/role counts; single-aggregate check |
| Annotation | views.dashboard and category_list/detail; / and /categories/ | category_backlog requires IT Admin then Category.annotate(open_ticket_count=Count('tickets', filter=active, distinct=True)); technician_workload requires IT Admin then eligible_technicians.annotate(active_assigned_count=Count('assigned_tickets', filter=active, distinct=True)) | dashboard and [category report table](../templates/tickets/includes/category_report_table.html); category_detail | ReportingTests known values, zero/empty, multiple comments/groups, eligibility/role guards and workflow updates; D03/D05 |

Dashboard copy explains category backlog decisions, active statuses, and assigned workload versus availability. UC01–UC07 establish the reported C browser steps; final read-only controls, new D manual cases, mobile/keyboard, full fresh checkout and student rehearsal remain unverified. Do not interpret feature/HTTP evidence as completed final grading or all manual acceptance.
