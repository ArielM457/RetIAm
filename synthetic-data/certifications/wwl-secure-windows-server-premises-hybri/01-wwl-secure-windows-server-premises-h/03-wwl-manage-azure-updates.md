# Manage Azure updates

> Curso: Secure Windows Server on-premises and hybrid infrastructures (wwl-secure-windows-server-premises-hybrid-infrastr) · Seccion: Secure Windows Server on-premises and hybrid infrastructures
> Duracion estimada: 40 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

In this module, you’ll learn how to ensure that on\-premises Windows Server instances and Azure infrastructure as a service (IaaS) virtual machines (VMs) are up to date with software updates.

### Scenario

Contoso is a medium\-size financial services company in London with a branch office in New York. Most of its compute environment runs on\-premises on Windows Server. This includes virtualized workloads on Windows Server 2012 R2 hosts. Contoso IT staff are in the process of migrating Contoso servers to Windows Server 2019\.

Contoso’s IT director realizes that Contoso has an outdated operational model with limited automation and reliance on dated technology. The Contoso IT Engineering team has started exploring Azure capabilities. They want to determine whether Microsoft Azure services might assist with modernizing the current operational model through automation and virtualization.

As part of the initial design, the Contoso IT team asked you, their lead system engineer and server administrator, to set up a proof of concept environment. This environment must verify whether Azure services can help to modernize the IT infrastructure and meet business goals.

One of the most important tasks that Contoso has to do in securing a hybrid server environment is to ensure that server updates are timely. Applying updates quickly, especially security updates, helps you block attacks based on the vulnerabilities that the updates address. Contoso IT staff are eager to find out how to manage their updates for both on\-premises and cloud\-based servers. They realize this could be challenging because few tools can manage both environments. They do have the option to extend Microsoft Endpoint Configuration Manager to manage their Azure servers. However, the Contoso IT team wants you to test whether they could manage updates for both cloud\-based and on\-premises servers by using the Azure Update Management service.

This module will cover enrolling Azure VMs in Azure Update Management, and configuring Windows Server Update Services (WSUS) with Azure Update Management. It will also cover reviewing, managing, and deploying Azure updates.

By the end of this module you'll be able to enable Azure Update Management, deploy updates, review an update assessment, and manage updates for your Azure VMs.

### Learning objectives

After completing this module, you will be able to:

* Describe Azure updates.
* Enable Update Management.
* Deploy updates.
* Review an update assessment.
* Manage updates for your Azure VMs.

### Prerequisites

In order to get the best learning experience from this module, it's important that you have knowledge and experience of the following:

* Managing the Windows Server operating system (OS) and Windows Server workloads in an on\-premises scenarios including Active Directory Domain Service (AD DS), Domain Name System (DNS), the Distributed File System (DFS), Microsoft Hyper\-V, and file and storage services.
* Common Windows Server management tools.
* Core Microsoft compute, storage, networking, and virtualization technologies.
* On\-premises resiliency Windows Server\-based compute and storage technologies.
* Implementing and managing IaaS services in Microsoft Azure.
* Microsoft Entra ID.
* Security\-related technologies (firewalls, encryption, multi\-factor authentication).
* Windows PowerShell scripting.
* Automation and monitoring.

---

## Describe update management

Updates to Windows are, of course, a recurring series of events. Updates can come quickly and frequently when newly discovered security flaws or attack vectors are addressed. Updates also arrive periodically based on events such as changes in device drivers or planned roll\-outs of new system features.

Contoso IT support staff realize that there is no set time that an urgent security update might become available, and it's imperative in many cases to deploy such an update as soon as possible. This approach applies whether the system is a physical host, an on\-premises VM, or an Azure VM. They must be vigilant when reviewing Windows Updates to their Azure VMs.

### Azure Automation and Update Management

Azure Automation helps you manage OS updates for Azure VMs running the Windows operating system. The Update Management feature is free, and the only cost is the cost of log storage in Azure Log Analytics.

The following table describes how Update Management features can help with updates for your Azure VMs.

| Feature | How it can help |
| --- | --- |
| Review the status of updates on your VMs | The service includes a cloud\-based console where you can review the status of updates across your Azure organization and for a specific VM. |
| Configure dynamic groups of VMs to target | It also allows you to define a query based on a computer group. A *computer group* is a group of computers that are defined based on another query or imported from another source such as WSUS or Microsoft Endpoint Configuration Manager. |
| Search the Azure Monitor logs | Update Management collects records from the Azure Monitor Logs. |

To implement Azure Update Management in your hybrid environment, you must complete the following high\-level steps:

1. Create an Azure Automation account.
2. Enable Update Management.
3. Onboard your on\-premises servers.
4. Select the machines to manage.
5. Schedule updates

Note

These steps are the same for on\-premises physical servers and VMs, and Azure VMs running Windows Server.

### Interaction with Windows Update

