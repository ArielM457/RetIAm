# Implement Microsoft Defender for Servers

> Curso: Implement security for servers and virtual machines (wwl-server-vm-security) · Seccion: Implement security for servers and virtual machines
> Duracion estimada: 26 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Manufacturing runs critical factory automation software on Azure virtual machines and Arc\-connected on\-premises servers. These servers control production lines, manage inventory systems, and run operational technology (OT) workloads. Currently, the security team has no vulnerability scanning, no endpoint detection, and no way to detect if a server is compromised. A silent attack on a server running Policy \& Configuration (PLC) integration software could disrupt production for days before anyone notices.

In this module, you implement Microsoft Defender for Servers across Contoso's entire server estate. You learn how to:

* Select the appropriate Defender for Servers plan and onboard Azure VMs and Arc\-connected servers
* Configure vulnerability scanning using both agentless and agent\-based Defender Vulnerability Management
* Manage the Microsoft Defender for Endpoint integration, configure agentless scanning capabilities, and enable File Integrity Monitoring

### Prerequisites

* Defender for Cloud enabled on your Azure subscription
* Azure Arc connectivity established for on\-premises servers
* Basic familiarity with Defender for Cloud environment settings and workload protection concepts

Now that you understand the security gap Contoso faces, you're ready to select the right Defender for Servers plan and onboard the server estate.

---

## Onboard servers to Defender for Servers

Enabling Defender for Servers transforms unmonitored virtual machines and Arc\-connected servers into actively protected assets with vulnerability scanning, endpoint detection and response, and advanced threat protection. Before you enable protection, you select the plan tier that matches your organization's security requirements and budget.

| Capability | Plan 1 | Plan 2 |
| --- | --- | --- |
| Microsoft Defender for Endpoint integration | Included | Included |
| Agent\-based vulnerability assessment | Included | Included |
| Security alerts and threat detection | Included | Included |
| Agentless scanning | Unavailable | Included |
| Just\-in\-time VM access | Unavailable | Included |
| File Integrity Monitoring | Unavailable | Included |
| OS configuration assessment (Machine Configuration) | Unavailable | Included |
| Premium Defender Vulnerability Management features | Unavailable | Included |
| OS updates assessment | Unavailable | Included |
| Network map | Unavailable | Included |

### Choose between Plan 1 and Plan 2

Plan 1 provides essential protection when Microsoft Defender for Endpoint integration and agent\-based vulnerability assessment meets your needs. Organizations with cost constraints or simple server workloads often start with Plan 1\. The plan delivers core endpoint detection and response (EDR) capabilities and continuous vulnerability scanning through the MDE sensor installed on each machine.

Plan 2 adds agentless scanning, which analyzes server disk contents without requiring agent deployment or consuming machine resources. With agentless scanning, you gain software inventory, vulnerability assessment, secrets scanning, and malware detection capabilities that run offline every 24 hours. Plan 2 also unlocks just\-in\-time VM access for securing management ports, File Integrity Monitoring for detecting unauthorized changes, and OS configuration assessment through Machine Configuration.

For Contoso Manufacturing, Plan 2 is the right choice. The factory environment includes Arc\-connected on\-premises servers where minimizing agent overhead matters, and the regulatory requirements for manufacturing demand the advanced capabilities that only Plan 2 provides—agentless scanning for comprehensive coverage and File Integrity Monitoring for detecting tampering with OT system files.

### Enable Defender for Servers at subscription scope

You enable Defender for Servers at the subscription level through the Defender for Cloud environment settings. Navigate to **Defender for Cloud** \> **Environment Settings**, select your subscription, then locate the **Servers** plan in the Defender plans list. Toggle the plan to **On** and choose either **Plan 1** or **Plan 2** from the plan selector. Select **Save** to apply the configuration.

When you enable Defender for Servers, a 30\-day trial period begins immediately. The trial provides full access to all plan features at no cost, giving you time to validate the deployment and assess the value before charges start. You can't stop, pause, or extend the trial once it starts—after 30 days, standard billing applies automatically.

### Override protection scope at resource group or resource level

