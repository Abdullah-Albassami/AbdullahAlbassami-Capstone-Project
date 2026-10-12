# Demonstration and individual technical rehearsal

**A–E functionality/audit is verified; final documentation/readiness/rehearsal still awaits F/G.** The user-observed HD-10013 lifecycle is preserved. E additionally executed 39 real Chrome checks on isolated fixtures (page/viewport/contrast/basic keyboard, workflows and guarded admin); this is distinct from human acceptance and rehearsal. Confirm instructor duration/scope, use fictional data, keep credentials out of slides/repository and demonstrate the submitted revision.

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

The user-created **HD-10013 is already resolved**. Read-only verification of the current local data shows total 13, active 8, resolved 3, cancelled 2; statuses New 3 / Assigned 3 / In progress 2 / Resolved 3 / Cancelled 2. Category backlog remains 3/2/2/1/0 and active technician workload 3/2. These are observed local values at D, not constants: future valid actions change them. Never reseed/reset to force old counts. Use a pristine separate setup for the initial 12-ticket demonstration if needed.

## Checkpoint C walkthrough available for review

Start the server using README instructions. Sign in at `/accounts/login/` as employee1 using your private runtime credential. Submit at `/tickets/new/`, optionally edit and comment while New, then use navigation's POST Sign out. Sign in as itadmin, open the saved ticket from All tickets and assign technician1. Sign out/in as technician1, open Assigned tickets, start progress, comment and supply a resolution note. Sign out/in as employee1 and read the retained resolution/discussion. A separate own New ticket can be cancelled from its confirmation page. This walkthrough is available to execute; it is not marked as a completed manual acceptance check.

The reported HD-10013 journey covers employee login/create/comment, admin assignment, technician login/visibility/start/resolve and employee dashboard Resolved. Those user-observed steps are recorded as UC01–UC07. Final read-only controls and employee outcome/thread detail were not explicitly observed; do not treat them as completed manual checks.

## Checkpoint D walkthrough available for review

As IT Admin, create a category from Categories, open its detail, edit it and delete it through confirmation while unused. Attempt to delete Hardware to see the protected-reference explanation. Dashboard shows four aggregate cards, all five statuses, category backlog and eligible technician workload; explain zero rows and the difference between assignments and availability.

On Tickets, search a known phrase in title/description, combine category/status/priority, and select Priority: high to low. Try a no-match query and a malformed status in the URL. Verify valid parameters remain across Next/Previous pages (at least 11 matching records are needed). Sign in as employee/technician to confirm own/assigned totals and category URL denial. This is a review script, not a recorded browser PASS. Tests cover these cases with controlled fixtures even when the working dataset has too few matching records for a particular pagination demo.

## Personal technical discussion

- Trace a ticket creation request: named URL → login/role guard → explicit ModelForm → actor-aware service → validated database record → redirect/detail template.
- Explain why save alone does not validate the entire model, and why request-derived requester/author are excluded from form fields.
- Explain database allowed-value/state checks versus service actor/previous-state checks.
- Explain Employee/Technician/IT Admin groups, exactly-one-role rule, and why is_staff is separate.
- Explain how per-user querysets prevent leaks in lists, detail, search and dashboard.
- Show aggregate versus annotate, active status definition and one fixture arithmetic example. Explain join inflation/zero rows.
- Explain a Django migration and prove setup without the original machine's database/configuration.
- Explain honest limitations and significant Codex/resource assistance. The student must understand the actual implementation, not memorize claims about planned code.

For remaining human review follow [MANUAL_BROWSER_CHECKS](MANUAL_BROWSER_CHECKS.md), particularly HD-10013's retained outcome/controls, full keyboard/zoom/device accessibility and guarded admin. Technician options now show Lina Demo (technician1); describe why only the label changes while IDs/eligibility remain server-enforced. E also isolates notifications across login/logout; request-method failures keep 405/Allow and provide navigation. Do not claim human checks or fresh-checkout rehearsal from the automated Chrome evidence.

## Final readiness checklist

- [ ] All required manual checks executed with actual outcomes; important automated tests passed.
- [ ] ERD matches final models/migrations and requirement matrix references actual UI/code/checks.
- [ ] Fresh checkout verified and instructions reflect commands actually run.
- [ ] Instructor repository access and presentation duration confirmed.
- [ ] Repository contains no credentials/private data/unused files.
- [ ] Demo revision matches submitted commit; core workflow rechecked.
- [ ] Student rehearsed request/relationship/validation/query explanations.
