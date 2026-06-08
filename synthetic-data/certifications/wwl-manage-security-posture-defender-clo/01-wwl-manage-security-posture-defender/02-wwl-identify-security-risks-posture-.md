# Identify security risks by using Cloud Security Posture Management

> Curso: Manage security posture by using Microsoft Defender for Cloud (wwl-manage-security-posture-defender-cloud) · Seccion: Manage security posture by using Microsoft Defender for Cloud
> Duracion estimada: 35 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Healthcare Systems operates a large Azure environment that includes core clinical and administrative workloads. Contoso is expanding AI\-powered applications—a patient triage assistant built on Azure OpenAI and an AI\-driven medical records summarization service running on Azure AI Foundry. The security team receives hundreds of daily security recommendations. The team has no structured method to determine which risks represent real, exploitable threats to patient data, AI model integrity, or business continuity.

Microsoft Defender for Cloud's Cloud Security Posture Management (CSPM) capabilities provide continuous visibility, risk\-based prioritization, attack path analysis, and proactive risk hunting to address exactly this challenge. CSPM helps you identify which misconfigurations and exposures matter most by showing you how attackers could exploit them to reach your critical assets.

In this module, you learn to use CSPM features to identify and prioritize security risks across your Azure environment. Specifically, you:

* Compare Foundational CSPM and Defender CSPM plan capabilities, including AI security posture management features
* Interpret the Cloud Secure Score and security recommendations using the risk\-based prioritization model in the Microsoft Defender portal
* Identify externally exploitable attack paths—including those targeting AI workloads—using attack path analysis
	+ **Initial Access**—internet\-exposed resources that serve as entry points into the environment
	+ **Lateral Movement**—paths an attacker can follow from one resource to another, including toward AI services
	+ **Exfiltration**—routes that lead to critical data such as patient health records or AI model training datasets
	+ **Privilege Escalation**—identity and permission misconfigurations that enable attackers to gain elevated access along a path
* Run graph\-based queries in Cloud Security Explorer to proactively discover security risks

---

## Explore CSPM plans and posture visibility

Contoso Healthcare's security team needs visibility across their entire Azure environment—clinical infrastructure, virtual machines, storage accounts, databases, and AI\-powered applications including Azure OpenAI services and Azure AI Foundry. Microsoft Defender for Cloud provides Cloud Security Posture Management (CSPM) capabilities that give security engineers comprehensive insight into their cloud security state. Here, you explore the two CSPM plan options. First, learn how to navigate the Cloud Overview dashboard in the Defender portal. Then discover how CSPM inventories cloud and AI workloads, and understand the Cloud Secure Score model that measures security risk.

### Understand the two CSPM plans

Defender for Cloud offers two CSPM plans with different capabilities. **Foundational CSPM** is enabled by default at no cost when you onboard an Azure subscription. This plan provides secure score, security recommendations, asset inventory, Microsoft Cloud Security Benchmark (MCSB) assessments, workflow automation, and remediation tools across Azure, AWS, GCP, and on\-premises environments.

**Defender CSPM** is a paid plan that extends foundational capabilities with advanced features. With Defender CSPM, you gain attack path analysis that identifies potential lateral movement routes. Additionally, you get risk prioritization capabilities that surface the most critical issues, and the cloud security explorer for proactive threat hunting. The plan also includes AI security posture management for Azure OpenAI and AI Foundry workloads. Combine this with data security posture management (DSPM), sensitive data scanning, agentless scanning for VMs and containers, external attack surface management, regulatory compliance assessments beyond MCSB, custom security recommendations, and governance rules for remediation tracking.

| Feature Category | Foundational CSPM | Defender CSPM |
| --- | --- | --- |
| Core capabilities | Secure score, recommendations, asset inventory, MCSB, remediation tools | All foundational features included |
| Risk analysis | Basic recommendations | Attack path analysis, risk prioritization, security explorer |
| Advanced scanning | Not included | Agentless VM/container scanning, secrets scanning |
| Specialized posture | Not included | AI security posture, DSPM with sensitive data discovery |
| Compliance | MCSB only | Regulatory compliance assessments, custom recommendations |
| Governance | Workflow automation | Governance rules, ServiceNow integration |

