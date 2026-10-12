# Amended Checkpoint A delivery report

Scope: design/foundation only, as authorized by the user. Application under `helpdesk-pro/`; official guide/specification remain at root. The user amendments retain four custom models, three roles, final lifecycle, required security/integrity and verifiable grading evidence. No additional account-management, audit-trail or integration subsystem is introduced. Stop before B until explicit review/approval.

## Plan and final structure

The root specification contains all eight amendments and the final directory layout. Application responsibilities, entity/role/state/HTTP/query/fixture contracts are finalized in DESIGN.md and ERD.md. WIREFRAMES.md defines shared layout, dashboard, list, detail/forms and confirmations. REQUIREMENTS_MATRIX.md maps all official requirements and all 100 marks; future behavior remains marked planned until implemented and verified. The A–G schedule and two-hour contingency remain in PROGRESS.md.

```text
repository-root/
  CapstoneProjectGuide.pdf              retained unchanged
  HELPDESK_PRO_CODEX_SPEC_FINAL.md       amended plan
  .gitignore                            retained, applies to nested application
  README.md                             repository entry point
  helpdesk-pro/
    .env.example
    README.md
    requirements.txt
    manage.py
    config/{__init__.py,settings.py,urls.py,asgi.py,wsgi.py}
    tickets/{__init__.py,apps.py}
    templates/base.html
    static/css/style.css
    docs/{DESIGN.md,ERD.md,WIREFRAMES.md,REQUIREMENTS_MATRIX.md,
          ACCEPTANCE_TESTS.md,PROGRESS.md,DEMO_SCRIPT.md,
          CHECKPOINT_A_REPORT.md}
    .venv/                              local/ignored, recreated here
```

The old ignored root `.venv/` was retained locally and is not used or submitted. No root application entry point remains. Settings compute BASE_DIR from their file location, so SQLite/templates/assets target the application directory regardless of invocation directory.

## All created, moved or modified files

Paths below are relative to the repository root. File movement reuses the original foundation rather than replacing its architecture. Entries labeled moved retain content unless a modification is specified.

| File | Action / responsibility |
| --- | --- |
| HELPDESK_PRO_CODEX_SPEC_FINAL.md | Modified: eight amendments, helpdesk-pro structure, compatibility order and A-only boundary |
| README.md | Replaced root application README with repository entry point; original content moved into application README |
| helpdesk-pro/.env.example | Moved: safe runtime configuration documentation, no credentials |
| helpdesk-pro/README.md | Moved/modified: amended setup paths, compatibility evidence, structure and actual foundation limits |
| helpdesk-pro/requirements.txt | Moved: exact verified dependency pins |
| helpdesk-pro/manage.py | Moved: Django CLI entry point |
| helpdesk-pro/config/__init__.py | Moved: project package |
| helpdesk-pro/config/settings.py | Moved: environment configuration, auth/middleware, application-relative resources |
| helpdesk-pro/config/urls.py | Moved: admin-only foundation routing |
| helpdesk-pro/config/asgi.py | Moved: ASGI entry point |
| helpdesk-pro/config/wsgi.py | Moved: WSGI entry point |
| helpdesk-pro/tickets/__init__.py | Moved: one application package |
| helpdesk-pro/tickets/apps.py | Moved: AppConfig; no business models yet |
| helpdesk-pro/templates/base.html | Moved: final reusable layout/blocks, landmarks, escaped messages and local stylesheet |
| helpdesk-pro/static/css/style.css | Moved: shared responsive styling, forms/panels/tables/focus foundations |
| helpdesk-pro/docs/DESIGN.md | Moved/modified: amended structure, compatibility, responsibility/dependency and no-extra-subsystem contracts |
| helpdesk-pro/docs/ERD.md | Moved: all target entities/fields/relationships/deletion choices; not yet migrated |
| helpdesk-pro/docs/WIREFRAMES.md | Moved: intended page and accessibility design |
| helpdesk-pro/docs/REQUIREMENTS_MATRIX.md | Moved/modified: root guide link, application-relative evidence paths, mandatory implementation/verification traceability |
| helpdesk-pro/docs/ACCEPTANCE_TESTS.md | Moved/modified: historical versus new path checks, actual rerun results, honest planned feature scenarios |
| helpdesk-pro/docs/PROGRESS.md | Moved/modified: latest authorization, amended checkpoint status and blockers |
| helpdesk-pro/docs/DEMO_SCRIPT.md | Moved: required guide-order demo and individual technical rehearsal |
| helpdesk-pro/docs/CHECKPOINT_A_REPORT.md | Created: complete file/command/result/remaining-work report |

`CapstoneProjectGuide.pdf` and root `.gitignore` are retained unchanged. The nested `.venv/` is a newly created ignored runtime directory, not a tracked source deliverable. Moves are intentional removals of the former root copies, not deletion of their contents.

## Commands and read-only checks executed

Secrets used in checks were generated inside temporary process environments and never printed or written to files. No command below runs migrations or implements B.

