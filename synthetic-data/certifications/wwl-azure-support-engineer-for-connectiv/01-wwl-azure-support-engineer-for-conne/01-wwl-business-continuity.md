# Troubleshoot business continuity with Microsoft Azure

> Curso: Azure Support Engineer for Connectivity Specialty (wwl-azure-support-engineer-for-connectivity-specia) · Seccion: Azure Support Engineer for Connectivity Specialty
> Duracion estimada: 33 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

As an Azure network support engineer, you understand that business data is valuable, and needs to be protected from internal and external risks. When you encounter problems with backing up or recovery, you need to know how to approach the problem. In this module, you will learn how to monitor the status of backups, review logs, and troubleshoot common issues that occur when backing up and recovering data.

### Learning objectives

By the end of this module, you will be able to:

* Review the status of a backup job, manage alerts, and review logs.
* Troubleshoot backing and restoring a virtual machine (VM).
* Troubleshoot Microsoft Azure Recovery Services backups.
* Troubleshoot backing up and restoring servers.
* Troubleshoot Azure to Azure Site Recovery.
* Troubleshoot site recovery with Hyper\-V, VMM, and VMware.

### Prerequisites

* Demonstrate an understanding of the OSI model
* Demonstrate an understanding of Azure CLI
* Demonstrate an understanding of PowerShell
* Know how to run Cloud Shell to run commands

---

## Troubleshoot backup issues with Microsoft Azure

### Review backup status in the Azure portal

The Azure Backup Center is a one\-stop location to manage Azure backups including:

* Azure VM backup
* SQL in Azure VM backup
* SAP HANA in Azure VM backup
* Azure Files backup
* Azure Blobs backup
* Azure Managed Disks backup
* Azure Database for PostgreSQL Server backup

For information about supported scenarios, see the [Support matrix for Backup center](/en-us/azure/backup/backup-center-support-matrix).

In the Azure portal, search for Backup center in the Search bar. You can then pin the Backup center to your dashboard. Use the filter options to view the specific jobs you are interested in. You can filter on the following parameters:

* Datasource subscription, resource group, location, tag, or type
* Vault
* Protection status

Use the Backup jobs menu to review the job status. You can review the time the backup started, the duration, the job operation, and its status. You can also display the backup instance associated with the job, the subscription, resource group, and location.

Select an item in the grid to get more details. Right\-click an item to go to the resource and take any necessary actions.

#### Review and respond to backup alerts

From the Backup center left menu, under Monitoring \+ reporting, select Alerts (preview).

By default, the summary displays open alerts in the last 24 hours. You can also filter by a range of parameters:

* Datasource subscription
* Datasource resource group
* Datasource location
* Datasource type
* Vault
* Severity (0 \= critical, 1 \= error, 2 \= warning, 3 \= informational, and 4 \= verbose)
* State (New, acknowledged, closed)
* Type (Security alert, configured alert)
* Signal type (metric or log)
* Time range (24 hours, week, two weeks, 30 days, or custom)

#### Alerts by email notification

You can get email notifications when alerts are triggered by creating an alert processing rule.

* From the Azure portal, go to the Backup center.
* From the left menu, select Alerts (Preview).
* From the top menu, select Alert processing rule (preview).
* From the top menu, select Create.
* In the Scope section, select Select scope to display the Select Scope pane.
* Select the resource you want the alert processing rule applied to by either selecting from the drop\-down list, or by typing to filter the resources. The matching resources are then displayed. Use the check boxes to select the resources you want the alert processing rule to apply to.
* Alternatively, you can apply the rule for all resources within a subscription. When the Select Scope pane is displayed, select the check box next to the correct subscription.
* In the Filter section, you can apply one or more filters. For example, select Severity to generate notifications for alerts of a certain severity.
* Under Rule Settings, create an action group (or use an existing one). An action group is the destination to which the alert notification should be sent, such as an email address.
* On the Basics tab, select the name of the action group, the subscription, and resource group under which it should be created.
* On the Notifications tab, select Email/SMS message/Push/Voice and enter the recipient’s details.
* Test the action group. A test email is sent to the specified email addresses.
* Select Review \+ Create, and then Create to save the action group.
* Select Create to save the action rule.

#### Review and interpret backup logs

To review and interpret backup logs, select the Backup Reports menu in the Backup center. When configured, Azure Backup Reports allow you to audit your backups and restores, analyze trends, and track and forecast usage.

