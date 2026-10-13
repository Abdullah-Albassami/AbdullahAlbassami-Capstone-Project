# System design

HelpDesk Pro is a Django application for internal IT support. It uses one `tickets` app, SQLite, Django templates and local CSS.

## Roles and workflow

| Role | Access |
|---|---|
| Employee | Create requests; view own tickets; edit or cancel own unassigned New tickets; comment while active |
| Technician | View assigned tickets; start work, comment and resolve |
| IT Admin | View all tickets; assign/reassign, manage categories and view reports |

Tickets follow **New → Assigned → In Progress → Resolved**, or a permitted **Cancelled** path. Resolved and cancelled tickets remain available for reference but cannot be edited through supported workflows.

## Database

The four custom models are **Department**, **Category**, **Ticket** and **TicketComment**, related to Django's built-in users. See the [ERD](ERD.md) for keys, cardinalities and deletion rules.

Referenced departments, categories and users are protected from deletion. Comments belong to tickets. Database constraints validate allowed states and priorities; forms and services enforce meaningful input and role-specific transitions.

## Architecture

- [URLs](../tickets/urls.py) route named pages to [views](../tickets/views.py).
- [Forms](../tickets/forms.py) validate submitted data.
- [Services](../tickets/services.py) apply business rules.
- [Permissions](../tickets/permissions.py) scope roles and records.
- [Queries](../tickets/queries.py) provide search, pagination and reports.
- [Templates](../templates/) render the interface.

The system includes server-side permission checks, CSRF protection and controlled record updates. Demo records are fictional.


## Development priorities

The project was organized around the following priorities:

| Priority | Work | Result |
|---|---|---|
| 1 — Essential | Database models, migrations, roles and safe sample data | Complete |
| 1 — Essential | Submit, assign, track, resolve and cancel support tickets with validation | Complete |
| 1 — Essential | Server-side access control and related ticket comments | Complete |
| 2 — Important | Category management, search, filtering, ordering and pagination | Complete |
| 2 — Important | Ticket summaries and category/technician workload reports | Complete |
| 2 — Important | Responsive interface, testing, documentation and reproducible setup | Complete |
| 3 — Future | Email notifications, SLA monitoring, integrations and hosted deployment | Outside capstone scope |

This list summarizes development priorities; the Git commit history records the implementation sequence.

## Limits

This is a working capstone prototype, not a production-deployed ITSM service. Email notifications, SLA tracking, API integrations, hosted operations and full assignment-history auditing are outside the delivered scope.
