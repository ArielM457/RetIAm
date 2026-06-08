# Design and implement network security

> Curso: AZ-700 Design and Implement Microsoft Azure Network Solutions (wwl-designing-implementing-microsoft-azure-network) · Seccion: AZ-700 Design and Implement Microsoft Azure Network Solutions
> Duracion estimada: 59 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Network security is the process of protecting resources from unauthorized access or attack by applying controls to network traffic. Azure includes a robust networking infrastructure to support your application and service security requirements.

Your security requirements might include:

* Making sure your app has proper authentication and authorization in place.
* Keeping an eye out for intrusions and having a plan to respond.
* Filtering URLs to block anything sketchy.
* Controlling who can access your application and what they can do.
* Protecting against DDoS attacks to keep everything running smoothly.

### Learning objectives

In this module, you:

* Understand how to get network security recommendations with Microsoft Defender for Cloud.
* Configure and monitor an Azure DDoS protection plan.
* Implement and manage firewalls.
* Implement network security groups (NSGs).
* Implement a web application firewall (WAF).
* Configure a monitoring environment for networking.

### Prerequisites

* Experience with networking concepts, such as IP addressing, Domain Name System (DNS), and routing.
* Experience with network connectivity methods, such as VPN or WAN.
* Experience with the Azure portal and Azure PowerShell.

---

## Get network security recommendations with Microsoft Defender for Cloud

Network security covers various technologies, devices, and processes. Security provides a set of rules and configurations designed to protect the integrity, confidentiality, and accessibility of computer networks and data. Every organization, regardless of size, industry, or infrastructure, requires a degree of network security solutions. These solutions protect from the ever\-growing risks of attacks.

Network security provides controls to secure and protect Azure networks. These controls include securing virtual networks, establishing private connections, preventing and mitigating external attacks, and securing DNS.

A full description of the network security controls can be found at [Security Control V3: Network Security on Microsoft Learn](/en-us/security/benchmark/azure/security-controls-v3-network-security).

### Using Microsoft Defender for Cloud for regulatory compliance

[Microsoft Defender for Cloud](/en-us/azure/defender-for-cloud/defender-for-cloud-introduction) helps streamline the process for meeting network regulatory compliance requirements.

The regulatory compliance dashboard shows the status of all the assessments within your environment for your chosen standards and regulations. As you act on the recommendations and reduce risk factors in your environment, your compliance posture improves. You can also view the overall compliance score, and the number of passing vs. failing assessments associated with each standard.

### Compliance controls

For each security control, you can drill down into more information.

1. Subscriptions the standard is applied on.
2. List of all controls for that standard.
3. View the details of passing and failing assessments associated with that control.
4. Number of affected resources.
5. Severity of the alert.

Tip

Learn more with the [Examine Defender for Cloud regulatory compliance standards](/en-us/training/modules/examine-defender-cloud-regulatory-compliance-standards/) module.

### Check your knowledge

---

## Deploy Azure DDoS Protection by using the Azure portal

A denial of service attack (DoS) is an attack that has the goal of preventing access to services or systems. A DoS attack originates from one location. A distributed denial of service (DDoS) attack originates from multiple networks and systems.

DDoS attacks are one of the security concerns facing customers that are moving their applications to the cloud. A DDoS attack tries to drain an APIs or application's resources, making that application unavailable to legitimate users. DDoS attacks can be targeted at any endpoint that is publicly reachable through the internet.

[Azure DDoS Protection](/en-us/azure/ddos-protection/ddos-protection-overview) protects resources in a virtual network. Protection includes virtual machine public IP addresses, load balancers, and application gateways. When coupled with the Application Gateway WAF, DDoS Protection can provide full layer 3 to layer 7 mitigation capabilities.

### Types of DDoS attacks

DDoS Protection can mitigate the following types of attacks.

