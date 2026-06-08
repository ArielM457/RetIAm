# Audit the security of Windows Server IaaS Virtual Machines

> Curso: Secure Windows Server on-premises and hybrid infrastructures (wwl-secure-windows-server-premises-hybrid-infrastr) · Seccion: Secure Windows Server on-premises and hybrid infrastructures
> Duracion estimada: 45 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You can use the Microsoft Defender for Cloud to assess the security configuration of your Azure VM resources and the Windows Server operating system (OS) that's running on the VM.

### Scenario

Contoso is a medium\-size financial services company in London with a branch office in New York. Most of its compute environment runs on\-premises on Windows Server. Contoso has virtualized workloads on Windows Server 2016 hosts. Contoso IT staff are in the process of migrating Contoso servers to Windows Server 2025\.

Contoso’s IT director realizes that Contoso has an outdated operational model with limited automation, and reliance on dated technology. The Contoso IT Engineering team is exploring Azure capabilities. They want to determine whether Azure services might assist with modernizing the current operational model through automation, and virtualization.

As part of the initial design, the Contoso IT team asked you, their lead system engineer and server administrator, to set up a proof of concept environment. This environment must verify whether Azure services can help to modernize the IT infrastructure and meet business goals.

Securing VM resources both in Azure and on\-premises is important to the IT staff at Contoso. In this module, learn about Microsoft Defender for Cloud and how to enable it in hybrid environments. This module teaches you to onboard Windows Server computers to Microsoft Defender for Cloud, and how to use it to protect your resources. Also learn about Microsoft Sentinel, security information and event management (SIEM), and security orchestration, automation, and response (SOAR).

### Learning objectives

After completing this module, you'll be able to:

* Describe Microsoft Defender for Cloud.
* Enable Microsoft Defender for Cloud in hybrid environments.
* Onboard Windows Server computers to Microsoft Defender for Cloud.
* Implement and assess security policies.
* Describe Microsoft Sentinel.
* Implement SIEM and SOAR.
* Protect your resources with Microsoft Defender for Cloud.

### Prerequisites

In order to get the best learning experience from this module, it's important that you have knowledge and experience of the following:

* Managing Windows Server operating system and Windows Server workloads in on\-premises scenarios, including Active Directory Domain Services (AD DS), Domain Name System (DNS), the Distributed File System (DFS), Microsoft Hyper\-V, and file and storage services
* Common Windows Server management tools
* Core Microsoft compute, storage, networking, and virtualization technologies
* On\-premises resiliency Windows Server–based compute and storage technologies
* Implementing and managing ​​infrastructure as a service (IaaS) services in Azure
* Microsoft Entra ID
* Security\-related technologies (firewalls, encryption, multifactor authentication)
* Windows PowerShell scripting
* Automation and monitoring

---

## Describe Microsoft Defender for Cloud

To address the unique security challenges that a hybrid environment presents, such as rapidly changing services, sophisticated attacks, and increased workload, Contoso IT staff need tools to help assess their security posture and identify risks. Ideally, they want to deploy those tools with minimal effort. Microsoft Defender for Cloud can help them meet all these requirements.

### What is Microsoft Defender for Cloud

*Microsoft Defender for Cloud* is a cloud\-based tool for managing the security of your cloud and on\-premises infrastructure. With Microsoft Defender for Cloud capabilities, you can:

* Improve your security position. Use Microsoft Defender for Cloud to implement security best practices across your IaaS, platform as a service (PaaS), data, and on\-premises resources. In addition to security best practices, you can also track compliance against regulatory standards.
* Protect your environment. Monitor for security threats to your cloud and on\-premises servers, including identifying misconfigurations and providing server Endpoint Detection and Response (EDR) with Microsoft Defender for Endpoint.
* Protect your data. Identify suspicious activity such as potential data breaches within your servers, files, databases, data warehouses, and storage accounts. Microsoft Defender for Cloud can also perform automatic data classification in your Azure SQL databases.

### How Microsoft Defender for Cloud works in hybrid environments

In addition to Microsoft Defender for Cloud capabilities for monitoring and protecting Azure IaaS, PaaS, and data resources, Microsoft Defender for Cloud also helps protect servers outside of Azure. From the Azure portal, you can install the Log Analytics agent on your on\-premises Windows Server and Linux server VMs and non–Azure cloud VMs. The agent then collects the data that Microsoft Defender for Cloud needs for monitoring and managing those resources.

