# Manage security for Arc-enabled hybrid servers

> Curso: Implement security for servers and virtual machines (wwl-server-vm-security) · Seccion: Implement security for servers and virtual machines
> Duracion estimada: 25 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Manufacturing recently connected its on\-premises production scheduling and supply chain servers to Azure using Azure Arc. The servers are enrolled and appear in Azure as managed resources. However, a critical security gap remains. Any user with sufficient Azure permissions can deploy extensions to these servers—effectively installing software with elevated privileges. The factory servers have no policy enforcement, no security baseline compliance checks, and no unified visibility in Microsoft Defender for Cloud.

In this module, you learn how to secure Arc\-enabled servers using a defense\-in\-depth approach. You explore:

* How to configure role\-based access control (RBAC) and extension allow/block lists to prevent unauthorized software installation on Arc\-enabled servers
* How to assign and manage Azure Policy to enforce security baselines across hybrid infrastructure
* How to monitor security posture and compliance for Arc\-enrolled servers in Microsoft Defender for Cloud
* How machine configuration policies extend security governance to Arc\-enrolled servers

### Prerequisites

* Working knowledge of Azure Arc server connectivity and the Azure Connected Machine agent
* Foundational understanding of Microsoft Defender for Cloud security recommendations and regulatory compliance features
* Access to an Azure subscription with Arc\-enabled servers already enrolled

With Arc connectivity established, you can now apply security governance at cloud scale to Contoso's factory servers. In the next unit, you examine how to control who can manage Arc servers and what software can run on them.

---

## Control access and extension security for Arc\-enabled servers

Extensions on Arc\-enabled servers grant code execution with elevated privileges. Any user who can deploy an extension can effectively run arbitrary code on the target server, making extension control a critical security boundary. A misconfigured role assignment or a compromised privileged account can expose your entire hybrid infrastructure to unauthorized software installation or malicious activity.

### Use RBAC to control Arc server management

Azure provides two specialized built\-in roles for Arc\-enabled server management. Understanding when to use each role prevents over\-privileging accounts and reduces blast radius if credentials are compromised.

The **Azure Connected Machine Onboarding** role grants the minimum privilege needed to connect servers to Azure Arc. Users or service principals with this role can create new Arc server resources but can't reonboard, delete, or modify existing resources. Crucially, this role can't deploy extensions. Use this role for accounts dedicated solely to server enrollment, such as automation service principals running in your on\-premises environment.

The **Azure Connected Machine Resource Administrator** role grants full control over Arc\-enabled servers, including the ability to deploy and remove extensions. Because extensions run with elevated privileges on the target machine, this role effectively grants root or administrator access to the underlying server. Treat this role with the same sensitivity you would grant to local administrator credentials. Consider using Azure Privileged Identity Management (PIM) for just\-in\-time elevation rather than persistent assignments.

| Role | Can Enroll Servers | Can Modify Existing Servers | Can Deploy Extensions | Recommended Use |
| --- | --- | --- | --- | --- |
| Azure Connected Machine Onboarding | Yes | No | No | Enrollment\-only automation |
| Azure Connected Machine Resource Administrator | Yes | Yes | Yes | Operational management (use PIM) |

For Contoso Manufacturing, enrollment automation uses the Onboarding role. Operations staff receives Resource Administrator access through PIM with approval workflows, ensuring every extension deployment is traceable and authorized.

### Configure extension allow and block lists

Azure RBAC controls who can request extension deployments, but it operates at the cloud layer where privileged users can modify role assignments and policies. For defense in depth against insider threats or account compromise, the Azure Connected Machine agent supports extension allow and block lists configured directly on the server.

Extension lists are configured using the `azcmagent config` command on the Arc\-enabled server itself. The agent enforces these lists locally, and Azure users can't override them, regardless of permissions. This agent\-level control provides a security boundary independent of cloud\-based access management.

An **allow list** specifies which extensions are permitted to install. When an allow list is configured, any extension not explicitly listed is blocked, even if a privileged Azure user requests deployment. Extension identifiers use the format `Publisher/Type` with a forward slash separator—for example, `Microsoft.Azure.Monitor/AzureMonitorLinuxAgent`. The command `azcmagent config set extensions.allowlist "Microsoft.Azure.Monitor/AzureMonitorLinuxAgent,Microsoft.Azure.AzureDefenderForServers/MDE.Linux"` permits only the Azure Monitor Agent and Microsoft Defender for Endpoint extensions on a Linux server.

A **block list** specifies extensions that are explicitly prohibited. All other extensions remain permitted. Use a block list when you want to allow most extensions but prevent specific ones known to conflict with your environment or security requirements.

