# HelpDesk Pro

*IT Support Ticket Management System — Django Capstone Project*

## 1. Introduction

HelpDesk Pro is a web application that helps organizations manage internal IT support requests. Instead of relying solely on disconnected emails, phone calls or messages, employees can create tickets that are tracked through assignment, progress and resolution.

The target audience is **small and medium-sized businesses** with a small internal IT team.

## 2. The problem

When support requests are handled informally, it can be difficult to identify outstanding issues, determine who is responsible and review previous resolutions. An organized ticket workflow gives both employees and IT staff a consistent record of requests.

## 3. The solution

HelpDesk Pro supports three roles:

| Role | Main responsibilities |
|---|---|
| Employee | Submit requests, follow own tickets and add comments |
| IT Admin | Prioritize, categorize, assign or reassign tickets, and review reports |
| Technician | Handle assigned tickets, update progress and record resolutions |

Tickets move through **New → Assigned → In Progress → Resolved**. Authorized users can also cancel tickets without deleting their history. The application includes searching, filtering, pagination and category management.

## 4. Validation and permissions

Django forms validate required fields and reject invalid input. Permissions are enforced by the backend, not just the interface. Employees can see only their own tickets; technicians see their assignments; IT Admin has broader access. Resolved and cancelled tickets remain read-only.

For example, a ticket cannot be resolved with an empty resolution note, and an employee cannot edit another employee's request.

## 5. Database and technical implementation

The application uses **Python, Django and SQLite**, with server-rendered HTML templates and responsive CSS.

Four application models—**Department**, **Category**, **Ticket** and **TicketComment**—connect to Django's built-in User and Group models. Foreign keys preserve relationships, while validation and database constraints protect data integrity.

The request flow is straightforward: **URL → View → Form/Service → Django ORM → Database → Template**.

The [ERD](ERD.md) shows the entities, keys and relationships.

## 6. Reporting

The IT Admin dashboard uses Django ORM queries to show:

- Total, active, resolved and cancelled tickets.
- Active tickets by category.
- Active assignments per technician.

**`aggregate()`** calculates overall totals; **`annotate()`** adds counts to individual categories and technicians. Reports reflect stored data rather than fixed example numbers.

## 7. Testing

The final independent verification passed **149 Django tests, 39 Chrome browser checks and 14 HTTP checks**, including a fresh installation and repeatable demo-data setup.

Manual testing also covered the ticket lifecycle, validation, search, pagination, category management and reporting. The exact observed scope and outstanding checks are recorded in [Acceptance Tests](ACCEPTANCE_TESTS.md).

## 8. Market potential

HelpDesk Pro is intended for SMBs with straightforward internal IT support needs. Its proposed advantage is a focused workflow that could be adapted to organization-specific requirements.

It is **not** claimed to be cheaper, more secure or more capable than established platforms such as ServiceNow or Jira Service Management. Commercial adoption would require customer validation, production security, backups, maintenance and cost analysis. See the [market assessment](MARKET_POTENTIAL.md).

## 9. Limitations and future improvements

This capstone is a functional prototype. Future development could include email notifications, SLA monitoring, integrations and production deployment safeguards. A small organizational pilot would help determine which improvements users actually need.

## Conclusion

HelpDesk Pro brings together Django development, relational database design, role-based permissions, CRUD workflows, form validation and ORM reporting in a working IT support application.

**Source repository:** [HelpDesk Pro on GitHub](https://github.com/Abdullah-Albassami/AbdullahAlbassami-Capstone-Project)
