# Secure access for Microsoft Entra Agent Identity

> Curso: Implement security for AI (wwl-implement-ai-security) · Seccion: Implement security for AI
> Duracion estimada: 23 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Financial Services expanded its use of AI agents—automating compliance checks, surfacing regulatory guidance, and handling routine client queries. Each agent runs as an identity in Microsoft Entra Agent ID. When the security team audits the agent landscape, they find agents created months ago that are still active with no access conditions enforced. Traditional access controls weren't designed for agent identities, and the team needs a systematic approach to secure them.

Microsoft Entra Agent ID gives agent identities a home in Microsoft Entra—but identity alone isn't security. The controls that matter are the ones that govern what agents can do, when they can authenticate, and what happens when an agent identity is no longer needed.

This module builds on the foundational knowledge of Microsoft Entra Agent ID and focuses on applying Conditional Access policies to agent identities. You map how agents authenticate, configure policies that enforce access conditions, and manage the agent identity lifecycle to reduce risk from compromised or over\-privileged agents.

Note

This module assumes you reviewed Introduction to Microsoft Entra Agent ID, which covers what agent identities are. It explores how they differ from other identity types, and how to navigate the Microsoft Entra admin center to view and manage them.

### Learning objectives

In this module, you learn how to:

* Map how AI agents authenticate and identify where Conditional Access applies
* Configure Conditional Access policies scoped to agent identities
* Control agent access
* Manage agent identity lifecycle events

### Prerequisites

Before you begin, you should have:

* Completed Introduction to Microsoft Entra Agent ID
* Understanding of Microsoft Entra Conditional Access policy structure
* Familiarity with Microsoft Entra ID authentication concepts

---

## Map authentication flows and Conditional Access scope

Before applying security controls to agent identities, you need to understand how they authenticate to Microsoft services and where Conditional Access policies intersect with their access patterns. Contoso Financial Services deploys AI agents for compliance automation, and the security team must map authentication flows to identify control points. Here, you learn the three ways agents authenticate and where Conditional Access applies to each pattern.

Agents in Microsoft Entra Agent ID access corporate resources using one of three access patterns. The correct Conditional Access configuration depends on which pattern your agents use:

| Access Pattern | Token subject | CA assignment scope | Interactive controls (MFA, device) |
| --- | --- | --- | --- |
| **On\-behalf\-of (OBO)** | The signed\-in user | Assign to users or groups | Available—user is present |
| **Application\-only (autonomous)** | The agent identity | Assign to agent identities | Not applicable—no users present |
| **Agent's user account** | The agent's user\-type identity | Assign to that user account | Not applicable—non\-interactive flow |

### How agent identities authenticate

The on\-behalf\-of (OBO) flow is the most common access pattern. In this flow, a user signs in to an agent application, and the agent then exchanges the user's token to obtain a separate token scoped to the corporate resource it needs to access. The resource token is issued to the user—the user's identity and permissions constrain what the agent can do. Because the user is the token subject throughout the OBO flow, standard user\-targeted Conditional Access policies apply, including MFA requirements, device compliance checks, and sign\-in risk conditions.

Autonomous agents operate without a signed\-in user. They authenticate directly as their service principal using the OAuth 2\.0 client credentials flow—presenting a certificate, managed identity token, or client secret to receive an access token issued to the agent identity itself. This non\-interactive flow is efficient for scheduled or event\-driven tasks but removes the interactive security checkpoints that user authentication provides. For autonomous agents, the agent identity is the token subject, and CA policies must target the agent service principal directly.

A third pattern applies when an agent operates with its own user\-type account—for example, a digital worker with a dedicated mailbox that participates in team workflows. In this case, the agent authenticates as a user, and CA policies target that user account identity using standard user\-targeted policy configuration.

The pattern in use determines which assignment scope to configure when you create Conditional Access policies. Applying a user\-targeted policy to an autonomous agent misses the enforcement point, and applying an agent\-targeted policy to an OBO flow won't intercept the authentication that matters.

### Where Conditional Access applies to agents

Conditional Access evaluates policies at token issuance time—before the agent or user receives a token for a resource. The assignment scope in a CA policy determines which authentication events trigger evaluation.

