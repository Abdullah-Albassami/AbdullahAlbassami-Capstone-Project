# HelpDesk Pro

An internal Django IT support application for employees and a small IT team. It is designed to replace scattered email or spreadsheet requests with clear ownership, consistent status, retained discussion and visible backlog.

**Current delivery: Checkpoint F — final documentation and demonstration preparation.** The complete ticket, category, query and reporting application was delivered through E. Its latest executed regression evidence is **149 passing Django tests and 39 real headless Chrome checks**. F changes documentation only. HD-10013's user-observed lifecycle remains separate from automation; outstanding human acceptance, a full fresh checkout and student rehearsal are pending. Checkpoint G requires explicit approval; final submission readiness is not yet established.

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
    scripts/         # optional isolated Chrome verification, no app dependency
    .venv/           # local only; ignored and recreated at this location
```

The `tickets` package contains models, shared roles/account guards/permissions, validated ticket/category services and forms, HTTP views/URLs, scoped queries/reports in queries.py, guarded Django admin, migrations, seed and tests. No alternative model, workflow, account-management, audit-trail or integration subsystem is introduced.

## Product and agreed scope

Employees submit and follow their requests; IT Admin assigns and prioritizes work; technicians start, discuss and resolve assigned requests. Tickets are retained through cancellation. Administrators manage categories and inspect backlog by category and technician. Departments are selected per issue.

The proposed organizational value is less ambiguity over responsibility and unresolved requests. Those benefits are hypotheses, not measured customer results; no market study or paying-customer claim is made. An organization could adopt the tool internally. No commercial launch or deployment is part of this capstone. The final product retains discussion and outcomes, not a complete status/assignment audit log.

The target is a small organization's employees, its technicians and the person coordinating IT support. Compared with email/shared spreadsheets, each request has one persisted owner, controlled lifecycle, related discussion and live workload counts. A realistic adoption model is a pilot within one IT team: a setup administrator provisions roles/departments/categories, employees submit requests and IT Admin assigns work. Staff could then review whether ownership and backlog visibility help them before any wider rollout. This is an adoption proposal, not a deployed pilot or validated demand. Executed workflows and reports demonstrate feasibility; they do not measure time savings or user satisfaction.

No API, file uploads, email notifications, AI, external services, multi-tenancy, SLA scheduling, Docker, payments or charts library is included. Authentication, role/object access, CRUD, search, ordering, reporting, validation, documentation and verification are required final features.

## Verified environment

- Python 3.14.7
- Django 5.2.18 LTS
- SQLite 3.53.4 on the development machine (other Django-supported SQLite versions may be used)
- asgiref 3.12.1 and sqlparse 0.6.0

`requirements.txt` pins the installed dependencies. Use Python 3.14 for a matching environment. The application uses SQLite and local assets; no third-party service is needed.

Compatibility was checked **before installation into this application environment** in A: official Django documentation supports Python 3.14 from 5.2.8, and the supported-release table at that verification listed Django 5.2.18 LTS with extended support through April 2028. The pinned Django/asgiref/sqlparse package metadata permits Python >=3.10. These are recorded compatibility checks, not a claim that this pin is the latest available patch. [Python support](https://docs.djangoproject.com/en/5.2/releases/5.2/), [supported releases](https://www.djangoproject.com/download/).

## Installation and configuration

Start from a checkout of this repository, not a copy of the local database or virtual environment. On macOS/Linux, ensure `python3 --version` reports the verified Python 3.14.7 (or select that installed interpreter explicitly). These commands use a bash/zsh shell; no application packages need to be installed globally.

```sh
cd helpdesk-pro
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(64))')"
python manage.py check
```

Generate your own key; the command captures it into the environment rather than displaying it. Never put the actual key in a commit, screenshot or shared command log. A new shell needs the environment variable again. `.env.example` documents the variable names only; the application does not load `.env` files automatically.

If you are already inside `helpdesk-pro/`, omit the first `cd`. Recreate the environment at this path instead of moving an old `.venv`, because activation scripts and executable paths depend on its location. A complete fresh-checkout/environment execution remains the G readiness check; earlier temporary-database checks and E's test database are evidence for migrations/seed, not that full installation.

| Variable | Behavior |
| --- | --- |
| `DJANGO_SECRET_KEY` | Required runtime random key, at least 50 characters; missing/example keys are rejected |
| `DJANGO_DEBUG` | Defaults to `true` for local development; accepts true/false/1/0 |
| `DJANGO_ALLOWED_HOSTS` | Defaults to localhost, 127.0.0.1 and [::1]; explicit hosts required, wildcard rejected |
| `DEMO_PASSWORD` | Required by seed_demo only for newly created users; no value belongs in the repository |

## Database, sample accounts and tests

After installation above, from `helpdesk-pro/` with the virtual environment active and runtime secret key set:

```sh
python manage.py migrate --noinput
# Type a private demo password and press Enter; read hides your input.
read -rs DEMO_PASSWORD
export DEMO_PASSWORD
python manage.py seed_demo
unset DEMO_PASSWORD
# Repeat without a password: recognized records and credentials are preserved.
python manage.py seed_demo
python -m pip check
python manage.py check --database default
python manage.py makemigrations --check --dry-run
python manage.py migrate --check
python manage.py test tickets.tests --verbosity 1
python manage.py runserver 127.0.0.1:8000
```

Use a password accepted by Django's validators. All five demo accounts initially use your runtime value, hashed by Django. The seed refuses unrelated reserved IDs/names, preserves recognized edited records and existing passwords, and can be rerun without DEMO_PASSWORD once all demo users exist. It is not a database reset. The command is intended for a local fictional demonstration.

Current development data was seeded using a generated password that was not displayed or stored in source. To choose known credentials privately for an existing account, run `python manage.py changepassword employee1` (or technician1/itadmin/etc.); repeating seed with a new environment password does not reset it. To provision a separate setup administrator, use `python manage.py createsuperuser` and choose a non-demo username/private password.

Open `http://127.0.0.1:8000/accounts/login/` and sign in with a demo username and your private password. `/` shows the role dashboard; `/tickets/` searches/filters/orders/pages permitted tickets; `/tickets/new/` accepts Employee/IT Admin submissions. Ticket detail offers permitted actions and related discussion. `/categories/` gives IT Admin Category CRUD and active counts; each category has a detail page and related-ticket link. Referenced categories cannot be deleted, including references from terminal tickets. Logout is a POST form. IT Admin manages Departments at `/admin/`; a setup superuser provisions accounts and inspects tickets/comments read-only.

