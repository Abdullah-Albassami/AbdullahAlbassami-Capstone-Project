# HelpDesk Pro — Codex Implementation Specification

**Status:** Checkpoint A reviewed/approved; Checkpoint B database/auth foundation is complete and verified inside `helpdesk-pro/`. Instructor approval is not independently verified. Checkpoint C has not begun and requires explicit user review and approval.
**Timebox:** Two calendar days.  
**Source of requirements:** `CapstoneProjectGuide.pdf`, pages 1–6.
**Purpose:** Build a presentable, individually explainable Django web app that satisfies the capstone's 100-mark rubric.  
**Principle:** Deliver the complete defined capstone scope and all rubric evidence; design dependencies up front and implement final intended versions, correcting verified defects whenever necessary.

**Approved audit corrections:** `helpdesk-pro/docs/DESIGN.md` records the exact architecture, security, state constraints, URL/error contracts and fixture decisions approved by the user. The official guide is primary; the approved audit and latest user amendments replace conflicting original proposals. `helpdesk-pro/docs/PROGRESS.md` records the revised A–G sequence and actual checkpoint status. No planned feature or check is evidence of implemented or passing behavior.

## Approved user amendments and execution boundary

1. **Repository structure:** Keep `CapstoneProjectGuide.pdf` and this specification at the repository root. Put the Django application, dependencies, configuration example, templates, assets and application documentation inside `helpdesk-pro/`. Keep a root README entry point and repository-wide `.gitignore`.
2. **Compatibility before installation:** Verify the actual Python 3.14.7 interpreter against official Django support documentation and package metadata before any new dependency installation. Use the compatible supported Django 5.2.18 LTS release and pin the dependencies actually installed and verified. Recreate virtual environments at their intended location; do not relocate a virtual environment with embedded absolute paths.
3. **Bounded complexity:** Retain four custom models, three application roles and the approved lifecycle. Use built-in Django auth/admin and small shared validation/permission/service functions; do not introduce account-management, event audit-trail or integration subsystems.
4. **Mandatory grading evidence:** Map every official requirement to its implemented UI/code, executed verification and documentation. Record incomplete/unverified evidence honestly until later checkpoints deliver it.
5. **Final-first implementation:** Inspect complete responsibilities and integration contracts before edits. Implement intended final behavior at each stage; extend it through planned checkpoints without temporary alternative implementations. Correct discovered defects.
6. **Checkpoint gates:** Each checkpoint delivers integrated, verified work appropriate to its stage. The latest authorization covers Checkpoint B only. Stop and wait for explicit review/approval before C.
7. **Two-day priority:** Preserve rubric compliance, working behavior, reproducibility and demonstration readiness. Keep the approximately 20-hour A–G plan including contingency; optional polish follows mandatory evidence.
8. **Truthful documentation:** Report commands and actual outcomes; distinguish historic checks from revalidation at the corrected path. Never label unexecuted tests, browser checks, migrations or final features as passed.

## 1. Product definition

**Product:** HelpDesk Pro, an internal IT support ticket management web application.  
**Audience:** Small/medium organizations with employees and a small IT support team.  
**Problem:** Support requests in email or messaging apps are hard to assign, prioritize, track, and report on.  
**Proposed value:** Centralized support workflow, retained discussion and final outcomes, and workload visibility without enterprise ITSM complexity. This is not a full event audit log.
**Market claim status:** Plausible use case and proposed positioning, NOT validated demand. Avoid fabricated figures or customer claims.  
**Adoption model:** An organization can host internally; an optional future subscription or managed-hosting model can be discussed, not implemented.

### Completed demo journey (must work through the UI)
1. Sign in as employee and submit an issue with a category, department, priority, title and description.
2. See a ticket reference and persisted status **New**; see the ticket in **My Tickets**.
3. Sign in as administrator and assign the ticket to an available technician.
4. Sign in as assigned technician; see the ticket in **Assigned to Me**.
5. Move the ticket from **Assigned** to **In Progress**; add a comment; resolve with a required resolution note.
6. Employee can see the resolution and comment thread.
7. Administrator can view correct live reports: total active/open tickets, status breakdown, category open count, and tickets per technician.
8. Demonstrate rejected invalid input and authorization failure (not only happy-path success).

## 2. Complete Capstone Scope, mandatory features, and exclusions

### Required for final submission (mandatory)
- Django project, one `tickets` app, SQLite database, migrations committed.
- Authentication with Django's User and Groups; login/logout, role-based pages and object-level authorization.
- Ticket creation, list/detail, update, cancel (safe retirement instead of physical deletion), status transitions, assignment, and comment creation.
- Category CRUD for admins; category delete blocked when referenced by tickets.
- Department model with admin-managed entries (Django admin is acceptable for setup); department chosen per ticket, NOT per user; no UserProfile model.
- Search/filter/order tickets; pagination; useful empty states.
- Dashboard aggregations AND per-row annotations in rendered pages.
- Model/form validation, success/error feedback, responsive templates, tests for core rules.
- Sample data management command, ERD, basic wireframes, README, verification record, reproducible setup and demo usernames with fictitious data; passwords are supplied at runtime and never committed.

