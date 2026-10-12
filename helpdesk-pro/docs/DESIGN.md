# Approved architecture and implementation contracts

Approved by the user's implementation request and subsequent eight amendments on 12 October 2026. The official guide is primary. This document incorporates the audit corrections and amended structure; it is the final target for upcoming checkpoints, not a claim that those features already exist. Instructor agreement remains unverified. Work is authorized for Checkpoint A only until its review.

## Structure and responsibilities

Project inside `helpdesk-pro/`; source guide/specification remain at repository root with the entry-point README and repository-wide `.gitignore`. Application documentation and safe environment example belong under `helpdesk-pro/`. One `tickets` app; built-in User/Groups; four custom models; SQLite; Django Templates and local CSS. Python 3.14.7 / Django 5.2.18. All application paths in this document are relative to `helpdesk-pro/`.

Before new dependency installation verify official Django/Python compatibility and actual package metadata, then pin installed/verified dependencies. Recreate the local `.venv` inside `helpdesk-pro/`; do not relocate virtual environments. Settings derive database/template/static paths from the application directory rather than the shell working directory.

Views handle HTTP, bind explicit forms, use scoped retrieval and render/redirect. `permissions.py` resolves roles, visibility and action permissions. Mandatory `services.py` owns ticket mutations and rechecks current state/actor/target; `queries.py` may hold reporting/list queries when reuse improves readability. No repository layer, generic workflow engine, signals for ordinary ticket actions, or custom user model.

Preserve final-first development: inspect each file's intended responsibilities and integration dependencies before writing it; implement the final behavior appropriate to its checkpoint, with genuine defect corrections as needed. Do not substitute temporary models, alternate workflows or extra account-management/audit/integration subsystems. Keep required grading evidence and actual verification mandatory; retain the two-day priority and checkpoint review stops.

Creation and editing forms whitelist title, description, category, department and priority. Assignment, resolution and comments use separate forms. State/requester/author/timestamps never come from editable client fields. Services validate complete instances after session-derived fields are set and save within transactions. Cross-field model errors use non-field validation where forms exclude workflow fields.

## Exact model decisions

All custom IDs use Django's BigAutoField. Required text is trimmed and whitespace-only values fail validation. Category and Department names are case-sensitive unique values. No redundant assignee FK index; Django creates FK indexes. Ticket defaults to newest creation then highest ID; comments oldest creation then ID; categories/departments by name.

| Model | Fields |
| --- | --- |
| Department | name: CharField(100), required/unique |
| Category | name: CharField(100), required/unique; description: TextField, blank allowed |
| Ticket | title: CharField(150); description: TextField; category/department/requester: required FK; assigned_to: nullable/blank FK; priority: CharField(10), low/medium/high, default medium; status: CharField(20), new/assigned/in_progress/resolved/cancelled, default new; resolution_note: TextField, blank allowed; created_at: auto_now_add; updated_at: auto_now; resolved_at: nullable/blank DateTimeField |
| TicketComment | ticket/author: required FK; body: TextField; created_at: auto_now_add |

Ticket reference is a display property derived from its ID, e.g. HD-00001; padding is a minimum width, not a limit. The description, resolution note and comments are plain escaped text. `updated_at` means ticket field/workflow modification; adding a comment does not alter it.

See ERD for every relationship and deletion choice. Cancellation preserves history and any existing assignee. Comments cascade only if a ticket is removed through privileged maintenance; no supported UI permits that deletion. This design retains discussion and final outcomes but is not an event audit log.

### State invariants

Database checks enforce allowed status/priority, assignment/state compatibility, and resolution field pairing:

| State | Assignee | Resolution note / timestamp |
| --- | --- | --- |
| new | Must be null | Empty / null |
| assigned | Required | Empty / null |
| in_progress | Required | Empty / null |
| resolved | Required | Nonempty / required |
| cancelled | Null or retained | Empty / null |

Meaningful trimmed text is additionally enforced by model validation. Related-group eligibility, actor permissions, transition history and terminal immutability are service rules, not cross-table database checks. Every supported mutation calls full validation; `save()` alone does not.

## Roles, provisioning and administration

Exactly one of Employee, Technician and IT Admin per active regular account. Unrelated non-application groups may coexist. No role/conflicting roles fail closed; inactive users cannot authenticate or act. An active superuser is the explicit application IT Admin override. Staff status grants no application role.

| Capability | Employee | Technician | IT Admin |
| --- | --- | --- | --- |
| List/detail/dashboard | Own tickets | Assigned tickets | All tickets |
| Create | Yes | No | Yes |
| Business-field edit | Own unassigned new | No | Any active |
| Cancel | Own new | No | Any active |
| Assign/reassign | No | No | Any active |
| Start/resolve | No | Own assigned, valid state | Valid state |
| Comment | Own active | Assigned active | Any active |
| Category CRUD | No | No | Yes |

Technician eligibility is an active non-superuser account with exactly the Technician application role; a superuser's effective application role is IT Admin. The same predicate supplies form choices and service validation.

Regular IT Admin is staff and receives only Department view/add/change/delete model permissions. Categories are managed in the application. Superusers provision accounts through guarded User admin forms. These forms reject conflicting roles and reject deactivation or loss of Technician role while active tickets remain assigned. Reassign first; historical terminal assignments remain valid. Guard built-in Group administration against rename/delete of the three reserved role groups. Ticket and TicketComment admin are view-only even for superusers, with no add/change/delete or delete-selected action. Direct shell/database maintenance is privileged outside the supported workflow.

## Workflow and HTTP contracts