The special value `"Allow/None"` creates a zero\-extension mode where the agent runs and maintains connectivity to Azure but refuses all extension installation requests. This configuration is useful when Arc enrollment serves only to deliver Extended Security Updates (ESU) for legacy Windows Server instances, with no need for other management capabilities.

Extension deletion requests are always honored, regardless of allow or block list configuration. This design ensures you can always remove unwanted extensions.

| Configuration | Command Example | Behavior |
| --- | --- | --- |
| Allow list | `azcmagent config set extensions.allowlist "Microsoft.Azure.Monitor/AzureMonitorLinuxAgent"` | Only listed extensions can install |
| Block list | `azcmagent config set extensions.blocklist "Microsoft.EnterpriseCloud.Monitoring/OMSAgentForLinux"` | Listed extensions can't install; all others permitted |
| Zero\-extension mode | `azcmagent config set extensions.allowlist "Allow/None"` | No extensions permitted (ESU\-only mode) |

### Use monitor mode for monitoring and security scenarios

For servers that need only monitoring and security extensions—such as Azure Monitor Agent and Microsoft Defender for Cloud—the agent's built\-in monitor mode provides a simpler alternative to manually maintained allow lists. Enable it with a single command:

```
azcmagent config set config.mode monitor

```

In monitor mode, Microsoft maintains the approved extension list and updates it automatically as new monitoring and security extensions become available. The agent blocks any extension capable of changing system configuration or running arbitrary scripts. To check the current mode and see which extensions are allowed, run `azcmagent config list`.

Monitor mode has two important limitations: you can't modify the extension allow or block list while in monitor mode, and the Guest Configuration policy agent is disabled—meaning machine configuration policies (covered in the next unit) won't run. If you need machine configuration policies alongside extension restrictions, use a custom allow list in full mode instead.

To return to full mode: `azcmagent config set config.mode full`

### Combine agent\-level and cloud\-level controls

Azure Policy provides cloud\-based extension governance at the subscription or management group scope, making it ideal for standardizing configurations across large deployments. However, anyone with policy authoring permissions can modify these assignments. Use Azure Policy to establish baseline requirements and deploy extensions automatically, but rely on agent\-level allow lists as an immutable control that protects against malicious or accidental policy changes.

For Contoso's factory servers, the security team configures an allow list that permits only the Microsoft Defender for Endpoint extension, the ChangeTracking extension for File Integrity Monitoring, and the Machine Configuration extension for baseline compliance checks. Any other extension installation attempt—even from an Azure administrator with Resource Administrator role—silently blocking with the agent. This layered approach ensures that even if an Azure account is compromised, the attacker can't deploy arbitrary software to production servers.

With RBAC scoping who can manage servers and extension controls limiting what can run on them, you're ready to enforce security policies at scale using Azure Policy.

---

## Apply Azure Policy to Arc\-enabled servers

Arc\-enabled servers appear in Azure as first\-class resources under the `Microsoft.HybridCompute/machines` resource type. This integration means you can apply the same Azure Policy governance framework to hybrid servers that you use for Azure virtual machines, enabling consistent security controls across cloud and on\-premises infrastructure.

### Assign policies at the right scope

Azure Policy assignments cascade from parent scopes to child resources. For organizations with hybrid infrastructure distributed across multiple subscriptions, assigning policies at the management group level ensures uniform coverage without repetitive per\-subscription configurations.

Contoso Manufacturing organizes its Azure environment with a management group hierarchy: a root management group contains a "Factory Operations" management group, which in turn contains subscriptions for North America, Europe, and Asia\-Pacific factories. By assigning Arc security policies at the Factory Operations management group, all current and future subscriptions inherit the same controls automatically. When a new regional subscription is created, its Arc\-enrolled servers are immediately subject to the established security policies.

| Scope Level | Coverage | Use Case |
| --- | --- | --- |
| Management group | All subscriptions within the group | Enterprise\-wide or division\-wide standards |
| Subscription | All resources in one subscription | Subscription\-specific requirements |
| Resource group | Resources in a single group | Granular control for specific server sets |

This scope strategy reduces configuration drift and ensures consistent security posture as infrastructure scales.

### Use built\-in policies for Arc servers

Azure provides built\-in policy definitions designed for Arc\-enabled servers. These policies cover security agent deployment, configuration baseline enforcement, and security feature enablement.

