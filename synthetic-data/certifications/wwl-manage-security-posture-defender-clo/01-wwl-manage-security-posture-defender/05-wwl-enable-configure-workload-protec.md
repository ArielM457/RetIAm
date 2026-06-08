# Enable and configure workload protection plans in Microsoft Defender for Cloud

> Curso: Manage security posture by using Microsoft Defender for Cloud (wwl-manage-security-posture-defender-cloud) · Seccion: Manage security posture by using Microsoft Defender for Cloud
> Duracion estimada: 33 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Financial Services operates a complex hybrid Azure environment with hundreds of Windows and Linux virtual machines, Azure SQL databases managing customer financial records, and Azure Blob Storage accounts storing transaction data and compliance reports. The environment also includes an Azure Kubernetes Service (AKS) cluster powering internal trading applications. The team is also rolling out a customer\-facing financial assistant built on Azure OpenAI Service, adding generative AI workloads to an already broad attack surface. The security team recently enabled foundational Cloud Security Posture Management (CSPM) in Microsoft Defender for Cloud, which now generates configuration recommendations and tracks regulatory compliance. While compliance reports provide valuable security posture visibility, Contoso faces a critical gap: no Cloud Workload Protection Platform (CWPP) plans are enabled, leaving the organization without runtime threat detection and response capabilities.

Without active CWPP plans, Contoso's workloads remain vulnerable to active threats. When an attacker uploads malware to a storage account, no alert fires. When suspicious queries target databases containing sensitive financial data, the security team receives no notification. When vulnerabilities in virtual machines are actively exploited, there's no detection or automated response. The foundational CSPM layer identifies misconfigurations and policy violations. However, it can't detect malicious behavior, active exploitation, or runtime threats targeting specific workload types like servers, databases, storage accounts, or container environments.

In this module, you:

* Identify the CWPP plans available in Defender for Cloud and explain what workloads each plan protects, including Defender for AI Services and Defender for APIs
* Enable workload protection plans at the subscription level using Environment Settings in the Azure portal
* Configure Defender for Servers (Plan 1 vs. Plan 2\), Defender for Storage protection layers, and Defender for Databases subplans for your protection requirements
* Deploy protection plans at scale using management groups and Azure Policy, and verify plan coverage using the Coverage workbook

---

## Understand the Defender for Cloud CWPP plan catalog

Contoso Financial Services enabled Cloud Security Posture Management (CSPM) and received a compliance score, but when live attacks occurred against production workloads, no security alerts appeared. The security team realized CSPM evaluates misconfigurations, but doesn't detect threats during active attacks. Here, you learn the conceptual difference between CSPM and Cloud Workload Protection Platform (CWPP). You explore the full catalog of CWPP plans available in Defender for Cloud, and understand what each plan protects.

### Understand the difference between CSPM and CWPP

CSPM and CWPP serve complementary but fundamentally different purposes in your cloud security strategy. CSPM evaluates your environment's security posture by comparing configurations against compliance standards and best practices—it tells you what's weak or misconfigured. CWPP operates during runtime, monitoring active workloads for threats, detecting malicious behavior, and generating alerts when attacks occur in progress.

Consider a misconfigured storage account with public access enabled. CSPM identifies misconfigured storage as a security recommendation and lowers your compliance score. CWPP monitors that same storage account in real time for suspicious activity—unauthorized access attempts, unusual data transfer patterns, or malware uploads. With CSPM alone, you understand your vulnerabilities but lack visibility into active exploitation.

This distinction matters for Contoso because compliance posture and threat detection require different technical capabilities. CSPM analyzes static configurations through Azure Resource Graph queries. CWPP deploys threat intelligence, behavioral analytics, and machine learning models that process data streams from your workloads continuously. You need both to achieve comprehensive cloud security.

### Explore the CWPP plan catalog

Defender for Cloud offers nine CWPP plans, each designed to protect specific Azure resource types with tailored threat detection capabilities. The plans integrate with native Azure platform data, eliminating the need for separate security tools in most scenarios.

