# Official guide and evidence matrix

Primary authority: [root CapstoneProjectGuide.pdf](../../CapstoneProjectGuide.pdf), pp.1–6. Total assessment: 100 marks. **A–E implements and audits the four-model ticket/category/query/report application. All five ORM capabilities remain integrated. E passes 149 Django tests and 39 real Chrome checks.** PASS sources are distinguished in ACCEPTANCE_TESTS: UC01–UC07 user-observed, E04/E05 browser automated, other E checks command/HTTP/inspection. Human/device/fresh-checkout/rehearsal gaps remain; no score is guaranteed.

## Assessment coverage

| Criterion | Marks | Deliverable / intended feature | Current evidence |
| --- | --- | --- | --- |
| Problem and market potential | 10 | README audience/problem/comparison/adoption; authentic evidence separated from assumptions | Written rationale; market benefits unvalidated |
| Core functionality | 20 | Employee → admin → technician → employee; ticket/category CRUD; comments; safe errors | C workflow + D Category CRUD/PROTECT tested; UC01–UC07 user-observed lifecycle |
| Database and ORM | 20 | Matching ERD/schema, constraints/deletion, all five ORM capabilities | Unchanged tested schema; rendered CRUD/filter/order/relationship/aggregate/annotation PASS D01–D06 |
| Django and Python | 15 | Routing, readable reusable logic, ModelForms, inherited templates | Named routes, explicit forms/shared services and queries, inherited pages verified |
| Interface and usability | 10 | Responsive accessible role pages, confirmations and feedback | E real Chrome 1280px/375px, labels/errors/contrast/basic keys/max-text checks and screenshots PASS; human/device/full-keyboard/zoom/screen-reader pending |
| Verification and reproducibility | 10 | Manual record, focused tests, known fixtures, fresh checkout | 149 tests + 39 real Chrome checks PASS; UC user-observed record; full fresh checkout/human checklist pending |
| Git and documentation | 5 | Meaningful validated history and usable README | Original/A–D milestones committed; E report/evidence/remaining instructions and README updated |
| Demonstration and understanding | 10 | Guide-ordered demo, personal request/constraint/query explanation | Rehearsal script written; browser demo/student rehearsal pending |
| Total | 100 | Working evidence and individual explanation | Not graded |

## Every guide requirement

| Guide | Requirement | Location / evidence | Current state at E |
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
| p.2 | Missing records, invalid requests, empty lists | views HTTP gate; error template; list/dashboard empty states | Existing HTTP checks + E03/E04/E05 helpful 405, actual browser errors/no-match/validation PASS |
| p.2 | Semantic HTML, associated labels, appropriate alt text | base/form/table templates; CSS | E04 Chrome landmark/label/error-description/unique-ID checks PASS; no content images; screen reader pending |
| p.2 | Responsive consistent interface/navigation/actions | CSS/WIREFRAMES; desktop/mobile browser checks | E04 fixed-width desktop/emulated mobile layouts and E05 basic keys PASS; human/device/full keyboard/zoom NOT RUN |
| p.2 | Empty/error/success states; destructive confirmation | Ticket/category confirmations, filters/forms/messages | C/D01/D02/D05 PASS: empty/no-match, field/non-field errors, safe delete feedback |
| p.2 | Django auth, server-enforced roles, safe demo information | Built-in-view subclasses; permissions/services/admin; tests | E02/E03 message isolation incl. admin logout, no-store/private headers, forged scope/role/terminal/CSRF tests PASS; browser role/admin checks E05 |
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
| p.4 | Important automated tests encouraged, no coverage quota | tickets/tests/; optional browser scripts | 149 Django + 39 Chrome checks PASS; no arbitrary coverage target; human gaps explicit |
| p.4 | Resource/AI acknowledgement and student understanding | README; DEMO_SCRIPT technical rehearsal | Attribution written; rehearsal pending |
| p.4 | Fictional/anonymized data, no secrets, safe config examples | .gitignore/.env.example/settings/demo_data/seed | Implemented; runtime-only passwords, ignored local DB; hygiene verified in B08 |
| p.5 | Source/dependencies/design/verification/demo package | Repository/requirements/docs | A–E code/design/evidence delivered, authentic browser artifacts and manual instructions; final F/G pending |
| p.5 | Instructor repository access | PROGRESS/G final checklist | Unverified |
| p.5 | Setup: environment/install/config/migrate/sample/server; versions | README, B–D reports; G fresh checkout | D05 fresh SQLite/normal hashing/seed/HTTP PASS; full checkout/environment pending |
| p.5 | Concise six-step demo and confirmed duration | DEMO_SCRIPT | Script target; duration unconfirmed |
| p.5 | URL→view→ORM→template, constraint/calculation explanation | DEMO_SCRIPT personal rehearsal | Pending |
| p.5 | Submitted revision matches demo; cleanup/access/setup/core recheck | G final checklist | Pending |
| p.6 | Complete focused dependable product and final checklist | C–G completion/acceptance gates | E audit/fixes verified; F/G and remaining human/readiness checklist pending |

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

