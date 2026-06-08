# Plan and implement updates, backups, and disaster recovery

> Curso: Monitor and maintain an Azure Virtual Desktop infrastructure (wwl-monitor-maintain-azure-virtual-desktop-infrast) · Seccion: Monitor and maintain an Azure Virtual Desktop infrastructure
> Duracion estimada: 31 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Backup provides independent and isolated backups to guard against unintended destruction of the data on your VMs. Backups are stored in a Recovery Services vault with built\-in management of recovery points. Configuration and scaling are simple, backups are optimized, and you can easily restore as needed. You use Azure Site Recovery to manage virtual machine replication in other Azure locations.

This module aligns with the exam AZ\-140: Configuring and Operating Microsoft Azure Virtual Desktop.

### Learning objectives

After completing this module, you'll be able to:

* Plan for disaster recovery for Azure Virtual Desktop
* Design and implement a backup strategy for Azure Virtual Desktop
* Monitor costs by using Azure Cost Management

### Prerequisites

* Conceptual knowledge of Azure compute solutions.
* Working experience with virtual machines, containers, and app service.

---

## Disaster recovery for Azure Virtual Desktop

Many users now work remotely, so organizations require solutions with high availability, rapid deployment speed, and reduced costs. Users also need to have a remote work environment with guaranteed availability and resiliency that lets them access their resources even during disasters.

To prevent system outages or downtime, every system and component in your Azure Virtual Desktop deployment must be fault\-tolerant. Fault tolerance is when you have a duplicate configuration or system in another Azure region that takes over for the main configuration during an outage. This secondary configuration or system reduces the impact of a localized outage. There are many ways you can set up fault tolerance, but this unit focuses on the methods currently available in Azure for dealing with business continuity and disaster recovery (BCDR).

Responsibility for components that make up Azure Virtual Desktop are divided between those components that are Microsoft\-managed, and those components that are customer\-managed, or partner managed.

The following components are customer\-managed or partner\-managed:

* Session host virtual machines
* Profile management, usually with FSLogix
* Applications
* User data
* User identities

To learn about the Microsoft\-managed components and how they're designed to be resilient, see [Azure Virtual Desktop service architecture and resilience](/en-us/azure/virtual-desktop/service-architecture-resilience).

### Business continuity and disaster recovery basics

When you design a disaster recovery plan, you should keep the following three things in mind:

* High availability: distributed infrastructure so smaller, more localized outages don't interrupt your entire deployment. Designing with high availability in mind can minimize outage impact and avoid the need for a full disaster recovery.
* Business continuity: how an organization can keep operating during outages of any size.
* Disaster recovery: the process of getting back to operation after a full outage.

Azure Virtual Desktop doesn't have any native features for managing disaster recovery scenarios, but you can use many other Azure services for each scenario depending on your requirements, such as [Availability sets](/en-us/azure/virtual-machines/availability-set-overview), [availability zones](/en-us/azure/availability-zones/az-region), Azure Site Recovery, and [Azure Files data redundancy](/en-us/azure/storage/files/files-redundancy) options for user profiles and data.

You can also distribute session hosts across multiple [Azure regions](/en-us/azure/best-practices-availability-paired-regions) provides even more geographical distribution, which further reduces outage impact. All these and other Azure features provide a certain level of protection within Azure Virtual Desktop, and you should carefully consider them along with any cost implications.

The following table lists the technology areas you need to consider as part of your disaster recovery strategy and links to other Microsoft documentation that provides guidance for each area:

| **Technology area** | **Documentation link** |
| --- | --- |
| Active\-passive vs active\-active plans | [Active\-Active vs. Active\-Passive](/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr#active-active-vs-active-passive) |
| Session host resiliency | [Multiregion Business Continuity and Disaster Recovery](/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr) |
| Disaster recovery plans | [Multiregion Business Continuity and Disaster Recovery](/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr#architecture-diagrams) |
| Azure Site Recovery | [Failover and failback](/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr#failover-and-failback) |
| Network connectivity | [Multiregion Business Continuity and Disaster Recovery](/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr#prerequisites) |
| User profiles | [Design recommendations](/en-us/azure/cloud-adoption-framework/scenarios/azure-virtual-desktop/eslz-business-continuity-and-disaster-recovery#design-recommendations) |
| Files share storage | [Storage](/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr#storage) |
| Identity provider | [Identity](/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr#identity) |
| Backup | [Backup](/en-us/azure/architecture/example-scenario/azure-virtual-desktop/azure-virtual-desktop-multi-region-bcdr#backup) |

---

## Design and implement a backup strategy for Azure Virtual Desktop

This unit describes how the [Azure Backup service](/en-us/azure/backup/backup-overview) backs up Azure virtual machines (VMs).

Azure Backup provides independent and isolated backups to guard against unintended destruction of the data on your VMs. Backups are stored in a Recovery Services vault with built\-in management of recovery points. Configuration and scaling are simple, backups are optimized, and you can easily restore as needed.

As part of the backup process, a [snapshot is taken](/en-us/azure/backup/backup-azure-vms-introduction#snapshot-creation), and the data is transferred to the Recovery Services vault with no impact on production workloads. The snapshot provides different levels of consistency. You can opt for an agent\-based application\-consistent/file\-consistent backup or an agentless crash\-consistent backup in the backup policy.

### Backup process

Here's how Azure Backup completes a backup for Azure VMs:

1. For Azure VMs that are selected for backup, Azure Backup starts a backup job according to the backup schedule you specify.
2. If you have opted for application or file\-system consistent backups, the VM needs to have a backup extension installed to coordinate for the snapshot process. If you have opted for [crash\-consistent backups](/en-us/azure/backup/backup-azure-vms-agentless-multi-disk-crash-consistent-overview), no agents are required in the VMs.
3. During the first backup, a backup extension is installed on the VM if the VM is running.
4. For Windows VMs that are running, Azure Backup coordinates with Windows Volume Shadow Copy Service (VSS) to take an app\-consistent snapshot of the VM.

	* By default, Backup takes full VSS backups.
	* If Backup can't take an app\-consistent snapshot, then it takes a file\-consistent snapshot of the underlying storage (because no application writes occur while the VM is stopped).
5. For Linux VMs, Backup takes a file\-consistent backup. For app\-consistent snapshots, you need to manually customize pre/post scripts.
6. For Windows VMs, Microsoft Visual C\+\+ 2013 Redistributable (x64\) version 12\.0\.40660 is installed, the startup of Volume Shadow Copy Service (VSS) is changed to *automatic*, and a Windows Service IaaSVmProvider is added.
7. After Backup takes the snapshot, it transfers the data to the vault.

	* The backup is optimized by backing up each VM disk in parallel.
	* For each disk that's being backed up, Azure Backup reads the blocks on the disk and identifies and transfers only the data blocks that changed (the delta) since the previous backup.
	* Snapshot data might not be immediately copied to the vault. It might take some hours at peak times. Total backup time for a VM will be less than 24 hours for daily backup policies.

### Encryption of Azure VM backups

When you back up Azure VMs with Azure Backup, VMs are encrypted at rest with Storage Service Encryption (SSE). Azure Backup can also back up Azure VMs that are encrypted by using Azure Disk Encryption.

| **Encryption** | **Details** | **Support** |
| --- | --- | --- |
| SSE | With SSE, Azure Storage provides encryption at rest by automatically encrypting data before storing it. Azure Storage also decrypts data before retrieving it. Azure Backup supports backups of VMs with two types of Storage Service Encryption: SSE with platform\-managed keys: This encryption is by default for all disks in your VMs. SSE with customer\-managed keys. With CMK, you manage the keys used to encrypt the disks. | Azure Backup uses SSE for at\-rest encryption of Azure VMs. |
| Azure Disk Encryption | Azure Disk Encryption encrypts both OS and data disks for Azure VMs.Azure Disk Encryption integrates with BitLocker encryption keys (BEKs), which are safeguarded in a key vault as secrets. Azure Disk Encryption also integrates with Azure Key Vault key encryption keys (KEKs). | Azure Backup supports backup of managed and unmanaged Azure VMs encrypted with BEKs only, or with BEKs together with KEKs.Both BEKs and KEKs are backed up and encrypted.Because KEKs and BEKs are backed up, users with the necessary permissions can restore keys and secrets back to the key vault if needed. These users can also recover the encrypted VM.Encrypted keys and secrets can't be read by unauthorized users or by Azure. |

For managed and unmanaged Azure VMs, Backup supports both VMs encrypted with BEKs only or VMs encrypted with BEKs together with KEKs.

The backed\-up BEKs (secrets) and KEKs (keys) are encrypted. They can be read and used only when they're restored back to the key vault by authorized users. Neither unauthorized users, or Azure, can read or use backed\-up keys or secrets.

BEKs are also backed up. So, if the BEKs are lost, authorized users can restore the BEKs to the key vault and recover the encrypted VMs. Only users with the necessary level of permissions can back up and restore encrypted VMs or keys and secrets.

### Snapshot creation

Azure Backup takes snapshots according to the backup schedule.

If you have opted for application or file\-system\-consistent backups, the VM needs to have a backup extension installed to coordinate for the snapshot process.

Windows VMs: For Windows VMs, the Backup service coordinates with VSS to take an app\-consistent snapshot of the VM disks. By default, Azure Backup takes a full VSS backup (it truncates the logs of application such as SQL Server at the time of backup to get application level consistent backup). If you're using a SQL Server database on Azure VM backup, then you can modify the setting to take a VSS Copy backup (to preserve logs).

---

## Monitor costs by using Azure Cost Management

Cost Management users often want answers to questions that many others ask. This unit walks you through getting results for common cost analysis tasks in Cost Management.

### View forecast costs

Forecast costs are shown in cost analysis areas for area and stacked column views. The forecast is based on your historical resource use. Changes to your resource use affect forecast costs.

In the Azure portal, navigate to cost analysis for your scope. For example: C**ost Management \+ Billing \> Cost Management \> Cost analysis.**

In the default view, the top chart has the Actual/Amortized cost and forecast cost sections. The solid color of the chart shows your Actual/Amortized cost. The shaded color shows the forecast cost.

### View forecast costs grouped by service

The default view doesn't show forecast costs group by a service, so you have to add a group by selection.

The view shows your costs grouped for each service. The forecast cost isn't calculated for each service. It's projected for the Total of all your services.

### View forecast costs for a service

You can view forecast costs narrowed to a single service. For example, you might want to see forecast costs for virtual machines.

1. In the Azure portal, navigate to cost analysis for your scope.
2. Select **Add filter** and then select **Service** name.
3. In the choose list, select a service. For example select, virtual machines.

Review the actual cost for selection and the forecast cost.

You can add more customizations to the view.

1. Add a second filter for **Meter** and select a value to filter for an individual type of meter under your selected service name.
2. Group by **Resource** to see the specific resources that are accruing cost. The forecast cost isn't calculated for each service. It's projected for the Total of all your resources.

### View cost breakdown by Azure service

Viewing costs by an Azure service can help you to better understand the parts of your infrastructure that cost the most. For example, VM compute costs might be small. Yet you might accrue significant networking costs because of the amount of information emitting from the VMs. Understanding the primary cost drivers of your Azure services is essential so that you can adjust service usage, as needed.

1. In the Azure portal, navigate to cost analysis for your scope.
2. Select **Cost** by service and then group by **Service tier**.
3. Change the view to **Table**.

---

## Module assessment

Choose the best response for each question.

### Check your knowledge

---

## Summary

In this module, you learned how to:

* Plan for disaster recovery for Azure Virtual Desktop
* Design and implement a backup strategy for Azure Virtual Desktop
* Monitor costs by using Azure Cost Management

### Learn more

* [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) \| [Azure free account FAQ](https://azure.microsoft.com/pricing/purchase-options/azure-account#FAQ?cid=msft_learn)
* [Free account for Students](https://azure.microsoft.com/free/students/?cid=msft_learn) \| [Azure for students FAQ](/en-us/azure/education-hub/azure-dev-tools-teaching/program-faq#azure-for-students/?azure-portal=true)
* [Create an Azure account](/en-us/learn/modules/create-an-azure-account/?azure-portal=true) module on Learn.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/plan-implement-business-continuity-disaster-recovery/_

## Fuentes
- [Plan and implement updates, backups, and disaster recovery](https://learn.microsoft.com/en-us/training/modules/plan-implement-business-continuity-disaster-recovery/?WT.mc_id=api_CatalogApi)
