# Enable real-time protection for Copilot Studio agents

> Curso: Implement security for AI (wwl-implement-ai-security) · Seccion: Implement security for AI
> Duracion estimada: 25 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Financial Services' development team deployed several Copilot Studio agents to handle client\-facing interactions and internal data queries. These agents interact with sensitive financial data through Power Platform connectors, and some are accessible externally. The security team has one key concern: if an agent behaves unexpectedly—from prompt injection, a misconfigured connector, or a compromised user session—do they know? And do records exist to investigate?

Real\-time runtime protection for Copilot Studio agents answers that question. Microsoft Defender for Cloud Apps provides three layers of capability for agent protection: discovery and hunting to find agents across your environment, audit, and alerts to capture agent activity. Then you have surface policy violations, and real\-time protection to inspect and intercept agent interactions as they happen.

Enabling that protection requires coordinating across two administrative surfaces—the Microsoft Defender portal and the Power Platform admin center. This module walks you through that configuration, shows you what to verify after setup, and explains what outputs to expect in Microsoft Defender XDR.

### Learning objectives

In this module, you learn how to:

* Describe the AI agent protection capabilities available in Microsoft Defender for Cloud Apps
* Enable real\-time protection for Copilot Studio agents in the Microsoft Defender portal
* Verify that agent protection outputs appear in the Microsoft Defender XDR inventory, alerts, and Advanced Hunting

### Prerequisites

Before you begin, you should have:

* Familiarity with Microsoft Copilot Studio and agent development concepts
* Experience with Microsoft Defender portal administration
* Understanding of Microsoft Defender for Cloud Apps capabilities
* One of the following licenses: a **Microsoft Agent 365** license, or both a **Microsoft Defender for Cloud Apps** license and a **Microsoft Copilot Studio** license
* Preview features enabled for both **Microsoft Defender for Cloud** and **Microsoft Defender XDR** in your tenant

---

## Explore Copilot Studio AI agent protection

Organizations deploy Copilot Studio agents to automate interactions and provide self\-service capabilities. As these agents access sensitive data sources and perform actions on behalf of users, they become attractive targets for attackers. The attackers attempt prompt injection, data exfiltration, and privilege escalation. Microsoft Defender for Cloud Apps provides comprehensive AI agent protection to detect, monitor, and block threats against Copilot Studio agents. Here, you explore the three capability pillars that protect your organization's AI agents from emerging threats.

Note

AI agent protection for Microsoft Copilot Studio is currently in **Preview**. Preview availability and feature scope can vary by tenant. Verify that preview features are enabled for Microsoft Defender for Cloud and Microsoft Defender XDR before following the configuration steps in this module.

| Capability | Purpose | Output |
| --- | --- | --- |
| Discovery and hunting | Automatically identifies all Copilot Studio agents and their risk exposure | AI agent inventory with connectors, data sources, and risk signals |
| Audit and alerts | Monitors agent activity and detects policy violations | Alerts integrated into Microsoft Defender XDR incidents |
| Real\-time runtime protection | Inspects and blocks suspicious interactions before they complete | Immediate threat blocking with detailed incident data |

### Discover agents and assess exposure

Microsoft Defender automatically discovers all Copilot Studio custom agents deployed across your Power Platform environment. The discovery process requires no manual registration—once you enable Security for AI in the Defender portal, the system identifies agents, catalogs their connectors, and maps the data sources they access.

The AI agent inventory provides security teams with visibility into agent deployment patterns and risk exposure. For each discovered agent, you see which SharePoint libraries, Dataverse tables, or external APIs the agent connects to. This visibility is essential for identifying agents that access sensitive data without appropriate controls.

Advanced Hunting extends this visibility with queryable agent activity data. Security analysts use KQL queries to search for suspicious patterns across all agent interactions, such as repeated access to sensitive files or unusual tool invocations outside normal business hours.

### Monitor activity with audit logs and alerts

After discovery, Defender for Cloud Apps continuously monitors agent activity through audit logs collected from Copilot Studio. The system analyzes these logs for suspicious patterns and policy violations, generating alerts when threats are detected.