Understandings which plan is active determine what features you can access. Many high\-value capabilities—including risk prioritization, attack path analysis across all workload types, agentless scanning for VMs and containers, and AI security posture management—require the Defender CSPM plan. For an environment like Contoso Healthcare's, where clinical infrastructure, sensitive data stores, and AI workloads all carry different risk profiles, Defender CSPM provides the depth of analysis needed.

### Navigate the Cloud Overview dashboard

The Cloud Overview dashboard serves as your central command center for cloud security in the Microsoft Defender portal. To access it, sign in to the Defender portal at security.microsoft.com, then navigate to Cloud security \> Overview. The dashboard provides scope and environment filters at the top, allowing you to narrow the view to specific Azure subscriptions or pivot between Azure, AWS, and GCP environments.

The **Security at a glance** section displays your most critical metrics. You see the Cloud Secure Score (preview) with a trend indicator, Threat Protection showing the count of active alerts by severity, and Assets Coverage breaking down how many resources have full protection (both posture and threat protection plans), partial protection (one plan), or no protection. This section immediately tells you where your security posture stands.

**Top Actions** guides your next steps by highlighting Critical Recommendations, High\-Severity Incidents to investigate, and Attack Paths that show potential exploitation routes. This actionable guidance helps you focus remediation efforts on what matters most.

The **Trends over time** section shows how your security posture and threat detection evolve. It includes a Security Posture graph—Cloud Secure Score history and recommendations by severity—and a Threat Detection graph showing alert trends by severity. Each graph updates daily and reflects your selected time range (30 days, 3 months, or 6 months).

The **Workload Insights** tiles at the bottom surface specialized intelligence from Microsoft's Cloud\-Native Application Protection Platform (CNAPP). Each tile represents a workload category: Compute, Data, Containers, AI, APIs, DevOps, and Cloud Infrastructure Entitlement Management (CIEM). Each tile shows top security issues, protection coverage status, and links to detailed views for that workload. For example, the Compute tile surfaces findings for virtual machines and scale sets, the Data tile highlights storage and database exposures, and the AI tile shows insights for Azure OpenAI, Azure AI Foundry, and AI agent deployments.

### Discover AI workloads with AI security posture management

Defender CSPM continuously discovers and inventories resources across your Azure environment—virtual machines, storage accounts, databases, containers, and more—providing the asset coverage foundation for all security recommendations and scoring. Beyond standard resource discovery, Defender CSPM also provides specialized discovery for generative AI workloads. For Contoso Healthcare, this means visibility into Azure OpenAI Service instances, Azure AI Foundry projects, and Azure Machine Learning deployments alongside their clinical and administrative infrastructure, all without requiring manual configuration.

The system builds an **AI Bill of Materials (AI BOM)**—a comprehensive inventory of all AI application components, data sources, and artifacts spanning from development code through cloud deployment. This inventory captures not just the AI services themselves, but also the identity configurations, data access patterns, internet exposure status, and associated infrastructure components. With the AI BOM, you understand the full attack surface of your generative AI applications.

Defender CSPM also provides AI agent discovery currently in preview. The system automatically identifies AI agents deployed through Azure AI Foundry and Microsoft Copilot Studio, populating the AI inventory with details about agent configurations, capabilities, and connections.

Note

AI agent discovery is currently in preview. Preview features are subject to change and have limited availability.

This visibility into AI workloads becomes the foundation for the AI\-specific security recommendations you evaluate in subsequent steps. Contoso Healthcare can now see exactly where their AI applications run and what components require security attention.

### Understand the Cloud Secure Score

The **Cloud Secure Score** in the Defender portal represents a risk\-based approach to measuring your security posture. Unlike the classic secure score available in the Azure portal—which uses a control\-based model that treats all recommendations with equal weight—the Cloud Secure Score incorporates asset criticality and contextual risk factors into its calculation.

The risk\-based model evaluates multiple dimensions: whether an asset has internet exposure, handles sensitive data, sits on potential lateral movement paths, or represents a critical business service. A misconfigured storage account containing customer health records and exposed to the internet receives higher risk weighting than a similarly misconfigured development storage account with no sensitive data. This contextual analysis means your score reflects actual business risk, not just control compliance.

