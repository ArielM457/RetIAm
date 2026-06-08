# Evaluate regulatory compliance in Defender for Cloud

> Curso: Manage security posture by using Microsoft Defender for Cloud (wwl-manage-security-posture-defender-cloud) · Seccion: Manage security posture by using Microsoft Defender for Cloud
> Duracion estimada: 23 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Healthcare Systems spent the past quarter surfacing and prioritizing cloud security risks using Microsoft Defender for Cloud. The security team now faces a different kind of challenge. The Security Officer (CISO) received a request from the compliance and legal teams: *"We need to demonstrate by end of quarter that our Azure environment meets ISO 27001 and NIST SP 800\-53 requirements. Can you show us where we stand, identify the gaps, and produce an audit report?"*

The team knows their environment has misconfigurations and vulnerabilities. What they don't yet know is how those security findings map to specific compliance framework controls—or how to communicate that mapping to auditors, legal counsel, and executive stakeholders in a format they can act on.

Microsoft Defender for Cloud's regulatory compliance capabilities connects security posture work to the compliance frameworks that matter to the organization. Every security recommendation that Defender for Cloud generates also maps to one or more compliance controls. The regulatory compliance dashboard makes that mapping visible, measurable, and reportable.

In this module, you learn to use Defender for Cloud to evaluate compliance posture. Specifically, you:

* Explain how compliance standards, controls, and assessments work in Defender for Cloud—including the role of the Microsoft Cloud Security Benchmark
* Navigate the regulatory compliance dashboard to identify and investigate failing compliance controls
* Assign regulatory compliance standards to Azure subscriptions and manage compliance scope in the Azure portal
* Generate compliance reports and communicate posture using audit downloads, compliance workbooks, and Microsoft Purview Compliance Manager

---

## Understand compliance standards and controls in Defender for Cloud

Before Contoso Healthcare's security team demonstrates compliance with ISO 27001 and National Institute of Standards and Technology (NIST) SP\-800\-53 to auditors, they need to understand how Defender for Cloud's compliance model works. The compliance dashboard provides a comprehensive view of an organization's security posture against industry standards, but interpreting that data requires knowledge of how standards, controls, and assessments function together. Here, you learn what compliance standards are, how Defender for Cloud evaluates them, and where to perform compliance management tasks.

### Compliance standards in Defender for Cloud

Compliance standards in Defender for Cloud represent industry, regulatory, and organizational guidelines used to assess resource configurations across your cloud environment. Defender for Cloud supports three types of standards that organizations use to measure security posture.

Security benchmarks provide built\-in baselines for cloud security best practices. The Microsoft Cloud Security Benchmark (MCSB) serves as the primary example—a comprehensive set of security recommendations based on common compliance frameworks including CIS and NIST. Organizations use these benchmarks as a foundation before layering on specific regulatory requirements.

Regulatory compliance standards reflect frameworks from industry programs and government regulations. Established examples include ISO 27001 for information security management, NIST SP 800\-53 for federal systems, and PCI\-DSS for payment card data. Emerging frameworks like DORA for financial resilience and the EU AI Act for artificial intelligence systems are also supported. For Contoso Healthcare, ISO 27001 and NIST SP 800\-53 represent the two critical frameworks auditors evaluate during compliance reviews.

Custom standards allow organizations to define assessments aligned to internal policies. These organization\-specific frameworks support vendor requirements, corporate security policies, or industry\-specific controls beyond standard frameworks. Creating and managing custom standards requires Defender for Cloud CSPM (Cloud Security Posture Management) enabled on the subscription.

Standards are assigned to specific scopes—Azure subscriptions, management groups, AWS accounts, or GCP projects. Once assigned, Defender for Cloud continuously evaluates all in\-scope resources against the controls defined in that standard, updating compliance scores as resources change.

### The Microsoft Cloud Security Benchmark

MCSB is the default standard enabled automatically when you activate Defender for Cloud on a subscription. Microsoft authored this benchmark to provide security and compliance best practices based on common compliance frameworks. The benchmark applies across Azure, AWS, and GCP, giving multicloud organizations a consistent security baseline.

