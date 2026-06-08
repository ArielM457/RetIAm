# Manage hybrid workloads with Azure Arc

> Curso: Manage Windows Servers and workloads in a hybrid environment (wwl-manage-windows-servers-workloads-hybrid-enviro) · Seccion: Manage Windows Servers and workloads in a hybrid environment
> Duracion estimada: 44 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You can use Azure Arc to apply Azure Policy guest configuration to on\-premises Windows Server instances.

### Scenario

Contoso is a medium\-size financial services company in London with a branch office in New York. Most of Contoso’s compute infrastructure consists of on\-premises Windows Servers. This includes virtualized workloads on Windows Server 2012 R2 hosts. Contoso’s IT staff is in the process of migrating to Windows Server 2025\.

Contoso’s IT director realizes that Contoso has an outdated operational model with limited automation and reliance on dated technology. The Contoso IT Engineering team has started exploring Azure capabilities. They want to determine whether Azure services might assist with modernizing the current operational model through automation and virtualization.

As part of the initial design, the Contoso IT team asked you, their lead system engineer and server administrator, to set up a proof\-of\-concept environment. This environment must verify whether Azure services can help to modernize the IT infrastructure and meet business goals.

Contoso will continue to operate an on\-premises environment for some time after they begin migrating workloads to Azure infrastructure as a service (IaaS) virtual machines (VMs). To remain compliant, Contoso needs the ability to apply Azure policies to on\-premises Windows Server workloads so that they're configured in a similar manner to IaaS VM workloads. In addition, administrators need to review on\-premises Windows Server instances in the Azure console.

In this module, you learn how to describe Azure Arc, implement Azure Arc with on\-premises server instances, deploy Azure policies with Azure Arc, and use role\-based access control (RBAC) to restrict access to Log Analytics data.

### Learning objectives

After completing this module, you'll be able to:

* Describe Azure Arc.
* Explain how to onboard on\-premises Windows Server instances in Azure Arc.
* Connect hybrid machines to Azure from the Azure portal.
* Use Azure Arc to manage devices.
* Restrict access using RBAC.

### Prerequisites

In order to get the best learning experience from this module, it's important that you have knowledge and experience of the following:

* Managing Windows Server operating systems and Windows Server workloads in on\-premises scenarios, including AD DS, Domain Name System (DNS), the Distributed File System (DFS), Microsoft Hyper\-V, and file and storage services.
* Common Windows Server management tools.
* Core Microsoft compute, storage, networking, and virtualization technologies.
* On\-premises resiliency Windows Server\-based compute and storage technologies.
* Implementing and managing IaaS services in Azure.
* Microsoft Entra ID.
* Security\-related technologies (firewalls, encryption, multifactor authentication).
* Windows PowerShell scripting.
* Automation and monitoring.

---

## Describe Azure Arc

*Azure Arc* is a service that provides a set of technologies for organizations such as Contoso that want to simplify their complex and distributed environments.

*Azure Arc* is a set of technologies that brings Azure security and cloud\-native services to hybrid and multicloud environments. It provides a centralized, unified, and self\-service approach to managing, securing, and monitoring:

* Windows Server
* Linux servers
* Kubernetes clusters
* SQL servers
* Azure Data Services

Azure Arc also extends adoption of cloud native services and DevOps across hybrid, multicloud, and edge environments. In addition to extending the control plane for managing infrastructure, Azure Arc enables companies to run Azure data services, and Azure Machine Learning on containerized infrastructure anywhere.

Continuous improvements have been made to the Azure control plane. This control plane is responsible for managing the lifecycle of resources such as VMs, database instances, Apache Hadoop clusters, and Kubernetes clusters.

For example, every time Contoso provisions, scales, stops, or terminates a resource—such as an Azure VM—the Azure fabric controller processes this operation. In between the fabric controller and the resources is another layer called the *Azure Resource Manager* that automates the resource lifecycle. Azure has resource providers for each of these resource types hosted in Azure.

Note

