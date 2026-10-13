# Acceptance testing

## Automated tests

A fresh installation passed **149 Django tests, 39 Chrome browser checks, and 14 HTTP checks**. Database migrations and demo-data seeding were also verified.

See the [final verification report](FINAL_VERIFICATION_REPORT.md) and [Django test suite](../tickets/tests/).

## Manual acceptance tests

**Test date:** 13 October 2026. The following scenarios were completed manually.

| ID | Status | Result |
|---|---|---|
| M01 | PASS | Resolved ticket **HD-10013** retained its note, timestamp and comments; employee1, technician1 and itadmin saw read-only details. |
| M02 | PASS | Whitespace-only ticket fields, comment and resolution note were rejected with validation feedback. |
| M03 | PASS | Case-insensitive printer search and combined filters returned expected tickets; category filter worked. |
| M04 | PASS | No-result state and invalid filter/order input displayed helpful feedback without traceback. |
| M05 | PASS | Priority ordering and ten-per-page pagination worked; invalid page inputs were handled safely. |
| M06 | PASS | Employee1 created/edited **HD-10014**; assigned edit was forbidden (403); employee2's out-of-scope views returned 404. |
| M07 | PASS | Cancellation of **HD-10015** and **HD-10014** retained ticket data, discussion/assignee as applicable and made records read-only. |
| M08 | PASS | Category create/edit/delete worked; referenced Hardware could not be deleted; unauthorized access and invalid names were rejected. |
| M09 | PASS | Dashboard and annotations matched active totals; assignment of HD-10001 updated New 3→2, Assigned 3→4 and Sami workload 2→3 while active remained 8. |