| Plan | What it protects | Key threats detected |
| --- | --- | --- |
| **Defender for Servers P1/P2** | Azure VMs, Arc\-enabled servers, on\-premises machines | Fileless attacks, process injection, lateral movement, privilege escalation |
| **Defender for Storage** | Azure Storage accounts (Blob, Files, Data Lake) | Malware uploads, unusual access patterns, data exfiltration, public exposure abuse |
| **Defender for Databases** | Azure SQL, SQL on VMs, open\-source databases, Cosmos DB | SQL injection, brute\-force attacks, anomalous queries, vulnerability exploitation |
| **Defender for Containers** | AKS clusters, ACR registries, container workloads | Image vulnerabilities, runtime threats, Kubernetes privilege escalation, network attacks |
| **Defender for App Service** | Azure App Service web apps and APIs | Code injection, command execution, dangling DNS takeover, suspicious network connections |
| **Defender for Key Vault** | Azure Key Vault secrets, keys, certificates | Unusual access patterns, anomalous application behavior, credential theft attempts |
| **Defender for Resource Manager** | Azure control plane operations | Lateral movement via Azure Resource Manager (ARM), suspicious resource modifications, privilege abuse |
| **Defender for APIs** | Azure API Management gateways | OWASP API Top 10 attacks, sensitive data exposure, broken authentication, excessive data exposure |
| **Defender for AI Services** | Azure OpenAI Service, Azure AI Model Inference service | Prompt injection, jailbreak attempts, data exfiltration via AI responses, model abuse |

Each plan activates immediately after enablement, with most requiring no agent deployment or configuration changes. Some plans offer tiered options—Defender for Servers provides P1 and P2 tiers with different feature sets, which you explore in detail later in this module.

### Protect compute and infrastructure

Your compute resources represent the most common attack surface because they run application code and process business data. **Defender for Servers** provides the most comprehensive protection, with two pricing tiers that differ in vulnerability assessment, endpoint detection, and response capabilities. You examine these differences thoroughly in the next unit, where you plan and enable server protection for Contoso's workloads.

**Defender for App Service** integrates natively with the platform to monitor web application traffic, API calls, and file operations without requiring agent installation. The plan detects code injection attempts, command execution attacks, and scanning behavior, plus identifies dangling DNS configurations that attackers could exploit for subdomain takeover. Because App Service operates as a fully managed platform, Defender analyzes data at the Azure infrastructure layer rather than within your application code.

**Defender for Resource Manager** monitors the Azure control plane—the API layer where you create, modify, and delete resources. Attackers who compromise an identity with Owner or Contributor permissions often execute lateral movement through ARM template operations. Operations like creating new VMs in different subscriptions or exfiltrating data by modifying resource configurations. This plan detects suspicious patterns in Azure Resource Manager activity, including unusual geographic locations, rare API combinations, and rapid resource provisioning that suggests automated reconnaissance.

**Defender for Containers** protects Kubernetes environments and container registries, detecting threats during image build, registry storage, and runtime execution. The plan scans container images for vulnerabilities, monitors AKS cluster control plane operations, and analyzes runtime behavior inside pods. Container security architecture—sensor deployment, registry scanning configuration, and runtime policy—is a broad subject in its own right; this unit focuses on identifying when to include Defender for Containers in your overall CWPP plan.

### Protect data and services

While compute resources execute attacks, data resources represent what attackers ultimately target. **Defender for Storage** operates at three distinct layers—Activity Monitoring detects unusual access patterns and public exposure events, Malware Scanning analyzes uploaded content for malicious files, and Sensitive Data Threat Detection combines both capabilities with data classification insights. You configure these layers individually to align protection depth with the risk profile of Contoso's storage accounts.

**Defender for Databases** functions as an umbrella plan that activates protection for four database engine types: Azure SQL Database, SQL Server on Azure VMs, open\-source relational databases (PostgreSQL, MySQL, MariaDB), and Azure Cosmos DB. The plan detects SQL injection attempts, brute\-force authentication attacks, and anomalous query patterns that suggest data exfiltration or privilege abuse. Each database engine receives tailored threat models—SQL injection detection differs between relational and NoSQL systems because the query languages and attack vectors diverge significantly.

**Defender for Key Vault** monitors access to secrets, keys, and certificates stored in Azure Key Vault, detecting unusual access patterns that deviate from normal application behavior. When an identity that typically retrieves one secret suddenly requests dozens, or when access originates from an unfamiliar geographic location, the plan generates alerts for investigation. This protection proves critical because compromised credentials often provide attackers with persistent access to your environment even after you remediate the initial breach.

