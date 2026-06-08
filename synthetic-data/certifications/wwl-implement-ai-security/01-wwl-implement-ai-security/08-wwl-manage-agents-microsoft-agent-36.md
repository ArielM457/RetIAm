# Manage agents using Microsoft Agent 365

> Curso: Implement security for AI (wwl-implement-ai-security) · Seccion: Implement security for AI
> Duracion estimada: 23 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Microsoft Agent 365 became generally available on May 1, 2026\. Contoso Financial Services holds a Microsoft 365 Copilot licensing agreement and is rolling out AI agents across its advisory, compliance, and operations teams. Department heads are already requesting agent approvals—but there's no formal process. Agents are being deployed without review, and the security team has no central view. There's no visibility of which agents are active, who approved them, or what they're accessing.

Managing AI agents at scale requires more than knowing they exist. Organizations need a way to review and approve agents before they're used. You need to apply access controls that align with organizational policies, and monitor agent activity to detect violations and enforce accountability.

Microsoft Agent 365 provides that governance layer directly in the Microsoft 365 admin center. You can enable and navigate the management interface, register agents through an approval workflow. Then you can apply usage policies and scope restrictions, and review activity data to enforce governance across your agent estate.

### Learning objectives

In this module, you learn how to:

* Enable and navigate the Microsoft Agent 365 management interface in the Microsoft 365 admin center
* Register agents and apply access controls to enforce organizational policies
* Monitor agent activity and enforce governance controls using Microsoft Agent 365

### Prerequisites

Before you begin, you should have:

* Experience administering Microsoft 365 with Microsoft 365 Copilot licensing
* Familiarity with Microsoft agent concepts and governance requirements
* Understanding of organizational AI governance policies

---

## Enable and navigate Microsoft Agent 365

Microsoft Agent 365 provides a centralized management interface for governing AI agents across your organization. At Contoso Financial Services, the IT team needs to establish oversight before allowing departments to deploy agents across advisory, compliance, and operations teams. Here, you learn how to access and navigate Microsoft Agent 365 to discover, review, and manage agents that users submit for approval.

| Management area | Purpose |
| --- | --- |
| Agent Registry | View all agents in your organization's catalog, accessible at **Agents \> All agents \> Registry** |
| Requests | Review agents awaiting administrator approval, accessible at **Agents \> All agents \> Requests** |
| All agents (Status: Available) | Manage agents currently approved and available to users |
| All agents (Status: Blocked) | View agents explicitly blocked from organizational use |

### What is Microsoft Agent 365

Microsoft Agent 365 is a governance and management layer built into Microsoft 365 that gives IT administrators centralized control over AI agents. With Agent 365, you can discover which agents exist in your organization, approve, or block agents before users interact with them. Then you can monitor agent activity to ensure compliance with organizational policies.

Microsoft Agent 365 became generally available on May 1, 2026, and requires a Microsoft 365 Copilot license. Organizations that deploy Microsoft 365 Copilot inherit Agent 365 capabilities automatically—no separate installation is required. The tight integration ensures that agent governance evolves alongside your Copilot deployment, providing consistent controls across the AI agent ecosystem.

Without Agent 365, agents built in Copilot Studio or submitted by users appear directly in the Microsoft 365 Copilot experience without administrative oversight. This creates security and compliance risks, particularly in regulated industries where data access and external integrations must be vetted before deployment.

### Access the Agent 365 management interface

To manage agents, navigate to the Microsoft 365 admin center and select **Agents** from the left navigation bar. From there, select **Overview** for the governance dashboard or **All agents** to access the Agent Registry. The Agent overview displays a snapshot of agent activity, pending requests, and governance gaps for the last 30 days.

You must hold either the **AI Administrator** role or the **Global Administrator** role to access and manage Agent 365 settings. These roles grant the permissions needed to approve, block, configure access controls, and monitor agent activity. Several roles provide view\-only access to agent data and registry information without governance authority: **AI Reader**, **Global Reader**, **Security Administrator**, **Security Reader**, and **Security Operator**. This distinction matters for security teams—your Security Operations team can monitor agent activity and view registry information to support investigations, but they can't approve agents or assign ownership. Important governance actions—such as approving agent requests or assigning agent ownership—the AI Administrator or Global Administrator perform the tasks.