### Optional refinements (only after mandatory requirements verified)
- Decorative status chips, additional edge-case tests, extra category reporting. Basic usable work queues, responsive navigation and accessible forms are mandatory.

### Explicit exclusions
- No AI, mail notifications, REST API, SPA, live polling, file uploads, external services, SLA scheduling, multi-tenancy, reporting exports, charts library, Docker, payments, complex role administration, or deployment requirement.
- Do not implement real-time technician availability, escalations, sophisticated workflows, or asset management.

## 2A. Locked decisions that prevent avoidable rework

- The guide does **not** mandate a product called an "MVP" or minimum viable product. This document specifies the **complete capstone scope**; optional features are excluded deliberately, not postponed required work.
- One Django app (`tickets`), built-in `auth.User`, **four** custom models (`Department`, `Category`, `Ticket`, `TicketComment`), SQLite, Django Templates, no custom profile model.
- Departments are selected per ticket, not attached to employees. This represents the **requesting department** recorded for that issue; the same employee may submit for different departments. Do not imply a `User → Department` foreign key in ERD.
- Exactly one application role per regular user: Employee, Technician, or IT Admin, provisioned through Django Groups. Superuser is the only explicit cross-role exception and is treated as IT Admin for app authorization. Users with no applicable group fail closed and receive 403 after authentication. Accounts assigned multiple application roles are rejected by seeding / provisioning and tested or handled as invalid, rather than assigning arbitrary precedence.
- IT Admin is an *application group*; Django `is_staff` alone grants no app admin privileges. Django Admin access remains governed separately by Django's built-in staff/superuser checks.
- `resolved` and `cancelled` are terminal: read-only detail, no edits, reassignment, comments, or state changes. Comment thread remains visible to authorized viewers. No reopen or hard-delete tickets.
- The admin assignment action requires `assigned_to` to be active and have exactly the Technician application role. A new ticket becomes `assigned` upon assignment. Reassigning an already `assigned` or `in_progress` ticket preserves its status. Do not allow clearing an active assignee through the interface or service.
- Ticket creator is the session user, not POST input. Employees may set initial low/medium/high priority as a self-reported urgency; admin may correct it before resolution. The title/description/category/department/priority edit form **never** exposes status, requester, assignee, timestamps or resolution note.
- All rules apply to the UI, view authorization, forms and shared service functions; do not trust hidden buttons or user-supplied fields. Normal invalid actions yield a clear form error or 403/404, not uncaught exceptions.
- Comments are immutable and only added to active, authorized tickets; resolution notes live on Ticket, not on TicketComment, and are required for resolution.
- The canonical active/open set is `new`, `assigned`, `in_progress`; use a single shared constant in all queries, view labels, tests and documentation.
- Do not invent customer research, deployment, production security assurances, or passing test results. The final application is a locally demonstrable capstone, with a credible possible internal adoption model.

## 3. Technologies and structure

Use Django 5.2.18 LTS with the verified local Python 3.14.7 interpreter; verify official compatibility before dependency installation, pin resolved dependencies in `helpdesk-pro/requirements.txt` and record versions actually tested in the application README. Use SQLite, Django templates with semantic HTML, small custom CSS, and minimal vanilla JavaScript only if needed. Avoid unnecessary libraries. The Django project lives inside `helpdesk-pro/`, as required by the user; source guide/specification remain at the repository root.

Final repository layout (feature modules/migrations are created in their approved checkpoints):

```text
repository-root/
  CapstoneProjectGuide.pdf
  HELPDESK_PRO_CODEX_SPEC_FINAL.md
  .gitignore
  README.md                   # links to application setup and evidence
  helpdesk-pro/
    .venv/                    # local only, ignored; never relocated
    manage.py
    requirements.txt
    .env.example              # documentation only; no real credentials
    README.md                 # actual application setup and current status
    config/{__init__.py,settings.py,urls.py,asgi.py,wsgi.py}
    tickets/
      __init__.py
      apps.py
      models.py
      forms.py
      views.py
      urls.py
      admin.py
      permissions.py          # shared object-level authorization helpers
      services.py             # mandatory shared workflow mutation boundary
      migrations/
      tests/                  # or a clearly organized tests.py
      management/commands/seed_demo.py
    templates/
      base.html
      registration/login.html
      tickets/{dashboard.html,ticket_list.html,ticket_detail.html,ticket_form.html,ticket_cancel_confirm.html,category_list.html,category_form.html,category_confirm_delete.html}
    static/css/style.css
    docs/{DESIGN.md,ERD.md,WIREFRAMES.md,ACCEPTANCE_TESTS.md,DEMO_SCRIPT.md,REQUIREMENTS_MATRIX.md,PROGRESS.md}
```

