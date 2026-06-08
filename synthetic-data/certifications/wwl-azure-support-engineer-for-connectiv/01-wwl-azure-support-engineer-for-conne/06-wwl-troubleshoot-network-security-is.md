# Troubleshoot network security issues with Microsoft Azure

> Curso: Azure Support Engineer for Connectivity Specialty (wwl-azure-support-engineer-for-connectivity-specia) · Seccion: Azure Support Engineer for Connectivity Specialty
> Duracion estimada: 59 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You work as an engineer who supports Azure infrastructure. Users within and outside your organization access various web services and applications hosted on your virtual network. They sometimes come across various network issues. Also, from a security point of view, you need to ensure the optimum health of your virtual network.

Within the Azure portal, resources such as Azure Firewall, Network Watcher, Azure Web Application Firewall, and Azure DDoS Protection, help you manage and monitor virtual network security.

In this module, you’ll learn how to troubleshoot network security, configuration, latency, bandwidth, and Azure Firewall issues.

### Learning objectives

After completing this module, you’ll be able to:

* Troubleshoot network security issues.
* Troubleshoot network security group (NSG).
* Troubleshoot Azure Firewall.
* Troubleshoot latency issues within a virtual network.

### Prerequisites

* Experience with the OSI model.
* Demonstrate an awareness of Azure Bastion.
* Experience with PowerShell and Azure CLI.
* Know how to get to Cloud Shell to run commands.
* Experience with Visual Studio Code.
* Demonstrate an understanding of JSON.

---

## Troubleshoot network security issues

### Determine why Web Application Firewall (WAF) is blocking wanted traffic

Occasionally, requests that should pass through your Web Application Firewall (WAF) are blocked.

To tune the strict Open Web Application Security Project (OWASP) regulations for the needs of an application or organization, WAF helps you to customize, or disable the rules, or create exclusions, that may be causing issues or false positives. This is done on a per\-site and per\-URI basis. That is, changes to the policies will only affect specific sites/URIs and wouldn't concern other sites that might not have the same issues.

The following articles will help you understand how the WAF functions and how its rule and logs work:

* [WAF overview](/en-us/azure/web-application-firewall/ag/ag-overview)
* [WAF configuration](/en-us/azure/web-application-firewall/ag/application-gateway-waf-configuration)
* [WAF monitoring](/en-us/azure/application-gateway/application-gateway-diagnostics)

### Understanding WAF logs

WAF logs work as a statement of all evaluated requests that are matched or blocked. If you notice a false positive, when the WAF blocks a request that it shouldn't, you can do the following steps:

1. Find the specific request.
2. Examine the logs to find the specific URI, timestamp, or transaction ID of the request.
3. Fix the false positives.

### Viewing WAF logs

To view WAF logs, complete the following steps:

1. In the Azure portal, select **All resources**, and select the **Application Gateway WAF policy**.
2. Select **Activity log**.
3. Select individual operations for more information.
4. You can download the Activity log by selecting **Download as CSV**.
5. To stream the Activity log events to another service, select **Export Activity Logs**.

In Export Activity Logs:

1. Select **Add diagnostic setting**.
2. Type a **Diagnostic setting name**.
3. Select the relevant log categories to stream in **Categories**. For example, select **Security**, **Policy**, and **Alert**.
4. Select the streaming destination in **Destination details**. For example, select **Send to Log Analytics workspace**.
5. Enter additional destination details. For example, the relevant **Subscription** and **Log Analytics workspace**.
6. Select **Save**.

### Anomaly Scoring mode

Anomaly Scoring mode is used by OWASP to decide whether to block traffic. In Anomaly Scoring mode, traffic that matches any rule isn't instantly blocked when the firewall is in Prevention mode. Rules have a certain criterion: Critical, Error, Warning, or Notice. Each of these has a numeric value associated with it, called Anomaly Score. The numeric value indicates the severity of a request.

For more information, see [Anomaly Scoring mode](/en-us/azure/web-application-firewall/ag/ag-overview).

### Fixing false positives

To fix false positives and avoid the issues of blocked traffic, you can use an exclusion list. Using an exclusion list is only applicable to a specific part of a request, or a rule set that is being disabled. You can decide to exclude either body, headers, or cookies for a certain condition instead of excluding the whole request. In a global setting environment, the specific exclusion applies to all traffic passing through your WAF.

Refer to [WAF configuration](/en-us/azure/web-application-firewall/ag/application-gateway-waf-configuration) for more information about exclusion lists.

#### To configure exclusion lists using the Azure portal

1. Go to the WAF portal.
2. Select **Manage exclusions** under **Managed rules**.

An example exclusion list:

* **Disable the rule**: Disabling a rule allows you to treat a certain condition as a non\-threat that would otherwise be flagged as malicious and be blocked. In a global setting environment, disabling a rule for the entire WAF is a risk and can weaken your security.

#### To disable rule groups or specific rules

