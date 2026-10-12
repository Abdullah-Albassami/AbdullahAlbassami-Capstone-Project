# HelpDesk Pro wireframes and user journey

Approved design for the implemented A–E interface. These diagrams remain design evidence; E's separate actual Chrome screenshots/results cover 1280px/375px layouts, basic keyboard and computed contrast. Human/device/accessibility checks remain pending. HD-10013's C lifecycle remains user-observed evidence.

## Shared layout

```text
┌────────────────────────────────────────────────────────────┐
│ HelpDesk Pro   Dashboard  Tickets  [Categories/admin only]   │
│                                     User · Role  [Sign out]│
├────────────────────────────────────────────────────────────┤
│ Success/error feedback                                     │
│ Page heading                         Permitted main action  │
│ Page content                                               │
└────────────────────────────────────────────────────────────┘
```

Light neutral background, white panels, dark text and blue primary actions. Text labels accompany statuses and priorities; color alone never communicates meaning. Navigation wraps/stack on narrow screens without JavaScript. Logout is a POST form.

## Admin dashboard

```text
Support overview                              [Create ticket]
[Total: 12]  [Active: 8]  [Resolved: 2]  [Cancelled: 2]
Status breakdown: New 3 · Assigned 3 · In Progress 2 · ...

Category backlog                 Technician assignments
Hardware                  3      technician1               3
Software                  2      technician2               2
Network                   2      (zero-count rows retained)
Accounts                  1
Unused                    0

Recent tickets: reference · title · status · assignee
```

Explain that active means New/Assigned/In Progress. Category totals guide backlog prioritization; technician totals support assignment decisions. Employee view shows own counts/recent tickets and Create; technician view shows their assigned workload and work queue. Neither exposes system-wide totals.

## Ticket list

```text
My Tickets / Assigned to Me / All Tickets       [Create*]
Search [________________]  Status [All v]  Priority [All v]
Category [All v]  Order [Newest v]              [Filter][Clear]

Reference | Issue | Status | Priority | Category | Requester | Assignee
HD-10001  | ...   | New    | High     | Hardware | Unassigned
...
Previous                     Page 1 of 2                 Next
```

*Create appears only for Employee/IT Admin. Required fields and form controls have associated labels. Valid filter parameters survive page changes. No matches shows a useful explanation and Clear filters; an empty initial queue shows the role-appropriate next action. Mobile retains every necessary value in cards or an explicitly labeled horizontally scrollable table.

## Detail and actions

```text
HD-10001 — Printer unavailable           Status · Priority
Requester · Requesting department · Category · Created/Updated
Description (escaped multiline text)

Permitted controls only:
[Edit] [Cancel → confirmation]
Admin: [Technician v] [Assign/reassign]
Assignee/admin: [Start] or Resolution note [____] [Resolve]

Discussion: author · timestamp · body
Comment [______________________________________] [Post comment]
Resolved outcome: resolution note and resolved timestamp
```

Controls reflect the server action matrix; hiding controls never replaces authorization. Terminal tickets show the outcome/thread read-only. Labels describe reassignment and cancellation consequences. Invalid action forms remain bound with readable errors.

## Create/edit/category forms and confirmations

```text
New ticket
Title *                  [_________________________]
Description *            [_________________________]
Category *               [Choose v]
Requesting department *  [Choose v]
Priority *               [Medium v]
Field/non-field errors   [Save ticket] [Back]

Cancel HD-10001?
This retains the ticket and discussion and ends further work.
[Keep ticket] [Confirm cancellation]

Delete unused category?
This removes the category. Referenced categories cannot be deleted.
[Keep category] [Confirm deletion]
```

Category list shows name, description and annotated active ticket count, with create/edit/delete controls. Login uses Django authentication with labeled username/password and generic invalid-credential feedback. Errors/missing records offer safe navigation, never tracebacks for expected requests.

Category detail shows full description, active count and a link to tickets filtered by its category. Delete confirmation explains permanent removal and the existing-ticket reference count; a protected POST returns an error on that page without deletion. Empty report rows show zero; completely empty reports explain the next setup action. Invalid filters retain other valid selections and show field feedback. Page values that are nonnumeric/nonpositive/repeated select first; positive out-of-range selects last.

## Realistic end-to-end journey

Employee signs in → submits issue → sees saved New ticket → IT Admin assigns eligible technician → technician sees assignment, starts work, adds comment and resolves with note → employee reads final outcome → admin explains live counts. Demonstrate missing input and denied cross-user access. Cancellation and unused/used category deletion are separate acceptance scenarios.

## Accessibility and manual checks

Semantic header/nav/main/footer; skip link; keyboard focus; meaningful link/action labels; labels, help text and associated error descriptions; polite message announcements; table headers/captions; no external fonts or required decorative images. Content images, if introduced, need meaningful alt text. Verify desktop (1280px), mobile (375px), keyboard-only operation and readable form errors in a real browser during later checkpoints.

E executed 34 page/viewport audits in real headless Chrome and basic skip-link/Enter, technician arrow selection and table ArrowRight scrolling. Valid maximum-length category/ticket confirmation text wraps; table cells retain readable widths inside local scroll regions with a visible mobile hint. Human complete keyboard operation, 200% zoom, physical devices/other browsers and screen-reader evaluation remain unexecuted; follow MANUAL_BROWSER_CHECKS. This is not accessibility certification.