One Django app is enough. Use namespaced URLs, template inheritance, `ModelForm`, Django messages, login-required guards, `get_object_or_404`, POST for mutations, CSRF tokens, and redirect-after-POST.

## 4. Data model: exact target

### Django `User` (built in)
- Use standard User, no custom user model and no plaintext passwords.
- Groups: `Employee`, `Technician`, `IT Admin` (seed these and assign sample users).
- Accounts provisioned using demo seeding or Django admin; no public self-registration.
- Staff/superuser privilege is not a substitute for checking the IT Admin group in application views. A superuser may be an explicit override if consistently designed and tested.

### Department
- `id` default PK.
- `name`: CharField(max_length=100, unique=True), required.
- `__str__` and ordering by name.
- Departments belong to tickets (not directly to users in this approved design).

### Category
- `id` default PK.
- `name`: CharField(max_length=100, unique=True), required.
- `description`: TextField(blank=True).
- `__str__`, ordering by name.

### Ticket
- `id`: default integer PK; show as `HD-00001` in templates (display property, not additional database column).
- `title`: CharField(max_length=150), required; trimmed and non-whitespace.
- `description`: TextField(), required; trimmed and non-whitespace.
- `category`: ForeignKey(Category, on_delete=PROTECT, related_name='tickets').
- `department`: ForeignKey(Department, on_delete=PROTECT, related_name='tickets').
- `requester`: ForeignKey(User, on_delete=PROTECT, related_name='submitted_tickets').
- `assigned_to`: ForeignKey(User, on_delete=PROTECT, related_name='assigned_tickets', null=True, blank=True).
- `priority`: CharField choices `low`, `medium`, `high`; default `medium`.
- `status`: CharField choices `new`, `assigned`, `in_progress`, `resolved`, `cancelled`; default `new`.
- `resolution_note`: TextField(blank=True); required by business validation when resolving.
- `created_at`: DateTimeField(auto_now_add=True).
- `updated_at`: DateTimeField(auto_now=True).
- `resolved_at`: DateTimeField(null=True, blank=True); populate on resolve, otherwise null.
- Meta ordering: newest first (`-created_at`, `-id`); indices on status / assigned_to if justified.
- Business validation for valid assignments/status combinations; do not rely solely on template/client validation.
- If enforcing business rules in `clean()`, invoke full_clean explicitly in mutation service or form paths; Django `save()` alone does NOT call `full_clean()`.

### TicketComment
- `id` default PK.
- `ticket`: ForeignKey(Ticket, on_delete=CASCADE, related_name='comments').
- `author`: ForeignKey(User, on_delete=PROTECT, related_name='ticket_comments').
- `body`: TextField(), trimmed, non-whitespace.
- `created_at`: DateTimeField(auto_now_add=True).
- Meta ordering by `created_at`, then `id`.
- No comment editing/deletion within the approved scope; immutable comments preserve discussion history.
- Comment creation is allowed only while the ticket is active (`new`, `assigned`, `in_progress`); resolved/cancelled tickets keep comments read-only.

### Cardinality/optionality for ERD
- Category 1 → 0..N Tickets; each Ticket has exactly one Category.
- Department 1 → 0..N Tickets; each Ticket has exactly one Department.
- User 1 → 0..N submitted Tickets; each Ticket has exactly one requester.
- User 1 → 0..N assigned Tickets; each Ticket has 0..1 assignee.
- Ticket 1 → 0..N TicketComments; each TicketComment belongs to exactly one Ticket.
- User 1 → 0..N TicketComments; each TicketComment has exactly one author.
- User ↔ Groups is Django auth's built-in M2M; don't invent a custom join model.

### Integrity rules
- All `PROTECT` relationships above prohibit deleting referenced records; active ticket history is preserved.
- Ticket cancellation is the normal safe-removal operation, not a database delete. For rubric evidence, demonstrate category deletion through the UI for an unused category and protected deletion for one in use.
- Must reject assignment of a ticket to a non-Technician user, including crafted POST.
- Must reject `assigned`/`in_progress` ticket without assignee; resolution requires assigned technician and non-blank resolution note.
- Validate invalid status transitions server-side. Consider forms + service boundary and test direct service calls.
- Choose one canonical definition: **active/open tickets** = status in `new`, `assigned`, `in_progress`; `resolved` and `cancelled` excluded.
- Do not allow arbitrary edits to foreign-key requester or created timestamps via form fields.

## 5. Access control matrix