1. Browse to the application gateway, and then select **Web application firewall**.
2. Select your **WAF Policy**.
3. Select **Managed Rules**.
4. Search for the rules or rule groups that you want to disable.
5. Select the check boxes for the rules that you want to disable.
6. Select the action at the top of the page (**Enable**/**Disable**) for the selected rules.
7. Select **Save**.

A third\-party tool called Fiddler can provide additional information. Fiddler will help you to:

* **Find request attribute names**: Review individual requests and determine what specific fields of a webpage are called. It also helps to exclude certain fields from inspection using exclusion lists.
* **Find request header names**: View request and response headers inside the developer tools of Chrome, or see the headers for the GET request.
* **Find request cookie names**: View cookies by selecting the Cookies tab in Fiddler.

### Restrict global parameters to eliminate false positives

* **Disable request body inspection**: Certain bodies that are not a threat to your application can be prevented from being evaluated by your WAF by setting **Inspect request body** to off. This way, only the request body is not inspected. The headers and cookies will still be inspected, unless they're on the exclusion list.
* **File size limits**: The possibility of an attack to web servers and applications can be reduced by limiting the file size for your WAF. Permitting large files increases the risk of your back end being exhausted. To prevent attacks, it is advisable to limit the file size to a typical case for your application.

Note

Firewall Metrics (WAF\_v1 only)
For v1 Web Application Firewalls, the following metrics are now available in the portal:

* **Web Application Firewall Blocked Request Count** \- the number of requests that were blocked.
* **Web Application Firewall Blocked Rule Count** \- all rules that were matched and the request was blocked.
* **Web Application Firewall Total Rule Distribution** \- all rules that were matched during evaluation

To enable metrics, select the **Metrics** tab in the portal, and select one of the three metrics.

### Determine which version of TLS a customer is running

If the client is using a version of Transport Layer Security (TLS) that is lower than the minimum required version, all calls to Azure Storage will fail. Therefore, from the security point of view, an Azure Storage account might require that clients use a minimum version of TLS to send requests. For example, a request sent by a client who is using TLS 1\.1 will fail, if a storage account requires TLS 1\.2\.

The article [Configure minimum required version of Transport Layer Security (TLS) for a storage account](/en-us/azure/storage/common/transport-layer-security-configure-minimum-version?tabs=portal) explains how to configure the minimum TLS version for an Azure Storage account that might affect client applications.

### Configure the client TLS version

For the client, sending a request with a particular version of TLS is only possible if the operating system and the .NET Framework used by the client supports that version.

To enable TLS 1\.2 in a PowerShell client:

```
## Set the TLS version used by the PowerShell client to TLS 1.2.

[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;

## Create a new container.

$storageAccount = Get-AzStorageAccount -ResourceGroupName $rgName -Name $accountName

$ctx = $storageAccount.Context

New-AzStorageContainer -Name "sample-container" -Context $ctx

```

To enable TLS 1\.2 in a .NET client using version 12 of the Azure Storage client library:

```
public static async Task ConfigureTls12()

{

    // Enable TLS 1.2 before connecting to Azure Storage

    System.Net.ServicePointManager.SecurityProtocol = System.Net.SecurityProtocolType.Tls12;

    // Add your connection string here.

    string connectionString = "";

    // Create a new container with Shared Key authorization.

    BlobContainerClient containerClient = new BlobContainerClient(connectionString, "sample-container");

    await containerClient.CreateIfNotExistsAsync();

}

```

To enable TLS 1\.2 in a .NET client using version 11 of the Azure Storage client library:

```
static void EnableTls12()

{

    // Enable TLS 1.2 before connecting to Azure Storage

    System.Net.ServicePointManager.SecurityProtocol = System.Net.SecurityProtocolType.Tls12;

    // Add your connection string here.

    string connectionString = "";

    // Connect to Azure Storage and create a new container.

    CloudStorageAccount storageAccount = CloudStorageAccount.Parse(connectionString);

    CloudBlobClient blobClient = storageAccount.CreateCloudBlobClient();

    CloudBlobContainer container = blobClient.GetContainerReference("sample-container");

    container.CreateIfNotExists();

}

```

For more information, refer to [Support for TLS 1\.2](/en-us/dotnet/framework/network-programming/tls).

Note

Fiddler or a similar tool can help you verify that the specified version of TLS was used by the client to send a request.

### Troubleshoot encryption/certificate\-related issues for point\-to\-site scenarios

A point\-to\-site (P2S) VPN connection is initiated by a single endpoint and is useful when you want to connect to your VNet from a remote location. Point\-to\-site is a better option when you have only a few clients that need to connect to a VNet. P2S connections do not require a VPN device, or a public network or IP address.

P2S VPN supports Secure Socket Tunneling Protocol (SSTP), and IKEv2\. You can securely connect different clients running Windows, Linux, or macOS to an Azure VNet through point\-to\-site connection.

### Generate certificates

* Generate a root certificate

First, obtain the public key (.cer file) for a root certificate. After creating the root certificate, export the public certificate (not the private key). Then this file is uploaded to Azure. The root certificate acts as a trusted source by Azure for connection over P2S to the virtual network. There are two ways to generate a root certificate, enterprise certificate, or self\-signed certificate. To create a self\-signed root certificate, consider the following steps:

1. Open a Windows PowerShell console.
2. The following example creates a self\-signed root certificate named "P2SRootCert" that is automatically installed in "Certificates\-Current User\\Personal\\Certificates". You can view the certificate by opening **certmgr.msc**, or **Manage User Certificates**.

You can modify and run the following command:

```
$cert = New-SelfSignedCertificate -Type Custom -KeySpec Signature `

-Subject "CN=P2SRootCert" -KeyExportPolicy Exportable `

-HashAlgorithm sha256 -KeyLength 2048 `

-CertStoreLocation "Cert:\CurrentUser\My" -KeyUsageProperty Sign -KeyUsage CertSign

```
3. Leave the PowerShell console open and proceed with the next steps to generate a client certificate.

	* Generate client certificates
	
	
	A client certificate is automatically installed on the computer where it is generated from a self\-signed root certificate. For installing a client certificate on another client computer, you need to export it as a .pfx file, along with the entire certificate chain. The .pfx file will contain the root certificate information required for client authentication. There are two methods to create client certificates, enterprise certificate, or self\-signed root certificate.
	
	
	It is recommended to generate a unique certificate for each client instead of using the same certificate. This is because, if you want to revoke a particular client certificate, you don't need to generate and install a new one for every client that uses the same certificate. To generate client certificate, consider the following steps:
4. Use the following example if the PowerShell console session is still open:

```
New-SelfSignedCertificate -Type Custom -DnsName P2SChildCert -KeySpec Signature `

-Subject "CN=P2SChildCert" -KeyExportPolicy Exportable `

-HashAlgorithm sha256 -KeyLength 2048 `

-CertStoreLocation "Cert:\CurrentUser\My" `

-Signer $cert -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.2")

```
5. If it's a new PowerShell console session, consider the following steps:

	* Identify the self\-signed root certificate that is installed on the computer. This cmdlet returns a list of certificates that are installed on your computer.
```
Get-ChildItem -Path "Cert:\CurrentUser\My"

```

	1. Locate the subject name from the returned list, then copy the thumbprint that is located next to it to a text file. In this case "P2SRootCert".
	
	
	
	```
	Thumbprint                                Subject
	
	----------                                -------
	
	7181AA8C1B4D34EEDB2F3D3BEC5839F3FE52D655  CN=P2SRootCert
	
	
	```
	2. Declare a variable for the root certificate using the thumbprint from the previous step.
	
	
	
	```
	$cert = Get-ChildItem -Path "Cert:\CurrentUser\My\<THUMBPRINT>"
	
	
	```
	3. Replace THUMBPRINT with the thumbprint of the root certificate from which you want to generate a child certificate.
	
	
	
	```
	$cert = Get-ChildItem -Path "Cert:\CurrentUser\My\7181AA8C1B4D34EEDB2F3D3BEC5839F3FE52D655"
	
	
	```
	4. In this example, a client certificate named "P2SChildCert" is generated. The client certificate that you generate is automatically installed in "Certificates \- Current User\\Personal\\Certificates" on your computer.

You can modify and run the following command to generate a client certificate:

```
New-SelfSignedCertificate -Type Custom -DnsName P2SChildCert -KeySpec Signature `

-Subject "CN=P2SChildCert" -KeyExportPolicy Exportable `

-HashAlgorithm sha256 -KeyLength 2048 `

-CertStoreLocation "Cert:\CurrentUser\My" `

-Signer $cert -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.2")

```

To learn about exporting the root certificate and the client certificate, see [Generate and export certificates for User VPN connections](/en-us/azure/virtual-wan/certificates-point-to-site).

To configure a point\-to\-site connection using Azure certificate, you need to:

1. Add the VPN client address pool.
2. Specify tunnel type and authentication type.
3. Upload root certificate public key information.
4. Install exported client certificate.
5. Configure settings for VPN clients.
6. Connect to Azure.

For detailed steps to configure a point\-to\-site connection using Azure certificate, refer to [Connect to a VNet using P2S VPN \& certificate authentication: portal \- Azure VPN Gateway](/en-us/azure/vpn-gateway/vpn-gateway-howto-point-to-site-resource-manager-portal).

To verify your VPN connection is active (Windows clients), open an elevated command prompt, and run **ipconfig/all**.

To connect to a virtual machine (Windows clients):

1. Locate the private IP address.
2. Verify that you're connected to your VNet.
3. Open Remote Desktop Connection by typing "RDP" or "Remote Desktop Connection" in the search box on the taskbar, then select **Remote Desktop Connection**. You can also open Remote Desktop Connection using the "mstsc" command in PowerShell.
4. In Remote Desktop Connection, enter the private IP address of the VM. Select **Show Options** to adjust additional settings, then connect.

### Troubleshoot a connection

If you're having trouble connecting to a virtual machine over your VPN connection, read the following:

* Check that your VPN connection is successful.
* Ensure that you're connecting to the private IP address for the VM.
* If you can connect to the VM using the private IP address, but not the computer name, check DNS configuration.
* For more information about RDP connections, see [Troubleshoot Remote Desktop connections to a VM](/en-us/troubleshoot/azure/virtual-machines/troubleshoot-rdp-connection).
* Verify that the VPN client configuration package was generated after the DNS server IP addresses were specified for the VNet. If you updated the DNS server IP addresses, generate and install a new VPN client configuration package.
* Ensure that there is no overlapping address space. For example, if the IP address is within the address range of the VNet that you are connecting to, or within the address range of your VPNClientAddressPool. Use "ipconfig" to check the IPv4 address assigned to the Ethernet adapter on the computer from which you are connecting.

To add a trusted root certificate, refer to [Upload a trusted root certificate](/en-us/azure/vpn-gateway/vpn-gateway-howto-point-to-site-resource-manager-portal).

To remove a trusted root certificate:

1. Go to the point\-to\-site configuration page for your virtual network gateway.
2. In the root certificate section of the page, locate the certificate that you want to remove.
3. Select the ellipsis next to the certificate, and then select **Remove**.

### Revoke a client certificate

Revoking a client certificate is different from removing a trusted root certificate. Removing a trusted root certificate .cer file from Azure revokes all the client certificates generated/authenticated by the root certificate. Revoking a client certificate allows other certificates associated with the same root certificate to continue working.

To revoke a client certificate, add the thumbprint to the revocation list.

* Retrieve the client certificate thumbprint. See [How to retrieve the Thumbprint of a Certificate](/en-us/dotnet/framework/wcf/feature-details/how-to-retrieve-the-thumbprint-of-a-certificate).
* Copy the information to a text editor and remove all spaces so that it is a continuous string.
* Go to the virtual network gateway point\-to\-site\-configuration page. This is the same page that you used to upload a trusted root certificate.
* In the **Revoked certificates** section, input a friendly name for the certificate.
* Copy and paste the thumbprint string to the **Thumbprint** field.
* The thumbprint validates and is automatically added to the revocation list. A message appears on the screen that the list is updating.
* After updating has completed, the certificate can no longer be used to connect. Clients that try to connect using this certificate receive a message saying that the certificate is no longer valid.

### Troubleshoot connectivity to secure endpoints

Azure Private Endpoint is a network interface that uses a private IP address from a virtual network and connects you privately and securely to a private link service.

The following are the connectivity scenarios available with Private Endpoint:

* Virtual network from the same region.
* Regionally peered virtual networks.
* Globally peered virtual networks.
* Customer on\-premises over VPN or Azure ExpressRoute circuits.

### Diagnose connectivity problems

The following steps will guide you to ensure that all the required configurations are in place, to resolve connectivity problems with your private endpoint setup. For detailed steps, see [Diagnose connectivity problems](/en-us/azure/private-link/troubleshoot-private-endpoint-connectivity).

1. Review Private Endpoint configuration by browsing the resource.
2. Use Azure Monitor to see if data is flowing.
3. Use VM Connection troubleshoot from Azure Network Watcher.
4. DNS resolution from the test results must have the same private IP address assigned to the private endpoint.
5. Source virtual machine should have the route to Private Endpoint IP next hop as InterfaceEndpoints in the NIC Effective Routes.
6. If the connection has validated results, the connectivity problem might be related to other aspects like secrets, tokens, and passwords at the application layer.
7. Narrow down before raising the support ticket.
8. If the Private Endpoint is linked to a Private Link Service which is linked to a load balancer, check if the backend pool is reporting healthy. Fixing the load balancer health will resolve the issue with connecting to the Private Endpoint.
9. Contact the Azure Support team if your problem is unresolved and a connectivity problem still exists.

### Troubleshoot encryption/certificate\-related issues for site\-to\-site scenarios

#### IPsec and IKE policy parameters for VPN gateways

The IPsec and IKE protocol standard supports a wide range of cryptographic algorithms in various combinations. The article [IPsec/IKE parameters](/en-us/azure-stack/user/azure-stack-vpn-gateway-settings) explains which parameters are supported in Azure Stack Hub to meet your compliance or security requirements.

Note the following important considerations when using these policies:

* The IPsec/IKE policy only works on the Standard and HighPerformance (route\-based) gateway SKUs.
* You can only specify one policy combination for a given connection.
* You must specify all algorithms and parameters for both IKE (Main Mode) and IPsec (Quick Mode). Partial policy specification is not allowed.
* Check with your VPN device vendor specifications if the policy is supported on your on\-premises VPN devices.

The following steps show how to create and configure an IPsec/IKE policy, and apply it to a new or existing connection. For detailed step\-by\-step instructions, follow [Steps to configure an IPsec/IKE policy for site\-to\-site (S2S) VPN connections in Azure Stack Hub](/en-us/azure-stack/user/azure-stack-vpn-s2s).

1. Create and set IPsec/IKE policy.
2. Create a new site\-to\-site VPN connection with IPsec/IKE policy:

	1. Step 1 \- Create the virtual network, VPN gateway, and local network gateway.
	2. Step 2 \- Create a site\-to\-site VPN connection with an IPsec/IKE policy.
3. Update IPsec/IKE policy for a connection.

---

## Troubleshoot Azure Firewall

### Troubleshoot Azure Firewall application rules

Azure Firewall helps you to control outbound network access from an Azure subnet. With Azure Firewall, you can configure:

* Application rules that define fully qualified domain names (FQDNs) that can be accessed from a subnet.
* Network rules that define source address, protocol, destination port, and destination address.

A [hub\-and\-spoke model](/en-us/azure/architecture/reference-architectures/hybrid-networking/hub-spoke?tabs=cli) is recommended for production deployments, where the firewall is in its own VNet. The workload servers are in peered VNets in the same region, with one or more subnets.

* **AzureFirewallSubnet** ‒ the firewall is in this subnet.
* **Workload\-SN** ‒ the workload server is in this subnet. This subnet's network traffic goes through the firewall.

The following [Deploy and configure Azure Firewall using the Azure portal](/en-us/azure/firewall/tutorial-firewall-deploy-portal) can help you learn how to:

* Set up a test network environment.
* Deploy a firewall.
* Create a default route.
* Configure an application rule to allow access to [www.google.com](https://www.google.com).
* Configure a network rule to allow access to external DNS servers.
* Configure a NAT rule to allow a remote desktop to the test server.
* Test the firewall.

#### Monitor Azure Firewall logs and metrics

Firewall logs allow you to monitor Azure Firewall. You can also consider using activity logs to audit Azure Firewall resources. To view performance counters in the portal, use metrics.

Logs can be sent to Azure Monitor logs, Storage, and Event Hubs. They can be analyzed in Azure Monitor logs or by using Excel and Power BI.

#### View and analyze the activity log

You can view and analyze activity log data by using any of the following methods:

* **Azure tools**: Through Azure PowerShell, the Azure CLI, the Azure REST API, or the Azure portal, you can retrieve information from the activity log.
* **Power BI**: By using the [Azure Activity Logs content pack for Power BI](/en-us/power-bi/connect-data/service-connect-to-services), you can analyze your data with preconfigured dashboards that you can use as is, or customize.
* **Microsoft Sentinel**: By connecting Azure Firewall logs to Microsoft Sentinel, you can view log data in workbooks, use it to create custom alerts, and incorporate it to improve your investigation.

Watch this video to learn more about the monitoring abilities of Azure Firewall:

#### View and analyze the network and application rule logs

Azure Firewall Workbook within the Azure portal is a platform where you can use Azure Firewall data analysis in an interactive way. For example, to create visual reports, combine multiple firewalls deployed across Azure, and so on.

For access and performance logs, you can connect to your storage account and retrieve the JSON log entries. After you download the JSON files, you can convert them to CSV and view them in Excel, Power BI, or any other data visualization tool.

To learn more, see [Monitor logs using Azure Firewall Workbook](/en-us/azure/firewall/firewall-workbook).

### Troubleshoot Azure Firewall network rules

Azure Firewall denies all traffic by default. You need to manually configure the rules to allow traffic. You can configure NAT rules, network rules, and applications rules on Azure Firewall using either classic rules or Firewall Policy.

#### Rule processing using classic rules

Rule collections are processed according to the priority order of a rule type, lower numbers to higher numbers, from 100 to 65,000\. A rule collection name can have only letters, numbers, underscores, periods, or hyphens. It must begin with a letter or number, and end with a letter, number, or underscore. The maximum name length is 80 characters.

To have room to add more rule collections if required, it's recommended to initially space your rule collection priority numbers in increments of 100 (100, 200, 300, and so on).

#### Rule processing using Firewall Policy

Rules are organized inside Rule Collections and Rule Collection Groups when using Firewall Policy. Rule Collection Groups contain zero or more Rule Collections. Rule Collections are of NAT, Network, or Applications types. You can define multiple Rule Collection types within a single Rule Group. You can specify zero or more Rules in a Rule Collection. Rules in a Rule Collection must be of the same type (NAT, Network, or Application).

Rules are processed based on Rule Collection Group and Rule Collection priority. They can be any number between 100 (highest priority) to 65,000 (lowest priority).

If a Firewall Policy is inherited from a parent policy, Rule Collection Groups in the parent policy always take precedence regardless of the priority of a child policy.

Here is an example of a Firewall Policy:

| Name | Type | Priority | Rules | Inherited from |
| --- | --- | --- | --- | --- |
| BaseRCG1 | Rule Collection Group | 200 | 8 | Parent policy |
| DNATRC1 | DNAT Rule Collection | 600 | 7 | Parent policy |
| DNATRC3 | DNAT Rule Collection | 600 | 7 | Parent policy |
| NetworkRc1 | Network Rule Collection | 800 | 1 | Parent policy |
| BaseRCG2 | Rule Collection Group | 300 | 3 | Parent policy |
| AppRCG2 | Application Rule Collection | 1200 | 2 | Parent policy |
| NetworkRC2 | Network Rule Collection | 1300 | 1 | Parent policy |
| ChildRCG1 | Rule Collection Group | 300 | 5 | \- |
| ChAppRC1 | Application Rule Collection | 700 | 3 | \- |
| ChNetRC1 | Network Rule Collection | 900 | 2 | \- |
| ChildRCG2 | Rule Collection Group | 650 | 9 | \- |
| ChNetRC2 | Network Rule Collection | 1100 | 2 | \- |
| ChAppRC2 | Application Rule Collection | 2000 | 7 | \- |
| ChDNATRC3 | DNAT Rule Collection | 3000 | 2 | \- |

The rule processing will be in the following order: DNATRC1, DNATRC3, ChDNATRC3, NetworkRC1, NetworkRC2, ChNetRC1, ChNetRC2, AppRC2, ChAppRC1, ChAppRC2\.

For more information about Firewall Policy rule sets, refer to [Azure Firewall Policy rule sets](/en-us/azure/firewall/policy-rule-sets).

Note

Application rules are always processed after Network rules, which are processed after DNAT rules, regardless of Rule Collection Group or Rule Collection priority and policy inheritance.

If you enable threat intelligence\-based filtering, those rules are highest priority and are always processed first. For more information, see [Azure Firewall threat intelligence\-based filtering](/en-us/azure/firewall/threat-intel).

#### IDPS

When IDPS is configured in Alert mode, it generates alerts on matching signatures for inbound and outbound flows. For an IDPS signature match, an alert is logged in firewall logs. However, there might still be another log entry generated for traffic that is denied/allowed by application/network rules. This is because the IDPS engine works in parallel to the rule processing engine.

### Troubleshoot Azure Firewall infrastructure rules

There is a built\-in rule collection for infrastructure Fully Qualified Domain Names (FQDNs) by default in Azure Firewall. Specific FQDNs used for the platform can't be used for other purposes.

The built\-in rule collection comprises of the following services:

* Compute access to storage Platform Image Repository (PIR).
* Managed disks status storage access.
* Azure Diagnostics and Logging (MDS).

#### Overriding

With the override feature, you can create a deny all application rule collection that is processed last. This will override the built\-in infrastructure rule collection and will always be processed before it. Anything not in the infrastructure rule collection is denied by default.

### Troubleshoot Azure Firewall network address translation (NAT) rules

Network rules allow or deny inbound, outbound, and east\-west traffic based on the network layer (L3\) and transport layer (L4\). A network rule facilitates traffic filtering based on IP addresses, any ports, and any protocols.

When you configure DNAT, the NAT rule collection action is set to Dnat. Each rule in the NAT rule collection can then be used to translate your firewall public IP address and port to a private IP address and port.

The following [Tutorial: Filter inbound Internet traffic with Azure Firewall DNAT policy using the portal](/en-us/azure/firewall/tutorial-firewall-dnat-policy) can help you learn how to:

* Set up a test network environment.
* Deploy a firewall.
* Create a default route.
* Configure a DNAT rule.
* Test the firewall.

### Troubleshoot Azure Firewall distributed network address translation (DNAT) rules

Azure Firewall Destination Network Address Translation (DNAT) translates and filters inbound internet traffic to your subnets. It allows or denies inbound traffic through the firewall public IP address(es). A DNAT rule translates a public IP address into a private IP address.

It's recommended to add a specific internet source to allow DNAT access to the network and avoid using wildcards for security reasons.

### Troubleshoot network\-level protection issues including firewalls

Adding security layers to the virtual machine (VM) networks protects inbound and outbound flows, to and from the users. You can use Firewall Policy to manage rule sets that the Azure Firewall uses to filter traffic.

#### Outbound connectivity

#### Network rules and applications rules

Network rules are applied in priority order before application rules. This means if a match is found in a network rule, no other rules are processed. IDPS may alert and/or block suspicious traffic.

In case there's no network rule match, and if the protocol is HTTP, HTTPS, or MSSQL, the packet is then evaluated by the application rules in priority order.

For HTTP, Azure Firewall looks for an application rule match according to the host header. For HTTPS, Azure Firewall looks for an application rule match according to SNI only.

In both HTTP and TLS\-inspected HTTPS cases, the firewall uses the DNS resolved IP address from the Host header instead of the packet's destination IP address. If the firewall does not get the port number in the host header, it assumes it to be the standard port 80\. In case of a port mismatch between the actual TCP port and the port in the host header, the traffic is dropped. DNS resolution is done by Azure DNS or by a custom DNS if configured on the firewall. 

#### Inbound connectivity

#### DNAT rules and network rules

Inbound internet connectivity is enabled by configuring Destination Network Address Translation (DNAT). NAT rules are applied in priority before network rules.

If a match is found, a corresponding network rule to allow the translated traffic is added.

To filter inbound HTTP/S traffic, you should use Web Application Firewall (WAF) as Application rules aren't applied for inbound connections.

To view the results of some of the rule combinations, refer to [Azure Firewall rule processing logic](/en-us/azure/firewall/rule-processing).

### Troubleshoot Azure Firewall Manager misconfiguration issues

Azure Firewall Manager is a security management service. You can use it to create secured virtual hubs to secure cloud network traffic destined for private IP addresses, Azure PaaS, and the internet.

| Secured virtual hub |
| --- |
|  |

The following [Tutorial: Secure your virtual hub using Azure Firewall Manager](/en-us/azure/firewall-manager/secure-cloud-network) can help you learn how to:

* Create the spoke virtual network.
* Create a secured virtual hub.
* Connect the hub\-and\-spoke virtual networks.
* Route traffic to your hub.
* Deploy the servers.
* Create a firewall policy and secure your hub.
* Test the firewall.

---

## Troubleshoot latency issues within a virtual network

You work as a support engineer supporting Azure infrastructure. You've been contacted by your web team about an issue with the website not responding. The web team have a pool of webservers behind a load balancer and public IP address.

In this exercise, you'll use what you've learned to go through steps to troubleshoot the connection issues to the virtual machines.

### Verify that the website can't be reached

Use the Cloud Shell on the right.

1. Use this Azure CLI command to get the public IP address of the scale set.

```
az network public-ip show \
--resource-group cloud-shell-storage-westeurope \
--name myScaleSetLBPublicIP \
--query '[ipAddress]' \
--output tsv

```
2. Copy the IP address, in a new tab in your browser, try to navigate to it.

### Check that Network Security Groups are configured correctly

1. In another browser tab, navigate to the Azure portal.
2. Search for **Network security groups**.
3. Under **Services**, select **Network Security Groups**.

### Check the port rules for the scale set

1. In the Azure portal, search for **scale set**, and then under **Services**, select **Virtual machine scale sets**.
2. In the list, select **myScaleSet** to view the details.
3. On the left, under **Settings**, select **Networking**.
4. Select the **Inbound port rules** tab, and then select the **Outbound port rules** tab.

Note

There are no network security groups (NSG) on this network interface.

### Check the network settings for the pool instances

1. On the left, under **Settings**, select **Instances**.
2. Select the first instance listed, in the above example this is **myScaleSet\_2**. In your environment this could be different.
3. On the left, under **Settings**, select **Networking**.
4. There isn't an NSG being used by this instance.
5. In the breadcrumb trail, select **myScaleSet**, and then repeat steps 2 to 4 to see that there isn't an NSG on the other instance.

### Check the load balancer for a scale set

1. Select the **Load balancing** tab, and then select the **myScaleSetLB** load balancer.
2. On the left, under **Settings**, select **Frontend IP configuration**.
3. Check that there is a frontend IP address, and that this is the IP you tested at the beginning of this exercise.
4. On the left, under **Settings**, select **Load balancing rules**.

Note

There is a rule for port **80** and port **443**.
5. On the left, select **Diagnose and solve problems**.

### Use the Diagnose and solve problems troubleshooter

1. Select the **No connectivity to the backend pool** troubleshooter.
2. In the **Tell us more about the problem you are experiencing** drop\-down box, select **Intermittent connectivity**.
3. Scroll down and read the insight found.

The insight points to the fact that the backend instances in the pool aren't listening for port **443**. The website instances should be listening to port **80**. This insight points to a problem in the load balancer rule.

---

## Exercise: Troubleshoot issue connecting virtual machine scale set

You work as a support engineer supporting Azure infrastructure. You've been contacted by your web team about an issue with the website not responding. The web team have a pool of webservers behind a load balancer and public IP address.

In this exercise, you'll use what you've learned to go through steps to troubleshoot the connection issues to the virtual machines.

### Verify that the website can't be reached

Use the Cloud Shell on the right.

1. Use this Azure CLI command to get the public IP address of the scale set.

```
az network public-ip show \
--resource-group <rgn>[sandbox resource group name]</rgn> \
--name webPublicIP \
--query '[ipAddress]' \
--output tsv

```
2. Copy the IP address, in a new tab in your browser, try to navigate to it.

### Check that Network Security Groups are configured correctly

1. In another browser tab, navigate to the [Azure portal](https://portal.azure.com/learn.docs.microsoft.com?azure-portal=true).
2. Search for **Network security groups**.
3. Under **Services**, select **Network Security Groups**.
4. Select **webNetworkSecurityGroup**.
5. Check that internet traffic over port **80** is allowed by the Network Security Group.

### Check the network settings for the virtual machines

1. On the left, select **Virtual Machines**.
2. Select the first virtual machine listed, in the above example this is **webVirtualMachine1**. In your environment this could be different.
3. On the left, under **Settings**, select **Networking**.
4. Note that port 80 is allowed.
5. Repeat these steps for **webVirtualMachine2**.

### Check the load balancer

1. In the Azure portal, search for **Load balancers**, then under **Services**, select **Load balancers**.
2. Select the **webLoadBalancer**.
3. On the left, under **Settings**, select **Frontend IP configuration**.
4. Check that there is a frontend IP address, and that this is the IP you tested at the beginning of this exercise.
5. On the left, under **Settings**, select **Load balancing rules**.

Note

There is a rule for port **80** and port **443**.
6. On the left, select **Diagnose and solve problems**.

### Use the Diagnose and solve problems troubleshooter

1. Select the **No connectivity to the backend pool** troubleshooter.
2. In the **Tell us more about the problem you are experiencing** drop\-down box, select **Intermittent connectivity**.
3. Scroll down and read the insight found.

The insight points to the fact that the backend instances in the pool aren't listening for port **443**. The website instances should be listening to port **80**. This insight points to a problem in the load balancer rule.

---

## Exercise: Resolve issue connecting virtual machine scale set

After investigating the connection issues to your website, you've found an issue with the load balancer rule user by the virtual machine scale set.

In this exercise, you'll resolve the issue and check that the website can now be accessed.

### Validate load balancer rules

1. In the Azure portal, search for **load balancers**, and then under **Services**, select **Load balancers**.
2. Select the **webLoadBalancer** load balancer.
3. Under **Settings**, select **Load balancing rules**.
4. From the list of rules, select **webLoadBalancerRule**.
5. To resolve the backend issue, change the **Backend port** from **443** to **80**, and then select **Save**.

Note

The front and backend in this environment need to be the same to get a response from the webserver to http requests.
6. Wait until the rule has been deployed successfully.

### Verify that the website can now be reached

1. Refresh the tab you opened to test the public IP address.

Note

If you have closed the previous browser tab, run this command to get the public IP address:

```
az network public-ip show \
--resource-group <rgn>[sandbox resource group name]</rgn> \
--name webPublicIP \
--query '[ipAddress]' \
--output tsv

```

If the website is online, you'll see a page with a **Hello World** message from the backend instance.

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary and resources

As a support engineer, you have investigated various network security issues. Having completed this module, you can troubleshoot issues arising in the security infrastructure using the Azure portal and other tools.

You now understand how to protect your Azure Virtual Network through network security policies and resources.

Now that you've completed this module, you should be able to:

* Troubleshoot network security issues.
* Troubleshoot Network Security Group (NSG).
* Troubleshoot Azure Firewall.
* Troubleshoot latency issues within a virtual network.

### Learn more

Use these resources to discover more:

[WAF overview](/en-us/azure/web-application-firewall/ag/ag-overview)

[WAF configuration](/en-us/azure/web-application-firewall/ag/application-gateway-waf-configuration)

[WAF monitoring](/en-us/azure/application-gateway/application-gateway-diagnostics)

[Anomaly scoring mode](/en-us/azure/web-application-firewall/ag/ag-overview)

[Configure minimum required version of Transport Layer Security (TLS) for a storage account](/en-us/azure/storage/common/transport-layer-security-configure-minimum-version?tabs=portal)

[Support for TLS 1\.2](/en-us/dotnet/framework/network-programming/tls)

[Generate and export certificates for User VPN connections](/en-us/azure/virtual-wan/certificates-point-to-site)

[Connect to a VNet using P2S VPN \& certificate authentication: portal \- Azure VPN Gateway](/en-us/azure/vpn-gateway/vpn-gateway-howto-point-to-site-resource-manager-portal)

[Troubleshoot Remote Desktop connections to a VM](/en-us/troubleshoot/azure/virtual-machines/troubleshoot-rdp-connection)

[How to retrieve the Thumbprint of a Certificate](/en-us/dotnet/framework/wcf/feature-details/how-to-retrieve-the-thumbprint-of-a-certificate)

[Diagnose connectivity problems](/en-us/azure/private-link/troubleshoot-private-endpoint-connectivity)

[IPsec/IKE parameters](/en-us/azure-stack/user/azure-stack-vpn-gateway-settings)

[Steps to configure an IPsec/IKE policy for site\-to\-site (S2S) VPN connections in Azure Stack Hub](/en-us/azure-stack/user/azure-stack-vpn-s2s)

[Azure limits](/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits?toc=/azure/virtual-network/toc.json)

[Azure service tags](/en-us/azure/virtual-network/service-tags-overview)

[Tutorial \- Restrict network access to PaaS resources with virtual network service endpoints using the Azure portal](/en-us/azure/virtual-network/tutorial-restrict-network-access-to-resources)

[Application security groups](/en-us/azure/virtual-network/application-security-groups)

[Virtual network overview](/en-us/azure/virtual-network/virtual-networks-overview)

[Create, change, or delete an Azure network interface](/en-us/azure/virtual-network/virtual-network-network-interface)

[Azure network security groups overview](/en-us/azure/virtual-network/network-security-groups-overview)

[Create, change, or delete an Azure network security group](/en-us/azure/virtual-network/manage-network-security-group)

[Forced\-tunneling](/en-us/azure/vpn-gateway/vpn-gateway-forced-tunneling-rm?toc=/azure/virtual-network/toc.json)

[Diagnose a virtual machine network traffic routing problem](/en-us/azure/virtual-network/diagnose-network-routing-problem)

[Introduction to flow logging for NSGs \- Azure Network Watcher](/en-us/azure/network-watcher/network-watcher-nsg-flow-logging-overview)

[Deploy and configure Azure Firewall using the Azure portal](/en-us/azure/firewall/tutorial-firewall-deploy-portal)

[Azure Activity Logs content pack for Power BI](/en-us/power-bi/connect-data/service-connect-to-services)

[Monitor logs using Azure Firewall Workbook](/en-us/azure/firewall/firewall-workbook)

[Azure Firewall Policy rule sets](/en-us/azure/firewall/policy-rule-sets)

[Azure Firewall threat intelligence\-based filtering](/en-us/azure/firewall/threat-intel)

[Tutorial: Filter inbound Internet traffic with Azure Firewall DNAT policy using the portal](/en-us/azure/firewall/tutorial-firewall-dnat-policy)

[Azure Firewall rule processing logic](/en-us/azure/firewall/rule-processing)

[Tutorial: Secure your virtual hub using Azure Firewall Manager](/en-us/azure/firewall-manager/secure-cloud-network)

[Tutorial: Diagnose a VM network traffic filter problem \- Azure portal \- Azure Network Watcher](/en-us/azure/network-watcher/diagnose-vm-network-traffic-filtering-problem)

[Test VM network latency](/en-us/azure/virtual-network/virtual-network-test-latency)

[Bandwidth/Throughput testing (NTTTCP)](/en-us/azure/virtual-network/virtual-network-bandwidth-testing)

[VM sizes \- Azure Virtual Machines](/en-us/azure/virtual-machines/sizes?toc=/azure/virtual-network/toc.json)

[About VPN Gateway](/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways)

[Resize a VM](/en-us/azure/virtual-machines/resize-vm?tabs=portal)

[Validate VPN throughput to a virtual network \- Azure VPN Gateway](/en-us/azure/vpn-gateway/vpn-gateway-validate-throughput-to-vnet)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/troubleshoot-network-security-issues/_

## Fuentes
- [Troubleshoot network security issues with Microsoft Azure](https://learn.microsoft.com/en-us/training/modules/troubleshoot-network-security-issues/?WT.mc_id=api_CatalogApi)
