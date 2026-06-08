# Describe Microsoft Azure resources management

> Curso: Introduction to Microsoft Azure Management tasks (wwl-introduction-microsoft-azure-management-tasks) · Seccion: Introduction to Microsoft Azure Management tasks
> Duracion estimada: 50 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Welcome to the Microsoft Learn module **Describe Microsoft Azure resources management**. This module focuses on basic management tasks for Azure compute, networking, and storage resources. It also quickly covers the use of tags and resource locks. This module focuses on the Azure portal interface.
To get the most out of this module, you should have a basic understanding of Azure resources, including virtual machines, blob storage, and basic network concepts.

### Learning objectives

By the end of this module, you will be able to:

* Explore an Azure subscription.
* Manage virtual machines
* Manage virtual networks
* Manage storage
* Use tags and resource locks.
* Use Copilot to help manage infrastructure.

---

## Explore a Microsoft Azure subscription

Recall that a Microsoft Azure subscription is unit of management, billing, and scale.

Using Azure requires an Azure subscription that is associated with your Microsoft account. The subscription provides authenticated and authorized access to Azure products and services. It also allows you to provision resources.

An account can have multiple subscriptions, but it’s only required to have one. You could use a second subscription to manage different projects, or different clients or customers.

As a key piece of how you use Azure, it’s important to at least be familiar with navigating a subscription.

Access your subscription by logging into your Azure account and selecting it from **Recent** resources, or by accessing the **Subscriptions** blade and then selecting your subscription.

From the subscription overview page, you can see many details about your subscription.

Some important information on this page includes:

* Subscription ID
* Current billing period
* Your role
* Subscription currency
* Your last bill
* Spending rate and forecast

Use the side menu to access other areas, such as the activity log, access control, tags, and cost management, and other settings such as resources and resource locks.

Take some time to explore your subscription and see what other information you can gather. Knowing where to quickly find information will help you manage your subscription and ask for help if the need arises.

---

## Manage virtual machines

Creating a virtual machine (VM) is often one of the first instances of working with cloud compute. It allows you to have a familiar environment (Windows or Linux), but operate in the cloud.

Unlike traditional, on\-premises computers, updating or changing the configuration for many settings on a virtual machine is easily accomplished from the Azure portal. Let’s take a look at managing a Linux virtual machine in the Azure portal.

You can access many of the management features from the VM blade that appears when you select the name of the VM from your list of resources.

### Overview blade

From the overview blade, you can quickly start, stop, or restart your VM. You can also connect to your VM if it’s already running.

The current VM status (running, stopped), operating system, networking information, and infrastructure information are all also available from the overview blade. Many of the settings are linked and you can change configuration by clicking on the linked items.

For example, if you need to change the resource group the VM is assigned to, selecting **move** next to **resource group** takes you to a new screen to reassign the VM to a new resource group.

This unit highlights some of the other blades as well. However, you’re encouraged to take some time to familiarize yourself with all of them, even if they’re not covered in this unit.

Let’s also cover some of the other blades, such as:

* Activity log
* Tags
* Networking
* Settings
* Availability \+ scale

### Activity log

The activity log provides a quick history of the VM’s activity. You can change filters to change what information displays in the report, such as adjusting the *timespan* to include a broader history report to look at trends.

### Tags

Recall that In Azure, **tags** can be used to track metadata on subscriptions, resource groups, or resources. The tags blade on a specific virtual machine provides a location to manage tags for this specific VM. It can be useful to apply tags at the VM level if you’re adding custom tags for custom reporting. For example, if this machine primarily functions as a web host, you could add a tag of **Purpose** with a value of **web host**.

By tagging resources, you can run reports on them to better track usage across specific use cases.

### Networking

The networking blade lets you handle many types of networking related tasks. From configuring load balances to swapping subnets or changing network security groups, if it’s networking related, you can likely accomplish it from the **networking** blade.

#### Changing a subnet

For example, if you have one subnet that’s focused strictly for production web hosting, and another subnet that you use just for testing updates before they’re pushed to live, you can move a virtual machine between subnets to keep metrics correct and networks fulfilling their purpose.