Dashboard copy explains backlog decisions, active statuses and assigned workload versus availability. UC01–UC07 establish reported C browser steps. E automation below covers disposable records; local HD-10013 final human detail/controls, other human/device/full-keyboard checks, fresh checkout and rehearsal remain pending. Do not interpret automation as completed final grading or all manual acceptance.

## E reliability and interface evidence

| Requirement | Implemented correction / source | Executed evidence | Remaining limit |
| --- | --- | --- | --- |
| Safe auth/account privacy and access | ApplicationLoginView/ApplicationLogoutView in [views](../tickets/views.py); common admin logout route in [project URLs](../config/urls.py); application_view never_cache | [ReliabilityTests](../tickets/tests/test_reliability.py): cookie/session messages, login/admin logout, changed roles, forged reports, redirects, CSRF rotation, no-store/private; E02/E03 | No production/concurrency certification; privileged maintenance outside UI |
| Complete lifecycle/terminal safeguards | Unchanged services/permissions/models; readable controls only when permitted | All prior lifecycle tests + all-visible-role terminal/forged-change and stale eligibility regressions; actual Chrome role/terminal/admin journey E05 | User-specific HD-10013 final detail/control human observations still pending |
| Readable names/ticket information | TechnicianChoiceField in [forms](../tickets/forms.py); requester/assignee in shared [ticket table](../templates/tickets/includes/ticket_table.html) | Name/username/fallback/ID/escaping/eligibility and requester HTTP tests; Chrome native selection E02/E05 | No schema/query-role change |
| Helpful invalid methods | method_not_allowed; errors/error.html; 405/Allow retained | Targeted regression + Chrome 405 page E03/E04 | Other expected errors retain existing tested contracts |
| Mobile layout, labels/keys/contrast | [CSS](../static/css/style.css), shared tables, wrap/hint/relative scroll containment and stronger borders | E04/E05: 34 page/viewport cases, 3 key checks; [actual results](evidence/checkpoint-e/results.json), [desktop](evidence/checkpoint-e/dashboard-desktop.png), [mobile](evidence/checkpoint-e/dashboard-mobile.png), [long confirmation](evidence/checkpoint-e/long-category-confirmation.png) | Physical mobile, other browsers, full human keyboard/zoom/screen reader NOT RUN; no WCAG certification |
| Reproducible verification/accurate manual record | [browser fixture](../scripts/browser_fixture.py), [CDP runner](../scripts/verify_browser.mjs), [manual instructions](MANUAL_BROWSER_CHECKS.md) | 149 tests, 39 genuine Chrome checks, system/migration/dependency/read-only snapshot/integrity checks; E02–E06 | F/G final documentation/checkout/rehearsal gated; UC remains user-attributed |

Models/migrations/ERD and all working app/account/role data are unchanged. Screenshots depict disposable fictional fixtures (initial 12 tickets), not the local 13-ticket dataset. The browser-only setup superuser was created in that temporary database and removed with it. Browser automation evidence does not upgrade unexecuted manual rows to PASS.