Detected threats include prompt injection attempts, where attackers craft inputs designed to manipulate the agent into performing unintended actions. The system also identifies data exfiltration patterns, such as an agent retrieving large volumes of sensitive content in response to external user requests.

These alerts don't exist in isolation. Defender for Cloud Apps correlates AI agent alerts into Microsoft Defender XDR incidents, combining them with related security signals from identity, endpoint, and cloud workload protection. This correlation gives security teams complete context when investigating potential compromises.

### Block threats with real\-time runtime protection

Real\-time runtime protection represents the most advanced layer of defense. When enabled, Defender for Cloud Apps acts as a proxy for agent interactions, inspecting tool invocations before the agent executes them.

With real\-time protection, Defender evaluates each tool invocation against threat intelligence and behavioral analytics. If the system determines that a tool invocation is suspicious—for example, accessing a data source that violates organizational policy—the invocation is blocked before it executes. The user receives notification that their message was blocked, and an alert flows to the Microsoft Defender portal for investigation.

Real\-time protection focuses on high\-confidence threats most likely to result in data exfiltration or agent compromise:

* Attempts to extract or exfiltrate system instructions or internal tool details
* Direct attempts to leak sensitive data through agent responses
* Misuse of internal\-only tools by external users
* Routing agent output to untrusted or malicious external destinations
* Use of obfuscated or hidden content designed to manipulate agent behavior
* Credential leakage through legitimate channels such as email or external APIs

This capability requires explicit configuration and coordination between security engineers and Power Platform administrators. The setup process registers the agent in the Defender portal and establishes the proxy connection that enables real\-time inspection.

### Explore agent identity and Microsoft Entra Agent IDs

Every Copilot Studio agent has its own identity in Microsoft Entra ID. Copilot Studio creates and manages this identity automatically—you don't configure it manually. For agents created after March 18, 2026 (when your tenant opts in to Microsoft Entra Agent Identity), this identity is an **Entra Agent ID**: a Microsoft Entra service principal with an "Agent" subtype. Agents created before that date use a legacy app registration instead.

Microsoft Entra Agent IDs unlock governance capabilities that legacy app registrations don't provide: Conditional Access policies scoped to individual agent identities, centralized audit logging in the Microsoft Entra admin center, and lifecycle management aligned with organizational policies. For security engineers working toward a Zero Trust posture, this means AI agents can be managed with the same rigor applied to users and workload identities. You can find an agent's Microsoft Entra Agent ID in Copilot Studio under **Settings** \> **Advanced** \> **Metadata**.

This agent identity is distinct from the App ID you configure during real\-time protection setup. The proxy App ID—exchanged between the Microsoft Defender portal and the Power Platform admin center—identifies the trusted connection that allows Defender to inspect agent traffic. It doesn't represent the agent's own Microsoft Entra identity.

### Distinguish Defender for Cloud Apps from Defender for Cloud AI threat protection

Microsoft Defender for Cloud Apps protects **Copilot Studio agents** at the session and interaction layer—inspecting tool invocations, blocking suspicious prompts, and surfacing alerts in the Defender XDR incident queue.

A separate Cloud Workload Protection plan \- **Defender for AI Services** in Microsoft Defender for Cloud—protects **Azure AI services workloads** (Azure OpenAI and Azure AI Model Inference service) at the Azure subscription layer. You enable it by toggling the **AI services** plan to **On** in **Defender for Cloud** \> **Environment settings** for the relevant subscription. Once enabled, it scans text tokens flowing through your AI services and generates security alerts for jailbreak attempts, data leakage, credential theft, and data poisoning. These alerts also integrate into Defender XDR, so your SOC team sees both Copilot Studio and Azure AI threats in a single incident queue.

The two capabilities protect different surfaces:

| Capability | What it protects | Where you enable it |
| --- | --- | --- |
| **Defender for Cloud Apps—AI agent protection** | Copilot Studio agent sessions and tool invocations | Microsoft Defender portal \> System \> Settings \> Security for AI |
| **Defender for Cloud—AI services plan** | Azure AI services workloads (Azure OpenAI, AI Model Inference) | Azure portal \> Defender for Cloud \> Environment settings \> AI services toggle |