Configure diagnostics settings for a Recovery Services vault by going to the vault and selecting Diagnostics settings. Select \+ Add Diagnostic Setting for the metrics you want to collect. Under Destination details, select the destinations that you want to stream them to. This includes Log Analytics workspace as an option.

The following views are available from the tabs:

* Overview – select specific subscriptions and workspaces, and links to more information.
* Summary – a high\-level overview of your backup estate.
* Backup Items – cloud storage consumed at a backup item level.
* Usage – key billing parameters for your backups.
* Jobs – view long\-running trends on jobs, such as the number of failed jobs per day, and the top causes of job failure.
* Policies – information on active policies, such as the number of associated items, and the total cloud storage consumed by items backed up under a given policy.
* Optimize – potential cost optimization opportunities for your backups.
* Policy adherence – success of backups per day for every backup instance.

### Troubleshooting backups with Microsoft Azure Recovery Services (MARS)

Note

Microsoft documentation refers to both the backup agent and MARS interchangeably: both refer to the same service name (cbengine). In this module, it is referred to as Microsoft Azure Recovery Services (MARS).

Microsoft Azure Recovery Services is also known as the backup agent. This is the Azure service that is used to back up data. The MARS agent can run on:

* On\-premises Windows machines.
* Azure VMs running Windows. The MARS agent runs side by side with the Azure VM backup extension. The agent backs up specific files and folders on the VM.
* A Microsoft Azure Backup Server (MABS) or a System Center Data Protection Manager (DPM) server.

Use the MARS agent to back up files, folders, and Windows machines either on\-premises or in the cloud. Data is backed up to an Azure Recovery Services Vault.

To troubleshoot with the MARS agent, first check basic issues, and then more advanced issues.

#### Step 1: Basic troubleshooting

Check that:

* You have network connectivity between the MARS backup agent and Azure.
* The MARS agent is running. You might need to restart it and ensure the MARS agent is ready.
* There is 5%\-10% free space in the scratch folder.
* Antivirus software or any other process is not interfering with the backup.
* Any warning messages have been reviewed.

#### Step 2: Troubleshoot versions and other steps

* For offline backups, ensure Azure PowerShell 3\.7\.0 is installed on both computers.
* The operating system and MARS agent are up\-to\-date.
* [Unsupported drives, and files with unsupported attributes, are excluded from backup](/en-us/azure/backup/backup-support-matrix-mars-agent).
* Are manual backups working, but scheduled backups are not?
* Are all relevant clocks set to the correct time zone?

### Troubleshoot backing up Azure VMs

When configuring backups for an Azure VM, follow best practice guidelines. If you encounter problems with backing up an Azure VM, try the following:

#### Step 1: Basic troubleshooting

* Is the Azure VM provisioning state ‘Running’? The backup will not run if it is in a Stopped/Deallocated/Updating state. You might see the error message: VM is not in a state that allows backups.
* Are there any pending operating system updates or does the VM need to reboot? Install system updates and reboot before retrying the backup.
* Does the Azure VM have internet connectivity?
* Is another backup service running? Two backup services cannot run at the same time. If you suspect another backup has not left a snapshot extension, [uninstall extensions](/en-us/azure/backup/backup-azure-troubleshoot-vm-backup-fails-snapshot-timeout) to force a reload, then try the backup again.
* Is antivirus software preventing the backup from running? If so, you might see the error message: antivirus configured in the VM is restricting the execution of backup extension. To resolve this issue, in the antivirus configuration, exclude the directories below:

C:\\Packages\\Plugins\\Microsoft.Azure.RecoveryServices.VMSnapshot

C:\\WindowsAzure\\Logs\\Plugins\\Microsoft.Azure.RecoveryServices.VMSnapshot

#### Step 2: Check the Azure VM Guest Agent

* Is the Azure VM Guest Agent service installed and started? Go to services.msc to check it is running then try rebooting the VM.
* Is the Microsoft Azure VM Guest Agent the latest version?

#### Step 3: Check Azure VM extension health

* Are all Azure VM extensions in the ‘provisioning succeeded’ state? From the Azure portal, go to the VM, then Settings. From the Extensions menu, select Extensions status.
* Have all [extension issues](/en-us/azure/virtual-machines/extensions/overview) been resolved?

#### Step 4: Check the Azure backup agent

