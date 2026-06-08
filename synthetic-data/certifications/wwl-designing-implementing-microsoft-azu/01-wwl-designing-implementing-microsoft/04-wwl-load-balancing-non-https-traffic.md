# Load balance non-HTTP(S) traffic in Azure

> Curso: AZ-700 Design and Implement Microsoft Azure Network Solutions (wwl-designing-implementing-microsoft-azure-network) · Seccion: AZ-700 Design and Implement Microsoft Azure Network Solutions
> Duracion estimada: 44 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Imagine yourself in the role of a network engineer at an organization that is migrating to Azure. As the network engineer you need to ensure line\-of\-business applications, services, and data are available to end users of your corporate network whenever and wherever possible. You also need to ensure users get access to those network resources in an efficient and timely manner.

Azure provides different flavors of load balancing services that help with the distribution of workloads across your networks. The aim of load balancing is to optimize the use of your resources, while maximizing throughput and minimizing the time it takes for a response. You can create internal and public load balancers in an Azure environment to distribute the network traffic within your network and the network traffic arriving from outside your network. In this module, you learn about using the Azure Load Balancer, and Traffic Manager load balancing services.

### Learning objectives

In this module, you:

* Understand non\-HTTP(S) options for load balancing.
* Learn about the Azure Load Balancer.
* Learn about Azure Traffic Manager.

### Prerequisites

* You should have experience with networking concepts, such as IP addressing, Domain Name System (DNS), and routing.
* You should have experience with network connectivity methods, such as VPN or WAN.
* You should have experience with the Azure portal and Azure PowerShell.

---

## Explore load balancing

The term load balancing refers to the even distribution of incoming network workloads to a group of backend computing resources or servers. Load balancing aims to optimize resource use, maximize throughput, minimize response time, and avoid overloading any single resource. Load balancing can also improve availability by sharing a workload across redundant computing resources.

This video reviews how to select a load balancing solution.

### Load Balancing options for Azure

Azure provides various load balancing services that you can use to distribute your workloads across multiple computing resources, but the following are the main services:

* **Azure Load Balancer**. High\-performance, ultra\-low\-latency Layer 4 load\-balancing service (inbound and outbound) for all UDP and TCP protocols. The load balancer can handle millions of requests per second ensuring your solution is highly available. Azure Load Balancer is zone\-redundant, ensuring high availability across availability zones.
* **Traffic Manager**. DNS\-based traffic load balancer that enables you to distribute traffic optimally to services across global Azure regions, while providing high availability and responsiveness. Because Traffic Manager is a DNS\-based load\-balancing service, it load\-balances only at the domain level. For that reason, it can't fail over as quickly as Front Door.
* **Azure Application Gateway**. Provides application delivery controller (ADC) as a service, offering various Layer 7 load\-balancing capabilities. Use it to optimize web farm productivity by offloading CPU\-intensive SSL termination to the gateway.
* **Azure Front Door**. Application delivery network that provides global load balancing and site acceleration service for web applications. It offers Layer 7 capabilities for your application. Front Door includes SSL offload, path\-based routing, fast failover, and caching.

### Categorizing load balancing services

Load balancing services can be categorized in two ways: global versus regional, and HTTP(S) versus non\-HTTP(S).

#### Global versus regional

**Global** load\-balancing services distribute traffic across regional backends, clouds, or hybrid on\-premises services. These services route end\-user traffic to the closest available backend. They also react to changes in service reliability or performance. You can think of them as systems that load balance between application stamps, endpoints, or scale\-units hosted across different regions/geographies.

In contrast, **Regional** load\-balancing services distribute traffic within virtual networks across virtual machines (VMs) or zonal and zone\-redundant service endpoints within a region. You can think of them as systems that load balance between VMs, containers, or clusters within a region in a virtual network.

#### HTTP(S) versus non\-HTTP(S)

**HTTP(S)** load\-balancing services are Layer 7 load balancers that only accept HTTP(S) traffic. They're intended for web applications or other HTTP(S) endpoints. They include features such as SSL offload, web application firewall, path\-based load balancing, and session affinity.