| Step / working directory | Actual command or tool execution | Outcome |
| --- | --- | --- |
| Repository inspection / root | git status --short; rg --files --hidden with Git/venv exclusions; cat/rg reads of README/settings/URLs/pins/ignore/design/specification/evidence; parent AGENTS.md lookup | Clean baseline; no applicable AGENTS.md found; existing foundation contracts inspected |
| Compatibility / root | .venv/bin/python -B - (stdin script reading Python/SQLite versions and installed distribution Requires-Python/dependency metadata) | Python 3.14.7, SQLite 3.53.4; pinned package metadata permits >=3.10 |
| Official compatibility / web read | Open official Django 5.2 release notes and supported-download page | Python 3.14 supported from 5.2.8; 5.2.18 LTS supported through April 2028; completed before new installation |
| Plan edits | apply_patch on root specification, followed by structure confirmation | All eight amendments recorded before relocating application files |
| Relocation / root | python3 -B - (stdin guarded Path.rename script) | First preflight safely aborted because target existed; no files moved on that attempt |
| Target inspection / root | ls -la helpdesk-pro; rg --files --hidden --no-ignore helpdesk-pro with generated-file exclusions | Existing target confirmed empty |
| Relocation / root | python3 -B - (corrected preflight and Path.rename of nine named files/directories) | Application/docs moved; source guide/specification retained |
| Environment / helpdesk-pro | python3 -m venv .venv | Fresh environment created at final location; old environment not moved |
| Dependencies / helpdesk-pro | .venv/bin/python -m pip install --no-cache-dir -r requirements.txt | Installed Django 5.2.18, asgiref 3.12.1, sqlparse 0.6.0 after compatibility verification; network approval used |
| Documentation edits | apply_patch on application README/design/progress/matrix/acceptance and root README/report | All paths/statuses reflect the amendment and actual development stage |
| Dependency verification / helpdesk-pro | .venv/bin/python -m pip --no-cache-dir check | No broken requirements found |
| Integration verification / helpdesk-pro | .venv/bin/python -B - (stdin assertions for pins/environment/syntax/checks/settings/template/static/HTTP) | R02–R06 passed; initial R07 debug-root assertion failed and was corrected as documented |
| Django subprocess checks / application and root | New .venv Python invokes manage.py check with runtime-only keys, from both working directories | Zero system issues for valid settings; invalid configurations rejected |
| HTTP recheck / helpdesk-pro | .venv/bin/python -B - (stdin R07 assertions using Client/resolve/override_settings) | Admin 200/302, CSRF 403, missing feature routes, debug welcome/default-false 404s; zero queries/no DB files |
| Hygiene / root | Python stdin checks of links, paths, preserved guide/source content, pins and Git-ignore rules; git diff --check and staged equivalent | R08 passed: 25 source files, guide/15 files byte-preserved, links/ignore rules/whitespace correct |
| Milestone / root | git add on explicit root/application paths; git commit -m "refactor: align checkpoint A with approved application structure"; git status --short | Local validated checkpoint commit; final result reported after execution |

The long stdin scripts are ad hoc assertions, not a checked-in business test suite. Their scenarios/outcomes are recorded in ACCEPTANCE_TESTS.md. Expected CSRF rejection logs are not application failures. No network-hosted deployment, actual browser session or running TCP development server is claimed.

## Actual verification and remaining evidence

R01–R08 passed as recorded in ACCEPTANCE_TESTS.md. The validated milestone is committed with this record; use Git history for the final commit identifier. The first debug-root assertion was an incorrect assumption about Django's development welcome page; the recheck verified no dashboard route and 404s with DEBUG=false. Original root-location results remain labeled historical.

No custom models, migration files/commands, seeded users, account provisioning guards, ticket forms/routes/services/reports or business test suite have been implemented. Real browser/mobile/keyboard checks and the complete fresh-checkout/schema/seed test remain NOT RUN. Scaffold HTTP/template checks do not satisfy the completed-product workflow evidence.

## Outstanding risks and next checkpoint

- Two-day deadline is tight; preserve mandatory functionality/evidence and contingency rather than optional additions.
- Instructor scope agreement, allotted presentation duration, repository access and available focused hours are not independently confirmed.
- Runtime secret key must be set for commands; DEBUG defaults to local development. This is not a production deployment assurance.
- The ERD is an approved target until B produces models/migrations and verifies a matching schema.
- Known-state seed/collision/password preservation and guarded Django admin/provisioning rules remain mandatory B work, not current protections.

**Next: Checkpoint B only after user review/approval.** Implement final Department/Category/Ticket/TicketComment models, explicit constraints and committed migrations, shared role/eligibility helpers, read-only ticket/comment admin and minimal guarded built-in account provisioning, and non-destructive idempotent demo seed. Verify schema, model/database rules, deletion protections, role changes and seed idempotency/collisions/password preservation; commit and stop before C.
