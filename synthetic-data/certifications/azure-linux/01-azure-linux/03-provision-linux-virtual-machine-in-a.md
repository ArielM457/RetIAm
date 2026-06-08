# Provisioning a Linux virtual machine in Microsoft Azure

> Curso: Linux on Azure (azure-linux) · Seccion: Linux on Azure
> Duracion estimada: 79 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Microsoft Azure supports several methods both to provision resources for a Linux virtual machine (VM) and transition existing Linux\-based workloads.

### Example scenario

Suppose you've been hired by a financial\-services company to transition their existing on\-premises Linux\-based workloads to Azure. You've selected Infrastructure as a service (IaaS) and Platform as a service (PaaS) as services that you'll need for the project, and you've completed planning for the resources required for deployment. You now need to select a deployment methodology that offers an optimal balance between simplicity and efficiency when provisioning the Azure VMs running Linux. Your choices include the Azure portal, the Azure CLI, and Terraform and Bicep templates.

### Review primary deployment methods

When choosing which deployment methodology to use, you should consider what each choice has to offer.

#### Azure portal

The easiest approach to provision Azure resources is to use the [Azure portal](https://portal.azure.com). The *Azure portal* is a web\-based, unified console that offers a convenient alternative to command\-line tools. Its browser\-based graphical interface is designed to assist with resource deployment and management tasks by prompting the user for any required information, providing hints, and displaying helpful messages.

#### Azure CLI

The Azure CLI is a cross\-platform command\-line tool that you can use to access Azure subscriptions and manage their resources. You can run Azure CLI commands interactively in a console interface, such as a Windows Command Prompt window or a Linux shell session. You also can incorporate the Azure CLI into scripts that use Bash shell commands and GNU utilities to automate the process.

#### Terraform

Terraform is an open\-source, multiplatform Infrastructure as Code (IaC) tool that you can use to provision and configure a wide range of environments, including multivendor public and private clouds. Unlike Azure CLI—which provides an *imperative approach* to resource management—Terraform follows a *declarative* approach.

An imperative approach involves writing scripts or running a sequence of commands. You explicitly provide the steps to run to produce a desired outcome. When you use imperative deployments, it's your responsibility to manage dependencies, error handling, and resource updates. A declarative approach involves writing a definition that describes the desired outcome, rather than the steps to implement it; the tooling determines the optimal method to deliver that outcome for you. It does this by inspecting the current state of your environment, comparing it to your target state, and then implementing the changes required to make them identical.

Note

Red Hat Ansible is another popular open\-source tool you can use to complement the Terraform functionality. However, Ansible facilitates provisioning of cloud resources and supports both configuration management and application deployments.

#### Bicep

Bicep offers an alternative declarative provisioning method to Terraform. Although it exclusively targets Azure resources, you can benefit from several integration and usability features common across Microsoft cloud\-based technologies.

Note

For a comprehensive comparison between Bicep and Terraform, refer to [Comparing Terraform and Bicep](/en-us/azure/developer/terraform/comparing-terraform-and-bicep).

Azure supports two types of templates for declarative provisioning:

* **Azure Resource Manager template**: This template uses the JavaScript Object Notation (JSON) open\-standard file format.
* **Bicep template**: This template relies on a domain\-specific language (DSL), which Microsoft developed recently to simplify the template\-authoring experience and enhance the resulting functionality.

You can use both these templates to deploy practically any Azure resource. These templates also easily integrate into version\-control systems and deployment pipelines, resulting in improved automation and reliability. However, in comparison to Azure Resource Manager templates, Bicep templates offer several additional benefits, including more concise syntax and built\-in dependency management.

### What will we learn?

In this module, you'll choose the optimal deployment method of provisioning Linux VMs in Azure. Your choice will be dependent on the criteria that have been established during the deployment planning phase.

### What is the main goal?

By the end of this module, you'll be able to provision Azure VMs running Linux by using the deployment methodology of your choice. You'll also have a better understanding of the most suitable use cases for each method.

---

## Provision a Linux virtual machine by using the Azure portal

To access your Azure subscription by using the Azure portal, you must first sign in with an authorized account. After you're successfully authenticated, the Azure portal's home page displays. This page provides links to core services, recently accessed and favorite resources, built\-in management tools, and online documentation. It also serves as a convenient entry point into your Azure environment.

If the functionality you're looking for isn't present on the home page, you can locate it by using either the portal menu or the global search textbox. Both options are available on every portal page to which you navigate.

* The portal menu simplifies accessing commonly used features and resource types, and it's available in the flyout and docked mode.
* The global search identifies matches for the text you enter across all services, resources, resource groups, marketplace offers, Microsoft Entra ID objects, and online documentation. (By default, the global search box displays the text "Search resources, services, and docs (G\+/)".)

Because the global search box offers a more comprehensive and consistent behavior, all procedures covered in this module will use this option.

To navigate to the portal page dedicated to the provisioning and management of Azure VMs, in the global search box, start entering the phrase *virtual machines*, which designates the Azure resource type you intend to provision. The global search box displays a list of search results even before you've entered the entire phrase. In the search results list, in the Services section, locate the Virtual machines entry. Selecting this entry automatically opens the Virtual machines page of the portal.

Note

For more information about the Azure portal interface, refer to [What is the Azure portal?](/en-us/azure/azure-portal/azure-portal-overview)

### Deploy a Linux VM by using the Azure portal

The process of deploying Azure resources by using the Azure portal involves the following sequence of high\-level steps:

* Initiate the provisioning wizard.
* Assign resource\-specific settings.
* Validate the assigned settings.
* Initiate the deployment.

#### Initiate the provisioning wizard

On the Virtual machines page, select the **\+ Create** link. This step is the same regardless of the resource type you provision.

#### Assign resource\-specific settings

The settings you assign at this stage determine the properties of the deployed resource. Although you can modify most of the settings after deployment, there are some settings that are immutable. The immutable settings include the resource name and the operating system (OS) image, so it's important to carefully consider their assignments. In addition, some of the modifiable settings might impact the resource availability if changed after deployment. For example, you can change an online Azure VM's resource group, but moving it across virtual networks, subscriptions, and regions (although possible) results in downtime. Similarly, changing the Azure VM size, while straightforward and commonly done, requires an OS restart.

Note

Microsoft doesn't support moving resources across subscriptions associated with different Microsoft Entra ID tenants, and provisioning multiple resources that are part of a larger deployment should follow a planning stage that determines their optimal configuration, including a naming convention.

The settings the Azure VM provisioning wizard displays in the Azure portal are grouped into the following pages:

* Basics
* Disks
* Networking
* Management
* Monitoring
* Advanced
* Tags

##### Basics

The settings on this page configure the target subscription, either an existing or new resource group, and the Azure region where the Azure VM and the resources on which it depends will reside. From here you also specify:

* The Azure VM name.
* Availability options.
* The OS image.
* Administrator account name.
* Depending on your choice of the authentication type, either the corresponding password or the secure shell protocol (SSH) key.
* Whether you want to:
	+ Generate a new key pair.
	+ Select an existing key stored in Azure.
	+ Provide an existing RSA public key in the Privacy Enhanced Mail (PEM) format.
* Whether you want to allow connectivity to the deployed Azure VM from the internet via Transmission Control Protocol (TCP) port 22 (SSH).

Caution

If you deploy an individual Azure VM for testing or evaluation purposes, you might choose to allow connectivity from the internet due to the convenience it provides. However, in general, you should avoid exposing Azure VMs to connections originating from the internet without additional constraints. To enhance security in such scenarios, consider implementing Azure Bastion or just\-in\-time (JIT) VM access, which is available as part of the Defender for Cloud service. Azure also offers hybrid connectivity options, including Site\-to\-Site (S2S) virtual private network (VPN), Point\-to\-Site (P2S) VPN, and Azure ExpressRoute. All three options eliminate the need for assigning public IP addresses to Azure VM network interfaces for connections originating from your on\-premises datacenter or designated, internet\-connected computers.

###### Disks

You can use the Disks tab to specify the type and encryption of the disk hosting the Azure VM OS. You can also attach one or more data disks, although this option is available at any point following the deployment. The maximum number of data disks that an Azure VM supports depends on its size.

###### Networking

In addition to the Basic grouping, networking is another critical part of Azure VM configuration that warrants careful consideration. Every Azure VM uses its network interface to attach to a virtual network's subnet. Therefore, having a virtual network with at least one subnet is a prerequisite when provisioning an Azure VM. The Azure portal facilitates implementing this prerequisite by choosing an IP\-address space that doesn't overlap with any existing virtual network in your subscription, and by suggesting the virtual network and subnet names. For test or evaluation scenarios, this is a viable option. However, for any larger deployments, you should design your network environment first. This category also provides additional, more granular settings that you can use to restrict inbound internet traffic. Lastly, to minimize network latency, ensure that accelerated networking is enabled.

Note

Support for accelerated networking depends on the Azure VM size.

###### Management

From the Management tab, you can enable several optional settings to enhance your Azure VM's manageability. These settings control support for Microsoft Defender for Cloud and Microsoft Entra authentication. You can also use them to enable schedule\-based auto\-shutdown, automatic backups, and patch orchestration.

Note

Patch\-orchestration support depends on the OS image.

###### Monitoring

You use the Monitoring tab to enable monitoring settings. These include automatic alerts that notify you about potential resource utilization issues and boot and operating\-system diagnostics.

###### Advanced

This tab provides miscellaneous options that allow you to further customize platform and operating system\-level settings of the Azure VM that are deploying, including:

* Post\-deployment configuration of the guest OS using a wide range of specialized software components and scripts such as Azure VM extensions, cloud\-init, custom data, and user data.
* Installation of applications within the guest OS.
* Deployment to dedicated physical servers, ensuring that your Azure VM isn't running on hardware shared with other Azure customers.
* Minimizing latency between multiple Azure VMs by ensuring that they're part of the same placement proximity group.
* Minimizing costs by using capacity reservations.

###### Tags

You can use this tab to create descriptive labels (*tags*) that you want to assign to the resource. Tags help organize resources based on your own custom criteria, facilitating functionality such as multiple\-resource management, inventory, and billing.

#### Validate the assigned settings

After completing the configuration steps in the various pages of the provisioning wizard, you'll reach the final tab, **Review \+ create**.

##### Review \+ create

At this point, the Azure portal will automatically invoke a validation task, which verifies that the options you've selected are valid. If you've misconfigured a setting or missed a required one, you'll have a chance to go back to the corresponding page to fix your mistake. When you return to the last page, validation will run again.

#### Initiate deployment

If validation is successful, select **Create** to initiate the deployment. Your Azure VM should be running shortly.

---

## Provision a Linux virtual machine by using Azure CLI

You can install Azure CLI locally on Linux, macOS, and Windows operating systems. The installation details depend on the operating system and in the case of Linux, also on the distribution.

Note

For more information about the Linux installation options, refer to [Install the Azure CLI on Linux](/en-us/cli/azure/install-azure-cli-linux).

To use Azure CLI interactively, launch a shell available within your operating system, such as cmd.exe in Windows, or Bash in Linux or macOS, and then issue a command at the command prompt. To automate repetitive tasks, assemble the CLI commands into a shell script using your chosen shell's script syntax, then run the script.

If you want to avoid installing Azure CLI, you can use Azure Cloud Shell. Azure Cloud Shell is an interactive, authenticated shell that you can use to manage Azure resources from a web browser. Azure Cloud Shell can run Bash and Azure PowerShell, and it has the current version of Azure CLI already preinstalled. To access Azure Cloud Shell, open the [Azure Cloud Shell](https://shell.azure.com/) link in a web browser or launch it from the Azure portal by selecting the **Cloud Shell** icon next to the global search textbox.

Azure Cloud Shell provides the benefit of built\-in authentication, which uses the credentials you provide when accessing your Azure subscription from your web browser. This eliminates the need for running the `az login` command at the beginning of each session, which is required when you run Azure CLI locally.

### Deploy a Linux VM by using Azure CLI

The process of provisioning an Azure VM running Linux by using Azure CLI typically involves the following sequence of high\-level steps:

* Identify a suitable VM image.
* Identify the suitable VM size.
* Create a resource group.
* Create and configure a virtual network.
* Create an Azure VM.

Depending on your existing environment and requirements, it might not be necessary to complete each of the preceding steps. For example, you might use an existing resource group or a virtual network subnet for your deployment. In addition, Azure CLI supports a wide range of default settings, which automatically apply if you decide not to explicitly assign values to some of the resource settings. For example, as with the Azure portal\-based deployment, if you don't specify an existing virtual network, Azure CLI automatically provisions one for you. In this module, you'll rely on the Azure CLI default settings and skip the process of creating a virtual network.

Note

For information regarding implementing virtual networks by using Azure CLI, refer to [Quickstart: Use Azure CLI to create a virtual network](/en-us/azure/virtual-network/quick-create-cli).

#### Identify a suitable VM image

Before you start your provisioning process, first you need to determine the VM image that you want to use. You must also verify that image's availability in the Azure region that will host your deployment.

To list the Azure regions available in your subscription, run the following command from a Bash session in the Azure Cloud Shell pane:

```
az account list-locations --output table

```

Review the output and identify the value in the Name column for the region you intend to use. Assume you chose the East US region as your target, so that the name is *eastus*.

To identify the suitable image, you'll need to determine its publisher, offer, and sku. To narrow down the list of available options, list the non\-Microsoft publishers for the region you identified earlier by running the following command:

```
az vm image list-publishers --location eastus --query [].name --output tsv | grep -v "Microsoft" | more

```

Note

The list is quite extensive, so you should ensure that you limit the output to the available session buffer. To exit the list, you can use **CTRL** \+ **C** on your keyboard.

Assume you chose `Canonical`. Next, identify the offers available from that publisher by running the following command:

```
az vm image list-offers --location eastus --publisher Canonical --query [].name --output tsv

```

Assume you chose `0001-com-ubuntu-server-jammy`. Next, run the following command to identify SKUs available with that offer by running the following command:

```
az vm image list-skus --location eastus --publisher Canonical --offer 0001-com-ubuntu-server-focal --query [].name --output tsv

```

Note

Canonical has recently been changing the offer names. Before Ubuntu 20\.04, the offer name was `UbuntuServer`. For Ubuntu 20\.04 the offer name is `0001-com-ubuntu-server-focal`, and for Ubuntu 22\.04 it's `0001-com-ubuntu-server-jammy`.

To deploy an Azure VM using a specific image, you need to determine the value of its `Urn` property. This value consists of the publisher, offer, SKU, and optionally a version number that uniquely identifies the image. You can also set the version number to *latest*, which designates the latest version of the distribution. To display the value of the `Urn` property for all Ubuntu's 22\_04\-lts images in the East US region, run the following command:

```
az vm image list --location eastus --publisher Canonical --offer 0001-com-ubuntu-server-jammy --sku 22_04-lts --all --output table

```

Note

You can use the `UrnAlias` property for a simpler (although much less flexible) approach to designating an image to use during deployment. This property is readily available for the most common images, and you can retrieve its values by running the `az vm image list --output table` Azure CLI command. For example, the `UrnAlias` `Ubuntu2204` corresponds to the image `Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest`.

#### Identify the suitable VM size

In addition to image availability, you also should ensure that the VM size you intend to use is available in the Azure region that will host your deployment. To confirm this, run the following command:

```
az vm list-sizes --location eastus --output table

```

Identify the VM size suitable for your sample deployment from the listing and note the value in the *Name* column. You'll need to enter the name in the identical format when running the Azure CLI command that initiates the Azure VM provisioning. Assume you chose *Standard\_F4s*.

Important

Before you proceed, verify that this VM size is available in the Azure region you're targeting, and if needed, adjust the values of parameters in the subsequent commands accordingly.

#### Create a resource group

After identifying the Azure VM image and size, you can now begin the provisioning process. Start by creating a resource group to host the Azure VM and its dependent resources. To create a resource group, use the `az group create` command. This command requires that you specify both the value of the name and location parameters, which designates the resource group name and the target Azure region, respectively.

```
az group create --name rg_lnx-cli --location eastus

```

The command's output should resemble the following example:

```
{
  "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/sample-RG",
  "location": "eastus",
  "managedBy": null,
  "name": "rg_lnx-cli",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
}

```

#### Create an Azure VM

To create a VM, use the `az vm create` command. This command supports a wide range of parameters, including the OS image, disk size, and administrative credentials. In the following example, the `az vm create` command triggers deployment of an Azure VM named *sample\-cli\-vm0*, which hosts the latest Ubuntu 22\_04\-lts\-gen2 SKU version. The provisioning process configures an administrative user account named azureuser with authentication based on an SSH key pair. The private and public key are generated and stored locally in their default location (\~/.ssh) to allow SSH access to the Azure VM. Use the following code example to create an Azure VM:

```
az vm create \
    --resource-group rg_lnx-cli \
    --name lnx-cli-vm \
    --image Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest \
    --size Standard_F4s \
    --admin-username azureuser \
    --generate-ssh-keys

```

Note

The `--size` parameter is optional. If you decide to exclude it, the resulting size will depend on the image you chose.

The Azure VM will begin running shortly afterwards, usually within a couple of minutes. The Azure CLI command output will include JSON\-formatted information about the newly deployed Azure VM:

```
{
  "fqdns": "",
  "id": "/subscriptions/bbbb1b1b-cc2c-dd3d-ee4e-ffffff5f5f5f/resourceGroups/rg_lnx-cli/providers/Microsoft.Compute/virtualMachines/lnx-cli-vm",
  "location": "eastus",
  "macAddress": "00-0D-3A-8C-C6-AE",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.4",
  "publicIpAddress": "20.51.149.212",
  "resourceGroup": "rg_lnx-cli",
  "zones": ""
}

```

At this point, you'll be able to connect to the Azure VM by running the following command (after replacing the *\<public\_ip\_address\>* placeholder with the IP address you identified in the Azure CLI\-generated output) from the computer where the private key is stored:

```
ssh azureuser@<public_ip_address>

```

---

## Provision a Linux virtual machine by using Terraform

Terraform implements and controls a target infrastructure by using configuration files that describe the desired state of its components. The basic format of the files and their general syntax—expressed in the Hashicorp Configuration Language (HCL)—are the same regardless of the cloud choice. However, individual component descriptions are cloud\-dependent, as determined by the corresponding Terraform provider.

Although there are several Terraform providers that support Azure infrastructure management, AzureRM is of particular relevance. The AzureRM provider facilitates provisioning and configuring common Azure IaaS resources, such as virtual machines, storage accounts, and networking interfaces. There are also additional non\-cloud\-specific providers that you might want to incorporate into your deployments. These include the random provider, which helps with avoiding resource\-naming conflicts by generating pseudo\-random character strings; and the tls provider, which simplifies managing asymmetric keys for securing Linux authentication.

Terraform is available as a single binary you can download from the [Hashicorp website](https://developer.hashicorp.com/terraform/downloads). This binary implements the Terraform command\-line interface (CLI), which you can then invoke from a shell session to initialize Terraform and process configuration files. You can use Terraform CLI from any of the shells that support Azure CLI.

Note

When using Azure Cloud Shell, make sure you run the current version of Terraform by following the instructions provided in [Configure Terraform in Azure Cloud Shell with Bash](/en-us/azure/developer/terraform/get-started-cloud-shell-bash).

### Deploy a Linux VM by using Terraform

Terraform lets you define, preview, and deploy resources to a provider\-specific cloud infrastructure. The provisioning process begins with creating configuration files that use the HCL syntax, which allows you to designate the target cloud environment—such as Azure—and the resources that make up your cloud infrastructure. After all relevant configuration files are in place (typically within the same filesystem location), you can generate an execution plan that allows you to preview the resulting infrastructure changes before the actual deployment. This requires you to initialize Terraform to download the provider modules necessary to implement cloud resources. After you validate the changes, you can apply the execution plan to deploy the infrastructure.

Note

Generating an execution plan is optional, but we recommend you do so because it allows you to identify any impact from the planned deployment without affecting the target environment. When you deploy Azure resources interactively, Terraform supports Azure CLI authentication transparently by reusing your credentials to access the target Azure subscription.

The process of provisioning an Azure VM running Linux by using Terraform typically involves the following sequence of high\-level steps:

* Identify the suitable VM image.
* Identify the suitable VM size.
* Create configuration files that define the Azure VM resource with its dependencies.
* Initialize Terraform.
* Generate a Terraform execution plan.
* Initiate a Terraform deployment.

To identify the suitable VM image and size, follow the steps described in Unit 4 of this module. This unit focuses on Terraform\-specific tasks.

#### Create configuration files

Note

The filenames that you choose for your Terraform files are arbitrary, although it's a good practice to choose a name that reflects the file content or purpose. You should use *.tf* for the file extension.

To deploy a Linux VM by using Terraform, you begin by creating a directory to host configuration files. Next, create a file named *providers.tf* that enforces the Terraform version and designates the providers on which you'll rely when defining the resources included in your deployment. This file should have the content displayed in the following code snippet:

```
terraform {
  required_version = ">=0.12"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3.0"
    }
    tls = {
      source = "hashicorp/tls"
      version = "~>4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

```

In the same directory, create a file named *main.tf* using the following code, which defines the Azure VM configuration and its dependencies:

```
resource "random_pet" "rg_name" {
  prefix = var.resource_group_name_prefix
}

resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = random_pet.rg_name.id
}

## Create virtual network
resource "azurerm_virtual_network" "terraform_network" {
  name                = "lnx-tf-vnet"
  address_space       = ["10.1.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

## Create subnet
resource "azurerm_subnet" "terraform_subnet" {
  name                 = "subnet0"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.terraform_network.name
  address_prefixes     = ["10.1.0.0/24"]
}

## Create public IPs
resource "azurerm_public_ip" "terraform_public_ip" {
  name                = "lnx-tf-pip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Dynamic"
}

## Create Network Security Group and rule
resource "azurerm_network_security_group" "terraform_nsg" {
  name                = "lnx-tf-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "ssh"
    priority                   = 300
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

## Create network interface
resource "azurerm_network_interface" "terraform_nic" {
  name                = "lnx-tf-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "nic_configuration"
    subnet_id                     = azurerm_subnet.terraform_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.terraform_public_ip.id
  }
}

## Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "lnx-tf-nic-nsg" {
  network_interface_id      = azurerm_network_interface.terraform_nic.id
  network_security_group_id = azurerm_network_security_group.terraform_nsg.id
}

## Generate random text for a unique storage account name
resource "random_id" "random_id" {
  keepers = {
    # Generate a new ID only when a new resource group is defined
    resource_group = azurerm_resource_group.rg.name
  }

  byte_length = 8
}

## Create storage account for boot diagnostics
resource "azurerm_storage_account" "storage_account" {
  name                     = "diag${random_id.random_id.hex}"
  location                 = azurerm_resource_group.rg.location
  resource_group_name      = azurerm_resource_group.rg.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

## Create (and display) an SSH key
resource "tls_private_key" "lnx-tf-ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

## Create virtual machine
resource "azurerm_linux_virtual_machine" "lnx-tf-vm" {
  name                  = "lnx-tf-vm"
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.terraform_nic.id]
  size                  = "Standard_F4s"

  os_disk {
    name                 = "lnx-tf-vm-osdisk"
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  computer_name                   = "lnx-tf-vm"
  admin_username                  = "azureuser"
  disable_password_authentication = true

  admin_ssh_key {
    username   = "azureuser"
    public_key = tls_private_key.lnx-tf-ssh.public_key_openssh
  }

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.storage_account.primary_blob_endpoint
  }
}

```

In the same directory, create another file named *variables.tf* using the following code, which assigns the value to the variables appearing in the *main.tf* file:

```
variable "resource_group_location" {
  default     = "eastus"
  description = "Location of the resource group"
}

variable "resource_group_name_prefix" {
  default     = "rg"
  description = "Prefix of the resource group name that's combined with a random ID so name is unique in your Azure subscription"
}

```

Lastly, create a file named *outputs.tf* using the following code, which determines the output that displays following a successful deployment:

```
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "public_ip_address" {
  value = azurerm_linux_virtual_machine.lnx-tf-vm.public_ip_address
}

output "tls_private_key" {
  value     = tls_private_key.lnx-tf-ssh.private_key_pem
  sensitive = true
}

```

#### Initialize Terraform

To initialize the Terraform deployment, run the following command from the shell prompt:

```
terraform init

```

This command downloads the Azure modules necessary to provision and manage Azure resources.

#### Generate an execution plan

After initialization, create an execution plan by running `terraform plan`. The command creates an execution plan, but doesn't run it. Instead, it determines what actions are necessary to create the resources defined in your configuration files. The optional `-out` parameter allows you to specify an output file for the plan, which you can reference during the actual deployment. Using this file ensures that the plan you review matches the exact deployment outcome. Use the following command to generate an execution plan:

```
terraform plan -out <terraform_plan>.tfplan

```

#### Initiate a deployment

When you're ready to apply the execution plan to your Azure environment, run `terraform apply`, including the name of the file you generated in the previous step. You'll have another chance to review the expected outcome. Terraform prompts you for confirmation to proceed, although you can eliminate the prompt by adding the `-auto-approve` switch. Use the following command to initiate the deployment:

```
terraform apply <terraform_plan>.tfplan

```

The Azure VM will shortly begin running, typically within a couple of minutes. The `terraform apply` command output includes the list of outputs, but terraform replaces the value of `tls_private_key` with the \<sensitive\> label:

```
Apply complete! Resources: 12 added, 0 changed, 0 destroyed.

```

Outputs:

```
public_ip_address = "74.235.10.136"
resource_group_name = "rg-flexible-shark"
tls_private_key = <sensitive>

```

To use the autogenerated private key for authenticating your SSH connection, store it in a file and then set the file's permissions to ensure it's not accessible by others. To accomplish this, run the following commands:

```
terraform output -raw tls_private_key > id_rsa
chmod 600 id_rsa

```

At this point, you'll be able to connect to the Azure VM by running the following command (after replacing the \<public\_ip\_address\> placeholder with the IP address you identified in the terraform apply\-generated output):

```
ssh -i id_rsa azureuser@<public_ip_address>

```

---

## Provision a Linux virtual machine by using Bicep

The core element of a Bicep template is `resource`, which designates an Azure resource. Each resource contains a set of generic and resource\-specific properties. For example, the template used in the following example describes an Azure virtual network. While the name and location properties are generic, `addressPrefix` is resource specific. The `Microsoft.Network/virtualNetworks@2021-05-01` string next to the resource designates its API version, and the `virtualNetwork` entry represents its symbolic name, which provides a way to reference the resource within the template.

In addition to the `resource` element, the following sample template also includes a parameter element that enables you to assign a name to the virtual network during deployment. If you don't assign a name at that time, the default value of `lnx-bcp-vnet` applies instead. The description element is an example of a decorator, as indicated by the leading `@` character. Its purpose is to describe the parameter's role, and its output appears beside the parameter's textbox when you use the Azure portal to review or deploy the corresponding Azure Resource Manager template. Use the following code example to provision a Linux VM by using Bicep:

```
@description('Name of the virtual network')
param virtualNetworkName string = 'lnx-bcp-vnet'

resource virtualNetwork 'Microsoft.Network/virtualNetworks@2021-05-01' = {
  name: virtualNetworkName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        addressPrefix
      ]
    }
  }
}

```

### Deploy a Linux VM by using Bicep templates

Working with Bicep involves authoring and deploying templates. To simplify and enhance the authoring experience, use Visual Studio Code with the Bicep extension. The same extension also supports Bicep\-based deployments. If you prefer to trigger a deployment from a command line or as part of a scripted task, you can install and use Bicep CLI as a standalone utility or use it directly from within an Azure CLI session. The Azure CLI installs the Bicep CLI automatically during the first invocation of any `az bicep` command. However, to perform a manual installation of Bicep, run `az bicep install`.

Effectively, the process of provisioning an Azure VM running Linux by using Bicep typically involves the following sequence of high\-level steps:

* Identify a suitable VM image.
* Identify the suitable VM size.
* Author a Bicep template.
* Initiate deployment of the Bicep template.

When you deploy Bicep templates, a task referred to as transpilation automatically converts them into equivalent Azure Resource Manager templates. You can also perform a conversion between the Bicep and Azure Resource Manager formats by running the `bicep build` and `bicep decompile` commands, respectively.

To identify the suitable VM image and size, follow the steps described in the earlier units of this module. This unit focuses on Bicep\-specific tasks.

### Author a Bicep template

To author a Bicep template, start by launching a Visual Studio Code session with the Bicep extension installed. Next, create a file named *main.bicep*. Add the following content to the file, then save the change:

Note

The filenames that you choose for your Bicep files are arbitrary, although it's a good practice to choose a name that reflects the file content or purpose. You should use *.bicep* for the file extension.

```
@description('The name of your virtual machine')
param vmName string = 'lnx-bcp-vm'

@description('Username for the virtual machine')
param adminUsername string

@description('Type of authentication to use on the virtual machine')
@allowed([
  'sshPublicKey'
  'password'
])
param authenticationType string = 'password'

@description('SSH Key or password for the virtual machine')
@secure()
param adminPasswordOrKey string

@description('Unique DNS Name for the Public IP used to access the virtual machine')
param dnsLabelPrefix string = toLower('${vmName}-${uniqueString(resourceGroup().id)}')

@description('The allowed Linux distribution and version for the VM')
@allowed([
  'Ubuntu-2204'
])
param ubuntuOSVersion string = 'Ubuntu-2204'

@description('Location for all resources')
param location string = resourceGroup().location

@description('The size of the VM')
param vmSize string = 'Standard_F4s'

@description('Name of the virtual network')
param virtualNetworkName string = 'lnx-bcp-vnet'

@description('Name of the subnet in the virtual network')
param subnetName string = 'subnet0'

@description('Name of the network security group')
param networkSecurityGroupName string = 'lnx-bcp-nsg'

var imageReference = {
  'Ubuntu-2204': {
    publisher: 'Canonical'
    offer: '0001-com-ubuntu-server-jammy'
    sku: '22_04-lts-gen2'
    version: 'latest'
  }
}
var publicIPAddressName = '${vmName}-pip'
var networkInterfaceName = '${vmName}-nic'
var osDiskType = 'Standard_LRS'
var subnetAddressPrefix = '10.3.0.0/24'
var addressPrefix = '10.3.0.0/16'
var linuxConfiguration = {
  disablePasswordAuthentication: true
  ssh: {
    publicKeys: [
      {
        path: '/home/${adminUsername}/.ssh/authorized_keys'
        keyData: adminPasswordOrKey
      }
    ]
  }
}

resource networkInterface 'Microsoft.Network/networkInterfaces@2021-05-01' = {
  name: networkInterfaceName
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          subnet: {
            id: subnet.id
          }
          privateIPAllocationMethod: 'Dynamic'
          publicIPAddress: {
            id: publicIPAddress.id
          }
        }
      }
    ]
    networkSecurityGroup: {
      id: networkSecurityGroup.id
    }
  }
}

resource networkSecurityGroup 'Microsoft.Network/networkSecurityGroups@2021-05-01' = {
  name: networkSecurityGroupName
  location: location
  properties: {
    securityRules: [
      {
        name: 'ssh'
        properties: {
          priority: 1000
          protocol: 'Tcp'
          access: 'Allow'
          direction: 'Inbound'
          sourceAddressPrefix: '*'
          sourcePortRange: '*'
          destinationAddressPrefix: '*'
          destinationPortRange: '22'
        }
      }
    ]
  }
}

resource virtualNetwork 'Microsoft.Network/virtualNetworks@2021-05-01' = {
  name: virtualNetworkName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        addressPrefix
      ]
    }
  }
}

resource subnet 'Microsoft.Network/virtualNetworks/subnets@2021-05-01' = {
  parent: virtualNetwork
  name: subnetName
  properties: {
    addressPrefix: subnetAddressPrefix
    privateEndpointNetworkPolicies: 'Enabled'
    privateLinkServiceNetworkPolicies: 'Enabled'
  }
}

resource publicIPAddress 'Microsoft.Network/publicIPAddresses@2021-05-01' = {
  name: publicIPAddressName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    publicIPAllocationMethod: 'Dynamic'
    publicIPAddressVersion: 'IPv4'
    dnsSettings: {
      domainNameLabel: dnsLabelPrefix
    }
    idleTimeoutInMinutes: 4
  }
}

resource vm 'Microsoft.Compute/virtualMachines@2021-11-01' = {
  name: vmName
  location: location
  properties: {
    hardwareProfile: {
      vmSize: vmSize
    }
    storageProfile: {
      osDisk: {
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: osDiskType
        }
      }
      imageReference: imageReference[ubuntuOSVersion]
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: networkInterface.id
        }
      ]
    }
    osProfile: {
      computerName: vmName
      adminUsername: adminUsername
      adminPassword: adminPasswordOrKey
      linuxConfiguration: ((authenticationType == 'password') ? null : linuxConfiguration)
    }
    securityProfile: json('null')
  }
}

output adminUsername string = adminUsername
output fqdn string = publicIPAddress.properties.dnsSettings.fqdn
output sshCommand string = 'ssh ${adminUsername}@${publicIPAddress.properties.dnsSettings.fqdn}'

```

Note

This template is based on the content of the GitHub repo [Azure Quickstart Templates](https://azure.microsoft.com/resources/templates/).

### Initiate deployment of the Bicep template

After saving the *main.bicep* file, you can proceed with a template\-based deployment. First, launch an Azure CLI session on your local computer and run `az login` to authenticate. You'll need to provide the credentials of a user with sufficient privileges to provision resources in your Azure subscription. Next, change the current directory to the one where the *main.bicep* file resides. Alternatively, you can start an Azure Cloud Shell Bash session and upload that file into your home directory within the Azure Cloud Shell environment.

Next, run the following command from an authenticated Azure CLI session to create a resource group, which will contain all resources that are part of the subsequent deployment:

```
az group create --name rg-lnx-bcp --location eastus

```

Before you proceed further, you might want to ensure that you're using the most recent version of Bicep CLI by running the following command:

```
az bicep upgrade

```

Finally, initiate deployment by running the following command:

```
az deployment group create --resource-group rg-lnx-bcp --template-file main.bicep --parameters adminUsername=azureuser

```

Note

This command includes the `--parameters` switch, which in this case sets the name of the local administrator for the Azure VM that you're deploying. Azure CLI prompts you to provide the corresponding password because the default value of the `adminPasswordOrKey` parameter isn't set.

The Azure VM should begin running shortly, typically within a few minutes. To connect to it, identify the fully qualified domain name (FQDN) associated with its network interface by reviewing the output the deployment generates. Alternatively, you can use the `shCommand` value. When prompted, provide the newly set password to authenticate when establishing an SSH connection.

In case you didn't record the Bicep deployment's output values, you can display them again by running the following command:

```
az deployment group show \
  --resource-group rg-lnx-bcp \
  --name main \
  --query properties.outputs

```

The JSON\-formatted output should resemble the following content:

```
{
  "adminUsername": {
    "type": "String",
    "value": "azureuser"
  },
  "fqdn": {
    "type": "String",
    "value": "lnx-bcp-vm-example.eastus.cloudapp.azure.com"
  },
  "sshCommand": {
    "type": "String",
    "value": "ssh azureuser@lnx-bcp-vm-example.eastus.cloudapp.azure.com"
  }
}

```

---

## Summary

In this module, you reviewed several methods for provisioning Azure VMs running Linux. You started by exploring the deployment process available in the Azure portal and identifying the most common configuration options. Next, you reviewed an example of imperative provisioning by using Azure CLI. You concluded your review with declarative deployments by using Terraform and Bicep.

The knowledge you gained will help you choose the deployment methodology that offers the optimal balance between simplicity and efficiency according to your requirements or preferences.

### Learn more

* [Quickstart: Create a Linux virtual machine in the Azure portal](/en-us/azure/virtual-machines/linux/quick-create-portal)
* [Tutorial: Create and Manage Linux VMs with the Azure CLI](/en-us/azure/virtual-machines/linux/tutorial-manage-vm)
* [Quickstart: Use Terraform to create a Linux VM](/en-us/azure/virtual-machines/linux/quick-create-terraform)
* [Quickstart: Create an Ubuntu Linux virtual machine using a Bicep file](/en-us/azure/virtual-machines/linux/quick-create-bicep)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/provision-linux-virtual-machine-in-azure/_

## Fuentes
- [Provisioning a Linux virtual machine in Microsoft Azure](https://learn.microsoft.com/en-us/training/modules/provision-linux-virtual-machine-in-azure/?WT.mc_id=api_CatalogApi)