Higher scores indicate lower identified risk. As you remediate higher\-risk recommendations, your score reflects the reduced risk across your environment—focus on Critical and High risk findings first, as they carry the most weight in the calculation. To view this score in the Defender portal, navigate to Exposure Management \> Initiatives \> Cloud Security, then select Open initiative page. The initiative page displays your current score, historical trend over time, and score breakdown by workload category.

Note

Microsoft Defender for Cloud offers two separate Secure Score models. The new Cloud Secure Score (risk\-based) is available in the Microsoft Defender portal and incorporates asset criticality for prioritization. The classic Secure Score remains available in the Azure portal and uses a control\-based calculation model.

For teams working primarily in the Azure portal, the classic secure score remains available and continues to function as before. However, the Cloud Secure Score in the Defender portal provides more accurate risk assessment by considering context around each security finding.

---

## Analyze security recommendations with risk prioritization

Contoso Healthcare's security team has enabled Defender CSPM and reviewed their Cloud Secure Score. With hundreds of security recommendations now generated across their Azure workloads — virtual machines, storage accounts, databases, containers, and AI services — they need a systematic approach to prioritize remediation efforts.

| Risk Factor | What It Evaluates | Example |
| --- | --- | --- |
| Internet exposure | Whether the resource is reachable from the public internet | Azure OpenAI endpoint with public access enabled |
| Data sensitivity | Presence of sensitive, confidential, or regulated data | Storage account containing patient health records |
| Lateral movement potential | Whether an attacker could use this resource to reach other assets | Virtual machine with overly permissive network rules |
| Attack path involvement | Whether the issue appears in a chain leading to critical assets | Misconfigured identity that grants access to sensitive databases |

### Understand how risk factors determine recommendation priority

Defender for Cloud assesses security recommendations using a dynamic risk engine that considers multiple environmental factors per asset, not just the severity of the underlying misconfiguration or vulnerability. This context\-aware approach means two resources with identical security issues can receive different risk levels based on their operational context.

Defender for Cloud assigns each recommendation one of five **risk levels**: Critical, High, Medium, Low, or Not evaluated. Critical and High recommendations demand immediate attention because they combine severe misconfigurations with high\-risk environmental factors. Medium and Low recommendations indicate issues that you can address during regular maintenance cycles. The Not evaluated status appears for resources not covered by the Defender CSPM plan or for new recommendations still being assessed by the engine.

Consider a concrete example from Contoso Healthcare's environment. An Azure OpenAI instance with a public endpoint and access to patient health records receives a **Critical** risk level for the "Azure AI Service endpoint should use private connectivity" recommendation. The same misconfiguration on a non\-internet\-facing development instance with synthetic data receives a **Low** risk level.

Note

Risk prioritization columns appear only when the Defender CSPM plan is enabled. Without this plan, risk level and risk factor columns appear blurred in the recommendations interface.

### Navigate and filter the recommendations page

The recommendations page in the Microsoft Defender portal provides a centralized view of all security findings across your multicloud environment. To access recommendations, sign in to the Microsoft Defender portal at security.microsoft.com, navigate to **Exposure Management** \> **Recommendations**, and select the **Cloud** tab.

At the top of the page, three summary cards provide an at\-a\-glance overview of your security posture. The **Cloud Secure Score** card displays your overall security health based on active recommendations. The **Score history** card tracks your Secure Score changes over the last seven days, helping you identify trends and measure improvement. The **Recommendations by risk level** card summarizes the number of active recommendations categorized by severity: Critical, High, Medium, and Low.

The left navigation pane organizes recommendations into three security categories. **Misconfigurations** shows configuration\-related security issues such as overly permissive access controls or missing encryption settings. **Vulnerabilities** displays software vulnerabilities requiring patches or updates. **Exposed Secrets** identifies credentials and secrets that might be compromised. Selecting a category updates both the recommendations list and the summary cards to reflect only that category's findings.

At the top of the recommendations list, you can apply filters to narrow your view. The **Exposed asset** filter shows only resources accessible from the internet. The **Asset risk factors** filter lets you select specific risk conditions such as data sensitivity or lateral movement potential. The **Environment** filter lets you focus on Azure, AWS, or GCP resources. The **Workload** filter isolates specific workload types including AI, databases, virtual machines, and storage. The **Recommendation maturity** filter controls whether you see preview or generally available recommendations.

