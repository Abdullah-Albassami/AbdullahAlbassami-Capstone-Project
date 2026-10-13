# HelpDesk Pro — Problem and Market Potential

**Audience:** Small and medium-sized businesses (SMBs) managing internal IT support.  
**Status:** Functional Django capstone prototype; not a production-ready commercial service.

## The problem

Requests received through emails, calls, messaging applications, and informal conversations may be difficult to track consistently. Without a shared process, support teams can lose visibility into unresolved issues, priority, ticket ownership, and resolution history. Atlassian documents standardized request submission, triage, fulfillment, and communication as established service-management practices [1]. This is workflow evidence, **not** measured SMB market demand.

## Solution and intended users

HelpDesk Pro provides a centralized, database-backed workflow:

- **Employees:** submit and follow their own support requests.
- **IT Admin:** categorize, prioritize, assign, manage categories, and monitor reports.
- **Technicians:** work on assigned requests, comment, change progress, and document resolutions.

The application implements **New → Assigned → In Progress → Resolved**, controlled cancellation, role-scoped access, search/filtering, retained comments, and category/technician workload reporting. The intended early audience is an SMB with employees across departments and a small internal IT function.

## Why choose it over ServiceNow or Jira Service Management?

Established products offer mature automation, integrations, extended ITSM functionality, and vendor support. HelpDesk Pro **does not claim parity**. The proposed differentiation is a **focused internal-ticket workflow**, potentially combined with organization-specific customization, deployment, and maintenance services. This is a hypothesis to test—not proof that the product is cheaper, better, safer, or easier to operate.

| Consideration | Established ITSM platforms | HelpDesk Pro today |
|---|---|---|
| Feature breadth | Broad and mature, depending on the platform | Core internal ticket management |
| Integrations and automation | Mature ecosystems | Limited; future work |
| Vendor track record | Established support and service operations | Educational prototype; no commercial history |
| Customization | Varies by provider/platform | Django source can be extended with development effort |
| Total cost | Plan, licensing and implementation dependent | Not measured or validated |

### Adoption risks

Before any real adoption, a business would need verified production security, backup and recovery, operational monitoring, support ownership, maintenance processes, training, and an honest total-cost comparison. Selecting an unproven vendor creates legitimate risk.

## Adoption and business model

Begin with a **small controlled organizational pilot** using defined IT-support scenarios, employee and technician feedback, and measurable criteria. Potential future revenue models include implementation/customization fees plus support agreements, or managed hosting/subscription. **No customers, interviews, pricing, cost savings, market-size estimates or revenue have been validated.**

## Evidence and limitations

Atlassian documents established service-request processes [1]; ServiceNow provides an appropriate feature-rich competitor benchmark [2]; Zendesk's reporting guidance identifies ticket/assignee measures used in support operations [3]. These are **vendor-authored industry-practice sources**, not independent proof of demand for HelpDesk Pro.

The expected benefits—clearer ticket ownership, more visible backlog, and consistent support records—remain unmeasured hypotheses.

## Next practical step

Pilot workflow usability with a small IT team, verify deployment/security/backup/support safeguards, and prioritize requirements identified by actual users. **The capstone demonstrates technical feasibility, not commercial product-market fit.**

## References

1. Atlassian, *Service Request Management: Definition & Process*. https://www.atlassian.com/itsm/service-request-management/
2. ServiceNow, *IT Service Management (ITSM)*. https://www.servicenow.com/products/itsm.html
3. Zendesk, *Understanding reports*. https://support.zendesk.com/hc/en-us/articles/4408839341082-Understanding-reports
