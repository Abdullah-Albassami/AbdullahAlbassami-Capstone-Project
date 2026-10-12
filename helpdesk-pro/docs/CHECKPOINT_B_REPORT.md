# Checkpoint B: database and authentication foundation

User authorization: B only, after A approval. Source authority remains the root guide; the four-model design, three roles, ticket lifecycle and helpdesk-pro structure are preserved. No C workflow views/forms/services or new integration/account-management/history subsystem is included. Stop before C for explicit review/approval.

## Files created or modified

All application paths are relative to helpdesk-pro. The root guide, Git ignore rules, dependency pins, project settings/URLs, templates and CSS are unchanged.

| Files | Change / responsibility |
| --- | --- |
| tickets/constants.py | Created: shared Role/Status/Priority choices and canonical active/terminal sets |
| tickets/models.py | Created: four final models, FK/deletion rules, uniqueness, state constraints, trimmed business validation and terminal/comment immutability validation |
| tickets/permissions.py | Created: role resolution/guards, eligible technicians, scoped ticket querysets and action permissions |
| tickets/accounts.py | Created: canonical role provisioning and proposed account/membership validation |
| tickets/signals.py | Created: post-migrate role bootstrap and narrow auth save/membership/group safeguards |
| tickets/apps.py | Modified: register those auth hooks once at app startup |
| tickets/admin_forms.py | Created: guarded built-in User creation/change and Group naming forms |
| tickets/admin.py | Created: role-limited Department setup, superuser provisioning, protected groups and read-only Ticket/Comment admin |
| tickets/demo_data.py | Created: fictional deterministic identities, descriptions and chronology; no credentials |
| tickets/management/__init__.py; tickets/management/commands/__init__.py | Created: command packages |
| tickets/management/commands/seed_demo.py | Created: preflight collisions, transactional validated seed, runtime password policy and non-destructive repeats |
| tickets/migrations/__init__.py; tickets/migrations/0001_initial.py | Created/generated: complete committed schema target and four named database checks |
| tickets/tests/__init__.py; tickets/tests/helpers.py | Created: test package, fictional fixtures and runtime-generated test password; test-only fast hashing |
| tickets/tests/test_models.py | Created: defaults/text/state/constraint/FK/deletion/immutability and ERD/schema tests |
| tickets/tests/test_permissions.py | Created: role/scope/action/authentication and ordinary account/membership safeguards |
| tickets/tests/test_admin.py | Created: actual admin GET/POST/form/protected-deletion tests |
| tickets/tests/test_seed.py | Created: initial metrics, zero data, duplicate prevention, edits/password preservation, collision/rollback and historical-record recovery tests |
| .env.example; README.md | Modified: actual runtime seed configuration, migration/test/admin instructions and limits |
| docs/DESIGN.md; docs/ERD.md | Modified: implemented interfaces/schema correspondence and auth/fixture identity boundaries |
| docs/PROGRESS.md; docs/REQUIREMENTS_MATRIX.md; docs/ACCEPTANCE_TESTS.md | Modified: current stage, implemented source/check evidence and real results; UI/manual work stays pending |
| docs/DEMO_SCRIPT.md | Modified: B data available, final frontend demo still unavailable |
| docs/CHECKPOINT_B_REPORT.md | Created: this final checkpoint report |
| root HELPDESK_PRO_CODEX_SPEC_FINAL.md; root README.md | Modified: B delivery/current authorization and next C review gate |

The ignored local db.sqlite3 was created/migrated/seeded, not committed. No new third-party packages were installed.

## Models, integrity and ERD correspondence

Department name is unique/required (100). Category name is unique/required (100), description optional. Ticket title (150), description, category/department/requester, nullable assignee, priority/status choices/defaults, resolution fields and creation/update timestamps match the ERD. TicketComment has ticket/author/body/time and chronological ordering. Every custom PK is BigAutoField; built-in User/Groups are retained with no profile/user-department link.

All Ticket FKs use PROTECT; comment author uses PROTECT and comment ticket uses CASCADE. Normal retirement is cancellation; admin cannot delete tickets/comments. The database checks valid status/priority, new-unassigned versus required assignment for assigned/in-progress/resolved, and resolution note/timestamp pairing. Model validation adds meaningful trimmed text, null rejection for non-null optional text, active eligible assignee checks, terminal read-only fields and immutable authorized active comments. Historical terminal assignees may later become inactive/change role after no active assignments remain.

The applied schema was introspected in ModelTests against the approved exact field sets, columns, requiredness, lengths, custom PK type, SQL FK targets and all named check constraints. Initial migration and schema match the finalized ERD; future final-readiness checks will repeat that comparison.

## Roles and supported security boundary

Active regular users need exactly Employee, Technician or IT Admin for application access. No-role/multiple-role/inactive accounts fail closed. Active superuser explicitly resolves to IT Admin; staff alone grants no app role. Eligible assignees are active, non-superuser accounts with exactly Technician as their application role; unrelated groups are permitted.

Shared helpers scope Employee tickets by requester, Technician tickets by assignee and IT Admin tickets globally. Their tested action flags match the approved state/ownership matrix; C views/services must enforce them and derive requester/author from the session. No application login/logout or ticket endpoint has been added at B; Django's built-in backend/admin provides the current authentication interface.

