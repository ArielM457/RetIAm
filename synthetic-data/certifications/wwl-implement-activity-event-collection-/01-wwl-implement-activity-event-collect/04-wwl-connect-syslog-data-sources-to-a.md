# Connect syslog data sources to Microsoft Sentinel

> Curso: Implement activity and event collection in Microsoft Sentinel (wwl-implement-activity-event-collection-sentinel) · Seccion: Implement activity and event collection in Microsoft Sentinel
> Duracion estimada: 28 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You send Syslog log data to the Microsoft Sentinel workspace using an Azure Monitor Agent Data Collection Rule (DCR).

You're a Security Operations Analyst working at a company that implemented Microsoft Sentinel. You need to collect log data from on\-premises network appliances. The network appliances' data is provided in an unstructured format.

You install an on\-premises Linux host used as a forwarder to send the log data. Next, you follow the instructions to install the Azure Connected Machine agent that enables you to manage your (Windows and) Linux machines hosted outside of Azure on your corporate network with Azure Arc. Once you have verified Azure Arc connectivity, you can install the Azure Monitor Linux Agent extension, and during that process you create an Azure Monitor Syslog Data Collection Rule. The final step is to configure the network appliances to forward their logs to your Linux host.

The network appliances are now sending logs to the new Linux host, and the Linux host is then forwarding the logs to the Microsoft Sentinel workspace via the Azure Monitor Agent Data Collection Rule. In Microsoft Sentinel, you create a parser using a KQL function to make it easier for the Security Operations team to query the log records containing the unstructured string data.

After completing this module, you'll be able to:

* Describe the Azure Monitor Agent Data Collection Rule (DCR) for Syslog
* Install and Configure the Azure Monitor Linux Agent extension with the Syslog DCR
* Run the Azure Arc Linux deployment and connection scripts
* Verify Syslog log data is available in Microsoft Sentinel
* Create a parser using KQL in Microsoft Sentinel

### Prerequisites

* Basic knowledge of operational concepts such as monitoring, logging, and alerting
* Familiarity with Linux operations and monitoring

---

## Plan for syslog data collection

Caution

This article references CentOS, a Linux distribution that is End Of Life (EOL) status. Please consider your use and plan accordingly. For more information, see the [CentOS End Of Life guidance](/en-us/azure/virtual-machines/workloads/centos/centos-end-of-life).

You can stream events from Linux\-based, Syslog\-supporting machines or appliances into Microsoft Sentinel using the Azure Monitor Agent for Linux and Data Collection Rules. You can do this streaming for any device that allows you to install the agent directly on the host. The host's native Syslog daemon collects local events of the specified types and forward them locally to the agent, which streams them to your Log Analytics workspace.

Log Analytics supports collecting messages sent by the **rsyslog** or **syslog\-ng** daemons, where rsyslog is the default. The default syslog daemon on version 5 of Red Hat Enterprise Linux (RHEL), CentOS, and Oracle Linux version (sysklog) isn't supported for Syslog event collection. The rsyslog daemon should be installed and configured to replace sysklog for these versions of Linux.

### How it works

**Syslog** is an event logging protocol that is common to Linux. When the agent is installed on your VM or appliance, the installation routine configures the local Syslog daemon to forward messages to the agent on TCP port 25224\. The agent then sends the message to your Log Analytics workspace over HTTPS, where it's parsed into an event log entry in the Syslog table in **Microsoft Sentinel \> Logs**.

---

## Collect data from Linux\-based sources using syslog

Configuring the Azure Monitor Agent for Syslog on Linux machines:

* [Azure Linux VM](#tabpanel_1_azure-linux-vm)
* [Non\-Azure Linux machine](#tabpanel_1_non-azure-linux-machine)

To install the agent on an Azure Linux virtual machine:

1. In the Azure portal, enter **Monitor** in the `Search resources, services, and docs` search bar.
2. In **Monitor**, scroll down the left menu to the **Settings** section and select `Data Collection Rules`.
3. In **Monitor \| Data Collection Rules**, select **\+ Create**.
4. On the `Data Collection Rule` **Basics** tab, enter a Rule name and specify a Subscription, Resource Group, Region, and Platform Type. For this exercise, select `Linux` for Platform Type.
5. Select **Next:Resources**
6. On the `Data Collection Rule` **Resources** tab, select **\+ Add resources**.
7. In the **Select a scope** page, expand the **Scope** column for `Subscription` and `Resource group` types until your target VM is displayed.
8. Select the target VM and select **Apply**. You should see your Linux VM displayed as a Resource.
9. Select **Next: Collect and deliver**.
10. On the `Data Collection Rule` **Collect and deliver** tab, select **\+ Add data source**.
11. In the **Add data source** page, select **Linux Syslog** from the `Data source type*` drop\-down menu, and select **Add data source**. You should see your `Linux Syslog` Data source and a `Destinations(s)` of `Azure Monitor Logs`displayed.
12. Select **Review \+ create**, and **Create** after **Validation passed** is displayed.

Note

This process initiates the Azure Monitor Linux Agent extension install.
13. After the process completes, locate **Virtual Machines** in the Azure portal and select the Linux VM you configured as a `Data Collection Rule` resource.
14. On the `Virtual machine` Overview, scroll down the left menu to the **Settings** section and select **Extensions \+ applications**.
15. Under the **Extensions** tab, you should see the **AzureMonitorLinuxAgent** displayed.

Note

If Microsoft Defender for Cloud Auto\-provisioning is enabled, the Azure Monitor Linux Agent is installed by default as an extension using Azure Policy assignment.

To install the agent on non\-Azure Linux physical or virtual machines:

1. In the Azure portal, enter **Arc** in the `Search resources, services, and docs` search bar.
2. In **Azure Arc**, scroll down the left navigation menu to the **Azure Arc resources** section and select **Machines**.
3. On the **Machines** page, select **\+ Add/Create** and **Add a machine**.
4. On the **Add servers with Azure Arc** page, locate the **Add a single server box**, and select **Generate script**.
5. On the **Add servers with Azure Arc** page, **Basics** tab, select your **Subscription** and **Resource group** from the drop\-down menus under **Project details**.

Tip

Select an Azure region in **Server details** before creating a new Resource groups.
6. In the **Server details** section, select your **Region** and then select **Linux** from the **Operating system** drop\-down menu under.
7. Select the appropriate **Connectivity method** from the radio buttons under **Connectivity method**, and then select **Next**.
8. On the **Add servers with Azure Arc** page, **Tags** tab, enter `Physical locations tags` as needed and select **Next**.
9. On the **Add servers with Azure Arc** page, **Download and run script** tab, either download or copy the script to the clipboard.

Tip

If you're using a Microsoft Windows system with Microsoft Azure, it's easy to copy and paste the script into notepad, then ssh into your Linux machine with PowerShell to run the script in a Bash console.
10. Open a `Bash console` as an administrative (root) user on your non\-Azure Linux machine and run the script.

This script does the following:

	* Download an installation script from the Microsoft Download Center.
	* Configure the package manager to use and trust the packages.microsoft.com repository.
	* Download the agent from Microsoft's Linux Software Repository.
	* Install the agent on the server.
	* Create the Azure Arc\-enabled server resource and associate it with the agent.
11. When the script successfully completes, you should see a message stating `Latest version of azcmagent is installed`.
12. On the **Add servers with Azure Arc** page, **Download and run script** tab, select **Close**.
13. The next step is to connect your non\-Azure Linux server `azcmagent` to **Azure Arc**.
14. Copy and edit the following Bash script to include the required parameters in double quotes:

```
sudo azcmagent connect --resource-group "$resourceGroup" --tenant-id "$tenantID" --location "$location" --subscription-id "$subscriptionID" --cloud "$cloud" --correlation-id "$correlationId";

```

Tip

You can use the export (variables) entries from the agent install script you downloaded or copied to fill in the parameters required in the agent connect script.
15. When the script editing is complete, open a `Bash console` as an administrative (root) user on your non\-Azure Linux machine and run the script.
16. The script tests connectivity to Azure endpoints and then requests you to sign in to `https://microsoft.com/devicelogin` and enter the supplied code to authenticate.
17. Open a Web browser and navigate to the address as directed, and paste or enter the code into the form and select **Next** to sign in.
18. On the **Pick an account** page, select your `administrator account`, and then select **Next**. Close browser tabs when complete.
19. In your `Bash console`, you should see an `INFO Connected machine to Azure` message.
20. Verify your non\-Azure machine is connected to **Azure Arc** in the Azure portal by entering **Arc** in the `Search resources, services, and docs` search bar.
21. In **Azure Arc**, scroll down the left navigation menu to the **Azure Arc resources** section and select **Machines**. You should see your machine with an `Arc agent Status` of **Connected**.

Note

Select Refresh if the Linux machine isn't displayed.
22. The next task is to add your newly connected Azure Arc Linux server to your previously created Data Collection Rule for Syslog.
23. In the Azure portal, enter **DCR** in the `Search resources, services, and docs` search bar.
24. Select your Syslog Data Collection Rule
25. In your `Data Collection Rule`, scroll down the left menu to the **Configuration** section and select **Resources**.
26. In **Resources** select **\+ Add**
27. In the **Select a scope** page, expand the **Scope** column until your **Server \- Azure Arc** `Resource type` newly connected Linux machine is displayed.
28. Select the Linux Azure Arc machine and select **Apply**
29. The Linux Azure Arc VM is now included as one of the `Data Collection Rule` Resources.

---

## Configure the Data Collection Rule for Syslog Data Sources

The Data Collection Rule (DCR) only collects events with the facilities and severities that are specified in its Data sources configurations. For Syslog, you can modify the `Facility Minimum log level` and `Destination` in the **Add data source** page.

To configure the Syslog `Facility log level`and `Destination`:

1. Access the Data collection rule Data sources **Add data source** page:

	* Select **Configuration**, **Data sources**
	* Select **Linux Syslog**.
2. Select the **Minimum log level** drop\-down menu to make changes for each `Facility`.
3. When completed select **Save**

Note

The default is "LOG\_DEBUG" for each Facility, and changes are automatically pushed to all configured resources.

---

## Parse syslog data with KQL

The Syslog collector writes log data to the Syslog table. One difference from the CEF Collector is that the message's data is stored in a string field named SyslogMessage. The Common Event Format (CEF) Connector writes to the CommonSecurityLog with the fields already parsed. For Syslog, you'll need to parse fields on every query that uses the Syslog table or write a Parser. A Parser is a KQL Function that is a query saved as a function and then referenced with the function name. The reference to the function name is like accessing any other table. By creating parses, you only need to write the SyslogMessage parsing once.

In the Logs window, create a query, select the Save button, and select Function from the drop\-down. Then specify function name and alias. In this case, if we create the Function named MyParser, I then can access the table using the name MyParser.

```
Syslog
| where ProcessName contains "squid"
| extend URL = extract("(([A-Z]+ [a-z]{4,5}:\\/\\/)|[A-Z]+ )([^ :]*)",3,SyslogMessage), 
         SourceIP = extract("([0-9]+ )(([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3}))",2,SyslogMessage), 
         Status = extract("(TCP_(([A-Z]+)(_[A-Z]+)*)|UDP_(([A-Z]+)(_[A-Z]+)*))",1,SyslogMessage), 
         HTTP_Status_Code = extract("(TCP_(([A-Z]+)(_[A-Z]+)*)|UDP_(([A-Z]+)(_[A-Z]+)*))/([0-9]{3})",8,SyslogMessage),
         User = extract("(CONNECT |GET )([^ ]* )([^ ]+)",3,SyslogMessage),
         RemotePort = extract("(CONNECT |GET )([^ ]*)(:)([0-9]*)",4,SyslogMessage),
         Domain = extract("(([A-Z]+ [a-z]{4,5}:\\/\\/)|[A-Z]+ )([^ :\\/]*)",3,SyslogMessage)
| extend TLD = extract("\\.[a-z]*$",0,Domain)

```

```
MyParser

```

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary and resources

You should have learned how to send Syslog log data to the Microsoft Sentinel workspace using the provided data connector.

You should now be able to:

* Describe the Azure Monitor Agent Data Collection Rule (DCR) for Syslog
* Run the Azure Arc Linux deployment and connection scripts
* Install and Configure the Azure Monitor Linux Agent extension with the Syslog DCR
* Verify Syslog log data is available in Microsoft Sentinel
* Create a parser using KQL in Microsoft Sentinel

### Learn more

You can learn more by reviewing the following.

[Collect Syslog events with Azure Monitor Agent](/en-us/azure/azure-monitor/agents/data-collection-syslog)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/connect-syslog-data-sources-to-azure-sentinel/_

## Fuentes
- [Connect syslog data sources to Microsoft Sentinel](https://learn.microsoft.com/en-us/training/modules/connect-syslog-data-sources-to-azure-sentinel/?WT.mc_id=api_CatalogApi)
