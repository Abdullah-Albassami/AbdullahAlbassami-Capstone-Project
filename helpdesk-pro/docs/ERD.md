# Entity Relationship Diagram (ERD)

HelpDesk Pro uses four application models—**Department**, **Category**, **Ticket**, and **TicketComment**—alongside Django's built-in **User** and **Group** models. The diagram shows their keys, relationships, and field requirements. See the [Django models](../tickets/models.py) for the implementation.

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

## Relationships

| Relationship | Cardinality |
|---|---|
| Category → Ticket | One category to many tickets; category required |
| Department → Ticket | One department to many tickets; department required |
| User → Ticket (requester) | One user to many tickets; requester required |
| User → Ticket (assignee) | One user to many tickets; assignee optional |
| Ticket → TicketComment | One ticket to many comments |
| User → TicketComment | One author to many comments |
| User ↔ Group | Many-to-many through Django's built-in membership table |

## Data integrity

- Category and department names are unique.
- **PROTECT** prevents deletion of referenced categories, departments, and users.
- **CASCADE** removes related comments if a ticket is deleted at the database level; ticket deletion is disabled in normal application workflows.
- Database constraints validate ticket status, priority, assignment, and resolution consistency: `ticket_valid_status`, `ticket_valid_priority`, `ticket_assignment_matches_status`, and `ticket_resolution_matches_status`.
- Forms and application services validate required text, role permissions, and permitted ticket status transitions.