If you don't see the Agents section in the admin center, verify that your organization has active Microsoft 365 Copilot licenses. Then confirm your account is assigned one of the required administrative roles. Agent name, current status (pending, active, or blocked), owner or publisher, category, and last activity timestamp. At Contoso, the Microsoft 365 administrator opens the Agents page for the first time and discovers 14 agents in pending approval status—submitted by five different department\-heads over the past two weeks, none of which were reviewed. This backlog indicates that departments are actively building agents, but without a governance process, those agents remain unapproved and unavailable to users.

### Navigate the Agent 365 interface

The Agent workload organizes management into several key areas, all accessible from **Agents** in the left navigation. The **Agent Registry** (at **Agents \> All agents \> Registry**) displays all agents in your organization's catalog—agents built in Copilot Studio, agents from external vendors your organization approved, and Microsoft\-built agents. Use Status filters to view agents by their current state: Available, Blocked, or other lifecycle states.

The **Requests** tab (at **Agents \> All agents \> Requests**) lists agents that are submitted for organizational approval but not yet reviewed by an administrator. Each pending agent shows the requestor's name, submission date, and a summary of requested capabilities. This is where you spend most of your time during initial rollout, as departments submit agents for production use. The available actions are **Publish** (approve the agent to the organization) or **Reject** (decline the submission).

Approved agents appear in the **Agent Registry** with a status of **Available**. For each available agent, you can review usage statistics, modify user scope, block access, or delete the agent if business requirements change.

Blocked agents remain in the **Agent Registry** with a status of **Blocked**. Blocking prevents an agent from being surfaced to any user in the organization. You can unblock an agent at any time, making a reversible action suitable for temporary enforcement during investigations. This view helps you maintain a record of governance decisions and ensures consistent enforcement of organizational AI policies.

---

## Register agents and apply access controls

Approving an agent makes it available to users, but effective governance requires more than binary approval decisions. At Contoso, the compliance team needs to ensure that agents requesting mailbox access are limited to specific departments, and that agents using external APIs align with the organization's approved vendor list. Here, you learn how to register agents through the approval workflow and apply granular access controls to enforce organizational policies.

### Understand the agent approval workflow

Agents arrive in Microsoft Agent 365 when users or developers build them in Copilot Studio and publish them to the Microsoft 365 tenant. Publishing triggers a submission for organizational approval, which places the agent in the **Requests** tab (**Agents \> All agents \> Requests**). Until you approve an agent, it remains unavailable to users—even the person who built it can't interact with it in the production Microsoft 365 Copilot experience.

The approval process begins when you select a pending agent to review its details. The agent detail view displays the agent's name, description, publisher/creator, and category. It displays the permissions and data access the agent requests. Common permission requests include reading mailbox items, accessing SharePoint files, querying Microsoft Graph endpoints, or connecting to external APIs through Power Platform connectors.

What approval means is important to understand: approving an agent makes it available in the Microsoft 365 Copilot experience, but it doesn't automatically grant every user access. You control which users or groups interact with the agent through user scope settings, which you configure during or after the approval process. This separation allows you to approve an agent once and then incrementally roll it out to pilot groups before enabling organization\-wide access.

### Evaluate agents against approval criteria

Before approving an agent, assess it against four key criteria. The first is **least\-privilege permissions**: does the agent request only the minimum permissions required to perform its intended function? An agent that analyzes employee survey responses needs read access to a specific SharePoint list, write access to all SharePoint sites is unneeded. If an agent requests broader permissions than its description justifies, return it to the publisher with feedback requesting clarification or a scope reduction.

The second criterion is **trusted publisher**. Agents built by your organization's employees in Copilot Studio display the creator's email address. Agents published by external vendors display the vendor's organizational identity. Verify that external publishers align with your organization's approved software vendor list. If a department submits an agent from an unknown publisher, investigate the vendor's security posture and data handling practices before approval.

