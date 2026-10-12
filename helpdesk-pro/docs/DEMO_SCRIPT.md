# Demonstration and individual technical discussion

Prepared in F; **not an executed rehearsal**. Follow the [official guide](../../CapstoneProjectGuide.pdf), p.5, in the six-step order below. Instructor duration/slot remain unconfirmed; adjust pacing after confirmation, preserving order. G automated fresh setup/tests/server/browser checks passed; remaining human acceptance and the student's M14 rehearsal are still open. Use the exact submitted revision, fictional data and private credentials; do not expose passwords, keys or session tokens in the presentation.

## Preparation before the presentation

Follow the [submission checklist](SUBMISSION_CHECKLIST.md). Start the server using [README](../README.md) commands only after private configuration is set. Have employee1, technician1 and itadmin credentials ready privately; use separate browser profiles or the application's POST Sign out between roles. Keep the ERD, queries.py, services.py and acceptance record available for discussion.

Record the actual starting dashboard counts and ticket reference created during rehearsal. The pristine seed has **12/8/2/2** total/active/resolved/cancelled; the preserved working data, including already-resolved HD-10013, has **13/8/3/2** at F. Re-seeding preserves changes/passwords and does not reset counts. Never reset the working database to obtain the pristine figures. G verified a separate disposable fresh setup; it did not reset or replace the working database.

HD-10013's user-reported UC01–UC07 cover create/comment/assignment/start/resolve and employee dashboard Resolved. Its final employee detail/thread/controls remain unreported. It is already terminal: read it without changes; create a different fictional request for a live transition demonstration.

## 1. Target audience, problem and supporting evidence

Say: “HelpDesk Pro serves employees and a small IT team. Requests spread across email or spreadsheets can make ownership and unresolved work hard to follow. This application gives each request a persisted record, owner, controlled status and discussion.”

Separate evidence from assumptions: the working persisted workflows, tests and user-observed HD-10013 establish technical feasibility. There is no documented market study, measured time saving, paying customer or validated demand. Add an authentic personal/user observation only if the student can substantiate it; do not invent one. Explain why this scope fits an individual Django capstone.

## 2. Product value and complete ticket workflow

1. As employee1, use **Submit ticket** at `/tickets/new/`. Example: “Finance printer unavailable”, meaningful impact description, Hardware, Finance, High. Save and record the new reference. Show New status, requester and saved related fields. Edit the description while still New; add a comment if useful.
2. Sign out via the page form; sign in as itadmin. Open All tickets and the new reference. Select **Lina Demo (technician1)** and assign. Show Assigned and technician ownership.
3. Sign out/in as technician1. Open Assigned tickets, find that reference, start work, add a fictional troubleshooting comment and resolve with a meaningful outcome note. Show In progress before resolving and Resolved afterward.
4. Sign out/in as employee1. Open the final detail: retained resolution note/date/discussion, no edit/cancel/assignment/start/resolve/comment controls. Refresh to show persisted data.

Explain the value: clear ownership, consistent state and visible discussion. This is the complete primary journey; Category CRUD and cancellation are also implemented and must have acceptance evidence, even if presentation time does not permit every action.

## 3. Server validation or rejected action

As employee1, open Submit ticket, choose valid related fields and enter **spaces only** for title/description. Submit; show bound server-side errors and that no ticket was saved. Spaces bypass simple browser required-field checks and exercise server validation. Return without saving.

If time permits, employee2's direct URL to employee1's demonstration ticket returns safe 404; opening a POST-only start URL with GET returns helpful 405. Do not represent clicking a forbidden GET as proof of a forged POST: the automated suite supplies separate HTTP-attack evidence.

## 4. Aggregation and annotation reporting

As itadmin, show `/` dashboard: Total, Active, Resolved, Cancelled and all five status counts. Active = New + Assigned + In progress. Explain `queries.ticket_summary()` uses **aggregate** to return one set of queryset totals, scoped to the actor.

Show Category backlog and Technician workload. `category_backlog()` and `technician_workload()` use **annotate** to add an active-ticket count to each category/eligible technician. Hardware/Software/Network/Accounts/Unused are **3/2/2/1/0** in the original seed; technician1/technician2 active assignments are **3/2**. Unused remains visible with zero. Zero-workload technician and completely empty datasets are covered by ReportingTests; do not claim the pristine UI contains a third technician.

For the single new journey above, total and resolved each increase by one after completion; active/category/technician active counts return to their prior baseline. For example, **13/8/3/2 → 14/8/4/2** is the expected change if no other actions occur, not a recorded F result. During assignment, that category/technician count temporarily rises. Explain why active category counts sum to 8 while technician workload sums to 5 in the pristine data: three New requests are unassigned. Use actual current values if other checks have changed data.

Category backlog helps prioritize issue areas; workload helps choose an assignee and measures assignments rather than real-time availability. Separate queries/filtered distinct Count avoid multiplied counts from several related comments/groups. Show `/categories/` and the related View tickets link if useful.

## 5. Relationships and an important technical decision

Show the [ERD](ERD.md): each Ticket has one Category, one requesting Department and one requester; optional one assignee; zero or more comments, each with one author. Built-in User–Group membership supplies roles; no profile/custom membership model is needed. Requesting Department belongs to the issue, so it is not copied from a user profile.

Explain **PROTECT** for category/department/requester/assignee/comment author: referenced parents cannot be deleted, including historical tickets. **CASCADE** applies to comments if a ticket is physically removed through privileged maintenance; the application/admin prohibit ticket deletion. Cancellation preserves the ticket, assignee and thread while making it terminal.

