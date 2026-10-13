# HelpDesk Pro

**Internal IT support ticket management for small and medium-sized businesses**

HelpDesk Pro is a Django web application for employees, IT administrators, and technicians to submit, assign, track, and resolve internal support requests. It includes role-based access, ticket and category management, search, and operational reporting.

## Start here — Submission documents

| Document | Purpose |
| --- | --- |
| [Application README](helpdesk-pro/README.md) | Features, users, setup, requirements, sample data, and usage |
| [Markdown presentation](helpdesk-pro/docs/CAPSTONE_PRESENTATION.md) | Project explanation in the format requested by the instructor |
| [ERD](helpdesk-pro/docs/ERD.md) | Entities, attributes, relationships, cardinality, and integrity rules |
| [Wireframes](helpdesk-pro/docs/WIREFRAMES.md) | Interface sketches and user journeys |
| [Market potential](helpdesk-pro/docs/MARKET_POTENTIAL.md) | Target audience, competing products, adoption proposal, and evidence |
| [Acceptance tests](helpdesk-pro/docs/ACCEPTANCE_TESTS.md) | Manual and automated verification, with evidence limitations |
| [Submission checklist](helpdesk-pro/docs/SUBMISSION_CHECKLIST.md) | Deliverables and remaining confirmations |

## Implementation and design

- [System architecture and business rules](helpdesk-pro/docs/DESIGN.md)
- [Requirements mapped to the 100-mark rubric](helpdesk-pro/docs/REQUIREMENTS_MATRIX.md)
- [Official Capstone Project Guide](CapstoneProjectGuide.pdf)
- [Final implementation specification](HELPDESK_PRO_CODEX_SPEC_FINAL.md)

## Verification summary

Checkpoint G verified an independent fresh installation, including **149 passing Django tests, 39 Chrome checks, and 14 HTTP/server checks**. On **13 October 2026**, the project owner also recorded **M01–M09 PASS within the scenarios actually observed**. Remaining manual checks and instructor confirmations are distinguished in the acceptance record rather than reported as completed.

The application is a **functional capstone prototype**, not a commercially deployed or production-hardened service. No customer adoption, measured cost savings, or validated pricing is claimed.

## Additional technical evidence

These files are retained for transparency and grading traceability. **They are not required reading to understand the product.**

- [Evidence index](helpdesk-pro/docs/EVIDENCE_INDEX.md)
- [Progress and development milestones](helpdesk-pro/docs/PROGRESS.md)
- [Manual browser test instructions](helpdesk-pro/docs/MANUAL_BROWSER_CHECKS.md)
- [Checkpoint G final verification](helpdesk-pro/docs/CHECKPOINT_G_REPORT.md)
- Earlier development logs are preserved in Git history, not included in the final documentation folder.

## Run the application

Clone this repository, enter `helpdesk-pro/`, and follow the [installation and configuration instructions](helpdesk-pro/README.md#installation-and-configuration). Dependencies, migrations, sample accounts, and safe runtime credentials are documented there. Local environments, database files, secrets, and generated files are excluded from version control.
