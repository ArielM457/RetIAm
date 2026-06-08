# Analyze AI identity risks using Microsoft Defender XDR

> Curso: Implement security for AI (wwl-implement-ai-security) · Seccion: Implement security for AI
> Duracion estimada: 19 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Financial Services has dozens of AI agents operating across its Microsoft environment. Some created by IT, others built by business units using Copilot Studio, and a few introduced by external integrations. The security team can name some of them—but not all. And when the Security Officer asks what would happen if one of those agents was compromised, the team can't answer with confidence.

What data could an attacker reach through that agent? What systems could they pivot to? Without a clear picture of each agent's blast radius and potential attack paths, the team can't prioritize which agents present the greatest risk—or know where to start remediating.

Microsoft Defender XDR extends its asset inventory to include AI agents, giving security teams a centralized view of which agents are running in their environment and what risks they represent. The AI agent inventory surfaces agent identities, their associated product sources, and the risk signals that indicate how much damage a compromised agent could cause.

### Learning objectives

In this module, you learn how to:

* Discover AI agents in Microsoft Defender XDR using the AI agent inventory
* Assess the blast radius of agent identities by examining permissions, knowledge sources, and blueprint configuration
* Analyze attack paths that could result in unauthorized access if an agent identity is compromised

### Prerequisites

Before you begin, you should have:

* Understanding of Microsoft Entra Agent ID concepts
* Familiarity with Microsoft Defender portal navigation
* Basic knowledge of identity\-based attack paths and risk assessment

---

## Discover AI agents in the Microsoft Defender portal

Organizations deploying AI agents often discover they have more agents than expected, with some created by business units outside of central IT oversight. As a security engineer at Contoso Financial Services, you need to discover all AI agents operating in your environment before you can assess their risk. Here, you learn how to use the AI agent inventory in Microsoft Defender XDR to discover agents and understand their basic properties.

### Access the AI agent inventory

Note

The AI agent inventory is currently in **Preview**. Before the inventory appears in the Defender portal, you must opt in to preview features for both Microsoft Defender XDR and Microsoft Defender for Cloud in their respective settings pages.

The AI agent inventory provides a centralized view of agents built with Microsoft Copilot Studio, Microsoft Foundry, AWS Bedrock, and GCP Vertex AI. Before you can view the inventory, you need to enable the required integrations for each platform you want to monitor.

**Licensing prerequisites:** You need either a Microsoft Agent 365 license, or both a Microsoft Defender for Cloud Apps license and a Microsoft Copilot Studio license (for Copilot Studio agent discovery).

To enable discovery, configure the integration for each platform:

* **Copilot Studio agents**: Go to **System** \> **Settings** \> **Security for AI** in the Microsoft Defender portal and turn on **Security for AI Agents**. Work with a Power Platform administrator to complete the integration in the Power Platform admin portal under **Security** \> **Threat Protection** \> **Microsoft Defender \- Copilot Studio AI Agents**.
* **Microsoft Foundry, AWS Bedrock, and GCP Vertex AI agents**: Enable the Microsoft Foundry integration in Microsoft Defender for Cloud.

Once integrations are enabled, navigate to **Assets** \> **AI Agents** in the Microsoft Defender portal. A list of all discovered agents appears, with tabs to filter by platform.

At Contoso, the security team enables the Copilot Studio integration and opens the AI agent inventory. They find 34 agents—more than the 22 they expected based on central deployment records. The other 12 agents built by business units using Copilot Studio are outside the security team's visibility. This discovery highlights why continuous monitoring matters: organizations often have more AI agents running than their central teams realize.

### Explore what the inventory shows

Each agent entry in the inventory displays key properties that help you identify and categorize agents.

| Property | Description |
| --- | --- |
| Agent name | The display name assigned when the agent was created |
| Product source | The platform where the agent was built (Microsoft Copilot Studio, Microsoft Foundry, AWS Bedrock, or GCP Vertex AI) |
| Status | Whether the agent is active, inactive, or disabled |
| Associated identities | The service principal or managed identity used by the agent |
| Last activity | The most recent time the agent was invoked or accessed resources |

The agent name and product source tell you what the agent is and where it was created. The associated identities field shows which service principal or managed identity the agent uses to authenticate—this identity is what you assess for risk.

