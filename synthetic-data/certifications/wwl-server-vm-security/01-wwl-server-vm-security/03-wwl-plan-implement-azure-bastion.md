# Plan and implement Azure Bastion

> Curso: Implement security for servers and virtual machines (wwl-server-vm-security) · Seccion: Implement security for servers and virtual machines
> Duracion estimada: 25 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Manufacturing operates factory floor systems that require remote management access for operational engineers. Currently, these virtual machines expose RDP (port 3389\) and SSH (port 22\) to the internet through network security group rules with broad source IP ranges. A recent threat analysis revealed active brute\-force and credential\-stuffing attacks targeting these open ports. The security team needs to eliminate public RDP and SSH exposure while preserving legitimate operational access for engineers who manage these systems.

Azure Bastion provides secure remote connectivity to Azure virtual machines without exposing RDP and SSH ports to the internet. In this module, you learn how to plan, deploy, and configure Azure Bastion to protect factory systems while maintaining operational workflows.

### Learning objectives

* Select the appropriate Azure Bastion SKU based on scale, feature, and cost requirements
* Deploy and configure Azure Bastion in an Azure virtual network
* Connect to Azure virtual machines through Azure Bastion using portal and native client methods
* Configure advanced Bastion features including native client support, shareable links, and session recording

### Prerequisites

* Familiarity with Azure virtual networks, subnets, and network security groups
* Understanding of RDP and SSH remote access protocols
* Experience with Azure virtual machine management
* Access to an Azure subscription with permissions to create network resources

Now that you understand the security challenge and what Azure Bastion provides, you're ready to explore how to select the right Bastion SKU and plan the deployment architecture.

---

## Plan Azure Bastion deployment

Contoso Manufacturing's factory systems need secure remote access without the attack surface created by public RDP and SSH ports. Azure Bastion provides browser\-based and native client connectivity through encrypted TLS 443 connections, eliminating the need for public IP addresses on virtual machines and open management ports in network security groups.

### Understand Azure Bastion connectivity model

Azure Bastion acts as a secure gateway between users and target virtual machines. When you connect through Bastion, the service establishes an RDP or SSH session from the Bastion host directly to the target VM over the Azure backbone network. The user's client connects to the Bastion host using HTTPS over port 443, which passes through most corporate firewalls without special exceptions.

This architecture removes several attack vectors. Virtual machines no longer need public IP addresses for remote access. Network security groups no longer require inbound rules for RDP port 3389 or SSH port 22 from internet sources. All remote connectivity flows through the hardened Bastion service, which provides a single, auditable access point.

### Select the appropriate Bastion SKU

Azure Bastion offers four SKUs with distinct capabilities and cost structures. The right choice depends on your access patterns, user count, required features, and budget constraints.

| SKU | Host Units | Concurrent Sessions | Browser Access | Native Client | Shareable Links | Session Recording | Typical Use Case |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Developer | Free tier | One user | Yes | No | No | No | Individual development, testing |
| Basic | 2 (fixed) | 40 RDP / 80 SSH | Yes | No | No | No | Small teams, browser\-only access |
| Standard | 2–50 (configurable) | 20 RDP \+ 40 SSH per instance | Yes | Yes | Yes | No | Enterprise deployments, native tooling |
| Premium | 2–50 (configurable) | 20 RDP \+ 40 SSH per instance | Yes | Yes | Yes | Yes | Regulated environments, compliance |

The **Developer SKU** provides no\-cost access for individual users during development and testing. This tier supports a single concurrent user and lacks scaling capabilities, making it unsuitable for production team environments.

The **Basic SKU** offers browser\-based access through its fixed allocation of 2 host units, supporting up to 40 concurrent RDP sessions or 80 concurrent SSH sessions. Users connect through the Azure portal using the browser\-based RDP or SSH client. This tier works well for small teams that don't require native RDP client features or significant scaling.

