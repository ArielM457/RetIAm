# Design and implement private access to Azure Services

> Curso: AZ-700 Design and Implement Microsoft Azure Network Solutions (wwl-designing-implementing-microsoft-azure-network) · Seccion: AZ-700 Design and Implement Microsoft Azure Network Solutions
> Duracion estimada: 42 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Imagine you're a cloud architect for a large organization that is migrating its existing applications to Azure. You need to ensure that these applications can securely access specific Azure services without exposing them to the public internet. Additionally, you want to provide private access from your Azure virtual network to Azure PaaS services and Microsoft Partner services. You also need to restrict network access to certain PaaS resources and create a private endpoint for an Azure web app. This scenario requires a deep understanding of Azure's networking services and how to implement them effectively.

Azure provides a range of services and features to enhance the security and privacy of your network connections. These services include Virtual Network Service Endpoints, Azure Private Link, Private Endpoint, and Azure Private Link Service. These technologies allow for secure and direct connectivity to Azure services over the Azure backbone network, replacing public endpoints with private network interfaces, and providing granular access control.

In this module, you learn to:

* Describe and implement Virtual Network Service Endpoints in Azure for secure and direct connectivity.
* Use Azure Private Link and Private Endpoint to replace public endpoints with private network interfaces.
* Use Azure Private Link Service to provide private access from your Azure virtual network to Azure PaaS services and Microsoft Partner services.

---

## Explain virtual network service endpoints

### Scenario

Your organization migrates an existing app with database servers to Azure virtual machines. Now, to reduce your costs and administrative requirements, you're considering using some Azure platform as a service (PaaS) services. Specifically, storage services to hold large file assets, such as engineering diagrams. These engineering diagrams have proprietary information, and must remain secure from unauthorized access. These files must only be accessible from specific systems.

Here are some other scenarios that have similar requirements.

* Connecting services to peered or multiple virtual networks.
* Securing Azure resources to services deployed directly into virtual networks.
* Filtering outbound traffic from a virtual network to Azure services.
* Managing disk traffic from an Azure virtual machine.

### What is a Virtual Network Service Endpoint?

By default, Azure services are all designed for direct internet access. All Azure resources have public IP addresses, including PaaS services such as Azure SQL Database and Azure Storage. Because these services are exposed to the internet, anyone can potentially access your Azure services.

[Virtual Network (VNet) Service Endpoint](/en-us/azure/virtual-network/virtual-network-service-endpoints-overview) provides secure and direct connectivity to Azure services over the Azure backbone network. Endpoints allow you to secure your critical Azure service resources to only your virtual networks. Service endpoints enable private IP addresses in the virtual network to reach the endpoint of an Azure service.

Service Endpoints can connect certain services directly to your private address space in Azure. Azure Service Endpoints are available for many services, including:

* Azure Storage
* Azure SQL Database
* Azure Cosmos DB
* Azure Key Vault
* Azure Service Bus
* Azure Event Hubs
* Azure App Service
* Azure Container Registry

### Service Endpoint optimization and security features

This video highlights the optimization and security features of endpoints.

### Service Endpoint policies

[Virtual Network Service Endpoint policies](/en-us/azure/virtual-network/virtual-network-service-endpoint-policies-overview) Service endpoint policies enable you to filter virtual network traffic to specific Azure resources, over service endpoints. For example, endpoint policies could provide granular access control for virtual network traffic to Azure Storage when connecting over a Service Endpoint.

Note

Microsoft recommends use of Azure Private Link and private endpoints for secure and private access to services hosted on the Azure platform. This information is covered in the next units.

Tip

Learn more about Service Endpoints in the [Secure and isolate access to Azure resources by using network security groups and service endpoints](/en-us/training/modules/secure-and-isolate-with-nsg-and-service-endpoints/) module. This module includes an exercise to create a Service Endpoint and use network rules to restrict access to Azure Storage.

### Check your knowledge

---

## Define Private Link Service and private endpoint

### Scenario

Your organization has an Azure virtual network, and you want to connect to a PaaS resource such as an Azure SQL database. When you create such resources, you normally specify a public endpoint as the connectivity method.

Having a public endpoint means that the resource is assigned a public IP address. So, even though both your virtual network and the Azure SQL database are located within the Azure cloud, the connection between them takes place over the internet.

