# Introduction to Azure Virtual Networks

> Curso: AZ-700 Design and Implement Microsoft Azure Network Solutions (wwl-designing-implementing-microsoft-azure-network) · Seccion: AZ-700 Design and Implement Microsoft Azure Network Solutions
> Duracion estimada: 70 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Imagine yourself in the role of a network engineer at an organization that is in the process of migrating infrastructure and applications to Azure. As the network engineer you need users to be able to access resources such as file storage, databases, and applications on\-premises and in Azure. Azure virtual networks enable you to provide secure, reliable access to your Azure infrastructure and resources, and on\-premises resources.

### Learning objectives

In this module, you will:

* Explore virtual networks and subnets.
* Configure public IP services.
* Explore domain name resolution.
* Explore virtual network peering.
* Explore virtual network routing.
* Learn about Azure Virtual Network NAT.

### Prerequisites

* Experience with networking concepts, such as IP addressing, Domain Name System (DNS), and routing.
* Experience with network connectivity methods, such as VPN or WAN.
* Experience with the Azure portal and Azure PowerShell.

---

## Configure public IP services

Public networks like the Internet communicate by using public IP addresses. Private networks like your Azure Virtual Network use private IP addresses, which aren't routable on public networks. To support a network that exists both in Azure and on\-premises, you must configure IP addressing for both types of networks.

Public IP addresses enable Internet resources to communicate with Azure resources and enable Azure resources to communicate outbound with Internet and public\-facing Azure services. A public IP address in Azure is dedicated to a specific resource. A resource without a public IP assigned can communicate outbound through network address translation services, where Azure dynamically assigns an available IP address that isn't dedicated to the resource.

As an example, public resources like web servers must be accessible from the internet. You want to ensure that you plan IP addresses that support these requirements.

### Use dynamic and static public IP addresses

In Azure Resource Manager, a [public IP](/en-us/azure/virtual-network/virtual-network-public-ip-address) address is a resource that has its own properties. Some of the resources you can associate a public IP address resource with:

* Virtual machine network interfaces
* Virtual machine scale sets
* Public Load Balancers
* Virtual Network Gateways (VPN/ER)
* NAT gateways
* Application Gateways
* Azure Firewall
* Bastion Host
* Route Server

Public IP addresses are created with an IPv4 or IPv6 address, which can be either static or dynamic.

**A dynamic public IP address** is an assigned address that can change over the lifespan of the Azure resource. The dynamic IP address is allocated when you create or start a virtual machine (VM). The IP address is released when you stop or delete the VM. In each Azure region, public IP addresses are assigned from a unique pool of addresses. The default allocation method is dynamic.

**A static public IP address** is an assigned address that is fixed over the lifespan of the Azure resource. To ensure that the IP address for the resource remains the same, set the allocation method explicitly to static. In this case, an IP address is assigned immediately. The IP address is released only when you delete the resource or change the IP allocation method to dynamic.

### Choose the appropriate SKU for a public IP address

Important

On September 30, 2025, Basic SKU public IPs were retired. If you're currently using Basic SKU public IPs, upgrade to Standard SKU public IPs as soon as possible. Basic IPs remain operational post\-retirement but are unsupported and not covered by SLA guarantees. For guidance on upgrading, visit [Upgrading a basic public IP address to Standard SKU](/en-us/azure/virtual-network/ip-services/public-ip-basic-upgrade-guidance).

| Public IP address | **Standard SKU** |
| --- | --- |
| Allocation method | Static |
| Idle time\-out | Have an adjustable inbound originated flow idle time out of 4\-30 minutes, with a default of 4 minutes, and fixed outbound originated flow idle time out of 4 minutes. |
| Security | Secure by default model and be closed to inbound traffic when used as a frontend. Allow traffic with network security group (NSG) is required (for example, on the NIC of a virtual machine with a Standard SKU Public IP attached). |
| Availability zones | Supported. Standard IPs can be nonzonal, zonal, or zone\-redundant. Zone redundant IPs can only be created in regions where there are three availability zones. |
| Routing preference | Supported to enable more granular control of how traffic is routed between Azure and the Internet. |
| Global tier | Supported via cross\-region load balancers. |

Choose the best response for each question.

### Check your knowledge

---