The **Standard SKU** adds native client support, IP\-based connections, and configurable scaling from 2 to 50 host units. Native client support allows users to connect using their existing RDP clients (such as Microsoft Remote Desktop or Windows App) and SSH tools through an Azure CLI tunnel command. IP\-based connections enable administrators to connect to virtual machines by specifying an IP address rather than selecting from the portal's VM list, which proves essential for hub\-spoke architectures where Bastion in the hub virtual network provides access to spoke VNets through peering. Shareable links provide time\-limited URL\-based access for users without Azure portal credentials, useful for contractor or vendor scenarios.

The **Premium SKU** adds session recording capabilities that capture complete RDP and SSH session activity to an Azure Storage account for compliance and security auditing. Private\-only mode removes the public IP address requirement from the Bastion host itself for air\-gapped or highly restricted network environments.

For Contoso Manufacturing, the **Standard SKU** provides the right balance. Factory engineers already use native RDP clients with custom configurations, and the native client tunnel feature preserves this workflow. The IP\-based connection capability allows Bastion to be deployed in the hub virtual network while serving factory VMs in spoke VNets.

### Design the network architecture

Azure Bastion deploys into a dedicated subnet within an Azure virtual network. This subnet must be named exactly **AzureBastionSubnet** and sized with a minimum /26 prefix (64 IP addresses). The /26 minimum ensures sufficient address space for the Bastion service infrastructure and future scaling requirements.

Organizations with hub\-spoke network topologies face a deployment choice: deploy Bastion in the hub virtual network to serve all spoke VNets, or deploy separate Bastion instances in each spoke virtual network. A hub deployment reduces costs (one Bastion host instead of many) and simplifies management, but requires Standard or Premium SKU with IP\-based connection capability. The Bastion host in the hub connects to VMs in spoke VNets through VNet peering relationships. With IP\-based connections enabled, administrators specify the target VM's IP address directly rather than selecting from the portal's resource list.

Per\-VNet deployment provides isolation and removes dependencies on virtual network peering, but multiplies costs and administrative overhead. This approach makes sense for VNets with strict isolation requirements or when different teams manage separate VNets independently.

Contoso Manufacturing operates a hub\-spoke topology with factory systems distributed across spoke VNets. Deploying Bastion with Standard SKU in the hub virtual network provides access to all factory VMs while maintaining a single managed endpoint and minimizing costs.

### Configure public IP and NSG requirements

Azure Bastion requires a Standard SKU static public IP address for inbound connectivity from user clients. This public IP attaches to the Bastion host itself, not to the target virtual machines. The target VMs can operate without any public IP addresses, which eliminates their exposure to internet\-based attacks.

The AzureBastionSubnet requires a network security group with specific inbound and outbound rules. Inbound rules must allow HTTPS (port 443\) from the internet to permit user connections, and allow port 443 from the GatewayManager service tag to enable Azure control plane operations. Outbound rules must allow traffic to target VMs on ports 3389 (RDP) and 22 (SSH), and allow port 443 to the AzureCloud service tag for Azure service dependencies.

These NSG requirements differ from typical subnet NSGs because they accommodate both user\-facing traffic (inbound 443 from Internet) and backend service communication (GatewayManager, AzureCloud). Restrictive NSGs that block these required flows prevent Bastion from functioning.

### Plan for scaling and performance

Each instance supports 20 concurrent RDP sessions or 40 concurrent SSH sessions. The Standard and Premium SKUs allow scaling from 2 to 50 instances, providing capacity for up to 1,000 concurrent RDP sessions or 2,000 concurrent SSH sessions at maximum scale. Host unit scaling happens manually through the Azure portal or programmatically through Azure CLI or Azure PowerShell.

Performance planning considers both the number of concurrent users and the bandwidth requirements of active sessions. RDP sessions with high\-resolution displays or multimedia content consume more bandwidth than basic SSH terminal sessions. Organizations with peak usage periods should configure host units to handle maximum concurrent load rather than average load.