If your organization uses both Copilot Studio agents and Azure AI services, you need both capabilities enabled to get full coverage. Enabling one doesn't activate the other.

Note

Enabling the Defender for Cloud AI services plan is covered in a separate module. This module focuses exclusively on Copilot Studio agent protection through Defender for Cloud Apps.

### Apply protection to Contoso's scenario

Contoso Financial Services deployed a Copilot Studio agent to handle common customer inquiries about account balances and transaction history. During initial discovery, Contoso's security team found that the agent is granted access to a SharePoint library containing unclassified but sensitive deal information—access that wasn't required for the agent's customer service function.

The discovery capability surfaced this misconfiguration. With audit logs and alerts enabled, the team received notifications whenever the agent accessed the sensitive library. After admins enable real\-time runtime protection and implementing appropriate policies, Defender now blocks any attempt by the agent to retrieve content from that library, preventing potential data exposure to external users.

Real\-time protection gives Contoso proactive defense against emerging threats while maintaining the agent's legitimate functionality for customer service interactions.

---

## Enable protection in Microsoft Defender

Real\-time protection for Copilot Studio agents requires configuration in both the Microsoft Defender portal and the Power Platform admin center. Security engineers can't complete setup alone—the process demands coordination with Power Platform administrators who manage the environment where agents run. Here, you learn the step\-by\-step process to enable real\-time protection and verify that the configuration is complete.

### Navigate to Security for AI settings

The configuration process begins in the Microsoft Defender portal. Navigate to **System** \> **Settings** \> **Security for AI agents**. This settings page controls all AI agent protection capabilities, including the AI agent inventory, audit logging, and real\-time runtime protection.

Note

The settings page can appear as **Security for AI** or **Security for AI agents** depending on your portal version. Both paths open the same configuration page.

Before configuring real\-time protection, verify that the **Microsoft 365 app connector** shows a connected status. The Microsoft 365 connector is required for audit logs and alerts to flow into the Defender portal. If the connector isn't connected, real\-time protection continues to block suspicious activity, but alerts and incidents related to those blocks don't appear in the Microsoft Defender XDR incident queue.

To enable the Microsoft 365 connector, select **Connect Microsoft 365** from the app connectors page and follow the authentication prompts. The connector requires global administrator or security administrator permissions to establish.

### Enable Security for AI agents

On the Security for AI settings page, locate the **Security for AI Agents** toggle. Turn on this toggle to enable the discovery and monitoring capabilities that form the foundation for real\-time protection.

Enabling Security for AI Agents confirms that you read the disclaimer and agree to use Microsoft Defender AI agent protection features. This setting activates the automatic discovery process that identifies all Copilot Studio custom agents in your tenant.

The discovery process runs continuously after enablement. Within 30 minutes of turning on this toggle, the AI agent inventory begins populating with discovered agents, their associated connectors, and the data sources they access.

### Configure real\-time protection during agent runtime

With Security for AI Agents enabled, you're ready to configure real\-time protection. In the **Real time protection during agent runtime** section on the same settings page, select the option to enable real\-time protection.

The portal provides a URL that you share with the Power Platform administrator. This URL contains the configuration endpoint that the Power Platform admin center uses to establish the proxy connection between Copilot Studio and Microsoft Defender.

The configuration requires an **App ID** that identifies the Microsoft Entra ID application used for the proxy connection. This App ID must match across both the Defender portal and the Power Platform admin center configuration.

Note

This proxy App ID represents the trusted connection between Power Platform and Microsoft Defender—it's separate from the Microsoft Entra Agent ID that Copilot Studio automatically creates for each agent's own channel authentication. You're configuring the inspection layer, not the agent's identity.

| Configuration step | Responsible role | Location |
| --- | --- | --- |
| Share Defender URL with Power Platform admin | Security Engineer | Microsoft Defender portal \> System \> Settings \> Security for AI |
| Configure threat detection endpoint | Power Platform Administrator | Power Platform admin center \> Security \> Threat Protection |
| Provide App ID to security engineer | Power Platform Administrator | Power Platform admin center configuration output |
| Enter App ID in Defender portal | Security Engineer | Microsoft Defender portal \> System \> Settings \> Security for AI |

