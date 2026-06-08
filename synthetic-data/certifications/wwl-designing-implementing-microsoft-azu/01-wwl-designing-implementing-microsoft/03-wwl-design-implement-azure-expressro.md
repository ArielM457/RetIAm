# Design and implement Azure ExpressRoute

> Curso: AZ-700 Design and Implement Microsoft Azure Network Solutions (wwl-designing-implementing-microsoft-azure-network) · Seccion: AZ-700 Design and Implement Microsoft Azure Network Solutions
> Duracion estimada: 57 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

ExpressRoute lets you extend your on\-premises networks into the Microsoft cloud over a private connection with the help of a connectivity provider. With ExpressRoute, you can establish connections to various Microsoft cloud services, such as Microsoft Azure and Microsoft 365\. Connectivity can be from an any\-to\-any (IP VPN) network, a point\-to\-point Ethernet network, or a virtual cross\-connection through a connectivity provider at a colocation facility. Since ExpressRoute connections don't travel over the public Internet, this approach offers more reliability, faster speeds, consistent latencies, and higher security.

### Learning objectives

In this module, you learn about:

* ExpressRoute and its capabilities.
* ExpressRoute deployments including high availability.
* ExpressRoute peering.
* ExpressRoute Global Reach.
* ExpressRoute FastPath.

### Prerequisites

* Experience with networking concepts, such as IP addressing, Domain Name System (DNS), and routing.
* Experience with network connectivity methods, such as VPN or WAN.
* Experience with the Azure portal and Azure PowerShell.

---

## Explore Azure ExpressRoute

This video summarizes the usage cases for Azure Expressroute. The video also covers the main components from the customer's network to the Microsoft Edge.

### Basic ExpressRoute architecture

ExpressRoute extends on\-premises networks into the Microsoft cloud over a private connection with the help of a connectivity provider. ExpressRoute establishes connections to various Microsoft cloud services, such as Microsoft Azure and Microsoft 365\. Connectivity can be from an any\-to\-any (IP VPN) network, a point\-to\-point Ethernet network, or a virtual cross\-connection through a connectivity provider at a colocation facility. Since ExpressRoute connections don't go over the public Internet, this approach offers more reliability, faster speeds, consistent latencies, and higher security.

### ExpressRoute connectivity models

ExpressRoute allows you to create a connection in two ways: the Service Provider model and the ExpressRoute Direct model. Within the Service Provider model there are three paths: CloudExchange Colocation, Point\-to\-point Ethernet Connection, and Any\-to\-any (IPVPN) Connection.

1. **Co\-located at a cloud exchange**. If you're colocated in a facility with a cloud exchange, you can request for virtual cross\-connections to the Microsoft cloud through the colocation provider’s Ethernet exchange. Colocation providers can offer either Layer 2 cross\-connections, or managed Layer 3 cross\-connections between your infrastructure in the colocation facility and the Microsoft cloud.
2. **Point\-to\-point Ethernet connections**. You can connect your on\-premises datacenters or offices to the Microsoft cloud through point\-to\-point Ethernet links. Point\-to\-point Ethernet providers can offer Layer 2 connections.
3. **Any\-to\-any (IPVPN) networks**. You can integrate your WAN with the Microsoft cloud. IPVPN providers (typically MPLS VPN) offer any\-to\-any connectivity between your branch offices and datacenters. The Microsoft cloud can be interconnected to your WAN to make it appear like any other branch office. WAN providers typically offer managed Layer 3 connectivity.
4. **ExpressRoute Direct**. You can connect directly into the Microsoft global network at a peering location strategically distributed across the world. ExpressRoute Direct provides dual 100\-Gbps or 10\-Gbps connectivity that supports Active/Active connectivity at scale.

Tip

Learn more about Azure ExpressRoute in the [Introduction to Azure ExpressRoute](/en-us/training/modules/intro-to-azure-expressroute/) module.

### Check your knowledge

---

## Design an ExpressRoute deployment

Choosing between ExpressRoute Direct and the Service Provider model depends on the requirements of the organization. These requirements include performance requirements, budget constraints, and desired level of control over the network infrastructure. Large enterprises with high data transfer needs might opt for ExpressRoute Direct. Smaller businesses or those seeking managed services might prefer the Service Provider model.

In this video, we discuss provisioning a ExpressRoute Direct circuit. An ExpressRoute circuit is a dedicated, private connection that allows you to extend your on\-premises networks into the Microsoft cloud.

#### Comparison of ExpressRoute Direct and the Service Provider models