Changing a VM’s subnet is done at the **Network interface / IP configuration** level. The easiest way to access the network interface is simply selecting it from the **network settings** blade.

On the **IP configurations** blade, changing the subnet is as simple as selecting a different subnet from the dropdown and **Apply** the updated settings. You can also add a load balancer from this screen, if one is already created.

Note

Changing networking settings, such as swapping subgroups, may require a restart of the virtual machine.

#### Load balancing

Recall that a load balancer helps distribute network traffic across multiple destinations or hosts.

From the **load balancing** sub under **Networking**, you can add a load balancer to help your virtual network perform more efficiently.

To add a load balancer:

1. Select **Add load balancing**.
2. Choose between an existing load balancer or creating a new one.
3. If creating a new one, select the type of load balancing.
4. Configure the load balancer and create it.

Note

Necessary settings for the load balancer are pulled from the virtual machine (such as resource group and network security group).

### Settings

The settings areas of the menu let’s you control things such as the disks associated with the virtual machine and resource locks, and you can view things like information on the operating system and configuration information.

#### Disks

In the **disks** menu, you can view and swap the operating system or storage disks. For example, if you wanted to upgrade the machine to a newer version of the operating system, and you already had the image configured exactly how you want, you could simply **Swap OS disk** instead of creating a new VM or doing a complete reinstall on this VM.

Similarly, if you need to add more disk storage, you can **Create and attach a new disk** or **Attach existing disks** to VM. This could be handy if you’re transitioning a VM from development to production and you want to quickly swap the data disk.

You can also select either your OS disk or your storage disk to see more information about that disk.

Note

Swapping the OS disk requires a virtual machine restart. You can add a data disk without having to restart the virtual machine.

#### Locks

Recall that you can use delete locks and read\-only locks to prevent anyone from deleting a resource or changing a resource without first removing the lock.

Imagine you have a fleet of VMs and you know that soon many of them will be deleted to decrease your cloud footprint. Adding a delete lock onto key VMs that need to be protected will help avoid them being accidentally deleted.

### Availability \+ scale

Recall that Azure enables both vertical (VM capability) and horizontal (number of VMs) scaling. Both of these types of scaling are accomplished in the **Availability \+ scale** section of the menu.

#### Size

The **Size** submenu provides vertical scaling capabilities. You can scale the VM up, increasing the computing power or memory, or down, decrease the computing power or memory, by selecting the **NEW** VM size and resizing the VM.

Note

Resizing a VM requires a machine restart if the machine is running. Additionally, it’s possible you’ll have more resizing options if you shut the machine down before attempting to change the VM size.

#### Availability \+ scaling

The ***Availability \+ scaling*** submenu provides access to setting up scaling groups and availability sets. Recall that scaling groups will automatically add or remove VMs based on predefined thresholds for VM load. As increased load is encountered, more VMs will be brought on line. Similarly, as load drops, VMs will be taken off\-line to save costs and resources.

Additionally, recall that availability sets help prevent failure by keeping VMs in fault domains and update domains. This helps prevent all of your VMs being updated at the same time or all failing if one fault domain fails.

### Keep exploring virtual machines

There are other menu and submenus available within the virtual machine blade of Azure. Keep exploring to see what other things you can find.

For example, under **Operations\\Auto\-shutdown** you can configure a VM to shut down at the same time every day. You can even configure a notification when it happens.

Under **Backup \+ disaster recovery** you can establish a backup cadence, create restore points, and configure disaster recovery options to configure disaster recovery to a different availability zone or region.

---

## Manage virtual networks

Recall that Azure provides the ability to create and manage your own virtual networks (VNets) and subnets for the virtual networks.

### Virtual networks

In Azure, a VNet is the foundational building block for private networking. It enables Azure resources like virtual machines, app services, and databases to securely communicate with each other, the internet, and on\-premises networks.