The status field indicates whether an agent is currently active. Active agents are processing requests and accessing resources. Inactive agents can still have permissions but aren't currently being invoked. Disabled agents are intentionally turned off but retain their identity and permissions until fully removed.

Last activity provides a timestamp of the most recent agent operation. The agent operations list helps you distinguish between production agents that run frequently and experimental or abandoned agents that are never used. Agents with no recent activity but broad permissions still represent risk—a dormant agent identity is as exploitable as an active one.

### Filter and search for specific agents

When you manage dozens or hundreds of agents, filtering becomes essential. The AI agent inventory supports filtering by product source, status, and risk level. You can filter to show only Copilot Studio agents, only active agents, or only agents flagged as high risk by Defender XDR's scoring engine.

The search function lets you find agents by name or associated identity. If you know a specific business unit created an agent, search for keywords in the agent name. If you're investigating an alert that references a service principal, search by the principal's object ID to find the associated agent.

Risk level filtering is useful for prioritization. Defender XDR assigns risk scores based on the agent's permissions, knowledge sources, and configuration. Filtering to high\-risk agents lets you focus your assessment effort on the agents most likely to cause damage if compromised.

Note

Agents that don't use Microsoft Entra\-backed identities can’t appear in the inventory. Some external or custom agents authenticate using API keys or external identity providers. These agents require separate discovery methods outside Defender XDR.

### Review discovery limitations

Discovery in Defender XDR relies on process data from Microsoft services and Microsoft Entra identity activity. An agent appears in the inventory when its platform integration is enabled and the agent's identity has activity in monitored resources.

Agents built on non\-Microsoft platforms or using custom authentication mechanisms can’t be discovered automatically. If your organization uses external AI frameworks or builds custom agents with API key authentication, you need supplementary discovery methods. Defender for Cloud can help discover Azure\-hosted workloads, but agents running entirely outside Microsoft ecosystems require manual inventory processes.

At Contoso, the 34 discovered agents represent only those using Microsoft Entra identities. The security team knows they also have several custom Python agents running in Azure Container Instances that authenticate with managed identities. Those appear in the inventory. However, a legacy chatbot using an external service and API key authentication doesn't appear—it requires manual documentation and monitoring.

---

## Assess blast radius and attack paths

Discovering AI agents is only the first step in securing your environment. The real risk lies in understanding what an agent identity can access and what damage it could cause if compromised. At Contoso Financial Services, the security team identified 34 agents—now they need to assess which ones represent the greatest risk to sensitive data and critical systems. Here, you learn how to assess the blast radius of agent identities and analyze attack paths to prioritize remediation.

| Blast Radius Component | What It Measures | Risk Indicator |
| --- | --- | --- |
| Permissions | API scopes and resource access granted to the agent's service principal | Broad permissions like Mail.ReadWrite.All or Sites.FullControl.All |
| Knowledge sources | SharePoint sites, databases, or files configured as grounding data | Access to sites with sensitive labels or broad organizational content |
| Blueprint configuration | Actions the agent is designed to take (send email, create records, execute code) | Actions that can move or modify data externally |

### Understand blast radius

The **blast radius** of an agent identity is the scope of resources, data, and capabilities accessible to that identity if compromised. Unlike traditional application identities that typically access a single service, AI agents often combine broad data access (for grounding and retrieval) with action capabilities (for task execution). This combination creates larger blast radiuses than many organizations initially recognize.

Three components determine an agent's blast radius. First, **permissions** define what APIs and resources the agent's service principal can access. An agent with Microsoft Graph permissions to read all mail, files, and calendars across the tenant has a larger blast radius than one with delegated access to a single SharePoint folder. Second, **knowledge sources** specify which content repositories are available for grounding—the data the agent uses to generate responses. An agent connected to a SharePoint site containing employee performance reviews has access to sensitive HR data. Third, **blueprint configuration** determines what actions the agent can take. An agent configured to send emails, create records in external systems, or execute code can exfiltrate or modify data, expanding its blast radius beyond read\-only access.

Why does blast radius matter? Consider two agents: Agent A has read\-access to a single SharePoint folder containing public product documentation. Agent B has Mail.ReadWrite.All, Files.ReadWrite.All, and access to SharePoint sites labeled "Confidential" containing financial records. If both agents are compromised, Agent A's potential exploitation is minimal—public documentation is already accessible. Agent B's compromised identity could read, modify, or exfiltrate confidential financial data across the entire organization. Blast radius assessment lets you prioritize securing Agent B while accepting the lower risk of Agent A.