This table highlights the key differences between ExpressRoute Direct and the Service Provider model.

| Feature/Aspect | ExpressRoute using a Service Provider | ExpressRoute Direct |
| --- | --- | --- |
| Usage cases | Small to medium sized business looking for a simple setup with managed services | Large enterprises with mission\-critical applications requiring high\-performance connectivity |
| Connectivity | Connection via a service provider's infrastructure | Direct connection to Microsoft's network through dual 10\-Gbps, 100\-Gbps,or 400\-Gbps ports |
| Circuit SKUs | Ranges from 50 Mbps to 10 Gbps | 10\-Gbps: 1, 2, 5, 10 Gbps; 100\-Gbps: 5, 10, 40, 100 Gbps; 400\-Gbps: 5, 10, 40, 100, 200, 400 Gbps |
| Optimization | Optimized for single tenant | Optimized for a single tenant with multiple business units |

Note

400\-Gbps ExpressRoute Direct is available in limited peering locations and requires enrollment.

Azure ExpressRoute offers different [SKUs](/en-us/azure/expressroute/expressroute-faqs#expressroute-premium) to cater to various connectivity needs and performance requirements. Each SKU has different pricing and features, such as varying limits on the number of virtual networks you can connect to and the bandwidth options available. When choosing a SKU, consider your organization's geographic footprint, latency requirements, and budget constraints.

* **Local SKU (if available)**. The Local SKU provides connectivity to a single Azure region. It's suitable for scenarios where you need low\-latency access to resources in a particular Azure region.
* **Standard SKU**: The Standard SKU allows connectivity to multiple Azure regions within the same geopolitical area. The Standard SKU is useful for businesses that operate within a specific region but need access to resources across multiple locations.
* **Premium SKU**: The Premium SKU extends connectivity to all Azure regions globally. This SKU is ideal for multinational organizations that require seamless connectivity to Azure resources across different continents.

Tip

You also need to select a billing model. ExpressRoute offers unlimited data, metered data, and a premium add\-on.

### Check your knowledge

---

## Exercise: Configure an ExpressRoute gateway

### Lab scenario

In this lab, you create a virtual network gateway for ExpressRoute.

### Architecture diagram

### Job skills

* Create the virtual network and gateway subnet.
* Create the virtual network gateway.

Important

Estimated time: 60 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Exercise: Provision an ExpressRoute circuit

### Lab scenario

In this exercise, you create an ExpressRoute circuit using the Azure portal and the Azure Resource Manager deployment model.

### Architecture diagram

### Job skills

* Create and provision an ExpressRoute circuit.
* Identify your provisioning Service Key.
* Deprovisioning an ExpressRoute circuit.

Important

Estimated time: 15 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Configure peering for an ExpressRoute deployment

### Choose a peering scheme

You can use two different peering schemes with ExpressRoute: **Private Peering** and **Microsoft Peering**.

* [**Private peering**](/en-us/azure/expressroute/expressroute-circuit-peerings#privatepeering). Private Peering is ideal for scenarios where you need secure, high\-performance connectivity to Azure resources. Private peering allows you to connect on premises hosts with Azure IaaS and PaaS services configured to work with Azure virtual networks. All resources must be located in Azure virtual networks and allocated IP addresses in a private address space that doesn't overlap with your on\-premises address space. You can’t connect to an Azure resource’s public IP address, such as an IaaS VM’s public IP address through private peering.
* **[Microsoft peering](/en-us/azure/expressroute/expressroute-faqs#microsoft-peering)**. Microsoft Peering is suitable for accessing Microsoft SaaS and PaaS services. Microsoft peering allows you to connect over ExpressRoute with Azure PaaS services, Microsoft 365 services, and Dynamics 365\.

#### Choose between Private peering and Microsoft peering

This comparison table compares Private peering with Microsoft peering.

| Feature | ExpressRoute Private Peering | ExpressRoute Microsoft Peering |
| --- | --- | --- |
| **Purpose** | Connects directly to Azure virtual networks | Connects to Microsoft services like Microsoft 365, Dynamics 365, and Azure PaaS services |
| **Traffic Type** | Private IP traffic | Public IP traffic |
| **Access** | Direct access to Azure VMs and services within virtual networks | Access to Microsoft SaaS services and Azure PaaS services |
| **Security** | Traffic stays on private network, not exposed to the internet | Traffic is routed over public IPs but through a private connection |
| **Use Cases** | Enterprise applications, databases, and other workloads requiring secure, high\-performance connectivity | Access to Microsoft services like Microsoft 365, Dynamics 365, and Azure PaaS services |
| **Network Isolation** | Provides network isolation from the public internet | Doesn't provide network isolation from the public internet, but ensures traffic doesn't traverse the public internet |
| **Bandwidth Options** | Offers scalable bandwidth options | Offers scalable bandwidth options |

### Choose a peering location

ExpressRoute locations, also known as peering locations or meet\-me locations, are colocation facilities where Microsoft Enterprise Microsoft Edge (MSEE) devices are situated. These locations serve as the entry points to Microsoft's network and are globally distributed, offering the ability to connect to Microsoft's network worldwide. To choose an Azure ExpressRoute [peering location](/en-us/azure/expressroute/expressroute-locations?tabs=america%2Ca-c%2Cus-government-cloud%2Ca-C), consider:

* **Proximity to your data centers**. Choose a peering location that is geographically close to your on\-premises data centers or office locations. Proximity to the data center minimizes latency and can improve the performance of your applications.
* **Azure region connectivity**: Ensure that the peering location provides connectivity to the Azure regions you need to access. Different peering locations can offer connectivity to different sets of Azure regions, especially if you're using the Local or Standard SKU.
* **Network Service Provider availability**: Check which network service providers (NSPs) are available at the peering location. You need to work with an NSP to establish the physical connection to Azure ExpressRoute. Choose a provider that offers competitive pricing and reliable service.
* **Bandwidth requirements**: Consider your bandwidth needs and ensure that the peering location can support the required capacity. Different locations may have different bandwidth options available.
* **Cost Considerations**: Costs can vary based on the peering location, the NSP chosen, and the bandwidth required. To find the most cost\-effective solution for your needs, compare costs across different locations and providers.
* **Compliance and regulatory requirements**: If your organization has specific compliance or regulatory requirements, ensure that the peering location meets these standards. Compliance requirements might include data residency or industry\-specific regulations.
* **Future growth and scalability**: Consider your future growth plans and ensure that the peering location can accommodate increased bandwidth and other connections as your needs evolve.

### Check your knowledge

---

## Connect geographically dispersed networks with ExpressRoute global reach

With [ExpressRoute Global Reach](/en-us/azure/expressroute/expressroute-global-reach), you can link ExpressRoute circuits to create a private network between your on\-premises networks.

#### Global Reach example architecture

Imagine you have a branch office in San Francisco and another branch office in London. Both branch offices have high\-speed connectivity to Azure resources in US West and UK South. However, the branch offices can't connect and send data directly with one another. With Global Reach the San Francisco office can directly exchange data with your London office through the existing ExpressRoute circuits and Microsoft's global network.

#### Global Reach advantages

* **Improved Connectivity**. Azure Global Reach enables direct connectivity between different on\-premises sites using Microsoft's global network.
* **Security**. Data is transmitted securely across Microsoft's private network, reducing exposure to potential threats compared to public internet connections.
* **Reduced Latency**. The use of Microsoft's high\-speed global network can significantly reduce latency, providing faster and more efficient data transfer between connected sites.
* **Scalability**. Azure Global Reach can easily scale to accommodate growing network demands, allowing businesses to expand their connectivity as needed without significant infrastructure changes.
* **Simplified Network Management**. Centralized management through Azure can simplify the configuration and monitoring of network connections, making it easier for IT teams to manage complex network topologies.

### Check your knowledge

---

## Improve data path performance between networks with ExpressRoute FastPath

ExpressRoute virtual network gateway facilitates the exchange of network routes and directs network traffic. [ExpressRoute FastPath](/en-us/azure/expressroute/about-fastpath) enhances data path performance between your on\-premises network and your virtual networks. When enabled, ExpressRoute FastPath routes network traffic directly to virtual machines, bypassing the ExpressRoute virtual network gateway.

To use FastPath, your ExpressRoute virtual network gateway must be one of the following SKUs. A gateway is still required to exchange route information. FastPath bypasses the gateway only for data traffic.

* Ultra Performance
* ErGw3AZ
* ErGwScale (minimum 10 scale units)

FastPath is available on all ExpressRoute circuits. ExpressRoute FastPath is useful for enterprises that need consistent and high\-performance connectivity to Azure for mission\-critical applications.

#### Advantages of ExpressRoute FastPath

* **Improved Performance**. FastPath reduces latency and increases throughput by allowing data to bypass the Azure WAN, providing a more direct path to your virtual network.
* **Lower Latency**. FastPath reduces the number of hops and routing directly to the virtual network. Optimized routing can significantly reduce latency, which is crucial for applications requiring real\-time processing.
* **Higher Throughput**. FastPath supports higher data transfer rates, making it suitable for bandwidth\-intensive applications and workloads.
* **Optimized Routing**. FastPath provides optimized routing for data packets, which can enhance the overall efficiency of network operations.
* **Reliability**. With a more direct connection, there's less chance of network congestion or packet loss, improving the reliability of data transfers.
* **Security**. FastPath ensures that data travels through fewer intermediary points, potentially reducing exposure to security risks.

#### Advanced FastPath features (ExpressRoute Direct only)

When using FastPath with an ExpressRoute Direct circuit, three additional capabilities are available:

* **Virtual network peering**: FastPath sends traffic directly to VMs in spoke virtual networks connected via VNet peering. Hub and spoke virtual networks must be in the same region.
* **User\-Defined Routes (UDRs)**: FastPath honors UDRs configured on the gateway subnet while maintaining the performance bypass.
* **Private Link and private endpoints**: FastPath sends traffic directly to private endpoints in spoke virtual networks. This feature is in limited general availability and requires enrollment.

### Check your knowledge

---

## Troubleshoot ExpressRoute connection issues

As an Azure network engineer supporting an ExpressRoute deployment, you have to diagnose and resolve any ExpressRoute connection issues that arise.

At the highest level, there are three main ExpressRoute routing domains. You should consider each area when trying to resolve an issue.

* The Azure network (blue cloud)
* The Internet or WAN (green cloud)
* The Corporate Network (orange cloud)

### Troubleshooting

Given the number of network components, a step\-by\-step process is more effective than random testing. Ensure your expectations are reasonable. Start at the edge of the network. Create a diagram. Keep an open mind and verify all assumptions. For more suggestions, consult the [troubleshooting reference](/en-us/azure/expressroute/expressroute-troubleshooting-network-performance).

#### Verify the circuit and provider status

For an ExpressRoute circuit to be operational, the Microsoft **Circuit status** must be **Enabled**. Also, the **Provider status** must be **Provisioned**.

#### Verify the peering

Each ExpressRoute circuit can have one or both peerings: Azure private peering and Microsoft peering. For success, the peering status should be **provisioned**.

#### Get support help

The Azure portal has information on configuring and troubleshooting ExpressRoute connections. The support wizard can identify and provide troubleshooting steps.

When you need assistance from Microsoft or from an ExpressRoute partner, you must provide the ExpressRoute Service Key. The Service Key uniquely identifies your circuit.

Tip

Learn more about ExpressRoute troubleshooting in the [Troubleshoot cloud and hybrid connectivity in Microsoft Azure](/en-us/training/modules/cloud-hybrid-connectivity/) module.

### Check your knowledge

---

## Summary and resources

This module covered Azure ExpressRoute deployments.

**The main takeaways from this module are:**

* ExpressRoute extends on\-premises networks into the Microsoft cloud over a private connection with the help of a connectivity provider.
* ExpressRoute has two connectivity provider models. The Service Provider model offers: CloudExchange Colocation, Point\-to\-point Ethernet Connection, and Any\-to\-any (IPVPN) Connection. There's also a ExpressRoute Direct model.
* ExpressRoute offers three SKUs: Local, Standard, and Premium.
* ExpressRoute has two different peering schemes: Private Peering and Microsoft Peering.
* ExpressRoute has three resiliency models: Standard, High, and Maximum.
* ExpressRoute Global Reach creates a private network between your on\-premises networks.
* ExpressRoute FastPath enhances data path performance between your on\-premises network and your virtual networks.

### Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

* What are the main features and capabilities of ExpressRoute?
* What resiliency options are available for ExpressRoute? Provide usage examples.
* What is the difference between ExpressRoute Global Reach and ExpressRoute FastPath?

### Learn more with self\-paced training

* [Introduction to Azure ExpressRoute](/en-us/training/modules/intro-to-azure-expressroute/). This module explains what Azure ExpressRoute does, how it works, and when you should choose to use Azure ExpressRoute as a solution.
* [Troubleshoot virtual network connectivity in Microsoft Azure](/en-us/training/modules/cloud-hybrid-connectivity/4-troubleshoot-virtual-network-connectivity). This module enables you to manage and troubleshoot different network configurations to support your organization’s needs.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/design-implement-azure-expressroute/_

## Fuentes
- [Design and implement Azure ExpressRoute](https://learn.microsoft.com/en-us/training/modules/design-implement-azure-expressroute/?WT.mc_id=api_CatalogApi)