Contoso Manufacturing identified 40 engineers who require factory VM access, with typical peak concurrency of 15 simultaneous sessions. The default 2 host units provide sufficient capacity, but the team configured four host units to accommodate growth and unexpected surge scenarios.

Now that you understand how to select the appropriate SKU and design the network architecture, you're ready to deploy and configure Azure Bastion in your environment.

---

## Deploy and configure Azure Bastion

Deploying Azure Bastion transforms your virtual network from exposing individual VM management ports to providing a centralized, secure gateway. The deployment process creates the Bastion host infrastructure, configures networking components, and enables the features you selected during planning.

### Prepare the virtual network

Before creating the Bastion resource, you prepare the target virtual network with required networking components. The deployment process requires a dedicated subnet named exactly **AzureBastionSubnet** with a minimum /26 address prefix. This subnet name is case\-sensitive and mandatory—the Bastion deployment fails if the subnet has any other name.

To create the AzureBastionSubnet, navigate to your virtual network in the Azure portal, select **Subnets**, and add a new subnet with the name AzureBastionSubnet and a CIDR range that provides at least 64 IP addresses. For example, if your virtual network uses 10\.0\.0\.0/16, you might allocate 10\.0\.1\.0/26 for the Bastion subnet. This subnet must not overlap with existing subnets in the virtual network.

You also create a Standard SKU static public IP address. In the Azure portal, create a new Public IP address resource with SKU set to Standard and assignment set to Static. The public IP provides the external endpoint for user connections to the Bastion service. Tag this resource appropriately to identify its purpose and relationship to the Bastion deployment.

### Deploy the Bastion host

Azure Bastion deploys through the Azure portal, Azure CLI, Azure PowerShell, or infrastructure\-as\-code templates. The portal provides the most straightforward experience for initial deployments.

To deploy through the portal, navigate to your virtual network and select **Bastion** from the security section. Select **Create a Bastion** to launch the deployment wizard. Configure the following settings:

* **Name**: Provide a descriptive name such as bastion\-hub\-prod
* **Region**: Must match the virtual network's region
* **Tier**: Select Developer, Basic, Standard, or Premium based on your planning decisions
* **Instance count**: For Standard or Premium, specify the number of host units (2–50\)
* **Virtual network**: Select the virtual network containing the AzureBastionSubnet
* **Subnet**: Automatically populated with AzureBastionSubnet
* **Public IP address**: Select the Standard static public IP you created

The deployment process typically completes in 5–10 minutes. During this time, Azure deploys the Bastion infrastructure, configures networking, and validates the subnet and public IP configuration.

### Configure advanced features

After the basic Bastion deployment completes, you configure advanced features based on your SKU and requirements. These features enable native client support, shareable links, and session recording capabilities.

#### Enable native client support

Native client support (Standard and Premium SKUs) allows users to connect using standard RDP clients and SSH tools through an Azure CLI tunnel. This feature preserves existing workflows for users who rely on specific RDP client configurations, clipboard operations, or file transfer capabilities.

To enable native client support, navigate to your Bastion resource in the Azure portal and select **Configuration**. Toggle **Native Client Support** to **Enabled** and select **Apply**. This configuration change takes a few minutes to propagate.

With native client support enabled, users install the Azure CLI bastion extension and use the `az network bastion tunnel` command to establish a local port tunnel. They then connect their RDP client to localhost on the specified port, and the Bastion service forwards the connection to the target VM.

#### Configure shareable links

Shareable links (Standard and Premium SKUs) generate time\-limited URLs that provide browser\-based access without requiring Azure portal credentials. This capability supports contractor access, vendor troubleshooting scenarios, or temporary access grants.

Enable shareable links in the Bastion **Configuration** page by toggling **Shareable Link** to **Enabled**. After enabling this feature, you generate links for specific virtual machines through the VM's Connect blade. Each shareable link includes an expiration time and optionally restricts access to specific credentials.

