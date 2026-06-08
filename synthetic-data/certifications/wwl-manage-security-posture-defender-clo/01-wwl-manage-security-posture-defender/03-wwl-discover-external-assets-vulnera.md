# Discover unprotected assets and vulnerabilities by using Microsoft Defender External Attack Surface Management

> Curso: Manage security posture by using Microsoft Defender for Cloud (wwl-manage-security-posture-defender-cloud) · Seccion: Manage security posture by using Microsoft Defender for Cloud
> Duracion estimada: 35 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Financial Services recently completed a major cloud migration to Azure and acquired a regional banking partner. Their security team uses Microsoft Defender for Cloud's Cloud Security Posture Management (CSPM) capabilities to monitor known Azure resources and Microsoft Defender Vulnerability Management (MDVM) to scan enrolled virtual machines for software vulnerabilities. However, security leadership is concerned about internet\-facing assets they don't know about: forgotten test environments, infrastructure inherited from the acquisition with no existing inventory, and developer\-created resources that bypass central IT. Traditional vulnerability scanners can't see beyond the firewall, and MDVM only scans VMs that are already enrolled and managed. The team needs an outside\-in perspective to discover what attackers can actually see when they scan Contoso's internet presence.

Microsoft Defender External Attack Surface Management (EASM) provides exactly this attacker's\-eye view by continuously discovering internet\-facing assets you own or operate, even if you don't know about them yet. EASM complements your inside\-out CSPM and vulnerability scanning by finding unknown assets, mapping their connections, and identifying security hygiene risks. These risks include expired certificates, open ports, exposed services, and OWASP vulnerabilities—all viewed from the perspective of an attacker scanning your organization from the outside.

In this module, you learn to use EASM to discover and secure your external attack surface. Specifically, you:

* Explain how EASM outside\-in discovery complements inside\-out CSPM posture management
* Configure asset discovery using seeds to identify unknown internet\-facing infrastructure and asset connections
* Use EASM dashboards to prioritize vulnerabilities and security hygiene risks across your attack surface
* Integrate EASM findings with Defender CSPM to analyze attack paths starting from internet\-exposed resources

---

## Explore EASM features and capabilities

Contoso Financial Services uses Cloud Security Posture Management (CSPM)—which assesses Azure resources for misconfigurations from the inside out—and Microsoft Defender Vulnerability Management (MDVM)—which scans enrolled VMs for software vulnerabilities. After their recent acquisition, the security team realized neither tool has visibility into what the acquired company exposed to the internet—because neither tool knows those assets exist. Defender EASM operates from the opposite direction: it starts from the internet and works inward. Here, you explore how EASM is deployed, what it scans, and what it produces.

### Deploy EASM as an Azure resource

Defender EASM is deployed as a standalone Azure resource through the Azure portal. Each EASM workspace is scoped to an Azure subscription and resource group, and is provisioned in a supported region. Once deployed, the EASM scanning engine continuously queries public internet data sources—it doesn't require agents, network access, or enrollment in the target infrastructure. Everything it discovers is based on publicly available data.

The scanning engine uses Microsoft's proprietary recursive technology to map assets connected to seeds you provide. Seeds are known, legitimate assets such as your organization's primary domains, registered IP blocks, or ASNs. From each seed, EASM queries multiple public data sources to discover related infrastructure, then recurses through those connections to expand the map. The next unit covers discovery configuration in detail.

#### Deploying an EASM workspace

To deploy EASM, you need at least **Contributor** access to the Azure subscription and resource group where the workspace is created. The deployment takes place entirely in the Azure portal—no agent or network changes are required. At a high level, the steps are:

1. In the Azure portal, search for **Microsoft Defender EASM** and select **Create**.
2. Select or create a **resource group** in a supported region (such as East US or West Europe).
3. Name the workspace and select **Review \+ create**, then **Create**.
4. Once the resource is provisioned, open it and select **Getting Started** to search for your organization's prebuilt attack surface or configure a custom discovery group.

Once deployed, the workspace begins discovery in the background. The portal shows discovery progress through the run history on the **Discovery** page.

#### Operating EASM—roles and Zero Trust alignment

Once the workspace exists, day\-to\-day operations require a defined set of permissions. Following the Zero Trust principle of **least privilege**, assign only the access level each team member needs:

| Role | What they can do |
| --- | --- |
| **Owner / Contributor** | Create, edit, and delete EASM resources and inventory assets; configure discovery groups; manage labels |
| **Reader** | View inventory, dashboards, and findings—read\-only; can't modify any asset or configuration |

Defender EASM does **not** support cross\-tenant resource access, including via Azure Lighthouse. Each EASM resource must be accessed by authenticating directly to the tenant where it was created. This constraint reinforces Zero Trust's **verify explicitly** principle—every access request to EASM data must come from an authenticated identity in the same tenant, with no implicit trust granted across organizational boundaries.

### Distinguish EASM from other security tools

EASM operates from a different vantage point than CSPM and MDVM. Where CSPM assesses known Azure resources from the inside out and MDVM scans enrolled VMs for software vulnerabilities, EASM discovers all internet\-facing infrastructure from an attacker's outside\-in perspective—including assets not in the inventory yet.

Note

EASM and MDVM both surface CVE\-related findings, but from opposite directions. MDVM identifies CVEs in software installed on enrolled VMs. EASM identifies CVEs in services exposed on the public internet, whether or not those hosts are enrolled in any management system.

### Examine what EASM discovers

EASM catalogs eight types of internet\-facing assets:

| Asset type | Description |
| --- | --- |
| **Domains** | Registered domain names associated with your organization |
| **Hosts** | Subdomains and fully qualified domain names (FQDNs) |
| **Pages** | Web pages including sign in portals and admin interfaces |
| **IP blocks** | IP address ranges associated with your network |
| **IP addresses** | Individual internet\-facing IPs |
| **Autonomous System Numbers (ASNs)** | Routing identifiers for your network infrastructure |
| **SSL certificates** | TLS certificates linked to your hosts and domains |
| **WHOIS contacts** | Registrant contact data associated with your domains |

Each discovered asset is assigned to a \*\*state—such as **Approved inventory**, **Candidate**, or **Dependency** \- that defines its relationship to your organization. The discovery unit covers all five states and how to use them when reviewing your inventory.

Findings across discovered assets are assigned to a severity rating—high, medium, or low—based on Microsoft assessment of potential issues. High\-severity findings include new or frequently exploited CVEs, easily exploitable vulnerabilities, and associations to known\-compromised infrastructure. Low\-severity findings include deprecated but noncritical technologies, infrastructure nearing expiration, and compliance misalignments. EASM identifies issues such as expired or weak SSL certificates, open administrative ports, services running deprecated protocols, known CVEs on internet\-exposed services, and IPs with poor reputation scores. Each finding links to the affected asset in the inventory for investigation.

OWASP Top 10 findings appear in a separate dedicated dashboard and use OWASP category classification—broken access control, cryptographic failures, injection, and so on—rather than EASM's high/medium/low scale. Both systems are covered in detail in the dashboard analysis unit later in this module.

### Explore EASM dashboards and Defender for Cloud integration

EASM includes eight dashboards that organize findings by risk category—including security posture, OWASP Top 10, data protection compliance, and an inventory changes view. The four highest\-value dashboards are covered in detail in the dashboard analysis unit later in this module.

EASM also integrates with Defender CSPM. The integration is included with the Defender CSPM plan and requires no extra license or configuration. It surfaces EASM outside\-in data in Defender for Cloud's attack path analysis and Cloud Security Explorer. The integration unit covers the specific query patterns it enables.

---

## Discover assets using recursive discovery

Contoso's security team knows the Azure resources in their subscription, but what about the test environment from two years ago that's still running? Or the regional partner's infrastructure they acquired last quarter? External Attack Surface Management uses recursive discovery to find these unknown assets by starting from what you know and expanding outward. Here, you learn how discovery seeds work, how to set up automated or custom discovery, and how to organize the assets External Attack Surface Management (EASM) finds.

| Discovery Phase | What Happens |
| --- | --- |
| 1\. Provide seeds | Supply known assets (domains, IP blocks, contacts) as starting points |
| 2\. Query data sources | EASM checks WHOIS, DNS, SSL certificates, ASN records for connections |
| 3\. Expand recursively | Each discovered asset becomes a seed for finding more connections |
| 4\. Populate inventory | Assets appear in your inventory organized by type and state |
| 5\. Schedule updates | Continuous scanning keeps your attack surface current |

