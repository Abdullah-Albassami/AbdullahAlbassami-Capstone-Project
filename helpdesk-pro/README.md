# HelpDesk Pro

A Django-based internal IT support system for small and medium-sized businesses. Employees report issues, IT administrators assign work, and technicians record progress and resolutions.

## Features

- Three roles: **Employee**, **Technician**, **IT Admin**, with record-level access controls
- Ticket creation, editing, comments, assignment, reassignment, cancellation and resolution
- Category management, search, filtering, ordering and pagination
- Status totals, category backlog and technician workload using Django ORM
- Input validation, protected relationships and responsive templates

See the [ERD](docs/ERD.md), [design overview](docs/DESIGN.md), [wireframes](docs/WIREFRAMES.md) and [Markdown presentation](docs/CAPSTONE_PRESENTATION.md).

## Requirements

- Python **3.14.7** (version used for verification)
- Django **5.2.18**, with versions pinned in [requirements.txt](requirements.txt)
- SQLite (included with Python)
- No external services or JavaScript packages required to run the application

## Installation and launch

From a fresh repository checkout, use macOS/Linux Terminal:

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

Choose a private demo password when prompted. Use a strong value accepted by Django's validators. Do not commit credentials. `.env.example` describes configuration variables; this project does **not** automatically load `.env` files. A new terminal needs `DJANGO_SECRET_KEY` set again.

Open **http://127.0.0.1:8000/accounts/login/**.

### Demo accounts

| Username | Role |
|---|---|
| `employee1`, `employee2` | Employee |
| `technician1`, `technician2` | Technician |
| `itadmin` | IT Admin |

These accounts use the private password specified when seed data was first created. Running `seed_demo` again preserves existing records and passwords. For an existing account, change its password locally with `python manage.py changepassword employee1` (substitute the username). Never publish passwords.

The fresh demo seed contains **12 fictional tickets**. Later development snapshots with 13 or 15 tickets are not part of the initial seed.

## Tests

With the virtual environment active and `DJANGO_SECRET_KEY` configured:

```bash
python manage.py check
python manage.py test tickets.tests
python manage.py makemigrations --check --dry-run
```

Final independent verification reported **149 passing Django tests**, **39 Chrome browser checks**, **14 HTTP checks** and a working fresh installation. The [acceptance record](docs/ACCEPTANCE_TESTS.md) separately identifies owner-observed manual checks and outstanding scenarios.

## How it works

- **Employee:** create a ticket, follow its status, comment on active requests, edit/cancel own unassigned New requests.
- **IT Admin:** view all tickets, assign/reassign, manage categories and inspect reports.
- **Technician:** work on assigned tickets, mark progress and submit a resolution note.

Ticket workflow: **New → Assigned → In Progress → Resolved**, with permitted cancellation. Closed tickets are read-only. Referenced categories/departments/users cannot be deleted through supported workflows.

## Limitations and acknowledgments

This is a functional **capstone prototype**, not a deployed commercial ITSM product. It does not include email notifications, SLAs, integrations, attachments or managed cloud hosting. Market demand and cost savings have not been validated; see [market potential](docs/MARKET_POTENTIAL.md).

Significant AI development assistance (OpenAI Codex and ChatGPT) and official Django documentation were used during implementation, review and documentation. The work should be evaluated through the actual source, test evidence and submitted explanation.

For the full rubric mapping see [requirements](docs/REQUIREMENTS_MATRIX.md); for submission status see the [checklist](docs/SUBMISSION_CHECKLIST.md).