Note

MCSB v2 is available in preview. This version introduces expanded risk\-based controls, broader Azure Policy mappings, and coverage for emerging workloads including AI. You can enable it from the Regulatory compliance dashboard alongside the current default MCSB.

Other default benchmarks apply for non\-Azure clouds. When you connect AWS accounts to Defender for Cloud, both MCSB and the AWS Foundational Security Best Practices standard are enabled by default. For GCP projects, both MCSB and the GCP Default benchmark are enabled by default. These cloud\-specific standards complement MCSB by providing native security guidance for each platform.

### Compliance controls and assessment states

A compliance standard consists of multiple compliance controls—logical groups of related security recommendations. Each control represents a specific security requirement from the standard. Defender for Cloud continuously assesses in\-scope resources against controls that support automated evaluation.

Three assessment states indicate compliance status for each control:

| Assessment State | Visual Indicator | Meaning |
| --- | --- | --- |
| Passing | Green circle | All in\-scope resources are compliant with the control |
| Failing | Red circle | One or more resources aren't compliant |
| Not available | Greyed out | The control can't be automatically assessed |

The following diagram shows how these states appear when you drill into a single control. ISO 27001 control A.9\.1 breaks into two subcontrols, each with its own assessment state and the specific Defender for Cloud assessments that drive it.

The third state—greyed out controls—often causes confusion during initial compliance reviews. These controls represent requirements Defender for Cloud can't automate, not missing security coverage. Grayed\-out controls typically fall into three categories: procedural or process controls (like security awareness training requirements), platform responsibilities under the shared responsibility model (physical datacenter security), or controls with no implemented automated assessment yet. For Contoso Healthcare, ISO 27001 includes many process\-oriented controls that require manual attestation rather than automated validation.

Manual attestation allows security teams to mark grayed\-out controls as compliant after completing manual verification. This capability ensures compliance scores accurately reflect an organization's full security posture, combining automated assessments with manual evidence.

### Working across the Azure and Defender portals

Compliance management spans two portals with distinct responsibilities. Understanding where to perform each task prevents confusion when configuring standards or reviewing compliance data.

The Azure portal at `portal.azure.com` serves as the configuration hub for compliance standards. You assign standards to subscriptions, configure scope, manage underlying Azure policies, and create custom standards in the Azure portal. To add a standard, you need **Owner** or **Policy Contributor** permissions on the subscription. To manage standards and access the full compliance dashboard, **Resource Policy Contributor** and **Security Admin** roles are required at minimum. Adding nondefault regulatory standards requires at least one paid Defender plan enabled—any Defender plan except Defender for Servers Plan 1 or Defender for API Plan 1\.

The Defender portal at `security.microsoft.com` provides the monitoring interface for compliance status. You view compliance scores, examine control details, filter security recommendations by framework, and track remediation progress in the Defender portal. This portal offers read\-only access to compliance data, making it ideal for security operations teams who monitor compliance without managing policy assignments. To view compliance data in the Defender portal, you need Reader role on the subscription—Security Reader role doesn't provide access to policy compliance data.

For Contoso Healthcare's security engineer, the typical workflow starts in the Azure portal to assign ISO 27001 and NIST SP 800\-53 standards. From there, the engineer switches to the Defender portal to monitor compliance scores and identify failing controls that require remediation.

In the next unit, you navigate the Regulatory compliance dashboard to see these standards and controls in action, learning how to interpret compliance scores and identify security gaps that need attention.

---

## Navigate the regulatory compliance dashboard and investigate control gaps

Assigning compliance standards is only the first step in building a compliance program. The real work begins when you investigate which controls are passing, which are failing, and what actions you must take to close the gaps. For Contoso Healthcare, the Security Officer (CISO) needs a report identifying ISO 27001 control failures before the upcoming audit. Here, you learn how to navigate the regulatory compliance dashboard, drill into failing controls, and trace them to specific resource recommendations.