Microsoft Defender for Cloud collects event log events and Event Tracing for Windows events from the agents. It then scans security\-related configurations, and native events in Azure. The Log Analytics agent also collects crash dumps when applications fail, and it enables command\-line auditing. It analyzes these data sources and generates a custom list of hardening tasks that it recommends you perform, and it generates security alerts that can be sent to your SIEM solution.

Note

In addition to the Log Analytics agent, the Microsoft Defender for Endpoint sensor is automatically enabled on Windows Server computers that are onboarded to Microsoft Defender for Cloud.

#### Notifications

One of the first things to do when onboarding to Microsoft Defender for Cloud is to provide contact information so Microsoft Defender for Cloud can notify you when it detects compromised resources. In Microsoft Defender for Cloud, select **Email notifications** on the **Pricing \& settings** page and then provide an email address and phone number. Choose whether to get alerts for high\-severity events and if all users with an Owner role in the subscription should receive notifications.

#### Microsoft Defender for Cloud feature coverage for VMs

Microsoft Defender for Cloud provides a wide variety of features, some of which are available for Azure VMs and PaaS services as part of the Free service tier, and some are available only as part of the Standard tier.

Note

Only some features apply to on\-premises servers and VMs, and those that do apply require the Standard tier.

Some common Microsoft Defender for Cloud features include:

* Microsoft Intune Endpoint Protection assessment
* Missing operating system patches assessment
* Security misconfigurations assessment
* Disk encryption assessment
* Network security assessment
* Third\-party vulnerability assessment
* VM behavioral analytics and security alerts
* Adaptive application controls
* File integrity monitoring
* Fileless security alerts
* Defender for Endpoint
* Regulatory compliance dashboard and reports
* Adaptive network controls
* Adaptive network hardening
* Just\-in\-time (JIT) VM access
* Native vulnerability assessment
* Network map
* Network\-based security alerts