* Is the Windows or Linux VM operating system supported? Refer to the [IaaS VM Backup Support Matrix](/en-us/azure/backup/backup-support-matrix-iaas) for supported versions.
* Is the VM agent up\-to\-date? Azure VMs are backed up by installing a backup agent. Check that the backup agent is installed and it’s a recent version.
* Is the Azure Backup option grayed out? Hover over the grayed\-out option to find out the reason.
* Is antivirus software blocking the extension? If there are log entries in Event Viewer Application logs with the faulting application name IaaSBcdrExtension.exe then it could be the antivirus software.
* Are there entries in the Event Log? The Event Log may show backup failures from products other than Azure Backup. If Azure Backup is failing, find the corresponding error code in [Common Issues](/en-us/azure/backup/backup-azure-troubleshoot-vm-backup-fails-snapshot-timeout) to discover the solution.

For an up\-to\-date list of common error messages, see [Troubleshoot backup errors with Azure VMs \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-vms-troubleshoot).

### Troubleshoot Azure Backup Server issues

Microsoft Azure Backup Server (MABS), also known as Azure Backup Server, is the software used to back up a range of servers and workloads. For a complete list of what can be protected with MABS, see:

* [MABS (Azure Backup Server) V3 UR1 (and later) protection matrix](/en-us/azure/backup/backup-mabs-protection-matrix)
* [Azure Backup Server V3 RTM protection matrix](/en-us/azure/backup/microsoft-azure-backup-server-protection-v3)

MABS must be installed on a dedicated, single\-purpose server. The computer cannot be a domain controller, a node of a cluster, have Exchange Server running, have System Center Operations Manager running, or have the Application Server role installed. It must be a dedicated backup server.

Microsoft Azure Backup Server isn't supported on Windows Server Core or Microsoft Hyper\-V Server.

Microsoft Azure Backup Server must be part of a domain. You cannot move an existing MABS machine to a new domain after deployment.

Microsoft Azure Backup Server must be registered with a Recovery Services vault, whether backup data is stored locally or in Azure.

Run through the following questions to troubleshoot Azure Backup Server issues:

* Is there network connectivity between the MARS agent and the Azure server?
* Is the MARS service running? In the Service console, start or restart the service and try the backup again.
* Is the SQL Agent service running and set to automatic in the MABS server?
* Is the MARS agent up\-to\-date?
* Ensure no other process or antivirus software is interfering with Azure backup.
* If Push install fails, check if DPM agent is already present. If yes, then uninstall the agent and install it again.
* Ensure .NET Framework 4\.5\.2 or later is installed on the server.
* Ensure the server on which you're trying to install Azure Backup Server isn't already registered with another vault.
* Configure antivirus software for MABS server.
* Check where MABs is installed, and what else is installed on that server.
* Check the backup vault credentials.

### Troubleshoot scheduled backups

There are two types of policies for scheduled backups:

* Default backup policy – the default policy backs up the VM once a day, retaining the backups for 30 days.
* Custom policy – you define whether backups run daily or weekly, and specify how long to retain the backup.

If you have problems with scheduled backups, try the following:

* The VMs must be in the same region and subscription as the recovery vault.
* If you get a message saying the recovery point is crash\-consistent, check whether the VM is switched on. If the VM is not on, it will be backed up as an offline VM and the recovery point will be crash\-consistent. This means that Azure gives no guarantee about the consistency of the data on the storage medium.
* [Troubleshoot scheduled backup job failures \- Data Protection Manager \| Microsoft Learn](/en-us/troubleshoot/system-center/dpm/troubleshoot-scheduled-backup-job-failures)

---

## Troubleshoot recovery issues with Microsoft Azure

When you have created a backup, you may need to recover the data as part of a planned migration, or in case of data loss. In this unit, you will learn how to troubleshoot data recovery for different scenarios.

### Troubleshoot file recovery for an Azure VM backup

When you recover data from an Azure VM backup you have three options to restore the data:

* File Recovery
* Restore VM
* Disk restore. Only the disks are restored, which can then be used to create a new VM or replace a disk on an existing VM.

To recover files, select the **File Recovery** option. It is then a three\-step process to recover the files:

1. Select a recovery point. This is the date when your files were available.
2. Download a script. The script will mount the drives storing your files. The drives will remain mounted for 12 hours for you to restore the files you need.
3. Unmount the drives and close the connection.

The following sections provide troubleshooting information when common error messages appear:

#### Error message: Exception caught while connecting to target