The third criterion is **clear business purpose**. Every agent should solve a specific problem or automate a defined task. Vague descriptions like "helps with productivity" or "analyzes data" don't provide enough context to evaluate risk. Require submitters to document the business process the agent supports, the data it accesses, and the expected user base. This documentation becomes part of your governance record and supports audit reviews.

The fourth criterion is **compliance with organizational AI policy**. If your organization maintains policies governing AI usage—such as restrictions on processing personal data, requirements for human oversight of AI\-generated decisions, or prohibitions on certain types of automated decision\-making—verify that the agent aligns with those policies. Agents that don't comply should be blocked, not left unapproved.

### Configure user scope and access controls

User scope determines which users or groups in your organization can discover and interact with an approved agent. By default, most agents default to organization\-wide access, but you should limit scope to the smallest appropriate audience—particularly during initial rollout. To configure user scope, select an approved agent, choose **Manage access**, and specify either individual users or Microsoft 365 groups.

Limiting scope to specific departments reduces risk in two ways. First, it contains the challenges of any agent misconfiguration or unexpected behavior to a smaller user base. If an agent inadvertently exposes sensitive data or produces incorrect outputs, fewer users are affected. Second, it aligns with the principle of least privilege: only users who need the agent to perform their job should have access to it.

Beyond user scope, review the Power Platform connectors the agent uses. Agents built in Copilot Studio use on\-behalf\-of (OBO) authentication by default—the agent acts using the signed\-in user's identity and permissions, not a separate service account. Actions appear in audit logs as performed by the user, with agent context recorded for compliance. This means a user's existing permissions form the effective ceiling for what the agent can access, which is why least\-privilege user permissions matter as much as least\-privilege agent permissions. If your organization enforces Data Loss Prevention (DLP) policies on Power Platform connectors, verify that the agent's connectors comply with those policies. For example, if your DLP policy classifies SharePoint as a business\-use connector and Dropbox as a nonbusiness connector. Then the agent that moves files between SharePoint and Dropbox violates the policy and should be blocked until the publisher redesigns the workflow.

External data access presents another governance consideration. Some agents query data outside the Microsoft 365 tenant—external APIs, on\-premises databases accessed through on\-premises data gateways, or public internet sources. Assess whether the agent's external data access aligns with your organization's data residency and sovereignty requirements. If your organization prohibits storing customer data outside specific geographic regions, an agent that sends data to an external API hosted in a noncompliant region should be blocked.

| Access control | Purpose | Configuration location |
| --- | --- | --- |
| User scope | Limit which users or groups can interact with the agent | Agent settings \> Manage access |
| Connector permissions | Ensure connectors comply with organizational DLP policies | Power Platform admin center \> Data policies |
| External data access | Verify data residency and sovereignty compliance | Agent detail view \> Permissions \& data access |

### Block agents that don't meet governance standards

When an agent doesn't meet approval criteria, you have two options: return it to the submitter with feedback, or block it outright. Returning with feedback is appropriate when the agent has a valid business purpose but requires minor adjustments—such as reducing permission scope or clarifying its description. Blocking is appropriate when the agent violates organizational policy or presents unacceptable risk.

Blocking prevents the agent from being surfaced to any user in the organization, even if the submitter modifies and resubmits it. Blocked agents appear in the **Blocked agents** view with the reason for blocking and the administrator who made the decision. This creates an audit trail that supports consistent governance enforcement and helps you explain decisions during compliance reviews.

At Contoso, the Microsoft 365 administrator reviews the 14 pending agents. Ten agents are approved with user scope limited to the requesting department—agents for document summarization, meeting follow\-up automation, and compliance policy lookup. Three agents are blocked: requests read access to all mailboxes without a justified business need, one connects to an external API that isn't on the approved vendor list, and one duplicates the functionality of an already\-approved agent. The final agent is returned to the submitter with feedback requesting clarification on how long the agent retains customer data, as the current description doesn't address the organization's data retention policy.

---

## Monitor agent activity and enforce governance

Agent governance doesn't stop after approval—it's an ongoing cycle of monitoring, reviewing, and remediating as usage patterns evolve. At Contoso, three months after deploying Microsoft Agent 365, the compliance team's document analysis agent shows usage spikes every Sunday night that weren't part of the original approval scope. Here, you learn how to monitor agent activity and enforce governance controls to ensure agents remain aligned with organizational policies over time.