Choose one key decision: the shared atomic workflow service re-fetches current scope/state and authorizes the actor before validating/saving. Views bind explicit forms; client fields cannot choose requester/author/status. Database checks add allowed-value/state protection; they cannot implement actor or transition-history authorization. SQLite transactions are used, without claiming row locking or enterprise concurrency guarantees.

## 6. Market potential, limitations and next improvement

Describe a realistic internal adoption proposal: one IT team provisions roles/departments/categories, pilots requests and reviews whether ownership/backlog visibility helps before wider use. Compared with email/spreadsheets, the product integrates assignment, controlled outcomes, discussion and reports. Benefits remain hypotheses until user feedback or measurement; no commercial launch is required by the guide.

State delivered limits: local SQLite capstone, no deployment/notifications/uploads/API/integrations, retained outcomes rather than a complete event audit log. G passed automated full fresh setup and server/browser checks. Remaining human acceptance/accessibility, instructor access and student rehearsal remain open until actually confirmed. A next practical improvement after feedback could be tested email notifications; it is outside the delivered scope.

## Request trace to explain personally

**Create POST:** [tickets/urls.py](../tickets/urls.py) `tickets:ticket_create` (`/tickets/new/`) → [views.py](../tickets/views.py) `application_view` login/current-role/method boundary and `ticket_create` → [forms.py](../tickets/forms.py) `TicketForm` validates its five allowed fields → [services.py](../tickets/services.py) `create_ticket` requires Employee/IT Admin, derives requester from actor, calls `apply_business_fields` and `save_validated` → [models.py](../tickets/models.py) `Ticket.full_clean()` plus database constraints, then INSERT → redirect to `tickets:ticket_detail` → fresh scoped `get_visible_ticket` SELECT/related retrieval → [ticket_detail.html](../templates/tickets/ticket_detail.html), inherited [base.html](../templates/base.html) and permission-controlled forms. Invalid input renders [ticket_form.html](../templates/tickets/ticket_form.html) with errors and no INSERT.

**Filtered GET:** `/tickets/?q=printer&category=1201&order=priority` → `tickets:ticket_list` → `views.ticket_list` → [queries.py](../tickets/queries.py) `ticket_list_page`: authorized `visible_tickets`, validated parameters, Q title OR description, category__name relation, Case priority rank, stable order and ten/page → [ticket_list.html](../templates/tickets/ticket_list.html) and shared [ticket table](../templates/tickets/includes/ticket_table.html). User scope is applied before searching/counting/paging.

## Likely instructor questions

| Question | Concise answer with implementation evidence |
| --- | --- |
| Where is CRUD? Why cancel instead of delete? | Ticket create/detail/edit/cancel through services and forms; Category full create/list/detail/edit/delete. Cancellation is safe retirement retaining dependencies; terminal records are read-only. `test_cancellation_preserves_assignment_thread_and_ticket` and CategoryTests verify it. |
| Which relationships and deletion behaviors matter? | Six custom FKs: five PROTECT, TicketComment.ticket CASCADE. A ticket assignee is nullable; all other FKs required. PROTECT keeps referenced historical data. `test_protected_deletion_all_five_parent_references` and schema test in ModelTests cover choices. |
| How do constraints differ from validation? | Four DB checks enforce status, priority, assignment/state and resolution pairing even without full_clean. Trim/meaningful text and actor/current-state rules require model/services. save alone does not invoke full_clean; supported services explicitly do. |
| How are authentication and authorization enforced? | Django authenticates/hashes/sessions; shared helpers read current persisted roles/flags. Employee own, Technician assigned, IT Admin all; no/conflicting role fails closed. is_staff alone grants no app role. Service authorization is repeated after state retrieval, and CSRF/POST protect mutations. |
| What prevents forged identity/terminal changes or invalid technicians? | Five business fields only; session requester/author; server status/timestamps. Active single-role non-superuser technicians only; target/state rechecked in services. Terminal UI/services/model validation and read-only admin prevent supported edits. Account guards require reassignment before ineligibility. |
| What are Q objects and relationship queries used for? | Q title OR description search, AND status/priority/category. `category__name` traverses a FK; select_related retrieves requester/assignee/category/department and comment authors. Ordering is whitelisted with explicit High→Medium→Low ranking and stable tie-breakers. |
| Aggregate versus annotate? How are counts correct? | Aggregate returns one scoped summary; annotate adds per-row counts. Active is three states; zero rows retained. Separate report queries/filtered distinct counts avoid join inflation. ReportingTests verify seed totals, zero/empty/multiple groups/comments and workflow changes. |
| How was it tested and reproduced? | G: 149 Django methods in a genuinely new clone/environment; seed twice identical; 39 Chrome checks on isolated normal-hasher/CSRF fixtures and 14 live HTTP/server checks. User UC01–UC07 separate; M01 partial, M02–M12/M14 human checks unrun, M13 automated setup PASS/human repeat unrun. README pins/config/migrations/seed match the executed fresh setup. |
| What assistance was used and what can the student explain? | README acknowledges significant Codex assistance and official Django/CDP/W3C resources. The student must review/adapt/understand the actual source and demonstrate these traces/calculations personally; generated preparation does not prove understanding. |

Use [MANUAL_BROWSER_CHECKS](MANUAL_BROWSER_CHECKS.md) for remaining acceptance actions and [SUBMISSION_CHECKLIST](SUBMISSION_CHECKLIST.md) for final revision/access. M14 remains **NOT RUN** until the student actually rehearses, records the reference/baseline/duration/outcome and can answer the questions above.
