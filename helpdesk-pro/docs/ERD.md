# HelpDesk Pro — Entity Relationship Diagram (ERD)

This diagram describes the implemented relational database structure for HelpDesk Pro. It shows the four application models—**Department**, **Category**, **Ticket**, and **TicketComment**—alongside Django's built-in **User** and **Group** entities, with primary keys, foreign keys, cardinalities, and deletion behavior.

The design corresponds to [Django models](../tickets/models.py) and the [initial migration](../tickets/migrations/0001_initial.py). The [automated schema tests](../tickets/tests/test_models.py) check the implemented fields, relationships, and constraints; verification results are recorded in the [Checkpoint G report](CHECKPOINT_G_REPORT.md). Built-in authentication entities show only the fields relevant to this application's design.

```mermaid
erDiagram
    USER ||--o{ TICKET : requests
    USER |o--o{ TICKET : assigned_to
    CATEGORY ||--o{ TICKET : categorizes
    DEPARTMENT ||--o{ TICKET : requesting_department
    TICKET ||--o{ TICKET_COMMENT : contains
    USER ||--o{ TICKET_COMMENT : authors
    USER }o--o{ GROUP : built_in_membership

    USER {
        integer id PK
        varchar username UK
        varchar password "Django password hash"
        boolean is_active
        boolean is_staff
        boolean is_superuser
    }
    GROUP {
        integer id PK
        varchar name UK
    }
    CATEGORY {
        bigint id PK
        varchar name UK "required, max 100"
        text description "blank allowed"
    }
    DEPARTMENT {
        bigint id PK
        varchar name UK "required, max 100"
    }
    TICKET {
        bigint id PK
        varchar title "required, max 150"
        text description "required"
        bigint category_id FK "required, PROTECT"
        bigint department_id FK "required, PROTECT"
        integer requester_id FK "required, PROTECT"
        integer assigned_to_id FK "nullable, PROTECT"
        varchar priority "max 10, default medium"
        varchar status "max 20, default new"
        text resolution_note "blank except resolved"
        datetime created_at "auto_now_add"
        datetime updated_at "auto_now"
        datetime resolved_at "nullable except resolved"
    }
    TICKET_COMMENT {
        bigint id PK
        bigint ticket_id FK "required, CASCADE"
        integer author_id FK "required, PROTECT"
        text body "required"
        datetime created_at "auto_now_add"
    }
```

## Cardinality and optionality

| Parent | Child relationship |
| --- | --- |
| Category | Zero or more tickets; each ticket has exactly one category |
| Department | Zero or more tickets; each ticket has exactly one requesting department |
| User as requester | Zero or more tickets; each ticket has exactly one requester |
| User as assignee | Zero or more tickets; each ticket has zero or one assignee |
| Ticket | Zero or more comments; each comment has exactly one ticket |
| User as author | Zero or more comments; each comment has exactly one author |
| User/Group | Built-in many-to-many through Django's automatically managed membership table |

There is no User–Department foreign key and no custom profile or group join model. Application roles constrain eligible memberships separately from the general auth M2M cardinality.

## Integrity and rationale

Category/Department names are required and unique; FK references prevent repeated organizational names on tickets. Requester and comment author are persisted references rather than copied account data. Status and priority use choices and database allowed-value checks. Required text is trimmed and validated. Database checks cover assignment/state and resolution fields as described in [DESIGN.md](DESIGN.md).

PROTECT prevents deletion of categories, departments and users referenced by tickets/comments, including terminal history. A user referenced only as an assignee is also protected. Cancelled tickets keep their record and any assignee/comments. CASCADE describes comment cleanup if a ticket is deleted by privileged maintenance; application/admin ticket deletion is disabled. Role/eligibility changes and previous-state transitions are application rules, not cross-table database constraints.

Applied constraints: ticket_valid_status, ticket_valid_priority, ticket_assignment_matches_status and ticket_resolution_matches_status. Validation additionally trims required text, rejects null optional text for non-null columns, requires a meaningful resolution note, validates active assignee eligibility and rejects terminal/comment edits. Transitional actor authorization and lifecycle services are implemented in C; B helpers establish their permission contracts.