The recommendations page supports three view options: **Recommendation per asset** shows one row per affected resource ordered by risk level, **Recommendation title** aggregates all instances of the same recommendation type with a count of affected resources, and **Group by resource** groups all findings for the same asset together.

When you select a recommendation row, a side panel opens with four key tabs: **Overview** (recommendation description, exposed asset, risk level distribution), **Remediation steps** (actionable configuration guidance), **Map preview** (related attack paths passing through this asset), and **Related initiatives** (compliance frameworks such as the Microsoft Cloud Security Benchmark).

Note

Defender for Cloud is transitioning from grouped recommendations — where related findings appeared under a single parent item — to individual per\-resource recommendations. During this transition, you may see both formats on the page. Recommendations marked as **Preview** don't yet affect your Secure Score. This is expected behavior and will resolve as the transition completes.

### Identify AI\-specific security recommendations

Defender CSPM generates security recommendations specifically for AI workloads discovered in the AI Bill of Materials (AI BOM) — an inventory of all AI application components, data sources, and artifacts across your environment. To view which AI workloads and models are included in your AI BOM, use the **"AI workloads and models in use"** prebuilt query template in Cloud Security Explorer, which you explore in depth in the next unit.

AI\-specific recommendations cover identity and access controls for Azure AI services, network exposure settings, and infrastructure configuration. To view AI recommendations, select the **Misconfigurations** category from the left navigation and apply the **Workload** filter with the value **AI**. This filter displays recommendations targeting Azure OpenAI Service, Azure AI Foundry, Azure Machine Learning, and multicloud AI services such as Amazon Bedrock and Google Vertex AI.

Defender for Cloud performs Infrastructure as Code (IaC) scans during the development lifecycle and continuously assesses deployed AI resources. The AI security posture capabilities detect four critical IaC misconfigurations:

* **Use Azure AI Service private endpoints** prevents public internet traffic from reaching AI services by requiring all connections to flow through Azure Private Link
* **Restrict Azure AI Service endpoints** limits which networks can reach the service by configuring network rules and firewall policies
* **Use managed identity for Azure AI Service accounts** eliminates stored credentials by allowing AI services to authenticate using Azure\-managed identities
* **Use identity\-based authentication for Azure AI Service accounts** removes API key reliance by requiring Microsoft Entra ID authentication

AI endpoint exposure carries elevated risk because AI models can be exploited to exfiltrate sensitive data from grounding data, fine\-tuning datasets, or model outputs — even if underlying databases are properly secured. Because of this risk, AI\-related recommendations frequently appear in attack paths, and Defender for Cloud continuously generates recommendations to address them before they can be exploited.

### Work with a recommendation — the investigation workflow

When you discover a Critical finding in your environment, a structured investigation workflow helps you understand the full scope of the risk and plan effective remediation. Consider a scenario where Contoso Healthcare's recommendations page displays a Critical finding: "Storage accounts should restrict public network access" affecting four storage accounts across their clinical and administrative environment.

1. **Select the recommendation row**. The side panel opens, providing detailed context about the finding.
2. **Review the Overview tab**. You see which storage accounts are affected and why each received its risk level. The account with internet exposure and sensitive patient records is rated Critical; another with internet exposure but only operational logs is rated High. The remaining accounts are Medium and Low based on lower exposure and data sensitivity.
3. **Review the Remediation steps tab**. The guidance explains what needs to be done: disable public network access on each storage account, configure firewall rules to allow only trusted networks and Azure services, and audit SAS tokens for excessive permissions. For Contoso Healthcare's Critical account, this means coordinating with the clinical data team to confirm application connectivity before disabling public access.
4. **Check the Map preview tab**. You discover the Critical storage account appears in two attack paths. The first path shows an attacker using compromised credentials to access the internet\-exposed account and exfiltrate patient records directly. The second path shows lateral movement from the storage account into the clinical application tier through a service connection with overly permissive network rules. Because this asset appears in active attack paths, remediation urgency increases significantly.
5. **Check the Related initiatives tab**. You confirm which compliance frameworks this affects. The finding maps to Microsoft Cloud Security Benchmark controls for network security and data protection, as well as specific requirements in your healthcare regulatory standards. This documentation helps you justify the remediation work during compliance audits.