### Coordinate with Power Platform administration

The Power Platform administrator completes their portion of the configuration in the Power Platform admin center. They navigate to **Security** \> **Threat Protection**, then select **Microsoft Defender \- Copilot Studio AI Agents**.

The Power Platform admin turns on **Enable Microsoft Defender \- Copilot Studio AI Agents** and enters the URL you provided from the Defender portal. During this process, they create or select a Microsoft Entra ID application that represents the trusted connection between Power Platform and Defender.

This Microsoft Entra ID application generates an App ID. The Power Platform administrator shares this App ID with you. You can complete the configuration in the Defender portal.

After the security expert receives the App ID from the Power Platform admin, return to the Microsoft Defender portal and enter the App ID in the designated field on the Security for AI settings page. Select **Save** to apply the configuration.

Note

If you recently changed the App ID in Power Platform, it can take up to one minute for the update to propagate across all portals. If you encounter a validation error when saving the updated value, wait a short time and try again.

### Verify connected status

After Contoso saves the App ID configuration, the **Real time protection during agent runtime** section displays a connection status indicator. When configuration is complete and the proxy connection is established, a green **Connected** status appears.

The connected status confirms that:

* The Microsoft Entra ID application configuration matches between Defender and Power Platform
* The proxy endpoint is reachable and authenticated
* Agent interactions now pass through Microsoft Defender for real\-time inspection

If the status shows **Disconnected** or **Pending**, the Power Platform administrator portion of the setup is incomplete or the App ID entered in the Defender portal doesn't match the App ID configured in Power Platform. Return to the Power Platform admin center to verify the configuration.

### Understand protection behavior after enablement

With real\-time protection enabled and showing connected status, Defender for Cloud Apps begins inspecting tool invocations from protected agents. Each time an agent attempts to execute a tool—such as retrieving data from SharePoint or querying Dataverse—Defender evaluates the invocation against threat policies and behavioral analytics.

Suspicious invocations are blocked before they execute. The user who triggered the interaction receives a message indicating that their request was blocked for security reasons. Simultaneously, an alert is created in the Microsoft Defender portal under **Incidents \& alerts**, where security teams can investigate the context and determine whether the block was appropriate.

Real\-time protection introduces a proxy layer into agent interactions. While latency is typically minimal, you should communicate this architectural change to agent owners and monitor performance after enabling protection to ensure acceptable user experience.

Existing agent sessions can’t immediately reflect protection status. Real\-time protection applies to new sessions initiated after the configuration is complete. Users who have active conversations with an agent often need to restart their session for protection to take effect.

### Apply enablement to Contoso's scenario

Contoso Financial Services identified their customer service agent as a high\-priority candidate for real\-time protection. The security engineer navigated to the Microsoft Defender portal and enabled Security for AI Agents, then configured the real\-time protection settings.

The security engineer shared the Defender URL with Contoso's Power Platform administrator. The Power Platform admin completed the threat detection configuration in the Power Platform admin center and provided the App ID back to the security engineer.

After entering the App ID in the Defender portal and saving the configuration, the connection status changed to green **Connected** within minutes. Contoso's customer service agent is now protected—any attempt to retrieve content from the sensitive SharePoint library identified during discovery is blocked before the agent executes the retrieval, and an alert is created for the security team to investigate.

The protection is now active and monitoring all interactions with the customer service agent in real time.

---

## Review AI agent protection outputs

After enabling real\-time protection for Copilot Studio agents, you verify that the protection is active by reviewing outputs in three key areas of the Microsoft Defender portal. These outputs confirm that agent discovery is complete, alerts are flowing into the incident queue, and interaction data is available for threat hunting. Here, you learn how to verify each output area and confirm that protection is functioning end\-to\-end.

### Verify agent inventory in AI assets

The AI agent inventory provides the first confirmation that discovery and protection are active. Navigate to **Assets** \> **AI assets** in the Microsoft Defender portal. This inventory displays all discovered Copilot Studio agents across your Power Platform environment.

Note

The navigation label appears as **AI assets** or **AI Agents** depending on your Defender portal version. Both paths open the same AI agent inventory.

