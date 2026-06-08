# Troubleshoot connectivity issues with virtual machines in Microsoft Azure

> Curso: Azure Support Engineer for Connectivity Specialty (wwl-azure-support-engineer-for-connectivity-specia) · Seccion: Azure Support Engineer for Connectivity Specialty
> Duracion estimada: 32 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You work as a support engineer looking after your company’s virtual machines (VMs). Some of the teams you support would like guidance on when to use Azure Bastion or just\-in\-time (JIT) to access their VMs. You want to be able to give them this guidance and show the teams how to troubleshoot any issues they have.

Azure supports connecting to VMs in multiple ways. Azure Bastion is a service that you deploy into your environment and use it to connect to your VM using only a browser. Just\-in\-time VM access is a way to restrict who and which services can connect to a VM—and for how long.

In this module, you explore why you might use Azure Bastion instead of just\-in\-time VM access to connect to your organization’s VMs. Then, you review common issues and how to troubleshoot them.

### Learning objectives

After completing this module, you’ll be able to:

* Choose between Azure Bastion or just\-in\-time VM access.
* Troubleshoot issues with Azure Bastion.
* Troubleshoot just\-in\-time VM access.

### Prerequisites

* Experience using the Azure portal
* Experience using Remote Desktop
* Knowledge of Azure Bastion
* Familiarity with server and client management concepts and tools
* Familiarity with Microsoft Azure and cloud concepts

---

## Troubleshoot issues with Azure Bastion

There are three main categories of issues you might see when troubleshooting Azure Bastion.

### Deployment

First, you go to the Azure VM where you're having trouble deploying Azure Bastion.

In the Azure portal, on the left navigation pane, select **Virtual machines**, then select the machine you're troubleshooting. Select **Connect** from the top of the pane, then select **Bastion**.

You should see the options to create an Azure Bastion Service. If you don't, check that you meet these prerequisites:

* You have the correct access to the VM—at a minimum, you need reader access to the VM, NIC, private IP address of the VM, and the virtual network.
* You have an active Azure subscription with enough credit.
* You have enough public IP address left in your subscription's quota.

Step 1 is already complete for you because you're creating the Azure Bastion Service from a VM.

For step 2, you can accept the defaults and create a new subnet named AzureBastionSubnet. The wizard creates the subnet with these attributes:

Step 3 allows you to select the tier, basic or standard. You can then create or use a public IP address to connect to the Azure Bastion Service. Finally, accept the Microsoft supplied defaults to create the service.

### Connectivity

To begin resolving connection issues between your Azure Bastion Service and a VM, check the VM is running.

The VM doesn't need to have a public IP address, but it must be in a virtual network that supports IPv4\. Currently, IPv6\-only environments aren't supported.

Azure Bastion can't work with VMs that are in an Azure Private DNS zone with **core.windows.net** or **azure.com** in the suffixes. This isn't supported because it could allow overlaps with internal endpoints. Azure Private DNS zones in national clouds are also unsupported.

If the connection to the VM is working but you can't sign in, check if it's domain\-joined. If the VM is domain\-joined, you must specify the credentials in the Azure portal using the **username@domain** format, instead of **domain\\username**. This change won't resolve the issues if the VM is Microsoft Entra joined only, as this kind of authentication isn't supported.

The AzureBastionSubnet isn't assigned an NSG by default. If your organization needs an NSG, you should ensure its configuration is correct in the Azure portal.

Inbound rules:

| Name | Port | Protocol | Source | Destination | Action |
| --- | --- | --- | --- | --- | --- |
| AllowHttpsInbound | 443 | TCP | Internet | Any | Allow |
| AllowGatewayManagerInbound | 443 | TCP | GatewayManager | Any | Allow |
| AllowAzureLoadBalancerInbound | 443 | TCP | AzureLoadBalancer | Any | Allow |
| AllowBastionHostCommunication | 8080, 5701 | Any | VirtualNetwork | VirtualNetwork | Allow |

Outbound rules:

| Name | Port | Protocol | Source | Destination | Action |
| --- | --- | --- | --- | --- | --- |
| AllowSshRdpOutbound | 22, 3389 | Any | Any | VirtualNetwork | Allow |
| AllowAzureCloudOutbound | 443 | TCP | Any | AzureCloud | Allow |
| AllowBastionCommunication | 8080, 5701 | Any | VirtualNetwork | VirtualNetwork | Allow |
| AllowGetSessionInformation | 80 | Any | Any | Internet | Allow |