Migrations/seed were verified on working and separate fresh temporary SQLite databases. The 149-test suite creates its database from committed migrations. Real Chrome used a disposable seeded WSGI server with normal hashing/CSRF: 34 page/viewport audits, three basic keyboard scenarios, a role/action journey and guarded administration (39 checks total). This covers contrast, labels/errors, terminal controls, Category/query behavior and long-text layouts; it is automation, not human acceptance or a full fresh checkout. Fast hashing is only under test overrides; normal settings retain default hashing. This setup is for loopback development.

For human acceptance, follow [MANUAL_BROWSER_CHECKS](docs/MANUAL_BROWSER_CHECKS.md) with your existing private demo credentials. Optional browser automation requires installed Node and Chrome, separate from application dependencies: Node 21.7.2 was verified; earlier runs used Chrome 154.0.8037.99 and the final run reported Chrome 155.0.8059.40.

```sh
# From the repository root. Uses a new temporary DB/profile; refuses an existing DB.
HELPDESK_BROWSER_EVIDENCE=/private/tmp/helpdesk-e-evidence node helpdesk-pro/scripts/verify_browser.mjs
```

HELPDESK_CHROME may point to another installed compatible Chrome binary. Without an evidence path the script creates a separate temporary evidence directory and prints its path. It generates runtime-only credentials, deletes its DB/profile/server, and retains screenshots/result JSON without secrets. It does not use or reset your working database. Sandbox execution may require local-port/browser approval. No browser packages or frontend dependencies are installed. [Executed evidence](docs/evidence/checkpoint-e/results.json) and [E report](docs/CHECKPOINT_E_REPORT.md) distinguish measured checks from remaining accessibility/human review.

## Ticket workflow and access

| Role | Visible tickets | Actions |
| --- | --- | --- |
| Employee | Own | Submit; edit/cancel own unassigned New; comment on own active; read outcomes |
| Technician | Assigned | Start Assigned; resolve In progress with a note; comment while active |
| IT Admin | All | Submit/edit active; assign/reassign; start/resolve in valid state; cancel/comment active |

New → Assigned → In progress → Resolved. Admin reassignment preserves Assigned/In progress status and removes the previous technician's access immediately. Employee cancels own New; IT Admin cancels any active ticket. Resolved/Cancelled are read-only, including comments. Cancellation retains the record, assignee and discussion. Requester, author, status and timestamps come from the server, never editable posted fields.

Missing/out-of-scope tickets return safe 404; forbidden role/action 403; stale/terminal lifecycle requests 409; unsupported methods 405. Invalid values return bound field/non-field errors without saving. Successful mutations redirect with feedback.

Login/logout use small Django-view subclasses to clear previous-account feedback, including the existing admin logout URL; authentication, CSRF, sessions and safe redirects remain Django's responsibility. Authenticated application pages use no-store/private cache headers. Method failures retain 405/Allow with navigation guidance. Assignment choices show Full Name (username), falling back to username; IDs/eligibility are unchanged. Queues display requester/assignee consistently. Mobile tables scroll locally with a hint/focus; valid long names/titles wrap in confirmations.

## Database design

Four custom models use integer BigAutoField keys. Department has a required unique name; Category has a required unique name and optional description. Ticket holds the issue, priority/state, requesting department/category/requester, optional assignee and timestamps/resolution. TicketComment holds immutable discussion with an author and timestamp. Name uniqueness is case-sensitive; meaningful required text is trimmed. User and Group are Django's built-in models, with exactly one application role per regular account.

| Foreign key | Required? | Deletion behavior |
| --- | --- | --- |
| Ticket → Category / Department / requester User | Yes, each | PROTECT |
| Ticket → assignee User | No | PROTECT |
| TicketComment → Ticket | Yes | CASCADE |
| TicketComment → author User | Yes | PROTECT |

