# Capstone requirements and evidence

The [official guide](../../CapstoneProjectGuide.pdf) grades eight categories totaling **100 marks**. The mappings below show evidence, not a promised grade.

| Criterion | Marks | Evidence |
|---|---:|---|
| Problem and market | 10 | [Market potential](MARKET_POTENTIAL.md), target SMB audience, adoption proposal |
| Core functionality | 20 | Ticket workflow, cancellation, comments, category CRUD; [acceptance](ACCEPTANCE_TESTS.md) |
| Database and ORM | 20 | [ERD](ERD.md), model constraints, relationships, search, `aggregate()` and `annotate()` reports |
| Django and Python | 15 | Named URLs, views, forms, shared services, templates and permissions |
| Interface and usability | 10 | [Wireframes](WIREFRAMES.md), responsive templates, form feedback; automated Chrome checks |
| Verification and reproducibility | 10 | Fresh install, 149 tests, 39 Chrome checks, 14 HTTP checks; [verification](CHECKPOINT_G_REPORT.md) |
| Git and documentation | 5 | Versioned source, pinned dependencies, README, design and acceptance records |
| Explanation and demonstration | 10 | [Markdown presentation](CAPSTONE_PRESENTATION.md) and technical explanation |
| **Total** | **100** | Instructor determines assessment |

**Required techniques implemented:** CRUD or safe cancellation, validated forms, filtering/search, intentional sorting, pagination, relational foreign keys, protected deletion, role permissions, database constraints, aggregate totals, annotated per-category/technician counts and reproducible sample data.

**Still unverified by a human:** M10–M12 and certain additional edge cases. The instructor indicated that the Markdown presentation is sufficient in place of a live demonstration. See [acceptance record](ACCEPTANCE_TESTS.md).