### Access

If your users are having access issues, check that they have roles that grant them read access to all these resources:

* The virtual machine
* The NIC
* The Azure Bastion Service and AzureBastionSubnet
* If it's a peered network, the virtual network

If all these resources are correct and the user is still seeing a black screen when they try to connect with Azure Bastion, there's likely a network connectivity issue between the user's web browser and Azure Bastion.

---

## Exercise \- Troubleshoot connectivity issues with Azure Bastion

One of the teams you support contacts you. The team has trouble connecting to their VM using Bastion. In this exercise, you see how to troubleshoot the Azure Bastion Service.

Bastion isn't supported in the Learn sandbox environment. To view this exercise, watch the video at the end. If you'd like to follow along in your own subscription, you can use the following steps.

Important

You need your own [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) to complete the exercises in this module. If you don't have an Azure subscription, you can still read along.

### Check that Bastion is deployed

1. In the Azure portal, in the search box, type **Bastions**.
2. From the results, under **Services**, select **Bastions**.
3. You should see the Bastion service listed.

If there aren’t any Bastion services listed, create one.

### Check if there’s a private DNS zone

1. In the Azure portal, in the search box, type **private dns**.
2. From the results, under **Services**, select **Private DNS zones**.
3. You shouldn’t see any private DNS zones.
4. If there are any zones listed, check that they don’t end in **azure.com** or **core.windows.net**.

### Check if AzureBastionSubnet is using a Network Security Group correctly

1. In the Azure portal, in the search box, type **Bastions**.
2. From the results, under **Services**, select **Bastions**.
3. Select the Bastion you're troubleshooting.
4. In the top right, select the **Virtual network/subnet** link.
5. Under **Settings**, select **Subnets**, and then choose **AzureBastionSubnet**.

Note

If Azure Bastion has a **Network security group** associated with the subnet, you need to check that it has all the inbound and outbound rules created.

### Run the Connection Troubleshoot tool to check for issues

1. In the Azure portal, in the search box, type **Bastions**.
2. From the results, under **Services**, choose **Bastions**.
3. Select the Bastion you're troubleshooting.
4. Under **Monitoring**, select **Connection Troubleshoot**.
5. Under **Virtual machine**, select the VM you want to connect to.
6. Select your **Preferred IP Version**.
7. In the **Destination port**, if you want to use **RDP**, enter **3389**, if you want to use **SSH**, enter **22**.
8. Select **Check**.

If you’ve resolved all the possible connection issues, the connection troubleshoot wizard should return a status of reachable.

You can watch the following video to see all the previous steps:

---

## Module assessment

Choose the best response for each of the following questions.

### Check your knowledge

---

## Summary

As your company's support engineer, you explore the differences between Bastion and JIT VM access. You can now provide guidance to your teams and suggest which access method supports their needs.

You then reviewed common issues with both approaches and how to troubleshoot them.

If Bastion or JIT VM access wasn't available, organizations would have to make commonly used ports open to the external internet, allowing bad actors to port scan their virtual machines. Using either approach to connect to your VMs greatly reduces the attack surface that can be exploited.

Now that you completed this module, you should be able to:

* Choose between Azure Bastion or just\-in\-time VM access.
* Troubleshoot issues with Azure Bastion.
* Troubleshoot just\-in\-time VM access.

For more information about the topics discussed in this module, see:

[Troubleshoot Azure Bastion](/en-us/azure/bastion/troubleshoot)

[Understanding just\-in\-time (JIT) VM access](/en-us/azure/defender-for-cloud/just-in-time-access-overview)

[Enable and work with Bastion resource logs](/en-us/azure/bastion/diagnostic-logs)

[What is Azure Bastion?](/en-us/azure/bastion/bastion-overview)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/troubleshoot-connectivity-issues-virtual-machines-azure/_

## Fuentes
- [Troubleshoot connectivity issues with virtual machines in Microsoft Azure](https://learn.microsoft.com/en-us/training/modules/troubleshoot-connectivity-issues-virtual-machines-azure/?WT.mc_id=api_CatalogApi)