* **Volumetric attacks**. These attacks flood the network layer with a substantial amount of seemingly legitimate traffic. They include UDP floods, amplification floods, and other spoofed\-packet floods.
* **Protocol attacks**. These attacks render a target inaccessible, by exploiting a weakness in the layer 3 and layer 4 protocol stack. Attacks include SYN flood attacks, reflection attacks, and other protocol attacks.
* **Resource (application) layer attacks**. These attacks target web application packets, to disrupt the transmission of data between hosts. Attacks include HTTP protocol violations, SQL injection, cross\-site scripting, and other layer 7 attacks.

### DDoS implementation tiers

Azure DDoS Protection offers two tiers: DDoS IP Protection and DDoS Network Protection. Both tiers provide active traffic monitoring, always\-on detection, and automatic attack mitigation. The tiers include application\-based mitigation policies, metrics and alerts, mitigation reports, and integration with Firewall Manager.
Each tier is designed to cater to different needs and scenarios.

* **DDoS IP Protection**. This tier is suitable for protecting individual public IP addresses. It's ideal for scenarios where you have fewer than 15 public IP resources to protect.
* **DDoS Network Protection**. This tier offers a few more benefits such as rapid response support and cost protection. Opt for this tier when you have a larger deployment with more than 15 public IP addresses.

### Azure DDoS protection features

Some of Azure DDoS protection features include:

* **Native platform integration**. Natively integrated into Azure and configured through portal.
* **Turnkey protection**. Simplified configuration protecting all resources immediately.
* **Always\-on traffic monitoring**. Your application traffic patterns are monitored 24 hours a day, 7 days a week, looking for indicators of DDoS attacks.
* **Adaptive tuning**. Profiling and adjusting to your service's traffic.
* **Attack analytics**. Get detailed reports in five\-minute increments during an attack, and a complete summary after the attack ends.
* **Attack metrics and alerts**. Summarized metrics from each attack are accessible through Azure Monitor. Alerts can be configured at the start and stop of an attack, and over the attack's duration, using built\-in attack metrics.
* **Multi\-layered protection**. When deployed with a WAF, DDoS Protection protects both at the network layer and the application layer.

### Check your knowledge

---

## Exercise: Configure DDoS Protection on a virtual network using the Azure portal

### Lab scenario

In this exercise, you're going to run a mock DDoS attack on the virtual network. The following steps walk you through creating a virtual network, configuring DDoS Protection, and creating an attack which you can observe and monitor with the help of telemetry and metrics.

### Architecture diagram

### Job skills

* Create a DDoS Protection plan.
* Enable DDoS Protection on a new virtual network.
* Configure DDoS telemetry.
* Configure DDoS diagnostic logs.
* Configure DDoS alerts.
* Monitor a DDoS test attack.

Important

Estimated time: 40 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Deploy Network Security Groups by using the Azure portal

A [Network Security Group (NSG)](/en-us/azure/virtual-network/network-security-groups-overview) in Azure allows you to filter network traffic to and from Azure resources in an Azure virtual network.

### Characteristics of network security groups

Let's look at the characteristics of network security groups.

* A network security group contains a list of security rules that allow or deny inbound or outbound network traffic.
* A network security group can be associated to a subnet or a network interface.
* A network security group can be associated multiple times.
* You create a network security group and define security rules in the Azure portal.

### NSG security rules

A network security group contains security rules that allow or deny inbound or outbound network traffic to Azure resources. For each rule, you can specify source and destination, port, and protocol. A network security group contains zero, or as many rules as desired, within Azure subscription limits. Each rule has these properties.

* Azure defines default **inbound** security rules for your network security group. These rules deny all inbound traffic except traffic from your virtual network and Azure load balancers.
* Azure defines default **outbound** security rules for your network security group. These rules only allow outbound traffic to the internet and your virtual network.

Each network security group and its defined security rules are evaluated independently. Azure processes the conditions in each rule defined for each virtual machine in your configuration. \- Effective security rules view is a feature in Azure Network Watcher that you can use to view the aggregated inbound and outbound rules applied to a network interface. It provides visibility into security and admin rules applied to a network interface.

* For inbound traffic, Azure first processes network security group security rules for any associated subnets and then any associated network interfaces.
* For outbound traffic, the process is reversed. Azure first evaluates network security group security rules for any associated network interfaces followed by any associated subnets.