VNets can quickly be created and managed to form the Virtual Network blade within Azure. You can create new virtual networks, manage and modify existing VNets, and configure additional settings and resources.

VNets are logically isolated from one another, providing a secure and customizable environment for deploying cloud resources. They also support advanced networking features such as peering, service endpoints, and private links, making them essential for scalable and secure cloud architectures.

Some things that VNETs are great for include:

* Environment isolation: Separate dev, test, and production environments.
* Security boundaries: Enforce strict access controls between workloads.
* Multi\-region deployment: Host VNets in different Azure regions for redundancy and performance.
* Organizational separation: Allow different teams or business units to manage their own networks.
* Subscription limits: Distribute resources across subscriptions to avoid hitting quotas.

### Subnets

Subnets are subdivisions within a VNet that allow you to segment the network into smaller, more manageable sections. Each subnet can host a specific group of resources and apply its own security and routing rules. This segmentation helps improve security, performance, and operational clarity by grouping similar resources together and controlling traffic flow between them.

Common reasons to use multiple subnets include:

* Tiered architecture: Separate web, application, and database layers.
* Custom security policies: Apply different Network Security Groups (NSGs) to control access.
* Service\-specific needs: Some Azure services, such as Azure Bastion, require dedicated subnets.
* Traffic routing: Use custom route tables to direct traffic differently per subnet.

Similarly, once a VNet is selected, managing most of the settings is straight forward. For example, you can quickly add additional subnets, or change the subnet configuration.

---

## Manage storage

Storage, much like compute, can be a complex area of Azure with many options for management and control. However, at a basic level, storage comes down to a handful of key factors for successful management.

Remember that each storage account needs a globally unique name.

### Overview

The overview blade of the storage account provides the opportunity to manage key aspects of the storage account, as well as access to components within the storage account.

For example, from the **Overview** you can identify and update the resource group and subscription for the storage account. You can also check the location or subscription ID.

You can manage tags for the storage account, access your different **Data storage** services, manage **Security \+ networking** and check and configure **Settings**, among other features and functions.

### Data storage

Within the **Data storage** submenu, you can manage your containers, files shares, queues, and tables. Initially, containers and file shares may be the most common areas you’ll access or use within an Azure storage account.

#### Containers

Within the containers blade, you can create a new container, change the access level of a container, or select the container to open the container and explore additional, container specific options.

Once selected to a container, you can add or delete files, make individual or bulk file updates (such as to the access tier), manage shared access tokens, set or update access policy, and check the properties and metadata associated with the container.

Note

Shared access is a way to grant tokenized, time\-bound access to resources within Azure in a secure manner. Shared access tokens apply to many areas within Azure, not just containers.

#### File shares

Selecting one of the file shares from within the **Data storage\\File shares** page gives you access to manage the settings for the file share.

By scrolling down to the properties section, you can manage things such as the data retention period (soft delete) and the access tier (cool, hot, and so on).

You can also configure operational settings such as snapshots and backups for your file tiers.

### Security \+ networking

The **Security \+ networking** area gives access to manage storage account networking, access keys, the shared access signatures, and encryption, among other things. The access keys menu item and the shared access signatures menu item are important areas to be familiar with to help ensure a more secure and robust storage account.

#### Access keys

Access key provides an easy location to manage your storage account access keys. Two access keys are provided, giving you the opportunity to rotate keys on an alternating basis, ensuring one key is always consistent. You can also **show** the access key and the associated connection string.

Rotating the access key is as simple as selecting **Rotate key**.

Warning

When you rotate an access key, the rotated key will be immediately replaced and any signatures or access relying on the old key will be invalid.

#### Shared access signature

The **Shared access signature** page provides a more comprehensive and detailed place to manage shared access for your storage account. You can set the type of service, allowed resource types, permissions, and other settings. It provides a fine\-grained control over your storage account access while enabling access to entities without a Microsoft Entra ID role for authentication.

Shared access signatures are more comprehensive, configurable, and detailed than shared access tokens.

### Settings