| Capability | Employee | Technician | IT Admin |
|---|---|---|---|
| Login/logout | yes | yes | yes |
| Submit ticket | yes | no | yes |
| List/view | own only | assigned only | all |
| Edit title/description/category/department/priority | own **New**, before assignment only | no | yes for non-terminal tickets |
| Cancel ticket | own **New** only | no | any non-terminal ticket |
| Assign or reassign | no | no | yes for non-terminal ticket |
| Start work (`assigned` → `in_progress`) | no | own assigned only | yes |
| Resolve (`in_progress` → `resolved`) with note | no | own in-progress only | yes |
| Add comment | own visible active tickets | assigned visible active tickets | active tickets |
| Dashboard | own basic counts/list | own assigned workload | all-system reports |
| Category CRUD | no | no | yes |

- Authorize every list queryset AND every detail/mutation request on the server. Do not rely on hidden links.
- Unauthenticated visitors redirect to login; authenticated unauthorized access returns 403 or appropriate safe 404 consistently.
- Prefer explicit role permissions; don't grant employees technician actions because the fields were submitted in a POST.
- Keep resolution terminal. No reopen feature. Do not reassign resolved/cancelled tickets.
- IT Admin can move a `new` ticket to `assigned` by assigning a technician. On reassignment of an `assigned`/`in_progress` ticket, preserve status and make the new technician accountable.
- Simple state transition rules:
  - `new` → `assigned` (admin assigns)
  - `new` → `cancelled` (requester or admin)
  - `assigned` → `in_progress` (assignee/admin)
  - `assigned` → `cancelled` (admin)
  - `in_progress` → `resolved` (assignee/admin, resolution note mandatory)
  - `in_progress` → `cancelled` (admin)
  - `resolved`/`cancelled` → no changes
- Assignment editing is separate from generic form update. An admin cannot resolve without having assigned a technician first.
- Ticket and TicketComment are read-only in Django admin, with add/delete and bulk deletion disabled. Regular IT Admin has staff access and only Department setup permissions; only superusers provision accounts. Protect reserved role groups from rename/deletion and block deactivation/removal of Technician role while active assignments remain.
- Enforce database checks for allowed status/priority, new-without-assignee, required assignment for assigned/in-progress/resolved, and resolution note/timestamp pairing. Non-resolved tickets have an empty note and null resolution timestamp. Cancelled tickets may retain an assignee. Cross-field model errors must be compatible with forms that exclude workflow fields.

## 6. Pages and URLs

| Named URL (suggested) | Path | Page/behavior |
|---|---|---|
| login/logout | `/accounts/login/`, `/accounts/logout/` | Auth; logout via POST |
| `tickets:dashboard` | `/` | Role-specific dashboard; IT Admin aggregate and annotated reports |
| `tickets:ticket_list` | `/tickets/` | Permission-filtered list, search, facets, ordering and pagination |
| `tickets:ticket_create` | `/tickets/new/` | Employee/admin create form |
| `tickets:ticket_detail` | `/tickets/<int:pk>/` | Ticket, status, comments, permitted controls |
| `tickets:ticket_update` | `/tickets/<int:pk>/edit/` | Allowed field edits |
| `tickets:ticket_cancel` | `/tickets/<int:pk>/cancel/` | GET confirmation + POST safe-cancel |
| `tickets:ticket_assign` | `/tickets/<int:pk>/assign/` | Admin POST or validated form |
| `tickets:ticket_start` | `/tickets/<int:pk>/start/` | Technician/admin POST |
| `tickets:ticket_resolve` | `/tickets/<int:pk>/resolve/` | Technician/admin POST and required note |
| `tickets:ticket_comment` | `/tickets/<int:pk>/comment/` | Authenticated authorized POST |
| `tickets:category_list` | `/categories/` | Admin list, including ticket counts |
| `tickets:category_create` | `/categories/new/` | Admin create |
| `tickets:category_update` | `/categories/<int:pk>/edit/` | Admin edit |
| `tickets:category_delete` | `/categories/<int:pk>/delete/` | Admin confirm and POST, reject if referenced |

- Avoid a separate user/profile management frontend; demo accounts are seeded and Django Admin is available.
- Show appropriate navigation by role.
- Reuse generic form/list templates when it keeps code simpler.

## 7. ORM evidence — MUST be in rendered application features

### CRUD
- Ticket create/detail/update, safe cancellation through UI.
- Category create/detail-in-list/update/delete through UI (for nonreferenced category).
- Comments created/read through ticket detail.
- Test category PROTECT behavior and ticket cancellation persistence.

### Filtering and ordering
- `q` searches ticket title and description and optional stringified reference via exact numeric ID if supported; avoid complicated cross-type expressions.
- Dropdown filters `status`, `priority`, `category` (and `assigned_to` only for admins if time).
- `order` whitelist: newest (default), oldest, priority high-to-low (explicit `Case/When` or mapped sorting; NEVER alphabetic priority), updated-most-recent.
- Search across title/description via `Q()`; combine independent filters with AND.
- Preserve valid query params in pagination links; paginate at 10 items/page; show zero-match state.
- Relationship filtering: `Ticket.objects.filter(category__name=...)`, `Ticket.objects.filter(assigned_to__groups__name='Technician')` when actually useful, or `TicketComment.objects.filter(ticket__requester=request.user)` as appropriate. Avoid duplicates from M2M joins.