With this investigation complete, you can assign remediation ownership and set due dates using Defender CSPM governance rules. Governance rules allow you to automatically route recommendations to specific owners based on resource tags or manually assign them during triage. For Contoso Healthcare, the Critical storage account finding is assigned to the Data Platform team with a 48\-hour due date, while the Medium SAS token finding is assigned to the Development team for resolution during the next maintenance window.

Understanding how to triage recommendations by risk level and investigate the full context of a security issue — whether for storage, compute, networking, or AI workloads — provides the foundation for effective remediation.

---

## Identify attack paths and choke points

Attack path analysis in Defender CSPM reveals the realistic exploitation chains that could allow an attacker to reach your critical assets. For Contoso Healthcare, understanding attack paths is essential. If an internet\-exposed VM with a vulnerability exists in the environment, the security team needs to know whether an attacker could use it to reach the patient triage assistant or the medical records dataset that grounds the AI models. Here, you explore how attack path analysis works, navigate the attack path experience in the Defender portal, investigate individual paths, and understand how attack paths extend to AI workloads.

| Attack path element | Description |
| --- | --- |
| Entry point | External access point where an attack could begin — for example, an internet\-exposed VM or publicly accessible storage |
| Target asset | The critical resource an attacker is trying to reach — for example, a database with patient health records or an Azure AI model endpoint |
| Choke point | A node where multiple attack paths converge — remediating a choke point can break several attack paths simultaneously |
| Vulnerable node | A resource with a security issue that enables lateral movement along the path |

### Understand how attack path analysis works

Attack path analysis uses a proprietary algorithm to identify realistic exploitation chains in your environment. The algorithm focuses on real, externally driven and exploitable threats — paths that begin outside your organization and progress toward business\-critical targets.

The algorithm considers only what's actually reachable and exploitable from external entry points. A short or empty attack paths list means the algorithm found no confirmed externally exploitable paths to your critical assets — a positive security signal, not a platform issue.

Attack path analysis requires the **Defender CSPM plan with agentless scanning** enabled. By default, attack paths are organized by risk level — High, Medium, or Low — using the same context\-aware risk\-prioritization engine that scores security recommendations. The risk level reflects environmental factors such as internet exposure, identity permissions, and the criticality of target assets.

Note

Attack path analysis is currently in preview. Preview features are subject to change and may have limited availability.

### Navigate attack path analysis in the Defender portal

You access attack path analysis through the Exposure Management section of the Microsoft Defender portal. Sign in to the Microsoft Defender portal at security.microsoft.com, then navigate to **Exposure Management** \> **Attack surface** \> **Attack paths**. The attack path experience provides three primary views: the Overview tab, the Attack paths list tab, and the Choke points tab.

The **Overview tab** displays a visual summary of your attack path data. You see a trend chart showing attack paths over time, the top five choke points where multiple paths converge, the top five attack path scenarios sorted by risk, and lists of top targets and top entry points.

The **Attack paths list tab** shows a filterable table of all detected attack paths in your environment. You can filter by risk level (High, Medium, Low), asset type, remediation status, or time frame such as the last 30 days. Select an attack path from the list to open the Attack Path Map, a graph\-based visualization that highlights vulnerable nodes, entry points, target assets, and choke points.

The **Choke points tab** lists nodes where multiple attack paths intersect. These are the highest\-leverage remediation targets — resolving a security issue at a choke point can break several attack paths simultaneously.

Note

You may see an empty attack paths list. This is expected behavior and indicates that the algorithm found no confirmed externally exploitable paths to your critical assets — a positive security signal.

### Investigate an attack path map

When you select an attack path from the list, the Attack Path Map opens to show you the full exploitation chain. For example, consider an attack path titled "Internet\-exposed VM can reach Azure OpenAI endpoint with access to patient health data." The map displays this chain visually: an entry point (internet\-exposed VM) connects to a vulnerable node (VM with CVE vulnerability), which connects to a choke point (storage account shared between services), which ultimately reaches the target asset (Azure OpenAI service with access to patient health data).

Select any node in the map to open its details panel. You see the MITRE ATT\&CK tactics and techniques relevant to that step — for example, Initial Access for the entry point, Lateral Movement for intermediate nodes, or Exfiltration for nodes near sensitive data. The panel also lists risk factors such as excessive permissions, internet exposure, or unpatched vulnerabilities.

