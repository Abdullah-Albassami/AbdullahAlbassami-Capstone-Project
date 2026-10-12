# HelpDesk Pro capstone repository

The Django application and its setup/design/evidence documents live in **`helpdesk-pro/`**. The official course guide and implementation specification stay at this repository root.

- [Application README and setup](helpdesk-pro/README.md)
- [Official Capstone Project Guide](CapstoneProjectGuide.pdf)
- [Implementation specification and approved user amendments](HELPDESK_PRO_CODEX_SPEC_FINAL.md)
- [Final architecture and responsibilities](helpdesk-pro/docs/DESIGN.md)
- [Checkpoint progress](helpdesk-pro/docs/PROGRESS.md)
- [Verification record](helpdesk-pro/docs/ACCEPTANCE_TESTS.md)

Checkpoint C delivers application sign-in/POST sign-out, role-scoped dashboards and queues, and the complete validated ticket workflow through responsive Django templates. The existing four-model schema and seed are retained; 101 automated tests pass. Category CRUD, advanced list queries/pagination and full status/category/workload reports remain Checkpoint D. Work stops before D pending explicit approval.

Start setup from `helpdesk-pro/`, following its README. The repository-wide `.gitignore` excludes local environments, credentials, databases and generated assets. No credentials or real personal data belong in the submission.

See the [Checkpoint B report](helpdesk-pro/docs/CHECKPOINT_B_REPORT.md) for file inventory, commands, actual results and remaining limitations.

See the [Checkpoint C report](helpdesk-pro/docs/CHECKPOINT_C_REPORT.md) for the current workflow, changed files and executed verification. Real browser/mobile acceptance and final fresh-checkout rehearsal are still pending.