You can find out which Microsoft Defender for Cloud features are included with which pricing tier, and learn more about what they do by reviewing [Feature coverage for machines](https://aka.ms/feature-coverage-for-machines?azure-portal=true).

---

## Enable Microsoft Defender for Cloud in hybrid environments

IT staff at Contoso want to use Microsoft Defender for Cloud to help secure their VM workloads and their on\-premises servers. To onboard their VMs and on\-premises servers to Microsoft Defender for Cloud, they must complete the following tasks:

* Enable the Standard pricing tier
* Enable automatic provisioning
* Onboard their VMs and servers

Note

Standard pricing must be enabled for Microsoft Defender for Cloud and any associated Log Analytics workspaces.

### Enable the Microsoft Defender for Cloud Standard pricing tier

To use Microsoft Defender for Cloud advanced capabilities or to use it with on\-premises servers, you'll need to enable the Microsoft Defender for Cloud Standard pricing tier in your Azure subscriptions. Subscriptions that aren't upgraded to the Standard pricing tier are listed in the Microsoft Defender for Cloud dashboard. If you already have a default **Log Analytics** workspace, you'll also need to upgrade it to the Standard pricing tier.

To switch to Standard tier pricing, use the following procedure:

1. In the Azure portal, select **Microsoft Defender for Cloud**.
2. In the navigation pane, select **Pricing \& settings**.
3. In the details pane, select your subscription.
4. Select **Standard**, and then select **Save**.
5. If necessary, repeat these steps for any Log Analytics workspaces you want to use with Microsoft Defender for Cloud.

### Enable automatic provisioning

If you enable automatic provisioning, Microsoft Defender for Cloud installs the Log Analytics agent on your existing Azure VMs and on any Azure VMs that you create in the future. When you enable automatic provisioning, you choose to store data either in the default Log Analytics workspace that Microsoft Defender for Cloud creates, or in an existing workspace. If no workspaces display, create a new one or upgrade an existing one.

To enable automatic provisioning, use the following procedure:

1. In the Azure portal, select **Microsoft Defender for Cloud**.
2. In the navigation pane, select **Pricing \& settings**.
3. In the details pane, select your subscription, and then in the navigation pane, select **Data Collection**.
4. In the details pane, under **Auto Provisioning**, select **On**. You can also select the preferred Log Analytics workspace under the **Workspace configuration** heading.
5. Select **Save**.

### Onboard your on\-premises servers and computers

After upgrading Microsoft Defender for Cloud to the Standard tier for your subscriptions, you can onboard your on\-premises computers. This requires that you download the Log Analytics agent and install it on the computers. Use the following procedure to install the required agents:

1. In the Azure portal, select **Microsoft Defender for Cloud**.
2. In the navigation pane, select **Getting started**.
3. In the details pane, select the **Install Agents** tab. Agents should be installed on your VMs already, and so the **Install agents** button is greyed out and unavailable.
4. Select the **Get Started** tab.
5. In the details pane, beneath the **Add non\-Azure servers** heading, select **Configure**.
6. On the **Onboard servers to Microsoft Defender for Cloud** blade, if necessary, select **Create New Workspace**.
7. Create a new Log Analytics workspace.
8. Select **\+ Add Servers** in the selected workspace.
9. On the **Agents management** blade, select the appropriate link for the agent you require. Typically, you will select **Download Windows Agent (64 bit)**.
10. Copy the **Workspace ID** and **Primary key**. You'll need those to install the agent.
11. Copy the downloaded agent to your on\-premises servers.
12. Run the **MMASetup\-AMD64\.exe** file to install the agent.
13. When prompted, in the **Microsoft Monitoring Agent Setup wizard** on the **Azure Setup Options** page, select the **Connect the agent to Azure Log Analytics (OMS) check box**, and then select **Next**.
14. On the **Azure Log Analytics** page, enter the **Workspace ID** and the **Primary key** that you previously copied.
15. Go through the remaining steps to complete the installation process.

### Onboard Windows servers and computers to Microsoft Defender for Endpoint

Threat protection in Microsoft Defender for Cloud is provided by its integration with Microsoft Defender for Endpoint. Combined with Microsoft Defender for Cloud, they provide a complete Endpoint Detection and Response (EDR) solution. You can onboard your Windows Server 2019 or Windows 10 computers to Microsoft Defender for Endpoint by using:

* A local script
* Group Policy
* Microsoft Endpoint Configuration Manager
* Virtual desktop infrastructure onboarding scripts for non\-persistent machines

### Additional reading

You can learn more by reviewing the following documents:

* [Log Analytics agent overview](https://aka.ms/log-analytics-agent?azure-portal=true).
* [Onboard devices to the Microsoft Microsoft Defender for Endpoint service](https://aka.ms/onboard-configure?azure-portal=true).

---

## Implement and assess security policies

The engineering team at Contoso decides to perform a trial of Microsoft Defender for Cloud. As part of the trial, they have a number of VM resources that they want to protect. From the **Overview** blade of the **Microsoft Defender for Cloud**, the team members review the overall security picture. The team notices that the **Overall Security Score** is just 38 percent. They also notice that under the **Resource security hygiene** heading, there are a significant number of recommendations. They decide to attempt to tighten up security on their resources.

### Audit your VM’s regulatory compliance

The team starts with reviewing regulatory compliance. Under the **Regulatory compliance** heading, they review the following measurements: **PCI DSS 3\.2\.1**, **ISO 27001**, and **Azure CIS 1\.1\.0**. A member of the team selects the **Regulatory compliance** tile and additional information displays.

The following table describes the compliance standards against which you can measure your security.

| Compliance standard | Description |
| --- | --- |
| **PCI DSS 3\.2\.1** | The Payment Card Industry Data Security Standard (PCI DSS) addresses security issues for organizations that manage credit card payments, and is intended to reduce card fraud. |
| **ISO 27001** | Part of the International Standards Organization (ISO) 27000 family of standards, 27001 defines a system that can bring management to IT systems. To be certified to have met this standard's criteria, organizations must submit to an audit. |
| **Azure CIS 1\.1\.0** | The Center for Internet Security (CIS) is an organization involved in developing best practice for securing It system. The Azure CIS 1\.1\.0 standard is devised to help ensure that organizations can secure their resources in the Azure cloud. |
| **SOC TSP** | The Service Organization Controls (SOC) framework is a standard for controls that focuses on safeguarding the confidentiality and privacy of information stored and processed in the cloud. |

To review your compliance posture relative to these standards, use the following procedure:

1. In the Azure portal, in **Microsoft Defender for Cloud**, on the **Regulatory compliance** blade, select **Download now \>**.
2. On the **Download report** blade, in the **Report standard** list, select the compliance standard. For example, select **SOC TSP** and then select **Download**.
3. Open the downloaded PDF and review its contents.

To review compliance remediation details, on the **Regulatory Compliance** blade, use the following procedure:

1. Select the appropriate tab for the relevant standard. For example, select **SOC TSP**.
2. To review additional details about a recommendation, select it from the **Assessment** list, and then select **View affected machines**.

### Remediate security recommendations

It's important to do more than just review how your organization compares with security and compliance standards. You should also seek to tighten your security to try and meet those standards. To access and apply security recommendations, in the Azure portal, in **Microsoft Defender for Cloud**, select the **Overall Secure Score** tile. Use the following procedure to apply recommendations for your subscription:

1. On the **Secure Score Dashboard**, select the appropriate subscription, and then select **View recommendations**.
2. On the **Recommendations** blade, you can download a CSV report. You can also expand the details for listed recommendations.
3. Select a specific recommendation, and then on the recommendation blade (the name of which varies based on the recommendation title), you can expand **Remediation steps** and review the manual steps required to address the security issue. You can then switch to those resources and apply the remediation steps.

Tip

In some circumstances, you can apply a quick fix by selecting **Remediate** on the specific recommendation. This applies the remediation automatically when you select.
4. You can also apply a logic app to fix the listed resources. To do this, select the affected resources, and then select **Trigger Logic App**.
5. On the **Logic App Trigger** blade, after the logic apps load, select the appropriate logic app, and then select **Trigger**.

### Run a vulnerability assessment against your Windows Server IaaS VM

You can use Microsoft Defender for Cloud to perform a vulnerability assessment on your VMs. First, however, you must install a vulnerability assessment solution on the required resources.

#### Install the vulnerability assessment solution

Azure provides a built\-in vulnerability assessment solution. To enable this on your VMs, use the following procedure:

1. Open **Microsoft Defender for Cloud**, and then select **Recommendations**.
2. On the **Recommendations** blade, if necessary, select an appropriate subscription.
3. In the **Controls** list, expand **Remediate vulnerabilities**, and then select the **Enable the built\-in vulnerability assessment solution on virtual machines (powered by Qualys)** recommendation.
4. Select all VMs that you want to apply the assessment to, and then select **Remediate**.
5. On the **Remediate resources** blade, select **Remediate *n* resources**. The process might take a few minutes or longer depending on the number of resources being remediated.

Tip

In addition to the built\-in vulnerability scanner, you can also install third\-party scanners.

#### Perform the vulnerability assessment

After you install the vulnerability assessment, you can perform the assessment. To begin the assessment:

1. On the **Enable the built\-in vulnerability assessment solution on virtual machines (powered by Qualys)** blade, refresh the display and wait until all resources display on the **Healthy resources** tab. (This can take a few minutes or longer.)
2. After the resources display on the **Healthy resources** tab, verify that scanning begins automatically.

Note

Scans run at four\-hour intervals. You cannot change this setting.

After Microsoft Defender for Cloud identifies vulnerabilities, they are presented as recommendations. To review the findings and remediate the identified vulnerability, use the following procedure:

1. Open **Microsoft Defender for Cloud** and go to the **Recommendations** page.
2. Select **Remediate vulnerabilities**, and then select **Vulnerabilities in your virtual machines should be remediated (powered by Qualys)**.

Microsoft Defender for Cloud displays all the findings for all VMs in the currently selected subscriptions. These findings are listed in order of severity. To learn more about a specific vulnerability, select it.

Tip

To filter the findings by a specific VM, open the **Affected resources** section, and then select the VM. Alternatively, you can select a VM from resource health, and review all the relevant recommendations for that resource.

### Additional reading

You can learn more by reviewing the following documents:

* [Tutorial: Improve your regulatory compliance](https://aka.ms/improve-regulatory-compliance?azure-portal=true).
* [Vulnerability assessments for your Azure Virtual Machines](https://aka.ms/vulnerability-assessment-recommendations?azure-portal=true).

---

## Implement Microsoft Sentinel

In addition to assessing and addressing problems with their hybrid environment's security configuration, Contoso must also monitor for new problems and threats, and respond appropriately. Microsoft Sentinel is both a SIEM and SOAR solution that's designed for hybrid environments.

Note

SIEM solutions provide storage and analysis of logs, events, and alerts that other systems generate, and you can configure these solutions to raise their own alerts. SOAR solutions support the remediation of vulnerabilities and the overall automation of security processes.

### What is Microsoft Sentinel?

Sentinel meets the needs of both SIEM and SOAR solutions through:

* Collecting data across cloud\-based and on\-premises users, devices, apps, and infrastructure.
* Using AI to identify suspicious activity.
* Detecting threats with fewer false positives.
* Responding to incidents quickly and automatically.

#### Prerequisites for Microsoft Sentinel

To enable Sentinel, you'll need:

* A **Log Analytics** workspace.

Tip

Sentinel can't use the same **Log Analytics** workspace as Microsoft Defender for Cloud.
* Contributor permissions or greater in the subscription and workgroup for your Sentinel workspace.
* Appropriate permissions on any resources that you connect to Sentinel.

#### Data connections

Sentinel can connect natively to Microsoft Defender for Cloud, providing coverage for your cloud and on\-premises servers. In addition, Sentinel data connection support includes:

* Native service\-to\-service connections. Sentinel integrates natively to these Azure and non\-Azure services:
	+ Azure activity logs
	+ Microsoft Entra audit logs
	+ Microsoft Entra ID Protection
	+ Azure Advanced Threat Protection (Azure ATP)
	+ AWS CloudTrail
	+ Microsoft Cloud App Security
	+ DNS servers
	+ Microsoft 365
	+ Defender ATP
	+ Microsoft web application firewall
	+ Windows Defender Firewall
	+ Windows security events
* External solution connections through APIs. Sentinel can connect to data sources through APIs for the following solutions:
	+ Barracuda
	+ Barracuda CloudGen Firewall
	+ Citrix Analytics for Security
	+ F5 BIG\-IP
	+ Forcepoint DLP
	+ squadra technologies secRMM
	+ Symantec ICDx
	+ Zimperium
* External solution connections through an agent. Sentinel can connect via an agent to data sources that support the Syslog protocol. The Sentinel agent can install directly on devices or on a Linux server that can receive events from other devices. Support for connecting through an agent includes the following devices and solutions:
	+ Firewalls, internet proxies, and endpoints
	+ Data loss prevention (DLP) solutions
	+ DNS machines
	+ Linux servers
	+ Other cloud providers

#### Permissions

Access in Sentinel is managed through role\-based access control (RBAC) roles. These roles give you the ability to manage what users can observe and do within Sentinel:

* Global roles. The built\-in Azure global roles—Owner, Contributor, and Reader—grant access to all Azure resources, including Sentinel and Log Analytics.
* Sentinel\-specific roles. The built\-in roles that are specific to Sentinel are:
	+ Microsoft Sentinel Reader. This role can get data, incidents, dashboards, and information about Sentinel resources.
	+ Microsoft Sentinel Responder. This role has all the capabilities of the Microsoft Sentinel Reader role and can also manage incidents.
	+ Microsoft Sentinel Contributor. In addition to the capabilities of the Microsoft Sentinel Responder role, this role can create and edit dashboards, analytics rules, and other Sentinel resources.
* Other roles. Log Analytics Contributor and Log Analytics Reader are built\-in roles that are specific to Log Analytics. These roles grant permissions only to the **Log Analytics** workspace. If you don't have the global Contributor or Owner roles, you'll need the Logic App Contributor role to create and run playbooks in response to alerts.

#### Implement Microsoft Sentinel

To implement Sentinel:

1. In the Azure portal, search for and select **Microsoft Sentinel**.
2. On the Microsoft Sentinel workspaces blade, select **Connect workspace**, and then choose the appropriate workspace.
3. Select **Add Microsoft Sentinel**. The workspace is modified to include Sentinel.
4. On the **Microsoft Sentinel** blade, in **News \& guides**, select the **Get started** tab.
5. Select **Connect** to begin collecting data.
6. Select the appropriate connector. For example, select **Microsoft Defender for Cloud**.
7. Select **Open connector page**.
8. Review the prerequisite information, and when ready, select **Connect**.

### What is SIEM?

SIEM solutions store and analyze log data that comes from external sources. You connect data sources from Azure and external sources in your organization, including on\-premises resources. Microsoft Sentinel then provides a default dashboard that helps you analyze and visualize those events. The dashboard displays data about the number of events you have received, the number of alerts generated from that data, and the status of any incidents created from those alerts.

Sentinel uses built\-in and custom detections to alert you to potential security threats—for example, attempts to access Contoso's organization from outside their infrastructure or when data from Contoso appears to be sent to a known malicious IP address. It also enables you to create incidents based on these alerts.

Sentinel provides you with built\-in and custom workbooks to help you analyze incoming data. *Workbooks* are interactive reports that include log queries, text, metrics, and other data. Microsoft incident creation rules enable you to create incidents from alerts that other services such as Microsoft Defender for Cloud generate.

To implement SIEM functionality in Sentinel:

* Enable Microsoft Sentinel.
* Create a data connection.
* Create a custom rule that generates an alert.

### What is SOAR?

SOAR solutions enable you to manage or orchestrate analysis of data that you have collected about security threats, coordinate your response to those threats, and create automated responses. Microsoft Sentinel's SOAR capabilities are tied closely to its SIEM functionality.

Use the following best practices to implement SOAR in Sentinel:

* When you create analytics rules that raise alerts, also configure them to create incidents.
* Use the incidents to manage the investigation and response process.
* Group related alerts into an incident.

#### Investigate incidents

In Sentinel, you can review how many incidents are open, how many are being worked on, and how many are closed. You can even reopen closed incidents. You can get the details of an incident, such as when it occurred and its status. You can also add notes to an incident and change its status so that progress is easier to understand. Incidents can be assigned to specific users.

#### Respond to alerts with security playbooks

Sentinel enables you use security playbooks to respond to alerts. *Security playbooks* are collections of procedures based on Azure Logic Apps that run in response to an alert. You can run these security playbooks manually in response to your investigation of an incident, or you can configure an alert to run a playbook automatically.

### Additional reading

You can learn more by reviewing the following documents:

* [Permissions in Microsoft Sentinel](https://aka.ms/sentinel-roles?azure-portal=true).
* [Overview – What is Azure Logic Apps?](https://aka.ms/logic-apps-overview?azure-portal=true).
* [Quickstart: On\-board Microsoft Sentinel](https://aka.ms/quickstart-onboard?azure-portal=true).
* [Tutorial: Create custom analytic rules to detect suspicious threats](https://aka.ms/tutorial-detect-threats-custom?azure-portal=true).

---

## Summary

The IT operations team at Contoso need to secure VM resources both in Azure and on\-premises.

In this module, you learned about using the tools available in Azure to assess current Azure resources and OS internal security configurations. You also learned about enabling Microsoft Defender for Cloud in hybrid environments, and how to onboard Windows Server computers. Finally, you learned to use Microsoft Defender for Cloud to protect your resources, and about Microsoft Sentinel, SIEM, and SOAR.

Now, you can help the Contoso IT team use Microsoft Defender for Cloud to assess the security configuration of their VM resources and the Windows Server OS that's running on the VMs.

### Learn more

You can learn more by reviewing the following documents:

* [Quickstart: Onboard Windows computers to Microsoft Defender for Cloud](https://aka.ms/onboard-windows-computer?azure-portal=true).
* [Tutorial: Improve your regulatory compliance](https://aka.ms/improve-regulatory-compliance?azure-portal=true).
* [Vulnerability assessments for your Azure Virtual Machines](https://aka.ms/vulnerability-assessment-recommendations?azure-portal=true).
* [Tutorial: Use Microsoft Defender for Cloud to monitor Windows virtual machines](/en-us/azure/security/fundamentals/virtual-machines-overview).
* [Protect your servers and VMs from brute\-force and malware attacks with Microsoft Defender for Cloud](https://aka.ms/secure-vms-with-security-center?azure-portal=true).

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/audit-security-of-windows-server-iaas-virtual-machines/_

## Fuentes
- [Audit the security of Windows Server IaaS Virtual Machines](https://learn.microsoft.com/en-us/training/modules/audit-security-of-windows-server-iaas-virtual-machines/?WT.mc_id=api_CatalogApi)
