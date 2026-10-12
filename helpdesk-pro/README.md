# HelpDesk Pro

An internal Django IT support application for employees and a small IT team. It is designed to replace scattered email or spreadsheet requests with clear ownership, consistent status, retained discussion and visible backlog.

**Current delivery: Checkpoint C — complete ticket web workflow.** Login/POST logout, role dashboards/queues, ticket CRUD through cancellation, assignment/reassignment, progress/resolution and immutable comments are implemented using shared validated services. The four-model schema and deterministic seed are retained; 101 automated tests pass. Category CRUD, advanced filtering/ordering/pagination and full status/category/technician reporting remain D. Real browser acceptance and final readiness checks remain pending.

## Final project structure

The user requires the application inside `helpdesk-pro/`. The source guide/specification, repository-wide `.gitignore` and entry-point README remain one directory above. Application setup, templates, static assets, environment and design/evidence documents belong here.

```text
repository-root/
  CapstoneProjectGuide.pdf
  HELPDESK_PRO_CODEX_SPEC_FINAL.md
  .gitignore
  README.md
  helpdesk-pro/
    .env.example
    requirements.txt
    manage.py
    README.md
    config/          # settings, URLs, ASGI and WSGI
    tickets/         # models, permissions, services, forms, views, URLs, admin, seed/tests
    templates/       # inherited login, workflow and error pages
    static/css/style.css
    docs/            # design, ERD, wireframes, evidence, progress and demo script
    .venv/           # local only; ignored and recreated at this location
```

The `tickets` package contains models, shared choices/roles, account guards, permissions, workflow services/forms/views/URLs, guarded Django admin, migrations, seed and tests. The list has stable newest-first ordering; advanced list controls, category CRUD and full reports finish in D. No alternative model, workflow, account-management, audit-trail or integration subsystem is introduced.

## Product and agreed scope

Employees submit and follow their requests; IT Admin assigns and prioritizes work; technicians start, discuss and resolve assigned requests. Tickets are retained through cancellation. Administrators manage categories and inspect backlog by category and technician. Departments are selected per issue.

The proposed organizational value is less ambiguity over responsibility and unresolved requests. Those benefits are hypotheses, not measured customer results; no market study or paying-customer claim is made. An organization could adopt the tool internally. No commercial launch or deployment is part of this capstone. The final product retains discussion and outcomes, not a complete status/assignment audit log.

No API, file uploads, email notifications, AI, external services, multi-tenancy, SLA scheduling, Docker, payments or charts library is included. Authentication, role/object access, CRUD, search, ordering, reporting, validation, documentation and verification are required final features.

## Verified environment

- Python 3.14.7
- Django 5.2.18 LTS
- SQLite 3.53.4 on the development machine (other Django-supported SQLite versions may be used)
- asgiref 3.12.1 and sqlparse 0.6.0

`requirements.txt` pins the installed dependencies. Use Python 3.14 for a matching environment. The application uses SQLite and local assets; no third-party service is needed.