Tip

Learn more about network security groups in the [Configure network security groups](/en-us/training/modules/configure-network-security-groups/) module.

### Check your knowledge

---

## Design and implement Azure Firewall

[Azure Firewall](/en-us/azure/firewall/overview) is a managed, cloud\-based network security service that protects your Azure virtual network resources. Azure firewall has built\-in high availability and unrestricted cloud scalability. Azure Firewall works not only for traffic to and from the internet, but also internally. Internal traffic filtering includes spoke\-to\-spoke traffic and hybrid cloud traffic between your on\-premises network and your Azure virtual network.

### When to use Azure Firewall

Azure Firewall has three [SKUs](/en-us/azure/firewall/choose-firewall-sku): Azure Firewall Basic, Azure Firewall Standard, and Azure Firewall Premium.

* You want to protect your network against infiltration.
* You want to protect your network against user error.
* Your business includes e\-commerce or credit card payments.
* You want to configure spoke\-to\-spoke connectivity.
* You want to monitor incoming and outgoing traffic.

#### How to choose the SKU

All SKUs support availability zone deployment for zone\-redundant high availability. All SKUs include policy analytics for tracking rule usage over time and managing redundant or conflicting rules.

* **Basic SKU**: Up to 250 Mbps; SMB environments; has threat intelligence in alert mode only.
* **Standard SKU**: Up to 30 Gbps; enterprise environments; L3–L7 filtering, DNS proxy, web categories, and threat intelligence.
* **Premium SKU**: Up to 100 Gbps; regulated/sensitive environments (healthcare, payment); adds TLS inspection, IDPS, full URL filtering, and PCI DSS compliance.

### What are Azure Firewall rules?

An Azure Firewall denies all traffic by default, until rules are manually configured to allow traffic. Rules are organized inside Rule Collections that are contained in Rule Collection Groups. In the Azure Firewall, you can configure NAT rules, network rules, and applications rules.

| Rule type | Description |
| --- | --- |
| NAT | Translate and filter inbound internet traffic based on your firewall's public IP address and a specified port number. For example, to enable a remote desktop connection to a virtual machine, you might use a NAT rule to translate your firewall's public IP address and port 3389 to the private IP address of the virtual machine. |
| Application | Filter traffic based on an FQDN. For example, you might use an application rule to allow outbound traffic to access an Azure SQL Database instance using the FQDN server10\.database.windows.net. |
| Network | Filter traffic based on one or more of the following three network parameters: IP address, port, and protocol. For example, you might use a network rule to allow outbound traffic to access a particular DNS server at a specified IP address using port 53\. |

Azure Firewall applies rules in priority order. Rules based on threat intelligence are always given the highest priority and are processed first. After that, rules are applied by type: NAT rules, then network rules, then application rules. Within each type, rules are processed according to the priority values you assign when you create the rule, from lowest value to highest value.

Tip

Learn more about Azure Firewall in the [Introduction to Azure Firewall](/en-us/training/modules/introduction-azure-firewall/) module.

### Check your knowledge

---

## Exercise: Deploy and configure Azure Firewall using the Azure portal

### Lab scenario

Being part of the Network Security team at Contoso, your next task is to create firewall rules to allow/deny access to certain websites.

### Architecture diagram

### Job skills

* Create a virtual network and subnets.
* Create a virtual machine.
* Deploy the firewall and firewall policy.
* Create a default route.
* Configure an application rule.
* Configure a network rule.
* Configure a Destination NAT (DNAT) rule.
* Change the primary and secondary DNS address for the server's network interface.
* Test the firewall.

Important

Estimated time: 60 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Secure your networks with Azure Firewall Manager

If you manage multiple firewalls, it's often difficult to keep the firewall rules in sync. Central IT teams need a way to define base firewall policies and enforce them across multiple business units. At the same time, DevOps teams want to create their own local derived firewall policies that are implemented across organizations.

[Azure Firewall Manager](/en-us/azure/firewall-manager/overview) helps solve these problems. Azure Firewall Manager provides centralized configuration and management across multiple Azure Firewall instances. Azure Firewall Manager lets you create one or more firewall policies and rapidly apply them to multiple firewalls.