This may appear if the script is unable to access the recovery point. To resolve this issue:

1. Check that the machine running the script has access to the recovery vault.
2. Verify the connection to the Azure target IP addresses. To check, run the following from an elevated command prompt:
nslookup download.microsoft.com
or
ping download.microsoft.com
3. Ensure access to iSCSI outbound port 3260\.
4. Check for a firewall or NSG blocking traffic to Azure target IPs or recovery service URLs.
5. Check that antivirus software isn't preventing the script from running.

Also check the following common error messages:

#### Error message: The target has already been logged in via an iSCSI session

This might be caused by the script already running on the same machine, and the drives are already attached. Browse the available volumes using File Explorer to find the mounted drives.

#### Error message: This script is invalid because the disks have been dismounted via portal/exceeded the 12\-hr limit. Download a new script from the portal

This message appears if you attempt to run the script more than 12 hours after you downloaded it. You need to download another script from the portal.

#### Error message: ExtensionSnapshotFailedCOM

The backup operation failed due to an issue with the Windows service COM\+ System application. To resolve this issue, follow these steps:

1. Try starting/restarting Windows service COM\+ System Application (from an elevated command prompt – net start COMSysApp).
2. Ensure Distributed Transaction Coordinator service is running as Network Service account. If not, change it to run as Network Service account and restart COM\+ System Application.
3. If unable to restart the service, then reinstall Distributed Transaction Coordinator service by following the steps below:
4. Stop the MSDTC service
5. Open a command prompt (cmd)
6. Run the command msdtc \-uninstall
7. Run the command msdtc \-install
8. Start the MSDTC service
9. Start the Windows service COM\+ System Application. After the COM\+ System Application starts, trigger a backup job from the Azure portal.

For an up\-to\-date list of common error messages and recommended action, see [Troubleshoot Azure VM file recovery \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-vm-file-recovery-troubleshoot).

### Troubleshoot restoring using Microsoft Azure Recovery Services (MARS) backup agent

To restore data that has been backed up using Microsoft Azure Recovery Services (MARS):

1. From the MARS agent home screen, select Recover Data. The Recover Data Wizard is displayed.
2. Specify where you want to restore the data.
3. Select the data to restore, and the date and time it was backed up. These selections determine the data recovery point.
4. Select Mount to mount the disk containing the recovery point then select the location where you want to recover the data.
5. Confirm your selections before starting the data recovery.

When you installed the MARS agent, an encryption passphrase was generated. This is stored in a text file and should be kept somewhere safe. If the passphrase is lost, you cannot recover any data backed up by the MARS backup agent.

When the MARS agent is configured, you specify how long the backup data should be retained. Data will not be kept after this period of time.

### Troubleshoot restore issues when using Azure backup agent

When you recover an Azure Virtual Machine from a backup, a process server is used to handle the data. If you encounter problems with restoring data, use a step\-by\-step methodology:

#### Step 1: Monitor process server health

It is good practice to proactively monitor the process server when restoring data. This allows you to monitor alerts, and handle issues as they occur.

The following graphic summarizes the steps to troubleshoot a backup recovery:

1. Are all services running?
2. Is the CPU state OK?
3. Is the memory state OK?
4. Is cache free space OK?
5. Does the process server have a heartbeat?
6. Troubleshoot connection/replication issues.

### Troubleshoot restore issues from Microsoft Azure Backup Server (MABS)

Azure Backup Server is designed to back up and restore workloads such as Hyper\-V VMs, Microsoft SQL Server, SharePoint Server, Microsoft Exchange, and Windows clients.

If you have problems restoring from MABS, try the following troubleshooting checklist:

#### Check the installation folder

The default installation folders for DPM are as follows:

C:\\Program Files\\Microsoft Azure Backup Server\\DPM\\DPM

You can also run the following command to find the install folder path:

Reg query "HKLM\\SOFTWARE\\Microsoft\\Microsoft Data Protection Manager\\Setup"

#### Invalid vault credentials

When you register to a vault, if you get an error message saying invalid vault credentials have been provided, either you have a corrupt file, or you provided incorrect credentials. Try the following:

1. Download the latest credentials file from the vault and try again.
2. Try downloading the credentials to a different local directory or create a new vault.
3. Try updating the date and time settings as described in [this article](/en-us/azure/backup/backup-azure-mars-troubleshoot).
4. Check to see if c:\\windows\\temp has more than 65000 files. Move stale files to another location or delete the items in the Temp folder.
5. Check the status of certificates.
6. In Control Panel, open **Manage Computer Certificates**.
7. Expand the **Personal** node and its child node **Certificates**.
8. Remove the certificate **Windows Azure Tools**.
9. Retry the registration in the Azure Backup client.
10. Check to see if a group policy is in place.

#### Replica is inconsistent

In the Protection Group Wizard, verify that the automatic consistency check option is turned on.

In the case of System State/BMR backup, verify that Windows Server Backup is installed on the protected server.

* Check for space\-related issues in the DPM storage pool on the DPM/Microsoft Azure Backup Server and allocate storage as required.
* Check the state of the Volume Shadow Copy Service on the protected server. If it's in a disabled state, set it to start manually. Start the service on the server then go back to the DPM/Microsoft Azure Backup Server console, and start the sync with the consistency check job.

#### Online recovery point creation failed

If you get an error message saying “the Windows Azure Backup Agent was unable to create a snapshot of the selected volume”, try increasing the available space in the recovery point volume.

If you get an error message saying “the Windows Azure Backup Agent cannot connect to the OBEngine service”, try verifying that the OBEngine exists in the list of running services on the computer. If the OBEngine service is not running, use the "net start OBEngine" command to start it.

If you get an error message saying that “the encryption passphrase for this server is not set. Please configure an encryption passphrase”, try configuring an encryption passphrase. If that fails, take the following steps:

1. Verify that the scratch location exists. This is the location that's mentioned in the registry **HKEY\_LOCAL\_MACHINE\\Software\\Microsoft\\Windows Azure Backup\\Config**, where the name **ScratchLocation** should exist.
2. If the scratch location exists, try re\-registering by using the old passphrase.

Note

When you configure an encryption passphrase, always save it in a secure location.

### Troubleshoot hybrid scenarios

#### Troubleshoot site recovery with Hyper\-V

When recovering an on\-premises Hyper\-V VM to Azure, use Azure Site Recovery. If you experience issues, use the following checklist to troubleshoot the problem:

* Do all your Hyper\-V hosts and VMs meet the requirements and prerequisites for recovery?
* Check the “Support for disaster recovery of on\-premises Hyper\-V VMs to Azure” link at the end of this module.
* If Hyper\-V hosts are managed by Virtual Machine Manager (VMM), the VMM server must have at least one cloud and one or more host groups. The Hyper\-V hosts running the VMs should be in the cloud with network mapping between on\-premises VMM VM networks, and Azure virtual networks. See links in the Summary of this module.
* Check the log located in **Applications and Services Logs** \> **Microsoft** \> **Windows**.
* On the guest VM, verify that WMI is enabled and accessible.

	+ [Troubleshoot](/en-us/windows/win32/wmisdk/wmi-troubleshooting) WMI.
	+ [Troubleshoot](/en-us/previous-versions/tn-archive/ff406382(v=msdn.10)) problems with WMI scripts and services.
* On the guest VM, ensure that you have the latest version of Integration Services and it is running. Microsoft recommends keeping integration services up\-to\-date.

Also, check common error messages:

#### Cannot enable protection as the virtual machine is not highly available

Try restarting the VMM service on the VMM machine. If that doesn't work, try removing the virtual machine from the cluster and adding it again.

#### The VSS writer NTDS failed with status 11 and writer specific failure code 0x800423F4

To resolve this issue, upgrade to Windows Server R2 with 4072650 applied. Also, check that the Hyper\-V host has Windows 2016 or later installed.

#### Troubleshoot site recovery with VMware

Before you restore a VMware VM, ensure it meets [Azure requirements](/en-us/azure/site-recovery/vmware-physical-azure-support-matrix).

Verify properties as follows:

1. In **Protected Items**, select **Replicated Items**, and then select the VM you want to verify.
2. In the **Replicated item** pane, there's a summary of VM information, health status, and the latest available recovery points. Select **Properties**.
3. In **Compute and Network**, you can modify these properties as needed:

	* Azure name
	* Resource group
	* Target size
	* [Availability set](/en-us/azure/virtual-machines/windows/tutorial-availability-sets)
	* Managed disk settings
4. You can view and modify network settings, including:

	* The network and subnet in which the Azure VM will be located after failover.
	* The IP address that will be assigned to it.
5. In **Disks**, review operating system information, and data disks on the VM.

