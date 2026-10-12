# Checkpoint G: final verification and submission readiness

13 October 2026 (Asia/Riyadh). A–F reviewed/approved. G verifies the approved application against the official [guide](../../CapstoneProjectGuide.pdf) without scope expansion. **Automated technical verification passed; human acceptance, student rehearsal and instructor confirmations remain open.** No submission, remote push, full approval or guaranteed grade is claimed. Stop after G.

## Fresh checkout: exact commands and outcomes

Source revision cloned: **d89f8748a9de33050eeb20ee7720df1eb2c253a1** (F). The executable application source is unchanged from E. A new local Git clone was created with `--no-local`, avoiding object hardlinks; no working virtual environment, database or environment file was copied. This proves reproduction from committed source, not instructor access to a remote repository.

Executed from the working repository root:

```sh
git clone --no-local /Users/abdullahalbassami/Documents/AbdullahAlbassami-Capstone-Project /private/tmp/helpdesk-g-d4n61a2_/checkout
```

Executed with working directory `/private/tmp/helpdesk-g-d4n61a2_/checkout/helpdesk-pro`:

```sh
git rev-parse HEAD
git status --short
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/python --version
.venv/bin/python -m pip --isolated install --no-cache-dir -r requirements.txt
```

Actual results: clone succeeds at the revision above; tree clean; independent Python **3.14.7** environment created; uncached package download/install succeeds with **Django 5.2.18, asgiref 3.12.1, sqlparse 0.6.0**. The first sandbox install fails to resolve pypi.org and exits 1; the approved execution of the same command succeeds. Neither the failure nor the success is disguised as use of existing installed packages.

An stdin Python wrapper removes inherited DJANGO_SECRET_KEY/DEBUG/ALLOWED_HOSTS/DEMO_PASSWORD, asserts no database or .env exists and that sys.prefix is the fresh .venv, and generates a **new private runtime secret/password**. It executes and captures these commands without printing credentials:

```sh
.venv/bin/python -m pip --isolated check
.venv/bin/python -B manage.py check --database default
.venv/bin/python -B manage.py migrate --noinput
.venv/bin/python -B manage.py seed_demo
.venv/bin/python -B manage.py seed_demo
.venv/bin/python -B manage.py makemigrations --check --dry-run
.venv/bin/python -B manage.py migrate --check
.venv/bin/python -B manage.py test tickets.tests --verbosity 1
```

[Actual fresh-checkout JSON](evidence/checkpoint-g/fresh-checkout.json) retains command/exit/stdout/stderr and versions. Every command exits **0**:

| Check | Actual result |
| --- | --- |
| Dependencies | No broken requirements; first check has a nonfatal disabled-cache advisory |
| System/database check | Zero issues |
| Fresh migrations | **19 migrations applied**, including tickets.0001_initial and Django auth/admin/session prerequisites |
| First seed | **12 new tickets**, five fictional users, related categories/departments/comments |
| Second seed | **0 new tickets**, DEMO_PASSWORD removed before execution |
| Idempotency | Exact snapshots of every table, password hashes and timestamps identical before/after second seed; PRAGMA integrity ok/FK violations zero |
| Initial totals | Total 12, active 8, resolved 2, cancelled 2; statuses New/Assigned/In progress/Resolved/Cancelled 3/3/2/2/2 |
| Migration consistency | No model changes; no unapplied migrations |
| Full suite | **149 tests PASS in 3.130s**, fresh migrated test database created/destroyed; no failures |

The seed snapshot digest is retained without exposing rows/password hashes. Tests include expected safe-404 logging; that is not a test failure. Afterwards `source .venv/bin/activate` and `python -B -` assert the correct independent prefix/version; `.venv/bin/python -m pip --isolated --no-cache-dir check` also passes without the cache advisory. The clone's tracked working tree stays clean.

## Actual browser and network/server verification

From the fresh clone's `helpdesk-pro/` directory:

```sh
HELPDESK_BROWSER_EVIDENCE=/private/tmp/helpdesk-g-d4n61a2_/evidence/browser node scripts/verify_browser.mjs
```

Actual result: **39 checks PASS**, Chrome/155.0.8059.40, installed Node 21.7.2. The existing runner uses the clone's fresh .venv and a further new seeded SQLite fixture/profile with generated private credentials, normal hashing and CSRF. It stops/removes its server/database/profile; genuine captures/results are retained. No browser/frontend packages are installed.

Coverage: **34 page audits** at desktop 1280px/emulated mobile 375px with labels/error associations/unique IDs/landmarks/CSS/selected contrast/page-width assertions; **3 basic keyboard checks**; **guarded admin**; **combined role/Category/query journey**. Actual cards initially 12/8/2/2, then 13/7/3/3 after the combined resolution/cancellation journey before stress fixtures. [Results](evidence/checkpoint-g/results.json), [desktop](evidence/checkpoint-g/dashboard-desktop.png), [mobile](evidence/checkpoint-g/dashboard-mobile.png), [login](evidence/checkpoint-g/login-mobile.png), [long category](evidence/checkpoint-g/long-category-confirmation.png), [long ticket](evidence/checkpoint-g/long-ticket-confirmation.png). Agent inspection of desktop/mobile captures agrees with the measured layout; this is not human/student acceptance.