### Defend APIs and AI workloads

APIs and AI services represent emerging attack surfaces that require specialized protection beyond traditional infrastructure security. **Defender for APIs** integrates with Azure API Management to analyze traffic patterns, detect OWASP API Top 10 vulnerabilities, and classify sensitive data exposed through API responses. The plan uses Cloud Security Graph to understand relationships between APIs, backend services, and data stores, identifying exposure risks that span multiple resources. APIs often expose authentication weaknesses or return excessive data in responses—attacks that CWPP must detect at the protocol level rather than through infrastructure monitoring.

**Defender for AI Services** provides real\-time protection for Azure OpenAI Service and Azure AI Model Inference service deployments, addressing threats unique to large language models and generative AI systems. The plan integrates with Azure AI Content Safety Prompt Shields and Microsoft Threat Intelligence. Then detects prompt injection attacks, jailbreak attempts, sensitive data anomalies in model responses, and credential theft targeting AI infrastructure. As organizations deploy AI\-powered applications—like Contoso's planned customer\-facing financial assistant—these attack vectors become as relevant as traditional server and database threats.

Both API and AI protection plans activate without requiring changes to your application code or API configurations. Defender analyzes data from Azure platform services, applying machine learning models trained on threat intelligence specific to API abuse and AI system manipulation.

---

## Enable workload protection plans in Environment Settings

Microsoft Defender for Cloud includes over a dozen workload protection plans, but every plan is disabled by default until you actively enable it. For Contoso Financial Services, this means navigating to Environment Settings in the Azure portal and making strategic choices about which plans to turn on and which service tiers to select. Here, you learn how to access the Defender plans configuration page. Then you decide between enabling all plans at once or selectively enabling individual plans. Finally, you explore subscription\-level and resource\-level scope, and choose the right plan for production workloads.

### Navigate to the Defender plans page

The Defender plans configuration interface lives within Environment Settings, where you control protection settings at the subscription level. To reach this page, follow these steps:

1. In the Azure portal, navigate to **Microsoft Defender for Cloud**.
2. In the left navigation, select **Environment settings**.
3. Select the subscription you want to configure.
4. The Defender plans page opens, showing all available workload protection plans with toggle switches. Plans with more configuration options show a **Settings** button in the row.

Tip

For most plans, configure at the subscription level to ensure consistent protection across all resources. Some plans—including Defender for Storage and Defender for SQL—also support resource\-level enablement for selective coverage without requiring a subscription\-level setting first.

### Enable all plans or select individually

The Defender plans page provides two approaches to enabling protection: the **Enable all** button at the top of the page, or individual toggle switches for each plan. Each approach serves different organizational needs based on environment scope, threat model, and coverage requirements.

Tip

Before enabling all plans on a production subscription, confirm you have resources of each type in scope—enabling plans for resource types that don't exist in your environment provides no security value. Review the [Microsoft Defender for Cloud pricing page](https://azure.microsoft.com/pricing/details/defender-for-cloud/) to understand billing models for plans you intend to use.

After you select your plans and configure any plan\-specific settings, select **Save** at the top of the page. Defender for Cloud deploys the necessary monitoring components automatically, which typically takes a few minutes. You don't need to manually install agents or configure data collection for most plans.

### Compare subscription\-level and resource\-level scope

Most Defender for Cloud plans operates at the subscription level, meaning you enable the plan once and it protects all resources of that type within the subscription. However, several plans support resource\-level scope, which lets you enable or disable protection for individual resources.

Defender for Servers provides the most flexible scoping options, with different capabilities for Plan 1 and Plan 2\. These scoping rules let you align protection depth with risk classification—applying Plan 2 capabilities to production workloads processing sensitive data while applying a lighter footprint to dev/test systems with a lower threat exposure.

| Scope | Plan 1 | Plan 2 |
| --- | --- | --- |
| Enable for a subscription | Yes | Yes |
| Enable for individual resource | Yes | No |
| Disable for individual resource | Yes | Yes |

Plan 1 allows both enabling and disabling at the resource level, giving you complete flexibility to protect specific virtual machines without enabling the plan at the subscription level. Plan 2 requires subscription\-level enablement but allows you to exclude specific resources by disabling protection at the resource level.

