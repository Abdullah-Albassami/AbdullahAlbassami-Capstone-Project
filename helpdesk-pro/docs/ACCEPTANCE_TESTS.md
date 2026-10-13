# Acceptance and verification results

**Date of owner checks:** 13 October 2026. **Status terminology:** PASS (user-observed) refers only to actions reported by the owner, not checks independently run by Codex or this assistant.

## Automated verification

An independent fresh installation passed **149 Django tests, 39 Chrome browser checks and 14 HTTP/server checks**. Migrations and repeatable fictional seed data were verified. See the [final verification report](CHECKPOINT_G_REPORT.md) and [test suite](../tickets/tests/).

## Manual acceptance

| ID | Status | Observed result |
|---|---|---|
| M01 | PASS (user-observed) | Resolved ticket **HD-10013** retained its note, timestamp and comments; employee1, technician1 and itadmin saw read-only details. |
| M02 | PASS (user-observed) | Whitespace-only ticket fields, comment and resolution note were rejected with validation feedback. |
| M03 | PASS (user-observed) | Case-insensitive printer search and combined filters returned expected tickets; category filter worked. |
| M04 | PASS (user-observed) | No-result state and invalid filter/order input displayed helpful feedback without traceback. |
| M05 | PASS (user-observed) | Priority ordering and ten-per-page pagination worked; invalid page inputs were handled safely. |
| M06 | PASS (user-observed) | Employee1 created/edited **HD-10014**; assigned edit was forbidden (403); employee2's out-of-scope views returned 404. |
| M07 | PASS (user-observed) | Cancellation of **HD-10015** and **HD-10014** retained ticket data, discussion/assignee as applicable and made records read-only. |
| M08 | PASS (user-observed) | Category create/edit/delete worked; referenced Hardware could not be deleted; unauthorized access and invalid names were rejected. |
| M09 | PASS (user-observed) | Dashboard and annotations matched active totals; assignment of HD-10001 updated New 3→2, Assigned 3→4 and Sami workload 2→3 while active remained 8. |
| M10 | NOT RUN | Extended reassignment and technician access review |
| M11 | NOT RUN | Extended guarded-admin review |
| M12 | NOT RUN | Full human mobile/zoom/keyboard usability |
| M13 | PASS (automated only) | Clean installation, migrations, repeatable seed and automated checks; no separate human repetition |
| M14 | Not required as live presentation | Instructor requested Markdown presentation; no live rehearsal claimed |

These PASS rows are limited to the stated observations. Other edge cases—including cancellation back-out, additional invalid-field variants and full accessibility review—were not fully completed manually.

## Data chronology

- **12 tickets:** deterministic fresh demo seed.
- **13 tickets:** earlier working snapshot with resolved HD-10013.
- **15 tickets:** owner-observed development snapshot after two cancellation tests, with **8 active / 3 resolved / 4 cancelled**.

These figures describe different environments/times, not conflicting seed results.

## Notes

The application was verified using fictional data. Unexecuted checks have not been presented as successful. [Final verification](CHECKPOINT_G_REPORT.md) provide context.
