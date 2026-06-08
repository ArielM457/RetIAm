# Prepare on-premises workloads for migration to Azure

> Curso: Migrate application workloads and data to Azure (wwl-migrate-application-workloads-data-azure) · Seccion: Migrate application workloads and data to Azure
> Duracion estimada: 35 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Migrate service can help you discover, assess, and migrate resources successfully to Azure.

You’re the solution architect for a manufacturing company that currently hosts its IT operations through a managed service provider. The datacenter lease is rapidly approaching expiration and the company’s executive management has decided not to renew the datacenter lease, and instead migrate their services to Azure. By moving to the cloud, the company will now pay only for resources they use, and the migration will pave the way for modernization of their apps and services. You have been asked to undertake the migration effort, but first you must prepare your on\-premises workloads and the tools you intend using to migrate to Azure.

Choosing the appropriate migration strategy for your business need is essential. You'll learn about the differences between Azure Migrate and Azure Site Recovery, which can also be used to migrate virtual machines to Azure. You’ll learn about agentless and agent\-based migration of virtual machines and when to use one over the other.

Finally, you’ll review procedures and guidelines for preparing Azure and your on\-premises environment before you can migrate your workloads.

#### Learning objectives

In this module, you’ll learn how to:

* Choose the appropriate migration tool to solve your business problem
* Prepare Azure for the Azure Migrate deployment
* Prepare the on\-premises environment for agentless server migration
* Deploy the Azure Migrate appliance to use with the Azure Migrate Server Migration tool

#### Prerequisites

* Knowledge of cloud and traditional architecture concepts
* Knowledge of networking, compute, and database systems
* Familiarity with virtualization concepts like VMs, virtual networks, and virtual hard disks
* Ability to manage cloud identities with Microsoft Entra ID

---

## Choose your migration approach

In an earlier phase of the project, you performed a full discovery and assessment of your current environment. You identified the inventory of servers and services that are in scope for the migration and the dependencies between them. You have received guidance and support from the IT and business teams working with the individual services and your leadership team has approved the migration.

Your first task is to confirm the migration approach and tools that will meet your company’s business goal to rehost their existing infrastructure in Azure.

In this unit, you’ll compare Azure Migrate and Azure Site Recovery as options for migrating server workloads to Azure. You’ll also review agentless and agent\-based migration options and pick the appropriate approach for your business scenario.

### Identify migration tools and services

Several tools and services are available in Azure to help you migrate your resources to Azure. Many of these tools are consolidated in the Azure Migrate service which acts as a hub for migration tools, letting you centralize the different migration tasks in one place.

The choice of tool depends on the type of workload you plan to migrate. For database workloads, a tool like Azure Database Migration Service (Azure DMS) helps you manage the whole process of moving database workloads to Azure.

#### Plan a migration pilot

As part of your strategy, you plan to run an initial pilot by migrating a subset of the company’s corporate applications that are not considered business\-critical. These applications currently run in the datacenter as Windows Server and Linux workloads hosted on Hyper\-V. Subsequent phases of the migration will include workloads running on VMware.

In this unit, you’ll learn how Azure Migrate can help you accomplish the pilot migration. You could also use Azure Site Recovery to move VMs from on\-premises to Azure. By comparing both options, you’ll understand which approach better meets your business scenario.

### Azure Migrate

Azure Migrate provides an integrated hub of tools to assess and migrate on\-premises infrastructure, applications, and data to Azure. Assume you have already used Azure Migrate to assess your environment. You can perform the migration using the Azure Migrate: Server Migration tool from the same Azure Migrate project. Within Azure Migrate there are native assessment and migration tools, available at no additional cost.

In this module, you'll focus on using the tools to assess and migrate workloads.

#### ISV tools

No single migration scenario is identical. Some migration projects can present unique challenges that require an extended migration solution apart from Azure’s native tools. Azure Migrate integrates with other Azure services, tools and independent software vendor (ISV) offerings through the same single unified portal interface. ISV offerings provide alternative options if your organization has specific challenges in a migration project, and you can access those options directly from Azure Migrate.

### Migration or disaster recovery

While, you could also use Azure Site Recovery to migrate your workloads into Azure, Azure Migrate is designed and optimized for migration. The Azure Migrate hub centralizes all the tools and support required for different workloads, including physical and virtual servers, databases, and applications.

Azure Migrate lets you discover your resources and provides an assessment report that includes monthly cost estimates (compute and storage), and Azure VM readiness and performance\-based right sizing.

