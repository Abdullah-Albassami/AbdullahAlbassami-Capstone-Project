# HelpDesk Pro

An internal Django IT support application for employees and a small IT team. It is designed to replace scattered email or spreadsheet requests with clear ownership, consistent status, retained discussion and visible backlog.

**Current delivery: Checkpoint B — verified database and authentication foundation.** Four models, migrations, role/permission helpers, guarded administration, deterministic seed and 60 automated tests are delivered. Application login/logout pages, ticket workflow services/views/forms and rendered reports remain later checkpoints. No completed-product claim is made.

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
    tickets/         # models, auth helpers, admin, migrations, seed and tests
    templates/base.html
    static/css/style.css
    docs/            # design, ERD, wireframes, evidence, progress and demo script
    .venv/           # local only; ignored and recreated at this location
```

The `tickets` package now contains final models, shared choices/roles, account guards, permission helpers, Django admin/forms, migrations, seed fixtures/command and tests. Workflow services/forms and application URLs/views are added in C; list/report features finish in D. No temporary alternative model, workflow, account-management, audit-trail or integration subsystem is introduced.

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

At Checkpoint B only Django admin routes are wired. IT Admin can manage Departments at `/admin/`; a setup superuser can provision accounts and inspect tickets/comments read-only. With DEBUG=true the root still shows Django's development welcome page, not a HelpDesk dashboard. Application login/logout, ticket/category frontend routes and reports are not implemented yet.

Migrations and seed were verified on the working SQLite database and on a separate fresh temporary SQLite database; the 60-test suite also creates its database from committed migrations. Complete fresh-checkout/environment and real browser/mobile acceptance remain later checks. Automated tests use a fast password hasher only under test overrides; normal application settings retain Django's default password hashing. The current foundation is intended for loopback development, not public hosting or production security certification.

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

The [official guide](../CapstoneProjectGuide.pdf) is primary. The [root specification](../HELPDESK_PRO_CODEX_SPEC_FINAL.md), audit corrections and eight user amendments describe the agreed design; evidence documents distinguish planned checks from executed results. Instructor scope approval, presentation duration and instructor repository access have not been independently confirmed.

## Sample identities and security

Demo usernames are `employee1`, `employee2`, `technician1`, `technician2` and `itadmin`. The seed creates 12 tickets: 3 New, 3 Assigned, 2 In Progress, 2 Resolved and 2 Cancelled; 8 are active. Initial category active counts are Hardware 3, Software 2, Network 2, Accounts 1, Unused 0; technician counts are 3 and 2. These expectations describe the initial seed, not a reset after edits. A setup superuser is separate and optional.

Role helpers reject inactive accounts, accounts without an application role, and conflicting roles. Only active regular Technician accounts with exactly that application role are eligible assignees. Guarded built-in admin/forms and auth save/membership hooks prevent active-assignee deactivation, role removal/conflicts and promotion to superuser. Reserved role groups are protected. Ordinary account timestamps are read-only in admin; fixture timestamps/IDs establish seed provenance. Terminal ticket/comment edits are rejected by model validation and all ticket/comment mutations are disabled in admin.

Model save alone does not call full_clean. Bulk updates, through-table inserts and raw SQL are privileged maintenance that bypass parts of Django validation/signals; they are not supported application write paths. Upcoming workflow services must re-fetch, authorize and fully validate every mutation. SQLite concurrency/production guarantees are outside this local capstone scope.

All demonstration people and issues are fictional. Git excludes local environments, credentials/configuration, populated databases and generated files. Use Django authentication and keep passwords, keys and personal information out of the repository. Do not share an authenticated demonstration publicly with real data.

## Resources and assistance

This individual capstone uses the official course guide and significant OpenAI Codex assistance for requirements analysis, architecture, source preparation and verification. The student must review and understand the code, verify its behavior and personally explain the final application.

- [Django 5.2 documentation](https://docs.djangoproject.com/en/5.2/)
- [Django 5.2 Python compatibility](https://docs.djangoproject.com/en/5.2/releases/5.2/)
- [Django supported releases](https://www.djangoproject.com/download/)

Future improvement after this agreed scope could include verified email notifications or a true event history, selected according to user feedback. Neither is a missing capstone requirement.