| Navigation Stage | Purpose |
| --- | --- |
| Dashboard overview | Identify lowest\-performing standards and overall pass rates |
| Standard drill\-down | Review control status by category and access control details |
| Assessment investigation | Link failing controls to affected resources and remediation steps |
| Recommendation filtering | Focus remediation work on controls that influence specific frameworks |

### The compliance dashboard in the Defender portal

The regulatory compliance dashboard provides a centralized view of your organization's compliance posture across all assigned standards. You access the dashboard through the Defender portal at `https://security.microsoft.com` by navigating to **Cloud security** \> **Regulatory compliance**.

At the top of the dashboard, you see a summary of your lowest\-performing standards, highlighting which frameworks need immediate attention. Next, the dashboard displays each assigned compliance standard with its current pass rate. For Contoso Healthcare, ISO 27001 appears in this list with a percentage indicating how many of its controls currently pass automated assessments.

Selecting a compliance standard expands it to show all controls organized by category. The color\-coded pass, fail, and unavailable states let you quickly identify which categories need attention and prioritize your investigation based on the number of failing controls.

### Drilling into a standard and its controls

When you select an individual control, you access detailed information through the **Control details** pane. This pane organizes information into three tabs that clarify responsibilities and actions.

The **Overview** tab describes the control requirement and explains what the control protects against. The **Your Actions** tab shows both automated and manual assessments that your organization owns under the shared responsibility model. Automated assessments link directly to Defender for Cloud recommendations, while manual assessments require you to provide attestation with supporting evidence. The **Microsoft Actions** tab displays platform\-level controls that Microsoft manages, demonstrating how shared responsibility works in practice.

Under **Your Actions**, you find the specific assessments that Defender for Cloud uses to evaluate this control. Each automated assessment shows how many resources pass or fail, and selecting a failing assessment takes you directly to the affected resources with remediation guidance.

### Investigating a failing assessment

The following diagram shows the full investigation path—from opening the dashboard to verifying a remediated control.

Following Contoso Healthcare's ISO 27001 review, you identify that a network controls assessment is failing under ISO 27001 A.13\.1\.1\. This control maps to the recommendation "Storage accounts should restrict network access."

Selecting this recommendation opens a detailed view showing all affected storage accounts. You see that three storage accounts currently allow public network access, creating compliance violations. Selecting one of the affected resources displays the remediation steps in the right pane.

For each storage account, the recommended action is to configure network rules that restrict access to specific virtual networks or IP address ranges. After you apply these network restrictions through the Azure portal or Infrastructure as Code templates, wait for the next assessment cycle before the dashboard reflects the change.

Note

Compliance assessments run approximately every 12 hours. After remediating a failing control, wait for the next assessment cycle before the compliance dashboard reflects the updated status.

This investigation pattern connects the high\-level control requirement to specific Azure resources that need configuration changes. By tracing from control to recommendation to resource, you create a clear remediation path that your team can execute.

### Filtering recommendations by compliance framework

The **Recommendations** page in the Defender portal supports compliance\-focused work through framework filtering. Select the filter icon and choose a specific compliance standard to display only recommendations that affect controls in that framework.

This filtering helps you focus sprint work on a single framework or track remediation progress against an audit deadline. For Contoso Healthcare, filtering recommendations by ISO 27001 shows exactly which security improvements contribute to their upcoming audit readiness.

Filtering by framework also helps you understand the overlap between compliance requirements and general security posture. Many recommendations satisfy multiple compliance controls simultaneously, so remediating one issue often improves your standing across several standards.

---

## Assign standards and communicate compliance posture

After investigating gaps in the ISO 27001 dashboard, Contoso Healthcare's Security Officer (CISO) now needs broader visibility. The security team must add NIST SP 800\-53 for federal client requirements, generate audit reports for the external compliance team, and provide a unified compliance view across all of Contoso's digital assets—not just Azure. Here, you learn how to assign other standards, generate audit\-ready reports, and integrate cloud infrastructure compliance data with Microsoft Purview Compliance Manager.

### Assign compliance standards in the Azure portal

