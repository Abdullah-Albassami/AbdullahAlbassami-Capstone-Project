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

Enter a private password when prompted. `.env.example` lists configuration variables, but `.env` files are not loaded automatically. Set `DJANGO_SECRET_KEY` in each new terminal session.

Open **http://127.0.0.1:8000/accounts/login/**.

### Demo accounts

| Username | Role |
|---|---|
| `employee1`, `employee2` | Employee |
| `technician1`, `technician2` | Technician |
| `itadmin` | IT Admin |

The accounts use the password set during initial seeding. Re-running `seed_demo` preserves existing accounts and passwords. To change one, run `python manage.py changepassword employee1` (replace the username as needed).

The demo seed includes **12 fictional tickets**.

## Tests

With the environment active and `DJANGO_SECRET_KEY` set:

```bash
python manage.py check
python manage.py test tickets.tests
python manage.py makemigrations --check --dry-run
```

## How it works

- **Employee:** create a ticket, follow its status, comment on active requests, edit/cancel own unassigned New requests.
- **IT Admin:** view all tickets, assign/reassign, manage categories and inspect reports.
- **Technician:** work on assigned tickets, mark progress and submit a resolution note.

Ticket workflow: **New → Assigned → In Progress → Resolved**, with permitted cancellation. Closed tickets are read-only. Referenced categories/departments/users cannot be deleted through supported workflows.