For each protected agent, the inventory shows:

* **Agent name** and the environment where it's deployed
* **Connection status**—Connected indicates real\-time protection is active
* **Associated connectors**—SharePoint, Dataverse, external APIs, and other data sources
* **Risk signals**—Access to sensitive data, external exposure, or policy violations

The protected agent you configured in the previous unit should appear in this inventory with **Connected** status. If the agent shows **Disconnected**, return to the Security for AI settings to verify that the Power Platform administrator completed their configuration steps and that the App ID matches across both portals.

The inventory also lists the data sources each agent accesses. Verify that the agent's connectors align with your security policies. For example, if the agent is intended for external customer interactions, it shouldn't have access to internal SharePoint libraries containing confidential business data.

Agent makers can also verify protection status directly inside Copilot Studio without accessing the Defender portal. On the **Agents** page in Copilot Studio, a **Protection status** column shows one of three values for each published agent:

| Status | Meaning |
| --- | --- |
| **Protected** (green shield) | Threat detection is active and no policy violations detected |
| **Needs review** | Agent policies are violated or authentication is inadequate |
| **Unknown** | Protection status can't be determined |

This maker\-visible status gives agent builders immediate feedback on protection health and surfaces issues—such as inadequate authentication or policy violations—that security engineers want to investigate.

### Review alerts and incidents in Defender XDR

Real\-time protection generates alerts when suspicious interactions are blocked or when agent activity violates organizational policies. These alerts correlate into Microsoft Defender XDR incidents, giving security teams full context for investigation.

Navigate to **Incidents \& alerts** \> **Incidents** in the Microsoft Defender portal. Filter for incidents related to AI agents or Defender for Cloud Apps to see agent\-related security events.

Each incident includes:

* The alert title and severity level
* The agent that triggered the alert
* The user or entity that initiated the interaction
* The blocked or suspicious action that generated the alert
* Related security signals from identity, endpoints, or cloud apps

Note

If you don't see AI agent alerts immediately after enabling protection, a delay is expected. Alerts are generated when suspicious activity occurs or policies are violated. You need to wait for agent activity to trigger detections, or you can generate a test interaction to verify alert flow.

When reviewing incidents, look for alert categories specific to AI agents:

| Alert category | Description | Example scenario |
| --- | --- | --- |
| Prompt injection detected | User input contains patterns consistent with prompt manipulation | External user attempts to override agent instructions with crafted prompts |
| Data exfiltration risk | Agent retrieves large volumes of sensitive content | Agent accesses more than 100 files from a confidential SharePoint library |
| Policy violation | Agent action violates organizational security policy | Agent attempts to execute a blocked connector or access restricted data |

These alerts confirm that Defender is actively monitoring and blocking threats in real time.

### Query Advanced Hunting for interaction data

Advanced Hunting provides the most granular view of agent activity. Navigate to **Hunting** \> **Advanced Hunting** in the Microsoft Defender portal to access the query editor.

Agent interaction data appears in dedicated Advanced Hunting tables that log every tool invocation, data retrieval, and user interaction. Use KQL queries to search this data for suspicious patterns, compliance verification, or threat investigation.

Run this sample query to verify that agent interaction data is flowing:

```
CloudAppEvents
| where Application == "Microsoft Copilot Studio"
| where Timestamp > ago(1h)
| project Timestamp, AccountDisplayName, ActivityType, ActivityObjects
| take 10

```

This query uses the `CloudAppEvents` table, which captures Agent 365 observability data including Copilot Studio agent actions, tool invocations, and data access events routed through the Microsoft 365 app connector.

For agent inventory and posture queries, use the companion `AIAgentsInfo` table, which contains configuration details for each discovered agent—including its name, tools, knowledge sources, authentication settings, and whether it's blocked by an administrator. For example:

```
AIAgentsInfo
| summarize arg_max(Timestamp, *) by AIAgentId
| project AIAgentName, Platform, CreatorAccountUpn, AgentToolsDetails, IsBlocked

```

Use `CloudAppEvents` to investigate what an agent *did* at runtime, and `AIAgentsInfo` to assess how an agent is *configured* and whether it represents a posture risk.

