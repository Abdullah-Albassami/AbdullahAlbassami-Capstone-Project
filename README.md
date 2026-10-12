# HelpDesk Pro capstone repository

The Django application and its setup/design/evidence documents live in **`helpdesk-pro/`**. The official course guide and implementation specification stay at this repository root.

- [Application README and setup](helpdesk-pro/README.md)
- [Official Capstone Project Guide](CapstoneProjectGuide.pdf)
- [Implementation specification and approved user amendments](HELPDESK_PRO_CODEX_SPEC_FINAL.md)
- [Final architecture and responsibilities](helpdesk-pro/docs/DESIGN.md)
- [Checkpoint progress](helpdesk-pro/docs/PROGRESS.md)
- [Verification record](helpdesk-pro/docs/ACCEPTANCE_TESTS.md)

Checkpoint E audits and hardens the implemented application: feedback is cleared across account changes, 405 pages are helpful, technician choices show readable names/usernames, queues include requester information, and mobile confirmations/tables handle long text. **149 Django tests and 39 real headless Chrome checks pass.** Models/migrations and local demo data are unchanged. HD-10013 remains user-observed evidence; human/device/fresh-checkout/rehearsal checks are distinguished from automation. Work stops before F/G pending approval.

Start setup from `helpdesk-pro/`, following its README. The repository-wide `.gitignore` excludes local environments, credentials, databases and generated assets. No credentials or real personal data belong in the submission.

See the [Checkpoint B report](helpdesk-pro/docs/CHECKPOINT_B_REPORT.md) for file inventory, commands, actual results and remaining limitations.

See the [Checkpoint C report](helpdesk-pro/docs/CHECKPOINT_C_REPORT.md) for the ticket workflow milestone and the [Checkpoint D report](helpdesk-pro/docs/CHECKPOINT_D_REPORT.md) for the query/report milestone. These are historical records; E adds the browser verification below.

See the [Checkpoint E report](helpdesk-pro/docs/CHECKPOINT_E_REPORT.md) for current audit findings, exact verification and file inventory, and [remaining human browser checks](helpdesk-pro/docs/MANUAL_BROWSER_CHECKS.md) for reproducible instructions. Automated Chrome coverage includes emulated widths/basic keyboard/contrast; human usability, physical devices and final readiness remain pending.