Compatibility was checked **before installation into this application environment**: official Django documentation supports Python 3.14 from 5.2.8, and its supported-release table lists Django 5.2.18 LTS with extended support through April 2028. The pinned Django/asgiref/sqlparse package metadata permits Python >=3.10. Runtime/dependency checks are recorded separately from these compatibility facts. [Python support](https://docs.djangoproject.com/en/5.2/releases/5.2/), [supported releases](https://www.djangoproject.com/download/).

## Foundation setup

From the repository root on macOS/Linux:

```sh
cd helpdesk-pro
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(64))')"
python manage.py check
```

Generate your own key; the command captures it into the environment rather than displaying it. Never put the actual key in a commit, screenshot or shared command log. A new shell needs the environment variable again. `.env.example` documents the variable names only; the application does not load `.env` files automatically.

If you are already inside `helpdesk-pro/`, omit the first `cd`. Recreate the environment at this path instead of moving an old `.venv`, because activation scripts and executable paths depend on its location. The ignored root environment from the earlier foundation is no longer used; it is not part of the submitted source.

| Variable | Behavior |
| --- | --- |
| `DJANGO_SECRET_KEY` | Required runtime random key, at least 50 characters; missing/example keys are rejected |
| `DJANGO_DEBUG` | Defaults to `true` for local development; accepts true/false/1/0 |
| `DJANGO_ALLOWED_HOSTS` | Defaults to localhost, 127.0.0.1 and [::1]; explicit hosts required, wildcard rejected |
| `DEMO_PASSWORD` | Required by seed_demo only for newly created users; no value belongs in the repository |

## Database, sample accounts and tests

After the foundation setup above, from `helpdesk-pro/` with the virtual environment active and runtime secret key set:

```sh
python manage.py migrate --noinput
# Type a private demo password and press Enter; read hides your input.
read -rs DEMO_PASSWORD
export DEMO_PASSWORD
python manage.py seed_demo
unset DEMO_PASSWORD
python manage.py check --database default
python manage.py makemigrations --check --dry-run
python manage.py migrate --check
python manage.py test tickets.tests --verbosity 1
python manage.py runserver 127.0.0.1:8000
```

Use a password accepted by Django's validators. All five demo accounts initially use your runtime value, hashed by Django. The seed refuses unrelated reserved IDs/names, preserves recognized edited records and existing passwords, and can be rerun without DEMO_PASSWORD once all demo users exist. It is not a database reset. The command is intended for a local fictional demonstration.

Current development data was seeded using a generated password that was not displayed or stored in source. To choose known credentials privately for an existing account, run `python manage.py changepassword employee1` (or technician1/itadmin/etc.); repeating seed with a new environment password does not reset it. To provision a separate setup administrator, use `python manage.py createsuperuser` and choose a non-demo username/private password.

Open `http://127.0.0.1:8000/accounts/login/` and sign in with a demo username and your private password. `/` shows the role dashboard; `/tickets/` lists permitted tickets; `/tickets/new/` accepts Employee/IT Admin submissions. Ticket detail offers only permitted actions and related discussion. Logout is a POST form in the navigation. IT Admin manages Departments at `/admin/`; a setup superuser provisions accounts and inspects tickets/comments read-only. Category frontend routes are reserved for D.

Migrations and seed were verified on the working database and separate fresh temporary SQLite files. The 101-test suite creates its database from committed migrations. A CSRF-enforced HTTP-client journey also used fresh seeded data with normal password hashing, exercised resolution and cancellation, and confirmed persisted state after reopening the connection. Complete fresh-checkout/environment and real browser/mobile acceptance remain later checks. Tests use a fast hasher only under overrides; normal settings retain Django's default hashing. This setup is for loopback development.

## Ticket workflow and access

| Role | Visible tickets | Actions |
| --- | --- | --- |
| Employee | Own | Submit; edit/cancel own unassigned New; comment on own active; read outcomes |
| Technician | Assigned | Start Assigned; resolve In progress with a note; comment while active |
| IT Admin | All | Submit/edit active; assign/reassign; start/resolve in valid state; cancel/comment active |

New → Assigned → In progress → Resolved. Admin reassignment preserves Assigned/In progress status and removes the previous technician's access immediately. Employee cancels own New; IT Admin cancels any active ticket. Resolved/Cancelled are read-only, including comments. Cancellation retains the record, assignee and discussion. Requester, author, status and timestamps come from the server, never editable posted fields.

Missing/out-of-scope tickets return a safe 404; forbidden role/action 403; stale/terminal lifecycle requests 409; unsupported methods 405. Invalid values return bound field/non-field errors without saving. Successful mutations redirect with feedback. The dashboard's four summary cards use scoped ORM aggregate counts; complete status/backlog/workload reporting remains D.

## Design and evidence

- [Approved architecture, role matrix and URL contracts](docs/DESIGN.md)
- [Target ERD](docs/ERD.md)
- [Wireframes](docs/WIREFRAMES.md)
- [Rubric and working-evidence matrix](docs/REQUIREMENTS_MATRIX.md)
- [Verification record](docs/ACCEPTANCE_TESTS.md)
- [Checkpoint progress and blockers](docs/PROGRESS.md)
- [Demonstration and technical rehearsal](docs/DEMO_SCRIPT.md)
- [Amended Checkpoint A file/command/result report](docs/CHECKPOINT_A_REPORT.md)
- [Checkpoint B file/command/result report](docs/CHECKPOINT_B_REPORT.md)
- [Checkpoint C file/command/result report](docs/CHECKPOINT_C_REPORT.md)

The [official guide](../CapstoneProjectGuide.pdf) is primary. The [root specification](../HELPDESK_PRO_CODEX_SPEC_FINAL.md), audit corrections and eight user amendments describe the agreed design; evidence documents distinguish planned checks from executed results. Instructor scope approval, presentation duration and instructor repository access have not been independently confirmed.

## Sample identities and security

Demo usernames are `employee1`, `employee2`, `technician1`, `technician2` and `itadmin`. The seed creates 12 tickets: 3 New, 3 Assigned, 2 In Progress, 2 Resolved and 2 Cancelled; 8 are active. Initial category active counts are Hardware 3, Software 2, Network 2, Accounts 1, Unused 0; technician counts are 3 and 2. These expectations describe the initial seed, not a reset after edits. A setup superuser is separate and optional.

Role helpers reject inactive accounts, accounts without an application role, and conflicting roles. Only active regular Technician accounts with exactly that application role are eligible assignees. Guarded built-in admin/forms and auth save/membership hooks prevent active-assignee deactivation, role removal/conflicts and promotion to superuser. Reserved role groups are protected. Ordinary account timestamps are read-only in admin; fixture timestamps/IDs establish seed provenance. Terminal ticket/comment edits are rejected by model validation and all ticket/comment mutations are disabled in admin.

Model save alone does not call full_clean. Bulk updates, through-table inserts and raw SQL are privileged maintenance that bypass parts of Django validation/signals; they are not supported application write paths. Every web mutation uses a transaction and re-fetches current scope/state, authorizes and validates the complete record before saving. SQLite does not provide row locking through select_for_update; enterprise concurrent-write guarantees are outside this local capstone scope.

All demonstration people and issues are fictional. Git excludes local environments, credentials/configuration, populated databases and generated files. Use Django authentication and keep passwords, keys and personal information out of the repository. Do not share an authenticated demonstration publicly with real data.

## Resources and assistance

This individual capstone uses the official course guide and significant OpenAI Codex assistance for requirements analysis, architecture, source preparation and verification. The student must review and understand the code, verify its behavior and personally explain the final application.

- [Django 5.2 documentation](https://docs.djangoproject.com/en/5.2/)
- [Django 5.2 Python compatibility](https://docs.djangoproject.com/en/5.2/releases/5.2/)
- [Django supported releases](https://www.djangoproject.com/download/)

Future improvement after this agreed scope could include verified email notifications or a true event history, selected according to user feedback. Neither is a missing capstone requirement.