### Aggregation (whole-queryset)
- Admin dashboard: `Ticket.objects.aggregate(total=Count('id'), active=Count('id', filter=Q(status__in=ACTIVE_STATUSES)), resolved=Count('id', filter=Q(status='resolved')), cancelled=Count('id', filter=Q(status='cancelled')))` or equivalent reliable aggregation.
- Display exact counts and explain active definition.
- Required five-status breakdown using `.values('status').annotate(count=Count('id'))`, filling absent statuses with zero for display.

### Annotation (per-row)
- Category table: `Category.objects.annotate(open_ticket_count=Count('tickets', filter=Q(tickets__status__in=ACTIVE_STATUSES)))`; render `open_ticket_count` next to each category.
- Admin workload report: technician User queryset annotated with ticket count using the reverse `assigned_tickets` relation, optionally only active statuses; restrict to Technician group and use distinct where joins may multiply rows.
- Ensure 0-ticket categories/technicians appear with 0, and tested multi-row data gives correct counts.
- Do NOT claim an isolated Django shell example as rubric evidence; provide page and code reference in `docs/REQUIREMENTS_MATRIX.md`.
- Use `select_related('requester','assigned_to','category','department')` for list/detail; `prefetch_related('comments__author')` or appropriate queryset for comments if needed; avoid premature optimization.

## 8. Forms and validations

- Use `ModelForm` for Ticket and Category, and a specific CommentForm and ResolveForm; use an explicit AssignmentForm constrained to technician users.
- Required fields: nonempty trimmed title/description/comment; selected valid existing category/department; priority from choices.
- Do not expose requester, assigned_to, status, resolved_at in employee editable forms.
- Enforce assignment: valid existing user in Technician group only.
- Verify state transitions and object ownership on every POST even if buttons are hidden.
- Resolution requires a nonempty note; save resolution_note, resolved_at, status together in a transaction if appropriate.
- Friendly error messages and Django messages for successes; `get_object_or_404` for missing records; no unhandled exception page during routine user errors.
- Respect browser/mobile usability: form labels, focus, messages, confirmation pages, keyboard navigation.

## 8A. Final workflow contracts and edge-case behavior

Use one coherent mutation boundary (service functions or equivalent) so the same business rules govern every endpoint. Do not let an unrestricted generic update view bypass the lifecycle.

1. **Create:** only Employee and IT Admin; requester from authenticated session; status `new`; assignee null; no resolution; full server validation. Redirect to the created detail page with success message.
2. **Edit:** Employee only on *own* `new` and unassigned ticket; IT Admin on any nonterminal ticket. Only the five editable business fields; use whitelist in ModelForm. Return 403/404 for unauthorized users and standard field errors for invalid values.
3. **Assign:** IT Admin only; `new → assigned` on first assignment; may reassign `assigned` or `in_progress` while retaining status; always require a technician as target and never permit blank. No assignment action on terminal tickets.
4. **Start:** assigned technician or IT Admin; exactly `assigned → in_progress`; reject other states or unassigned tickets.
5. **Resolve:** assigned technician or IT Admin; exactly `in_progress → resolved`; resolution note must have meaningful non-whitespace text; save status, note and `resolved_at=timezone.now()` together; no empty note or second resolution.
6. **Cancel:** owner Employee only on own `new`; IT Admin on any nonterminal status. Confirmation GET + POST only for mutation. Keep ticket data, assignee (if any) and comment history for audit, status `cancelled`; no physical delete.
7. **Comment:** only authorized viewers on active tickets; author always authenticated session; no editing, no physical deletion. Reject whitespace-only bodies and comments on terminal tickets.
8. **Category admin:** IT Admin only; create/list/edit/delete unused categories via UI. If used by any Ticket, `PROTECT` prevents deletion; catch the condition and present a user-friendly message rather than HTTP 500. Category edits cannot violate uniqueness.
9. **Department setup:** manage via Django admin (not an additional custom UI); seed useful options; `PROTECT` prevents deleting departments referenced by tickets. Document this conscious scope boundary and show it in the Django admin or a setup demonstration if needed.
10. **Visibility:** Employee sees own tickets, Technician only tickets assigned to them, IT Admin all; base querysets for search, dashboard and detail actions must use those scopes. A forged URL or POST must never expose a ticket outside scope.
11. **Ordering:** explicit `Case/When` priority order high → medium → low; order whitelist only; use a deterministic second key (`-created_at` or `-id`) so pagination is stable. Invalid filter/order parameters fall back safely, not 500.
12. **Counters:** Category open count and Technician active-assigned count are **per-row annotations** using filtered `Count`; global totals use `aggregate`; zero-ticket categories and technicians return 0. Compare against fixed expected seed/test fixtures and avoid inflated join counts.
13. **Idempotent sample seed:** re-running does not duplicate role groups, demo users, departments, categories, tickets or comments. Identify seeded records with stable fixture identifiers and use `get_or_create`/careful `update_or_create`, never destructive resets of user data. Keep credentials for local demonstrations only; no real secrets in repository.
14. **Error responses:** use login redirect for anonymous users, consistent 403/404 for unauthorized or missing objects, actionable validation errors for invalid form data, and confirmation/success feedback for changes. Test GET and POST bypass attempts, not only link visibility.
15. **Fresh checkout:** installation must work from committed migrations with no existing `db.sqlite3`; the README shows exact tested commands and runtime versions. Do not fabricate screenshots, test outcomes or acceptance statuses.

