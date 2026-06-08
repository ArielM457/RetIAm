# Administer and manage Windows Server IaaS Virtual Machine remotely

> Curso: Manage Windows Servers and workloads in a hybrid environment (wwl-manage-windows-servers-workloads-hybrid-enviro) · Seccion: Manage Windows Servers and workloads in a hybrid environment
> Duracion estimada: 44 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Tools and techniques such as Cloud Shell, Azure Bastion, and the just\-in\-time (JIT) feature of Microsoft Defender for Cloud allows you to remotely administer and manage Windows Server virtual machines (VMs).

### Scenario

Contoso is a medium\-size financial services company in London with a branch office in New York. Most of its compute environment runs on\-premises on Windows Server. This includes virtualized workloads on Windows Server 2012 R2 hosts. Contoso's IT staff are in the process of migrating Contoso servers to Windows Server 2025\.

Contoso’s IT director realizes that Contoso has an outdated operational model with limited automation and reliance on dated technology. The Contoso IT Engineering team has started exploring Azure capabilities. They want to determine whether Microsoft Azure services might assist with modernizing the current operational model through automation and virtualization.

As part of the initial design, the Contoso IT team asked you, their lead system engineer and server administrator, to set up a proof of concept environment. This environment must verify whether Azure services can help to modernize the IT infrastructure and meet business goals.

The IT operations staff at Contoso need to know how they can remotely manage Windows infrastructure as a service (IaaS) VMs. They also want to be sure that it's possible to restrict administrative connections to those Windows Server IaaS VMs.

This module describes available remote administration tools and how to select the appropriate tools. You'll also learn to use Azure Bastion to secure management connections to Windows Server IaaS VMs. Finally, you learn to configure JIT VM access to restrict connections.

By the end of this module you're able to select and use suitable tools and techniques to remotely manage Windows Server IaaS VMs, and restrict administrative connections to those VMs.

### Learning objectives

After completing this module, you'll be able to:

* Select appropriate remote administration tools.
* Secure management connections to Windows Server IaaS VMs with Azure Bastion.
* Configure JIT VM access.

### Prerequisites

In order to get the best learning experience from this module, you should have knowledge and experience of:

* Managing Windows Server operating system and Windows Server workloads in on\-premises scenarios, including Active Directory Domain Services (AD DS), Domain Name System (DNS), the Distributed File System (DFS), Microsoft Hyper\-V, and file and storage services
* Common Windows Server management tools
* Core Microsoft compute, storage, networking, and virtualization technologies
* On\-premises resiliency Windows Server\-based compute and storage technologies
* Implementing and managing IaaS services in Azure
* Microsoft Entra ID
* Security\-related technologies (firewalls, encryption, multifactor authentication)
* Windows PowerShell scripting
* Automation and monitoring

---

## Select the appropriate remote administration tool

At Contoso, the server operations team is used to performing remote management of their on\-premises servers. They understand that it's more efficient to remotely administer and maintain servers than it is to interactively administer them using locally installed tools. They realize that for the Windows IaaS VMs being deployed in Azure, they must rely solely on remote management to administer and maintain cloud\-based resources. As lead engineer, you've set up a short presentation on the available management tools for the new hybrid environment that exists at Contoso.

### What is the Azure portal?

The *Azure portal* is a web\-based, unified console that provides an alternative to command\-line tools. With the Azure portal, you can manage your Azure subscription using a graphical user interface (GUI). The first thing you observe after you sign in to the portal is Azure Home. This page compiles resources that help you get the most from your Azure subscription. It also has links to free online courses, documentation, core services, and useful sites for staying current and managing updates to your organization.

The Azure portal menu and page header are global elements that are always present. These persistent features are the shell for the user interface associated with each service or feature, and the header provides access to global controls. The configuration page (sometimes referred to as a *blade*) for a resource might also have a resource menu to help you move between features.

### What is Windows Admin Center?

The Azure hybrid services tool in Windows Admin Center consolidates all the integrated Azure services into a single location where you can explore all the available Azure services in your on\-premises or hybrid environment. The capabilities that the Azure hybrid services tool provides includes:

* Extend storage capacity. You can extend storage capacity by using one of the following methods:
	+ Syncing your file server with the cloud.
	+ Migrating storage to an Azure VM.
* Extend compute capacity. You can extend compute capacity by using one of the following methods:
	+ Creating a new Azure VM.
	+ Providing cloud witness for cluster.
