# Troubleshoot name resolution issues in Microsoft Azure

> Curso: Azure Support Engineer for Connectivity Specialty (wwl-azure-support-engineer-for-connectivity-specia) · Seccion: Azure Support Engineer for Connectivity Specialty
> Duracion estimada: 34 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

As an Azure network support engineer, you are responsible for ensuring that computers and devices on your network stay connected. Name resolution is the process of matching the name of a computer to its network address. If a name cannot be resolved, the computer will not be visible on the network, causing a breakdown in connectivity. Name resolution may be:

* Public, using public Domain Name System (DNS) servers.
* Internal to Azure, using Azure infrastructure.
* On\-premises, using your own DNS server.

You might also adopt a hybrid approach, using a combination of either private and public DNS, or on\-premises and Azure DNS servers.

In this unit you will learn how to troubleshoot internal Azure name resolution issues and public DNS issues.

### Learning objectives

By completing this module, you'll learn how to:

* Troubleshoot built\-in Azure name resolution issues
* Troubleshoot custom Azure name resolutions issues
* Troubleshoot Azure Private Zone DNS
* Troubleshoot Public DNS issues
* Review the Azure DNS logs

### Prerequisites

* Demonstrate an understanding of the OSI model
* Demonstrate an understanding of Azure CLI
* Demonstrate an understanding of PowerShell
* Know how to run Cloud Shell to run commands

---

## Troubleshoot name resolution issues

Name resolution in Azure is done by one of three methods:

* Azure built\-in name resolution
* Azure custom name resolution
* Azure DNS private zones

In this unit you will learn how to troubleshoot each of these methods.

### 2\.1 Troubleshoot built\-in Azure name resolution

Built\-in Azure name resolution provides basic authoritative Domain Name System (DNS) capabilities. DNS names and records are managed by Azure. Built\-in Azure name resolution does not allow you to control the DNS names or the life cycle of DNS records.

Azure built\-in name resolution works with public DNS names and provides internal name resolution for VMs and role instances within the same virtual network or cloud service.

Built\-in Azure name resolution has some limitations:

* The Azure\-created DNS suffix cannot be modified.
* DNS lookup is scoped to a virtual network. DNS names created for one virtual network can't be resolved from other virtual networks.
* You cannot manually register your own records.
* WINS and NetBIOS are not supported. You cannot see your VMs in Windows Explorer.
* Host names must be DNS\-compatible. Names must use only 0\-9, a\-z, and '\-', and cannot start or end with a '\-'.
* DNS query traffic is throttled for each virtual machine (VM). Throttling shouldn't impact most applications. If request throttling is observed, ensure that client\-side caching is enabled.
* Only VMs in the first 180 cloud services are registered for each virtual network in a classic deployment model. This limit does not apply to virtual networks in Azure Resource Manager.
* The Azure DNS IP address is 168\.63\.129\.16\. This is a static IP address, is used in all regions and all national clouds and will not change.
* Azure Dynamic Host Configuration Protocol (DHCP) provides an internal DNS suffix (.internal.cloudapp.net) to each VM. This suffix enables host name resolution because the host name records are in the internal.cloudapp.net zone.

### 2\.2 Troubleshoot Domain Name System private zones

Azure Private DNS allows you to manage and resolve domain names in a virtual network without the need to add a custom DNS solution. You can use custom domain names, rather than the Azure\-provided names.

DNS resolution using a private DNS zone works only from virtual networks that are linked to it. These private DNS zones records can be resolved from the internet, but the private IP address is not routable via the Internet.

You can link a private DNS zone to one or more virtual networks by creating [virtual network links](/en-us/azure/dns/private-dns-virtual-network-links). You can also enable the [autoregistration](/en-us/azure/dns/private-dns-autoregistration) feature to automatically manage the life cycle of the DNS records for the virtual machines that get deployed in a virtual network. With autoregistration enabled, Azure DNS will update the zone record whenever a virtual machine gets created, changes its' IP address, or gets deleted.

Note