A separate stdin urllib/cookie/CSRF harness starts an actual Django development server in the disposable clone. Private HTTP credentials are rotated there only, after the seed-idempotency assertion. Actual command:

```sh
.venv/bin/python -B manage.py runserver 127.0.0.1:53507 --noreload
```

With new runtime secret, local DEBUG=true and 127.0.0.1 hosts, **14 checks PASS**: reachable login/local CSS, anonymous redirect, normal-hasher CSRF login, employee Category denial, create/edit/comment, safe cancellation confirmation, missing-CSRF 403/no mutation, cancellation/thread/read-only retention, terminal forged comment 409, missing object 404/action GET 405, POST logout/session removal and report update **12/8/2/2 → 13/8/2/3**. [Actual HTTP/server JSON](evidence/checkpoint-g/server-access.json). Server stops in finally.

| Failure / advisory | Correction and actual recovery |
| --- | --- |
| Sandbox PyPI DNS failure | Approved network retry installs the exact pins into the fresh venv; no fallback to working packages |
| First dependency check cache advisory | Requirements were valid; additional isolated no-cache check passes without advisory |
| First ad hoc server probe sets DEBUG=false; CSS is 404 | Harness corrected to README's local default DEBUG=true; login/CSS and all 14 HTTP checks pass. Ordinary runserver does not serve static assets with DEBUG=false; README clarifies this local configuration boundary |
| Non-raw regex SyntaxWarnings in discarded probe | Corrected probe uses raw regex literals and passes; no warning originates from application source |

No genuine application defect or schema/dependency/code correction was required. The full suite reruns assignment/reassignment/access revocation, every permitted/prohibited transition, terminal/forged fields, Category CRUD/PROTECT, combined Q/related filters, all orders/page boundaries, aggregate/annotation known/zero/empty/multi-group/comment/live counts and admin/account guards. The 39 browser and 14 server checks add actual rendered/network evidence, rather than replacing these broader tests.

## Security, design and data preservation

Models, migration, permission/account/admin/service/form/query/view code, templates/CSS, verification scripts, pins and guide are unchanged from the freshly tested F commit. The fresh schema-match test validates ERD field types/nullability/relationships/deletion/four named checks; migration generation/checks have no drift. Ticket/Comment admin stays read-only, and active technician deactivation is rejected in actual Chrome; forged admin mutation/account protections also pass the suite.

Git ignores .venv/.env/SQLite/generated runtime files. Current tracked source and eight existing historical commits were scanned for private-key/token/password-literal indicators without disclosing values; no review flags found. Runtime secrets/passwords were generated only in verification processes. This inspection is evidence of repository hygiene, not a security certification or proof against every privileged maintenance operation.

Original working database is opened read-only for preservation checks only. File-byte SHA-256 and eight-table logical snapshot match G's baseline/F/E; PRAGMA integrity ok and foreign-key check empty. **HD-10013 remains Resolved**, requester 9001, assignee 9003, meaningful resolution note/timestamp. Original counts **13/8/3/2**, 13 tickets, 5 comments, 5 accounts; all department/category/membership/group/permission records preserved. Clone ticket 10013 is a different record in a different database. No login/seed/migration application/action touches the original database.