#### Azure Site Recovery

Migrating your on\-premises and public cloud workloads to the cloud is a specific business decision. Azure Site Recovery was designed as a service to be used for disaster recovery for on\-premises and Azure VMs. It can replicate workloads automatically from a primary site to a secondary site if there’s an outage. By providing access to Azure as a secondary site, you can avoid the cost of building or leasing and maintaining another datacenter. VMs failover either from on\-premises to Azure or from one Azure region to another. However, if you use Azure Site Recovery to migrate workloads to Azure, you cannot failback as a migration is a one\-time operation.

Despite sharing some similarities in the data replication process, Azure Migrate and Azure Site Recovery serve different purposes. In this module, you’ll focus on using Azure Migrate to meet your company’s business need and migrate your workloads.

### Compare agentless versus agent\-based migration

When planning your migration, you’ll first decide between an agent\-based or agentless migration approach. An agent\-based approach involves installing a lightweight agent on each machine you want to replicate for migration. The agent coordinates replication data from each machine and prepares it to send to Azure. With agent\-based replication, you don’t need to power down systems during migration, ensuring a continuous operating cycle.

Agent\-based migration comes with a cost of managing and keeping agents up\-to\-date. Agentless migration provides a cheaper solution and avoids the management overhead. However, it requires systems to be offline during migration. Generally, if a system is business\-critical, you should use an agent\-based option. For non\-critical or remote systems, short offline periods present no great problem, and you can use agentless migration.

#### Migrate using agentless

As you consider your choice of migration tool, keep in mind the initial goal of the pilot to migrate Hyper\-V\-based VMs to Azure. The Azure Migrate Server Migration tool provides agentless replication for on\-premises Hyper\-V VMs, using a migration workflow that's optimized for Hyper\-V. You install a software agent only on Hyper\-V hosts or cluster nodes. You don’t need to install anything on individual Hyper\-V VMs.

The pilot requires you to migrate non\-critical workloads running on Hyper\-V to Azure. Therefore, you’ll use an agentless migration with Azure Migrate.

#### Assess VMware workloads

For subsequent phases of the migration, you’ll want to consider an agent\-based approach as a significant number of the company’s business\-critical workloads run on VMware.

Using an agent\-based option also lets you obtain details about how your VMware workloads are related to each other and the dependencies between VMs. The agents will collect that data and you can then use Azure’s dependency visualization feature to understand those dependencies. Your stakeholders want to ensure the success of the entire migration and agent\-based dependency visualization will give you a higher confidence level when you assess your more business\-critical workloads.

### Check your knowledge

---

## Prepare Azure for the Azure Migrate deployment

You’ve decided to use the Azure Migrate: Server Migration tool for the migration pilot. Your next task is to ensure that you meet all the prerequisites for the Azure Migrate deployment.
Before beginning the migration, you need to prepare Azure to interact with the on\-premises environment.

In this unit, you’ll review the Azure permissions needed for an Azure Migrate deployment. As you already created an Azure Migrate project for discovery and assessment, you’ll review and ensure you have met any prerequisites that Azure needs for the migration.

### Assign Azure permissions

You’ll need to set up permissions to:

* Create an Azure Migrate project
* Register the Azure Migrate appliance

Whether assessing your on\-premises environment or migrating your workloads, you create an Azure Migrate project. Your Azure account needs permissions to create the Azure Migrate project.

#### Verify permissions to create the project

In Azure portal, open the subscription and check that the account you plan to use for the Azure Migrate project has **Owner** or **Contributor** permissions.

The business unit that owns the subscription has already assigned you the Owner role, which is why you were able to create the project for the VM discovery and assessment phase.

#### What is the Azure Migrate appliance?

As part of the discovery and assessment phase, Azure Migrate: Server Assessment creates a single virtual machine, called a migration appliance, that runs in your on\-premises environment. The appliance collects data about your on\-premises Hyper\-V VMs that you plan to migrate and Azure Migrate uses that data to assess your environment.

When creating an Azure Migrate project, you enable the Azure Migrate: Server Assessment tool for machine discovery and assessment. To set up the appliance, you download a compressed Hyper\-V VHD file, which you then configure and register with the Azure Migrate project.

#### Appliance registration process

Registering the appliance enables it to push the metadata collected during discovery and assessment to the Azure Migrate project. To do this, Azure Migrate creates two Microsoft Entra apps during appliance registration.

