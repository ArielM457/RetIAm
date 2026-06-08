# Migrate on-premises workloads to Azure

> Curso: Migrate application workloads and data to Azure (wwl-migrate-application-workloads-data-azure) · Seccion: Migrate application workloads and data to Azure
> Duracion estimada: 31 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You’re the solution architect for a manufacturing company that currently hosts its IT operations through a managed service provider. The company has recently decided to migrate their on\-premises operations to Azure and has completed the planning and assessment of their on\-premises environment, in which a mix of virtualized Windows and Linux workloads currently runs.

As a result of the planning phase, you’ve decided to use Azure Migrate to migrate your on\-premises workloads to Azure. You now plan to run a pilot to migrate an initial subset of the workloads in your environment.

You’ve set up an Azure Migrate project, confirmed that prerequisites are in place, and are ready to complete the migration. You’ll ensure that each VM is successfully migrated to Azure with no data loss and that the migrated workloads have adequate security controls in place.

In this module, you’ll learn how to use Azure Migrate to:

* Configure replication of VMs in Azure Migrate
* Monitor and test the migration
* Migrate VMs to Azure

### Learning objectives

In this module, you’ll learn how to:

* Set up the migration target environment
* Prepare virtualized on\-premises workloads for migration
* Monitor and test a failover of workloads for successful migration
* Complete the migration
* Implement security controls for migrated workloads

### Prerequisites

* Knowledge of cloud and traditional architecture concepts
* Knowledge of networking, compute, and database systems
* Familiarity with virtualization concepts like VMs, virtual networks, and virtual hard disks
* Ability to manage cloud identities with Microsoft Entra ID

---

## Enable Hyper\-V host servers for replication

You’re ready to migrate your on\-premises workloads to Azure. If you haven’t yet added the Azure Migrate Server Migration tool to the Azure Migrate project, you can do so now. The tool supports agentless migration of Windows and Linux VMs, which is appropriate as agentless migration is a requirement for your migration pilot.

Azure Migrate: Server Migration runs a lightweight Hyper\-V VM appliance that discovers VMs and sends VM metadata and performance information to the tool. You’ve already set up the appliance during the discovery and assessment phase.

The Azure Migrate Server Migration service uses Azure Site Recovery as the underlying migration engine.

In this unit, you’ll look at how to deploy the Azure Site Recovery Provider on your Hyper\-V host.

### Hyper\-V replication components

Before migrating your VMs, you’ll set up your Hyper\-V host with the components it needs to manage replication of your VMs and data. With agentless migration, you install components on the Hyper\-V host only. You don’t need to install anything on the Hyper\-V VMs.

The Microsoft Azure Site Recovery provider orchestrates replication for Hyper\-V VMs. The provider also installs the Microsoft Azure Recovery Service agent which handles data replication. Data is uploaded to a storage account that you created as part of preparing your on\-premises workloads for migration.

You use a single setup file downloaded from the Server Migration tool in the portal to install both components on the Hyper\-V host.

The provider and agent communicate securely with Azure Migrate Server Migration across outbound HTTPS port 443\. All communication is encrypted.

#### Prepare the Hyper\-V host server

In this task, you will register your Hyper\-V host with the Azure Migrate: Server Migration service. As part of the registration process, you will deploy the Azure Site Recovery Provider on your Hyper\-V host.

The Azure portal guides you through creating the resources that the Hyper\-V host needs to replicate your VMs to Azure. From the Discover machines pane in Azure Migrate Server Migration, Set the target Azure region for the migration. You’ll use this region for subsequent migrations in the project, and once set it can’t be changed.

Next, click **Create resources**. This creates an Azure Site Recovery vault in the background, to hold data and configuration information for the VMs you’re migrating.

#### Download replication components

Next, download the Hyper\-V Replication provider and the registration key file on the Hyper\-V host. The registration key is needed to register the Hyper\-V host with Azure Migrate Server Migration.

1. In the Azure Migrate: Server Assessment panel, select **Discover** to open the Discover machines panel.
2. In the **Are your machines virtualized?** dropdown list, select **Yes, with Hyper\-V**.
3. Copy the provider setup file and registration key file to the Hyper\-V host running the VMs you want to replicate.

#### Install the provider

Run the Azure Site Recovery Provider setup for Hyper\-V, which also installs the Azure Site Recovery Services Agent on the host. In the Provider Setup wizard, opt in to use Microsoft Update and accept the default installation location for the Provider and agent.

#### Register the Hyper\-V host

When setup completes, the Registration wizard presents options to complete the registration of the Hyper\-V host.

* Locate the registration key file you downloaded and associate it with the Azure Site Recovery vault that was created in the Azure Migrate project.
* Specify how the provider connects from the host to the internet. To keep it simple for the pilot, you’ll connect directly to Azure Site Recovery without a proxy server.

Click **Finish** to close the Registration wizard. Return to the Discover panel in Azure Migrate Server Migration and finalize the registration, which is now enabled.

Once registration is complete, close the Discover machines panel.

It can take up to 15 minutes after finalizing registration until discovered VMs appear in Azure Migrate Server Migration. As VMs are discovered, the **Discovered servers** count increases.

### Check your knowledge

---

## Summary

### Summary

In this module, you learned how to implement a migration of your on\-premises workloads to Azure with Azure Migrate. First, you saw how to register your Hyper\-V host server with Azure Migrate Server Migration. Second, you learned how to configure your on\-premises Hyper\-V VMs for replication.

You also learned how to monitor and test that your on\-premises workloads could successfully failover to Azure with no data loss. You then saw how to complete a cutover of your VMs to complete the migration.

Finally, you learned how to secure the migrated VMs by improving resilience, limiting inbound access to VMs, and applying Azure Disk Encryption.

### Learn more

To learn more about the process of migrating Hyper\-V VMs from on\-premises to Azure, see these articles:

* [Migrate Hyper\-V VMs to Azure](/en-us/azure/migrate/tutorial-migrate-hyper-v)
* [How does Hyper\-V replication work?](/en-us/azure/migrate/hyper-v-migration-architecture)
* [Prepare Hyper\-V hosts](/en-us/azure/migrate/tutorial-migrate-hyper-v#prepare-hyper-v-hosts)
* [Replicate Hyper\-V VMs](/en-us/azure/migrate/tutorial-migrate-hyper-v#replicate-hyper-v-vms)

For information on post\-migration best practices and ensuring security of your migrated VMs, see these articles:

* [Azure Virtual Machine Agent overview](/en-us/azure/virtual-machines/extensions/agent-windows)
* [Azure Backup service](/en-us/azure/backup/quick-backup-vm-portal)
* [Just\-in\-time virtual machine access](/en-us/azure/security-center/security-center-just-in-time)
* [Azure Disk Encryption](/en-us/azure/security/fundamentals/azure-disk-encryption-vms-vmss)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/migrate-on-premises-workloads-azure/_

## Fuentes
- [Migrate on-premises workloads to Azure](https://learn.microsoft.com/en-us/training/modules/migrate-on-premises-workloads-azure/?WT.mc_id=api_CatalogApi)