### Examine recursive discovery

EASM finds assets you don't know about by following connections from assets you do know about. The discovery engine starts with **seeds** \- legitimate assets you provide as starting points—and expands recursively to map your entire internet\-facing attack surface.

Seeds can take several forms. You can provide domain names like `contoso.com`, IP address blocks your organization owns, specific hosts, email contacts used for domain registration, Autonomous System Numbers (ASNs), or WHOIS organization names. Each seed type unlocks different discovery paths through your infrastructure.

The discovery engine queries multiple data sources for each seed. From a domain seed like `contoso.com`, EASM queries WHOIS records to find other domains registered by the same contact email or organization. It queries DNS records to discover hosts, subdomains, IP blocks, and mail servers associated with the domain. SSL certificate databases reveal all hosts using certificates linked to your organization. ASN lookups find IP blocks under the same autonomous system. Each of these data sources provides a different view into your infrastructure's connections and ownership patterns.

From each first\-level connection, EASM discovers second\-level and third\-level connections, recursively expanding the search. Consider Contoso's scenario: Starting from `contoso.com`, EASM finds all hosts under that domain. For each host, it finds SSL certificates in use. Those certificates can be shared with other domains—including `contoso-partner.net` from the recent acquisition. The partner domain leads to more hosts, IP blocks, and infrastructure that shares certificates, WHOIS contacts, or network ownership.

### Configure your discovery approach

EASM offers two paths for building your attack surface: automated discovery with prebuilt attack surfaces, or custom discovery groups you configure yourself.

The automated attack surface approach is the fastest starting point. Microsoft maintains preconfigured attack surfaces for many large organizations, built from public data sources linking assets to company names and registrations. To access it:

1. Open your EASM instance and select **Getting Started** under **General**.
2. Search for your organization name.
3. Select **Build my Attack Surface**.

Discovery runs in the background, and your inventory populates in preview mode. This approach works well for established organizations with consistent branding and domain registration practices.

For organizations not in the prebuilt list—or to supplement automated discovery—you create custom discovery groups. A discovery group contains seed assets and a recurrence schedule for ongoing discovery. To create one:

1. In EASM, go to **Manage** \> **Discovery** \> **Add Discovery Group**.
2. Name the group and set the recurrence frequency (default: **Weekly**).
3. Add seeds—domains, IP blocks, hosts, ASNs, email contacts, or WHOIS organization names.
4. Optionally add exclusions for subsidiaries or assets outside your scope.
5. Select **Review \+ Create**, then **Create \& Run**.

Organize discovery groups by business unit, brand, or subsidiary—for example, separate groups for core infrastructure and acquired domains—to maintain clear boundaries as your attack surface evolves.

Tip

Start with the automated attack surface search before creating custom groups. Microsoft could have a preconfigured attack surface ready for your organization, saving time on initial setup.

### Organize and manage your asset inventory

As discovery runs, EASM populates your inventory with the eight asset types covered in the previous unit—domains, hosts, pages, IP blocks, IP addresses, ASNs, SSL certificates, and WHOIS contacts.

Every asset receives a **state** that defines its relationship to your organization. This state system helps Contoso's team manage the mixed infrastructure from their acquisition:

| State | Description |
| --- | --- |
| **Approved inventory** | Confirmed as owned by your organization; actively monitored and included in dashboard charts |
| **Candidate** | Has a connection to your seeds but needs manual review to confirm ownership |
| **Dependency** | Owned by an external but directly supports your approved assets (for example, a CDN or hosting provider) |
| **Monitor only** | Relevant to your attack surface but not directly controlled—used for franchises or related entities |
| **Requires investigation** | Low\-confidence connection; flagged for manual review to determine how it should be categorized |

When Contoso runs discovery after their acquisition, new assets surface as **Candidates** \- they appear connected to Contoso infrastructure through shared SSL certificates, WHOIS contacts, or network blocks, but aren't manually confirmed yet. The security team reviews these candidates and moves legitimate acquired assets to **Approved inventory** for ongoing monitoring. Former partner infrastructure that wasn't part of the acquisition can be marked **Requires investigation** and reviewed for removal or reassignment.