#### Enable session recording

Session recording (Premium SKU only) captures complete RDP and SSH session activity to an Azure Storage account. This feature supports compliance requirements, security investigations, and audit trails.

To configure session recording, you first create or designate an Azure Storage account with blob storage. This account should have appropriate access controls and retention policies aligned with your compliance requirements. Navigate to the Bastion resource, select **Session Recording** under Monitoring, and specify the storage account and container. Toggle session recording to **Enabled** and configure the recording scope (all sessions or specific users/groups).

Recorded sessions appear as individual files in the designated storage container. Each recording includes the complete session activity in a format that can be replayed for review. Configure storage lifecycle management policies to automatically archive or delete recordings after your required retention period.

### Configure network security group rules

The AzureBastionSubnet requires a network security group with specific inbound and outbound rules to support Bastion operations. While you can associate a new or existing NSG with the subnet, the rules must permit required traffic flows.

Required inbound rules:

| Priority | Name | Source | Source Ports | Destination | Destination Ports | Protocol | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | AllowHttpsInbound | Internet | \* | \* | 443 | TCP | Allow |
| 110 | AllowGatewayManagerInbound | GatewayManager | \* | \* | 443 | TCP | Allow |
| 120 | AllowAzureLoadBalancerInbound | AzureLoadBalancer | \* | \* | 443 | TCP | Allow |
| 130 | AllowBastionHostCommunication | Virtual network | \* | Virtual network | 8080, 5701 | \* | Allow |

Required outbound rules:

| Priority | Name | Source | Source Ports | Destination | Destination Ports | Protocol | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | AllowSshRdpOutbound | \* | \* | Virtual network | 22, 3389 | \* | Allow |
| 110 | AllowAzureCloudOutbound | \* | \* | AzureCloud | 443 | TCP | Allow |
| 120 | AllowBastionCommunication | Virtual network | \* | Virtual network | 8080, 5701 | \* | Allow |
| 130 | AllowHttpOutbound | \* | \* | Internet | 80 | \* | Allow |

These rules enable user connectivity (inbound 443 from Internet), Azure management operations (GatewayManager, AzureCloud), and Bastion\-to\-VM communication (outbound 22 and 3389\). Omitting any of these required rules causes connection failures or deployment issues.

### Scale host unit capacity

For Standard and Premium SKUs, you configure the number of host units to handle expected concurrent session load. Each instance supports 20 concurrent RDP sessions or 40 concurrent SSH sessions, so a deployment with 4 instances accommodates up to 80 simultaneous RDP connections or 160 SSH connections.

To adjust host unit count, navigate to the Bastion resource, select **Configuration**, and modify the **Instance count** value. Azure deploys more host units or deallocates excess units based on your specification. This operation takes several minutes and doesn't interrupt active sessions.

Consider scaling proactively before expected usage increases rather than reactively when performance degrades. Scaling down reduces costs but should account for typical peak usage patterns rather than only current load.

### Verify the deployment

After deployment and configuration complete, verify that Bastion operates correctly before removing public IP addresses from target VMs. Check the Bastion resource **Overview** page to confirm the **Provisioning state** shows **Succeeded** and the **Status** shows **Running**.

Test connectivity by navigating to a target virtual machine, selecting **Connect**, and choosing **Bastion** from the connection options. Enter valid credentials for the VM and verify that a browser\-based RDP or SSH session opens successfully. If native client support is enabled, test the tunnel command to confirm the configuration works as expected.

Review the AzureBastionSubnet's NSG flow logs to confirm traffic flows match expected patterns—inbound 443 from user IP addresses, outbound 3389 or 22 to target VM IP addresses, and Azure service tag communication.