* Simplify network connectivity between your on\-premises and Azure network. You can simplify network connectivity by:
	+ Connecting your on\-premises servers to an Azure virtual network (VNet).
	+ Making Azure VMs seem like your on\-premises network.
	+ Monitoring all the servers in your environment.
	+ Centrally managing operating system updates.
	+ Improving your security posture.
	+ Ensuring compliance across your hybrid environment.
	+ Performing backups using Azure Backup.

Important

Windows Admin Center requires connectivity to your Azure VMs. You'll need to either assign a public IP address to a VM, set up a gateway, or establish a virtual private network (VPN) connection from the Windows Admin Center computer to Azure.

### What is Azure PowerShell?

Windows PowerShell is a technology that consists of a scripting language and the corresponding engine responsible for script processing. You can extend PowerShell capabilities by importing software libraries, known as *modules*. Modules encapsulate Windows PowerShell code in the form of functions and compiled assemblies, referred to as *cmdlets*. This principle also applies when you work with Azure. You can use Windows PowerShell in combination with **Azure PowerShell** modules to connect to an Azure subscription and provision and manage Azure services.

To manage Azure resources by using Windows PowerShell, you must first install the **Azure PowerShell** modules that provide this functionality. For the most part, this will be the `Az` modules, which include cmdlets that implement features of Azure Resource Manager resource providers. For example, Compute provider cmdlets, which facilitate the deployment and management of Azure VMs, reside in the Az.Compute module.

Note

Deploying and managing Azure resources and services might require using other modules.

After you install the Azure PowerShell modules, you can connect the Azure PowerShell session to the Azure subscriptions that you want to manage. To establish this connection, you first need to authenticate by using an account that exists in the Microsoft Entra tenant that is associated with the target subscription.

Tip

When managing Azure Resource Manager resources, you authenticate by running the `Connect-AzAccount` cmdlet.

You can use Azure PowerShell directly from Azure Cloud Shell in the Azure portal. This approach offers several benefits. It eliminates the need to install Azure PowerShell modules on your local computer, and also guarantees that you're using the latest release of Azure PowerShell.

Tip

This method also doesn't require a separate sign\-in because it uses the same credentials that you use to authenticate to your Azure subscription in the Azure portal.

### What is Azure CLI?

Azure Command\-Line Interface (Azure CLI) provides a command\-line, shell\-based interface that you can use to interact with your Azure subscriptions. Azure CLI offers many of the same features as the Azure PowerShell modules, although the functionality might differ. Azure CLI is available on Windows, Linux, and macOS. You can install Azure CLI directly on Windows or within a Windows Subsystem for Linux.

After you install the Azure CLI, you can connect to the Azure subscriptions that you want to manage. Similar to the Azure PowerShell modules, to establish such a connection you must first authenticate by using either a Microsoft account or a work or school account that exists in the Microsoft Entra tenant associated with the target subscription. To initiate the authentication process, run the following command from a command prompt or Windows PowerShell command prompt.

```
az login

```

Tip

Azure CLI runs from the Windows command prompt or Windows PowerShell.

### What is the Run Command?

Azure Compute provides a feature named *Run Command* that enables you to run scripts inside VMs. The Run Command feature uses the VM agent to run PowerShell scripts within an Azure Windows VM. You can use these scripts for general machine or application management.

Tip

The **Run Command** feature enables VM and application management and troubleshooting using scripts. It's available even when the machine isn't reachable. For example, if the guest firewall doesn't have the Remote Desktop Protocol (RDP) or Secure Shell (SSH) port open.

#### Available PowerShell commands

You can launch a number of PowerShell commands against your Windows VMs using *Run command*.

The following table describes the list of commands available for Windows VMs.

| Name | Description |
| --- | --- |
| **RunPowerShellScript** | Runs a PowerShell script. You can use the RunPowerShellScript command to run any custom script that you want. |
| **DisableNLA** | Disables Network Level Authentication (NLA) |
| **DisableWindowsUpdate** | Disables Automatic Updates through Windows Update. |
| **EnableAdminAccount** | Checks if the local administrator account is disabled, and if so, enables it. |
| **EnableEMS** | Enables Emergency Management Services (EMS) to allow for serial console connection in troubleshooting scenarios. |
| **EnableRemotePS** | Configures the machine to enable remote PowerShell. |
| **EnableWindowsUpdate** | Enables Automatic Updates through Windows Update. |
| **IPConfig** | Displays detailed information for the IP address, subnet mask, and default gateway for each adapter bound to Transmission Control Protocol (TCP)/IP. |
| **RDPSettings** | Checks registry settings and domain policy settings. Suggests policy actions if the machine is part of a domain, or modifies the settings to default values. |
| **ResetRDPCert** | Removes the Transport Layer Security (TLS)/Secure Socket Layer (SSL) certificate tied to the RDP listener and restores the RDP listener security to default. Use this script if you notice any issues with the certificate. |
| **SetRDPPort** | Sets the default or user\-specified port number for Remote Desktop connections. Enables firewall rules for inbound access to the port. |

