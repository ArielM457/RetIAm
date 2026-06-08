# Design and implement hybrid networking

> Curso: AZ-700 Design and Implement Microsoft Azure Network Solutions (wwl-designing-implementing-microsoft-azure-network) · Seccion: AZ-700 Design and Implement Microsoft Azure Network Solutions
> Duracion estimada: 47 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Your organization is migrating to Azure and evaluating a global transit network architecture. This network must support a growing number of distributed offices. As the network engineer, you need to design and implement a hybrid connectivity solution.

Network architects and engineers ensure that communication between the on\-premises environment and Azure workloads is both secure and reliable.

### Learning objectives

In this module, you learn:

* Design and implement a site\-to\-site VPN connection.
* Design and implement a point\-to\-site VPN connection.
* Design and implement authentication for point\-to\-site VPN connections.
* Design and implement Azure Virtual WAN.

### Prerequisites

* You should have experience with networking concepts, such as IP addressing, Domain Name System (DNS), and routing.
* You should have experience with network connectivity methods, such as VPN or WAN.
* You should have experience with the Azure portal and Azure PowerShell.

---

## Exercise: Create and configure a virtual network gateway

### Lab scenario

In this exercise, you configure a virtual network gateway to connect the Contoso Core Services VNet and the Manufacturing VNet.

### Architecture diagram

**Important**: Look closely at this design. Did you notice the CoreServicesSubnet overlaps with the GatewaySubnet? As a best practice, these subnets should be segregated to avoid potential connectivity issues.

### Job skills

* Create the CoreServicesVnet and ManufacturingVnet.
* Create the CoreServicesTestVM.
* Create the ManufacturingTestVM.
* Connect to the test VMs using RDP.
* Test the connection between the VMs.
* Create the CoreServicesVnet Gateway.
* Create the ManufacturingVnet Gateway.
* Connect the CoreServicesVnet to ManufacturingVnet.
* Connect the ManufacturingVnet to CoreServicesVnet
* Verify that the connections are provisioned.
* Test the connection between the VMs.

Important

Estimated time: 70 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Connect networks with Site\-to\-site VPN connections

