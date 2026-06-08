# Monitor and manage performance and health

> Curso: Monitor and maintain an Azure Virtual Desktop infrastructure (wwl-monitor-maintain-azure-virtual-desktop-infrast) · Seccion: Monitor and maintain an Azure Virtual Desktop infrastructure
> Duracion estimada: 40 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

For Azure Virtual Desktop issues, check Azure Advisor first. Azure Advisor will give you directions for how to solve the problem, or at least point you towards a resource that can help.  

This module aligns with the exam AZ\-140: Configuring and Operating Microsoft Azure Virtual Desktop.

### Learning objectives

After completing this module, you'll be able to:

* Configure log collection and analysis for Azure Virtual Desktop session hosts
* Monitor Azure Virtual Desktop by using Azure Monitor
* Customize Azure Monitor workbooks for Azure Virtual Desktop Insights
* Optimize for capacity and performance
* Monitor Azure Virtual Desktop by using Azure Advisor
* Implement scaling plans in host pools

### Prerequisites

* Working experience with developing cloud applications.
* Conceptual knowledge of monitoring, messaging, events, and API management.

---

## Configure log collection and analysis for Azure Virtual Desktop session hosts

Azure Virtual Desktop uses [Azure Monitor](/en-us/azure/azure-monitor/overview) for monitoring and alerts like many other Azure services. This lets admins identify issues through a single interface. The service creates activity logs for both user and administrative actions. Each activity log falls under the following categories:

| **Category** | **Description** |
| --- | --- |
| Management Activities | Whether attempts to change Azure Virtual Desktop objects using APIs or PowerShell are successful. |
| Feed | Whether users can successfully subscribe to workspaces. |
| Connections | When users initiate and complete connections to the service. |
| Host registration | Whether a session host successfully registered with the service upon connecting. |
| Errors | Where users encounter issues with specific activities. |
| Checkpoints | Specific steps in the lifetime of an activity that were reached. |
| Agent Health Status | Monitor the health and status of the Azure Virtual Desktop agent installed on each session host. |
| Network | The average network data for user sessions to monitor for details including the estimated round\-trip time. |
| Connection Graphics | Performance data from the Azure Virtual Desktop graphics stream. |
| Session Host Management Activity | Management activity of session hosts. |
| Autoscale | Scaling operations. |

Connections that don't reach Azure Virtual Desktop won't show up in diagnostics results because the diagnostics role service itself is part of Azure Virtual Desktop. Azure Virtual Desktop connection issues can happen when the user is experiencing network connectivity issues.

Azure Monitor lets you analyze Azure Virtual Desktop data and review virtual machine (VM) performance counters, all within the same tool. This article will tell you more about how to enable diagnostics for your Azure Virtual Desktop environment.

Before you can use Azure Virtual Desktop with Log Analytics, you need:

* A Log Analytics workspace. For more information, see [Create a Log Analytics workspace in Azure portal](/en-us/azure/azure-monitor/logs/quick-create-workspace) or [Create a Log Analytics workspace with PowerShell](/en-us/azure/azure-monitor/logs/powershell-workspace-configuration). After you've created your workspace, follow the instructions in [Connect Windows computers to Azure Monitor](/en-us/azure/azure-monitor/agents/agent-windows#workspace-id-and-key) to get the following information:

	+ The workspace ID
	+ The primary key of your workspaceYou'll need this information later in the setup process.
* Access to specific URLs from your session hosts for diagnostics to work. For more information, see [Required URLs for Azure Virtual Desktop](/en-us/azure/virtual-desktop/safe-url-list) where you'll see entries for Diagnostic output.
* Make sure to review permission management for Azure Monitor to enable data access for users who monitor and maintain your Azure Virtual Desktop environment. For more information, see [Get started with roles, permissions, and security with Azure Monitor](/en-us/azure/azure-monitor/roles-permissions-security).

### Push diagnostics data to your workspace