The **Dependency** state is useful for tracking external infrastructure your assets rely on. Dependency assets are tracked in your inventory but aren't included in dashboard charts by default—they represent external risk context rather than assets you're directly responsible for.

You use inventory filters to navigate large attack surfaces efficiently. Filter by asset type to focus on all domains or all IP blocks at once. Filter by state to review candidates needing confirmation or investigate assets flagged for review. Filter by discovery date to find recently added assets that represent new exposure from development activity or infrastructure changes. Combine filters to surface specific risks—for example, all hosts in candidate state discovered in the last 30 days.

### Maintain your attack surface over time

EASM continuously scans your attack surface, running scheduled discoveries to keep your inventory current as your infrastructure evolves.

Assets receive temporal tags based on their activity status. **Recent** assets are currently active—EASM observed them during the latest scan cycle. **Historic** assets were observed previously but no longer appear in current scans. Historic assets matter because they represent services you forgot about but that an attacker could still find and exploit. A development environment you think you decommissioned six months ago might still be running, and its historic tag alerts you to investigate.

The combination of continuous scanning and recursive discovery keeps your inventory current as your infrastructure changes—without requiring manual seed updates unless you're expanding into entirely new IP blocks or acquiring new organizations.

Now that you understand how to discover and organize your attack surface, you're ready to analyze what EASM found.

---

## Analyze your attack surface with dashboards

Discovering hundreds—or even thousands—of internet\-facing assets is valuable, but without context it's overwhelming. External Attack Surface Management (EASM) dashboards transform that raw inventory data into actionable risk intelligence, helping you identify which findings deserve attention first. In Contoso's case, the dashboards reveal which of those newly discovered assets pose the most immediate security risks. EASM includes eight dashboards; here, you learn how to use the four focused on security operations and vulnerability prioritization.

| Dashboard | Use it to... |
| --- | --- |
| **Overview** | Get an at\-a\-glance view of your attack surface and recent changes |
| **Attack surface summary** | Understand asset types, vulnerability distribution, and sensitive service exposure |
| **Security posture** | Identify CVE exposure, risky open ports, SSL issues, and domain risks |
| **OWASP Top 10** | Find web application vulnerabilities across your external\-facing pages |

### Navigate the Overview and Attack surface summary dashboards

EASM dashboards are analytical tools—they surface, prioritize, and contextualize findings across your attack surface by severity. They don't issue work orders or trigger fixes. Remediation happens in your external workflows or through the Defender for Cloud integration covered in the next unit. Think of these dashboards as giving you the full outside\-in view of your organization, organized by risk, so you know exactly what to hand off and why.

The Overview dashboard serves as your landing page when you open EASM. It provides immediate context: how many assets you have, how they're distributed by type, and which risks are flagged as high, medium, or low priority. For daily security operations, this dashboard offers a quick health check of your attack surface. You can see at a glance whether new high\-priority findings appeared overnight or whether recent remediation efforts reduced your risk counts.

The Attack surface summary dashboard goes deeper. It breaks down your full attack surface by asset type—domains, hosts, pages, IP blocks, SSL certificates, and autonomous system numbers (ASNs). Each asset type shows vulnerability severity counts with direct links to filter the inventory view. This dashboard answers critical questions about your infrastructure composition.

The cloud hosting breakdown reveals which providers host your external assets. For Contoso, this insight becomes valuable after the acquisition—some partner assets might be hosted on AWS or other cloud platforms rather than Azure. The sensitive services section highlights databases, remote management ports, and file\-sharing services accessible from the internet. You also see SSL certificate expiration timelines (30, 60, 90 days), domain expiry warnings, and IP reputation findings.

Important

IP reputation findings indicate that Microsoft detected signals—such as involvement in DDoS activity or associations with malicious behavior—linked to an owned IP address. A flagged IP can indicate the asset is susceptible to attack or already leveraged by a malicious actor. Investigate flagged IPs promptly, especially for acquired infrastructure where the operational history can be unknown to your team.

### Identify critical risks with the Security posture dashboard

The Security posture dashboard provides the most immediately actionable technical findings for remediation. It organizes discoveries into four critical categories that directly map to common attack vectors.

