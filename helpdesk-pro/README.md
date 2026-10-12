# HelpDesk Pro

An internal Django IT support application for employees and a small IT team. It is designed to replace scattered email or spreadsheet requests with clear ownership, consistent status, retained discussion and visible backlog.

**Current delivery: Checkpoint A — approved design and Django foundation.** Ticket models, migrations, account provisioning, application authentication pages and business features are scheduled for the later reviewed checkpoints. This is a development status, not a claim that the final application is ready.

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
    tickets/         # one application; models/features begin in later checkpoints
    templates/base.html
    static/css/style.css
    docs/            # design, ERD, wireframes, evidence, progress and demo script
    .venv/           # local only; ignored and recreated at this location
```

Models, forms, services, permissions, feature URLs/views, admin guards, tests and migrations will be added to the existing `tickets` package in their approved checkpoints. No temporary alternative model, workflow, account-management, audit-trail or integration subsystem is introduced.

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
| `DEMO_PASSWORD` | Reserved for Checkpoint B sample-user provisioning; no value belongs in the repository |

The development server can be started with `python manage.py runserver 127.0.0.1:8000`. At Checkpoint A only Django's administration routes are wired. With DEBUG=true, Django's built-in development welcome page appears at `/`; it is not the HelpDesk dashboard. The dashboard, accounts and ticket routes are not implemented, and no database has been migrated or seeded. A pending-migrations warning is expected. Do not try to authenticate or use the admin database until Checkpoint B has been reviewed and migrations applied.

The final setup will also apply committed migrations, create sample data and verify tests; those steps are not represented as available or tested yet. The current foundation is intended for loopback development, not public hosting or production security certification.

## Design and evidence

- [Approved architecture, role matrix and URL contracts](docs/DESIGN.md)
- [Target ERD](docs/ERD.md)
- [Wireframes](docs/WIREFRAMES.md)
- [Rubric and working-evidence matrix](docs/REQUIREMENTS_MATRIX.md)
- [Verification record](docs/ACCEPTANCE_TESTS.md)
- [Checkpoint progress and blockers](docs/PROGRESS.md)
- [Demonstration and technical rehearsal](docs/DEMO_SCRIPT.md)
- [Amended Checkpoint A file/command/result report](docs/CHECKPOINT_A_REPORT.md)

The [official guide](../CapstoneProjectGuide.pdf) is primary. The [root specification](../HELPDESK_PRO_CODEX_SPEC_FINAL.md), audit corrections and eight user amendments describe the agreed design; evidence documents distinguish planned checks from executed results. Instructor scope approval, presentation duration and instructor repository access have not been independently confirmed.

## Sample identities and security

The planned demo usernames are `employee1`, `employee2`, `technician1`, `technician2` and `itadmin`. They do not exist at Checkpoint A. Checkpoint B will accept a runtime password and create hashed credentials. Rerunning the seed must not reset existing passwords or overwrite user changes. A setup superuser, if needed, is provisioned separately with a privately chosen password.

All demonstration people and issues are fictional. Git excludes local environments, credentials/configuration, populated databases and generated files. Use Django authentication and keep passwords, keys and personal information out of the repository. Do not share an authenticated demonstration publicly with real data.

## Resources and assistance

This individual capstone uses the official course guide and significant OpenAI Codex assistance for requirements analysis, architecture, source preparation and verification. The student must review and understand the code, verify its behavior and personally explain the final application.

- [Django 5.2 documentation](https://docs.djangoproject.com/en/5.2/)
- [Django 5.2 Python compatibility](https://docs.djangoproject.com/en/5.2/releases/5.2/)
- [Django supported releases](https://www.djangoproject.com/download/)

Future improvement after this agreed scope could include verified email notifications or a true event history, selected according to user feedback. Neither is a missing capstone requirement.