For **OBO flows**, assign the policy to users or groups. Because the user is the token subject, evaluation happens against the user's context—location, device, and sign\-in risk all apply. Target resources should include the corporate resources the agent accesses on the user's behalf, so the policy evaluates every token exchange in the flow.

For **autonomous (application\-only) flows**, assign the policy to agent identities. When you create a Conditional Access policy, select **Assignments** \> **Users, agents or workload identities**, then select **Agents**. The option **All agent identities** covers all agent service principals in your tenant. You can also target specific agent identities or their parent agent identity blueprint to cover all agents derived from that blueprint.

For **agent's user account flows**, assign the policy to the user account that represents the agent, using standard user\-targeted CA configuration.

### Scale policy targeting with attributes and blueprints

As your agent population grows, individually listing agent service principals in CA policies becomes operationally unsustainable. Two approaches support scalable targeting.

**Attribute\-driven targeting** uses custom security attributes—business\-specific key\-value pairs you define and assign to agent identities in Microsoft Entra ID. For example, you can define a `DataSensitivity` attribute with values like `Confidential` or `Internal`, then write a CA policy condition that blocks any agent identity where `DataSensitivity = Confidential`. The policy applies automatically to agents with that attribute value, including new agents added in the future—no policy update required.

**Blueprint\-level targeting** applies a CA policy to a parent agent identity blueprint, automatically covering all agent identities derived from that blueprint. If multiple agents for a project or product are created from the same blueprint, a single policy enforces consistent controls across the group without listing individual agents.

### What Conditional Access enforces for autonomous agents

For both autonomous agent identities and agent user accounts, the non\-interactive authentication flow limits, which Conditional Access controls apply. Understanding these boundaries helps you design realistic policies for agents that operate without a user present.

Conditional Access **can enforce** the following for autonomous agent identities:

* **Block sign\-in**: Prevent the agent identity from authenticating entirely
* **Named location conditions**: Restrict authentication to specific IP ranges or geographic regions
* **Sign\-in frequency restrictions**: Require token refresh at defined intervals
* **Risk\-based conditions**: Block agents flagged as high\-risk by Microsoft Entra ID Protection

Conditional Access **cannot enforce** the following for autonomous agent identities:

* **Multifactor authentication (MFA)**: There's no user present to complete a prompt
* **Device compliance**: No physical device is registered to evaluate
* **User\-based session controls**: App\-enforced restrictions and similar controls require an interactive user session

These limits apply equally to autonomous agent identities (which use a service principal). And the limits apply to agent user accounts (which use a user\-type identity but still authenticate non\-interactively). Agents can't respond to an MFA prompt or present a device compliance certificate. For OBO flows these limits don't apply—the full user CA control set is available, including MFA, device compliance, sign\-in risk, and session controls, because the human user is the token subject throughout.

Contoso's security team uses named location conditions to enforce a base policy: all autonomous agent identities must authenticate from corporate network IP ranges or designated Azure regions. Agents attempting to authenticate from other locations are blocked automatically.

Now that you understand where Conditional Access intersects with agent authentication, you're ready to configure specific policies scoped to agent identities.

---

## Configure Conditional Access policies for agents

Conditional Access policies scoped to agent identities provide granular control over which agents can authenticate and under what conditions. Contoso Financial Services needs to restrict a legacy Copilot Studio agent that was deployed for a completed project but never decommissioned. Here, you configure Conditional Access policies targeting agent identities and apply them safely using report\-only mode.

| Configuration Step | Action |
| --- | --- |
| **Define scope** | Select **All agent identities** or specific agent service principals |
| **Set conditions** | Named locations, sign\-in risk, or application filters |
| **Choose access control** | Block access, or grant with conditions, or session controls |
| **Validate impact** | Deploy in report\-only mode and review sign\-in logs |
| **Enforce policy** | Switch to enabled after validation period |

### Configure Conditional Access for OBO flows

In an OBO flow, the access token is issued to the user—not the agent service principal. Conditional Access policies for OBO agents assign to users or groups, not to agent identities. Because the user is the token subject, the full CA control set is available, including MFA, device compliance, and sign\-in risk requirements.

To configure a CA policy for agents operating in an OBO flow:

1. Navigate to **Protection** \> **Conditional Access** \> **Policies** and select **New policy**.
2. Under **Assignments**, select **Users, agents or workload identities**. Under **What does this policy apply to?**, select **Users and service principals**.
3. Under **Include**, select the users or groups who interact with the agent—or select **All users** for a broader baseline policy.
4. Under **Target resources**, select the resources the agent accesses on the user's behalf—specific applications such as Microsoft Graph or SharePoint Online, or **All resources** for broad coverage.
5. Under **Conditions**, configure signals based on where users sign in, such as named locations or sign\-in risk.
6. Under **Access controls** \> **Grant**, configure the controls appropriate to the resource's sensitivity, such as **Require multifactor authentication** or **Require compliant device**.
7. Set **Enable policy** to **Report\-only** and select **Create**. Review sign\-in logs for at least 24–48 hours before switching to enforcement.

The recommended baseline CA policies for OBO flows include blocking legacy authentication, requiring MFA for elevated sign\-in risk, and requiring MFA for guest users accessing agent\-connected resources.

The remainder of this unit covers configuring CA for the application\-only (autonomous) scenario—blocking a specific agent service principal from authenticating.

### Create a Conditional Access policy for agent identities

Conditional Access policies for agents follow the same creation flow as user\-focused policies but target agent identities instead of user accounts. Conditional Access for agents requires a **Microsoft Entra ID P1** or **Microsoft 365 E3** license. Microsoft Entra Agent ID is part of Microsoft Agent 365—users need a Microsoft Agent 365 or Microsoft 365 E5 license to use Agent ID features, with the specific security features each requiring their own licensing tier.

To create a Conditional Access policy for agent identities, sign in to the Microsoft Entra admin center and navigate to **Protection** \> **Conditional Access** \> **Policies**. Select **New policy** and give the policy a descriptive name that reflects its purpose, such as "Block Copilot Studio agent \- Legacy compliance project."

Under **Assignments**, select **Users, agents or workload identities**. In the **Include** section, choose **All agent identities** to apply the policy to every agent in your tenant. Alternatively, select **Select agent identities** and choose specific agent service principals by name or object ID. This granular targeting allows you to isolate individual agents for blocking or conditional access without affecting other agents.

The choice between targeting all agents and targeting specific agents depends on your security posture. Blocking all agents by default and selectively allowing approved agents creates a secure\-by\-default environment but increases operational overhead. Targeting specific agents for blocking provides flexibility but requires ongoing monitoring to detect new unauthorized agents.

### Design the policy for agent\-specific conditions

Agent authentication flows support a subset of Conditional Access conditions compared to user authentication. When admins design policies for agents, focus on conditions that evaluate at token issuance time without requiring interactive prompts.

**Named locations** are the most common condition for agent policies. You can restrict agent authentication to corporate IP ranges, Azure regions, or specific datacenters. For example, Contoso restricts all Copilot Studio agents to authenticate only from their Azure East US and West Europe regions, where their primary workloads run. Agents attempting to authenticate from other locations are blocked automatically.

**Sign\-in risk** conditions apply to agents through Microsoft Entra ID Protection. If an agent's service principal exhibits suspicious behavior—such as authentication from an unusual location or at an unusual time—the risk level increases. You can configure Conditional Access to block high\-risk agent sign\-ins or require extra validation.

**Application filters** allow you to target agents based on the resources they're trying to access. For instance, you might block all agent identities from accessing Microsoft Graph but allow access to Power Platform APIs. This approach limits the blast radius if an agent's credentials are compromised.

Under **Target resources** \> **Resources (formerly cloud apps)**, select **All resources** to apply the policy globally or choose specific applications like Microsoft Graph or Microsoft Power Platform.

### Configure access controls and session policies

After defining conditions, you configure what happens when an agent meets those conditions. Under **Access controls** \> **Grant**, you have three primary options:

* **Block access**: Completely prevent the agent from authenticating. Use this option to decommission agents or enforce an allow list model where only approved agents can authenticate.
* **Grant access**: Allow authentication without other conditions. This option is rare for agent policies because it doesn't add security value over no policy at all.
* **Grant access with controls**: Require specific conditions before granting access. For agents, the most applicable control is **Require compliant network** (enforced through named locations).