CVE exposure shows you external\-facing assets with known Common Vulnerabilities and Exposures—these are security flaws visible from the internet without requiring internal network access. Each finding includes the CVE identifier, Common Vulnerability Scoring System (CVSS) severity score, and affected asset count. You prioritize high\-severity CVEs that affect multiple assets first, since remediating one vulnerability across 10 hosts yields more risk reduction than addressing a medium\-severity issue on a single system.

The open ports and services section identifies exposed ports across your internet\-facing hosts and surfaces risky services. Telnet (port 23\), FTP (port 21\), Remote Desktop Protocol (port 3389\), and SMB (port 445\) are all considered high\-risk when exposed to the internet. For Contoso, recently acquired partner infrastructure, this analysis is critical. Older environments can have services exposed that would never pass security review in the main Azure environment. Legacy systems often accumulate technical debt, and external discovery reveals configurations that internal scans might miss if those systems weren't properly inventoried.

The SSL certificate configuration section flags multiple security hygiene issues. Expired certificates appear here, along with certificates using weak cipher suites or deprecated signature algorithms like SHA\-1 and MD5\. Self\-signed certificates on production hosts also generate findings—while appropriate for development, they undermine trust and encryption validation in production environments.

Domain administration findings focus on expiring domain registrations and misconfigured DNS records. An expired domain can be re\-registered by an attacker, who could then use it for phishing campaigns that appear to come from your organization. For Contoso, the post\-acquisition dashboard review reveals three critical findings: two hosts running Telnet from the acquired company's legacy infrastructure, 14 SSL certificates expiring within the next 30 days, and one domain registration expiring in 45 days—all on assets the team didn't know existed before EASM discovery.

### Find web application vulnerabilities with OWASP Top 10

The Open Web Application Security Project (OWASP) Top 10 dashboard evaluates your internet\-facing pages and hosts against the most critical web application security risks. These categories represent the most common and impactful vulnerabilities that attackers exploit in web applications.

Broken access control findings identify public\-facing pages that expose administrative functionality or allow unauthorized actions. Cryptographic failures include unencrypted data transmission, weak cipher suites, and improper certificate validation. Injection vulnerabilities appear when input fields are vulnerable to SQL injection, command injection, or other code execution attacks. Security misconfiguration findings flag default credentials, exposed configuration files, debug modes active in production, and enabled features.

The outdated components category identifies pages using vulnerable JavaScript libraries or frameworks. A common example appears when sites run outdated JavaScript libraries—such as older versions of jQuery or similar widely used frameworks—that have CVEs. These library vulnerabilities persist because web development teams can’t track their client\-side dependencies as rigorously as server\-side code. For Contoso, this dashboard becomes especially valuable for evaluating the acquired company's web applications, which likely lack the same security hardening as Contoso's main properties.

Note

EASM evaluates OWASP risks from an external perspective. It observes what's publicly accessible and detectable without authentication. Unlike penetration testing, it doesn't perform authenticated testing or attempt exploitation.

### Apply inventory filters to investigate findings

Every dashboard insight links directly to filtered inventory views. When you see a concerning finding—such as 14 hosts with expiring SSL certificates—you select that count to view the specific affected assets. The inventory view loads with filters already applied, showing you exactly which hosts need attention.

You can combine multiple filters to narrow your focus. Filter by asset state (Approved Inventory, Candidate, Requires Investigation), severity level, asset type, or discovery date range. For Contoso's scenario, filtering by discovery date helps distinguish between long\-standing assets and assets discovered through the acquisition integration. You can also apply custom labels to group assets for tracking purposes. Labeling all acquired partner assets as "PARTNER\-LEGACY" creates a persistent tag that helps you track remediation progress across that specific infrastructure subset.

The combination of dashboard insights and inventory filtering creates a workflow: identify the highest\-priority risk category in a dashboard, drill into the specific affected assets through the filtered inventory, investigate the context of each asset, and create remediation tasks for your operations teams. This systematic approach prevents the paralysis that comes from facing thousands of undifferentiated assets.

---

## Integrate EASM insights with Defender for Cloud

Contoso's security team discovered their external attack surface, organized their inventory, and identified critical findings in the acquired partner infrastructure. Now they need to connect the outside\-in insights with their existing Defender for Cloud tooling to get a unified view of their security posture. Here, you learn how EASM integrates with Defender Cloud Security Posture Management (CSPM) to enable attack path analysis and security queries that combine internet exposure data with internal findings.