### Locked page-level evidence

| Rubric capability | Application page | Evidence to verify |
|---|---|---|
| CRUD | `/tickets/new/`, `/tickets/<id>/`, `/tickets/<id>/edit/`, `/tickets/<id>/cancel/`; `/categories/` + category forms | Persist, edit, safe-cancel, create/edit/delete unused category; block deletion of used category |
| Filtering/ordering | `/tickets/` | Combined search, status/priority/category, priority ordering, pagination and empty state |
| Relationship query | `/tickets/` and ticket detail | Query tickets using `category__name` or assignee relations; detail loads requester/assignee/category/department/comments |
| Aggregate | `/` IT Admin dashboard | Total, active, resolved, cancelled counts from ORM `aggregate()` |
| Annotation | `/` IT Admin dashboard and `/categories/` | Category open counts and technician active-assigned counts via ORM `annotate()` |
| Validation and access | Create/edit/assign/resolve/comment/cancel routes | Reject invalid values, transitions, role bypasses, cross-user requests |
| Reporting usefulness | `/` | Admin sees backlog by category and workload by technician to prioritize staffing |
| Reproducibility | README + `seed_demo`, migrations/tests | New environment install, seed twice, known metrics, repeatable demo |

## 9. Required automated and manual tests

### Automated tests — prioritize these
1. Employee can create ticket and requester is set from session, not submitted POST.
2. Missing/blank title and description rejected.
3. Unauthorized anonymous access redirects to login.
4. Employee cannot view/edit someone else's ticket (GET and forged POST).
5. Employee cannot assign/resolve ticket with forged POST.
6. Admin cannot assign a non-technician.
7. Admin assigns technician; status becomes assigned.
8. Assigned technician starts ticket; wrong technician cannot.
9. Resolve without resolution note rejected; valid resolve sets timestamp and note.
10. Invalid transitions rejected (e.g., new → resolved, resolved → in_progress).
11. Employee cancels own NEW ticket; cannot cancel an in-progress ticket.
12. Category delete succeeds when unused, and is blocked if referenced.
13. Search, combined filters, ordering and empty results behave correctly.
14. Aggregation active count excludes resolved/cancelled.
15. Annotation per-category and per-technician works with multiple tickets and zero-ticket category.
16. Comment cannot be posted to an unauthorized ticket.
17. Model migrations fresh and `manage.py check` clean.

### Manual verification record format
`Scenario | Expected | Actual | PASS/FAIL | Notes`.
Include complete end-to-end demo, invalid values, no-results search, update and safe-delete dependencies, reporting metrics, access checks, viewport desktop/mobile, and fresh clone installation. Record failures honestly; no fabricated PASS outcomes.

## 10. Demo seed data

Implement an idempotent `python manage.py seed_demo` management command. Use fake people and organizational data only. Supply a demo password at runtime, validate it, and hash it using Django. Never hardcode or commit any password (including local demo passwords), secret key, token or populated database. Document usernames and password configuration instructions only. Repeated seeding must preserve existing passwords and user changes; reserved-ID collisions must fail safely.

Suggested sample distribution:
- Departments: Finance, Human Resources, Operations, Sales.
- Categories: Hardware, Software, Network, Accounts, plus an optional UNUSED category solely to demo protected vs allowed deletion.
- 2 Employees, 2 Technicians, 1 IT Admin (plus a superuser only if needed, separate from application role).
- Exactly 12 initial tickets: 3 new, 3 assigned, 2 in progress, 2 resolved and 2 cancelled; total 12, active 8. Active category counts Hardware 3, Software 2, Network 2, Accounts 1, unused category 0; active technician counts 3 and 2. Zero-workload technician and empty-dataset cases are also required test fixtures.
- Ticket samples: printer not responding, unable to connect to Wi-Fi, ERP login request, laptop overheating, VPN connection issue, slow workstation, password reset.
- Comments on multiple tickets, including a resolved ticket.
- Create deterministic or known counts so dashboard expectations can be asserted and demonstrated; test idempotency of seeding and ensure repeating seeding does not duplicate data.

## 11. UX/wireframes