The concern here's that your Azure SQL database is exposed to the internet through its public IP address. This exposure creates multiple security risks. These security risks are present when any Azure resource is accessed via a public IP address from:

* A peered Azure virtual network.
* An on\-premises network that connects to Azure using ExpressRoute and Microsoft peering.
* A customer's Azure virtual network that connects to an Azure service offered by your company.

### Overview of Azure Private Endpoint and Azure Private Link

This video summarizes Private Endpoints and Private Links.

### What is Azure Private Link?

[Azure Private Link](/en-us/azure/private-link/private-link-overview) enables you to access Azure PaaS Services and Azure hosted customer\-owned/partner services over a Private Endpoint in your virtual network. Private Link is designed to eliminate security risks by removing the public part of the connection.

Private Link provides secure access to Azure services. Private Link achieves that security by replacing a resource's public endpoint with a private network interface. There are three key points to consider with this new architecture.

* The Azure resource becomes, in a sense, a part of your virtual network.
* The connection to the resource now uses the Microsoft Azure backbone network instead of the public internet.
* You can configure the Azure resource to no longer expose its public IP address, which eliminates that potential security risk.

### What is Azure Private Endpoint?

[Azure private endpoint](/en-us/azure/private-link/private-endpoint-overview) is the key technology behind private link. Private endpoint is a network interface that enables a private and secure connection between your virtual network and an Azure service. In other words, private endpoint is the network interface that replaces the resource's public endpoint.

Private Link provides secure access to Azure services. Private Link achieves that security by replacing a resource's public endpoint with a private network interface. Private Endpoint uses the private IP address for services into the virtual network.

[Network policies](/en-us/azure/private-link/disable-private-endpoint-network-policy/) are disabled by default for private endpoint subnets. You can selectively enable support for:

* **Network Security Groups (NSG)**: Control inbound traffic to the private endpoint from specific sources.
* **User Defined Routes (UDR)**: Override the default /32 route to redirect traffic through an NVA or firewall.
* **Application Security Groups (ASG)**: Group private endpoints for policy application.

### How is Azure Private Endpoint different from a service endpoint?

Azure Private Endpoint lets you connect to an Azure service using a private IP address from your own virtual network. This process ensures all traffic on Microsoft's network and means you don't need the public internet to access the service.

In contrast, Service Endpoints secure access to an Azure service’s public endpoint by allowing traffic from specific VNets or subnets, but the service itself still uses a public IP.

Private Endpoints offer full isolation and higher security, while Service Endpoints are easier to set up but provide less isolation.

Note

When public internet access is required for PaaS services, [Network Security Perimeter](/en-us/azure/private-link/network-security-perimeter-concepts) provides a logical security boundary with controlled inbound and outbound access rules. Network Security Perimeter is generally available in all Azure public regions and complements Private Link.

### Check your knowledge

---

## Integrate private endpoint with Domain Name Service

### What is Azure Private Link Service?

Private Link gives you private access from your Azure virtual network to PaaS services and Microsoft Partner services in Azure. But, what if your company has its own Azure services? Is it possible to offer those customers a private connection to your company's services?

Yes, by using [Azure Private Link Service](/en-us/azure/private-link/private-link-service-overview). This service lets you offer Private Link connections to your custom Azure services. Consumers of your custom services can then access those services privately—that is, without using the internet—from their own Azure virtual networks.

Azure Private Link service is the reference to your own service that's powered by Azure Private Link. Your service that's running behind Azure standard load balancer can be enabled for Private Link access so that consumers to your service can access it privately from their own VNets. Your customers can create a private endpoint inside their VNet and map it to this service. A Private Link service receives connections from multiple private endpoints. A private endpoint connects to one Private Link service.

### Private link and DNS integration for hub\-spoke networks