### Assess blast radius in Defender XDR

Defender XDR provides detailed visibility into each agent's blast radius. How you access this data depends on the agent's platform.

Note

For agents built with **Microsoft Foundry, AWS Bedrock, or GCP Vertex AI**, select the agent in the **Assets** \> **AI Agents** inventory to open the agent detail pane. The detail pane displays posture insights, risk factors, and security recommendations—including permissions, knowledge sources, and capabilities.

For **Microsoft Copilot Studio agents**, the AI agent inventory supports discovery only—not security posture management in the UI. To assess blast radius for Copilot Studio agents, use Advanced Hunting in the Defender portal. Navigate to **Investigation \& response** \> **Hunting** \> **Advanced hunting**, select the **Queries** tab, and choose **AI Agents** to access the prebuilt security queries that surface permission breadth, knowledge source configuration, and risky settings.

For Foundry agents, the detail pane displays three critical sections: permissions assigned to the agent's service principal, knowledge sources configured for grounding, and capabilities enabled in the agent's blueprint.

The permissions list shows all API scopes granted to the agent identity. Look for broad, tenant\-wide permissions rather than scoped or delegated permissions. Permissions like `Mail.ReadWrite.All`, `Files.ReadWrite.All`, or `Sites.FullControl.All` grant access to resources across the entire organization. In contrast, permissions like `Mail.Send` (restricted to sending only) or `Files.Read.Selected` (restricted to specific files the user has access to) represent smaller blast radiuses. The presence of multiple broad permissions significantly increases risk—an agent with both `Mail.ReadWrite.All` and `Files.ReadWrite.All` can access and exfiltrate nearly any content in the tenant.

Knowledge source assessment requires understanding both the quantity and sensitivity of connected data. The detail pane lists all SharePoint sites, databases, or file shares configured as grounding sources. For SharePoint sites, check how many sites are connected and whether they contain sensitivity labels. An agent connected to five SharePoint sites labeled "Highly Confidential" has a larger blast radius than one connected to 50 sites containing public content. Also assess whether the sites are broadly accessible or restricted—an agent accessing a restricted HR site effectively bypasses the site's access controls.

Defender XDR assigns a risk score to each agent based on permission breadth and knowledge source sensitivity. This score helps you prioritize your assessment. Agents with high risk scores warrant immediate deep\-dive analysis. Agents with low scores can still require review, but they represent less urgent risk. At Contoso, the security team sorts agents by risk score and focuses first on the top 10—these agents have combinations of broad permissions and access to confidential content.

Tip

When assessing permissions, distinguish between application permissions (granted at the tenant level) and delegated permissions (granted on behalf of a user). Application permissions typically create larger blast radiuses because they don't require user context.

### Analyze attack paths

Attack paths show how an attacker could move from a compromised agent identity to sensitive resources or privileged operations. Unlike blast radius, which describes static access scope, attack paths map dynamic exploitation scenarios—the step\-by\-step process an attacker follows to achieve their objectives.

You access attack paths from the agent detail pane by selecting **View on map**. Defender XDR generates attack paths using its knowledge of resource relationships, permission chains, and access patterns. An attack path typically starts with the agent identity as the entry point, shows intermediate steps where the attacker pivots through connected resources, and ends at a target—sensitive data, privileged accounts, or critical systems.

Reading an attack path requires understanding each step's significance. For example, an attack path might show: (1\) attacker compromises agent identity, (2\) uses agent's Mail.ReadWrite.All permission to access executive mailboxes, (3\) extracts credentials from email attachments, (4\) uses credentials to access financial database. This four\-step path demonstrates how broad permissions enable lateral movement beyond the agent's intended function.

Prioritize attack paths by criticality, not complexity. A three\-step path to customer financial records is higher priority than a seven\-step path to internal meeting notes. Focus on paths that end at sensitive data stores (databases with personal data, SharePoint sites with trade secrets), privileged operations (creating admin accounts, modifying security policies), or external exfiltration points (email, file uploads).