### What is Azure Cloud Shell?

*Azure Cloud Shell* is an interactive, authenticated, browser\-accessible shell for managing Azure resources. It provides the flexibility of choosing the shell experience that best suits the way you work, either **Bash** or **PowerShell**. You can launch Azure Cloud Shell from within the Azure portal. When you select the link on the menu bar, the shell opens in the same window. From there, you can choose the shell experience you're most comfortable with.

Note

Cloud Shell requires an Azure file share to be mounted.

The following table describes the features of Azure Cloud Shell.

| Feature | Description |
| --- | --- |
| Browser\-based shell experience | Cloud Shell enables you to use a browser to access a command\-line environment. |
| Choice of preferred shell experience | You can choose between Bash or PowerShell. |
| Authenticated and configured Azure workstation | Cloud Shell is managed by Microsoft and provides popular command\-line tools and language support. Cloud Shell also securely and automatically authenticates for access to your Azure resources through Azure CLI or Azure PowerShell cmdlets. |
| Integrated Cloud Shell editor | Cloud Shell provides an integrated graphical text editor. |
| Integrated with `learn.microsoft.com` | You can use Cloud Shell directly from documentation hosted on `learn.microsoft.com`. Cloud Shell is integrated in Microsoft Learn, Azure PowerShell, and Azure CLI documentation. Select the **Try It** button in a code snippet, and the shell opens for you to run the code in the **Focus mode** window. |
| Connect your Azure Files storage | When you run Cloud Shell for the first time, Cloud Shell prompts you to create a resource group, a storage account, and an Azure Files share on your behalf. This is a one\-time step and these resources will be automatically attached for all future sessions. |

Tip