To run a failover to Azure, in **Settings**, select **Replicated items**, select the VM to fail over, and then select **Failover**.

In **Failover**, select a **Recovery Point** to fail over to. You can use one of the following options:

* **Latest**: This option first processes all the data sent to Site Recovery. It provides the lowest Recovery Point Objective (RPO) because the Azure VM that's created after failover has all the data that was replicated to Site Recovery when the failover was triggered.
* **Latest processed**: This option fails the VM over to the latest recovery point processed by Site Recovery. This option provides a low RTO (Recovery Time Objective) because no time is spent processing unprocessed data.
* **Latest app\-consistent**: This option fails the VM over to the latest app\-consistent recovery point processed by Site Recovery.
* **Custom**: This option lets you specify a recovery point.

You then select **Shut down machine before beginning failover** to attempt to shut down source VMs before triggering the failover. Failover continues even if the shutdown fails. You can follow the failover progress on the Jobs page.

In some scenarios, failover requires additional processing that takes around 8 to 10 minutes to complete. You might notice longer test failover times for:

* VMware VMs running a Mobility service version older than 9\.8\.
* Physical servers.
* VMware Linux VMs.
* Hyper\-V VMs protected as physical servers.
* VMware VMs that don't have the DHCP service enabled.
* VMware VMs that don't have the following boot drivers: storvsc, vmbus, storflt, intelide, atapi.

Note

Don't cancel a failover in progress. If you cancel a failover in progress, the VM won't replicate again.

If you have problems, try the following troubleshooting steps:

1. Monitor process server health. In the Azure portal, monitor the process servers to verify they are connected and working.
2. Check connectivity between the source server and the process server, and between the process server and Azure.
3. Check that the source machine is available for replication, specifically:

	* Check that two VMs don't have the same UUID. Refer to [Azure Site Recovery VMware\-to\-Azure: How to clean up duplicate or stale entries](https://social.technet.microsoft.com/wiki/contents/articles/32026.asr-vmware-to-azure-how-to-cleanup-duplicatestale-entries.aspx).