**Base:** Responsive sidebar/top-nav; application title; login/out; role indicator; Django messages; mobile menu or stacked nav.

**Dashboard:** Four summary cards on admin view (all/active/resolved/cancelled), category workload table with `open_ticket_count`, technician workload table with `active_assigned_count`, newest ticket list. For employee/technician show only authorized relevant metrics. These should all be DB-backed.

**Ticket list:** Header + create button when permitted; search box; status/priority/category filters; order dropdown; ticket table/cards with ref/title/status/priority/category/requester/assignee/date; pagination with preserved filters; no-results message.

**Detail:** Ticket summary, timeline-like comments (simple list acceptable), permitted action controls, comment form, resolution panel if resolved.

**Forms:** Clear required markers, server-validation messages, cancel/back links, destructive confirmation. On mobile, horizontal tables can become stacked cards.

Store simple ASCII/Markdown wireframes in `docs/WIREFRAMES.md`; do not spend hours producing graphics before a working app.

## 12. Explicit grading map (100 points)

| Guide criterion | Marks | Application/deliverable evidence |
|---|---:|---|
| Problem and market potential | 10 | README audience/problem/benefits/adoption model; real-world demo narrative; explicitly distinguish market hypotheses from verified evidence |
| Core functionality | 20 | Employee creates → admin assigns → technician starts/comments/resolves → employee sees outcome; persisted data, validation, safe cancel and category CRUD |
| Database and ORM | 20 | `docs/ERD.md`; PK/FK cardinality/optionality; constraints/PROTECT; migrations; ticket CRUD; filtered ticket list; relationship filtering; dashboard `aggregate`; category and technician `annotate` |
| Django/Python implementation | 15 | Clean namespaced URLs, templates inheritance, ModelForms, small cohesive views/services, role/ownership checks, readable application structure |
| Interface and usability | 10 | Responsive HTML/CSS, accessible labels, navigation, empty states, errors, message feedback, cancel/delete confirmation |
| Verification and reproducibility | 10 | Meaningful tests, real manual acceptance log, `seed_demo`, fresh install/migration/run proof, sample data, no unresolved crash paths |
| Git and documentation | 5 | Meaningful incremental commits, README setup/version/features, ERD/wireframes/verification/demo documents, AI attribution |
| Demonstration and individual understanding | 10 | `docs/DEMO_SCRIPT.md`; show workflow, validation, live ORM reports and relational design; be able to trace URL → view → queryset → template and explain constraints |

**Source note:** The guide's exact requirements are on pp. 1–6; this table is the implementation mapping, not a copied rubric.

## 13. Deliverables and documentation definition of done

- `README.md`: description, audience, pain point, market hypothesis/adoption, feature list and roles, tech stack, exact Python/Django versions, prerequisites, install/venv/pip, env vars if used, migrate, seed, run, sample login identities, screenshots optional, testing commands, clear scope/limitations, future work, external resources & substantial AI/Codex assistance attribution.
- `docs/ERD.md`: Mermaid ER diagram or embedded source showing all entities, PK/FK, optionality/cardinality, deletion choices; MUST match actual migrated models.
- `docs/WIREFRAMES.md`: simple dashboard/list/form/detail design representations.
- `docs/REQUIREMENTS_MATRIX.md`: rubric capability → actual URL/UI behavior → code location → automated/manual evidence.
- `docs/ACCEPTANCE_TESTS.md`: scenarios, expected/actual, pass/fail, known issues; distinguish tests actually run from planned ones.
- `docs/DEMO_SCRIPT.md`: short role-switch demo with reproducible sample records, explain real reports and failure case.
- `requirements.txt`, `.gitignore`, committed migrations, static/templates, runnable seed command, tested clean setup.
- `git log` shows several meaningful milestones, not one massive autogenerated commit.

## 14. Execution plan and stop rules

### Day 1 — product
1. **Checkpoint A (~1h):** approved corrections, exact ERD, URL/access contracts, wireframes, progress record and safe Django scaffold. Validate foundation; commit and stop for review. No custom models or migrations yet.
2. **Checkpoint B (~2h):** models/constraints/migrations, role helpers, guarded admin and idempotent seed; validate database/provisioning/deletion rules; commit and stop for review.
3. **Checkpoint C (~4h):** complete role workflow with usable templates and focused authorization/state tests; demonstrate persisted end-to-end flow; commit and stop for review.
4. **Checkpoint D (~2h):** category CRUD, filters/order/pagination and all reports; verify known metrics and protected deletion; commit and stop for review.

### Day 2 — grading evidence and reliability
5. **Checkpoint E (~3h):** complete security/state/report tests; resolve integration defects; finish responsive/accessibility/error states; commit and stop for review.
6. **Checkpoint F (~2h):** finalize all documentation and real verification outcomes; commit and stop for review.
7. **Checkpoint G (~3h):** separate fresh checkout setup, migrations, seed twice, checks/tests, browser acceptance, student rehearsal and final submission/access check; commit and stop for review.
8. **Contingency (~2h):** repair mandatory blockers and repeat impacted checks. Approximately 20 focused hours total; optional polish only after readiness evidence passes.

