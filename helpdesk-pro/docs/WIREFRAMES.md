# Interface wireframes and user journeys

These simple layouts show the intended screens; the real interface uses Django templates and responsive CSS.

## Employee

```text
Dashboard → Submit ticket → Ticket details → Comments / status
               ↓
        Title, description,
        category, department,
        priority
```

## Technician

```text
Assigned tickets → Ticket details → Start progress → Add resolution
```

## IT administrator

```text
Dashboard
 ├─ Ticket queue → Assign / reassign / review
 ├─ Category management → Create / edit / delete unused categories
 └─ Reports → Status totals / category backlog / technician workload
```

## Shared layout

```text
[HelpDesk Pro] [Dashboard] [Tickets] [Categories when authorized] [Sign out]
[Feedback / validation messages]
[Page heading]
[Filters or form / list / ticket detail]
```

Forms include labels and validation feedback. On smaller screens, navigation adapts and wide tables can scroll horizontally.
