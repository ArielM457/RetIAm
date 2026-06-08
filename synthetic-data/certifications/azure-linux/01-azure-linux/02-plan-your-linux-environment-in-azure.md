# Plan your Linux environment in Azure

> Curso: Linux on Azure (azure-linux) · Seccion: Linux on Azure
> Duracion estimada: 35 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Suppose you work as an information technology (IT) system engineer for a financial services company. The company intends to transition its existing on\-premises Linux\-based workloads to Azure Linux virtual machines (VMs), which requires consolidating and upgrading some of these systems.

Azure offers several options for deploying Linux\-based Azure VMs. The company asks you to design a set of guidelines that will help:

* Ensure that the target environment is properly sized and secure.
* Maintain the same support, performance, and functionality as the on\-premises environment.

To optimize the VMs' performance, functionality, and pricing, you must properly plan their configuration and deployment. This learning module reviews how to plan for a deployment of Azure VMs that run Linux operating system (OS). The deployment planning process involves:

* Choosing the VM sizes most suitable for their intended workloads.
* Identifying corresponding networking dependencies.
* Defining storage options.
* Implementing optimization techniques that help maximize deployment benefits.

After you complete this module, you can plan for and recommend compute, networking, and storage options for deploying Azure Linux VMs. You also gain a good understanding of overall Azure platform capabilities that help you optimize your Azure Linux VM environments.

---

## Plan for sizing and networking

Azure VM is a popular infrastructure\-as\-a\-service (IaaS) compute resource type in Azure. Compared with platform\-as\-a\-service (PaaS) compute services, Azure VMs provide more flexibility and control over the VM operating system (OS) and its configuration. The increased control and flexibility require more planning to support optimal outcomes.

This unit describes overall factors and considerations for planning Azure Linux VM deployments. The planning process should consider the compute, networking, and storage aspects of the VM configuration. Some of these characteristics are OS–specific, with implementation details varying across different Linux distributions.

Microsoft partners work with prominent Linux vendors to integrate their products with the Azure platform. To fully benefit from this integration, you can create Azure VMs from prebuilt images for various popular Linux distributions, such as SUSE, Red Hat, and Ubuntu. Optionally, you can build a custom image of a Linux distribution to run in the cloud environment. In this case, there might be more steps in your Azure VM provisioning process.

In either case, this learning module can help further optimize your resulting deployment. Optimization requires you to have a strong understanding of the Azure VM resource and its dependencies.

### Understand resource dependencies

When you create an Azure VM, you also need to create several associated resources on which the Azure VM depends to provide full functionality to the virtualized OS. These resources include:

* Virtual disks to store the OS, applications, and data.
* A virtual network with one or more subnets to connect the Azure VM to other Azure services, or to your on\-premises datacenters.
* A network interface to connect the Azure VM to a subnet of the virtual network.

Note

Every network interface must have at least one private IP address assigned to it dynamically or statically. Private IP addresses aren't separate Azure resources, but are part of the subnet configuration.
* A resource group to host the Azure VM.
* Optionally, a public IP address associated with the VM's network interface to provide direct inbound access to the VM from the internet.

Now that you understand the Azure VM resource dependencies, you can begin planning for VM sizing.

### Plan for sizing

To determine the right size for your Azure VM, you need to consider its intended workload. The size you choose determines the following characteristics of the VM:

* Processing power
* Memory
* Storage capacity
* Performance
* Support for advanced networking features

Important

Azure VMs have virtual CPU (vCPU) quota limits for which you should account in planning. To raise quota limits after deployment, you must submit an online request to Azure Support.

Azure offers a wide range of sizes with different specifications and price points to meet a wide variety of needs. VM sizes are grouped into several categories that represent the types of workloads for which they're optimized. Each category includes one or more series, or *families*, which share common underlying hardware characteristics but offer a range of different sizes.

The following list shows the workload types and common use cases for each workload type. Each workload type has corresponding families that include various sizes.

