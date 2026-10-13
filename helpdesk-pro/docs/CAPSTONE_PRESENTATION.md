# HelpDesk Pro — Capstone Presentation

**Individual Django capstone** | **Audience:** SMBs | **Estimated speaking:** 5–7 minutes, excluding extended demonstration and questions.

> Each numbered section is a presentation segment with speaker guidance. This is a Markdown presentation, not a PowerPoint. Present the working application, not an invented deployment.

## 1. Introduction

**HelpDesk Pro — Internal IT support, organized.**

A Django application for managing support requests using a relational database, role-based workflows, and operational reporting.

**What to say:** “HelpDesk Pro organizes internal IT support requests in one workflow. It is an individually developed and verified capstone prototype rather than a commercially deployed ITSM service.”

## 2. Audience and problem

**Audience:** Small and medium-sized businesses with employees and internal IT support responsibilities.

IT requests handled through separate emails, calls, messages, or spreadsheets may be difficult to prioritize and track consistently. A centralized record makes ownership and unresolved work visible.

**What to say:** “A small business may receive requests through several channels, making it harder to see what's still open and who owns it. HelpDesk Pro provides a consistent workflow. This is a plausible problem supported by industry ITSM practices, not an interview result or quantified market claim.”

## 3. Core solution and users

| Role | What the user can do |
|---|---|
| Employee | Create and follow own requests; comment where permitted |
| IT Admin | Review, prioritize, categorize, assign/reassign, manage categories, view reports |
| Technician | Work on assigned tickets, comment, and record resolutions |

**Lifecycle:** **New → Assigned → In Progress → Resolved**. Cancellation is a separate controlled terminal path. The backend enforces record and action permissions.

**What to say:** “The three roles have clear responsibilities. We do not rely only on hidden buttons; server-side authorization protects the records.”

## 4. Live workflow

**Show:**
1. Open the local application and sign in with a private demo account.
2. Create or inspect a temporary ticket, including category, department and priority.
3. Show assignment, progress, comments, and resolution across authorized roles.
4. Show that the final outcome remains recorded.

**Preserve HD-10013**, the existing resolved-ticket evidence record; use another safe ticket for mutations.

**What to say:** “The employee submits a request, the administrator assigns it, the technician starts work and records the outcome. These actions persist in the database.”

## 5. Validation and access restrictions

**Show one actual failure case:** attempt a blank/whitespace-only required ticket field and point out the form error. Optionally demonstrate a forbidden edit or private-ticket access using a relevant test account.

**What to say:** “The form validates server-side input. Access restrictions distinguish an employee's own ticket from someone else's, and prevent prohibited transitions.”

## 6. Reporting with Django ORM

- **Aggregation:** totals by status (total, active, resolved, cancelled).
- **Annotation:** category backlog and technician workload, including zero-count categories.
- **Querying:** related-field filters, Q-object search, ordering, and pagination.

**Historical owner-observed snapshot (13 Oct 2026):** 15 total, 8 active, 3 resolved, 4 cancelled. These numbers reflect a development database after manual tests; **fresh seed is 12 tickets**. Use the *actual live counts* during the presentation rather than presenting the historical snapshot as current.

**What to say:** “Aggregate returns overall QuerySet summary values. Annotate adds calculated counts to each category or technician. The dashboard queries the stored data rather than hardcoding counts.”

## 7. Architecture and database

**Request path:** named URL → view/permissions/form → service/business logic → Django ORM/models → database → template.

**Custom models:** `Department`, `Category`, `Ticket`, `TicketComment`; Django provides built-in users and groups.

**Show:** the repository ERD at [ERD.md](ERD.md) and an actual ticket detail or category page. Highlight Foreign Keys, protective deletion, model validation, and database check constraints.

**What to say:** “Django URLs route requests to views. Forms validate input; services enforce workflow rules, and the ORM persists related records. Protected references prevent removal of categories used by tickets.”

## 8. Market potential and competition

ServiceNow and Jira Service Management already offer comprehensive products. HelpDesk Pro is **not** presented as their equal or as proven cheaper. Its **hypothesized positioning** is a focused, customizable internal ticketing workflow for organizations with comparatively straightforward requirements, potentially combined with setup and maintenance services.

**Adoption sequence:** controlled pilot → real usability/security/cost assessment → supported deployment if validated.

**What to say:** “The product's narrower scope could suit some businesses, but adopting an unfamiliar provider is a real risk. Security, backups, total cost, maintenance, and actual user demand must be validated first.”

Read the [market-potential justification](MARKET_POTENTIAL.md) for references and the limits of the claims.

## 9. Limitations and next improvement

- Functional educational prototype, not a production-hardened SaaS/enterprise platform.
- No claim of customer adoption, production SLAs, commercial support, or validated cost savings.
- Future priorities: pilot feedback, deployment safeguards/backups, then targeted additions such as notifications or SLA monitoring if users need them.

**What to say:** “The next step is not to add features randomly. It is to validate the workflow and address operational requirements before a company could rely on the service.”

## 10. Conclusion and questions

**HelpDesk Pro demonstrates** a persisted ticket lifecycle, permissions, CRUD, database relationships, ORM queries/reporting, validation, and reproducible setup.

**Repository:** https://github.com/Abdullah-Albassami/AbdullahAlbassami-Capstone-Project (private; instructor requires access)

**What to say:** “Thank you. I'm ready to explain the implementation, database design, permissions, reports, and testing evidence.”

---

## Technical Q&A

**Why Django?** It provides routing, forms, ORM, authentication, templates, and migrations in one Python framework.

**Aggregate versus annotate?** `aggregate()` returns overall summary values; `annotate()` attaches calculations to individual objects or groups.

**Why backend authorization?** A user can send crafted requests even when a UI button is hidden. Views/services enforce role and record access.

**Why not ServiceNow?** HelpDesk Pro targets a narrower use case. It cannot yet match mature vendors' integrations, reliability, or support; commercial fit requires a pilot.

**Why cancel instead of delete?** Retain the requester, assignment, comments, and outcome; prevent losing historical support records.

**How was it verified?** Checkpoint G passed 149 Django tests, 39 Chrome checks, 14 HTTP checks, and a fresh installation. M01–M09 were separately recorded as user-observed. Remaining human checks and instructor confirmation should not be claimed completed.

**Explain a request:** `/tickets/new/` → named URL/view → validated form → authorized service → model/ORM save → redirect/rendered template.

**Reminder:** Rehearse personally, use current live data, don't expose passwords, and don't claim any unperformed acceptance checks passed. The instructor's allocated duration still needs confirmation.