Contoso Manufacturing deployed Bastion with Standard SKU in the hub virtual network, configured four host units for capacity, and enabled native client support. Factory engineers tested connections to VMs in spoke VNets using both browser and native RDP client methods. After the admins confirm successful connectivity, the security team prepared to remove public IP addresses from factory VMs.

Now that you deployed and configured Azure Bastion, you're ready to connect to virtual machines using browser\-based and native client methods.

---

## Connect to VMs through Azure Bastion

Azure Bastion provides multiple connection methods that accommodate different user workflows and security requirements. Factory engineers at Contoso Manufacturing connect to operational VMs using browser\-based sessions for quick troubleshooting and native client tunnels for complex administrative tasks requiring full RDP client features.

### Connect using browser\-based sessions

Browser\-based connectivity works with all Bastion SKUs and provides the simplest connection experience. This method requires no client\-side software beyond a modern web browser and establishes RDP or SSH sessions directly through the Azure portal.

To initiate a browser\-based connection, navigate to the target virtual machine in the Azure portal and select **Connect** from the overview page. Choose **Bastion** from the available connection methods. The portal displays a connection form requesting credentials—enter the username and password (or SSH private key for Linux VMs) for the target system. Select **Connect** to launch the session.

The browser opens a new tab or window displaying the remote desktop or terminal session. All keyboard input, mouse actions, and display output flow through the HTTPS connection to the Bastion service, which forwards the session to the target VM. The target VM requires no public IP address and needs no open inbound ports for RDP or SSH in its network security group.

Browser\-based sessions support standard RDP features including clipboard operations, though some advanced features like drive redirection or printer mapping can have limitations. For Linux VMs, the SSH session provides a full terminal interface with command history, tab completion, and text\-based application support.

This connection method works seamlessly across operating systems and network environments because it runs entirely through HTTPS port 443\. Users behind restrictive corporate firewalls or using managed devices with limited software installation rights can connect without more configuration.

### Connect using native client tunneling

Native client support (Standard and Premium SKUs) enables connections using standard RDP and SSH client applications through an Azure CLI tunnel. This capability preserves existing workflows for engineers who rely on specific client configurations, custom RDP settings, or advanced features not available in the browser\-based client.

#### Configure the Azure CLI tunnel

Native client connectivity requires the Azure CLI with the bastion extension installed. Install the extension using:

```
az extension add --name bastion

```

To establish a tunnel for an RDP connection, use the `az network bastion tunnel` command with the target VM's resource ID and a local port number:

```
az network bastion tunnel --name bastion-hub-prod \
  --resource-group rg-network-prod \
  --target-resource-id /subscriptions/<subscription-id>/resourceGroups/<vm-rg>/providers/Microsoft.Compute/virtualMachines/<vm-name> \
  --resource-port 3389 \
  --port 50001

```

This command establishes a listening port on localhost:50001 that tunnels through the Bastion service to the target VM's RDP port. The command continues running in the terminal and maintains the tunnel as long as it executes. Keep this terminal window open while you use the RDP connection.

#### Connect RDP clients through the tunnel

With the tunnel established, launch your preferred RDP client and connect to `localhost:50001`. Microsoft Remote Desktop, Windows App, or the built\-in mstsc.exe client all work with the tunnel. The RDP client treats the localhost connection as a standard RDP session, enabling all client\-side features including:

* Display configuration (multi\-monitor support, custom resolutions)
* Clipboard synchronization (copy/paste between local and remote)
* Drive redirection (access local files from the remote session)
* Audio redirection (play remote system audio locally)
* Printer mapping (print from remote applications to local printers)

The connection flows from the RDP client to localhost, through the Azure CLI tunnel command, across the internet to the Bastion service over HTTPS 443, and finally to the target VM over the Azure backbone network. This path preserves the security benefits of Bastion while enabling full native client functionality.

#### Connect SSH clients through native tunneling

For SSH connections, Azure Bastion provides direct SSH support through the `az network bastion ssh` command:

```
az network bastion ssh --name bastion-hub-prod \
  --resource-group rg-network-prod \
  --target-resource-id /subscriptions/<subscription-id>/resourceGroups/<vm-rg>/providers/Microsoft.Compute/virtualMachines/<vm-name> \
  --auth-type password \
  --username azureuser

```

This command establishes an interactive SSH session directly through Bastion without requiring a separate tunnel setup. You also tunnel SSH connections similarly to RDP if you need to use specific SSH client features or configurations not supported by the direct method.

### Generate and use shareable links

Shareable links (Standard and Premium SKUs) provide time\-limited browser\-based access without requiring Azure portal authentication. This feature supports scenarios where contractors, vendors, or temporary staff need access without full Azure subscriptions or role\-based access control assignments.

To create a shareable link, navigate to the target VM in the Azure portal, select **Connect**, and choose **Bastion**. Toggle the **Shareable link** option and select **Create shareable link**. The portal generates a URL that provides direct browser\-based access to the VM through Bastion.

Configure the shareable link properties:

* **Expiration time**: Set how long the link remains valid (maximum 90 days)
* **Allowed credentials**: Optionally restrict which VM credentials can authenticate through the link
* **Description**: Add notes about the link's purpose for audit records

Share the generated URL with the intended recipient. When they open the URL, they see a connection form requesting VM credentials. After authentication, the browser establishes a Bastion session identical to the standard browser\-based connection experience.

Shareable links appear in the Bastion resource's **Shareable Links** page, where you can revoke individual links before their expiration time. Revoked links immediately stop working, terminating any active sessions using those links.

Contoso Manufacturing uses shareable links to provide vendor access during equipment maintenance windows. The security team creates 24\-hour links before scheduled maintenance and revokes them immediately after the vendor completes their work.

### Authenticate using Kerberos

Kerberos authentication is available with all Azure Bastion SKU tiers and enables domain\-joined virtual machines to authenticate users through Active Directory without transmitting passwords over the connection. This capability supports Windows domains using Active Directory Domain Services (AD DS) or Azure Active Directory Domain Services (Azure AD DS).

With Kerberos authentication enabled in the Bastion configuration, domain users connecting through the native client tunnel authenticate using their domain credentials. The authentication process uses Kerberos tickets instead of password validation, which provides enhanced security and supports single sign\-on workflows.

To enable Kerberos authentication, the target VMs must be domain\-joined, and the Bastion subnet must have network connectivity to domain controllers. Users initiate connections using the native client tunnel with their domain username in the format `domain\username`.

### Monitor and manage active sessions

Azure Bastion maintains visibility into all active connections through the **Sessions** page in the Azure portal. This view displays currently connected users, target VMs, connection duration, and session types (RDP or SSH).

Security teams use this monitoring capability to identify unusual access patterns, verify that expected users have appropriate access, and disconnect sessions when necessary. To terminate an active session, select the session from the list and choose **Disconnect**. The disconnection happens immediately and logs the administrative termination for audit purposes.

Session monitoring provides real\-time visibility without requiring access to individual VMs or reviewing distributed logs. All Bastion connectivity—regardless of whether users connect through the browser, native clients, or shareable links—appears in this centralized view.

### Remove public IP addresses from VMs

Once Bastion provides reliable connectivity, you can remove public IP addresses from target virtual machines to eliminate their exposure to internet\-based attacks. This change represents the primary security benefit of Azure Bastion—VMs become inaccessible from the internet while remaining fully manageable through Bastion.

Before removing public IPs, verify that all required access paths work through Bastion. Test browser\-based connections, native client tunnels, and any other workflows that users depend on for VM management. Confirm that monitoring tools, backup systems, and other automation that might depend on direct VM connectivity either work through private networks or have alternative access methods.

To remove a public IP, navigate to the VM in the Azure portal, select **Networking**, and disassociate the public IP address from the network interface. You can delete the now\-unused public IP resource or retain it for potential future use.