The **Configure Azure Defender for Servers to be enabled (with 'P1' subplan) for all resources** policy automatically enables Microsoft Defender for Servers Plan 1 on all Arc\-enrolled machines. This DeployIfNotExists policy creates the necessary Defender configuration when it detects an Arc server without coverage, ensuring all hybrid servers receive threat detection and vulnerability assessment capabilities.

The **Configure ChangeTracking Extension for Windows Arc machines** and **Configure ChangeTracking Extension for Linux Arc machines** policies deploy the ChangeTracking extension to enable File Integrity Monitoring (FIM). FIM alerts you when critical system files, registry keys, or configuration files are modified, providing early warning of unauthorized changes or malware activity.

The **Windows machines should meet requirements of the Azure compute security baseline** and **Linux machines should meet requirements for the Azure compute security baseline** policies assess operating system configurations against CIS benchmarks and Microsoft security baselines. These policies require the Machine Configuration extension (covered in detail in Module 7\) and report compliance status for hundreds of individual settings, such as password complexity requirements, audit logging configuration, and service hardening.

Preview policies such as **vTPM should be enabled on supported virtual machines** and **Secure Boot should be enabled on supported Windows virtual machines** enforce security features on virtualized Arc servers, protecting against boot\-level malware and ensuring trusted boot chains.

### Assign and remediate policies

The policy assignment workflow for Arc servers follows the standard Azure Policy pattern. Navigate to **Azure Policy** in the Azure portal, select **Assign Policy** or **Assign Initiative**, and choose the management group, subscription, or resource group scope.

When configuring a DeployIfNotExists policy, specify the Azure region for the remediation managed identity. This system\-assigned managed identity performs the deployment actions on your behalf. Grant the identity the minimum permissions needed to deploy the target extension or configuration—typically the Azure Connected Machine Resource Administrator role scoped to the assignment's target resources.

After assignment, Azure Policy evaluates resources on a periodic cycle and marks noncompliant resources. For existing Arc servers that were enrolled before policy assignment, compliance violations appear immediately but no automatic remediation occurs. Create a **remediation task** from the policy assignment detail pane to deploy extensions or apply configurations to preexisting noncompliant resources. New Arc servers enrolled after policy assignment are automatically remediated as they appear.

| Policy Effect | Behavior | Remediation Required |
| --- | --- | --- |
| Audit | Reports compliance status only | No |
| AuditIfNotExists | Reports compliance for nested conditions | No |
| DeployIfNotExists | Automatically deploys resources for new violations | Yes, for existing resources |
| Deny | Blocks noncompliant resource creation | No |

### Understand policy applicability for Arc versus Azure VMs

Some built\-in policies apply exclusively to Azure virtual machines, some target only Arc\-enabled servers, and some cover both resource types. Review the policy definition's description and the `if` condition clause to determine applicability. Policies that reference `"type": "Microsoft.Compute/virtualMachines"` affect only Azure VMs, while those referencing `"type": "Microsoft.HybridCompute/machines"` target Arc servers. Policies with both conditions in an `anyOf` block cover hybrid and cloud resources.

This distinction matters when interpreting compliance reports. If you assign a policy intended for Azure VMs to a scope containing Arc servers, the Arc servers appear as "Not applicable" rather than compliant or noncompliant, preventing false compliance metrics.

### Recognize policy limitations and layer controls

Azure Policy assignments are mutable resources. Any user with `Microsoft.Authorization/policyAssignments/write` permissions at the target scope can modify or delete assignments, disabling controls. For this reason, combine cloud\-based Azure Policy with agent\-level extension controls (configured in the previous unit). Azure Policy provides ease of management and visibility; agent\-level allow lists to enforce against privileged threats.

### Prepare for machine configuration policies

Azure Machine Configuration policies (formerly Azure Guest Configuration) assess and enforce configurations inside the operating system, such as registry settings, file permissions, installed software, and service states. These policies use the Machine Configuration extension, which runs on both Azure VMs and Arc\-enabled servers. You can assign machine configuration policies to Arc servers through the same Azure Policy mechanism described in this unit. Module 7 covers machine configuration in depth, including how to create custom policies for organization\-specific security requirements.

### Apply policies at Contoso Manufacturing

Contoso's security team assigns three policies at the Factory Operations management group scope:

* **Configure Azure Defender for Servers to be enabled (with 'P1' subplan) for all resources** — ensures all Arc servers receive vulnerability scanning and threat detection
* **Configure ChangeTracking Extension for Windows Arc machines** — enables FIM on all factory Windows servers
* **Windows machines should meet requirements of the Azure compute security baseline** — assesses compliance with CIS benchmarks