If the `CloudAppEvents` query returns results, protection is active and logging agent interactions. If the query returns no results, verify that:

* Sufficient time passed since enabling protection (allow at least 30 minutes for initial data ingestion)
* The agent received user interactions that generate activity logs
* The Microsoft 365 app connector is connected in the Defender portal

Advanced Hunting enables proactive threat detection beyond automated alerts. Security teams create custom queries to identify emerging patterns such as:

* Agents accessing sensitive data sources outside normal business hours
* Repeated failed authentication attempts to agent\-connected resources
* Unusual tool invocation sequences that indicate reconnaissance

### Confirm end\-to\-end protection for Contoso

After completing the configuration steps in the previous unit, Contoso's security engineer verified protection by reviewing all three output areas.

**AI agent inventory**: The customer service agent appeared in the AI assets inventory with **Connected** status. The inventory listed the SharePoint library connector and the Dataverse connection used for customer account lookups. The risk signal panel flagged the sensitive SharePoint library access, confirming that discovery identified the misconfiguration.

**Incidents and alerts**: Within hours of enabling protection, an alert appeared in the incident queue. A test interaction where an external user attempted to access the sensitive SharePoint library was blocked, and Defender generated a low\-severity alert titled "AI agent policy violation." The incident included the blocked SharePoint request and the user who initiated the conversation.

**Advanced Hunting**: The security engineer ran a query against agent interaction data and confirmed that tool invocations from the customer service agent were being logged. The query returned results showing successful Dataverse lookups for customer account balances and the blocked SharePoint access attempt.

With all three verification steps complete, Contoso confirmed that real\-time protection is active and functioning end\-to\-end. The agent continues to serve legitimate customer inquiries while Defender blocks attempts to access sensitive data that shouldn't be exposed through the agent interface.

---

## Summary

Contoso Financial Services' external facing Copilot Studio agents were operating without any runtime inspection. User interactions passed directly between agents and their connected data sources—no visibility, no record, no ability to detect or block suspicious behavior. This module changed that.

### Review what you accomplished

You explored the three capability pillars of Microsoft Defender for Cloud Apps AI agent protection:

* discovery and hunting to find agents and query their activity.
* audit and alerts to surface policy violations.
* real\-time runtime protection to inspect and intercept interactions before they complete.

Understanding these pillars matters. Each pillar has different setup requirements and provides different types of value—discovery is automatic, while real\-time protection requires explicit configuration.

You configured real\-time protection by navigating to **System** \> **Settings** \> **Security for AI agents** in the Microsoft Defender portal, registering the target Copilot Studio agent by App ID, and coordinating with the Power Platform admin to configure the Defender App ID in the Power Platform admin center. The two\-admin coordination requirement is by design—runtime protection requires changes on both the security and platform administration sides, and the Connected status indicator in the Security for AI settings page confirms when both steps are complete.

You also explored agent identity—how Copilot Studio automatically assigns each agent a Microsoft Entra Agent ID (a Microsoft Entra service principal with an "Agent" subtype) that enables Conditional Access policies, centralized audit logging, and Zero Trust lifecycle management. This identity is distinct from the proxy App ID exchanged during real\-time protection setup.

You then verified protection outputs across three surfaces:

* the AI assets inventory in Microsoft Defender XDR (confirming the agent appears with Connected status and connector data).
* the Incidents view (confirming alerts flow and correlate).
* Advanced Hunting (confirming agent interaction data is queryable).

Verification isn't optional—Connected status confirms the proxy is in place, but checking the outputs confirms data is flowing end\-to\-end.

In this module, you learned how to:

* Describe the AI agent protection capabilities available in Microsoft Defender for Cloud Apps
* Enable real\-time protection for Copilot Studio agents in the Microsoft Defender portal
* Verify that agent protection outputs appear in the Microsoft Defender XDR inventory, alerts, and Advanced Hunting

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/enable-protection-copilot-studio-agents/_

## Fuentes
- [Enable real-time protection for Copilot Studio agents](https://learn.microsoft.com/en-us/training/modules/enable-protection-copilot-studio-agents/?WT.mc_id=api_CatalogApi)
