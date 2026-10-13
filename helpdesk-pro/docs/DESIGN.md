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

## Limits

This is a working capstone prototype, not a production-deployed ITSM service. Email notifications, SLA tracking, API integrations, hosted operations and full assignment-history auditing are outside the delivered scope.