At Contoso, the security team analyzes attack paths for their highest\-risk agents. One Microsoft Foundry agent built for HR has SharePoint access to employee records, a Microsoft Graph permission to read all user profiles (User.Read.All), and an action configured to send emails. The attack path shows: (1\) attacker compromises agent identity, (2\) queries all employee records from SharePoint, (3\) reads sensitive user profile data including salary information, (4\) sends data to external email address using the agent's send\-mail capability. This is a three\-step path to a critical data breach involving personal data and compensation data. The security team flags this agent for immediate remediation.

### Plan remediation actions

The output of your blast radius and attack path assessment is a prioritized list of agents requiring remediation. This list drives conversations between security engineers, agent owners, and AI developers about how to reduce risk while maintaining agent functionality.

Remediation options fall into four categories. First, **remove excess permissions**. Many agents are granted broad permissions during development and never scoped down for production. Review each permission and remove any that aren't actively used. Replace broad permissions like `Sites.FullControl.All` with scoped alternatives like `Sites.Selected` that grant access only to specific sites. Second, **restrict knowledge sources**. Remove access to SharePoint sites or databases that aren't necessary for the agent's function. Apply sensitivity labels to knowledge sources and configure the agent to access only labeled content appropriate for its business purpose.

Third, **modify blueprint actions**. If an agent doesn't need to send external emails or execute code, remove those actions from its configuration. Reducing action capabilities limits what an attacker can do even if they compromise the identity. Fourth, **apply Conditional Access policies**. Configure policies that restrict agent sign\-in based on network location, device compliance, or risk level. Conditional Access provides runtime controls that complement permission and configuration changes.

At Contoso, the HR agent remediation plan includes:

* First: replacing `User.Read.All` with `User.ReadBasic.All` to limit profile data access
* Second: restricting SharePoint access to only the HR records site instead of all employee\-related sites
* Third: removing the send\-email action and replacing it with a create\-task action that queues messages for human review
* Fourth: applying a Conditional Access policy that blocks agent sign\-in from outside the corporate network. These changes reduce the agent's blast radius by 80% while maintaining its core HR support functionality.

Important

Always coordinate remediation with agent owners and business stakeholders. Removing permissions or knowledge sources without understanding agent functionality can break production workflows. Document the business justification for each permission before proposing removal.

---

## Knowledge check

Use the questions to check your knowledge and understanding.

### Check your knowledge

---

## Summary

Contoso Financial Services started this module unable to answer a basic question: if one of our AI agents were compromised, what could an attacker reach? By the end, the security team has a methodology for answering that question for every agent in their environment—and a prioritized list of agents that need immediate remediation.

### Review what you accomplished

You used the AI agent inventory in Microsoft Defender XDR to discover every AI agent operating across the Contoso environment—including 12 agents that business units created independently through Copilot Studio, none of which were on the security team's radar. The inventory provided a single view of agent names, product sources, associated identities, and initial risk signals.

From there, you assessed blast radius—the scope of resources, data, and capabilities accessible to each agent identity if compromised. By examining permissions, knowledge sources, and blueprint\-defined actions, you identified which agents could cause limited, contained damage and which could cause organization\-wide exposure. The HR agent's three\-component blast radius—employee records, all\-user profile data, and unrestricted email send capability—placed it at the top of the remediation list.

You also analyzed attack paths, following the structured paths that show how an attacker could move from a compromised agent identity to sensitive data or privileged operations. The analysis output isn't a theoretical risk model—it's a prioritized work order. Each attack path points to a specific permission, knowledge source, or action that can be removed to close it.

In this module, you learned how to:

* Discover AI agents in Microsoft Defender XDR using the AI agent inventory
* Assess the blast radius of agent identities by examining permissions, knowledge sources, and blueprint configuration
* Analyze attack paths that could result in unauthorized access if an agent identity is compromised

### What's next

You now have visibility into which agents exist and which present the greatest risk. The next step is adding real\-time protection to the highest\-risk agents operating in your environment. In the next module, you'll enable runtime protection for Copilot Studio agents using Microsoft Defender for Cloud Apps—intercepting and inspecting agent sessions in real time.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/analyze-ai-identity-risks-defender-xdr/_

## Fuentes
- [Analyze AI identity risks using Microsoft Defender XDR](https://learn.microsoft.com/en-us/training/modules/analyze-ai-identity-risks-defender-xdr/?WT.mc_id=api_CatalogApi)
