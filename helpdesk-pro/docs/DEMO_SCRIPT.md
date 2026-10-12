# Demonstration and individual technical rehearsal

**Planned final demonstration; application journey not executable at Checkpoint B.** The sample database/accounts and admin setup now exist, but ticket/frontend/report pages remain later checkpoints. Confirm the instructor's duration and scope agreement. Use only fictitious data, keep passwords out of slides/repository, and demonstrate the submitted revision.

## Guide-prescribed order

1. **Users, problem and supporting context.** Introduce employees and a small IT team. Explain fragmented email/spreadsheet requests and unclear responsibility. Describe only authentic observations; label demand and efficiency benefits as unvalidated assumptions.
2. **Value and main workflow.** Employee1 submits an issue with category/requesting department/priority; shows persisted New reference in My Tickets. IT Admin assigns Technician1. Technician1 shows Assigned to Me, starts work, adds a comment and resolves with a meaningful note. Employee1 reads the saved outcome. Prefer separate browser sessions or explicit POST sign-out/sign-in.
3. **Validation/failure.** Attempt a blank required field or missing resolution note and show feedback/no invalid save. Show employee2 cannot retrieve employee1's new demonstration ticket, including a forged direct URL.
4. **Useful reports.** IT Admin displays total/active/resolved/cancelled aggregate cards, five-status breakdown, annotated category backlog and technician workload. Explain active New/Assigned/In Progress and how the demonstrated workflow changes counts. Show the unused category with zero; explain zero technician coverage in tests.
5. **Relationships and one technical decision.** Present the matching ERD. Explain requesting department belongs to the issue; requester/assignee have different User reverse relationships; category PROTECT versus ticket-comment CASCADE. Explain cancellation and read-only terminal records or the shared service authorization boundary.
6. **Market potential, limitations and next improvement.** Internal adoption without a commercial launch; clear ownership/backlog compared with email/spreadsheets. Local capstone scope excludes deployment/integrations and complete event history. A next practical improvement, after feedback, could be verified email notifications.

## Reproducibility contract

Final README must supply exact setup/configuration/migrations/seed/run/test instructions. Runtime demo password config creates employee1/employee2/technician1/technician2/itadmin without repository credentials. Seed initially supplies ticket IDs 10001–10012: total 12, active 8, resolved 2, cancelled 2; category active counts 3/2/2/1/0; technicians 3/2. Re-seeding preserves changes/passwords and is not a reset. A pristine demo requires a separate fresh local database configured through the documented setup, never a destructive reset of someone's working data.

Record the actual final demo ticket reference and submitted commit before rehearsal. Show category CRUD/cancellation separately when time permits; those are mandatory acceptance checks even if not all are narrated in the concise primary presentation.

## Personal technical discussion

- Trace a ticket creation request: named URL → login/role guard → explicit ModelForm → actor-aware service → validated database record → redirect/detail template.
- Explain why save alone does not validate the entire model, and why request-derived requester/author are excluded from form fields.
- Explain database allowed-value/state checks versus service actor/previous-state checks.
- Explain Employee/Technician/IT Admin groups, exactly-one-role rule, and why is_staff is separate.
- Explain how per-user querysets prevent leaks in lists, detail, search and dashboard.
- Show aggregate versus annotate, active status definition and one fixture arithmetic example. Explain join inflation/zero rows.
- Explain a Django migration and prove setup without the original machine's database/configuration.
- Explain honest limitations and significant Codex/resource assistance. The student must understand the actual implementation, not memorize claims about planned code.

## Final readiness checklist

- [ ] All required manual checks executed with actual outcomes; important automated tests passed.
- [ ] ERD matches final models/migrations and requirement matrix references actual UI/code/checks.
- [ ] Fresh checkout verified and instructions reflect commands actually run.
- [ ] Instructor repository access and presentation duration confirmed.
- [ ] Repository contains no credentials/private data/unused files.
- [ ] Demo revision matches submitted commit; core workflow rechecked.
- [ ] Student rehearsed request/relationship/validation/query explanations.
