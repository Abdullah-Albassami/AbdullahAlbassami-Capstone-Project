# HelpDesk Pro — Implementation scope

This document records the delivered capstone scope. The [official guide](CapstoneProjectGuide.pdf) is the authoritative assessment document.

## Product

Internal ticket management for small and medium-sized businesses, developed with Python, Django, SQLite, server-rendered templates and local CSS. The application lives in [helpdesk-pro/](helpdesk-pro/).

## Delivered requirements

- **Accounts and roles:** Employee, Technician and IT Admin, using Django's built-in User/Group system and object-level permissions.
- **Core workflow:** submit, edit when permitted, assign/reassign, start work, comment, resolve with notes and safely cancel.
- **Database:** Department, Category, Ticket, TicketComment; foreign-key relationships, deletion protection, constraints and migrations.
- **Queries:** search, filters, ordering, pagination, relationship traversals, aggregation and annotation.
- **Administration:** protected category management and guarded account/admin behavior.
- **UX:** responsive templates, forms, feedback, errors and role-specific pages.
- **Reproducibility:** pinned packages, safe environment configuration, repeatable fictional seed and automated tests.

## Out of scope

API, email notifications, attachments, enterprise SLA automation, multi-tenancy, commercial hosting and external integrations.

## Documentation and evidence

See the [application README](helpdesk-pro/README.md), [design](helpdesk-pro/docs/DESIGN.md), [ERD](helpdesk-pro/docs/ERD.md), [verification](helpdesk-pro/docs/ACCEPTANCE_TESTS.md), [market potential](helpdesk-pro/docs/MARKET_POTENTIAL.md) and [Markdown presentation](helpdesk-pro/docs/CAPSTONE_PRESENTATION.md).

Implementation and verification have been completed for the agreed capstone scope. This prototype is not represented as commercially deployed or production hardened.