Azure Resource Manager provides a management layer that enables you to create, update, and delete your Azure resources.

### Azure Arc capabilities

Azure Arc enables you to deploy and configure the following cloud based technologies to secure, manage, and monitor Arc\-enabled servers:

**Feature**

**Description**

Azure Policy guest configuration

Audit Azure Arc resources to validate such settings as configurations of the operating system (OS), applications, and environment settings

Support for resource\-context–access Log Analytics data

Restrict the scope of access to Log Analytics data based on the permissions to the corresponding Azure resource.

Microsoft Defender for Cloud

Microsoft Defender for Endpoint provides threat detection and vulnerability management.

Microsoft Sentinel

Collect security\-related events and correlate them with other data sources.

Azure Monitor

Monitor and store data related system performance and events. Discover application components and processes to determine dependencies.

### Additional reading

You can learn more by reviewing the following documents.

* [What is Azure Resource Manager?](https://aka.ms/azure-resource-manager-management-overview?azure-portal=true)
* [What is Azure Arc for servers?](https://aka.ms/azure-arc-servers?azure-portal=true)

---

## Onboard Windows Server instances

Azure Arc expands the support for Azure Resource Manager to resources running outside of Azure. This means that a physical server or a VM running in an on\-premises datacenter can be registered with Azure Resource Manager and presented as a compute resource to the fabric controller. This applies to any server running the Windows Server or Linux server in an on\-premises datacenter or hosted by a third\-party cloud provider.

### Deploy Azure Arc to on\-premises computers

Before the physical server or VM can register, you must install the Azure Connected Machine agent on each of the operating systems targeted for Azure Resource Manager\-based management. The agent for Windows Server is implemented as a Microsoft Windows Installer (.msi), which is available from the Microsoft Download Center.

Tip

Download the Azure Connected Machine agent from the [Microsoft Download Center](https://aka.ms/AzureConnectedMachineAgent?azure-portal=true).

For smaller\-scale deployments, you can use the onboarding script available directly from the Azure portal.

#### Azure Connected Machine

The Azure Connected Machine agent enables you to manage Windows and Linux machines hosted on\-premises or with another cloud provider. The Azure Connected Machine agent officially supports the following versions of the Windows and Linux operating systems:

* Windows Server 2012 R2, 2016, 2019, 2022, and 2025
* Azure Stack HCI
* Ubuntu 18\.04, 20\.04, and 22\.04 LTS (x64\)
* SUSE Linux Enterprise Server (SLES) 12 and 15 (x64\)
* Red Hat Enterprise Linux (RHEL) 7, 8 and 9 (x64\)
* Amazon Linux 2 and Amazon Linux 2023 (x64\)
* Oracle Linux 7, 8 and 9 (x64\)

#### Permissions

To onboard and manage machines to Azure Arc\-enabled servers, you must have the respective Azure permissions described in the following table.

**Role**

**Ability**

Azure Connected Machine OnboardingOnboard machines

Onboard machines

Azure Connected Machine Resource Administrator

Read, modify, and delete a machine

#### Installation process

Deploy at ease, selecting from a range of onboarding methods:

* Using a single server deployment script generated from Azure portal
* Using an at scale service principal based deployment script generated from Azure portal
* Using PowerShell script or PowerShell remoting
* Using a Configuration Manager script for a collection of devices
* Using a Configuration Manager custom task sequence for a collection of devices
* Using Group Policy for an organizational unit or domain
* Directly from Azure portal through Automation Update Management
* Directly from Windows Admin Center

The installation creates a number of folders, Windows services, and environment variables during installation. These changes are detailed in the following table.

**Object type**

**Details**

Folders

`C:\Program Files\AzureConnectedMachineAgent`, `%ProgramData%\AzureConnectedMachineAgent`, `%ProgramData%\AzureConnectedMachineAgent\Tokens`, `%ProgramData%\AzureConnectedMachineAgent\Config`, `%SystemDrive%\Program Files\ArcConnectedMachineAgent\ExtensionService\GC`, `%ProgramData%\GuestConfig`, `%SystemDrive%\AzureConnectedMachineAgent\ExtensionService\downloads`

Services

Azure Hybrid Instance Metadata Service and Guest Configuration Service

Variables

IDENTITY\_ENDPOINT (value: `http://localhost:40342/metadata/identity/oauth2/token`) and IMDS\_ENDPOINT (value `http://localhost:40342`)

Local security group

Hybrid agent extension applications

Note

The Azure Connected Machine agent sends a heartbeat message to the Azure Arc service every 5 minutes. If the Azure Arc service stops receiving heartbeat messages from the connected machine, it considers it offline. The machine is then marked as **Disconnected** until heartbeats resume, at which time the machine is marked as **Connected**.

#### Using a PowerShell Script method to onboard a machine

A typical way to onboard a computer is to generate and download a Windows PowerShell script from the Azure portal. To generate the script, use the following procedure:

1. In the Azure portal, search for **Azure Arc**, and then from the returned list, select **Azure Arc**.
2. In Azure Arc, select **Servers** from the left navigation bar.
3. On the **Azure Arc \| Servers** page, select **\+ Add**.
4. On the **Add servers with Azure Arc** page, select **Generate script under Add a Single server**.
5. On the **Prerequisites** section of the **Add servers with Azure Arc** page, review the **Prerequisites** and then select **Next**.
6. On the **Resource details** section of the **Add servers with Azure Arc** page, select the following information, and then select **Next**.

	* Subscription
	* Resource group
	* Region
	* Operating system
	* Optionally, proxy server URL
7. On the **Tags** section of the **Add servers with Azure Arc** page, add Tags and select **Next**.
8. On the **Download and run script** section of the **Add servers with Azure Arc** page, select **Download**.
9. Sign in as a local administrator on computers that you want to onboard, and then run the downloaded script.

When you install the script on target computers, the script downloads the Azure Arc agent from the Microsoft Download center, installs the agent on the server, and then creates an Azure Arc\-enabled server resource to associate with the agent.

The script prompts you to authenticate the target Azure subscription. You must also enter a generated security code and may need to verify your request with multifactor authentication.

Note

Computers will all be assigned to the same subscription, resource group, and Azure region.

In larger environments, you can use the remote PowerShell scripting or a service principal l to perform the installation and registration in an unattended manner. Alternatively, you can automate the deployment using Configuration Manager or Group Policy.

When you onboard a hybrid machine to Azure Arc\-enabled servers, it becomes a connected machine and is represented by a corresponding Azure resource. That resource has a unique Resource ID property. It belongs to a resource group inside a subscription, and it can benefit from Azure Resource Manager\-based mechanisms such as Azure Policy and tags.

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary

Contoso will need to continue operating an on\-premises environment even after migrating workloads to Azure. Consequently, having the ability to apply Azure policies to on\-premises Windows Server workloads is proving to be important. In addition, administrators need be able to review on\-premises Windows Server instances in the Azure console.

In this module, you learned about Azure Arc, including how to onboard on\-premises Windows servers to Azure Arc, how to deploy Azure policies on Azure Arc\-enabled resources, and how to use RBAC to restrict access to Log Analytics data.

You and the IT Team at Contoso are now prepared to use Azure Arc to use Azure’s control pane to consistently manage and govern the company's on\-premises Windows Servers alongside its Azure VMs.

### Learn more

You can learn more by reviewing the following documents.

* [Azure Arc](https://aka.ms/azure-azure-arc?azure-portal=true)
* [What is Azure Arc for servers (preview)?](https://aka.ms/azure-arc-servers?azure-portal=true)
* [Understand Azure Policy's Guest Configuration](https://aka.ms/guest-configuration?azure-portal=true)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/manage-hybrid-workloads-azure-arc/_

## Fuentes
- [Manage hybrid workloads with Azure Arc](https://learn.microsoft.com/en-us/training/modules/manage-hybrid-workloads-azure-arc/?WT.mc_id=api_CatalogApi)