Standard assignment and policy configuration happen in the Azure portal—not the Defender portal. The Defender portal provides a read\-only view of compliance data, but you manage which standards to monitor through the Azure portal's security policy interface.

To assign a standard:

1. Sign in to the [Azure portal](https://portal.azure.com) and open **Microsoft Defender for Cloud**.
2. Select **Regulatory compliance**, then choose **Manage compliance policies**.
3. Select your subscription or management group.
4. Navigate to **Security policies**.
5. Locate the standard you want to enable and toggle the status to **On**.

After you enable a standard, Defender for Cloud begins evaluating your resources against that standard's controls.

| Configuration aspect | Key consideration |
| --- | --- |
| Required permissions | Owner or Policy Contributor role on the subscription |
| Required prerequisites | Any Defender plan enabled—except Defender for Servers Plan 1 or Defender for API Plan 1 |
| Recommended scope | Assign at management group level for aggregate tracking |
| Initial data population | Up to 12 hours for first assessment results |

Standard assignment follows Azure Policy's scope hierarchy. When you assign a standard at a management group level, all nested subscriptions inherit the assignment and contribute to aggregate compliance tracking. This approach gives you organization\-wide visibility rather than subscription\-by\-subscription reporting. If you assign a standard but have no resources in scope—for example, enabling PCI\-DSS when you have no payment systems—the standard doesn't appear in the dashboard until relevant resources exist.

Available standards include ISO 27001, NIST SP 800\-53, PCI\-DSS, CIS benchmarks, SOC 2, FedRAMP, and HIPAA. Microsoft adds new standards regularly based on customer demand and regulatory landscape changes.

Note

Microsoft added several new standards to the compliance dashboard in mid\-2025, including the Digital Operational Resilience Act (DORA), the European Union Artificial Intelligence Act (EU AI Act), the Korean Information Security Management System for Public Cloud (k\-ISMS\-P), and the CIS Microsoft Azure Foundations Benchmark v3\.0\. Check the Defender for Cloud documentation to confirm current availability before including any of these standards in production compliance programs.

### Download audit reports

After a standard completes its initial assessment, you can generate audit\-ready reports directly from the compliance dashboard. Auditors typically request point\-in\-time compliance evidence, and the PDF report format provides exactly that—a formatted summary showing overall compliance percentage, control\-by\-control status, and resource\-level findings.

To download a report:

1. Open the compliance dashboard in either the Azure portal or the Defender portal.
2. Select the standard you want to report on.
3. Select **Download report**.
4. Choose your format:
	* **PDF** \- formatted summary for auditors and stakeholders, including compliance score, control\-by\-control status, and remediation recommendations.
	* **CSV** \- underlying assessment data with resource\-level detail for each control, suited for spreadsheet analysis and governance tools.

Beyond point\-in\-time reports, the **Compliance over time workbook** tracks compliance score trends for each standard. This workbook demonstrates continuous improvement posture—a key requirement for many audit frameworks—by visualizing how your compliance score changes as you remediate findings and onboard new resources.

### Integrate with Microsoft Purview Compliance Manager

Defender for Cloud integrates with Microsoft Purview Compliance Manager to provide unified compliance visibility across your entire digital estate. When you add any standard to the Defender for Cloud compliance dashboard—including standards monitoring AWS and GCP resources—the resource\-level compliance data automatically surfaces in Compliance Manager for the same standard.

This integration bridges the gap between security operations and compliance management. The security team configures standards and remediates findings in Defender for Cloud, while the legal and compliance team manages improvement actions and status in Compliance Manager. Compliance Manager aggregates data from Microsoft 365, endpoints, cloud infrastructure, and on\-premises systems into a single compliance view. For Contoso Healthcare, compliance view means the CISO sees patient data compliance across Azure storage accounts, Microsoft 365 mailboxes, and on\-premises file servers in one dashboard.

No more configuration is required—the integration activates automatically when you assign standards in Defender for Cloud.

Note

Allow up to seven days for Compliance Manager to fully collect and factor in initial compliance data. Smaller, single\-subscription environments typically populate faster—the seven\-day window reflects large multicloud deployments where data aggregates across many subscriptions.

### Create custom standards with Defender CSPM

Built\-in standards cover major regulatory frameworks, but organizations often need custom security baselines aligned to internal policies or industry\-specific requirements. Custom standards and recommendations appear in the regulatory compliance dashboard alongside built\-in frameworks. All customers can create custom recommendations based on Azure Policy. To create custom recommendations using KQL queries, the **Defender CSPM** paid plan is required.

Custom recommendations use KQL (Kusto Query Language) queries to evaluate resource configurations against your specific requirements. For example, Contoso Healthcare might create a "Healthcare Data Security Baseline" that enforces encryption and network isolation rules on storage accounts containing patient data—requirements more specific than HIPAA's general controls. These custom recommendations integrate into the compliance dashboard with the same assessment, scoring, and remediation workflow as built\-in standards.

With standards assigned and reports generated, Contoso's security team can provide the CISO with both a current compliance snapshot, and a trend workbook that demonstrates progress over time.

---

## Knowledge check

Answer the following questions to check your understanding of regulatory compliance in Microsoft Defender for Cloud.

### Check your knowledge

---

## Summary

Contoso Healthcare's security team can now answer the Security Officer's (CISO) compliance question with precision. By using Microsoft Defender for Cloud's regulatory compliance capabilities, they mapped their cloud security findings to the frameworks that matter to the organization—ISO 27001, National Institute of Standards and Technology (NIST) SP\-800\-53, and their internal baseline—and produced the audit\-ready reports the compliance team requested.

You explored how compliance standards, controls, and assessments work in Defender for Cloud. The Microsoft Cloud Security Benchmark is enabled by default and provides coverage across Azure, AWS, and GCP. Regulatory standards, custom standards, and security benchmarks give organizations flexibility to assess resources against the frameworks most relevant to their industry and obligations. Understanding the three assessment states—passing, failing, and grayed out—tells you where automated remediation is possible and where manual attestation applies.

You navigated the regulatory compliance dashboard in the Defender portal to identify failing controls across assigned standards. Drilling into a control reveals Overview, Your Actions, and Microsoft Actions tabs that clarify shared responsibility and provide direct remediation paths. Filtering recommendations by compliance framework connects the risk\-prioritized posture work to specific audit obligations—every recommendation is also a control gap waiting to be closed.

You assigned other regulatory standards in the Azure portal, including industry frameworks and emerging standards such as DORA and the EU AI Act. You generated downloadable audit reports and used the compliance over time workbook to show continuous improvement rather than a single point\-in\-time snapshot. The integration with Microsoft Purview Compliance Manager automatically surfaced cloud infrastructure compliance data in the organization's broader compliance management platform, giving Contoso's CISO a unified view across all digital assets.

With these capabilities, Contoso's security and compliance teams can operate from shared data—the security engineer remediates risks, and those remediations immediately improve compliance posture against every applicable standard.

### Learn more

* [What is regulatory compliance in Defender for Cloud](/en-us/azure/defender-for-cloud/concept-regulatory-compliance-standards)
* [Improve regulatory compliance](/en-us/azure/defender-for-cloud/regulatory-compliance-dashboard)
* [Assign regulatory compliance standards](/en-us/azure/defender-for-cloud/assign-regulatory-compliance-standards)
* [Microsoft Cloud Security Benchmark in Defender for Cloud](/en-us/azure/defender-for-cloud/concept-regulatory-compliance)
* [Create custom security standards and recommendations](/en-us/azure/defender-for-cloud/create-custom-recommendations)
* [Microsoft Purview Compliance Manager multicloud support](/en-us/microsoft-365/compliance/compliance-manager-multicloud)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/evaluate-regulatory-compliance/_

## Fuentes
- [Evaluate regulatory compliance in Defender for Cloud](https://learn.microsoft.com/en-us/training/modules/evaluate-regulatory-compliance/?WT.mc_id=api_CatalogApi)