* The first app communicates with Azure Migrate service endpoints.
* The second app is used by the appliance to create an Azure Key Vault, which stores Microsoft Entra app information and appliance configuration settings. (For VMware virtual machine migration, download an OVA file instead.)

When you register the appliance, these resource providers are registered with the subscription chosen in the appliance:

* Microsoft.OffAzure
* Microsoft.Migrate
* Microsoft.KeyVault

Registering a resource provider configures your subscription to work with the resource provider. Not only do you need **Owner** or **Contributor** role to create an Azure Migrate project, but also to configure and register the appliance.

#### Assign permissions to register the appliance

To register the appliance, the Azure account needs permissions for Azure Migrate to create the Microsoft Entra apps. A tenant/global administrator can assign the required permissions in either of two ways:

* Grant permissions to users in the tenant to create and register Microsoft Entra apps.
* Assign the Application Developer role (that has the permissions) to the account.

The apps need only enough access permission to create and register the AD apps, and don’t inherit permissions for any other actions on the subscription. You can revoke the permissions once discovery is set up.

Your global administrator has granted permissions by navigating in Microsoft Entra ID to **Microsoft Entra ID** \> **Users** \> **User Settings** and setting **App registrations** to **Yes**.

### Finalize setting up Azure prerequisites

Remember to review your assessment and analyze your on\-premises workloads. Consider network bandwidth, database performance, and storage capacity, and compare them to their Azure equivalents. Address any mismatches and ensure the migrated workloads will meet all the needs of your system. For example, if you need to dynamically scale your apps to meet changing requirements, you can use the built\-in Azure Autoscale feature.

In the next unit, you’ll focus on preparing your on\-premises environment for the migration pilot.

#### Set up an account for VM discovery

The small subset of applications you’ve selected to migrate to Azure for the pilot run on a single Hyper\-V host. You’ve purposefully constrained the scope of the pilot to learn as much as possible before deploying a fuller migration of your on\-premises estate.

When creating the assessment, Azure Migrate also needs permissions to discover on\-premises VMs. You set up a single account for the Hyper\-V host and VMs you want to include in the discovery. You can set the account up to be a domain or local user account with Administrator permissions on the host.

You can also choose to create a local user account without Administrator permissions that the Azure Migrate service uses to communicate with the Hyper\-V host. Instead, you would add the user account to the following groups:

* Remote Management Users
* Hyper\-V Administrators
* Performance Monitor Users

#### Allocate storage and networking resources

In the migration process, Azure Migrate creates only the VMs, their network interfaces, and their disks. So, before you can migrate your VMs, you must create all other required resources in advance.

First create a new Azure storage account that Azure Migrate: Server Migration uses to store virtual machine data during migration. For the migration pilot, you’ll create a general purpose storage account that uses locally\-redundant storage (LRS) replication.
You’ll also need to create a new Azure virtual network that your migrated virtual machines will use when they are migrated to Azure. You specify this network when you configure the migration in the Azure Migrate project.

Before you migrate, assign the Virtual Machine Contributor role to your Azure account so that you can:

* Create a VM in the selected resource group.
* Create a VM in the selected virtual network.
* Write to an Azure managed disk.

### Check your knowledge

---

## Deploy the Azure Migrate appliance

During the assessment phase you used the Azure Migrate Server Assessment tool to discover and assess VMs in your on\-premises Hyper\-V environment. As part of the process, Azure Migrate uses a lightweight Hyper\-V VM called the Azure Migrate appliance.

You don’t have to perform an assessment when you create an Azure Migrate project, however it is recommended you do so. Even if you choose to skip the assessment and proceed directly to migration, you must still download and set up the appliance.

In this unit, you’ll learn how to download, create, and configure the appliance VM. You’ll also learn how to register the appliance with the Azure Migrate project.

### Work with the Azure Migrate appliance

The Hyper\-V host should be running Windows Server 2012 R2 or later and should have sufficient space to allocate RAM, CPU, and storage. When deploying the Azure Migrate appliance, you’ll create a network switch that the appliance uses to communicate with the Hyper\-V host.

#### Download the migration appliance

When you first deploy an Azure Migrate project, you select the tools you’ll use to assess and migrate your on\-premises VMs. Azure Migrate: Server Assessment lets you discover and assess resources for either a VMware or Hyper\-V environment.

From the Azure Migrate project, you can download the appliance that you’ll set up and connect to Azure Migrate.

1. In the Azure Migrate: Server Assessment panel, select **Discover** to open the Discover machines blade.
2. In the **Are your machines virtualized?** dropdown list, select **Yes, with Hyper\-V**.

