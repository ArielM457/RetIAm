# Load balance HTTP(S) traffic in Azure

> Curso: AZ-700 Design and Implement Microsoft Azure Network Solutions (wwl-designing-implementing-microsoft-azure-network) · Seccion: AZ-700 Design and Implement Microsoft Azure Network Solutions
> Duracion estimada: 42 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Application Gateway and Azure Front Door are powerful tools provided by Microsoft Azure to manage web traffic, ensure high availability, and secure web applications.

Imagine you're a system administrator for a large e\-commerce company. Your company's website experiences heavy traffic, especially during peak shopping seasons. The website is hosted on a pool of servers, and you need to balance the load effectively to ensure smooth operation. Additionally, you need to protect your web applications from common threats and ensure secure data delivery. You also want to provide a fast and reliable user experience by delivering content swiftly to end users. To achieve these goals, you decide to use Azure Application Gateway and Azure Front Door.

### Learning objectives

In this module, you learn to:

* Implement Azure Application Gateway
* Implement Azure Front Door

The topics covered in this module include:

* Designing and implementing Azure Application Gateway
* Configuring Azure Application Gateway for load balancing
* Creating and testing an Azure Application Gateway
* Designing, configuring, and securing Azure Front Door

### Prerequisites

* Experience with networking concepts, such as IP addressing, Domain Name System (DNS), and routing.
* Experience with network connectivity methods, such as VPN or WAN.
* Experience with the Azure portal.

---

## Design Azure Application Gateway

The [Azure Application Gateway](/en-us/azure/application-gateway/overview) processes network traffic to web apps hosted on a pool of web servers. The processing performed by Azure Application Gateway includes load balancing HTTP traffic and inspecting traffic using a web application firewall. This type of routing is known as application layer (OSI layer 7\) load balancing. A

Azure Application Gateway v2 includes the following features.

* Support for the HTTP, HTTPS, HTTP/2, and WebSocket protocols.
* A web application firewall (WAF) to protect against web application vulnerabilities.
* SSL/TLS termination at the gateway, offloading encryption overhead from backend servers.
* End\-to\-end TLS encryption for compliance scenarios requiring encryption to the backend.
* Autoscaling to dynamically adjust capacity as your web traffic load change.
* Connection draining allowing graceful removal of backend pool members during planned service updates.
* Session stickiness to ensure client requests in the same session are routed to the same backend server.
* Path and URL based routing.
* Zone redundancy, Azure key vault integration, and HTTP header rewrite.

Note

Support for Application Gateway V1 ends on April 28, 2026\.

### How Azure Application Gateway works

Let's review the [Azure Application Gateway components](/en-us/azure/application-gateway/application-gateway-components).

* **Front\-end IP address**. Client requests are received through a front\-end IP address. You can configure the Application Gateway to have a public IP address, a private IP address, or both.
* **Listeners**. A listener is a logical entity that checks for incoming connection requests. A listener accepts a request if the protocol, port, hostname, and IP address match the listener's configuration. You must have at least one listener.
* **Request routing rules**. A request routing rule is a key component of an application gateway because it determines how to route traffic on the listener. The rule binds the listener, the backend server pool, and the backend HTTP settings. When a listener accepts a request, the request routing rule forwards the request to the backend or redirects it elsewhere. If the request is forwarded to the backend, the request routing rule defines which backend server pool to forward it to.
* **Backend pools**. A backend pool is a collection of web servers. Backend targets can include: a fixed set of virtual machines, a virtual machine scale\-set, an app hosted by Azure App Services, or a collection of on\-premises servers. The backend pool receives and processes requests.
* **Health probes**. Health probes determine which servers are available for load\-balancing in a backend pool. Servers are automatically added and removed from the backend pool based on their availability.

Tip

Learn more about Azure Application Gateway check out the [Introduction to Azure Application Gateway](/en-us/training/modules/intro-to-azure-application-gateway/) module.

### Check your knowledge

---

## Configure Azure Application Gateway

This diagram explains how the Azure Application Gateway components work together.

### Routing configuration

One of the most important gateway configuration settings is the routing rules. The Azure Application Gateway has two primary methods of routing client requests: path\-based and multiple sites.

#### Path\-based routing

[Path\-based routing](/en-us/azure/application-gateway/url-route-overview) sends requests with different URL paths to different pools of back\-end servers. For example, you could direct video requests to a back\-end pool optimized to handle video streaming. You could also direct image requests to a pool of servers that handles image retrieval.

#### Multiple site routings

[Multiple site routing](/en-us/azure/application-gateway/multiple-site-overview) configures more than one web application on the same Application Gateway instance. In a multiple site configuration, you register multiple DNS names (CNAMEs) for the IP address of the application gateway, specifying the name of each site. Application Gateway uses separate listeners to wait for requests for each site. Each listener passes the request to a different rule, which can route the requests to servers in a different back\-end pool. For example, you could direct all requests for `http://contoso.com` to a specific backend pool.

This video reviews the routing methods.

### Other routing capabilities

Along with path\-based routing and multiple site hosting, there are a few other capabilities when routing with Application Gateway.