Firewall Manager can provide security management for secured virtual hubs and hub virtual networks.

* **Secured Virtual Hub**. A Microsoft\-managed resource that enables you to easily create hub and spoke architectures. When you associate policies, you're using a secured virtual hub. The underlying resource is a virtual WAN hub.
* **Hub Virtual Network**. A standard Azure virtual network that you create and manage. When you associate firewall policies with this type of hub, you're creating a hub virtual network. This architecture's underlying resource is a virtual network.

#### Azure Firewall Manager capabilities

Azure Firewall Manager provides six key capability areas:

* **Central deployment and configuration**. Manage Azure Firewall deployment and policies across multiple subscriptions and regions.
* **Hierarchical policies**. Create global policies authored by central IT with locally authored overrides.
* **Security partner provider integration**. Route Internet\-bound VNet and branch traffic through Zscaler, Check Point, or iboss while Azure Firewall handles private traffic in the same hub.
* **Centralized route management**. Automatically route spoke traffic to secured hubs without manually configuring user\-defined routes.
* **DDoS protection plan management**. Associate virtual networks with a DDoS plan directly from Firewall Manager.
* **WAF policy management**. Centrally create, view, and associate WAF policies to Front Door and Application Gateway across subscriptions.

#### Azure Firewall Manager decision criteria

Administrators who protect multiple Azure virtual networks use rules to control traffic throughout their perimeter networks. As a virtual network infrastructure grows, it can become more complex to manage. Administrators benefit from using Firewall Manager to centralize configuration of Azure Firewall rules and settings. Here are some factors that help you decide whether Firewall Manager can benefit your organization.

| Criteria | Analysis |
| --- | --- |
| Complexity | A key question if you're considering Firewall Manager is "How complex are my organization's firewall and security requirements?" If you have a simple virtual\-network structure with limited firewalls, you probably don't need Firewall Manager. |
| Need for centralized management | The next question to ask is "Will I benefit from a more centralized approach to managing my virtual networks and firewalls?" If the answer is yes, consider implementing Firewall Manager. |
| Number of virtual networks | Do you have several virtual networks with many distinct Azure Firewalls? Firewall Manager could benefit your organization. Conversely, do you have only a few virtual networks? Firewall Manager might not be beneficial for you. |

Tip

Learn more about Azure Firewall in the [Introduction to Azure Firewall Manager](/en-us/training/modules/introduction-azure-firewall/) module.

### Check your knowledge

---

## Exercise: Secure your Virtual Hub using Azure Firewall Manager

### Lab scenario

In this lab, you secure your virtual hub with Azure Firewall Manager.

### Architecture diagram

### Job skills

* Create two spoke virtual networks and subnets.
* Create the secured virtual hub.
* Connect the hub and spoke virtual networks.
* Deploy the servers.
* Create a firewall policy and secure your hub.
* Associate the firewall policy.
* Route traffic to your hub.
* Test the application rule.
* Test the network rule.

Important

Estimated time: 35 minutes.
To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Launch the exercise, and follow the instructions. When finished, be sure to return to this page so you can continue learning.

---

## Implement a Web Application Firewall

[Web Application Firewall (WAF)](/en-us/azure/web-application-firewall/overview) provides centralized protection of your web applications from common exploits and vulnerabilities. SQL injections and cross\-site scripting are among the most common attacks.

Preventing attacks in application code is challenging. Prevention can require rigorous maintenance, patching, and monitoring at multiple layers of the application. A centralized WAF helps make security management simpler. A WAF also gives application administrators better assurance of protection against threats and intrusions. A WAF solution can react to a security threat faster by centrally patching a known vulnerability, instead of securing each individual web application.

### Web Application Firewall policy modes

There are two WAF policy modes: Detection and Prevention. By default, the WAF policy is in Detection mode. In Detection mode, WAF doesn't block any requests. Instead, requests matching the WAF rules are logged. In Prevention mode, requests that match rules are blocked and logged.

