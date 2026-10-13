# Capstone requirements and evidence

This table maps the eight assessment criteria in the capstone assessment to HelpDesk Pro's implementation and documentation.

| Criterion | Marks | Evidence |
|---|---:|---|
| Problem and market | 10 | [Market potential](MARKET_POTENTIAL.md), target SMB audience, adoption proposal |
| Core functionality | 20 | Ticket workflow, cancellation, comments, category CRUD; [acceptance](ACCEPTANCE_TESTS.md) |
| Database and ORM | 20 | [ERD](ERD.md), model constraints, relationships, search, `aggregate()` and `annotate()` reports |
| Django and Python | 15 | Named URLs, views, forms, shared services, templates and permissions |
| Interface and usability | 10 | [Wireframes](WIREFRAMES.md), responsive templates, form feedback; automated Chrome checks |
| Verification and reproducibility | 10 | Fresh install, 149 tests, 39 Chrome checks, 14 HTTP checks; [verification](FINAL_VERIFICATION_REPORT.md) |
| Git and documentation | 5 | Versioned source, pinned dependencies, README, design and acceptance records |
| Explanation and demonstration | 10 | [Markdown presentation](CAPSTONE_PRESENTATION.md) and technical explanation |
| **Total** | **100** | |

## Implemented techniques

CRUD operations and ticket cancellation, form validation, search and filtering, sorting, pagination, foreign-key relationships, protected deletion, role-based permissions, database constraints, aggregation, annotations, and sample data.