You can override the subscription\-level plan setting at the resource group or individual resource level when different environments require different protection tiers. For example, you might apply Plan 1 to development and test resource groups while maintaining Plan 2 for production workloads. This approach optimizes costs while ensuring critical assets receive premium protection.

At the resource level, you can exclude specific virtual machines from Defender for Servers protection entirely. Use this capability cautiously—excluded VMs lose all Defender for Servers protections including vulnerability scanning, threat detection, and endpoint protection. Valid use cases include temporary test VMs or machines with conflicting external security software that can't coexist with Defender for Endpoint.

### Onboard Arc\-connected servers automatically

Arc\-connected servers in your subscription automatically receive protection when you enable Defender for Servers at the subscription level. Defender for Cloud detects Arc\-enrolled machines and deploy the Microsoft Defender for Endpoint extension to them without requiring manual intervention. This automatic deployment ensures consistent protection across your hybrid server estate.

Verify that Arc servers appear in your protected inventory by navigating to **Defender for Cloud** \> **Asset Inventory** and filtering for **Non\-Azure machines**. Each Arc\-connected server shows its Defender for Servers plan assignment and the status of security agents. If a server doesn't appear, confirm that the Azure Arc Connected Machine agent is installed and that the server resource is in a subscription with Defender for Servers enabled.

### Deploy at scale using Azure Policy

For organizations with multiple subscriptions or management groups, manual enablement becomes impractical. Use the built\-in Azure Policy **Configure Azure Defender for Servers to be enabled (with 'P1' subplan) for all resources (resource level)** to automatically enable Defender for Servers Plan 1 on all VMs and Arc\-connected machines at the resource level. Assign this policy at a management group to cover all factory subscriptions in the Contoso environment.

The policy assignment creates a managed identity that continuously evaluates resources and enables Defender for Servers on any new or existing VMs that lack protection. Policy\-based deployment ensures that newly provisioned factory servers immediately receive protection without manual configuration steps.

### Verify post\-enablement behavior

After enablement, Defender for Cloud automatically deploys the Microsoft Defender for Endpoint extension to supported Windows and Linux VMs. The extension provides the EDR sensor that performs continuous monitoring, behavioral analysis, and threat detection on each protected machine. Vulnerability assessment activates immediately, with the MDE sensor beginning to report software inventory and vulnerability findings within minutes.

For Plan 2 subscriptions, agentless scanning activates automatically and begins its 24\-hour scanning cycle. The first agentless scan completes within 24 hours of enablement, after which scans repeat on a daily schedule. You see results from both agent\-based and agentless vulnerability assessment in the Defender portal vulnerability management dashboard.

For Contoso Manufacturing, the security team enables Plan 2 at the subscription level covering all factory environments. Within hours, the Asset Inventory shows protected status for both Azure VMs running factory software and Arc\-connected on\-premises servers controlling production equipment. The deployment establishes comprehensive visibility into vulnerabilities and threats across the entire server estate.

Now that Defender for Servers is active on your environment, you configure vulnerability scanning to identify security weaknesses in your server software stack.

---

## Configure vulnerability scanning with Defender Vulnerability Management

Vulnerability scanning identifies security weaknesses in operating systems, applications, and software packages before attackers exploit them. Defender for Servers provides two complementary scanning methods—agent\-based and agentless—that work together to ensure comprehensive vulnerability coverage across your server estate with minimal operational overhead.

| Scanning Method | Plan Requirement | How It Works | Update Frequency | Performance Challenge |
| --- | --- | --- | --- | --- |
| Agent\-based | Plan 1 or Plan 2 | Microsoft Defender for Endpoint (MDE) sensor scans locally installed software | Continuous, real\-time | Minimal CPU/memory usage |
| Agentless | Plan 2 only | Disk snapshots analyzed offline | Every 24 hours | None (runs outside VM) |

### Use agent\-based vulnerability scanning for real\-time detection

Agent\-based vulnerability scanning runs through the Microsoft Defender for Endpoint sensor installed on each protected machine. The sensor continuously monitors installed software, compares it against Microsoft's vulnerability intelligence database, and reports findings in near real\-time. When a new vulnerability disclosure affects software running on your servers, the agent detects it within minutes and surfaces the finding in Defender for Cloud.