| Monitoring focus | Key indicator | Governance action |
| --- | --- | --- |
| Anomalous usage | 500% increase over baseline | Investigate for automation or misuse |
| Inactive agents | Zero interactions for 60\+ days | Review for decommissioning |
| Policy violations | Data Loss Prevention (DLP) alerts or unauthorized access attempts | Block agent pending investigation |

### Monitor agent activity in Microsoft Agent 365

Microsoft Agent 365 tracks key activity metrics for every approved agent, including interaction volumes, active user counts, and usage trends over time. To view activity data, navigate to the **Agents** page, select an agent, and open the **Usage** or **Activity** tab. The usage view displays total interactions since approval, the number of unique users who interacted with the agent, and a time\-series chart showing interactions per day over the past 30 days.

Risk signals—such as policy violations flagged by Microsoft Entra, Defender, or Purview—are aggregated into the Agent overview's **Agents at risk** card, giving you a single place to identify and act on cross\-platform governance signals.

A closely related governance card is **Agents without owners**. When the person who created or submitted an agent leaves the organization, that agent becomes ownerless—there's no longer a designated person responsible for its lifecycle, compliance, or ongoing maintenance. The Agent overview surfaces ownerless agents as an actionable governance gap. Assigning an owner to each agent ensures accountability and prevents approved agents from persisting in production without anyone responsible for reviewing them during governance cycles.

These metrics help you identify patterns that indicate successful adoption or potential problems. An agent with steadily increasing interactions and expanding user adoption likely delivers value and operates within its intended scope. An agent with erratic usage patterns—such as thousands of interactions in a single day followed by weeks of inactivity—can indicate automation, misuse, or a business process that no longer requires the agent.

Peak usage times also provide governance insights. If an agent designed for interactive user assistance shows most of its activity between midnight and 6:00 AM, someone can be using it in a batch automation workflow rather than the intended ad\-hoc query scenario. This doesn't automatically mean the usage is inappropriate, but it signals a need to verify that the actual use case aligns with the approved purpose.

### Identify anomalous usage and governance risks

Anomalous usage often indicates changes in how users interact with an agent or unexpected adoption beyond the original scope. An agent with 500 percent more interactions than its 30\-day baseline could indicate successful viral adoption within a department, integration into an automated workflow, or misuse by a few power users. Each scenario has different governance implications.

To investigate anomalous usage, compare the unique user count to total interactions. If an agent shows 10,000 interactions but only five unique users, a small group is generating most of the activity. Review whether those users are using the agent as intended or whether they integrated it into processes that weren't part of the approval scope. If the usage aligns with organizational policies, update the agent's documentation to reflect the new use case. If it doesn't, block the agent and work with the users to modify their workflow.

Unused agents present a different risk. Agents with zero interactions for 60 or more days should be reviewed for decommissioning. Inactive agents still consume license resources, appear in the agent catalog where they create clutter, and expand your organization's attack surface. When you add in the fact the agent's permissions or connectors aren't actively monitored, there could be more challenges. During quarterly governance reviews, filter for agents with no recent activity. Work with the original submitters to determine whether to decommission the agents or whether they serve a seasonal business need.

### Enforce governance through remediation actions

When monitoring reveals that an agent no longer meets governance standards, Microsoft Agent 365 provides several enforcement actions. **Blocking an agent** removes it from user access immediately—no user in the organization can interact with the blocked agent. Blocking is reversible: select **Unblock** at any time to restore access. Use block during investigations—such as when an agent triggers Data Loss Prevention policy alerts and you need time to determine whether the alerts indicate legitimate usage or policy violations—then unblock once the investigation is resolved.

**Updating user scope** allows you to narrow the audience for an agent that expanded beyond its intended user base. If you approved an agent for a 20\-person pilot group and discover through monitoring that 200 users now have access because the pilot group expanded into a distribution list, reduce the scope back to the original intended audience. Alternatively, work with stakeholders to justify the broader rollout and update the approval documentation.