4. Ensure the **vCenter credentials** are correct when you set up the configuration server, by using the OVF template or unified setup. To verify the credentials, see [Modify credentials for automatic discovery](/en-us/azure/site-recovery/vmware-azure-manage-configuration-server#modify-credentials-for-automatic-discovery).
5. If insufficient permissions are provided to access vCenter, failure to discover virtual machines might occur. Ensure that the permissions described in [Prepare an account for automatic discovery](/en-us/azure/site-recovery/vmware-azure-tutorial-prepare-on-premises) are added to the vCenter user account.
6. Management servers cannot be replicated. If the VM is used as one or more of the following roles—Configuration server / scale\-out process server / Master target server—then you will not be able to choose the virtual machine from the portal.
7. If the virtual machine is already protected or failed over through Site Recovery, it will not be available to select for protection in the portal. Ensure that the virtual machine isn't already protected by any other user, or under a different subscription.
8. Check if vCenter is in connected state. To verify, go to **Recovery Services vault** \> **Site Recovery Infrastructure** \> **Configuration Servers** \> **Click on respective configuration server**. A pane opens on the right with details of associ/rvers. Check if vCenter is connected. If it's in a "Not Connected" state, resolve the issue and then refresh the configuration server on the portal. After this, virtual machine will be listed on the portal.
9. If the ESXi host under which the VM resides is in powered off state, then virtual machine will not be listed or will not be selectable on the Azure portal. Power on the ESXi host, and refresh the configuration server on the portal. After this, virtual machine will be listed on the portal.
10. If there is a pending reboot, you will not be able to select the VM on the Azure portal. Complete the pending reboot and refresh the configuration server. They should then be listed on the portal.
11. If the virtual machine doesn't have a valid IP address associated with it, you will not be able to select the machine on the Azure portal. Assign a valid IP address to the virtual machine, and refresh the configuration server. This could also be caused by the machine not having a valid IP address associated with one of its NICs. Either assign a valid IP address to all NICs or remove the NIC that's missing the IP.

#### Troubleshoot site recovery with SCCM

A System Center Configuration Manager (SCCM) site recovery is needed if a site fails, or you lose data in the site database. Site recovery includes repairing and resynchronizing the data.

If you experience problems, try the following troubleshooting issues:

1. Check that previous configurations are not on the site server, as this can cause conflicts. Remove previous configurations before restoring Configuration Manager by using one of the following methods:

	* Restoring to a new server.
	* Formatting the disks and reinstalling the operating system.
	* Cleaning an existing server, including deleting registry entries starting with SMS from HKLM\\System\\CurrentControlSet\\Services.
2. For site database recovery only before restoring Configuration Manager:

	* Back up the site database, including supporting databases such as WSUS.
	* Note the SQL Server name and instance name.
	* Delete the site database from the SQL Server.
	* Restart the SQL Server.
3. Clean an existing server for full recovery before restoring Configuration Manager:

	* Back up the site database, including supporting databases such as WSUS.
	* Make a copy of the content library.
	* Uninstall the Configuration Manager site.
	* Manually delete the site database from the SQL Server.
	* Manually delete the Configuration Manager installation folder, and any other Configuration Manager folders.
	* Restart the server.
	* Restore the content library and other databases like WSUS.
4. Use a supported version and the same edition of SQL Server:

	* Check that the version of SQL Server is both supported, and the same edition as the original. Restoring to a newer version of SQL Server is supported, providing you don't change the edition—you can restore Standard to Standard and Enterprise to Enterprise.
	* Ensure SQL Server is not set to **single\-user mode**.
	* Make sure the MDF and LDF files are valid. When you recover a site, there's no check for the state of the files.
5. SQL Server Always On availability groups:/

	* If you use SQL Server Always On availability groups to host the site database, modify your recovery plans as described in [Prepare to use SQL Server Always On](/en-us/mem/configmgr/core/servers/deploy/configure/sql-server-alwayson-for-a-highly-available-site-database).
6. Database replicas:

	* After you restore a site database that you configured for database replicas, reconfigure each replica. Before you can use the database replicas, recreate both the publications and subscriptions.

### Troubleshoot site\-to\-site recovery

Azure to Azure Site Recovery allows you to replicate Azure virtual machines (VMs) from one region to another. In case of problems, check the following:

#### High data change rate on the source virtual machine

Azure Site Recovery creates an event if the data change rate on the source virtual machine is higher than the supported limits. Go to **Replicated items** \> **VM** \> **Events** \- **last 72 hours**. You should see the event **Data change rate beyond supported limits**:

Select the event to display disk information:

#### Azure Site Recovery limits

Azure Site Recovery limits are data churn per disk and data churn per virtual machine. The actual limits vary according to specific configurations. For example, a single VM Site Recovery can handle 5MB/s of churn per disk and a maximum of five disks. Site Recovery has a limit of 54MB/s of total churn per VM.

To find out whether this is a recurring problem, check the data change rate of the relevant virtual machine under **Monitoring**. You will need to add the metrics shown in the following screenshot:

#### Network connectivity problems

Site Recovery sends replicated data to the cache storage account. You might experience network errors if uploading the data from a virtual machine to the cache storage account is slower than 4MB in three seconds.

To check for latency problems, use the command\-line utility [AzCopy](/en-us/azure/storage/common/storage-use-azcopy-v10). This uploads data from the virtual machine to the cache storage account. If the latency is high, check whether you're using a network virtual appliance (NVA) to control outbound network traffic from VMs. The appliance might get throttled if all the replication traffic passes through the NVA.

Microsoft recommends creating a network service endpoint in your virtual network for "Storage" so that the replication traffic doesn't go to the NVA.

#### Network connectivity

Site Recovery needs the VM to provide outbound connectivity to specific URLs or IP ranges. You might have your VM behind a firewall or use network security group (NSG) rules to/l outbound connectivity. If so, you might experience issues. Make sure all the URLs are connected. For more information, see [Outbound connectivity for URLs](/en-us/azure/site-recovery/azure-to-azure-about-networking).

For an up\-to\-date list of common issues, see: [Troubleshoot replication of Azure VMs with Azure Site Recovery \- Azure Site Recovery \| Microsoft Learn](/en-us/azure/site-recovery/azure-to-azure-troubleshoot-replication).

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary

In this module, you have learned how to troubleshoot common backup and restore issues when working in Azure.

Now that you have completed this module, you'll be able to:

* Review the status of a backup job, manage alerts, and review logs.
* Troubleshoot backing up and restoring a virtual machine (VM).
* Troubleshoot Microsoft Azure Recovery Services backups.
* Troubleshoot backing up and restoring servers.
* Troubleshoot Azure to Azure Site Recovery.
* Troubleshoot site recovery with Hyper\-V, SCCM, and VMware.

### Resources

Use these resources to discover more.

* [Support matrix for Backup center](/en-us/azure/backup/backup-center-support-matrix)
* [Monitor and operate backups using Backup Center \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-center-monitor-operate)
* [Monitoring and reporting solutions for Azure Backup \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/monitoring-and-alerts-overview)
* [Monitor Azure Backup with Azure Monitor \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-monitoring-use-azuremonitor)
* [Monitor Azure Backup protected workloads \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-monitoring-built-in-monitor)
* [Configure Vault Diagnostics settings at scale \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/azure-policy-configure-diagnostics)
* [Monitoring Azure Backup workloads](/en-us/azure/backup/backup-azure-monitoring-built-in-monitor)
* [Alert processing rules for Azure Monitor alerts \- Azure Monitor \| Microsoft Learn](/en-us/azure/azure-monitor/alerts/alerts-action-rules?tabs=portal)
* [Troubleshoot Azure Backup Server \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-mabs-troubleshoot)
* [Troubleshoot Agent and extension issues \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-troubleshoot-vm-backup-fails-snapshot-timeout)
* [Troubleshoot the Azure Backup agent \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-mars-troubleshoot)
* [Troubleshoot Hyper\-V disaster recovery with Azure Site Recovery \- Azure Site Recovery \| Microsoft Learn](/en-us/azure/site-recovery/hyper-v-azure-troubleshoot)
* [Troubleshoot replication of Azure VMs with Azure Site Recovery \- Azure Site Recovery \| Microsoft Learn](/en-us/azure/site-recovery/azure-to-azure-troubleshoot-replication)
* [Troubleshoot replication issues for disaster recovery of VMware VMs and physical servers to Azure by using Azure Site Recovery \- Azure Site Recovery \| Microsoft Learn](/en-us/azure/site-recovery/vmware-azure-troubleshoot-replication)
* [Troubleshoot Azure VM file recovery \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-vm-file-recovery-troubleshoot)
* [Troubleshoot backup errors with Azure VMs \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-vms-troubleshoot)
* [Troubleshoot slow backup of files and folders \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-troubleshoot-slow-backup-performance-issue)
* [Site recovery \- Configuration Manager \| Microsoft Learn](/en-us/mem/configmgr/core/servers/manage/recover-sites)
* [Prepare to use an availability group \- Configuration Manager \| Microsoft Learn](/en-us/mem/configmgr/core/servers/deploy/configure/sql-server-alwayson-for-a-highly-available-site-database)
* [Support matrix for Azure VM backup \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-support-matrix-iaas)
* [Azure Backup Server V3 RTM protection matrix](/en-us/azure/backup/microsoft-azure-backup-server-protection-v3)
* [MABS (Azure Backup Server) V3 UR1 (and later) protection matrix](/en-us/azure/backup/backup-mabs-protection-matrix)
* [About Azure Site Recovery \- Azure Site Recovery \| Microsoft Learn](/en-us/azure/site-recovery/site-recovery-overview)
* [About Azure VM backup \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-vms-introduction)
* [Microsoft Azure Recovery Services (MARS) Agent – FAQ \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-file-folder-backup-faq)
* [Set up VMware VM disaster recovery to Azure with Azure Site Recovery \- Classic \- Azure Site Recovery \| Microsoft Learn](/en-us/azure/site-recovery/vmware-azure-tutorial)
* [Support for disaster recovery of Hyper\-V VMs to Azure with Azure Site Recovery \- Azure Site Recovery \| Microsoft Learn](/en-us/azure/site-recovery/hyper-v-azure-support-matrix)
* [Prepare for disaster recovery of Hyper\-V VMs to Azure with Azure Site Recovery \- Azure Site Recovery \| Microsoft Learn](/en-us/azure/site-recovery/hyper-v-prepare-on-premises-tutorial)
* [Network virtual appliance configuration](/en-us/azure/site-recovery/azure-to-azure-about-networking).
* [Back up Azure VMs in a Recovery Services vault \- Azure Backup \| Microsoft Learn](/en-us/azure/backup/backup-azure-arm-vms-prepare)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/business-continuity/_

## Fuentes
- [Troubleshoot business continuity with Microsoft Azure](https://learn.microsoft.com/en-us/training/modules/business-continuity/?WT.mc_id=api_CatalogApi)