In contrast, **non\-HTTP(S)** load\-balancing services can handle non\-HTTP(S) traffic and are recommended for nonweb workloads.

Important

In this module, we're focusing on the non\-HTTP(S) solutions.

This table summarizes these categorizations for each Azure load balancing service.

| Service | Global/regional | Recommended traffic |
| --- | --- | --- |
| Azure Front Door | Global | HTTP(S) |
| Traffic Manager | Global | non\-HTTP(S) |
| Application Gateway | Regional | HTTP(S) |
| Azure Load Balancer | Regional | non\-HTTP(S) |

### Choosing a load balancing option for Azure

Here are the key factors to decide on a load balancing option.

* **Type of traffic** \- is it for a web application? Is it a public\-facing or private application?
* **Scope** \- do you need to load balance virtual machines and containers within a virtual network, or load balance across regions, or both?
* **Availability** \- what is the Service Level Agreement (SLA) for the service?
* **Cost** \- In addition to the cost of the actual service itself, consider the operational cost to manage and maintain a solution built on that service. See [Load balancing pricing](https://azure.microsoft.com/pricing/details/load-balancer/).
* **Features and limitations** \- what features and benefits does each service provide, and what are its limitations? See [Load balancer limits](/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits).

This [flowchart](/en-us/azure/architecture/guide/technology-choices/load-balancing-overview#decision-tree-for-load-balancing-in-azure) helps you select the most appropriate load\-balancing solution for your application.

Tip

You should use this flowchart and the suggested recommendation only as a starting point. A completed solution can incorporate two or more load\-balancing solutions.

### Selecting a load balancing solution by using the Azure portal

You can use the **Azure Load Balancing** page in the Azure portal to help guide you to a load\-balancing solution. Search for and select **Load balancing \- help me choose**. The wizard provides an interactive way to select a load balancing solution.

---

## Design and implement Azure load balancer using the Azure portal

[**Azure Load Balancer**](/en-us/azure/load-balancer/load-balancer-overview) operates at layer 4 of the Open Systems Interconnection (OSI) model. It's the single point of contact for clients. Azure Load Balancer distributes inbound flows that arrive at the load balancer's front end to backend pool instances. These flows are according to configured load\-balancing rules and health probes. The backend pool instances can be Azure Virtual Machines or instances in a virtual machine scale set.

This video reviews how to select a load balancer type.

### Choosing a load balancer type

Load balancers can be public (external) or internal (private).

A **public load balancer** can provide outbound connections for virtual machines (VMs) inside your virtual network. These connections are accomplished by translating their private IP addresses to public IP addresses. External load balancers are used to distribute client traffic from the internet across your VMs. That internet traffic might come from web browsers, module apps, or other sources.

An **internal load balancer** is used where private IPs are needed at the frontend only. Internal load balancers are used to load balance traffic from internal Azure resources to other Azure resources inside a virtual network. A load balancer frontend can also be accessed from an on\-premises network in a hybrid scenario.

This diagram shows how public and internal load balancers can work together.

### Azure load balancer and availability zones

Azure Load Balancer supports [availability zones scenarios](/en-us/azure/reliability/reliability-load-balancer#availability-zone-support). A Load Balancer can either be zone redundant, zonal, or nonzonal.

#### Zone redundant

In a region with Availability Zones, a Standard Load Balancer can be zone\-redundant. A single frontend IP address survives zone failure. The frontend IP can be used to reach all (nonimpacted) backend pool members no matter the zone. One or more availability zones can fail and the data path survives as long as one zone in the region remains healthy.

#### Zonal

You can choose to have a frontend guaranteed to a single zone, which is known as a *zonal*. With this scenario, a single zone in a region serves all inbound or outbound flow. Your frontend shares fate with the health of the zone. The data path is unaffected by failures in zones other than where it was guaranteed.

#### Nonzonal

Load Balancers can also use a "no\-zone" frontend. In these scenarios, a public load balancer would use a public IP or public IP prefix, an internal load balancer would use a private IP. This option doesn't give a guarantee of redundancy.

### Selecting an Azure load balancer SKU

There are two [load balancer SKUs](/en-us/azure/load-balancer/skus): Standard, and Gateway. These SKUs differ in terms of their scenario scope and scale, features, and cost.

Important

On September 30, 2025, the Basic Load Balancer was retired. The Basic Load Balancer is no longer available for new deployments. Existing Basic Load Balancer resources should be [upgraded to Standard Load Balancer](/en-us/azure/load-balancer/load-balancer-basic-upgrade-guidance).

| **Features** | **Standard Load Balancer** | **Gateway Load Balancer** |
| --- | --- | --- |
| Primary use case | General\-purpose load balancing for web applications and services | High performance and high availability scenarios with Network Virtual Appliances (NVAs) |
| Backend pool size | Supports up to 1,000 instances | Supports up to 1,000 instances |
| Backend pool endpoints | Any virtual machines or virtual machine scale sets in a single virtual network. | Network Virtual Appliances (NVAs) in a single virtual network |
| Traffic inspection | No built\-in traffic inspection | Enables transparent traffic inspection and filtering through NVAs |
| Cross\-region connectivity | Regional load balancing | Regional load balancing with NVA integration |

Tip

Learn more about the Load Balancer check out the [Introduction to Azure Load Balancer](/en-us/training/modules/intro-to-azure-load-balancer/) module.

### Check your knowledge

---

## Exercise: Create and configure an Azure load balancer

### Lab scenario

In this lab, you create an internal load balancer for the fictional Contoso Ltd organization.

### Architecture diagram

### Job skills

* Create the virtual network.
* Create backend servers.
* Create the load balancer.
* Create load balancer resources.
* Test the load balancer.

Important

Estimated time: 60 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Explore Azure Traffic Manager

[Azure Traffic Manager](/en-us/azure/traffic-manager/traffic-manager-overview) is a DNS\-based traffic load balancer. This service allows you to distribute traffic to your public facing applications across the global Azure regions. Traffic Manager also provides your public endpoints with high availability and quick responsiveness. The most important point to understand is that Traffic Manager works at the DNS level, which is at the Application layer (Layer\-7\).

This video reviews Traffic Manager features and how the service works.

### Key features of Traffic Manager

Traffic Manager offers the several key features.

| **Feature** | **Description** |
| --- | --- |
| Increase application availability | Traffic Manager delivers high availability for your critical applications by monitoring your endpoints and providing automatic failover when an endpoint goes down. |
| Improve application performance | Azure allows you to run cloud services and websites in datacenters located around the world. Traffic Manager can improve the responsiveness of your website by directing traffic to the endpoint with the lowest latency. |
| Service maintenance without downtime | You can plan maintenance on your applications without downtime. Traffic Manager can direct traffic to alternative endpoints while the maintenance is in progress. |
| Combine hybrid applications | Traffic Manager supports external, non\-Azure endpoints enabling it to be used with hybrid cloud and on\-premises deployments, including the burst\-to\-cloud, migrate\-to\-cloud, and failover\-to\-cloud scenarios. |
| Distribute traffic for complex deployments | Using nested Traffic Manager profiles, multiple traffic\-routing methods are combined to create sophisticated and flexible rules to scale to the needs of larger, more complex deployments. |

### How Traffic Manager works

Azure Traffic Manager enables you to control how network traffic is distributed to application deployments (endpoints) running in your different datacenters. Azure Traffic Manager [uses DNS to direct the client requests](/en-us/azure/traffic-manager/traffic-manager-how-it-works#how-clients-connect-using-traffic-manager) to the appropriate service endpoint based on a traffic\-routing method. For any profile, Traffic Manager applies the traffic\-routing method associated to it to each DNS query it receives. The traffic\-routing method determines which endpoint is returned in the DNS response.

Azure Traffic Manager supports different traffic\-routing methods to determine how to route network traffic to the various service endpoints. You select the method that best fits your requirements.

This video reviews Traffic Manager routing methods.

##### Priority routing method

Use the [priority routing method](/en-us/azure/traffic-manager/traffic-manager-routing-methods#priority-traffic-routing-method) for a primary service endpoint for all traffic. You can provide multiple backup endpoints in case the primary or one of the backup endpoints is unavailable.

##### Weighted routing method

Use the [**Weighted** routing method](/en-us/azure/traffic-manager/traffic-manager-routing-methods?branch=main#weighted-traffic-routing-method) when you want to distribute traffic across a set of endpoints based on their importance. Set the weight the same to distribute evenly across all endpoints.

##### Performance routing method

Use the [**Performance** routing method](/en-us/azure/traffic-manager/traffic-manager-routing-methods#performance-traffic-routing-method) when endpoints are in different geographic locations. Users should use the "closest" endpoint for the lowest network latency.

##### Geographic routing method

Use the [**Geographic** routing method](/en-us/azure/traffic-manager/traffic-manager-routing-methods#geographic-traffic-routing-method) to direct users to specific endpoints based on where their DNS queries originate from geographically. Good choice for regional compliance requirements.

Note

The are two other routing methods: Multivalue and Subnet. Use the [**Multivalue** routing method](/en-us/azure/traffic-manager/traffic-manager-routing-methods#multivalue-traffic-routing-method) when you want to return multiple healthy endpoints in a single DNS query response. Use the [**Subnet** routing method](/en-us/azure/traffic-manager/traffic-manager-routing-methods#subnet-traffic-routing-method) when you want to map user IP address ranges to specific endpoints.

### Check your knowledge

---

## Exercise: Create a Traffic Manager profile using the Azure portal

### Lab scenario

In this lab, you create a Traffic Manager profile to deliver high availability for the fictional Contoso Ltd organization's web application.

You create two instances of a web application deployed in two different regions (East US and West Europe). The East US region is the primary endpoint for Traffic Manager, and the West Europe region is the failover endpoint.

Then you create a Traffic Manager profile based on endpoint priority. This profile directs user traffic to the primary site running the web application. Traffic Manager continuously monitors the web application, and if the primary site in East US is unavailable, it provides automatic failover to the backup site in West Europe.

### Architecture diagram

### Job skills

* Create web apps.
* Create a Traffic Manager profile.
* Add Traffic Manager endpoints.
* Test the Traffic Manager profile.

Important

Estimated time: 35 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Summary

In this module, you learned about the Azure Load Balancer and Azure Traffic Manager.

**The main takeaways from this module are:**

* Load balancing distributes workloads to servers and services.
* Azure offers two non\-HTTP(S) load balancing solutions: Azure Load Balancer and Azure Traffic Manager.
* Azure Load Balancers can distribute workloads globally or regionally.
* Azure Load Balancers can be public (external) or internal (private).
* Azure Load Balancer has two SKUs: Standard and Gateway.
* Azure Traffic Manager is a DNS\-based network traffic load balancer.
* Azure Traffic Manager supports different traffic\-routing methods. These methods include performance, weighted, priority, geographic, multivalue, and subnet.

#### Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

* What is Azure Load Balancer? Provide benefits, features, and usage cases for the product.
* What is Azure Traffic Manager? Provide benefits, features, and usage cases for the product.
* Compare and contrast Azure Load Balancer and Azure Traffic Manager. When should you use each product? Provide usage cases.

### Learn more with self\-paced training

* [Introduction to Azure Load Balancer](/en-us/training/modules/intro-to-azure-load-balancer/). This module explains what Azure Load Balancer does, how it works, and when you should choose to use Load Balancer as a solution to meet your organization's needs.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/load-balancing-non-https-traffic-azure/_

## Fuentes
- [Load balance non-HTTP(S) traffic in Azure](https://learn.microsoft.com/en-us/training/modules/load-balancing-non-https-traffic-azure/?WT.mc_id=api_CatalogApi)