A [site\-to\-site (S2S) VPN gateway](/en-us/azure/vpn-gateway/design#s2smulti) lets you create a secure connection to your virtual network from another virtual network or a physical network.

The following diagram illustrates how you would connect an on\-premises network to the Azure platform. The internet connection uses an IPsec VPN tunnel.

### In the diagram:

* The on\-premises network represents your on\-premises Active Directory and any data or resources.
* The gateway is responsible for sending encrypted traffic to a virtual IP address when it uses a public connection.
* The Azure virtual network holds all your cloud applications and any Azure VPN gateway components.
* An Azure VPN gateway provides the encrypted link between the Azure virtual network and your on\-premises network. An Azure VPN gateway is made up of these elements:

	+ Virtual network gateway
	+ Local network gateway
	+ Connection
	+ Gateway subnet
* An internal load balancer, located in the front end, routes cloud traffic to the correct cloud\-based application or resource.

Using this architecture offers several benefits, including:

* Simplifying configuration and maintenance.
* Encrypting data and traffic between the on\-premises gateway and the Azure gateway.
* Allowing for future network requirements.

This architecture isn't applicable in all situations because it uses an existing internet connection as the link between the two gateway points. Bandwidth constraints can cause latency issues that result from reuse of the existing infrastructure.

### Check your knowledge

---

## Connect devices to networks with Point\-to\-site VPN connections

A [Point\-to\-Site (P2S) VPN gateway](/en-us/azure/vpn-gateway/point-to-site-about) connection lets you create a secure connection to your virtual network from an individual client computer.

A P2S connection is established by starting it from the client computer. This solution is useful for telecommuters who want to connect to Azure VNets from a remote location, such as from home or a conference. P2S VPN is also a useful solution to use instead of S2S VPN when you have only a few clients that need to connect to a VNet.

#### Point\-to\-site protocols

Point\-to\-site VPN can use one of the following protocols:

* OpenVPN® Protocol, an SSL/TLS based VPN protocol. A TLS VPN solution can penetrate firewalls, since most firewalls open TCP port 443 outbound, which TLS uses. OpenVPN can be used to connect from Android, iOS (versions 11\.0 and above), Windows, Linux, and Mac devices (macOS versions 10\.13 and above).
* Secure Socket Tunneling Protocol (SSTP), a proprietary TLS\-based VPN protocol. A TLS VPN solution can penetrate firewalls, since most firewalls open TCP port 443 outbound, which TLS uses. SSTP is only supported on Windows devices. Azure supports all versions of Windows that have SSTP (Windows 7 and later).
* IKEv2 VPN, a standards\-based IPsec VPN solution. IKEv2 VPN can be used to connect from Mac devices (macOS versions 10\.11 and above).

#### Point\-to\-site authentication methods

The user must be authenticated before Azure accepts a P2S VPN connection. The two most common authentication methods are: Entra ID authentication and on\-premises Active Directory Domain Services authentication.

**Authenticate using native Microsoft Entra ID authentication**

Native authentication allows users to connect to Azure using their Microsoft Entra ID credentials. Native authentication is only supported for OpenVPN protocol and Windows and requires the use of the Azure VPN Client. With this authentication, you can use conditional access and multifactor authentication (MFA) features for VPN.

**Authenticate using Active Directory Domain Services**

This authentication is a popular option because it allows users to connect to Azure using their organization domain credentials. It requires a RADIUS server that integrates with the server. Organizations can also use their existing RADIUS deployment.

The RADIUS server is deployed either on\-premises or in your Azure VNet. During authentication, the Azure VPN Gateway passes authentication messages back and forth between the RADIUS server and the connecting device. Thus, the Gateway must be able to communicate with the RADIUS server. If the RADIUS server is present on\-premises, then a VPN S2S connection from Azure to the on\-premises site is required for reachability.

---

## Connect remote resources by using Azure Virtual WANs

Today’s workforce is more distributed than ever before. Organizations are exploring options that enable their employees, partners, and customers to connect to the resources they need from wherever they are. It’s not unusual for organizations to operate across national/regional boundaries, and across time zones.

[Azure Virtual WAN](/en-us/azure/virtual-wan/virtual-wan-about) is a networking service that brings many networking, security, and routing functionalities together to provide a single operational interface.

#### Azure Virtual WAN features

Some of the main features include:

* Branch connectivity (via connectivity automation from Virtual WAN Partner devices such as SD\-WAN or VPN CPE).
* Site\-to\-site VPN connectivity.
* Remote user VPN connectivity (point\-to\-site).
* Private connectivity (ExpressRoute).
* Intra\-cloud connectivity (transitive connectivity for virtual networks).
* VPN ExpressRoute inter\-connectivity.
* Routing, Azure Firewall, and encryption for private connectivity.

This diagram shows an organization with two Virtual WAN hubs connecting the spokes. VNets, Site\-to\-site and point\-to\-site VPNs, SD WANs, and ExpressRoute connectivity are all supported.

To configure an end\-to\-end virtual WAN, you create:

* **Virtual WAN**. This resource represents a virtual overlay of your Azure network and is a collection of multiple resources. It contains links to all your virtual hubs that you would like to have within the virtual WAN. Virtual WANs are isolated from each other and can't contain a common hub.
* **Hub**. A virtual hub is a Microsoft\-managed virtual network. The hub contains various service endpoints to enable connectivity.
* **Hub virtual network connection**. The hub virtual network connection resource is used to connect the hub seamlessly to your virtual network. One virtual network can be connected to only one virtual hub.
* **Hub\-to\-hub connection**. Hubs are all connected to each other in a virtual WAN.
* **Hub route table**. You can create a virtual hub route and apply the route to the virtual hub route table. You can apply multiple routes to the virtual hub route table.
* **Site (optional)**. This resource is used for site\-to\-site connections only.

#### Choose a Virtual WAN SKU

The Virtual WAN SKUs are: Basic and Standard. This table shows the available configurations for each type.

| **Virtual WAN type** | **Hub type** | **Available configurations** |
| --- | --- | --- |
| Basic | Basic | Site\-to\-site VPN only |
| Standard | Standard | ExpressRouteUser VPN (P2S)VPN (site\-to\-site)Inter\-hub and VNet\-to\-VNet transiting through the virtual hubAzure FirewallNVA in a virtual WAN |

### Check your knowledge

---

## Exercise: Create a Virtual WAN by using the Azure portal

### Lab scenario

In this exercise, you create a Virtual WAN for Contoso.

### Architecture diagram

### Job skills

* Create a Virtual WAN.
* Create a virtual hub by using Azure portal.
* Connect a virtual network to the virtual hub.

Important

Estimated time: 65 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Summary

In this module, you learned about the Azure VPN gateway. The Azure VPN gateway enables secure, encrypted connections between an Azure virtual network and an on\-premises network. You also learned about the two types of VPN gateways: policy\-based and route\-based. Site\-to\-Site (S2S) and Point\-to\-Site (P2S) VPN gateways, their benefits, and potential limitations were described. Lastly, the module introduced Azure Virtual WAN, a networking service that provides various networking, security, and routing functionalities.

**The main takeaways from this module are:**

* VPN gateway planning considers throughput, public IP address availability, VPN device compatibility, VPN gateway type, and Azure VPN Gateway SKU.
* Most VPN gateways are route\-based. Route\-based gateways use dynamic routing.
* There are several high availability options for VPN connections. The default option is active\-standby but you can also configure active\-active.
* A site\-to\-site VPN gateway uses IPsec tunnels to secure connections between virtual and physical networks.
* A point\-to\-site VPN gateway creates a secure connection to your virtual network from an individual client computer. Several authentication methods are available including Microsoft Entra ID and Active Directory Domain Services.
* Network virtual appliances support connecting many different technologies. You can deploy partner solutions from the Microsoft Azure Marketplace.

#### Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

* What is an Azure VPN gateway? Provide key features, benefits, and usage cases.
* Compare Azure site\-to\-site and point\-to\-site connections. Provide usage examples.
* What is an Azure virtual WAN? Provide usage cases and how it works.

#### Learn more with documentation and online training

* [Introduction to Azure VPN Gateway training](/en-us/training/modules/intro-to-azure-vpn-gateway/). This module describes what Azure VPN Gateway does, how it works, and when you should choose to use Azure VPN Gateway as a solution to meet your organization's needs.
* [VPN Gateway documentation](/en-us/azure/vpn-gateway/). Learn how to configure, create, and manage an Azure VPN gateway. Create encrypted cross\-premises connections to your virtual network from on\-premises locations, or create encrypted connections between VNets.
* [Virtual WAN documentation](/en-us/azure/virtual-wan/). Learn how to configure, create, and manage an Azure Virtual WAN. Azure Virtual WAN is a networking service that brings many networking, security, and routing functionalities together to provide a single operational interface.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/design-implement-hybrid-networking/_

## Fuentes
- [Design and implement hybrid networking](https://learn.microsoft.com/en-us/training/modules/design-implement-hybrid-networking/?WT.mc_id=api_CatalogApi)