Defender for Storage and Defender for SQL also support resource\-level enablement. When you enable Defender for Storage at the subscription level, it protects all storage accounts. Alternatively, you can enable protection selectively on storage accounts that contain sensitive or regulated data—ensuring your highest\-risk resources receive full coverage while lower\-risk accounts receive a baseline configuration.

### Evaluate Defender for Servers Plan 1 and Plan 2

Defender for Servers offers two service tiers with different feature sets. Your choice should reflect the threat exposure of the workloads being protected, your compliance obligations, and any gaps in existing detective controls.

**Plan 1** provides foundational server protection through Microsoft Defender for Endpoint integration, core vulnerability management capabilities, and security alerts for suspicious behavior. This plan suits development and test environments, or production workloads with limited internet exposure and an existing control stack that already covers file integrity and network visibility.

**Plan 2** includes everything in Plan 1 plus advanced features designed for production workloads handling sensitive data: just\-in\-time VM access, file integrity monitoring, network map visualization, agentless disk scanning, and 500 MB of free daily data ingestion per server into Log Analytics.

| Feature | Plan 1 | Plan 2 |
| --- | --- | --- |
| Microsoft Defender for Endpoint integration | Yes | Yes |
| Defender Vulnerability Management—core features | Yes | Yes |
| Defender Vulnerability Management—premium features | No | Yes |
| Security alerts and threat detection | Yes | Yes |
| Just\-in\-time VM access | No | Yes |
| Network map | No | Yes |
| File integrity monitoring | No | Yes |
| Free daily data ingestion (500 MB per server) | No | Yes |
| Agentless scanning | No | Yes |

**Just\-in\-time VM access** provides critical protection for internet\-facing virtual machines by keeping management ports closed except when explicitly needed. With this feature enabled, Defender for Cloud blocks inbound traffic on SSH port 22 and RDP port 3389 by default. When an administrator needs to connect, they submit an access request through the Azure portal specifying the port, source IP addresses, and time window. Defender for Cloud evaluates the request against configured policies, and if approved, opens the requested port only for the approved source IPs and only for the approved time window.

**File integrity monitoring** tracks changes to critical operating system files, application binaries, Windows registry keys, and Linux system files. The feature establishes a baseline of known\-good file states and generates alerts when it detects unauthorized modifications. These alerts help you identify potential malware infections, privilege escalation attempts, or configuration drift that could indicate a security compromise. For Contoso's production servers handling financial data, file integrity monitoring provides essential visibility into system\-level changes that could indicate an active attack.

Note

File integrity monitoring is available in Plan 2 but isn't turned on by default. After enabling Plan 2, navigate to **Environment settings** → **Settings** for the Defender for Servers plan to enable it separately.

### Enable plans and verify the configuration

After you evaluate which plans align with your workload types and risk tolerance, you implement the configuration and verify that protection activates successfully. The activation process requires just a few actions but has significant security implications.

On the Defender plans page, toggle each desired plan to **On**. For Defender for Servers, use the **Select plan** dropdown to choose between Plan 1 and Plan 2\. If any plans display a **Settings** button, select it to review plan\-specific options. Select **Save** at the top of the page. Defender for Cloud deploys monitoring components automatically—typically within 5 to 10 minutes. Once all toggled plans display **On** in the status column, protection is active and Defender for Cloud begins generating recommendations and alerts for covered resources.

---

## Configure Defender for Storage and Defender for Databases

Enabling a workload protection plan is the first step—configuring it for the right coverage depth is the second. Defender for Storage and Defender for Databases both offer configuration choices that directly determine what gets protected and how deeply threats are detected. In the Contoso Financial Services scenario, customer financial records live in Blob Storage and sensitive transaction data runs in Azure SQL databases. Here, you learn how to configure the three protection layers in Defender for Storage. You learn to manage malware scanning scope, enable Defender for Databases protection, and choose between the bundle and individual subplans based on your database portfolio.

### Configure Defender for Storage protection layers

Defender for Storage provides three distinct protection layers. Understanding each layer helps you make informed configuration decisions. The first layer is always active when the plan is enabled, while the other two require explicit configuration choices.