After assignment, the team creates remediation tasks to deploy extensions to the 47 Arc\-enrolled servers that existed before the policies were assigned. All future Arc enrollments receive these extensions automatically within minutes of registration.

With policies assigned and remediation underway, you're ready to monitor the security posture of Arc\-enrolled servers in Microsoft Defender for Cloud.

---

## Monitor Arc server security posture in Defender for Cloud

Arc\-enabled servers integrate seamlessly with Microsoft Defender for Cloud, appearing in asset inventory, security recommendations, and regulatory compliance assessments alongside Azure virtual machines. This unified view eliminates the operational overhead of managing separate security tools for cloud and on\-premises infrastructure.

### View Arc servers in asset inventory

Arc\-enabled servers appear in Defender for Cloud's asset inventory under the resource type filter **Machines \- Azure Arc**. The inventory view displays each server's subscription, resource group, location (the Azure region where the Arc resource is registered, not the physical server location), and Defender coverage status.

When you enable Microsoft Defender for Servers Plan 1 or Plan 2 on a subscription containing Arc machines, Defender for Cloud automatically extends coverage to those servers. The inventory Coverage column indicates whether each Arc server has Defender enabled and which plan is active. Machines without coverage show actionable recommendations to enable Defender.

Filter the inventory by resource type to isolate Arc servers, by Defender coverage to identify gaps, or by subscription to review regional deployments. Tag\-based filtering helps you segment servers by function, such as "production\-scheduling" or "supply\-chain," allowing focused security reviews for business\-critical workloads.

### Review security recommendations for Arc servers

Defender for Cloud assesses Arc\-enabled servers using the same security controls applied to Azure VMs. Recommendations appear in the **Recommendations** pane organized by severity: High, Medium, and Low. Each recommendation includes a description, remediation steps, and an estimated effort level.

Common recommendations for Arc servers include:

* **Install endpoint protection solution on machines** \- prompts deployment of Microsoft Defender for Endpoint (MDE) via the MDE extension
* **System updates should be installed on your machines** \- identifies missing security patches and provides remediation guidance through Azure Update Manager integration
* **Machines should be configured securely** \- indicates noncompliance with OS security baselines, requiring Machine Configuration extension for detailed assessment

Recommendations that require extensions to provide detailed findings automatically deploy those extensions if you assigned the corresponding Azure Policy with DeployIfNotExists effect. For example, assigning the OS security baseline policy deploys the Machine Configuration extension, which then scans hundreds of configuration settings and reports specific noncompliant controls.

| Recommendation Severity | Meaning | Example |
| --- | --- | --- |
| High | Exposes server to immediate risk | Missing endpoint protection |
| Medium | Increases attack surface | Weak password policy |
| Low | Best practice improvement | Audit logging not optimized |

Remediate high\-severity recommendations first to address the most critical risks. Many recommendations provide automated remediation workflows, such as one\-click extension deployment or Azure Policy assignment links.

### Track regulatory compliance posture

Arc\-enabled servers contribute to regulatory compliance assessments in Defender for Cloud. When you enable a compliance standard such as ISO 27001, PCI DSS, or NIST SP 800\-53, Defender for Cloud evaluates Arc servers against the relevant controls and reports aggregate compliance scores.

The **Regulatory Compliance** dashboard displays compliance percentage for each standard and breaks down control categories. Select a standard to view individual controls, then drill into specific controls to see which Arc servers are compliant or noncompliant. This granular visibility supports audit preparation by providing evidence of control implementation across hybrid infrastructure.

Contoso Manufacturing is pursuing ISO 27001 certification. By enrolling factory servers with Arc and enabling Defender for Cloud, the security team tracks compliance across on\-premises and Azure resources in a single dashboard. Auditors can review the compliance report to verify that Contoso's hybrid infrastructure meets ISO 27001 control requirements, such as access management, change tracking, and security monitoring.

### Monitor coverage with workbooks

The Defender for Cloud Coverage workbook visualizes which subscriptions have Defender plans enabled and which resources are protected. Filter the workbook by resource type to view Arc server coverage across your organization. The workbook highlights subscriptions with partial coverage, helping you identify gaps where Arc servers exist but Defender for Servers isn't enabled.

Use the workbook to track coverage expansion over time. As Contoso enrolls other factory servers with Arc, the workbook reflects increasing protected resource counts, providing a measurable metric for security program progress.

### Investigate security alerts for Arc servers

When Defender for Servers is enabled, Arc\-enrolled servers generate security alerts based on behavioral analysis, threat intelligence, and anomaly detection. Alerts appear in the **Security Alerts** pane with details about the detected threat, affected resources, and recommended response actions.