Azure Automation Update Management relies on the Windows Update client to download and install Windows updates. There are specific settings that are used by the Windows Update client when connecting to WSUS or Windows Update. You can manage many of these settings by:

* Using Local Group Policy Editor
* Using Group Policy
* Using Windows PowerShell
* Editing the Registry directly

Update Management respects many of the settings specified to control the Windows Update client.

Tip

If you use settings to enable non\-Windows updates, Update Management also manages those updates.

#### Configure WSUS for managing updates

WSUS improves the security of the systems at Contoso by applying security updates to Microsoft products and third\-party products in a timely manner. It provides the infrastructure to download, test, and approve security updates. Applying security updates quickly helps prevent security incidents that are a result of known vulnerabilities. While implementing WSUS, you must keep in mind the hardware and software requirements for WSUS, the settings to configure, and the updates to approve or remove according to Contoso’s needs.

Update Management in Azure supports WSUS settings. You can specify sources for scanning and downloading updates using instructions in **Specify intranet Microsoft Update service location**. By default, the Windows Update client is configured to download updates from Windows Update. When you specify a WSUS server as a source for your machines, if the updates aren't approved in WSUS, update deployment fails.

Tip

To restrict machines to the internal update service, set **Do not connect to any Windows Update Internet locations**.

---

## Enable update management

*Azure Automation* is a cloud\-based service that provides process automation, configuration management, update management, and other management features for both Azure and non\-Azure environments, including on\-premises environments. Contoso can use Update Management, which is a free service in Automation to manage OS updates for Windows and Linux computers, both in the cloud and on\-premises.

Note

The associated Azure Log Analytics log storage does incur a charge based on the usage.

To implement Update Management in a hybrid environment, complete the following high\-level steps:

1. Create an Automation account.
2. Enable Update Management.
3. Onboard your on\-premises servers.
4. Schedule updates.

### Create an Automation account

When creating an Automation account, you'll choose an Azure region for the account. While the resources that are associated with the account are located in that region, the Automation account can manage any resources in your subscription. You can also choose to create a Run As account, which is a way to manage authentication for runbooks that use PowerShell. You don't need to create a Run As account to enable Update Management.

To create an Automation account, perform the following steps:

1. In the Azure portal, on the home page, search for and select **Automation Accounts**.
2. On the **Automation Accounts** blade, select **Create automation account**.
3. Enter the **Name**, and then select **Subscription**, **Resource group**, and **Location**.
4. In **Create Azure Run As account**, be sure to select **Yes**, and then select **Create**.

### Enable Update Management

To enable Update Management, in addition to having an Automation account you also must have an Azure Log Analytics workspace that's linked to that Automation account. The Log Analytics workspace must exist before enabling Update Management.

You can enable Update Management in Azure by using the:

* Azure Resource Manager template. Use a Resource Manager template to create a Log Analytics workspace, create an Automation account, link the Automation account to the Log Analytics workspace, and enable Update Management as one operation.
* Virtual machines dashboard in the Azure portal. You can enable Update Management and onboard Azure VMs from multiple resource groups and regions at the same time in the Virtual machines dashboard. When choosing this option, let Azure configure Log Analytics automatically, or create a custom configuration.
* **Virtual machine** page in the Azure portal. You can onboard a single VM and enable Update Management at the same time by selecting **Update management** from the options in the **Operations** section, and then selecting **Enable**.
* Automation account. You can enable **Update Management** from within an Automation account. With this option, you can automatically onboard Azure VMs and provide instructions for onboarding non\-Azure VMs such as on\-premises servers. You can also use an Azure runbook to onboard Azure VMs to Update Management. To do this, you must first onboard at least one VM.

To enable Update Management from your Automation Account, use the following procedure:

1. In the Azure portal, select your **Automation Account**.
2. In the **Automation Account** blade, select **Update Management**.
3. On the **Update Management** blade, you can verify that the Log Analytics workspace location, the Log Analytics workspace subscription, and the Automation account are already selected.
4. In the Log Analytics workspace list, select a suitable workspace, or select **Create New Workspace**, and then select **Enable**.

### Onboard your servers

The next step is to onboard your Azure VMs and on\-premises machines. To complete this task, return to your Automation Account, and then select **Update management**. You can review the details, and then select the **\+ Add Azure VMs**, **Add non\-Azure machine**, and **Manage machines** links from the menu.

#### Onboard Azure VMs

To add Azure VMs to Update management, use the following procedure:

1. In your Automation Account, select **Update management**.
2. Select **\+ Add Azure VMs**.
3. Select the VMs you want to onboard, and then select **Enable**.

Note

The VMs must use the Log Analytics workspace that you have configured for your Automation account, otherwise you cannot onboard the VMs.

#### Onboard on\-premises servers