Active statuses are one shared constant: new, assigned, in_progress. Terminal statuses are resolved/cancelled. Services re-fetch current state and scope in a transaction; authorize the actor again and never mutate stale posted model instances. Reassignment immediately removes old technician visibility. Do not claim SQLite row-locking behavior or enterprise concurrency guarantees.

| Action | Contract |
| --- | --- |
| Create | Employee/admin; requester is actor; new/unassigned/no resolution |
| Edit | Five business fields only; role/state rules above |
| Assign | Admin; eligible target; new → assigned; assigned/in_progress reassign preserves state; never blank |
| Start | Assignee/admin; assigned → in_progress only |
| Resolve | Assignee/admin; in_progress → resolved; meaningful note and timezone-aware current timestamp saved together |
| Cancel | Employee own new or admin active; GET confirmation then POST; no hard delete |
| Comment | Authorized active viewer; session author; immutable; terminal thread remains readable |
| Category delete | Admin; GET confirmation then POST; catch PROTECT and explain dependency |

All mutations require POST/CSRF. Success redirects and shows a message. Anonymous requests redirect to login; out-of-scope/missing objects return 404; forbidden role/action returns 403; unsupported method returns 405. Invalid form values return 200 with bound form errors; state conflicts return a friendly 409 page without mutation. Resolve/comment/assignment errors render the ticket detail with the appropriate bound form. Filter parameters are independently validated: retain valid fields and ignore invalid ones with useful feedback. Invalid order defaults to newest; nonnumeric page selects first, out-of-range page selects last.

### Final route map (not wired at Checkpoint A except admin)

| Name | Path | Methods |
| --- | --- | --- |
| login / logout | /accounts/login/ /accounts/logout/ | GET+POST / POST |
| tickets:dashboard | / | GET |
| tickets:ticket_list | /tickets/ | GET |
| tickets:ticket_create | /tickets/new/ | GET+POST |
| tickets:ticket_detail | /tickets/<int:pk>/ | GET |
| tickets:ticket_update | /tickets/<int:pk>/edit/ | GET+POST |
| tickets:ticket_cancel | /tickets/<int:pk>/cancel/ | GET+POST |
| tickets:ticket_assign | /tickets/<int:pk>/assign/ | POST |
| tickets:ticket_start | /tickets/<int:pk>/start/ | POST |
| tickets:ticket_resolve | /tickets/<int:pk>/resolve/ | POST |
| tickets:ticket_comment | /tickets/<int:pk>/comment/ | POST |
| tickets:category_list | /categories/ | GET |
| tickets:category_create | /categories/new/ | GET+POST |
| tickets:category_update | /categories/<int:pk>/edit/ | GET+POST |
| tickets:category_delete | /categories/<int:pk>/delete/ | GET+POST |
| admin:index | /admin/ | Django admin setup |

## Queries and metrics

Ticket list is scoped before searching/filtering/pagination. `q` uses OR over title/description; other filters combine with AND. Status/priority choices and category ModelChoice are validated. Category filtering traverses `category__name` using the selected object's unique name. Ordering whitelist: newest (-created_at, -id), oldest (created_at, id), priority (Case high=0/medium=1/low=2 then -created_at/-id), updated (-updated_at, -id). Ten records per page; preserve sanitized non-page parameters.

Select requester/assignee/category/department in list/detail; retrieve comments with their authors. Dashboard totals use aggregate Count with filtered active/resolved/cancelled counts. Required status breakdown uses grouped counts, with zero for absent statuses. Category rows annotate filtered active tickets; eligible technician rows annotate active assigned tickets, retaining zero rows. Avoid multi-collection joins that multiply counts; use distinct when necessary and verify multi-row fixtures. Employee/technician dashboards use only their visibility queryset. Category backlog helps prioritize issue areas; technician counts support assignment, not real-time availability.

## Deterministic demo data

Usernames: employee1, employee2, technician1, technician2, itadmin. Fictional identities only. Four departments: Finance, Human Resources, Operations, Sales. Categories: Hardware, Software, Network, Accounts, Unused. Reserve ticket IDs 10001–10012 and comment IDs 20001 onward for seeded fixtures; preflight collisions and abort atomically rather than overwrite unrelated data. Reserved usernames/record IDs are documented; preserve existing passwords and user changes on repeat. No destructive reset option.

| Ticket IDs | Status | Active category distribution | Technician |
| --- | --- | --- | --- |
| 10001–10003 | new | Hardware 1, Software 1, Network 1 | None |
| 10004–10006 | assigned | Hardware 1, Software 1, Accounts 1 | technician1: 2; technician2: 1 |
| 10007–10008 | in_progress | Hardware 1, Network 1 | One each |
| 10009–10010 | resolved | Excluded from active | One each |
| 10011–10012 | cancelled | Excluded from active | One null, one retained |

Initial totals: 12 overall; 8 active; 2 resolved; 2 cancelled. Active categories 3/2/2/1/0 and technicians 3/2. Add comments while active before terminal transitions. Additional test fixtures cover zero-workload technician, empty data, several comments/groups, collisions and changed seeded records. The seed command validates runtime DEMO_PASSWORD only for newly created accounts and never prints it. Existing accounts are not silently adopted or promoted on unrelated username collisions; fail with actionable feedback.

## Definition of done and external assumptions

The complete guide-ordered browser journey, useful ORM evidence, required manual record, focused tests, fresh checkout, responsive/accessibility checks, documentation and meaningful Git history must all be verified. No promised score, fabricated PASS, customer evidence or production readiness claim. Deployment/integrations are excluded. Instructor scope approval, presentation duration, repository access and available development hours remain external facts to confirm; they do not block the user-authorized foundation checkpoint.