## Exercise: Design and implement a virtual network in Azure

### Lab scenario

Contoso Ltd, a fictitious organization, is in the process of migrating infrastructure and applications to Azure. As network engineer, you plan and implement three virtual networks and subnets to support resources in those virtual networks.

### Architecture diagram

### Job skills

* Create the **Contoso** resource group.
* Create the **CoreServicesVnet** virtual network and subnets.
* Create the **ManufacturingVnet** virtual network and subnets.
* Create the **ResearchVnet** virtual network and subnets.
* Verify the creation of the virtual networks and subnets.

Important

Estimated time: 30 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Implement virtual network traffic routing

Azure automatically creates a route table for each subnet within an Azure virtual network. The route table has the default system routes and any user defined routes you require.

### System routes

Azure automatically creates system routes and assigns the routes to each subnet in a virtual network. You can't create or remove system routes, but you can override some system routes with custom routes. Azure creates default system routes for each subnet, and adds other optional default routes to specific subnets, or every subnet, when you use specific Azure capabilities.

#### Default system routes

Whenever a virtual network is created, Azure automatically creates the following default system routes for each subnet within the virtual network. Each system route contains an address prefix and next hop type.

| **Source** | **Address prefixes** | **Next hop type** |
| --- | --- | --- |
| Default | Unique to the virtual network | Virtual network |
| Default | 0\.0\.0\.0/0 | Internet |
| Default | 10\.0\.0\.0/8 | None |
| Default | 172\.16\.0\.0/12 | None |
| Default | 192\.168\.0\.0/16 | None |
| Default | 100\.64\.0\.0/10 | None |

In routing terms, a hop is a waypoint on the overall route. Therefore, the next hop is the next waypoint that the traffic is directed to on its journey to its ultimate destination. The next hop types are defined as follows:

* **Virtual network:** Routes traffic between address ranges within the address space of a virtual network. Azure creates a route with an address prefix that corresponds to each address range defined within the address space of a virtual network. Azure automatically routes traffic between subnets using the routes created for each address range.
* **Internet:** Routes traffic specified by the address prefix to the Internet. The system default route specifies the 0\.0\.0\.0/0 address prefix. Azure routes traffic for any address not specified by an address range within a virtual network to the Internet, unless the destination address is for an Azure service. Azure routes any traffic destined for its service directly to the service over the backbone network, rather than routing the traffic to the Internet. You can override Azure's default system route for the 0\.0\.0\.0/0 address prefix with a custom route.
* **None:** Traffic routed to the None next hop type is dropped, rather than routed outside the subnet.

#### Optional default system routes

Azure adds default system routes for any Azure capabilities that you enable. Depending on the capability, Azure adds optional default routes to either specific subnets within the virtual network, or to all subnets within a virtual network.

| **Source** | **Address prefixes** | **Next hop type** | **Subnet within virtual network that route is added to** |
| --- | --- | --- | --- |
| Default | Unique to the virtual network, for example: 10\.1\.0\.0/16 | Virtual network peering | All |
| Virtual network gateway | Prefixes advertised from on\-premises via BGP, or configured in the local network gateway. | All |  |
| Default | Multiple | VirtualNetworkServiceEndpoint | Only the subnet a service endpoint is enabled for. |

* **Virtual network (VNet) peering**: When you create a virtual network peering between two virtual networks, a route is added for each address range within the address space of each virtual network.
* **Virtual network gateway:** When you add a virtual network gateway to a virtual network, Azure adds one or more routes with Virtual network gateway as the next hop type. The source is listed as virtual network gateway because the gateway adds the routes to the subnet.
* **VirtualNetworkServiceEndpoint:** Azure adds the public IP addresses for certain services to the route table when you enable a service endpoint to the service. Service endpoints are enabled for individual subnets within a virtual network, so the route is only added to the route table of a subnet a service endpoint is enabled for. The public IP addresses of Azure services change periodically, and Azure manages the updates to the routing tables when necessary.

### User defined routes

You can override the default routes that Azure creates with [user\-defined routes (UDR)](/en-us/azure/virtual-network/virtual-networks-udr-overview). This technique can be useful when you want to ensure that traffic between two subnets passes through a firewall appliance. These custom routes override Azure's default system routes. In Azure, each subnet can have zero or one associated route table. When you create a route table and associate it to a subnet, the routes within it are combined with, or override, the default routes Azure adds to a subnet.