**Activity monitoring** operates automatically the moment you enable Defender for Storage—no diagnostic logs or other setup required. This layer analyzes data and control plane data from Azure Blob Storage, Azure Files, and Azure Data Lake Storage Gen2\. Powered by Microsoft Threat Intelligence and behavioral models, activity monitoring detects threats like SAS token abuse (entities accessing data without identities), anomalous access from Tor exit nodes, and suspicious data access patterns. For Contoso, this baseline protection identifies unusual account activity across all storage resources without configuration overhead.

Note

A **Tor exit node** is the final relay in the Tor anonymization network—the point where traffic leaves Tor and reaches its destination. Threat actors use Tor to mask their true origin when accessing cloud resources. Because legitimate enterprise workloads rarely access Azure Storage via Tor, any request from a known Tor exit node IP is a high\-confidence anomaly signal, even when the request uses valid credentials.

**Malware scanning** operates as a configurable add\-on that scans uploaded blobs in near real time using Microsoft Defender Antivirus. This layer is important for Contoso's customer\-facing upload workflows—any blob a user uploads could contain malware before Contoso's systems process it. Unlike activity monitoring, malware scanning is billed per gigabyte of data scanned. Microsoft applies a default monthly cap of 10,000 GB (10 TB) of scanned data per storage account per month. When the cap is reached, scanning stops for the remainder of the month and an alert fires to notify you—meaning any blobs uploaded after that point aren't scanned until the next month. You configure malware scanning by navigating to the Defender for Storage plan in Environment Settings → Settings → configure the malware scanning toggle and set the monthly cap value.

**Sensitive data threat detection** uses an agentless engine called Sensitive Data Discovery that automatically finds storage resources containing sensitive information. This layer integrates with Microsoft Purview sensitive information types (SITs) and classification labels. When enabled, security alerts for resources containing sensitive data are prioritized higher, giving your security operations team clearer context about what's at risk. Sensitive data threat detection is enabled by default in the Defender for Storage plan Settings and incurs no extra cost beyond the base plan. For Contoso's financial records storage, this prioritization ensures alerts about customer data receive immediate attention.

Important

When malware scanning reaches its monthly cap, uploaded blobs are no longer scanned until the next month—creating a detection gap. Set the monthly cap based on your expected upload volume and risk tolerance. High\-risk storage accounts handling user\-generated content should have a cap that reflects actual traffic patterns, not a conservative default.

### Manage malware scanning scope

The scope at which you enable Defender for Storage determines how uniformly protection applies across your environment and how granularly you tune malware scanning per account.

When you enable Defender for Storage at the subscription level, protection applies to all storage accounts in that subscription with the same settings. This approach provides comprehensive coverage with minimal configuration effort—every storage account inherits the subscription's malware scanning toggle and monthly cap value. For organizations with consistent security requirements across all storage resources, subscription\-level enablement simplifies management and ensures no storage account is accidentally left unprotected.

When you enable Defender for Storage at the storage account level, you gain selective coverage and can apply different malware scanning configurations to specific accounts. This approach is useful for Contoso because their customer\-facing storage accounts need malware scanning enabled. A configuration with caps sized to match upload volumes, while internal storage accounts for operational logs or backups don't require malware scanning at all. Configuring at the account level lets you align protection depth with the risk profile of each resource.

You can also combine approaches: enable Defender for Storage at the subscription level to establish baseline activity monitoring for all accounts, then override malware scanning settings at the storage account level to fine\-tune cost and coverage. Storage account\-level settings always take precedence over subscription\-level defaults, giving you flexibility to adjust protection as risk profiles change.

### Enable Defender for Databases protection

Defender for Databases protects database workloads by detecting threats through anomaly detection, behavioral baselines, and integration with Microsoft Threat Intelligence. When suspicious activity occurs—such as SQL injection attempts, brute force sign in attacks, or unusual data exfiltration patterns—Defender for Databases generates security alerts that your security operations team can investigate and respond to.

The Databases plan uses a bundle approach: when you toggle the Databases plan to On in Environment Settings, it simultaneously enables four subplans:

1. **Defender for Azure SQL Databases** \- protects Azure SQL Database and Azure SQL Managed Instance against SQL injection, brute force attacks, and anomalous access patterns.
2. **Defender for SQL Servers on Machines** \- protects SQL Server instances running on virtual machines, whether hosted in Azure, on\-premises, AWS, or Google Cloud Platform via Azure Arc.
3. **Defender for open\-source relational databases** \- protects PostgreSQL, MySQL, and MariaDB on Azure against database\-specific attack vectors and anomalous query patterns.
4. **Defender for Azure Cosmos DB** \- protects Azure Cosmos DB accounts against document injection, unusual access patterns, and data exfiltration attempts.

All four subplans activate together with a single toggle, providing comprehensive database protection across your entire portfolio. For Contoso, this means their Azure SQL databases, on\-premises SQL Servers connected via Azure Arc, and any open\-source databases used for development workloads are all protected under one unified plan.

### Choose between the bundle and individual subplans

The bundle approach provides comprehensive coverage with minimal configuration, but individual subplan enablement offers precision when your database portfolio is more selective or when cost control requires targeted protection.

Each of the four database subplans can be enabled individually rather than as a bundle. This approach is appropriate when a subscription's actual database portfolio doesn't include all four types—you enable protection only where you deployed workloads. If your organization has no Cosmos DB deployments that subplan provides no detection value and can remain disabled until those workloads are introduced. Similarly, if all database workloads run on Azure SQL with no on\-premises SQL Server instances, the SQL Servers on Machines subplan isn't relevant to your environment.

Defender for Azure SQL and Defender for open\-source relational databases also support resource\-level scope, letting you enable or disable protection at the individual database level. This granularity is useful for excluding dev/test databases from paid protection while covering all production databases.

Tip

Start with the bundle approach to establish baseline protection across all database types, then refine enablement at the subplan or resource level after mapping your actual database workloads and their risk classifications.

---

## Deploy plans at scale and verify coverage

Contoso Financial Services doesn't manage one subscription—they manage dozens, spread across multiple business units and environments. Enabling plans subscription\-by\-subscription through the portal doesn't scale, and the Secruity Officer (CISO) needs assurance that protection is consistent across the entire estate. Here, you learn how to deploy protection at management group level. Then you enforce configurations with Azure Policy, verify coverage across your entire environment, and optimize costs with resource\-level control.

| Deployment approach | Scope | Best for |
| --- | --- | --- |
| Management group enablement | All current and future subscriptions | Enterprise\-wide consistent protection |
| Azure Policy enforcement | Compliance reporting and governance | Regulated environments requiring audit trails |
| Coverage workbook verification | Estate\-wide visibility | Security audits and gap analysis |

### Enable protection across a management group

The most efficient way to deploy Defender plans at scale is to enable them at the management group level. When you select a management group in Environment Settings instead of an individual subscription, the plans you enable apply automatically to all child subscriptions—including subscriptions created after you configure the plans.

To enable plans at the management group level, navigate to **Microsoft Defender for Cloud** \> **Environment settings**, then select the management group rather than drilling into an individual subscription. Choose which plans to enable, and Defender for Cloud propagates those settings down the management group hierarchy. This approach ensures that new subscriptions inherit protection automatically, eliminating coverage gaps when teams deploy new resources.

Security administrators use this capability to enforce consistent protection across business units. With a single configuration at the root or intermediate management group level, you establish the baseline protection standard for the entire organization.

Note

When you enable plans at the management group level, subscriptions that already have a plan enabled retain their existing configuration. The management group setting applies to subscriptions without explicit settings.

### Enforce plan enablement using Azure Policy

Management group enablement provides deployment efficiency, but it doesn't prevent someone from disabling a plan at the subscription level. Azure Policy adds an enforcement and compliance layer that makes protective coverage auditable and enforceable.

Defender for Cloud provides built\-in Azure Policy initiative definitions for each Defender plan. When you assign one of these policy initiatives to a management group or subscription, Azure Policy evaluates whether the specified plan is enabled. If a subscription doesn't have the required plan active, the policy marks that subscription as "Noncompliant" in Azure Policy's compliance dashboard.

This compliance signal is essential in regulated environments where security governance requires proof that plans are consistently enforced. Assign the policy initiative at the management group level enforcing the requirement across all child subscriptions. Then use **Azure Policy** \> **Compliance** to generate reports showing which subscriptions meet the requirement and which need remediation. This combination gives security teams both preventive control and audit evidence.

Tip