Note

The built\-in Defender CSPM integration runs automatically with no extra licensing or configuration. If your organization needs the full EASM dashboards, custom discovery groups, and Security Exposure Management integration, which require a standalone Defender EASM workspace.

### Compare EASM integration options in Defender for Cloud

Defender CSPM manages the security posture of your known Azure resources from the inside out—assessing configurations, misconfigurations, and access controls within your environment. EASM adds the outside\-in view. When integrated, these two perspectives give you a complete, unified picture—what attackers can see from outside, what misconfigurations exist inside, and how those two views intersect.

EASM integrates with Defender for Cloud at two levels, depending on your organization's needs. The built\-in integration is available automatically with the Defender CSPM plan. No separate EASM license or configuration is needed. This integration enables discovery of all internet\-facing cloud resources through outside\-in scanning, attack path analysis starting from internet\-exposed IPs, and Cloud Security Explorer queries that combine exposure data with internal findings.

The full EASM workspace provides the comprehensive capabilities you explored in this module—all eight dashboards, custom discovery groups, and detailed inventory management. You create it as a dedicated Azure resource in the Azure portal and connect it to your tenant. This standalone resource connects to Microsoft Security Exposure Management (MSEM) for the External Attack Surface Protection initiative, giving security teams deeper discovery capabilities and unified external attack surface visibility.

For Contoso, this integration means their Cloud and AI Security Engineers can now analyze the three critical findings from the acquired partner infrastructure (discovered by EASM) alongside their existing Azure security posture (managed by CSPM) in a single workflow.

### Analyze attack paths from internet\-exposed resources

The scenarios in this section use the full EASM workspace configuration—the same standalone resource Contoso deployed to run custom discovery and manage their inventory in the previous units. This configuration feeds EASM inventory data directly into Defender CSPM's attack path engine.

Attack path analysis in Defender CSPM traces exploitable paths through your cloud environment—how an attacker could move from an initial foothold to a high\-value target. EASM integration extends this capability to include paths that start from internet\-exposed IPs discovered through outside\-in scanning.

Defender CSPM's attack path analysis finds all exploitable paths from internet\-exposed endpoints. With EASM data, the analysis includes IPs and resources discovered by EASM—not just resources already enrolled in your Azure subscription. An attack path might look like this: Internet\-exposed IP (discovered by EASM) → Misconfigured VM → SQL database with customer financial records.

Misconfigured resources matter for Contoso because CSPM alone could only trace attack paths starting from known Azure resources. With EASM integration, paths can now begin from the acquired partner infrastructure—hosts that Contoso didn't even know existed before their EASM deployment. EASM expands the visible attack surface to include assets that CSPM alone can't see.

To view attack paths with EASM context, navigate to **Cloud security** \> **Attack path analysis** in the Microsoft Defender portal. Filter attack paths by **Internet exposed** to surface paths that start from EASM\-discovered resources. Select a path to see the full chain from the internet\-exposed entry point to the internal target asset.

When Contoso's team filters by internet\-exposed attack paths, they find a high\-severity path that begins at one of the Telnet\-exposed hosts discovered by EASM on the acquired partner's domain. The path traverses through a misconfigured network peering and reaches a database containing customer financial records. This path was invisible to CSPM alone—it only became visible once EASM identified the external entry point.

### Query internet exposure with Cloud Security Explorer

Cloud Security Explorer lets you run graph\-based queries across your cloud resources. With EASM integration, you can correlate internet\-facing exposure data with internal resource findings to answer questions that neither tool can answer alone.

Contoso's security team runs several query scenarios to understand their risk posture. To find internet\-exposed resources with high\-severity vulnerabilities, they query for internet\-facing hosts that have vulnerabilities with severity equal to high. The result shows all EASM\-discovered internet\-facing hosts that also have high\-severity vulnerabilities in Defender for Cloud's internal assessment.

To validate whether internet exposure is intentional, they query for virtual machines that are exposed to the internet. This surfaces VMs that EASM identifies as internet\-reachable, letting the team verify each exposure against their security policies. For several VMs in the acquired partner infrastructure, the exposure is unintentional—these systems were never meant to be publicly accessible.