You can specify the following next hop types when creating a user\-defined route:

* **Virtual appliance:** A virtual appliance is a virtual machine that typically runs a network application, such as a firewall. When you create a route with the virtual appliance hop type, you also specify a next hop IP address.
* **Virtual network gateway**: Specify when you want traffic destined for specific address prefixes routed to a virtual network gateway. The virtual network gateway must be created with type **VPN**.
* **None**: Specify when you want to drop traffic to an address prefix, rather than forwarding the traffic to a destination.
* **Virtual network**: Specify when you want to override the default routing within a virtual network.
* **Internet:** Specify when you want to explicitly route traffic destined to an address prefix to the Internet.

### Consider Azure Route Server

[Azure Route Server](/en-us/azure/route-server/quickstart-configure-route-server-portal) simplifies dynamic routing between your network virtual appliance (NVA) and your virtual network. Azure Route Server is a fully managed service and is configured with high availability. Azure Route Server simplifies configuration, management, and deployment of your NVA in your virtual network.

* You no longer need to manually update the routing table on your NVA whenever your virtual network addresses are updated.
* You no longer need to update user defined routes manually whenever your NVA announces new routes or withdraws old ones.
* You can peer multiple instances of your NVA with Azure Route Server.
* The interface between NVA and Azure Route Server is based on a common standard protocol. As long as your NVA supports BGP, you can peer it with Azure Route Server.
* You can deploy Azure Route Server in any of your new or existing virtual networks.

### Troubleshoot with effective routes

Imagine your attempts to connect to a specific virtual machine (VM) in your Azure virtual network consistently fail. You can diagnose a routing problem by viewing the effective routes for a virtual machine network interface. You can view the [effective routes](/en-us/azure/virtual-network/diagnose-network-routing-problem#diagnose-using-azure-portal) for each network interface by using the Azure portal.

### Check your knowledge

---

## Summary

As your organization moves to Azure, you must design a secure virtual networking environment that provides connectivity and name resolution for both virtual and on\-premises resources. Users must be able to access the resources they need smoothly and securely, regardless of where they're accessing the network from. This module provided an overview of some of the most crucial aspects of designing and planning an Azure virtual network.

**The main takeaways from this module are:**

* Azure virtual networks enable resources in Azure to securely communicate with each other, the internet, and on\-premises networks.
* A subnet is a range of IP address in a virtual network. Each subnet must have a unique address range.
* Public networks like the Internet communicate by using public IP addresses. Private networks like your Azure Virtual Network use private IP addresses.
* A dynamic public IP address can change over the lifespan of the Azure resource. A static public IP address doesn't change over the lifespan of the Azure resource.
* Azure provides both public and private DNS resolution.
* Virtual network peering enables you to seamlessly connect two Azure virtual networks. Peering can be either global or regional.
* Azure automatically creates system routes and assigns the routes to each subnet in a virtual network. Each route contains an address prefix and next hop type.
* You can create custom, or user\-defined(static), routes. To troubleshoot routing issues, you can view the effective routes for each network interface.
* NAT enables you to share a single public IPv4 address among multiple internal resources.

### Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

* What are the basic steps to configure a virtual network with subnets? What are the most important considerations for the design?
* What is the difference between Azure public and private DNS resolution? Provide usage examples.
* What is Azure virtual network peering? What usage cases are appropriate for this feature?
* What is the difference between Azure system routes and user\-defined routes? Provide usage cases for each route type.

### Learn more with self\-paced training

* [Configure virtual networks](/en-us/training/modules/configure-virtual-networks/). Learn to configure virtual networks and subnets, including IP addressing.
* [Manage and control traffic flow in your Azure deployment with routes](/en-us/training/modules/control-network-traffic-flow-with-routes/). Learn how to control Azure virtual network traffic by implementing custom routes.
* [Configure Azure Virtual Network peering](/en-us/training/modules/configure-vnet-peering/). Learn to configure an Azure Virtual Network peering connection and address transit and connectivity concerns.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-virtual-networks/_

## Fuentes
- [Introduction to Azure Virtual Networks](https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-virtual-networks/?WT.mc_id=api_CatalogApi)