The agent\-based approach provides the fastest detection because the sensor runs locally on each machine and doesn't depend on scheduled scans. For critical production servers where rapid vulnerability identification matters, this continuous monitoring ensures that you learn about exploitable weaknesses immediately after vulnerability databases update.

Agent\-based scanning is available with both Plan 1 and Plan 2, making it the baseline vulnerability assessment method for all Defender for Servers deployments. The MDE sensor consumes minimal system resources—typically less than 2% CPU and 100 MB of memory—making it suitable even for resource\-constrained factory servers running OT workloads.

### Use agentless scanning to eliminate agent deployment overhead

Agentless vulnerability scanning takes a fundamentally different approach. Instead of installing software on your VMs, agentless scanning creates a snapshot of each VM's disk, then analyzes that snapshot in an isolated Azure environment completely outside your virtual machine. The VM itself experiences no performance issues because the analysis happens on a copy of the disk data.

Here's how the technical process works. Once every 24 hours, Defender for Cloud takes a point\-in\-time snapshot of each running VM's disk. The snapshot process uses Azure's native snapshot capabilities, which complete in seconds without pausing or interrupting the VM. Defender for Cloud then mounts the snapshot disk in a secure analysis environment, scans the file system to build a software inventory, and compares installed packages against vulnerability databases. After analysis completes, the snapshot is immediately deleted. Your VM never knows the scan happened.

Agentless scanning requires Defender for Servers Plan 2 or Defender CSPM. The capability is enabled by default when you activate Plan 2\. If you need to verify or manually enable it, navigate to **Environment Settings** \> **Plan settings** \> **Settings \& Monitoring** \> **Agentless scanning for machines** and toggle the setting to **On**.

### Understand agentless scanning disk and VM limits

Agentless scanning has technical limits based on disk size, disk count, and encryption type. The maximum total disk size that can be scanned is 4 TB, calculated as the sum of all attached disks. If a VM has six disks of 1 TB each (6 TB total), only the OS disk is scanned, provided the OS disk alone is under 4 TB. The maximum number of disks per VM is six—if a VM has more than six disks, the scan skips that VM entirely.

Disk encryption affects scan eligibility. Agentless scanning supports unencrypted disks, disks encrypted with SSE using platform\-managed keys, and disks encrypted with SSE using customer\-managed keys (CMK). However, certain disk types are unsupported: UltraSSD\_LRS, PremiumV2\_LRS, and AKS Ephemeral OS Disks can't be scanned because they use storage architectures incompatible with the snapshot\-based scanning process.

Only running VMs are scanned. If a VM is powered off or deallocated when the 24\-hour scan cycle starts, the scan skips that VM until the next cycle. For servers that run on scheduled start/stop automation, ensure they remain online during scan windows to maintain vulnerability visibility.

### Combine agent\-based and agentless scanning for hybrid coverage

When you enable both agent\-based and agentless scanning—the default configuration for Plan 2—you benefit from the strengths of each method. Agent\-based scanning provides continuous, real\-time detection with immediate visibility into newly disclosed vulnerabilities. Agentless scanning provides a second layer of validation that doesn't depend on agent health or connectivity, ensuring you maintain visibility even if an agent fails or is tampered with.