You must manually add your on\-premises servers to Update Management in Automation. Before doing that, you must install the Log Analytics agent for Windows on the servers or VMs that you want to manage. Run the installation file interactively, or from the command line if you want to use Group Policy or other options to install the agent at scale. After the agent installs and starts reporting to your Automation account, choose which computers you want to manage in the **Update management** blade of your Automation account.

### Schedule updates

To schedule updates, navigate to your Automation account, select **Update management**, and then select **Schedule update deployment**. You can then add a name for the scheduled update deployment, and configure the properties for the update deployment.

Note

If you want to try configuring Update Management, refer to [Exercise: Use Update Management on a virtual machine](https://aka.ms/exercise-use-update-management-on-vm?azure-portal=true). You can use a trial Azure account to complete the exercise.

### Additional reading

You can learn more by reviewing the following documents:

* [Supported regions for linked Log Analytics workspace](https://aka.ms/region-mappings?azure-portal=true).
* [Enable Update Management from a runbook](/en-us/azure/automation/update-management/enable-from-runbook).
* [Install the agent using the command line](https://aka.ms/install-agent-using-command-line?azure-portal=true).
* [Log Analytics agent overview](https://aka.ms/log-analytics-agent?azure-portal=true).
* [Update Management overview](/en-us/azure/automation/update-management/overview).

---

## Deploy updates

You can use the Azure portal to configure update jobs, and to schedule them to run against onboarded VMs and physical servers. To create an update deployment, in the Azure portal, navigate to your automation account, select **Update management**, and then select **Schedule update deployment**.

### Create an update deployment

In the Azure portal, on the **Schedule update management** blade, you must configure the update deployment properties. This requires configuring the update deployment using the settings described in the following table.

| Setting | Your action |
| --- | --- |
| **Name** | Enter the name of the update deployment. |
| **Operating system** | Choose either **Windows** or **Linux**. |
| **Groups to update** | Select the groups to update. These are dynamic groups that Azure resolves at deployment time. You can preview the machines in the groups, but the final list of machines could change when the deployment starts. A query of more than 1,000 machines is currently not supported and will fail the update deployment. Azure and non\-Azure machines are supported. |
| **Machines to update** | Select from a list of available machines. |
| **Update classifications** | Select from the following list: **Critical updates**, **Security updates**, **Update rollups**, **Feature packs**, **Service packs**, **Definition updates**, **Tools**, and **Updates**. You can also select **Select all** for the default values. |
| **Include/exclude updates** | Enter the knowledge base (KB) ID of any updates you want to exclude, or specifically include. |
| **Schedule settings** | Specify the start date and time, the time zone, and the recurrence values. If the schedule recurs, then specify the interval and any expiration value. |
| **Pre\-scripts \+ Post\-scripts** | Pre\-scripts and Post\-scripts are tasks that can be automatically executed before or after an update deployment runs. Configure up to one Pre\-script and Post\-script per deployment. |
| **Maintenance window (minutes)** | Set the maintenance window in minutes. The duration must be a minimum of 30 minutes and less than 6 hours. The last 20 minutes of the maintenance window is dedicated to machine restart. Any remaining updates will not be started after this interval is reached. Updates which are in progress will be applied. The default maintenance window is 120 minutes. |
| **Reboot options** | Choose one from the following list: **Reboot if required**, **Never reboot**, **Always reboot**, and **Only reboot \- will not install updates**. |

### Additional reading

You can learn more by reviewing the following document.

* [Schedule an update deployment](https://aka.ms/schedule-an-update-deployment?azure-portal=true)

---

## View update assessments

In this demonstration, you'll learn to:

* Create an automation account.
* Enable auto\-update management.

### Next steps

You can review the steps for this demonstration at [View update assessments](/en-us/azure/automation/update-management/view-update-assessments#view-update-assessment)

If you want to repeat these steps, [get a free trial Azure subscription](https://aka.ms/Azure_free_account?azure-portal=true).

After completing the steps, delete any resource groups you created.

### Quick quiz

---

## Summary

Contoso IT staff were eager to find out how to manage their updates for both on\-premises and cloud\-based servers. They realized this could be challenging because few tools can manage both environments. However, by using the Azure Update Management service, they can manage updates for both cloud\-based and on\-premises servers.

In this module, you learned how to enroll Azure VMs in Azure Update Management. You also learned how to configure WSUS with Azure Update Management, and how to manage and deploy Azure updates.

### Learn more

You can learn more by reviewing the following documents:

* [Tutorial: Monitor changes and update a Windows virtual machine in Azure](https://aka.ms/tutorial-config-management?azure-portal=true)
* [Manage updates and patches for your Azure VMs](/en-us/azure/automation/update-management/manage-updates-for-vm)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/manage-azure-updates/_

## Fuentes
- [Manage Azure updates](https://learn.microsoft.com/en-us/training/modules/manage-azure-updates/?WT.mc_id=api_CatalogApi)
