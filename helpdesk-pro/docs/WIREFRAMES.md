# HelpDesk Pro wireframes and user journey

Final schematic wireframes reviewed against the implemented templates in F; the unchanged interface passed G's fresh-clone Chrome checks. They explain layout rather than reproducing screenshots. [E's actual Chrome results](evidence/checkpoint-e/results.json) cover 1280px/375px layouts, basic keyboard and selected computed contrast. Human/device/accessibility checks remain pending. HD-10013's C lifecycle remains user-observed evidence.

## Shared layout

```text
┌────────────────────────────────────────────────────────────┐
│ HelpDesk Pro   Dashboard  Tickets  [Categories/admin only]   │
│ [Submit ticket*] [Organization setup**]          [Sign out] │
├────────────────────────────────────────────────────────────┤
│ Success/error feedback                                     │
│ Page heading                         Permitted main action  │
│ Page content                                               │
└────────────────────────────────────────────────────────────┘
```

Light neutral background, white panels, dark text and blue primary actions. Role/name are presented in page headings rather than a shared header badge. Submit ticket appears for Employee/IT Admin; Organization setup appears for staff IT Admin. Navigation wraps on narrow screens without JavaScript. Logout is a POST form. Source: [base.html](../templates/base.html), [style.css](../static/css/style.css).

## Admin dashboard

```text
IT Admin workspace
Welcome, Rana Demo                            [Submit ticket]
[Total: 12]  [Active: 8]  [Resolved: 2]  [Cancelled: 2]
Status breakdown: New 3 · Assigned 3 · In Progress 2 · ...

Category backlog                 Technician workload
Hardware                  3      Lina Demo (technician1)     3
Software                  2      Sami Demo (technician2)     2
Network                   2      (zero-count rows retained)
Accounts                  1
Unused                    0

Recent tickets: shared ticket table (up to five)
```

The names/usernames in the technician report appear on separate lines. Numbers here describe the pristine 12-ticket seed, not the working 13-ticket data. Employee/Technician dashboards use the same cards, five-status breakdown and recent table, scoped to own/assigned tickets; Employee has Submit ticket. Organization reports appear only for IT Admin. Source: [dashboard.html](../templates/tickets/dashboard.html). Actual [desktop](evidence/checkpoint-e/dashboard-desktop.png) and [mobile](evidence/checkpoint-e/dashboard-mobile.png) screenshots show this fixture layout.

## Ticket list

```text
My tickets / Assigned tickets / All tickets     [Submit ticket*]
Search [________________]  Status [All v]  Priority [All v]
Category [All v]  Order [Newest v]     [Apply filters][Clear filters]

Ticket (reference/title) | Status | Priority | Category / department
Requester | Assigned to | Created (date/time)
HD-10001 / ... | New | High | Hardware / ... | Nora Demo
Awaiting assignment | ...
...
Previous                     Page 1 of 2                 Next
```

Submit appears only for Employee/IT Admin. Valid filter parameters survive page changes. No matches shows Clear filters; an empty initial queue explains the next action. Mobile uses the same labeled, focusable horizontally scrollable table with a visible hint. Source: [ticket_list.html](../templates/tickets/ticket_list.html), [ticket table](../templates/tickets/includes/ticket_table.html).

## Detail and actions

```text
HD-10001 — Printer unavailable           Status · Priority
Requester · Requesting department · Category · Created/Updated
Description (escaped multiline text)

Permitted controls only:
[Edit details] [Cancel ticket → confirmation]
Admin: [Lina Demo (technician1) v] [Assign technician / Save assignment]
Assignee/admin: [Start progress] or note [____] [Resolve ticket]

Discussion: author · timestamp · body
Comment [______________________________________] [Add comment]
Resolved outcome: resolution note and resolved timestamp
```

Controls reflect the server action matrix; hiding controls never replaces authorization. Terminal tickets show the outcome/thread read-only. Invalid action forms remain bound with readable errors. Source: [ticket_detail.html](../templates/tickets/ticket_detail.html).

## Create/edit/category forms and confirmations

```text
Submit a ticket / Edit ticket
Title *                  [_________________________]
Description *            [_________________________]
Category *               [Choose v]
Requesting department *  [Choose v]
Priority *               [Medium v]
Field/non-field errors   [Submit ticket / Save changes]
                         [Return without saving]

Cancel this ticket? (HD-10001 and issue title)
Retains ticket, assignee and discussion; permanently ends work.
[Confirm cancellation] [Keep ticket active]

Delete unused category?
This removes the category. Referenced categories cannot be deleted.
[Confirm deletion] [Keep category]
```

Category list shows name, description and annotated active ticket count, with create/edit/delete controls. Login uses Django authentication with labeled username/password and generic invalid-credential feedback. Errors/missing records offer safe navigation, never tracebacks for expected requests.

```text
Categories                                   [Create category]
Name/link | Description | Active tickets | Actions: Edit / Delete

Category detail: name · full description · active count
[View tickets] [Edit category] [Delete category]

Create/Edit category: Name * [____] Description [____]
[Create category / Save changes] [Return without saving]

Sign in: Username [____] Password [____] [Sign in]
Error page: status · explanation · navigation back to work
```

Sources: [category list](../templates/tickets/category_list.html), [category detail](../templates/tickets/category_detail.html), [category form](../templates/tickets/category_form.html), [category confirmation](../templates/tickets/category_confirm_delete.html), [ticket form](../templates/tickets/ticket_form.html), [ticket cancellation](../templates/tickets/ticket_cancel_confirm.html), [login](../templates/registration/login.html), [errors](../templates/errors/error.html).

Category detail shows full description, active count and a link to tickets filtered by its category. Delete confirmation explains permanent removal and the existing-ticket reference count; a protected POST returns an error on that page without deletion. Empty report rows show zero; completely empty reports explain the next setup action. Invalid filters retain other valid selections and show field feedback. Page values that are nonnumeric/nonpositive/repeated select first; positive out-of-range selects last.

## Realistic end-to-end journey

Employee signs in → submits issue → sees saved New ticket → IT Admin assigns eligible technician → technician sees assignment, starts work, adds comment and resolves with note → employee reads final outcome → admin explains live counts. Demonstrate missing input and denied cross-user access. Cancellation and unused/used category deletion are separate acceptance scenarios.

## Accessibility and manual checks

Semantic header/nav/main/footer; skip link; keyboard focus; meaningful link/action labels; labels, help text and associated error descriptions; polite message announcements; table headers/captions; no external fonts or required decorative images. Content images, if introduced, need meaningful alt text. Verify desktop (1280px), mobile (375px), keyboard-only operation and readable form errors in a real browser during later checkpoints.

E executed 34 page/viewport audits in real headless Chrome and basic skip-link/Enter, technician arrow selection and table ArrowRight scrolling. Valid maximum-length category/ticket confirmation text wraps; table cells retain readable widths inside local scroll regions with a visible mobile hint. Human complete keyboard operation, 200% zoom, physical devices/other browsers and screen-reader evaluation remain unexecuted; follow MANUAL_BROWSER_CHECKS. This is not accessibility certification.

G repeated all 39 Chrome checks from a genuinely new clone/environment; [latest results](evidence/checkpoint-g/results.json), [desktop](evidence/checkpoint-g/dashboard-desktop.png) and [mobile](evidence/checkpoint-g/dashboard-mobile.png) show the same implemented layout. These are automated fixed-viewport captures, not a student/physical-device/zoom/screen-reader acceptance claim.