The Defender portal displays results using a precedence model. When both scanning methods report data for the same VM, the portal shows agent\-based results because they offer better freshness—the agent reports in real\-time while agentless scans run once daily. When only agentless scanning is active (for example, on a VM where the MDE sensor isn't deployed yet), the portal displays agentless results. If only agent\-based scanning is configured, you see only agent\-based data.

This hybrid model provides resilience. If an attacker disables or uninstalls the MDE sensor to hide their activities, the agentless scan still runs the next day and reveals the compromise. If a VM is offline when the agentless scan runs, the agent\-based sensor continues reporting until the next scan cycle completes.

### Use BYOL scanners as alternatives to Defender Vulnerability Management

Organizations with existing investments in Qualys or Rapid7 vulnerability scanning platforms can integrate those scanners instead of using Microsoft Defender Vulnerability Management. Defender for Cloud supports bring\-your\-own\-license (BYOL) integrations for both Qualys and Rapid7, allowing you to deploy those agents to Defender for Servers\-protected VMs and view findings in Defender for Cloud alongside other security data.

The BYOL approach makes sense when you have enterprise licensing agreements with Qualys or Rapid7, when you need vulnerability scanning features specific to those platforms, or when compliance requirements mandate a particular scanning vendor. For most organizations deploying Defender for Servers for the first time, Defender Vulnerability Management provides comprehensive coverage without other licensing costs or agent management complexity.

### View vulnerability findings in the Defender portal

After vulnerability scanning activates, findings appear in the **Defender portal** under **Vulnerability management** \> **Recommendations**. Each recommendation describes a specific vulnerability, lists affected machines, provides a severity score based on exploitability and issues, and offers remediation guidance. You can filter recommendations by severity, affected machine, or vulnerability type to prioritize remediation efforts.

The vulnerability management dashboard shows trends over time, helping you measure whether your patching processes are reducing the attack surface or if new vulnerabilities are accumulating faster than you remediate them. For Contoso Manufacturing, this visibility transforms factory servers from unknown risk to actively managed assets with quantified vulnerability counts and clear remediation paths.

For Arc\-connected on\-premises servers in the Contoso factory, agentless scanning delivers vulnerability visibility without agent overhead on systems that can have strict change control requirements. Azure VMs running factory management software, benefits from hybrid coverage—continuous agent\-based monitoring backed by daily agentless validation.

Now that vulnerability scanning is configured and reporting findings, you manage the Microsoft Defender for Endpoint integration. You need to configure agentless scanning capabilities, and enable File Integrity Monitoring to detect unauthorized changes to critical server files.

---

## Configure Defender for Endpoint integration, agentless scanning, and File Integrity Monitoring

Microsoft Defender for Endpoint integration, agentless scanning capabilities, and File Integrity Monitoring work together to create multiple layers of visibility and protection on your server estate. Each capability addresses a different detection need—from real\-time behavioral threat detection to offline malware scanning to detecting unauthorized file changes that might indicate lateral movement by an attacker.

| Capability | What It Provides | Plan Requirement | Data Source |
| --- | --- | --- | --- |
| Microsoft Defender for Endpoint (MDE) integration | EDR, behavioral analytics, threat intelligence | Plan 1 or Plan 2 | MDE agent sensor |
| Agentless scanning | Software inventory, vulnerability assessment, secrets scanning, malware scanning | Plan 2 | Disk snapshots analyzed offline |
| File Integrity Monitoring | Change detection for OS files, registries, application files | Plan 2 | MDE agent \+ agentless scanning |

### Manage the Microsoft Defender for Endpoint integration

The Microsoft Defender for Endpoint extension autoprovisions to every supported VM when you enable Defender for Servers. This extension deploys the MDE sensor, which provides endpoint detection and response (EDR) capabilities including behavioral analysis, threat intelligence integration, and vulnerability assessment through continuous software monitoring. The sensor runs as a lightweight service on Windows and Linux machines, monitoring process behavior, network connections, and file system changes to detect suspicious activity in real\-time.

The extension appears in the Azure portal with the name **MDE.Windows** on Windows VMs and **MDE.Linux** on Linux VMs. You can verify deployment status by navigating to a VM's **Extensions** screen or by checking the **Asset Inventory** in Defender for Cloud, where each VM displays its MDE integration status. A status of **Monitored** indicates the sensor is deployed, reporting data, and actively protecting the machine.

In most environments, you leave autoprovisioning enabled to ensure consistent protection across all VMs without manual intervention. However, you can disable autoprovisioning if you need to manually control which machines receive the MDE sensor or if you want to deploy Defender for Endpoint through an alternative method like Microsoft Intune or Group Policy. To disable autoprovisioning, navigate to **Environment Settings** \> **Settings \& Monitoring** \> **Endpoint protection** and toggle the setting to **Off**. After disabling autoprovisioning, you become responsible for deploying and maintaining the MDE sensor through your chosen deployment method.

### Configure agentless scanning capabilities for Plan 2

Agentless scanning in Defender for Servers Plan 2 provides four distinct security capabilities that run during the daily disk snapshot analysis. These capabilities operate as a unified feature set—when you enable agentless scanning, all four capabilities activate together and you can't selectively disable individual features.

**Software inventory** catalogs every installed application, package, and component on scanned VMs. The inventory data feeds into Defender for Cloud's asset management views, giving you a complete picture of what software runs across your server estate. This visibility helps you identify unauthorized software installations, locate machines running deprecated frameworks, and track software version distribution across environments.

**Vulnerability assessment** uses the same Defender Vulnerability Management engine that powers agent\-based scanning. During disk analysis, the agentless scanner identifies installed software versions, compares them against vulnerability databases, and reports exploitable weaknesses. The findings appear alongside agent\-based vulnerability results in the Defender portal, providing redundant coverage that persists even if the agent is disabled or removed.

**Secrets scanning** analyzes disk contents to identify exposed credentials, API keys, certificates, connection strings, and other secrets that could grant attackers unauthorized access to systems and data. The scanner examines configuration files, scripts, environment variable files, and application directories where developers commonly store secrets during development but forget to remove before deploying to production. When secrets are detected, Defender for Cloud generates high\-severity alerts with remediation guidance.

**Malware scanning** inspects files in the disk snapshot to detect malicious code, backdoors, rootkits, and other indicators of compromise. This capability is exclusive to Defender for Servers Plan 2—it isn't available if you enable agentless scanning through Defender CSPM alone. The offline analysis approach means the scanner can detect dormant malware that isn't actively running, fileless malware artifacts stored on disk, and malicious code that might evade runtime detection by hiding in encrypted archives or obfuscated scripts.

### Extend agentless scanning to Arc servers and multicloud environments

Agentless scanning supports not only Azure VMs but also AWS EC2 instances and GCP compute instances connected through Defender for Cloud's multicloud onboarding. For AWS and GCP resources, you configure agentless scanning through the same **Environment Settings** interface, ensuring consistent vulnerability and malware visibility across your entire hybrid and multicloud server estate.

The same 24\-hour scanning schedule applies to all supported platforms. For Azure VMs, agentless scanning supports disks encrypted with customer\-managed keys (CMK), ensuring that even highly regulated workloads with strict encryption requirements can benefit from agentless capabilities. This encryption support is critical for Contoso Manufacturing, where compliance requirements mandate CMK encryption for all data at rest.

### Enable and configure File Integrity Monitoring

File Integrity Monitoring (FIM) detects unauthorized changes to operating system files, Windows registries, application software files, and Linux system files. These changes might indicate an attack in progress—for example, an attacker modifying system binaries for establishing persistence, altering registry keys to disable security controls, or tampering with application configuration files to redirect data flows.

FIM requires Defender for Servers Plan 2 and has one core prerequisite: the Microsoft Defender for Endpoint agent must be deployed to the VM through the Defender for Servers extension. Enabling agentless scanning is optional but recommended—it extends FIM coverage to custom file paths beyond the default monitored locations and adds a daily validation layer through disk snapshot analysis.

To enable FIM, navigate to **Microsoft Defender for Cloud** \> **Environment settings** \> select the relevant subscription \> locate the Defender for Servers plan and select **Settings** \> in the **File Integrity Monitoring** section, toggle the setting to **On** \> select **Edit configuration** to choose a Log Analytics workspace. After enablement, configure the monitored paths by selecting specific files, directories, or registry keys to watch. Default paths cover critical OS locations including system binaries, security policy files, and authentication components. Custom paths allow you to monitor application\-specific configuration files—for Contoso Manufacturing, this includes PLC integration software configuration files and OT device communication settings.

FIM uses two complementary data sources. The MDE agent sensor monitors file changes in real\-time, generating change events within seconds of a modification. Agentless scanning extends monitoring to custom paths and provides a daily validation layer that detects changes even if an attacker disables the agent. This dual\-source approach ensures resilient change detection that's difficult for attackers to evade completely.

### Review and respond to File Integrity Monitoring events

Change events appear in **Defender for Cloud** under the **File Integrity Monitoring** dashboard. Each event shows what file changed, when the change occurred, who made the change (if identifiable through process tracking), and whether the change matches a known threat pattern. The dashboard allows you to filter events by severity, time range, and affected machines to focus on suspicious modifications that require investigation.

For baseline changes during scheduled maintenance windows, you can mark events as expected to reduce alert noise. Over time, FIM learns your environment's normal change patterns and surfaces anomalous modifications more effectively. However, the system doesn't automatically suppress alerts—you must explicitly acknowledge expected changes to refine the baseline.

In Contoso Manufacturing's factory environment, FIM provides critical visibility into OT system integrity. If an attacker compromises a factory server and modifies a PLC communication driver to intercept production commands, FIM detects the binary modification and alerts the security team within seconds. Even if the attacker disables the MDE agent to hide their activities, the next agentless scan detects the unauthorized file change and generates an alert, ensuring the compromise doesn't remain undetected for long.

The combination of MDE integration, agentless scanning capabilities, and File Integrity Monitoring transforms Contoso's factory servers from opaque assets into comprehensively monitored systems with multiple overlapping detection layers. An attacker must evade agent\-based monitoring, avoid leaving file system artifacts that agentless scanning detects, and make changes that don't trigger FIM alerts—a nearly impossible task that drastically increases the cost and complexity of successful attacks.

---

## Knowledge check

You implemented Defender for Servers across Contoso Manufacturing's Azure VMs and Arc\-connected factory servers, configured both agent\-based and agentless vulnerability scanning, and enabled File Integrity Monitoring to detect unauthorized changes. Now validate your understanding of plan selection, scanning methods, and configuration requirements.

### Check your knowledge

---

## Summary

You've successfully implemented Microsoft Defender for Servers across Contoso Manufacturing's server estate, transforming unmonitored virtual machines and Arc\-connected servers into actively protected assets with comprehensive vulnerability visibility and threat detection capabilities.

You selected Defender for Servers Plan 2 to meet the organization's security requirements. Plan 2 provides agentless scanning for Arc\-connected factory servers without agent deployment overhead, just\-in\-time VM access for securing management ports, and File Integrity Monitoring for detecting tampering with OT system files—capabilities essential for regulated manufacturing environments that Plan 1 doesn't include.

You configured vulnerability scanning using both agent\-based and agentless methods. Agent\-based scanning through the MDE sensor provides continuous, real\-time detection with immediate visibility into newly disclosed vulnerabilities. Agentless scanning runs every 24 hours, analyzes disk snapshots offline with no performance challenge on VMs, and provides redundant coverage that persists even if an attacker disables the agent. When both methods are active, agent\-based results take precedence in the Defender portal because they offer better freshness.

You managed the Microsoft Defender for Endpoint integration, which autoprovisions to all protected VMs and delivers endpoint detection and response capabilities including behavioral analytics and threat intelligence. You configured agentless scanning capabilities—software inventory, vulnerability assessment, secrets scanning, and malware scanning—that operate as a unified feature set during daily disk analysis.

Finally, you enabled File Integrity Monitoring to detect unauthorized changes to OS files, Windows registries, and application software files. FIM requires Plan 2, the MDE agent, and agentless scanning to provide both real\-time change detection through the agent sensor and daily validation through agentless scans. This dual\-source approach ensures resilient change detection that's difficult for attackers to evade.

### Learn more

* [Defender for Servers overview](/en-us/azure/defender-for-cloud/defender-for-servers-overview)
* [Enable agentless machine scanning](/en-us/azure/defender-for-cloud/enable-agentless-scanning-vms)
* [File Integrity Monitoring overview](/en-us/azure/defender-for-cloud/file-integrity-monitoring-overview)
* [Integration with Microsoft Defender for Endpoint](/en-us/azure/defender-for-cloud/integration-defender-for-endpoint)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/implement-microsoft-defender-servers/_

## Fuentes
- [Implement Microsoft Defender for Servers](https://learn.microsoft.com/en-us/training/modules/implement-microsoft-defender-servers/?WT.mc_id=api_CatalogApi)