You can push diagnostics data from your Azure Virtual Desktop objects into the Log Analytics for your workspace. You can set up this feature right away when you first create your objects.

To set up Log Analytics for a new object:

1. Sign in to the Azure portal and go to **Azure Virtual Desktop**.
2. Navigate to the object (such as a host pool, application group, or workspace) that you want to capture logs and events for.
3. Select **Diagnostic settings**
4. Select **Add diagnostic setting**. The options shown in the **Diagnostic Settings** page will vary depending on what kind of object you're editing. Remember to enable diagnostics for each Azure Resource Manager object that you want to monitor. Data will be available for activities after diagnostics has been enabled. It might take a few hours after first set\-up.
5. Enter a name for your settings configuration, then select **Send to Log Analytics**. The name you use shouldn't have spaces and should conform to [Azure naming conventions](/en-us/azure/azure-resource-manager/management/resource-name-rules).
6. Select **Save**.

### How to access Log Analytics

You can access Log Analytics workspaces on the Azure portal or Azure Monitor.

#### Access Log Analytics on a Log Analytics workspace

1. Sign in to the Azure portal.
2. Search for **Log Analytics workspace**.
3. Under **Services**, select **Log Analytics workspaces**.
4. From the list, select the workspace you configured for your Azure Virtual Desktop object.
5. Once in your workspace, select **Logs**. You can filter out your menu list with the Search function.

#### Access Log Analytics on Azure Monitor

1. Sign in to the Azure portal.
2. Search for and select **Monitor**.
3. Select **Logs**.
4. Follow the instructions in the logging page to set the scope of your query.
5. You're ready to query diagnostics. All diagnostics tables have a "WVD" prefix.

---

## Customize Azure Monitor workbooks for Azure Virtual Desktop Insights

Azure Virtual Desktop Insights is a dashboard built on Azure Monitor Workbooks that helps IT professionals understand their Azure Virtual Desktop environments. This unit will walk you through how to set up Azure Virtual Desktop Insights to monitor your Azure Virtual Desktop environments.

Before you start using Azure Virtual Desktop Insights, you'll need to set up the following things:

* All Azure Virtual Desktop environments you monitor must be based on the latest release of Azure Virtual Desktop that’s compatible with Azure Resource Manager.
* At least one configured Log Analytics Workspace. Use a designated Log Analytics workspace for your Azure Virtual Desktop session hosts to ensure that performance counters and events are only collected from session hosts in your Azure Virtual Desktop deployment.
* Enable data collection for the following things in your Log Analytics workspace:

	+ Diagnostics from your Azure Virtual Desktop environment
	+ Recommended performance counters from your Azure Virtual Desktop session hosts
	+ Recommended Windows Event Logs from your Azure Virtual Desktop session hostsThe data setup process described in this unit is the only one you'll need to monitor Azure Virtual Desktop. You can disable all other items sending data to your Log Analytics workspace to save costs.