You can also launch Cloud Shell by navigating to [Azure Cloud Shell](https://aka.ms/Azure-Cloud-Shell?azure-portal=true).

#### Additional reading about Azure Cloud Shell

You can learn more by reviewing the following documents:

* [Tutorial: Create and Manage Windows VMs with Azure PowerShell](https://aka.ms/tutorial-manage-vm?azure-portal=true).
* [Tools installed in Cloud Shell](https://aka.ms/tools-installed-in-cloud-shell?azure-portal=true).

#### Try it with Azure Cloud Shell

If you'd like to try managing VMs using Azure CLI, you can use the exercise in the following Learn module.

* [Manage virtual machines with the Azure CLI](https://aka.ms/manage-virtual-machines-with-the-azure-cli?azure-portal=true).

These exercises run within the context of a sandbox and don't require an Azure subscription.

---

## Create an Azure Bastion host

In this demonstration, you'll learn to:

* Create an Azure Bastion host.

### Next steps

Review the steps for this demonstration: [Create an Azure Bastion host using the portal](https://aka.ms/create-an-azure-bastion-host-using-the-portal?azure-portal=true).

If you want to repeat these steps, [get a free trial Azure subscription](https://aka.ms/Azure_free_account?azure-portal=true).

After completing the steps, delete any resource groups you created.

---

## Configure just\-in\-time administration

The security specialists at Contoso know that all their VMs are potentially at risk from malicious hackers that actively hunt for security weaknesses. These persons search for open ports such as RDP and SSH. Although using Azure Bastion can help mitigate these risks, the specialists would like to know more about other mitigations that Azure can offer. You decide to investigate the Just In Time (JIT) VM access feature. By using JIT, you can lock down the inbound traffic to your VMs, helping to reduce exposure to attacks while still providing the ability to connect to VMs when needed.

### How does JIT administration work?

You enable JIT for VMs through Microsoft Defender for Cloud. You can then define the network ports that are to be secured for inbound communications on your VMs. Microsoft Defender for Cloud imposes a *deny all inbound traffic* rule for your selected ports by using the NSG and Azure Firewall rules. Together, these elements help to protect your VMs by screening the management ports.

If an administrator needs to perform a management task on a protected VM, Microsoft Defender for Cloud verifies that the user has the required role\-based access control (RBAC) permissions for that VM, and then approves the request and reconfigures the NSGs and Azure Firewall. These changes allow inbound traffic to the selected ports from the relevant IP address, for the specified period of time.

Microsoft Defender for Cloud applies flow logic to determine how to categorize your VMs.
Microsoft Defender for Cloud classifies a device as **healthy** by checking:

* If JIT access already enabled on the VM
* If the VM is assigned to an NSG that doesn't have Allow rules for ports 22, 3389, 5985, and 5986
* If the VM is protected by a firewall that doesn't have Allow rules for ports 22, 3389, 5985, and 5986

If the VM isn't already JIT\-enabled, and isn't assigned to an NSG, and also isn't protected by a firewall, then Microsoft Defender for Cloud classifies the VM as **not applicable**. Otherwise, Microsoft Defender for Cloud recommends enabling JIT for the VM.

The following diagram describes the flow process.

Using this logic, Microsoft Defender for Cloud might decide that a VM can benefit from JIT. As a result of this determination, the VM is moved to the **Unhealthy resources** tab in the Microsoft Defender for Cloud **Recommendations** blade for **Management ports of virtual machines should be protected with just\-in\-time network access control**.

Tip

You can access this information in Microsoft Defender for Cloud by selecting the **Compute \& apps** link in **RESOURCE SECURITY HYGIENE** section. Then select **Management ports of virtual machines should be protected with just\-in\-time network access control**.

### Enable JIT on your VMs

You can enable JIT from within Microsoft Defender for Cloud. Use the following procedure:

1. From the list of VMs displaying on the **Unhealthy resources** tab, select any that you want to enable for JIT, and then select **Remediate**.
2. On the **JIT VM access configuration** blade, for each of the ports listed:

	1. Select and configure the port using one of the following ports:
		* 22
		* 3389
		* 5985
		* 5986
	2. Configure the protocol **Port**, which is the protocol number.
	3. Configure the **Protocol**:
		* Any
		* TCP
		* UDP
	4. Configure the **Allowed source IPs** by choosing between:
		* Per request
		* Classless Interdomain Routing (CIDR) block
	5. Choose the **Max request time**. The default duration is 3 hours.
3. If you made changes, select **OK**.
4. When you've finished configuring all ports, select **Save**.

Alternatively, you can navigate to the VM in the Azure portal. On the selected VM's **Virtual machine** blade, select both **Security** in the navigation pane, and the link for **Management ports of virtual machines should be protected with just\-in\-time network access control**.

#### Request access to a JIT\-secured VM

If you attempt to connect to a VM that isn't protected with JIT, you'll receive a warning in the **Connect** blade.

Tip

You can select this warning link to enable JIT.

However, if JIT is enabled for a VM and you attempt to connect to it, Azure instructs you to request access. You can do this by selecting **Request access**.

After you select **Request access**, it takes up to a minute for Microsoft Defender for Cloud to enable access, assuming that you've the relevant permissions. After access is granted, a message displays instructing you that you've access over the desired port.

### Try it

If you'd like to try setting up JIT for your VMs, you can attempt the [Exercise \- enable JIT VM access](https://aka.ms/3-exercise-jit-vm-access?azure-portal=true). You'll need an Azure subscription to use it. If you don't have one, you can [get a free trial Azure subscription](https://aka.ms/Azure_free_account?azure-portal=true). After completing the exercise, delete any resource groups that you've created.

Note

Make sure to select a subscription that's enrolled in the standard tier of Microsoft Defender for Cloud, or has an active 30\-day trial for Microsoft Defender for Cloud.

---

## Summary

The IT operations staff at Contoso needed to know how to remotely manage Windows Server IaaS VMs. They also wanted to be able to restrict administrative connections to those VMs. You were tasked with evaluating the options and recommending solutions.

In this module, you've learned about remote administration tools for Windows Server IaaS VMs, such as Cloud Shell. You've also learned how to secure management connections to Windows Server IaaS VMs with Azure Bastion and to configure JIT VM access. Now, you and Contoso's IT operations staff can use Azure Bastion and other tools to make secure connections to VMs and manage them remotely.

### Learn more

You can learn more by reviewing the following documents:

* [Overview of Azure Cloud Shell](https://aka.ms/overview-of-azure-cloud-shell?azure-portal=true?).
* [Secure your management ports with just\-in\-time access](https://aka.ms/security-center-just-in-time?azure-portal=true).
* [Tutorial: Learn about Windows virtual machine management with Azure PowerShell](/en-us/azure/virtual-machines/windows/quick-create-powershell).
* [Azure CLI command reference](https://aka.ms/azure-cli-command-reference?azure-portal=true).

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/administer-manage-windows-server-iaas-virtual-machine-remotely/_

## Fuentes
- [Administer and manage Windows Server IaaS Virtual Machine remotely](https://learn.microsoft.com/en-us/training/modules/administer-manage-windows-server-iaas-virtual-machine-remotely/?WT.mc_id=api_CatalogApi)