The following diagram shows a typical [high\-level architecture](/en-us/azure/architecture/networking/guide/private-link-hub-spoke-network#azure-hub-and-spoke-topologies) for enterprise environments with central DNS resolution. The network architecture is hub\-spoke network with Private Link resources and Azure Private DNS.

In the previous diagram, it's important to highlight:

1. All Azure virtual networks use the DNS private resolver that's hosted in the hub virtual network.
2. On\-premises DNS servers have conditional forwarders configured for each private endpoint public DNS zone, pointing to the DNS private resolver hosted in the hub virtual network.
3. The DNS private resolver hosted in the hub virtual network uses the Azure\-provided DNS (168\.63\.129\.16\) as a forwarder. IP address 168\.63\.129\.16 is a virtual public IP address that facilitates a communication channel to Azure platform resources.
4. The hub virtual network must be linked to the Private DNS zone names for Azure services, such as privatelink.blob.core.windows.net.

Note

A DNS zone group is automatically created when integrating a private endpoint with a private DNS zone. The group links the endpoint to DNS zones and manages DNS records automatically. This automation reduces manual work and prevents configuration drift.

#### What is Azure DNS Private Resolver

[Azure DNS Private Resolver](/en-us/azure/dns/dns-private-resolver-overview) enables you to query Azure DNS on\-premises private zones without deploying VM based DNS servers. When you use DNS Private Resolver, you don't need a DNS forwarder, and Azure DNS is able to resolve on\-premises domain names.

Tip

Learn more about Azure DNS Private Resolver in the [Intro to Azure DNS Private Resolver](/en-us/training/modules/intro-to-azure-dns-private-resolver/) module.

### Check your knowledge

---

## Exercise: Create an Azure private endpoint using Azure PowerShell

### Lab scenario

In this lab, you create a Private Endpoint for an Azure web app and deploy a virtual machine to test the private connection.

### Architecture diagram

### Job skills

* Create a resource group
* Create a virtual network
* Deploy Azure Bastion
* Create a private endpoint
* Configure the private DNS zone
* Create a test virtual machine
* Test connectivity to the private endpoint

Important

Estimated time: 45 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
This lab is optional.

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Summary

In this module, you learned about service endpoints, private endpoints, private links, private link services, and DNS integration.

**The main takeaways from this module are:**

* **Service Endpoints** limit the Azure service's access to the allowed virtual network and subnet. Service endpoints provide network\-level security and isolation of the Azure service traffic.
* **Service Endpoint policies** allow you to filter virtual network traffic to the Service Endpoint.
* **Azure Private Link** enables you to access Azure PaaS Services and Azure hosted customer\-owned/partner services over a Private Endpoint in your virtual network. Private Link is designed to eliminate security risks by removing the public part of the connection.
* **Azure private endpoint** is the key technology behind private link. Private endpoint is a network interface that enables a private and secure connection between your virtual network and an Azure service.
* **Azure Private Link service** lets you offer Private Link connections to your custom Azure services. Consumers of your custom services can then access those services privately—that is, without using the internet—from their own Azure virtual networks.
* **Azure DNS Private Resolver** lets you query Azure DNS private zones from an on\-premises environment and vice versa without deploying VM based DNS servers. When you use DNS Private Resolver, you don't need a DNS forwarder, and Azure DNS is able to resolve on\-premises domain names.

#### Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

* What is an Azure Service Endpoint and when would you use it?
* What is an Azure private endpoint and how is it accessed using Azure private link?

### Learn more with self\-paced training

Use these resources to discover more.

* [Secure and isolate access to Azure resources by using network security groups and service endpoints](/en-us/training/modules/secure-and-isolate-with-nsg-and-service-endpoints/). Learn how network security groups and service endpoints help you secure your virtual machines and Azure services from unauthorized network access.
* [Introduction to Azure DNS](/en-us/training/modules/intro-to-azure-dns/). This module explains what Azure DNS does, how it works, and when you should choose to use Azure DNS as a solution to meet your organization’s needs.
* [Design and implement private access to Azure Services](/en-us/training/modules/design-implement-private-access-to-azure-services/). Learn to design and implement private access to Azure Services with Azure Private Link, and virtual network service endpoints.
* [Intro to Azure DNS Private Resolver](/en-us/training/modules/intro-to-azure-dns-private-resolver/). This module introduces you to Azure DNS Private Resolver and describes its characteristics, capabilities, and use cases.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/design-implement-private-access-to-azure-services/_

## Fuentes
- [Design and implement private access to Azure Services](https://learn.microsoft.com/en-us/training/modules/design-implement-private-access-to-azure-services/?WT.mc_id=api_CatalogApi)