After removing public IPs, update network security group rules to remove inbound allow rules for ports 3389 and 22\. These ports no longer require internet accessibility because all RDP and SSH traffic flows through the Bastion service.

Contoso Manufacturing's security team followed a staged approach: they deployed Bastion, validated connectivity for two weeks while monitoring the Sessions view, confirmed all engineers successfully connected through Bastion, and then removed public IPs from factory VMs during a scheduled maintenance window. Post\-implementation monitoring showed zero inbound attempts on RDP and SSH ports, confirming the elimination of the attack surface.

Now that you understand how to connect to VMs through Azure Bastion using multiple methods, you're ready to validate your knowledge with a few scenario\-based questions.

---

## Knowledge check

You explored how Azure Bastion provides secure remote connectivity to virtual machines without exposing RDP and SSH ports to the internet. Test your understanding of SKU selection, deployment requirements, and connection methods with these scenario\-based questions.

### Check your knowledge

---

## Summary

Contoso Manufacturing eliminated public RDP and SSH exposure from factory virtual machines by implementing Azure Bastion as a centralized secure gateway. The deployment transformed the security posture from VMs with internet\-facing management ports to a zero\-public\-IP architecture where all remote access flows through a hardened platform service.

### What you accomplished

You planned an Azure Bastion deployment by selecting the appropriate SKU based on scale, feature, and cost requirements. The SKU comparison showed that Developer provides no\-cost individual access, Basic supports small teams with browser\-only connectivity, Standard adds native client support and scaling for enterprise deployments, and Premium includes session recording for compliance requirements.

You deployed and configured Azure Bastion by creating the required AzureBastionSubnet with a minimum /26 prefix, associating a Standard static public IP, and enabling advanced features. Native client support preserved existing RDP tooling workflows for operational engineers. Host unit scaling configured capacity for concurrent session requirements. Network security group rules permitted the specific traffic flows required for Bastion operations.

You connected to virtual machines through Azure Bastion using browser\-based sessions for quick access and native client tunneling for full RDP client features. The browser method works across all platforms without software installation. Native client tunneling through Azure CLI enables drive redirection, clipboard synchronization, and custom display configurations. Shareable links provided time\-limited access for contractors without Azure portal credentials.

### Key decisions for Azure Bastion

Azure Bastion eliminates the need for public IP addresses on virtual machines and removes the requirement for open RDP and SSH ports in network security groups. This architectural shift transforms the attack surface by removing direct internet exposure while preserving operational access through a managed platform service.

SKU selection balances capability requirements against cost:

* **Developer**: Individual use, no host unit charges, browser\-only
* **Basic**: Small teams, fixed two host units, browser\-only, no native client
* **Standard**: Enterprise scale, configurable host units, native client support, IP\-based connections
* **Premium**: Compliance environments add session recording and private\-only mode

The AzureBastionSubnet must be named exactly **AzureBastionSubnet** (case\-sensitive) and sized with a minimum /26 prefix. This dedicated subnet hosts the Bastion infrastructure and requires specific network security group rules for Azure management operations and user connectivity.

Native client tunneling preserves existing workflows for users who depend on RDP client features or specific SSH tools. The Azure CLI establishes a localhost tunnel, and users connect their standard clients to the local port. This approach delivers browser\-based security with native client functionality.

### Learn more

* [Azure Bastion overview](/en-us/azure/bastion/bastion-overview)
* [Azure Bastion configuration settings](/en-us/azure/bastion/configuration-settings)
* [Connect to VMs using native client](/en-us/azure/bastion/native-client)
* [Session recording](/en-us/azure/bastion/session-recording)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/plan-implement-azure-bastion/_

## Fuentes
- [Plan and implement Azure Bastion](https://learn.microsoft.com/en-us/training/modules/plan-implement-azure-bastion/?WT.mc_id=api_CatalogApi)