The **Settings** area allows you to manage additional components of your Azure storage account. In settings, you can change **configuration** settings around anonymous blob access, storage keys, or even the service tier (hot, cool, or cold).

You can also check your service endpoints and manage resource locks.

---

## Use tags and resource locks

Recall that tags and resource locks are two (2\) tools within Microsoft Azure to help protect and manage resources.

### Tags

Tags let you keep track of resources, group them in ways that make sense to you, and then gather information based on the tagging methodology or schema that you implement.

For example, if you had 100 virtual machines, some used by developers, some used by testers, and other machines used by people not working on your website, you could create a tagging schema that would help you separate the costs into different buckets. You could create a **Purpose** tag. Within that tag, you could assign values such as developers, testers, an overhead.

Then, you could see statistics and metrics on each of those groups simply by referencing the tag value when querying the data.

From the **Tags** blade of Azure, you can quickly see your assigned tags. By selecting one of the tags, you can also see all resources that have that tag assigned.

And recall that tags can be set at different levels. You can set a tag at the subscription level, or the resource group level, or on individual resources. You can even use Azure policy to set it up so that a tag on a resource group is automatically applied to resources within the resource group. Or, you could set it so you got a notification if a resource within that resource group didn’t have the tag – so you could investigate if the resource was in the wrong resource group or if you simply needed to update the tags.

### Locks

Recall that **resource locks** are another management tool available within Azure. Azure offers two types of resource locks.

* Read\-only: Prevents any modifications or deletions. Users are able to read the resource.
* Delete: A delete lock prevents the locked entity from being deleted. However, users with sufficient permissions can still read and edit the resource.

Note

Resource locks override other access and control permissions. For example: If a resource has a delete lock preventing deletion, a user with full administrative rights still won’t be able to delete the resource without first removing the delete lock.

Locks can be created at various levels and they apply to child resources as well. For example, if you create a delete lock on a resource group to prevent deletion of the resource group, all resources within that resource group would also be protected from deletion.

Locks can typically be applied within the resource *settings* section of the resource blade.

---

## Use Copilot to help manage infrastructure

Microsoft Copilot in Azure is an additional and powerful piece to help you manage your Azure resources. Microsoft Copilot in Azure is an artificial intelligence (AI) tool that can help you engage with your Azure resources. Use Microsoft Copilot in Azure to:

* Help find information
* Perform tasks in Azure
* Provide recommendations

### Help find information

You can use Microsoft Copilot in Azure to find information. Have a question about your account or subscription? Ask Microsoft Copilot in Azure. Curious if there are any service outages impacting your resources? Again, ask Microsoft Copilot in Azure.

Or you can ask Microsoft Copilot in Azure to help explain services and resources available, or answer other questions about your Azure environment, resources, or capabilities. It’s even able to let you know which Azure resource is the most or least expensive this billing cycle!

### Perform tasks in Azure

Not only does Microsoft Copilot in Azure help you with information in Azure, but it can also help manage resources directly, provide you with Bicep or JSON scripts to perform actions, write CLI or BASH commands to manage resource, or provide you with a step\-by\-step guide on how to take action within the Azure portal.

And for simple tasks, such as restarting a virtual machine, you can simply ask Microsoft Copilot in Azure to restart the virtual machine for you.

### Provide recommendations

Microsoft Copilot in Azure provides recommendations too! If Microsoft Copilot in Azure needs further information to help, it will ask follow\-up questions until it has enough information to provide a recommendation.

---

## Module assessment

Choose the best response for each question.

### Check your knowledge

---

## Summary

Congratulations on completing the training module. In this module you covered basic management functionality and tools for Microsoft Azure.

You should now be able to:

* Explore an Azure subscription.
* Manage virtual machines
* Manage virtual networks
* Manage storage
* Use tags and resource locks.
* Use Copilot to help manage infrastructure.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/describe-microsoft-azure-resources-management/_

## Fuentes
- [Describe Microsoft Azure resources management](https://learn.microsoft.com/en-us/training/modules/describe-microsoft-azure-resources-management/?WT.mc_id=api_CatalogApi)