To trace from internet exposure to sensitive data, they query for internet\-exposed resources that have attack paths leading to storage accounts with sensitive data. The trace identifies which customer financial data stores could be reached by an attacker starting from an internet\-exposed entry point. The results highlight two storage accounts containing financial records that are potentially reachable through the attack paths discovered earlier.

These queries combine EASM outside\-in exposure data with Defender for Cloud's internal assessment to answer the critical question: "Can an external attacker actually reach our most sensitive assets?"

For Contoso, the Cloud Security Explorer results confirm it—two storage accounts containing financial records are potentially reachable through attack paths that begin at internet\-exposed entry points EASM discovered. Those findings now have a complete, traceable chain: from the public internet, through the acquired partner infrastructure, to sensitive internal data.

With EASM integrated into Defender for Cloud, your external attack surface findings become actionable inputs to the same attack path and posture workflows you already use for internal resources. You covered the core EASM workflow—discovery, inventory management, dashboard analysis, and Defender for Cloud integration.

---

## Knowledge check

Answer the following questions to check your knowledge of Microsoft Defender External Attack Surface Management.

### Check your knowledge

---

## Summary

In this module, you learned how Microsoft Defender External Attack Surface Management gives you an outside\-in view of your organization's internet\-facing infrastructure. While traditional tools focus on known, enrolled resources, External Attack Surface Management (EASM) discovers assets from an attacker's perspective. This includes shadow IT, forgotten infrastructure, and newly acquired systems outside of your known inventory.

You configured asset discovery using seeds like domains, IP addresses, and ASNs, letting EASM recursively map connections across your attack surface. For Contoso Financial Services, this discovery process revealed critical gaps after their partner acquisition, including unknown assets from the acquired company's infrastructure that traditional inventory methods missed.

Using four of EASM's eight security\-focused dashboards, you learned to prioritize risks across your external attack surface. Contoso uncovered Telnet\-exposed hosts, expiring SSL certificates, and domain registration issues in their newly acquired partner infrastructure—vulnerabilities that could go unnoticed without EASM's comprehensive visibility.

The integration with Defender CSPM extended that visibility further. By analyzing attack paths that start from internet\-exposed resources, Contoso traced a critical exposure from a Telnet\-accessible acquired host to their customer financial database—a risk that was invisible to CSPM alone before EASM identified the external entry point.

As you apply these skills in your own environment, you gain the visibility needed to secure not just the assets you know about, but the ones you don't—closing security gaps before attackers find them.

### In this module, you:

* Explored EASM features and capabilities, including the eight asset types, five asset states, and how its outside\-in scanning scope and deployment model differ from Defender CSPM and MDVM
* Configured asset discovery by deploying an EASM workspace, providing seeds, and setting up automated and custom discovery groups to identify unknown internet\-facing infrastructure
* Used EASM dashboards to prioritize vulnerabilities and security hygiene risks—including CVE exposure, open ports, SSL certificate issues, and OWASP Top 10 web application findings—across your external attack surface
* Integrated EASM findings with Defender CSPM to analyze attack paths starting from internet\-exposed resources discovered through outside\-in scanning

### Learn more

* [Microsoft Defender EASM overview](/en-us/azure/external-attack-surface-management/overview)
* [What is discovery in Defender EASM?](/en-us/azure/external-attack-surface-management/what-is-discovery)
* [Use and manage discovery](/en-us/azure/external-attack-surface-management/using-and-managing-discovery)
* [Understanding dashboards](/en-us/azure/external-attack-surface-management/understanding-dashboards)
* [Understanding inventory assets](/en-us/azure/external-attack-surface-management/understanding-inventory-assets)
* [External attack surface management in Defender for Cloud](/en-us/azure/defender-for-cloud/concept-easm)
* [Create a Defender EASM Azure resource](/en-us/azure/external-attack-surface-management/deploying-the-defender-easm-azure-resource)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/discover-external-assets-vulnerabilities/_

## Fuentes
- [Discover unprotected assets and vulnerabilities by using Microsoft Defender External Attack Surface Management](https://learn.microsoft.com/en-us/training/modules/discover-external-assets-vulnerabilities/?WT.mc_id=api_CatalogApi)