The details panel includes a **Recommendations** section with two categories. **Recommendations** are security fixes that break this attack path entirely — resolving these removes the path from your environment. **Additional recommendations** reduce exploitation risk but don't fully break the path when resolved alone — they're still valuable to address as defense\-in\-depth measures. Each recommendation includes its risk level, affected resources, and remediation guidance.

Once you remediate the necessary recommendations, it can take up to 24 hours for the resolved path to be removed from the list.

### How attack paths extend to AI workloads

Defender CSPM's attack path analysis extends to AI workloads deployed on Azure OpenAI Service, Azure AI Foundry, Azure Machine Learning, Amazon Bedrock, and Google Vertex AI.

Attack path analysis identifies scenarios where AI model training data, fine\-tuning datasets, and inference data are at risk during model grounding operations. For example, an internet\-exposed compute resource with excessive managed identity permissions could reach an Azure AI Foundry project with access to the medical records dataset used for model grounding.

Attack path analysis surfaces this exploitation chain and highlights the specific security issues that enable the lateral movement — such as overly permissive role assignments or publicly exposed AI service endpoints.

AI\-specific attack path findings appear in the same attack paths list and map view you use for traditional infrastructure. Target assets are labeled as AI model data or AI service endpoints, making it clear when an attack path threatens AI workloads.

Attack path analysis shows you the exploitation chains that already exist in your environment.

---

## Hunt for risks with cloud security explorer

Contoso Healthcare's security team has reviewed recommendations and attack paths, gaining insight into known risks. Now they want to go further—proactively hunting for risk patterns that may not yet surface in the standard recommendations list. For example, are there VMs with known vulnerabilities that also have internet exposure and access to sensitive storage accounts? Are there identity permissions that could enable lateral movement to the AI services? Here, you learn to use Cloud Security Explorer to build custom graph\-based queries that uncover hidden risk combinations in your environment.

| Query Component | Purpose | Example |
| --- | --- | --- |
| Resource type | Starting point for your query | Virtual machines, Storage accounts, Azure AI services |
| Filter conditions | Criteria that narrow results | Internet exposed, has vulnerabilities, contains sensitive data |
| Relationship filters | Connections between resources | VM "has access to" Storage account |
| Results | Assets matching all conditions | Specific resources requiring remediation |

### Understand cloud security explorer and the security graph

Cloud Security Explorer uses the cloud security graph, Defender for Cloud's context engine that maps relationships between resources, identities, data, network exposure, and security findings. Unlike recommendations that surface algorithmically determined risks, the explorer lets you bring your own questions to the data.

The security graph is updated through snapshot publishing, a method of refreshing data at regular intervals. Snapshot publishing ensures that your workload configuration data remains fresh with daily updates.

With this foundation, you build custom multi\-resource queries to find risk combinations that standard recommendations might miss. For example, you can query "find all VMs with high\-severity vulnerabilities that are internet\-exposed and have access to storage accounts containing sensitive data." This type of query reveals compound risks — situations where multiple factors combine to create significant exposure.

### Navigate and build queries in Cloud Security Explorer

Cloud Security Explorer is accessed through the Azure portal, providing a dedicated interface for proactive risk hunting.

Note

Cloud Security Explorer is available in the Azure portal. Sign in at portal.azure.com and navigate to **Microsoft Defender for Cloud** \> **Cloud Security Explorer**.

Building a query follows a structured workflow that transforms security questions into actionable results:

1. Select a resource type from the dropdown menu (for example, Virtual machines, Storage accounts, Azure AI services).
2. Select the **\+** button to add filter conditions (for example, internet exposed, has high\-severity vulnerabilities, connected to storage).
3. Add additional resource types and relationship filters as needed to create chained conditions.
4. Select **Search** to run the query against the security graph.
5. Review the results—each row represents an asset matching all specified conditions.
6. Select **Download CSV report** to export results for remediation tracking or reporting to stakeholders.

Filters are grouped into logical categories including asset type, exposure, permissions, vulnerabilities, network connections, and lateral movement potential.