**Cut scope rather than quality:** If behind schedule, remove only explicitly optional refinements, such as charts or decorative UI, after seeking approval. Do NOT remove any mandatory implemented feature, required category CRUD, core persisted journey, at least one annotated report and one aggregate report, relationship queries, validation, access control, documentation, or verification.

## 15. Codex operating contract

**Do not code until the user explicitly starts implementation.** When implementation begins:
1. Read this entire specification and inspect the existing repository first; do not overwrite user work.
2. Report installed Python/Django and repo status; propose ordered checkpoints with estimated time.
3. Implement only the requested checkpoint, then stop for review. Each checkpoint must deliver final, integrated versions of its files; no knowingly throwaway first drafts.
4. For every checkpoint, explain what files changed, why, how to run, which tests ran and outcomes, and any known limitations.
5. Do not invent test success or claim a fresh install without running it.
6. Confirm actual behavior via tests and, where feasible, a real end-to-end manual walkthrough.
7. Keep code reasonably simple for a student to explain. No architecture astronautics, unnecessary JS frameworks, or unrequested integrations.
8. Never print or commit secrets; use dummy account data and safe configuration.
9. Commit coherent milestones only after validation; do not force-push or overwrite main without permission.
10. If the specification conflicts with framework constraints, explain a minimal fix and ask before material scope changes. Bug fixes and ordinary code corrections may proceed within the authorized checkpoint.
11. Before creating or modifying a file, inspect the complete baseline, other dependent files and contracts. Avoid "write it now, change it later" instructions caused by foreseeable omissions.
12. Never optimize for fewer lines or faster completion at the expense of rubric coverage. Preserve time for tests, documentation, the real demonstration, and student explanation.
13. Do not claim a guaranteed score. Report observable evidence and any unresolved risks honestly.

### Suggested next Codex prompt (AFTER Checkpoint B review)

> Read the root `HELPDESK_PRO_CODEX_SPEC_FINAL.md` and `helpdesk-pro/docs/DESIGN.md` fully and inspect the repository. Checkpoint B is approved. Work inside `helpdesk-pro/` and implement Checkpoint C only: application login/logout and role-scoped dashboard/list/detail; create/edit/cancel/assign/start/resolve/comment forms, service functions and views; final usable templates and focused authorization/lifecycle tests. Reuse the verified models, role helpers and sample data. Show actual validation results and stop for review before Checkpoint D. Do not add features outside the approved scope.

## 15A. Final-first development and grade-maximization rules

**Avoid predictable rewrites:** Before any implementation phase, Codex must check the entire document, fields, forms, namespaced URLs, permissions, lifecycle, seed fixtures, HTML requirements, test cases and assessment matrix for dependency conflicts. Implement the intended final code for all files in that phase; do not propose partial scaffolds or TODO implementations that will require a planned rewrite. Phase boundaries are for safe review and validation, not for reinventing the architecture.

**Maintain a live evidence matrix:** Track requirement → code path → visible URL → reproducible test/manual scenario → actual PASS/FAIL. New work is accepted only when the directly impacted acceptance checks pass. Run appropriate regressions after corrections.

**No guarantee of 100/100:** The goal is maximal rubric coverage and a presentation the student understands. A grade is awarded by the instructor; never say an implementation has "full marks" without grading evidence.

**Priority under the timebox:** Finish and verify every mandatory capability, then documentation and student rehearsal, then optional aesthetic refinements. Where estimates threaten the deadline, report risks and ask the user about tradeoffs instead of silently weakening an approved requirement.

## 16. Final acceptance criteria

The project is ready only when all are true:
- [ ] All eight steps of the complete role-switch demo journey in section 1 work in browser with DB persistence.
- [ ] Ticket and category interfaces demonstrate CRUD and safe deletion/cancellation behavior.
- [ ] Filters/order/pagination correctly preserve scope, with no leaks of other users' tickets.
- [ ] Dashboard shows tested aggregate **and** annotated category counts.
- [ ] FK constraints, validation, permission checks, and status transitions are covered by tests/manual checks.
- [ ] README setup works from a new environment; migrations and sample data work reproducibly.
- [ ] Mobile and desktop views usable; empty/error/confirmation states functional.
- [ ] ERD, wireframes, verification table, demo script, Git commits, and AI credit present.
- [ ] Student can personally explain one request, key FK/deletion choice, business validation and ORM math.
- [ ] `docs/REQUIREMENTS_MATRIX.md` maps every item on the 100-mark rubric to visible evidence and a verified scenario.
- [ ] No known mandatory feature is represented only by a shell transcript, placeholder, unrun test, or unverified claim.