* **General purpose**: Testing and development, small\-to\-medium databases, and low\-to\-medium traffic web servers.
* **Compute\-intensive**: Medium\-traffic web servers, network appliances, batch processes, and application servers.
* **Memory\-intensive**: Relational database servers, medium\-to\-large caches, and in\-memory analytics.
* **Storage\-intensive**: Big data, SQL, and NoSQL databases that require high disk throughput and input/output (I/O).
* **Graphics Processing Unit (GPU)\-enabled**: Heavy graphics rendering or video editing, and model training and inferencing with deep learning.
* **High\-performance computing (HPC)**: Fastest and most powerful CPU VMs, with optional high\-throughput network interfaces that support Remote Direct Memory Access (RDMA).

When you plan for Azure VM sizes, also consider the following factors:

* Changing the Azure VM series or size, while straightforward and commonplace, requires an OS restart. To avoid restarts, size the VM appropriately from the beginning, if possible.
* VM size availability varies by region, so account for regional availability when you plan your deployment.
* The maximum number of disks you can attach to an Azure VM depends on its size.

#### Other size considerations

Consider using [Microsoft Copilot in Azure](https://techcommunity.microsoft.com/blog/azurecompute/using-microsoft-copilot-in-azure-to-find-the-best-vm-size-for-you/4356049) to determine the most suitable VM size based on the workload type, OS, software installed, and deployment region.

If you plan to use the same or similar size Azure VMs in the same region over an extended period, consider using [Azure Reservations](/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations) to reduce compute cost by up to 72 percent.

To lower the cost of Azure VMs for workloads that can handle interruptions, such as batch processing jobs, use [Azure Spot VMs](/en-us/azure/virtual-machines/spot-vms).

### Plan for networking

VMs communicate with external resources by using a *virtual network*. A virtual network represents a private network within an Azure region. You can connect virtual networks to other networks, including networks in your on\-premises datacenters, and apply traffic rules to control inbound and outbound connectivity.

Each virtual network designates an *IP address space* that typically consists of one or more *private address ranges*, as defined by [RFC 1918](https://datatracker.ietf.org/doc/html/rfc1918). As with on\-premises networks, you can divide the virtual network address space into multiple *subnets* to isolate Azure VM workloads. Each subnet within a virtual network represents a private address range. To enforce workload isolation, you associate a *Network Security Group (NSG)* with each subnet.

Every Azure VM includes one or more *network interfaces*, and each interface connects to a subnet within the same virtual network. Azure automatically assigns every VM in the subnet an IP address from the subnet's range. Azure reserves the first four and the last IP address on every subnet for its own use and doesn't assign them.

While it's possible to create a virtual network and subnets as part of a VM provisioning process, the recommended approach is to start Azure VM deployment planning with the network environment. After you account for all networking requirements and create the corresponding virtual networks, you can proceed with deploying the Azure VMs.

As you plan for Azure virtual networks and subnets, keep in mind the following design principles:

* Make sure address spaces don't overlap. If you want to connect your virtual networks and on\-premises networks, the IP address spaces can't overlap.
* Use a smaller number of larger virtual networks rather than a larger number of smaller virtual networks. This practice helps minimize management overhead and facilitates scalability.

#### Network bandwidth

Although an Azure VM can have multiple network interfaces, its available bandwidth depends completely on its size. In general, larger VM sizes are allocated more bandwidth than smaller sizes.

To measure the amount of actual network bandwidth against the allocated limit, Azure targets only egress traffic. All network traffic leaving the VM counts toward that limit, regardless of the traffic destination.

Azure doesn't directly limit ingress bandwidth. However, factors such as storage and compute resource utilization affect the volume of incoming data an Azure VM can process.

### Plan for remote connectivity

As part of your deployment planning, consider the most suitable approach to providing remote connectivity. For Linux VMs, remote connectivity typically involves using *Secure Shell (SSH)* to implement in\-transit encryption of a terminal shell session.

To authenticate over an SSH connection, you can use a username and password or an *SSH key pair*. Using passwords for SSH connections leaves the VM vulnerable to brute\-force attacks. Using SSH keys is a more secure and preferred method of connecting to a Linux VM with SSH.

Even with SSH keys, by default you must open connectivity to a public IP address associated with the target Azure VM's network adapter. This public IP is vulnerable to external threats and represents a potential attack vector. To mitigate this risk, consider implementing Azure Bastion or just\-in\-time (JIT) VM access.

Note

To eliminate the need for public IP addresses when connecting from your on\-premises environment to Azure VMs in hybrid scenarios, you can use a site\-to\-site virtual private network (VPN) or Azure ExpressRoute.

#### Azure Bastion

You deploy the Azure Bastion service into a dedicated subnet of a virtual network that has connectivity to the target VM. Azure Bastion serves as a broker for external SSH connections over HTTPS that are available only from the Azure portal. Azure Bastion eliminates the need for assigning public IP addresses to the target VM's network interface, and also ensures that only authenticated and properly authorized users can initiate SSH connections.

#### JIT VM Access

JIT VM access is a Microsoft Defender for Cloud feature that limits access to a public IP address associated with an Azure VM's network interface. These limits dynamically adjust the NSG to allow incoming connections only from a designated IP address range during a designated time window. As with Azure Bastion, users must authenticate before initiating a connection from the Azure portal.

---

## Manage Azure Linux VMs

To optimize the manageability of Azure Linux VMs, you must understand the interaction between the Azure platform and the VM operating system (OS). This interaction is especially significant during VM provisioning.

### Platform\-supported management agents

*VM provisioning* is the process of creating Azure VM configuration parameter values, such as hostname, username, and password, that are available to the OS during the startup or *boot* process. A *provisioning agent* consumes these values, configures the OS, and reports the results when finished.

Azure supports cloud\-init provisioning agents and Azure Linux Agent (WALA).

* **Cloud\-init provisioning agents** are a widely used approach to customizing Linux during an initial boot. You can use cloud\-init to install packages and write files, or to configure users and security. Because cloud\-init is called during the initial boot process, you don't need any more steps or required agents to apply the configuration. For more information, see the [Cloud\-init documentation](https://cloudinit.readthedocs.io/en/latest).

Note

Microsoft is enhancing the VM configuration process to use cloud\-init instead of the Linux Agent. Existing cloud\-init customers can use their current cloud\-init scripts, and new customers can use rich cloud\-init configuration functionality.
* **WALA**. WALA is an Azure platform\-specific agent you can use to provision and configure Azure VMs. You can also use WALA to implement support for Azure extensions.

### Boot diagnostics and serial console

To optimize managing and troubleshooting the boot process, you can enable boot diagnostics and use the serial console.

#### Enable boot diagnostics

Boot diagnostics help you analyze boot failures by collecting serial log information and screenshots. You can enable boot diagnostics during or after VM creation. To expedite the provisioning process, select the managed storage account option to store the boot diagnostics data.

#### Use the Azure VM serial console

You can use Azure VM serial console access for troubleshooting boot failures. Serial console provides a text\-based console over the Linux VM's `ttyS0` serial port. This access is independent of network connectivity or OS state.

Azure users with at least **Contributor**\-level permissions can access the serial console by using the Azure portal or Azure CLI. You must enable boot diagnostics to use the serial console.

The serial console can help you restore a VM to an operational state in situations like the following scenarios:

* Broken file system table *fstab* files
* Misconfigured firewall rules
* File system corruption
* SSH configuration issues
* Common bootloader issues:

	+ **GRUB menu countdown on Gen2 Azure VMs**. Because legacy hardware has been removed from emulation in Generation 2 Azure VMs, the Grand Unified Bootloader (GRUB) menu countdown timer can count down too quickly to display real\-time loading of the default entry. To address this issue, replace the default entry `"timeout=5"` with `"timeout=100000"` in */boot/grub/grub.conf*, or */etc/default/grub*, or their equivalents.
	+ **Kernel panic boot error in kdump**. If the crash dump capture ends with a kernel panic on boot, you should reserve more memory for the kernel. For example, in the Ubuntu GRUB configuration, change the parameter `crashkernel=384M-:128M` to `crashkernel=384M-:256M`.

---

## Optimize performance and functionality

After you incorporate the best sizing, networking, and management practices into your Azure Linux VM deployment plan, consider performance and functionality. This unit explains how to optimize network and storage resources for Azure Linux VM deployments.

### Optimize network performance

To optimize network performance for Azure Linux VMs, you can use kernel\-based network optimizations and implement accelerated networking, if available.

#### Kernel\-based network optimizations

Linux kernels released after September 2017 include network optimization options that enable Azure Linux VMs to achieve higher network throughput. You can get significant throughput performance by using the latest Linux kernel.

New and existing Azure VMs can also benefit from installing the latest [Linux Integration Services (LIS)](https://www.microsoft.com/download/details.aspx?id=55106). Throughput optimization is part of LIS beginning with version 4\.2, and subsequent versions contain further improvements.

#### Accelerated networking

You can implement accelerated networking to minimize latency, maximize throughput, and lower CPU utilization. Accelerated networking uses the host hardware's single\-root I/O virtualization (SR\-IOV) capabilities to improve network performance.

Without accelerated networking, all networking traffic in and out of the VM must traverse the host and the virtual switch. With accelerated networking, network traffic that arrives at the VM's network interface forwards directly to the VM, bypassing the host.

Accelerated networking applies only to the VM it's enabled on. For best results, enable this feature on Azure VMs that are connected to the same virtual network. For communicating across virtual networks or in hybrid scenarios, this feature has minimal impact on overall latency.

Azure supports accelerated networking for most general\-purpose and compute\-optimized–instance sizes that have two or more vCPUs. VM instances that use hyperthreading support accelerated networking on instances that have four or more vCPUs.

### Optimize storage performance

Every Azure Linux VM has at least the following two virtual disks:

* The OS disk, labeled as `/dev/sda`, has a maximum capacity of 2 tebibytes (TiB) for disks in the Master Boot Record (MBR) format or 4 TiB for disks in the GUID Partition Table (GPT) format. The image you use to provision the Azure VM determines the default size.

Avoid storing data and installing applications on the OS disk, because it's optimized for fast boot rather than running non\-OS workloads.
* A temporary disk labeled as `/dev/sdb` and mounted to `/mnt` provides temporary storage. The disk's size and performance depend on the VM size, and its primary purpose is to store a swap file.

	+ The temporary disk serves as short\-term storage for data that can either be discarded or easily recreated. Don't use the temporary disk to store files that must persist across operations like resizing, redeployment, or restarts.
	+ To implement the optimal configuration for a swap file, use cloud\-init for images that support it. Use the Azure VM Linux Agent for images that don't support cloud\-init.

#### Virtual data disks

For storing data and installing applications, you can create virtual disks, attach them to an Azure VM, and mount them within the OS. You can add more disks as needed according to your storage and *input/output per second (IOPS)* requirements. Keep the following considerations in mind:

* The maximum number of disks you can attach to an Azure VM depends on the VM size.
* The maximum number of IOPS an Azure VM supports depends not only on the aggregate throughput of its disks, but also on the VM's maximum IOPS throughput, which the VM size determines. The effective throughput is the lower of the two values.

To provide storage for an Azure VM, you can use Azure\-managed block\-level storage volumes. Azure\-managed disks support the following five disk types to address specific customer scenarios:

* **Ultra Disks** for I/O\-intensive workloads such as SAP HANA, top\-tier databases such as SQL and Oracle, and other transaction\-heavy workloads.
* **Premium solid\-state drives (SSDs) v2** for production and performance\-sensitive workloads that consistently require low latency, high IOPS, and high throughput.
* **Premium SSDs** for production and performance\-sensitive workloads.
* **Standard SSDs** for web servers, lightly used enterprise applications, and development or test scenarios.
* **Standard hard disk drives (HDDs)** for backups and noncritical data with infrequent access.

#### Write barriers for Premium SSDs

To achieve the highest IOPS on Premium SSD disks that have their caches set to `ReadOnly` or `None`, disable write barriers while mounting the file system in Linux. You don't need barriers, because writes to Premium Storage–backed disks are durable for these cache settings. If caching is set to `Read/Write`, keep barriers enabled to ensure write durability.

* If you use reiserFS file system, disable barriers by using the mount option `barrier=none`.
* If you use ext3/ext4, disable barriers by using the mount option `barrier=0`.
* If you use XFS, disable barriers by using the mount option `nobarrier`.

#### I/O scheduling algorithm for Premium SSDs

The Linux kernel offers two sets of disk I/O schedulers to reorder requests, one for the older `blk` subsystem, and one for the newer `blk-mq` subsystem. For Azure Premium storage disks, use a scheduler that passes the scheduling decisions to the underlying virtualization platform.

* For Linux kernels that use the `blk` subsystem, choose the `noop` scheduler.
* For Linux kernels that use the `blk-mq` subsystem, choose the `none` scheduler.

#### Multi\-disk configurations

If your workloads require more IOPS than a single disk can provide, use a software Redundant Array of Independent Disks (RAID) configuration that combines multiple disks. Azure offers disk resiliency at the storage fabric layer, so you can focus on performance by implementing a RAID\-0 stripe.

As an alternative, you can install Logical Volume Manager (LVM) and use it to combine multiple virtual disks into a single\-striped logical storage volume. In this configuration, reads and writes are distributed to multiple disks contained in the volume group, similar to RAID\-0\. For performance reasons, you might want to stripe your logical volumes so reads and writes use all of your attached data disks.

---

## Summary

This module reviewed the process of planning a deployment of Azure Linux VMs.

* You chose the VM sizes most suitable for their intended workloads and identified the corresponding networking dependencies.
* You learned how to manage and troubleshoot your VMs by using boot diagnostics and serial console.
* You reviewed storage options and performance optimization techniques that help maximize the benefits of the planned deployment.

With the knowledge you've gained, you can recommend the compute, networking, and storage options most suitable for hosting your company's Linux\-based workloads on Azure VMs.

### Related resources

* [Sizes for virtual machines in Azure](/en-us/azure/virtual-machines/sizes?toc=%2Fazure%2Fvirtual-network%2Ftoc.json)
* [What are Azure Reservations?](/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations)
* [Use Azure Spot Virtual Machines](/en-us/azure/virtual-machines/spot-vms)
* [What is Azure Bastion?](/en-us/azure/bastion/bastion-overview)
* [Azure Serial Console for Linux](/en-us/troubleshoot/azure/virtual-machines/linux/serial-console-linux)
* [Use Serial Console to access GRUB and single\-user mode](/en-us/troubleshoot/azure/virtual-machines/linux/serial-console-grub-single-user-mode)
* [Create an Azure Virtual Machine with Accelerated Networking](/en-us/azure/virtual-network/create-virtual-machine-accelerated-networking)
* [Create an Azure Virtual Machine with Accelerated Networking](/en-us/azure/virtual-network/create-virtual-machine-accelerated-networking)
* [Optimize network throughput for Linux virtual machines](/en-us/azure/virtual-network/virtual-network-optimize-network-bandwidth#linux-virtual-machines)
* [Azure managed disk types](/en-us/azure/virtual-machines/disks-types)
* [Azure premium storage: design for high performance](/en-us/azure/virtual-machines/premium-storage-performance)
* [Create a SWAP partition for an Azure Linux VM](/en-us/troubleshoot/azure/virtual-machines/create-swap-file-linux-vm)
* [Optimize your Linux VM on Azure](/en-us/previous-versions/azure/virtual-machines/linux/optimization)
* [Configure Software RAID on Linux](/en-us/previous-versions/azure/virtual-machines/linux/configure-raid?toc=%2Fazure%2Fvirtual-machines%2Flinux%2Ftoc.json)
* [Configure LVM on a Linux VM in Azure](/en-us/previous-versions/azure/virtual-machines/linux/configure-lvm)
* [Cloud\-init support for virtual machines in Azure](/en-us/azure/virtual-machines/linux/using-cloud-init)
* [Azure Linux VM Agent overview](/en-us/azure/virtual-machines/extensions/agent-linux)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/plan-your-linux-environment-in-azure/_

## Fuentes
- [Plan your Linux environment in Azure](https://learn.microsoft.com/en-us/training/modules/plan-your-linux-environment-in-azure/?WT.mc_id=api_CatalogApi)