Use Azure Policy's built\-in remediation tasks to automatically enable plans on noncompliant subscriptions. Built\-in remediation closes the enforcement loop without manual intervention.

### Verify coverage with the Coverage workbook

After enabling plans at scale, you need visibility into protected resources. The Coverage workbook is Defender for Cloud's purpose\-built audit tool for understanding plan coverage across your entire estate.

Access the Coverage workbook through **Microsoft Defender for Cloud** \> **Workbooks** \> **Coverage workbook**. The workbook displays plan enablement status across your subscriptions and resources through four views: **Relative coverage** shows the percentage of subscriptions with each plan enabled, **Absolute coverage** shows each plan's status per subscription, **Detailed coverage** shows other settings required for full plan value, and **Additional information** explains each toggle. You can filter by Azure, AWS, or GCP environment to scope the view to a specific cloud.

Use the Coverage workbook immediately after deploying plans at scale to confirm no subscriptions were missed during rollout. Security teams also use this workbook as evidence during audits, demonstrating comprehensive protection coverage to compliance officers and regulators.

Note

Management group settings apply as the default for all child subscriptions. You can override plan settings at the individual resource level. An example is excluding a dev/test VM from Defender for Servers Plan 2 or disabling malware scanning on low\-sensitivity storage accounts. Resource\-level settings always take precedence over subscription and management group defaults.

---

## Knowledge check

Answer the following questions to check your understanding of enabling and configuring workload protection plans in Microsoft Defender for Cloud.

### Check your knowledge

---

## Summary

Contoso Financial Services started with Foundational Cloud Security Posture Management (CSPM) active but no workload protection plans enabled. Their environment had visibility into misconfigurations but no runtime threat detection—no alerts when attackers accessed storage, exploited server vulnerabilities, or attempted suspicious database queries. By enabling the right CWPP plans, configuring layer\-specific settings, and deploying protection at scale, the security team transformed Defender for Cloud into an active threat detection platform. The Coverage workbook now confirms full protection across all critical workloads.

In this module, you explored how CSPM provides posture recommendations while Cloud Workload Protection Plans (CWPP) deliver runtime threat detection—and you identified which plan protects each Azure workload type. You enabled plans through Environment Settings and compared Defender for Servers Plan 1 (foundational endpoint protection and vulnerability management) with Plan 2 (which adds just\-in\-time VM access, file integrity monitoring, agentless scanning, OS configuration assessment, and 500\-MB free daily data ingestion). You configured Defender for Storage's three protection layers—activity monitoring, malware scanning, and sensitive data threat detection—and enabled Defender for Databases subplans for SQL, open\-source databases, and Cosmos DB. You deployed protection at scale using management groups and Azure Policy, then verified coverage with the Coverage workbook to confirm no gaps remain.

CWPP plans transform Defender for Cloud from a compliance and posture tool into a comprehensive threat detection platform. Posture recommendations reduce your attack surface by fixing vulnerabilities before exploitation. CWPP plans catch threats in real time—detecting malicious activity, blocking malware uploads, and alerting on anomalous database queries. Together, they create defense in depth: fewer vulnerabilities to exploit, and immediate detection when attacks occur.

### Learn more

* [What is Microsoft Defender for Cloud?](/en-us/azure/defender-for-cloud/defender-for-cloud-introduction)
* [Enable Defender for Cloud enhanced security features](/en-us/azure/defender-for-cloud/connect-azure-subscription)
* [Defender for Servers overview](/en-us/azure/defender-for-cloud/defender-for-servers-overview)
* [What is Microsoft Defender for Storage](/en-us/azure/defender-for-cloud/defender-for-storage-introduction)
* [Protect your databases with Defender for Databases](/en-us/azure/defender-for-cloud/tutorial-enable-databases-plan)
* [About Microsoft Defender for APIs](/en-us/azure/defender-for-cloud/defender-for-apis-introduction)
* [AI threat protection in Defender for Cloud](/en-us/azure/defender-for-cloud/ai-threat-protection)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/enable-configure-workload-protection-plans/_

## Fuentes
- [Enable and configure workload protection plans in Microsoft Defender for Cloud](https://learn.microsoft.com/en-us/training/modules/enable-configure-workload-protection-plans/?WT.mc_id=api_CatalogApi)