* Anyone monitoring Azure Virtual Desktop Insights for your environment will also need to have the following Azure role\-based access control (RBAC) roles assigned as a minimum:

	+ [Desktop Virtualization Reader](/en-us/azure/role-based-access-control/built-in-roles#desktop-virtualization-reader) assigned on the resource group or subscription where the host pools, workspaces and session hosts are.
	+ [Log Analytics Reader](/en-us/azure/role-based-access-control/built-in-roles#log-analytics-reader) assigned on any Log Analytics workspace used with Azure Virtual Desktop Insights.

### Log Analytics settings

To start using Azure Virtual Desktop Insights, you'll need at least one Log Analytics workspace. Use a designated Log Analytics workspace for your Azure Virtual Desktop session hosts to ensure that performance counters and events are only collected from session hosts in your Azure Virtual Desktop deployment. If you already have a workspace set up, skip ahead to [Set up the configuration workbook](/en-us/azure/virtual-desktop/insights?tabs=monitor#set-up-the-configuration-workbook). To set one up, see [Create a Log Analytics workspace in the Azure portal](/en-us/azure/azure-monitor/logs/quick-create-workspace).

### Set up the configuration workbook

If it's your first time opening Azure Virtual Desktop Insights, you'll need to set up Azure Virtual Desktop Insights for your Azure Virtual Desktop environment. To configure your resources:

1. Open Azure Virtual Desktop Insights in the Azure portal at [aka.ms/avdi](https://aka.ms/avdi).
2. Select **Workbooks**, then select **Check Configuration**.
3. Select an Azure Virtual Desktop environment to configure from the drop\-down lists for **Subscription**, **Resource Group**, and **Host Pool**.

The configuration workbook sets up your monitoring environment and lets you check the configuration after you've finished the setup process. It's important to check your configuration if items in the dashboard aren't displaying correctly, or when the product group publishes updates that require new settings.

#### Resource diagnostic settings

To collect information on your Azure Virtual Desktop infrastructure, you'll need to enable several diagnostic settings on your Azure Virtual Desktop host pools and workspaces (this is your Azure Virtual Desktop workspace, not your Log Analytics workspace).

To set your resource diagnostic settings in the configuration workbook:

1. Select the **Resource diagnostic settings** tab in the configuration workbook.
2. Select **Log Analytics workspace** to send Azure Virtual Desktop diagnostics.

##### Host pool diagnostic settings

To set up host pool diagnostics using the resource diagnostic settings section in the configuration workbook:

* Under **Host pool**, check to see whether Azure Virtual Desktop diagnostics are enabled. If they aren't, an error message will appear that says "No existing diagnostic configuration was found for the selected host pool." You'll need to enable the following supported diagnostic tables:

	+ Management Activities
	+ Feed
	+ Connections
	+ Errors
	+ Checkpoints
	+ HostRegistration
	+ AgentHealthStatus

##### Workspace diagnostic settings

To set up workspace diagnostics using the resource diagnostic settings section in the configuration workbook:

* Under **Workspace**, check to see whether Azure Virtual Desktop diagnostics are enabled for the Azure Virtual Desktop workspace. If they aren't, an error message will appear that says "No existing diagnostic configuration was found for the selected workspace." You'll need to enable the following supported diagnostics tables:

	+ Management Activities
	+ Feed
	+ Errors
	+ Checkpoints

#### Session host data settings

You can use either the Azure Monitor Agent or the Log Analytics agent to collect information on your Azure Virtual Desktop session hosts. We recommend you use the Azure Monitor Agent as the Log Analytics Agent will be deprecated on August 31st, 2024\. Select the relevant tab for your scenario.

* [Azure Monitor Agent](/en-us/azure/virtual-desktop/insights?tabs=monitor#tabpanel_1_monitor)
* [Log Analytics agent](/en-us/azure/virtual-desktop/insights?tabs=monitor#tabpanel_1_analytics)

To collect information on your Azure Virtual Desktop session hosts, you must configure a [Data Collection Rule (DCR)](/en-us/azure/azure-monitor/essentials/data-collection-rule-overview) to collect performance data and Windows Event Logs, associate the session hosts with the DCR, install the Azure Monitor Agent on all session hosts in host pools you're collecting data from, and ensure the session hosts are sending data to a Log Analytics workspace.

The Log Analytics workspace you send session host data to doesn't have to be the same one you send diagnostic data to.

To configure a DCR and select a Log Analytics workspace destination using the configuration workbook:

1. From the Azure Virtual Desktop overview page, select **Host pools**, then select the pooled host pool you want to monitor.
2. From the host pool overview page, select **Insights**, then select **Open Configuration Workbook**.
3. Select the **Session host data settings** tab in the configuration workbook.
4. For **Workspace destination**, select the **Log Analytics workspace** you want to send session host data to.
5. For **DCR resource group**, select the resource group in which you want to create the DCR.
6. Select **Create data collection rule** to automatically configure the DCR using the configuration workbook. This option only appears once you've selected a workspace destination and a DCR resource group.

---

## Implement scaling plans in host pools

Autoscale lets you scale your session host virtual machines (VMs) in a host pool up or down according to schedule to optimize deployment costs.

* Azure Virtual Desktop (classic) doesn't support autoscale.
* You can't use autoscale and [scale session hosts using Azure Automation and Azure Logic Apps](/en-us/azure/virtual-desktop/scaling-automation-logic-apps) on the same host pool. You must use one or the other.
* Autoscale is available in Azure and Azure Government.
* Autoscale support for Azure Stack HCI with Azure Virtual Desktop is currently in PREVIEW. See the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/) for legal terms that apply to Azure features that are in beta, preview, or otherwise not yet released into general availability.

For best results, we recommend using autoscale with VMs you deployed with Azure Virtual Desktop Azure Resource Manager templates or first\-party tools from Microsoft.

### To use scaling plans, make sure you follow these guidelines

* Scaling plan configuration data must be stored in the same region as the host pool configuration. Deploying session host VMs is supported in all Azure regions.
* When using autoscale for pooled host pools, you must have a configured *MaxSessionLimit* parameter for that host pool. Don't use the default value. You can configure this value in the host pool settings in the Azure portal or run the [New\-AzWvdHostPool](/en-us/powershell/module/az.desktopvirtualization/new-azwvdhostpool) or [Update\-AzWvdHostPool](/en-us/powershell/module/az.desktopvirtualization/update-azwvdhostpool) PowerShell cmdlets.
* You must grant Azure Virtual Desktop access to manage the power state of your session host VMs. You must have the Microsoft.Authorization/roleAssignments/write permission on your subscriptions in order to assign the role\-based access control (RBAC) role for the Azure Virtual Desktop service principal on those subscriptions.
* If you want to use personal desktop autoscale with hibernation, you'll need to enable the hibernation feature for VMs in your personal host pool. FSLogix and app attach currently don't support hibernate. Don't enable hibernate if you're using FSLogix or app attach for your personal host pools. For the full list of prerequisites for hibernation, see [Prerequisites to use hibernation](/en-us/azure/virtual-machines/hibernate-resume).
* If you're using PowerShell to create and assign your scaling plan, you'll need module [Az.DesktopVirtualization](https://www.powershellgallery.com/packages/Az.DesktopVirtualization/) version 4\.2\.0 or later.
* If you are [configuring a time limit policy using Microsoft Intune](/en-us/azure/virtual-desktop/autoscale-create-assign-scaling-plan?tabs=portal#configure-a-time-limit-policy-using-microsoft-intune), you will need:

	+ A Microsoft Entra ID account that is assigned the Policy and Profile manager built\-in RBAC role.
	+ A group containing the devices you want to configure.

### Assign the Desktop Virtualization Power On Off Contributor role with the Azure portal

Before creating your first scaling plan, you'll need to assign the *Desktop Virtualization Power On Off Contributor* RBAC role to the Azure Virtual Desktop service principal with your Azure subscription as the assignable scope. Assigning this role at any level lower than your subscription, such as the resource group, host pool, or VM, will prevent autoscale from working properly. You'll need to add each Azure subscription as an assignable scope that contains host pools and session host VMs you want to use with autoscale. This role and assignment will allow Azure Virtual Desktop to manage the power state of any VMs in those subscriptions. It will also let the service apply actions on both host pools and VMs when there are no active user sessions.

### Create a scaling plan

Now that you've assigned the *Desktop Virtualization Power On Off Contributor* role to the service principal on your subscriptions, you can create a scaling plan. To create a scaling plan using the portal:

1. Sign in to the [Azure portal](https://portal.azure.com/).
2. In the search bar, type *Azure Virtual Desktop* and select the matching service entry.
3. Select **Scaling Plans**, then select **Create**.
4. In the **Basics** tab, look under **Project details** and select the name of the subscription you'll assign the scaling plan to.
5. If you want to make a new resource group, select **Create new**. If you want to use an existing resource group, select its name from the drop\-down menu.
6. Enter a name for the scaling plan into the **Name** field.
7. Optionally, you can also add a "friendly" name that will be displayed to your users and a description for your plan.
8. For **Region**, select a region for your scaling plan. The metadata for the object will be stored in the geography associated with the region. To learn more about regions, see [Data locations](/en-us/azure/virtual-desktop/data-locations).
9. For **Time zone**, select the time zone you'll use with your plan.
10. For **Host pool type**, select the type of host pool that you want your scaling plan to apply to.
11. In **Exclusion tags**, enter a tag name for VMs you don't want to include in scaling operations. For example, you might want to tag VMs that are set to drain mode so that autoscale doesn't override drain mode during maintenance using the exclusion tag "excludeFromScaling". If you've set "excludeFromScaling" as the tag name field on any of the VMs in the host pool, autoscale won't start, stop, or change the drain mode of those particular VMs.
12. Select **Next**, which should take you to the **Schedules** tab. Schedules let you define when autoscale turns VMs on and off throughout the day. The schedule parameters are different based on the **Host pool type** you chose for the scaling plan.

#### Pooled host pools

In each phase of the schedule, autoscale only turns off VMs when in doing so the used host pool capacity won't exceed the capacity threshold. The default values you'll see when you try to create a schedule are the suggested values for weekdays, but you can change them as needed.

To create or change a schedule:

1. In the **Schedules** tab, select **Add schedule**.
2. Enter a name for your schedule into the **Schedule name** field.
3. In the **Repeat on** field, select which days your schedule will repeat on.
4. In the **Ramp up** tab, fill out the following fields:

	* For **Start time**, select a time from the drop\-down menu to start preparing VMs for peak business hours.
	* For **Load balancing algorithm**, we recommend selecting **breadth\-first algorithm**. Breadth\-first load balancing will distribute users across existing VMs to keep access times fast.
	* For **Minimum percentage of hosts**, enter the percentage of session hosts you want to always remain on in this phase. If the percentage you enter isn't a whole number, it's rounded up to the nearest whole number. For example, in a host pool of seven session hosts, if you set the minimum percentage of hosts during ramp\-up hours to **10%**, one VM will always stay on during ramp\-up hours, and it won't be turned off by autoscale.
	* For **Capacity threshold**, enter the percentage of available host pool capacity that will trigger a scaling action to take place. For example, if two session hosts in the host pool with a max session limit of 20 are turned on, the available host pool capacity is 40\. If you set the capacity threshold to **75%** and the session hosts have more than 30 user sessions, autoscale will turn on a third session host. This will then change the available host pool capacity from 40 to 60\.
5. In the **Peak hours** tab, fill out the following fields:

	* For **Start time**, enter a start time for when your usage rate is highest during the day. Make sure the time is in the same time zone you specified for your scaling plan. This time is also the end time for the ramp\-up phase.
	* For **Load balancing**, you can select either breadth\-first or depth\-first load balancing. Breadth\-first load balancing distributes new user sessions across all available session hosts in the host pool. Depth\-first load balancing distributes new sessions to any available session host with the highest number of connections that hasn't reached its session limit yet.

---

## Optimize capacity and performance

Use the Performance Diagnostics tool to identify and troubleshoot performance issues on your Azure virtual machine (VM) in one of two modes:

* Continuous diagnostics (preview) collects data at five\-second intervals and reports actionable insights about high resource usage every five minutes.
* On\-demand diagnostics helps you troubleshoot an ongoing performance issue with more in\-depth data, insights, and recommendations based on data collected at a single point in time.

Performance Diagnostics stores all insights and reports in a storage account, which you can configure for short data retention to minimize costs.

Run Performance Diagnostics directly from the Azure portal, where you can also review insights and a report on various logs, rich configuration, and diagnostics data. We recommend that you run Performance Diagnostics and review the insights and diagnostics data before you contact Microsoft Support.

This unit explains how to use Performance Diagnostics and what the continuous and on\-demand modes offer.

The following operating systems are currently supported for both on\-demand and continuous diagnostics:

* Windows Server 2022
* Windows Server 2019
* Windows Server 2016
* Windows Server 2012 R2
* Windows Server 2012
* Windows 11
* Windows 10

### Install and run Performance Diagnostics on your VM

To install and run Performance Diagnostics:

1. In the [Azure portal](https://portal.azure.com/), select Virtual machines.
2. From the list of VM names, select the VM that you want to run diagnostics on.
3. In the **Help** section, select **Performance Diagnostics**.
4. Select **Enable Performance Diagnostics.**
5. Select the options to install and run for the tool.
6. This table describes the available options. Review the legal terms and privacy policy, and select the corresponding checkbox to acknowledge (required).

| **Option** | **Description** |
| --- | --- |
| Enable continuous diagnostics | Get continuous, actionable insights into high resource usage with data collected every 5 seconds and updates uploaded every 5 minutes to address performance issues promptly. Store insights in your preferred storage account. |
| Run on\-demand diagnostics | Get on\-demand, actionable insights into high resource usage and various system configurations. Receive a downloadable report with comprehensive diagnostics data to address performance issues. Store insights and reports in your preferred storage account. |
| Storage account | Optionally, if you want to use a single storage account to store the Performance Diagnostics results for multiple VMs, you can select a storage account from the dropdown. If you don't specify a storage account, Performance Diagnostics uses the default diagnostics storage account or creates a new storage account. |
7. To install and run **Performance Diagnostics**, you must agree to the legal terms and accept the privacy policy.
8. Select **Apply** to apply the selected options and install the tool. A notification is displayed as Performance Diagnostics starts to install. After the installation is completed, you see a notification that indicates that the installation is successful. If the Run on\-demand diagnostics option is selected, the selected performance analysis scenario is then run for the specified duration.

### View insights and reports

This table compares the data provided by Continuous and On\-demand Performance Diagnostics.

|  | **Continuous Performance Diagnostics** | **On\-demand Performance Diagnostics** |
| --- | --- | --- |
| **Availability** | Currently supported only for Windows VMs | Supported for both Windows and Linux VMs |
| **Insights generated** | Continuous actionable insights into high resource usage, such as high CPU, high memory, and high disk usage | On\-demand actionable insights into high resource usage and various system configurations |
| **Data collection frequency** | Collects data every 5 seconds, updates uploaded every 5 minutes | Collect data on demand for the selected duration of the on\-demand run |
| **Reports generated** | Doesn't generate a report | Generates a report with comprehensive diagnostics data |

---

## Module assessment

Choose the best response for each question.

### Check your knowledge

---

## Summary

In this module, you learned how to:

* Configure log collection and analysis for Azure Virtual Desktop session hosts
* Monitor Azure Virtual Desktop by using Azure Monitor
* Customize Azure Monitor workbooks for Azure Virtual Desktop Insights
* Optimize for capacity and performance
* Monitor Azure Virtual Desktop by using Azure Advisor
* Implement scaling plans in host pools

### Learn more

* [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) \| [Azure free account FAQ](https://azure.microsoft.com/pricing/purchase-options/azure-account#FAQ?cid=msft_learn)
* [Free account for Students](https://azure.microsoft.com/free/students/?cid=msft_learn) \| [Azure for students FAQ](/en-us/azure/education-hub/azure-dev-tools-teaching/program-faq#azure-for-students/?azure-portal=true)
* [Create an Azure account](/en-us/learn/modules/create-an-azure-account/?azure-portal=true) module on Learn.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/monitor-manage-performance-health/_

## Fuentes
- [Monitor and manage performance and health](https://learn.microsoft.com/en-us/training/modules/monitor-manage-performance-health/?WT.mc_id=api_CatalogApi)