Final Markdown/source/evidence/staged inventory checks are recorded as G05 in [ACCEPTANCE_TESTS](ACCEPTANCE_TESTS.md#checkpoint-g-final-automated-verification). G changes documentation and authentic evidence only; historical A–F delivery reports and UC01–UC07 are preserved. The final candidate commit's executable-source parity with the tested clone is checked at delivery. Its hash comes from Git after commit, avoiding a self-referential hash in this file.

Actual final audit: **94 repository files, 20 Markdown documents, 268 valid local links/targets/fragments, 16 shell blocks parsed in bash/zsh**; all 66 baseline non-Markdown files unchanged, six historical delivery reports/UC section preserved, 149 test methods and all G JSON/PNG counts/results valid, all eight rubric values total 100. Exact changes: 13 modified Markdown files and nine created report/artifact files. Runtime exclusions and diff whitespace are clean; staged paths/whitespace are checked before committing.

## Eight-category grading-readiness assessment

The [source-linked requirements matrix](REQUIREMENTS_MATRIX.md) maps every normative guide requirement and all **100 marks**. These assessments do not assign predicted marks.

| Criterion | Marks | Readiness / verified evidence | Reasonable lost-marks risk remaining |
| --- | ---: | --- | --- |
| Problem and market potential | 10 | Audience/problem/value/comparison/internal adoption narrative; working product feasibility | Authentic supporting user context, demand and efficiency benefits unvalidated; label assumptions and confirm instructor scope |
| Core functionality | 20 | Complete implemented ticket/Category workflows; 149 tests + Chrome/server evidence | Human M01 final original detail and M02/M06–M11 acceptance unreported |
| Database and ORM | 20 | Fresh migrations/ERD/constraints/seed; integrated CRUD/filter/order/relationship/aggregate/annotate tests | Student must explain relationships/deletion/validation/metric arithmetic; human report checks outstanding |
| Django and Python implementation | 15 | Named routes, four-model one-app structure, forms/shared services/permissions/queries/inheritance verified | Personal URL→view→service/ORM→template explanation in M14 not confirmed |
| Interface and usability | 10 | 34 real Chrome page audits and 3 basic keyboard checks, responsive screenshots/labels/contrast/feedback | Full human keyboard/zoom/mobile/device/other-browser/screen-reader review unexecuted; no WCAG certification |
| Verification and reproducibility | 10 | Genuine fresh clone/new venv/install/config/migrate/seed twice, 149 tests/39 Chrome/14 live HTTP | Required remaining human acceptance; automated setup does not prove a student performed it |
| Git and documentation | 5 | Genuine milestone history, complete source/design/evidence/setup, valid links, local candidate commit | Instructor access and actual remote submitted revision unconfirmed; no push/submission performed |
| Demonstration and individual understanding | 10 | Six guide steps, request traces, Q&A and live metric examples prepared | Student rehearsal/live explanation and allotted duration remain unconfirmed |
| **Total** | **100** | All criteria have implemented/documented evidence | Grade remains instructor assessment; human/external gaps must be closed |

## Remaining human checks and instructor confirmations

Use [MANUAL_BROWSER_CHECKS](MANUAL_BROWSER_CHECKS.md); record scenario/expected/actual/status plus browser/version/viewport/date. **M01 partial user-observed**, **M02–M12/M14 human NOT RUN**, **M13 automated setup PASS, human repeat NOT RUN**.

- Original HD-10013: employee1, technician1, itadmin view resolution/date/discussion and verify no mutation controls; never alter it.
- M02–M11: invalid input, matching/no-match/combined queries, order/pages, edits/cancellation, Category CRUD/PROTECT, live reports, scope/reassignment and guarded admin. Use fictional temporary records; live counts change after valid actions.
- M12: desktop 1280px/emulated 375px, full Tab/Shift-Tab/Enter/arrow workflow, visible focus/skip link/local table scroll, 200% zoom and errors. Physical device/other browser/screen reader if available; explicitly record unavailable checks as unverified.
- M14: student rehearses the six-step [DEMO_SCRIPT](DEMO_SCRIPT.md): users/problem/evidence → value/persisted workflow → server validation/failure → aggregate/annotation reports → relationships/technical decision → market/limitations/next improvement. Personally trace a request and explain FK/check/role/query/math; preparation is not proof of understanding.
- Confirm instructor scope agreement, presentation duration/slot and access to the ultimately submitted repository revision. Actual remaining deadline/hours are not confirmed. No instructor message is sent by Codex.

No known unresolved application defect from executed checks. SQLite concurrent-write guarantees and privileged bulk/through-table/raw SQL validation bypass remain documented scope limits; deployment/integrations/complete event history are excluded. See [SUBMISSION_CHECKLIST](SUBMISSION_CHECKLIST.md) for final candidate/submitted hash and access actions. G stops without declaring submission/full approval.

## Complete changed-file inventory

**Modified (13):** [root README](../../README.md), [root specification](../../HELPDESK_PRO_CODEX_SPEC_FINAL.md), [application README](../README.md), [DESIGN](DESIGN.md), [ERD](ERD.md), [WIREFRAMES](WIREFRAMES.md), [REQUIREMENTS_MATRIX](REQUIREMENTS_MATRIX.md), [ACCEPTANCE_TESTS](ACCEPTANCE_TESTS.md), [PROGRESS](PROGRESS.md), [DEMO_SCRIPT](DEMO_SCRIPT.md), [MANUAL_BROWSER_CHECKS](MANUAL_BROWSER_CHECKS.md), [EVIDENCE_INDEX](EVIDENCE_INDEX.md), [SUBMISSION_CHECKLIST](SUBMISSION_CHECKLIST.md).

**Created (9):** this [G report](CHECKPOINT_G_REPORT.md), [fresh-checkout JSON](evidence/checkpoint-g/fresh-checkout.json), [HTTP/server JSON](evidence/checkpoint-g/server-access.json), [Chrome JSON](evidence/checkpoint-g/results.json), [login-mobile.png](evidence/checkpoint-g/login-mobile.png), [dashboard-desktop.png](evidence/checkpoint-g/dashboard-desktop.png), [dashboard-mobile.png](evidence/checkpoint-g/dashboard-mobile.png), [long-category-confirmation.png](evidence/checkpoint-g/long-category-confirmation.png), [long-ticket-confirmation.png](evidence/checkpoint-g/long-ticket-confirmation.png).

No application or package files modified. Verification clone/runtime files are disposable, ignored/untracked and removed after final parity/evidence checks; retained source/evidence includes no populated database/environment/private runtime values.