Session controls offer limited applicability to agents because they're designed for interactive sessions. However, **Sign\-in frequency** can enforce token expiration, requiring agents to reauthenticate at defined intervals. This control limits the window of opportunity if an agent's token is stolen.

For Contoso's scenario, the security team configures the following policy:

* **Name**: Block Copilot Studio agent \- Legacy compliance project
* **Scope**: Specific agent service principal (selected by object ID)
* **Conditions**: None (block unconditionally)
* **Access control**: Block access
* **Policy state**: Report\-only (initially)

This configuration completely blocks the legacy agent from authenticating once the policy is enforced.

### Validate the policy with report\-only mode

Before enforcing a Conditional Access policy targeting agents, deploy it in report\-only mode to understand its operational changes. Report\-only mode evaluates the policy against every authentication request and logs what *would* happen without actually blocking access. This validation step prevents accidental disruption of production agents.

When you create a new policy, set **Enable policy** to **Report\-only** instead of **On**. Microsoft Entra ID evaluates the policy and logs the results in the Conditional Access sign\-in logs. Navigate to **Microsoft Entra ID** \> **Monitoring** \> **Sign\-in logs** and filter by **Conditional Access** to view policy evaluations.

Review the logs for at least 24\-48 hours to capture a full cycle of agent activity. Look for unexpected matches—agents you didn't intend to block—and verify that the intended agents are correctly scoped. If the policy targets the wrong service principals or blocks critical agents, adjust the scope and repeat the validation period.

Important

Targeting the wrong service principal in a Conditional Access block policy can break production services with no warning. Always start in report\-only mode and validate policy issues before enforcing.

After validating the policy, return to **Protection** \> **Conditional Access** \> **Policies**, select the policy, and change **Enable policy** to **On**. The policy now actively blocks authentication for the targeted agents.

### Apply the policy to Contoso's legacy agent

Contoso's security team identifies the legacy Copilot Studio agent by reviewing the agent identities list in the Microsoft Entra admin center. They note the agent's object ID and create a Conditional Access policy scoped specifically to that service principal.

After admins deploy the policy in report\-only mode for two days, the sign\-in logs confirm the agent attempted authentication three times per day from an Azure East US region. No other agents match the policy scope. The team switches the policy to enforcement mode, and the next authentication attempt is blocked. The legacy agent stops functioning, and the compliance project's automated workflows—now obsolete—are safely decommissioned.

This targeted approach allows Contoso to remove access for individual agents without disrupting other agent\-based automation across the organization.

---

## Control agent access and lifecycle

Controlling agent access extends beyond Conditional Access policies to include preventing unauthorized agent creation and monitoring agent lifecycle events. Contoso Financial Services needs ongoing visibility into which agents exist in their tenant and when new agents are created. Here, you explore three approaches to disabling agent access and implement monitoring to track agent lifecycle events through audit logs.

| Approach | Scope | When to Use |
| --- | --- | --- |
| **Conditional Access block** | Blocks authentication for existing and new agents | Primary enforcement mechanism; prevents token issuance |
| **Block agent creation per product** | Prevents new agents from being created in specific products | Reduces sprawl; enforces approval workflows |
| **Disable individual agents** | Deactivates a specific agent identity | Targeted decommissioning or incident response |

### Block agent authentication with Conditional Access

Conditional Access policies provide the frontline of defense against unauthorized agent access. As you configured in the previous unit, CA policies intercept authentication requests and block token issuance based on policy conditions. This approach works for both existing agents and newly created agents because the policy evaluates every authentication attempt regardless of when the agent was created.

Conditional Access block policies are effective when you need to enforce tenant\-wide restrictions—for example, blocking all agent identities from authenticating unless explicitly allowed. This secure\-by\-default model prevents agents from operating without explicit security team approval. However, CA policies don't prevent the creation of agent identities; they only block authentication. This distinction matters because unauthorized agents can still appear in your tenant and consume directory quota, even if they can't authenticate.

For comprehensive control, combine CA block policies with product\-level restrictions that prevent agent creation at the source.

### Block agent creation per product