* [Redirection](/en-us/azure/application-gateway/redirect-overview). Redirection can be used to another site, or from HTTP to HTTPS. For example, redirecting HTTP requests to a secure HTTPS shopping site.
* Rewrite HTTP headers. HTTP headers allow the client and server to pass additional information with the request or the response.
* Custom error pages. Application Gateway allows you to create custom error pages instead of displaying default error pages. You can use your own branding and layout using a custom error page.

Tip

Learn more about Azure Application Gateway routing check out the [Load balance your web service traffic with Application Gateway](/en-us/training/modules/load-balance-web-traffic-with-application-gateway/) module.

### Check your knowledge

---

## Exercise: Deploy Azure Application Gateway

### Lab scenario

In this lab, you use the Azure portal to create an application gateway. Then you test it to make sure it works correctly.

### Architecture diagram

### Job skills

* Create an application gateway.
* Add backend targets.
* Use a template to create the virtual machines.
* Add backend servers to backend pool.
* Test the application gateway.

Important

Estimated time: 25 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Design and configure Azure Front Door

[Azure Front Door](/en-us/azure/frontdoor/front-door-overview) is Microsoft’s modern cloud Content Delivery Network (CDN) that provides fast, reliable, and secure access between your users and your applications. Azure Front Door delivers your content using the Microsoft’s global edge network with hundreds of global and local POPs distributed around the world close to both your enterprise and consumer end users.

### Azure Front Door tiers

Note

Azure Front Door has three tiers: Standard, Premium, and Classic. This module focuses on Standard and Premium. New resources will not be supported on Azure Front Door Classic after August 2025\.

**Azure Front Door Standard** provides both content delivery and security features.

* Provide for both static and dynamic content acceleration.
* Support global load balancing.
* Implement SSL offload.
* Implement domain and certificate management.
* Benefit from enhanced traffic analytics.
* Custom WAF rules for basic protection against known attack patterns.

**Azure Front Door Premium** is security optimized and provides other features.

* BOT protection.
* Private Link support.
* Integration with Microsoft Threat Intelligence and security analytics.
* Microsoft\-managed WAF rule sets that autoupdate against OWASP top\-10 and emerging threats.

### Azure Front Door usage cases

This diagram shows a user request processed by Azure Front Door.

1. A user is requesting `www.contoso.com`. This request is routed from the client to Azure Front Door. Azure Front Door resides at the edge of the Microsoft Global Network. In Azure, an edge location is a data center that's geographically closer to end\-users than traditional Azure regions. These locations are designed to cache content and deliver services with lower latency, improving the speed and responsiveness of applications for users worldwide.
2. Azure Front Door determines where to direct the client request. The routing process includes the web application firewall, routing rules, rules engine, and caching configuration.
3. A nonspecific request can be routed to any one of the three regions.
4. A search request can be routed to a specific region optimized for search.
5. A request can even be routed to a region with another cloud service.

### Other things to know

* **Routing algorithm**. The Azure Front Door routing algorithm first matches based on HTTP protocol, then frontend host, and then Path. The Standard and Premium tiers also support a Rules Engine that uses regular expressions and server variables for complex routing conditions.
* **Response codes**. Azure Front Door response codes help clients understand the purpose of the redirect. You can set the protocol used for redirection. The most common use case of the redirect feature is to set HTTP to HTTPS redirection.
* **Health probes**. Front Door periodically sends a synthetic HTTP/HTTPS request to each of your configured backends. Front Door then uses these responses from the probe to determine the "best" backend resources to route your client requests.

### Check your knowledge

---

## Summary

In this module, you learned about Azure Application Gateway and Azure Front Door.

**The main takeaways from this module are:**

* Azure Application Gateway processes traffic to web apps hosted on a pool of web servers.
* Azure Application Gateway provides OSI Layer 7 load balancing at a regional level.
* Azure Application Gateway components include: the frontend, listeners, request routing rules, backend pools, and health probes.
* The Azure Application Gateway uses path\-based routing and multiple\-site routing.
* Azure Front Door is a Content Delivery Network that provides fast, reliable, and secure access between your users and your applications.
* Azure Front Door provides OSI Layer 7 load balancing at the global level.
* Azure Front Door routes request routing based on HTTP protocol, frontend host, and the requested path.

#### Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

* What is the Azure Application Gateway and what are the main features of the product? Provide usage scenarios.
* What is the Azure Front Door and what are the main features of the product? Provide usage scenarios.
* Compare and contrast the Azure Application Gateway with Azure Front Door.

### Learn more with self\-paced training

* [Introduction to Azure Application Gateway](/en-us/training/modules/intro-to-azure-application-gateway/). Improve application resilience by distributing load across multiple servers and use path\-based routing to direct web traffic.
* [Load balance your web service traffic with Application Gateway](/en-us/training/modules/load-balance-web-traffic-with-application-gateway/). Improve application resilience by distributing load across multiple servers and use path\-based routing to direct web traffic.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/load-balancing-https-traffic-azure/_

## Fuentes
- [Load balance HTTP(S) traffic in Azure](https://learn.microsoft.com/en-us/training/modules/load-balancing-https-traffic-azure/?WT.mc_id=api_CatalogApi)