Azure Migrate presents the link for the VHD file with which you can create a new virtual machine on your Hyper\-V host server.

#### Confirm the ZIP file is secure

Before deploying the appliance VM, verify the zipped file is secure. Run the following PowerShell command:

`Get-FileHash -Path ./AzureMigrateAppliance_v2.19.11.12.zip -Algorithm SHA256`

The command generates a hash for the zipped VHD file. The hash should match these settings.

> | **Algorithm** | **Hash value** |
> | --- | --- |
> | MD5 | 29a7531f32bcf69f32d964fa5ae950bc |
> | SHA256 | 37b3f27bc44f475872e355f04fcb8f38606c84534c117d1609f2d12444569b31 |

#### Create the appliance VM

After verifying the zipped VHD file is secure, extract the zipped file. Using Hyper\-V Manager, import the VHD file. Specify a virtual network switch for the VM to use and create the Azure Migrate appliance VM.

Before starting the appliance, configure network subnets in your existing on\-premises environment so that the appliance can obtain the appropriate IP address. The appliance also connects to specific Azure URLs during discovery and assessment. Azure documentation lists the [URL](/en-us/azure/migrate/migrate-appliance#url-access) and [port access](/en-us/azure/migrate/migrate-support-matrix-hyper-v#port-access) requirements for the appliance VM. Review the list and make sure those are in place before deploying the appliance.

#### Configure the appliance VM

Next, configure the appliance VM and register it with the Azure Migrate project. When you set up the appliance for the first time, you’re ready for discovery and assessment. Deploying and setting up the appliance also prepares Azure Migrate for the migration phase.

In Hyper\-V Manager, connect to the appliance VM and when requested, provide a password for the built\-in administrator account. When the appliance VM is running, open a browser on a computer that can connect to the appliance.

Type the URL **https://appliancename\-or\-IPAddress:44368**. This opens the appliance web app, where you configure the appliance for use. You first verify and set up appliance prerequisites and then register the appliance with Azure Migrate.

Accept the license terms

The appliance web app steps through the process of configuring the appliance. Internet connectivity and computer time synchronization verification should pass automatically. Wait while the app installs latest Azure Migrate updates. You may be prompted for administrator credentials and to restart the management app.

When you’ve completed setting up the prerequisites, select **Continue** to proceed to appliance registration.

#### Register the appliance VM

Next, register the appliance with Azure Migrate.

Click **Login**. The appliance web app opens a separate browser tab where you enter the Azure subscription credentials. Return to the appliance web app tab and then:

1. Select the subscription in which the Azure Migrate project was created
2. Select the project
3. Specify a name for the appliance
4. Click **Register**.

From this point, the appliance web app steps through the remainder of the process to get discovery and assessment underway. You’ve already completed your assessment and are ready to begin the migration.

### Check your knowledge

---

## Summary

In this module, you learned about essential preparations for a migration to Azure. You saw how choice of tools and approach are key to accomplishing a successful migration.

You also learned about several requirements to be handled before you migrate your workloads. First, an Azure Migrate project needs the correct Microsoft Entra permissions. Second, you confirmed that the prerequisites for the on\-premises environment are in place. Last, the Azure Migrate appliance is used for agentless assessment and migration of Hyper VMs. You learned how to deploy the appliance.

### Learn more

To learn more about the tools and services available to help you migrate to Azure, see these articles:

* [Azure Migrate](/en-us/azure/migrate/migrate-services-overview)
* [Prepare Hyper\-V for assessment and migration](/en-us/azure/migrate/tutorial-prepare-hyper-v)
* [Assess Hyper\-V VMs for migration](/en-us/azure/migrate/tutorial-assess-hyper-v)

For information on the support settings and limitations for migrating Hyper\-V VMs, see these articles:

* [Hyper\-V hosts](/en-us/azure/migrate/migrate-support-matrix-hyper-v-migration#hyper-v-hosts)
* [Hyper\-V VMs](/en-us/azure/migrate/migrate-support-matrix-hyper-v-migration#hyper-v-vms)
* [Set up the appliance VM](/en-us/azure/migrate/tutorial-assess-hyper-v#set-up-the-appliance-vm)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/prepare-onpremises-workloads-migration-azure/_

## Fuentes
- [Prepare on-premises workloads for migration to Azure](https://learn.microsoft.com/en-us/training/modules/prepare-onpremises-workloads-migration-azure/?WT.mc_id=api_CatalogApi)