Individual Microsoft products that create agent identities provide their own configuration settings to restrict or prevent agent creation. Blocking creation at the product level reduces agent sprawl and enforces approval workflows before agents are deployed.

**Microsoft Agent 365** (now generally available) provides the centralized control plane for agent governance across all products in your organization. In the Microsoft 365 admin center under **Agents** \> **Settings**, you can configure which categories of agents are permitted (**Allowed agent types**), apply **Security templates** that bundle Conditional Access policies and custom security attributes as presets enforced on every new agent, and define **User access** controls that specify which users or groups can interact with agents. **Agent management rules** let you apply governance actions in bulk—for example, automatically reassigning ownership of agents whose creators left the organization. These controls apply across agent sources, making Agent 365 the recommended starting point before applying per\-product restrictions.

For **Copilot Studio**, you can restrict agent creation through licensing, role\-based access control, or data policies. The most effective approach combines licensing and RBAC: prevent users from signing up for Copilot Studio free trials and remove the Power Platform Administrator role from users who shouldn't create agents. Without the appropriate license and role, users can't create Copilot Studio environments or deploy agents.

Alternatively, apply data loss prevention (DLP) policies that prevent agents from being published. This approach doesn't block agent *creation*, but it prevents agents from becoming operational. Users can build agents in Copilot Studio but can't deploy them for actual use. This middle ground allows experimentation while maintaining control over production deployments.

For **Azure AI Foundry**, restrict agent creation by controlling Azure subscription creation and role assignments. Only users with the Billing Administrator or Account Administrator role can create subscriptions. Within a subscription, only users with the Azure AI Account Owner role can create Foundry projects. Within a project, users need the Azure AI User role to create agents. By not assigning these roles broadly, you limit who can create agents at each layer of the Azure hierarchy.

For **Security Copilot**, block agent creation by removing users from the Owner or Contributor role in Security Copilot workspaces. Microsoft\-owned agents (such as the Microsoft Entra Conditional Access Optimization Agent) require Security Administrator or Identity Governance Administrator roles to enable. Request that users with these roles don't enable agents without approval. For complete blockage, delete all Security Compute Unit (SCU) capacity, which disables Security Copilot entirely—though this approach also blocks Security Copilot itself, not just agents.

Tip

Blocking agent creation at the product level works best when combined with approval workflows. For example, require users to submit a request through a ticketing system before being granted the roles needed to create agents.

Contoso Financial Services restricts Copilot Studio agent creation by removing the Power Platform Administrator role from most users and requiring users to request this role through an approval workflow managed by the IT operations team.

### Disable individual agent identities

For targeted decommissioning or incident response, you can disable specific agent identities without affecting other agents. Each product provides an admin interface to disable agents, and you can also disable agents directly in the Microsoft Entra admin center.

To disable an agent identity in the Microsoft Entra admin center, sign in as at least an **Agent ID Administrator** and browse to **Entra ID** \> **Agents** \> **Agent identities**. Select the agent identity you want to disable, then select **Disable**. This action blocks token issuance for that specific agent without requiring a Conditional Access policy. To disable all agents derived from the same blueprint, browse to **Entra ID** \> **Agents** \> **Agent blueprints** and disable the parent blueprint.

Disabling an agent through the product\-specific admin interface achieves the same result but can provide more context or warnings specific to that product. For example, disabling a Copilot Studio agent through the Power Platform admin center shows which workflows or connectors depend on that agent, helping you assess the issues before proceeding.

This approach is ideal for incident response scenarios where you need to immediately stop a compromised agent from authenticating. You can disable the agent, investigate the compromise, rotate credentials, and re\-enable the agent after remediation.

### Monitor agent lifecycle events in audit logs

Audit logs provide visibility into agent creation, modification, and deletion events, allowing you to detect unauthorized agents or configuration drift. Microsoft Entra ID logs agent lifecycle events under the **ApplicationManagement** category with specific activity types.

To monitor agent creation events, navigate to **Microsoft Entra ID** \> **Monitoring** \> **Audit logs**. Filter by **Category** \= **ApplicationManagement** and **Activity** \= **Add service principal**. Agent identities appear as service principals in the audit log, so you must verify whether the created service principal is an agent identity.