The Web Application Firewall works with the Application Gateway and Azure Front Door.

### Microsoft managed rule sets, rule groups, and rules

Azure Web Application Firewall thwarts known exploits by applying rules to an app's incoming HTTP/HTTPS requests. A rule is designed to recognize and prevent a particular threat.

The rules that Azure Web Application Firewall uses to detect and block common vulnerabilities are mostly managed rules that belong to various rule groups. Each rule group is a collection of rules, and a managed rule set is collection of rule groups. Managed rule sets include Microsoft Threat Intelligence based rule groups, CVE (Common Vulnerabilities and Exposures) rule groups, and core rule groups (CRS). Common threats the WAF checks for are:

* **Cross\-site scripting**. A threat actor uses a web application to send malicious code to another user's web browser.
* **Local file inclusion**. An attacker exploits vulnerabilities in a server's handling of include statements, most often in PHP scripts.
* **PHP injection attacks**. The attacker inserts text specially configured to trick the server into running PHP commands.
* **Remote command execution**. The attacker tricks a server into running commands associated with the server's operating system.
* **Session fixation**. An attacker exploits a web app vulnerability that allows the attacker to obtain a valid session ID.
* **SQL injection protection**. In a web form field, the attacker inserts (or "injects") text specially configured to trick the server into running SQL commands.
* **Protocol attackers**. An attacker inserts specially configured text into an HTTP/HTTPS request header.

### Check your knowledge

---

## Summary and resources

In this module, you explored a range of network security features.

**The main takeaways from this module are:**

* Microsoft Defender for Cloud helps streamline the process for meeting network regulatory compliance requirements.
* Azure DDoS Protection protects resources in a virtual network. Protection includes virtual machine public IP addresses, load balancers, and application gateways. DDoS Protection can mitigate volumetric attacks, protocol attacks, and resource layer attacks. DDoS Protection offers two tiers: DDoS IP Protection, and DDoS Network Protection.
* A Network Security Group (NSG) in Azure allows you to filter network traffic to and from Azure resources in an Azure virtual network. An NSG contains default security rules that allow or deny inbound or outbound network traffic.
* Azure Firewall is a managed, cloud\-based network security service that protects your Azure virtual network resources. Azure Firewall has three SKUs: Basic, Standard, and Premium. In the Azure Firewall, you can configure NAT rules, network rules, and applications rules.
* Azure Firewall Manager provides centralized configuration and management across multiple Azure Firewall instances. Azure Firewall Manager lets you create one or more firewall policies and rapidly apply them to multiple firewalls. Firewall Manager can provide security management for secured virtual hubs and hub virtual networks.
* Web Application Firewall provides centralized protection of your web applications from common exploits and vulnerabilities. There are two WAF policy modes: Detection and Prevention. WAF works with the Application Gateway and Azure Front Door.

### Learn more with Copilot

Copilot can assist you in configuring Azure infrastructure solutions. Copilot can compare, recommend, explain, and research products and services where you need more information. Open a Microsoft Edge browser and choose Copilot (top right) or navigate to copilot.microsoft.com. Take a few minutes to try these prompts and extend your learning with Copilot.

* Provide a description of common Azure network security features. Provide usage examples.
* List best practices for implementing Azure network security.

### Learn more with self\-paced training

* [Configure network security groups](/en-us/training/modules/configure-network-security-groups/). Learn how to implement network security groups, and ensure network security group rules are correctly applied.
* [Introduction to Azure Firewall](/en-us/training/modules/introduction-azure-firewall/). Describe how Azure Firewall protects Azure virtual network resources. Topics include features, rules, and deployment options.
* [Introduction to Azure Firewall Manager](/en-us/training/modules/introduction-azure-firewall/). Describe whether you can use Azure Firewall Manager to provide central security policy and route management. Evaluate whether Azure Firewall Manager can help secure your cloud perimeters.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/design-implement-network-security-monitoring/_

## Fuentes
- [Design and implement network security](https://learn.microsoft.com/en-us/training/modules/design-implement-network-security-monitoring/?WT.mc_id=api_CatalogApi)
