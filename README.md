# HelpDesk Pro

**Internal IT support ticket management for small and medium-sized businesses**

## Overview

IT support requests are often scattered across emails, messages, and informal conversations, making it difficult to track ownership, progress, and resolution. **HelpDesk Pro** brings those requests into one system where employees submit tickets, administrators organize and assign them, and technicians manage their work.

The application is designed for businesses that need a straightforward internal help desk without a complex IT service-management platform.

## Features

- **Role-based access:** Employee, Technician, and IT Admin accounts, with permissions enforced per ticket.
- **Ticket management:** Submit, edit, assign, reassign, comment, start work, resolve, or cancel requests according to role and status.
- **Search and organization:** Categories, filtering, sorting, and pagination.
- **Reporting:** Ticket status summaries, category backlog, and technician workload using Django ORM aggregation and annotations.
- **Validation and usability:** Server-side validation, helpful feedback, and responsive layouts.

**Workflow:** New → Assigned → In Progress → Resolved. Tickets may also be cancelled when permitted. Closed tickets remain available for reference.

## Technology

- Python **3.14.7**
- Django **5.2.18**
- SQLite
- Django templates, HTML, and CSS

Dependencies are pinned in [requirements.txt](helpdesk-pro/requirements.txt).

## Installation and setup

From a fresh checkout of this repository, run the following commands in a macOS/Linux terminal:

```bash
cd helpdesk-pro
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(64))')"
python manage.py migrate
read -rs DEMO_PASSWORD
export DEMO_PASSWORD
python manage.py seed_demo
unset DEMO_PASSWORD
python manage.py runserver
```

When the terminal pauses at `read -rs DEMO_PASSWORD`, enter a private password and press Enter. This password is used for the sample accounts. The seed command creates **12 fictional tickets** and can be run again without duplicating the initial data.

Open **http://127.0.0.1:8000/accounts/login/**.

Configuration variables are documented in [`.env.example`](helpdesk-pro/.env.example). The application reads environment variables from the shell; it does not load `.env` files automatically. Set `DJANGO_SECRET_KEY` again when starting a new terminal session.

### Demo accounts

| Username | Role |
|---|---|
| `employee1`, `employee2` | Employee |
| `technician1`, `technician2` | Technician |
| `itadmin` | IT Admin |

All sample users have the password entered during the first seed. For the demo, sign in as an employee to submit a ticket, as an IT Admin to assign it, and as a technician to complete the resolution.

## Running tests

With the virtual environment active and `DJANGO_SECRET_KEY` configured:

```bash
python manage.py check
python manage.py test tickets.tests
python manage.py makemigrations --check --dry-run
```

The recorded final verification includes **149 Django tests, 39 Chrome browser checks, and 14 HTTP checks**. Results and manual acceptance scenarios are documented in [Acceptance testing](helpdesk-pro/docs/ACCEPTANCE_TESTS.md).

## Project documentation

- [System design](helpdesk-pro/docs/DESIGN.md) and [ER diagram](helpdesk-pro/docs/ERD.md)
- [Interface wireframes](helpdesk-pro/docs/WIREFRAMES.md)
- [Project presentation](helpdesk-pro/docs/CAPSTONE_PRESENTATION.md)
- [Market potential and future improvements](helpdesk-pro/docs/MARKET_POTENTIAL.md)
- [Capstone requirements mapping](helpdesk-pro/docs/REQUIREMENTS_MATRIX.md)
- [Final verification report](helpdesk-pro/docs/FINAL_VERIFICATION_REPORT.md)
- [Application documentation](helpdesk-pro/README.md)