Guarded User admin creation/change forms require a valid regular role. Ordinary auth save and forward/reverse group membership hooks reject deactivation, role loss/conflicts or superuser promotion that strands active assignments. Reassign first. Reserved role groups cannot be renamed/deleted and are read-only in admin. Groups are provisioned post-migration with IT Admin's four Department model permissions; other application groups have no admin permissions. Normal IT Admin may manage Departments but cannot provision accounts/groups or inspect Ticket/Comment admin. Superusers may inspect those records but add/change/delete/bulk-delete remains disabled. Account date_joined/last_login are read-only.

Full_clean is explicit, not automatic on save. Raw SQL, bulk updates and direct through-table inserts are privileged maintenance that bypass some validation/hooks; no supported application path uses them for ordinary workflow changes. Signal use is limited to existing auth safeguards, not the ticket lifecycle. SQLite concurrency guarantees and production hosting are outside the local capstone scope.

## Seed behavior and actual dataset

Five fictional users use reserved IDs 9001–9005; Departments 1101–1104, Categories 1201–1205, Tickets 10001–10012 and Comments 20001–20004. Existing timestamp fields establish provenance without an extra model/column/state file. Collision preflight refuses unrelated usernames/IDs/reference names before adoption or promotion. Recognized user profile/name/password, reference names and edited ticket fields are retained. Changing provenance dates through privileged maintenance causes safe rejection.

DEMO_PASSWORD is read only from runtime environment, validated per new user and stored through Django's password hasher. Existing accounts are never reset; repeated seeding needs no password. Missing records are validated atomically; errors roll back. Initial terminal-ticket comments are added while active; missing comments on already terminal tickets do not trigger reopening/history rewriting.

Verified initial counts: 4 departments, 5 categories, 5 users, 12 tickets and 4 comments. Statuses: 3 New, 3 Assigned, 2 In Progress, 2 Resolved, 2 Cancelled. Total/active/resolved/cancelled = 12/8/2/2; category active counts Hardware 3, Software 2, Network 2, Accounts 1, Unused 0; technicians 3/2. These are fixture/data checks, not rendered dashboard evidence. The local verification password was generated, never displayed, and not saved in source; choose known credentials privately with changepassword.

## Exact verification commands and results

From helpdesk-pro, with DJANGO_SECRET_KEY generated only inside temporary process environments:

| Command | Actual result |
| --- | --- |
| .venv/bin/python -B manage.py makemigrations tickets | Generated 0001_initial: four models plus four constraints |
| .venv/bin/python -B manage.py migrate --noinput | Auth/admin/contenttypes/sessions/tickets migrations applied OK |
| .venv/bin/python -B manage.py check | Zero issues |
| .venv/bin/python -B manage.py test tickets.tests --verbosity 2 | Initial 53 tests: one null-text validation failure; fixed, not hidden |
| .venv/bin/python -B manage.py test tickets.tests --verbosity 1 | Intermediate 53/55/56/58 PASS; final persisted-state/admin integration suite: 60 PASS |
| .venv/bin/python -B manage.py makemigrations --check --dry-run | No changes detected |
| .venv/bin/python -B manage.py migrate --check | Exit 0; no pending migrations |
| .venv/bin/python -B manage.py check --database default | Zero issues |
| .venv/bin/python -B manage.py seed_demo (twice) | 12 then 0 new; second without password; exact row/hash/time snapshots unchanged |
| .venv/bin/python -m pip --no-cache-dir check | No broken requirements found |

Commands ran via stdin Python wrappers launching actual manage.py subprocesses. The first initial wrapper called Django management directly without settings; it failed before migrations, then was corrected to invoke manage.py. An additional stdin harness configured a fresh temporary SQLite file before setup, migrated it, asserted role bootstrap, seeded twice, checked exact preservation/counts/constraints, and removed the file. That passed and establishes fresh schema/data reproducibility, not the full G checkout/environment/browser acceptance.

Final review reproduced an unsaved Group rename/deletion bypass and two unsaved-user-flag role/membership bypasses. The targeted tests initially failed; the guards were corrected to consult persisted identity/flags. Admin superuser checks use persisted state, and positive admin tests verify demotion from allowed multiple superuser roles to one regular role within the existing transaction. The final total is 60 passing tests, with no schema drift/pending migrations/system issues. Smaller totals above are intermediate results, not current coverage.

Root verification also uses git diff --check, git diff --cached --check and a source/link/ignore/pin/guide integrity harness. The verified changes are committed as `feat: add verified ticket schema, role safeguards and demo seed`; Git history supplies the final identifier without a self-referential hash in this file. Final commit/status are reported in chat.

## Remaining limitations, risks and next checkpoint

No C workflow service/form/view/frontend route, complete browser journey, mobile check or D rendered ORM report is implemented/verified. All final manual cases remain NOT RUN. Known math is supported by realistic fixtures and tests but must be integrated in rendered pages for the ORM marks. Full fresh checkout/environment proof and student rehearsal remain G. No grade guarantee is made.

Instructor scope agreement, presentation duration and repository access remain external confirmations. The two-day deadline requires prioritizing required features/evidence over optional additions. Provisioning hooks and database checks do not provide enterprise concurrency guarantees or restrict privileged arbitrary SQL maintenance.

Next is C only after explicit user review/approval: integrate login/logout, scoped dashboard/list/detail, final workflow service/forms and create/edit/cancel/assign/start/resolve/comment actions with final usable templates and session/object/state/CSRF tests. Reuse the finalized schema/helpers/seed and stop before D.