Each parent has zero or more children; each child has one parent except the optional ticket assignee. There is no User–Department relationship: the department is selected for each issue. Database checks constrain allowed priority/status, assignment by state and resolution note/timestamp pairing. Model validation enforces meaningful text; services enforce actor, current state and terminal rules. `full_clean()` is explicit because `save()` does not invoke it. PROTECT retains referenced records; cancellation provides safe ticket retirement. CASCADE describes privileged physical deletion, which the supported application/admin ticket interfaces prohibit. See the [matching ERD](docs/ERD.md) and [business-rule design](docs/DESIGN.md).

## Search, pagination and reports

Ticket filters are optional: q (case-insensitive title/description search, maximum 200 characters), status, priority and category. Valid filters combine with AND; category filtering traverses category__name using the selected category. Order choices are newest, oldest, priority (High → Medium → Low) and recently updated, with ID/time tie-breakers. Invalid fields are ignored independently with visible errors; ambiguous repeated filters are ignored; unexpected keys never enter the queries or pagination links. Valid selections are retained across ten-ticket pages. Missing/nonnumeric/negative/zero/repeated page values select the first page; positive out-of-range numbers select the last.

Dashboard cards and five-status breakdown share one scoped aggregate query and show zeros for absent states. Only IT Admin sees every-category active-ticket annotations and eligible-technician active-assignment annotations, including zero rows. Active always means New + Assigned + In progress. Category backlog helps identify issue areas needing attention; workload supports assignment decisions and measures assigned work, not actual availability. Independent queries and distinct counts prevent relationship-based inflation. Employees see own metrics; technicians see assigned metrics.

In [queries.py](tickets/queries.py), `ticket_summary()` uses `aggregate()` to return one set of queryset totals. `category_backlog()` and `technician_workload()` use `annotate()` to attach a filtered `Count(..., distinct=True)` to each category/eligible technician. They are rendered by the [dashboard](templates/tickets/dashboard.html) and [category table](templates/tickets/includes/category_report_table.html); [report tests](tickets/tests/test_reports.py) verify known values, zero/empty datasets, role scope and multiple related comments/groups. Search uses Q objects for title OR description, ANDs the other filters and traverses `category__name` for explicit related-model filtering.

The pristine seed has 12/8/2/2 total/active/resolved/cancelled. The local database now includes user-created resolved HD-10013; read-only verification found **13/8/3/2**, with status counts 3/3/2/3/2. Reports calculate current persisted values, never seed constants. Repeated seed preserves edits and does not reset the database.

## Design and evidence

- [Approved architecture, role matrix and URL contracts](docs/DESIGN.md)
- [Implemented ERD](docs/ERD.md)
- [Wireframes](docs/WIREFRAMES.md)
- [Rubric and working-evidence matrix](docs/REQUIREMENTS_MATRIX.md)
- [Verification record](docs/ACCEPTANCE_TESTS.md)
- [Checkpoint progress and blockers](docs/PROGRESS.md)
- [Demonstration and technical rehearsal](docs/DEMO_SCRIPT.md)
- [Amended Checkpoint A file/command/result report](docs/CHECKPOINT_A_REPORT.md)
- [Checkpoint B file/command/result report](docs/CHECKPOINT_B_REPORT.md)
- [Checkpoint C file/command/result report](docs/CHECKPOINT_C_REPORT.md)
- [Checkpoint D file/command/result report](docs/CHECKPOINT_D_REPORT.md)
- [Checkpoint E audit/file/command/result report](docs/CHECKPOINT_E_REPORT.md)
- [Remaining human acceptance instructions](docs/MANUAL_BROWSER_CHECKS.md)
- [Consolidated evidence and its limits](docs/EVIDENCE_INDEX.md)
- [Actionable submission checklist](docs/SUBMISSION_CHECKLIST.md)
- [Checkpoint F documentation delivery report](docs/CHECKPOINT_F_REPORT.md)

## Known issues and verification limits

No unresolved functional defect is known from the executed E checks. Remaining grading evidence includes human review of HD-10013's final detail/thread/controls, full keyboard-only usability, 200% zoom, screen-reader behavior, physical mobile/other browsers, guarded-admin human checks, full fresh checkout and student demonstration. Automated Chrome covered fixed desktop/mobile viewports, basic key actions and selected computed contrast rules; it is not WCAG certification. M01 remains partial user-observed and M02–M14 manual checks remain unexecuted.

SQLite transactions preserve validated writes but do not provide enterprise concurrent-write guarantees. Privileged bulk ORM/raw SQL may bypass application validation and is outside supported UI writes. Instructor scope/access/duration remain unconfirmed. G requires explicit approval; F prepares the documents and demonstration without claiming final submission readiness or a guaranteed score.

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
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) for the optional browser-verification harness.
- [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [control/focus contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) for measured interface checks. Human accessibility review remains required.

Future improvement after this agreed scope could include verified email notifications or a true event history, selected according to user feedback. Neither is a missing capstone requirement.