You can chain multiple resource types using relationship filters to model real attack scenarios. For example, construct a query for a VM that "has access to" a storage account, which "contains" sensitive data. This chaining capability mirrors how attackers move through environments, exploiting relationships between resources to reach high\-value targets.

### Use query templates for common risk patterns

The bottom of the Cloud Security Explorer page provides prebuilt query templates that cover common risk scenarios preconfigured for immediate use. Templates eliminate the need to construct queries from scratch, offering a practical starting point for establishing regular proactive hunting practices.

Templates cover scenarios such as:

* Internet\-exposed VMs with high\-severity vulnerabilities
* Storage accounts with sensitive data that are accessible from the internet
* Resources with exposed secrets (credentials, tokens, or keys found in environment variables or code)
* Resources with managed identity permissions that could enable lateral movement across the tenant

To use a template, find it at the bottom of the Cloud Security Explorer page and select **Open query**. The template pre\-populates the query builder with filters and conditions, which you can modify before selecting **Search**.

When AWS or GCP cloud connectors are active and Defender CSPM is enabled on those accounts, the same explorer interface supports multicloud queries. Organizations with hybrid cloud architectures can extend these hunting practices across all connected cloud platforms.

### Share and export query results

Queries can be shared with team members using the **Share query link** button, which copies a shareable URL to your clipboard. When a query reveals a risk cluster, share the link with workload owners or governance teams to ensure coordinated response. Select **Download CSV report** to export results for remediation tracking or reporting.

---

## Knowledge check

Answer the following questions to check your understanding of Cloud Security Posture Management in Microsoft Defender for Cloud.

### Check your knowledge

---

## Summary

You now have a structured, risk\-driven approach to identify security risks across cloud and AI workloads. For Contoso Healthcare Systems, this means turning hundreds of daily security findings into a prioritized, actionable set of insights that protect their patient triage assistant and medical records summarization services.

You explored how Foundational CSPM provides basic posture visibility, while Defender CSPM unlocks advanced capabilities including AI Bill of Materials discovery, attack path analysis, and the Cloud Security Explorer. The Cloud Overview dashboard and AI workload discovery features give Contoso's security team dedicated visibility into their Azure OpenAI and Azure AI Foundry deployments alongside their broader Azure workloads.

You learned to interpret the Cloud Secure Score using the risk\-based prioritization model in the Microsoft Defender portal. As a security specialist, by understanding how internet exposure, data sensitivity, criticality, and lateral movement potential combine to surface the most dangerous vulnerabilities first, Contoso can focus remediation efforts where they matter most. AI\-specific recommendations ensure their generative AI workloads receive appropriate security attention.

You used attack path analysis to identify externally exploitable paths targeting high\-value assets, including AI workloads. The Attack Path Map reveals entry points, choke points, and vulnerable nodes along MITRE ATT\&CK\-contextualized attack chains, helping Contoso understand realistic attacker scenarios before exploitation occurs.

You ran graph\-based queries in Cloud Security Explorer to proactively hunt for risks across Azure environments. Prebuilt templates and custom queries let Contoso's team discover misconfigurations, exposure patterns, and compliance gaps that traditional scans might miss.

With these capabilities, Contoso's security team can assess posture coverage, prioritize the most dangerous findings, trace exploitation chains, and proactively hunt for hidden risks—shifting from reactive alert response to continuous, context\-aware risk identification.

### Learn more

* [What is Cloud Security Posture Management (CSPM)](/en-us/azure/defender-for-cloud/concept-cloud-security-posture-management)
* [Risk prioritization in Defender for Cloud](/en-us/azure/defender-for-cloud/risk-prioritization)
* [Overview: AI security posture management](/en-us/azure/defender-for-cloud/ai-security-posture)
* [Identify and remediate attack paths](/en-us/azure/defender-for-cloud/how-to-manage-attack-path)
* [Build queries with Cloud Security Explorer](/en-us/azure/defender-for-cloud/how-to-manage-cloud-security-explorer)
* [Enable Defender CSPM](/en-us/azure/defender-for-cloud/tutorial-enable-cspm-plan)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/identify-security-risks-posture-management/_

## Fuentes
- [Identify security risks by using Cloud Security Posture Management](https://learn.microsoft.com/en-us/training/modules/identify-security-risks-posture-management/?WT.mc_id=api_CatalogApi)