A Virtual Network can only have autoregistration enabled on one Private DNS Zone link. If you try to link two private DNS zones to the same VNet, only one of the links will be enabled for autoregistration.

There are limits on how many private DNS zones you can create, how many records sets, and records per record set.

Single\-labelled private DNS zones aren't supported. Your private DNS zone must have two or more labels. For example, contoso.com has two labels separated by a dot. A private DNS zone can have a maximum of 34 labels.

You can't create zone delegations (NS records) in a private DNS zone. If you intend to use a child domain, you can directly create the domain as a private DNS zone. Then you can link it to the virtual network without setting up a nameserver delegation from the parent zone.

To create a Private DNS zone:

1. In the Azure portal, **type private dns zones** in the search text box and press **Enter**. The **Private DNS zones** blade is displayed.
2. Select **Create**. The **Create Private DNS** zone blade is displayed.
3. Type or select the following:

	1. Subscription
	2. Resource group
	3. Name – this must be unique within the Resource group.
	4. Resource group location
4. Select **Review \+ Create**.
5. Select **Create**.

To troubleshoot issues relating to DNS zones:

1. Review the Azure DNS audit logs.
2. Check that each DNS zone name is unique within its resource group.
3. Do not create zone names that could affect the DNS resolution of Microsoft services, such as azure.com, and the like.
4. Do not use a .local domain for your private DNS zone. Not all operating systems support this.
5. Check you have not reached the maximum number of zones for your subscription. If so, you will see the error message "You have reached or exceeded the maximum number of zones in subscription {subscription ID}." Either use a different Azure subscription, delete some zones, or contact Azure Support to raise your subscription limit.
6. "The zone '{zone name}' is not available" indicates that Azure DNS is unable to allocate name servers for this DNS zone. Rename the zone or contact Azure support to allocate name servers for you.

To troubleshoot issues related to DNS records:

1. The record set already exists. Record set names must be unique within the zone.
2. CNAME records must not be created at the apex.
3. CNAME record sets cannot have the same name as other record sets.
4. Apex records consist of the '@' character.
5. The maximum number of records that can be created is shown in the Azure portal, under the 'Properties' for the zone. If you've reached this limit, then either delete some record sets or contact Azure Support to raise your record limit for this zone.

Note

Apex records are records added at the root of the zone.

To troubleshoot resolving DNS records:

1. Check that the fully qualified name, zone name, and record type are correct.
2. Check that no DNS records have the same name, even if they are of different types.
3. Check that the DNS records resolve correctly on the Azure DNS name servers.
4. Check name resolution with a service such as **[digwebinterface](https://digwebinterface.com/)**. This tests the current state of the name servers by removing proxy servers and cached results.
5. Check that the name servers are correct for your DNS zone, as shown in the Azure portal.
6. Check that the DNS domain name has been correctly [delegated to Azure DNS](/en-us/azure/dns/dns-domain-delegation). Use nslookup to validate that the zone is delegated to in\-built Azure DNS.

Note

If your environment uses a hybrid approach and uses both private zone DNS and public zone, records in private zone DNS will be resolved first.

To troubleshoot resolving DNS records:

1. Check that the fully qualified name, zone name, and record type is correct.
2. Check that no DNS records have the same name, even if they are of different types.
3. Check that the DNS records resolve correctly on the Azure DNS name servers.
4. Check name resolution with a service such as [digwebinterface](https://digwebinterface.com/). This removes proxy servers and cached results, and only tests the current state of the name servers.
5. Check that the name servers are correct for your DNS zone, as shown in the Azure portal.

Azure Private DNS zones have the following limitations:

* If automatic registration of VM DNS is enabled, only one private zone can be linked to a virtual network. You can however link multiple virtual networks to a single DNS zone.
* Reverse DNS works only for private IP space in the linked virtual network.
* Reverse DNS for a private IP address in linked virtual network will return internal.cloudapp.net as the default suffix for the virtual machine. For virtual networks that are linked to a private zone with autoregistration enabled, reverse DNS for a private IP address returns two fully qualified domain names (FQDNs): one with default the suffix internal.cloudapp.net and another with the private zone suffix.
* Conditional forwarding isn't currently natively supported. To enable resolution between Azure and on\-premises networks, see [Name resolution for VMs and role instances.](/en-us/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances)

### 2\.3 Troubleshoot custom Domain Name System configuration issues

As well as Azure in\-built DNS, you also have the option to configure a custom DNS server. For example, you might want to integrate with on\-premises Active Directory or resolve names between VNets.

To use Azure custom DNS, you must add a list of IP addresses that point to DNS servers. This list will be distributed to any devices in the virtual network that were using the Azure DNS server.

There are some limitations with Azure custom DNS:

* You cannot register a public domain name using Azure custom DNS.
* DNSSEC is not enabled.
* You cannot do zone transfers.

Note

Updating from in\-built DNS (Inherit from virtual network) to custom DNS will restart all affected VMs.

In DNS settings, you can choose whether to inherit DNS settings from the virtual network or use custom DNS. Check that you have saved any change from Azure in\-built DNS to custom DNS, otherwise, the changes will not persist.

To test whether custom DNS is working, use the PowerShell command:

```
test-netconnection -computername -port  

```

To check your custom DNS is using the correct DNS server, from a command prompt type:

```
Ipconfig /all

```

---

## Exercise: Name resolution issues

Important

You need your own [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) to complete the exercises in this module. If you don't have an Azure subscription, you can still view the demonstration video at the bottom of this page.

Sign in to the [Azure portal](https://portal.azure.com/learn.docs.microsoft.com?azure-portal=true) using the same account you used to activate the sandbox.

If you have not already run the script in unit 2, please do so now so you can follow the exercise below.

You work for Contoso as a network engineer, and users are complaining that they cannot access VM1 or VM2\. You have configured two Azure virtual networks: VNet1 and VNet2\. They are connected with peering.

| **Virtual network** | **IPv4 network address** | **Subnet** | **IPv4 network address** |
| --- | --- | --- | --- |
| VNet1 | 10\.1\.0\.0/16 | Subnet1 | 10\.1\.1\.0/24 |
|  |  | Subnet2 | 10\.1\.2\.0/24 |
| VNet2 | 10\.2\.0\.0/16 | Default | 10\.2\.0\.0/24 |

| **Virtual machine** | **Operating system** | **VNet and subnet** | **DNS domain** |
| --- | --- | --- | --- |
| VM1 | Windows Server 2019 | VNet1, Subnet1 | contoso.com |
| VM2 | Windows Server 2019 | VNet1, Subnet2 | contoso.com |
| VM3 | Windows Server 2019 | VNet2, default | contoso.com |

### Diagnosis

Use Nslookup on VM1 and VM2 and check you get the following results:

* vm1\.contoso.com – success
* vm2\.contoso.com – success
* vm3\.contoso.com – can't find

Nslookup on VM3 gives these results:

* vm1\.contoso.com – can't find
* vm2\.contoso.com – can't find
* vm3\.contoso.com – can't find

### Diagnosis

#### Examine the Internet Protocol configuration of the Virtual Machines

Connect to each VM using Remote Desktop. Open a command prompt window and type: ipconfig /all

The IP addresses are:

* VM1 \= 10\.1\.1\.4
* VM2 \= 10\.1\.2\.4
* VM3 \= 10\.2\.0\.4

The DNS server address is 192\.168\.016, which is the wire server.

#### Test network connectivity

Use **ping** to test network connectivity between the three virtual machines.

All three VMs are able to ping each other, so network connectivity is good at the IP level (OSI Layer 3\).

#### Examine the Azure resource group

There are two virtual networks (VNets) called VNet1 and VNet2\.

There is a private DNS zone, which is contoso.com.

The private DNS zone has vm1 and vm2 automatically registered, but vm3 does not appear.

Go to **Settings** \> **Virtual network links**. We see that the private DNS zone is linked to VNet1, but not to VNet2\.

### Resolution

#### Link the private Domain Name System zone to Virtual Network 2

Navigate to the private DNS zone (contoso.com) and select the Virtual network links page. Add a new link.

* Link name: vnet2\_dns
* \[ ] I know the resource ID of virtual network – leave unchecked
* Subscription: \<the name of your subscription\>
* Virtual network: VNet2
* Configuration: \[X] Enable auto registration

After you select OK, it may take a few minutes for the link to be created. Select Refresh occasionally to see the latest status. Wait until the link status says Completed.

#### Inspect the Domain Name System name table

Navigate to the Overview page and inspect the DNS name table.

VM1, VM2, and VM3 should appear. You may need to wait a short while for VM3 to appear. Select Refresh if necessary.

Nslookup on VM1 and VM2 should resolve vm3\.contoso.com.

Tip

If VM3 does not appear after several minutes, try restarting the VM.

Optionally, you can test pinging the VMs, using their DNS names.

* vm1\.contoso.com
* vm2\.contoso.com
* vm3\.contoso.com

In this demonstration you will see how to proactively troubleshoot Conditional Access policies using the What if tool in the Azure portal:

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary

In this module you have learned how to troubleshoot Azure in\-built name resolution, custom name resolution, and Azure private zone. You have learned how to troubleshoot public DNS, and domain delegation.

Now that you have completed this module you know how to troubleshoot:

* Troubleshoot built\-in Azure name resolution issues
* Troubleshoot custom Azure name resolutions issues
* Troubleshoot Azure Private Zone DNS
* Public DNS issues
* Reviewing the Azure DNS logs

### Resources

For more information about the articles discussed in this module, see:

#### Azure Built\-in Name resolution

[Azure DNS troubleshooting guide](/en-us/azure/dns/dns-troubleshoot)

[Name resolution for resources in Azure virtual networks](/en-us/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances)

[Tutorial: Host your domain in Azure DNS](/en-us/azure/dns/dns-delegate-domain-azure-dns)

[Create a DNS zone](/en-us/azure/dns/dns-getstarted-powershell)

#### Azure DNS Private Zones

[DNS Analytics solution in Azure Monitor](/en-us/azure/azure-monitor/insights/dns-analytics)

[Quickstart: Create an Azure private DNS zone using the Azure portal](/en-us/azure/dns/private-dns-getstarted-portal)

[Quickstart: Create an Azure DNS zone and record using Azure PowerShell](/en-us/azure/dns/dns-getstarted-powershell)

[Troubleshooting DNS Servers](/en-us/windows-server/networking/dns/troubleshoot/troubleshoot-dns-server)

[Azure DNS delegation overview](/en-us/azure/dns/dns-domain-delegation)

[Azure subscription limits and quotas](/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits)

#### Custom DNS

[Tutorial \- Create custom Azure DNS records for a web app](/en-us/azure/dns/dns-web-sites-custom-domain)

[Using dynamic DNS to register hostnames in Azure](/en-us/azure/virtual-network/virtual-networks-name-resolution-ddns)

#### Log Analytics

[Install Log Analytics agent on Windows computers](/en-us/azure/azure-monitor/agents/agent-windows)

[Connect Operations Manager to Azure Monitor](/en-us/azure/azure-monitor/agents/om-agents)

[Microsoft Azure Marketplace](https://azuremarketplace.microsoft.com/marketplace/apps/Microsoft.DnsAnalyticsOMS?tab=Overview)

[Monitoring solutions in Azure Monitor](/en-us/azure/azure-monitor/insights/solutions?tabs=portal)

[Gather insights about your DNS infrastructure with the DNS Analytics Preview solution](/en-us/azure/azure-monitor/insights/dns-analytics)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/name-resolution-issues/_

## Fuentes
- [Troubleshoot name resolution issues in Microsoft Azure](https://learn.microsoft.com/en-us/training/modules/name-resolution-issues/?WT.mc_id=api_CatalogApi)