To confirm an audit event involves an agent identity, check the `agentType` property on the `targetResources` field of the audit log entry—a value other than `notAgentic` indicates agent involvement. You can also query Microsoft Graph using the object ID returned in the audit event to inspect the `agentType` property on the service principal object. This two\-step process—filtering the audit log and verifying the object type—allows you to track agent creation in near real\-time.

**Key audit events to monitor**:

* **Add service principal**: Agent identity created
* **Update service principal**: Agent configuration or permissions changed
* **Delete service principal**: Agent identity removed
* **Add app role assignment to service principal**: Agent granted access to a resource

Set up alerts or automated workflows to notify the security team when these events occur. For example, configure a Logic App or Microsoft Sentinel playbook to send an email notification whenever a new service principal tagged as an agent identity is created.

Note

Agent user account creation appears as a **Create user** audit event, not a service principal event. To monitor both agent identities and agent user accounts, filter for both **Add service principal** and **Create user** activities and verify the object type.

### Implement access reviews for agent identities

Microsoft Entra access reviews can be applied to workload identities, including agent identities, to periodically validate which agents should remain active. Access reviews prompt designated reviewers to confirm whether each agent is still needed and deactivate agents that are no longer required.

To set up an access review for agent identities, navigate to **Microsoft Entra ID** \> **Identity Governance** \> **Access reviews** and create a new review. Under **Review scope**, select **Workload identities** and specify the service principals representing your agents. Configure the review frequency (for example, monthly or quarterly) and assign reviewers—typically the business owners or project managers responsible for each agent.

During each review cycle, reviewers receive a notification with the list of agents and their current status. Reviewers mark each agent as approved (keep active) or denied (deactivate). Agents marked as denied are automatically disabled or flagged for manual deactivation, depending on your configuration.

Contoso Financial Services sets up a monthly access review for all Copilot Studio agent service principals. The review is assigned to the compliance automation team lead, who confirms whether each agent is still supporting active compliance workflows. Agents not confirmed by the team leads are flagged for deactivation, and the security team disables them using a Conditional Access block policy or by disabling the agent identity directly.

This periodic review process ensures agents don't accumulate over time and provides a governance checkpoint for agent lifecycle management.

---

## Summary

Contoso Financial Services started this module with a landscape of agent identities running without access conditions—agents created months ago, still active, holding permissions beyond what their role required. By the end, the security team has a set of controls in place and a repeatable process for managing agent identity security going forward.

### Review what you accomplished

You mapped how agent identities authenticate to Microsoft services through the OAuth 2\.0 client credentials flow and identified the key difference that shapes every control decision: agents authenticate non\-interactively. They can't respond to MFA prompts or device compliance checks. That constraint focuses enforcement on Conditional Access workload identity policies—the mechanism designed for exactly this authentication pattern.

With that foundation, you created Conditional Access policies scoped to agent service principals. You used report\-only mode to validate policy challenges before enforcement, targeted the specific service principals representing Copilot Studio agents, and set access conditions appropriate to each agent's risk level. The most important pattern: block policies for inactive or over\-privileged agents are effective, reversible, and leave the identity record intact for audit purposes.

You also worked through the full lifecycle—from blocking creation of new agents by product, to monitoring the Microsoft Entra audit log for "Add service principal" events. The event indicates new agent creation, to configuring periodic access reviews that require business owners to confirm each agent should remain active. The result is a governance loop: creation is controlled, activity is visible, and continued access requires periodic validation.

In this module, you learned how to:

* Map how AI agents authenticate and identify where Conditional Access applies
* Configure Conditional Access policies scoped to agent identities
* Control agent access
* Manage agent identity lifecycle events

### What's next

You now have controls on agent identity access. The next step is assessing the risk those identities represent—specifically, how much damage a compromised agent could cause. In the next module, you'll use Microsoft Defender XDR to discover AI agents in your environment and assess their blast radius and attack paths.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/secure-access-entra-agent-identity/_

## Fuentes
- [Secure access for Microsoft Entra Agent Identity](https://learn.microsoft.com/en-us/training/modules/secure-access-entra-agent-identity/?WT.mc_id=api_CatalogApi)