**Revoking approval** moves an agent back to pending status, requiring a new approval before users can access it again. Revocation is appropriate when an agent's publisher updates the agent and adds new permissions or data connections that weren't part of the original approval. Some agent platforms notify administrators when published agents change, but monitoring activity patterns can also reveal functional changes—such as an agent that suddenly starts accessing SharePoint sites it didn't query during the first 90 days of deployment.

### Establish a continuous governance cycle

Effective agent governance follows a repeating cycle: approve based on initial criteria, monitor for changes in usage or risk, review agents against current policies, and remediate when deviations occur. This cycle ensures that agents approved six months ago under one set of business requirements don't persist unchanged when those requirements evolve.

Set a governance cadence that matches your organization's risk tolerance and regulatory requirements. A monthly review of usage anomalies catches unexpected changes quickly. A quarterly review of all active agents against current organizational policies ensures that older agents remain compliant as your AI governance framework matures. An annual reapproval process for high\-access agents—those with broad permission scopes or access to sensitive data—provides a formal checkpoint to verify that business justification remains valid.

At Contoso, the Sunday night usage spikes in the compliance team's document analysis agent prompt an investigation. The compliance team explains that they integrated the agent into a weekend batch process that analyzes regulatory filings submitted during the week. This workflow wasn't included in the original approval request, which described the agent as an interactive tool for ad\-hoc policy research. The Microsoft 365 administrator blocks the agent, reviews the batch processing workflow with the compliance team to ensure it aligns with data retention policies. Then it unblocks the agent with updated approval documentation reflecting the expanded scope.

---

## Summary

Contoso Financial Services launched Microsoft Agent 365 into a situation where 14 agents were sitting in an approval queue. The department heads were deploying agents without review, and the security team had no central view of what agents were active or what they were doing. Three months after rollout, the governance process is operational, the agent catalog is reviewed and documented, and an anomalous Sunday\-night usage pattern indicated a policy violation was caught, investigated, and addressed.

### Review what you accomplished

You enabled Microsoft Agent 365 by navigating to **Agents** in the Microsoft 365 admin center, and explored the management interface—the Agent Registry, Requests tab, and the Available and Blocked status views within All agents. You identified the role requirements (AI Administrator or Global Administrator) and confirmed that a Microsoft 365 Copilot license is required.

You worked through the agent approval process, reviewing each pending agent against evaluation criteria: least\-privilege permissions, trusted publisher, clear business purpose, and compliance with organizational policy. You applied user scope restrictions to limit approved agents to the requesting department rather than all users, reviewed connector permissions for alignment with Power Platform Data Loss Protection (DLP) policies, and documented blocking decisions with reasons to support consistent governance. Of Contoso's 14 pending agents, 10 were approved, 3 were blocked with documented justification, and 1 was returned for clarification.

You used the activity monitoring capabilities in Agent 365 to review interaction volumes and identify usage anomalies. You explored the enforcement actions available like blocking an agent during investigation, narrowing user scope as adoption expands beyond intent, and revoking approval when agents no longer meet policy requirements. The governance cycle you established (approve, monitor, review, remediate) provides a repeatable framework for managing the agent estate as it grows.

In this module, you learned how to:

* Enable and navigate the Microsoft Agent 365 management interface in the Microsoft 365 admin center
* Register agents and apply access controls to enforce organizational policies
* Monitor agent activity and enforce governance controls using Microsoft Agent 365

### Apply your learning

You now have the tools to govern AI agents across your organization's Microsoft 365 environment. As agent adoption grows, the discipline of consistent approval criteria, documented blocking decisions, and regular activity review will determine whether your AI security posture strengthens or erodes over time.

Tip

To explore Microsoft Agent 365 capabilities and governance workflows in depth, see [Microsoft Agent 365 overview](/en-us/microsoft-agent-365/overview).

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/manage-agents-microsoft-agent-365/_

## Fuentes
- [Manage agents using Microsoft Agent 365](https://learn.microsoft.com/en-us/training/modules/manage-agents-microsoft-agent-365/?WT.mc_id=api_CatalogApi)