Defender for Cloud correlates alerts across Azure and hybrid environments, creating unified incident views when a threat spans multiple resources. For example, if an attacker compromises an Arc server and uses it to probe Azure storage accounts, Defender for Cloud links the related alerts into a single incident, accelerating investigation and response.

Alert severity levels (High, Medium, Low, Informational) help you prioritize investigation. High\-severity alerts indicate active exploitation or critical security violations requiring immediate action. Configure alert notifications to send high\-severity alerts to your security operations center (SOC) via email, webhook, or integration with Microsoft Sentinel.

### Manage Extended Security Updates for Arc servers

Arc\-enabled servers running Windows Server 2012 or Windows Server 2012 R2 can receive Extended Security Updates (ESUs) through Azure Arc using a monthly pay\-as\-you\-go billing model via your Azure subscription—no traditional volume licensing keys or manual key activation required. Extended Security Updates (ESUs) are free only for servers hosted in Azure; on\-premises servers connected via Arc must purchase ESU coverage. ESU Year 3 support ends October 13, 2026, making server modernization the long\-term priority.

Defender for Cloud tracks ESU patch status and surfaces recommendations when critical ESU patches are missing. Integrate Arc servers with Azure Update Manager to automate ESU deployment on a recurring schedule, ensuring servers remain protected against vulnerabilities in end\-of\-support operating systems.

### Review posture at Contoso Manufacturing

Contoso's engineering team uses Defender for Cloud to monitor the security posture of Arc\-enrolled factory servers. The team filters the asset inventory to view all **Machines \- Azure Arc**, confirms that Defender for Servers Plan 1 is enabled on all resources, and reviews the top three security recommendations: install endpoint protection, apply system updates, and configure machines securely.

The regulatory compliance dashboard shows 78% compliance with ISO 27001 controls for Arc servers, up from 0% before Arc enrollment. The remaining noncompliant controls require machine configuration policy remediation and endpoint protection deployment, both scheduled for completion in the next sprint.

By centralizing security monitoring in Defender for Cloud, Contoso gains unified visibility across Azure and on\-premises infrastructure, accelerates compliance reporting, and reduces the operational burden of managing separate security tools for hybrid environments.

---

## Knowledge check

You explored how to secure Arc\-enabled servers using RBAC, extension controls, Azure Policy, and Microsoft Defender for Cloud. Test your understanding of these security governance concepts with the following questions.

### Check your knowledge

---

## Summary

Contoso Manufacturing's factory servers are now secured with defense\-in\-depth controls that span cloud\-based governance and agent\-level enforcement. You configured RBAC to limit who can manage Arc servers, applied extension allow lists to prevent unauthorized software installation, assigned Azure Policy to enforce security baselines at scale, and enabled Microsoft Defender for Cloud to monitor security posture and compliance across hybrid infrastructure.

### Key security decisions

Effective Arc server security requires layered controls operating at multiple enforcement points:

* **Agent\-level extension controls cannot be overridden by cloud users**, providing immutable protection against insider threats and compromised privileged accounts. Cloud\-based Azure Policy provides ease of management and visibility but allows users with sufficient permissions of make modifications. Use both controls together.
* **Azure Policy assigned at management group scope** covers all subscriptions automatically, reducing configuration drift, and ensuring consistent security posture as infrastructure scales. DeployIfNotExists policies automate extension deployment and configuration, but require remediation tasks for existing resources.
* **Defender for Cloud treats Arc\-enabled servers as first\-class resources**, providing unified security recommendations, regulatory compliance tracking, and security alert correlation across Azure and on\-premises environments. Arc servers running legacy operating systems receive Extended Security Updates at no extra cost, reducing risks from unpatched vulnerabilities.
* **Role\-based access control separates enrollment privileges from operational management**. Use the Azure Connected Machine Onboarding role for server registration automation and the Azure Connected Machine Resource Administrator role (with PIM) for operational tasks requiring extension deployment.

### Learn more

* [Security overview for Azure Arc\-enabled servers](/en-us/azure/azure-arc/servers/security-overview)
* [Extensions security for Azure Arc\-enabled servers](/en-us/azure/azure-arc/servers/security-extensions)
* [Azure Policy built\-in definitions for Arc\-enabled servers](/en-us/azure/azure-arc/servers/policy-reference)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/manage-security-azure-arc-servers/_

## Fuentes
- [Manage security for Arc-enabled hybrid servers](https://learn.microsoft.com/en-us/training/modules/manage-security-azure-arc-servers/?WT.mc_id=api_CatalogApi)
