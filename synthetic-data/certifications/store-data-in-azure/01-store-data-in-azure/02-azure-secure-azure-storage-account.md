# Secure your Azure Storage account

> Curso: Store data in Azure (store-data-in-azure) · Seccion: Store data in Azure
> Duracion estimada: 45 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Storage accounts provide a wealth of security options that protect your cloud\-based data. Azure services such as Blob storage, Files share, Table storage, and Data Lake Store all build on Azure Storage. Because of this foundation, the services benefit from the fine\-grained security controls in Azure Storage.

Imagine the network administrator at Contoso is auditing the security of the assets within the domain. At the end of the audit, they need to be satisfied that all the data stored in Azure strictly follows Contoso's security policy. As Contoso's primary data consultant, you help the network administrator understand how Azure Storage can help them meet Contoso's security requirements.

### Learning objectives

In this module, you'll:

* Investigate the ways Azure Storage protects your data.
* Explore the authentication options to access data.
* Learn about Advanced Threat Protection.
* Learn how to control network access to data.
* Explore the Azure Data Lake enterprise\-class security features.

---

## Explore Azure Storage security features

Contoso relies heavily on massive amounts of data in Azure Storage. Their many applications rely on blobs, unstructured table storage, Azure Data Lake, and Server Message Block (SMB)\-based file shares.

After Contoso's competitor has a data breach, Contoso tasks the network administrator to check the organization's data security. As Contoso's data consultant, you assure the network administrator that Azure Storage accounts provide several high\-level security benefits for the data in the cloud:

* Protect the data at rest
* Protect the data in transit
* Support browser cross\-domain access
* Control who can access data
* Audit storage access

### Encryption at rest

All data written to Azure Storage is automatically encrypted by Storage Service Encryption (SSE) with a 256\-bit Advanced Encryption Standard (AES) cipher, and is FIPS 140\-2 compliant. SSE automatically encrypts data when writing it to Azure Storage. When you read data from Azure Storage, Azure Storage decrypts the data before returning it. This process incurs no additional charges and doesn't degrade performance. It can't be disabled.

For virtual machines (VMs), Azure lets you encrypt virtual hard disks (VHDs) by using Azure Disk Encryption. This encryption uses BitLocker for Windows images, and uses dm\-crypt for Linux.

Azure Key Vault stores the keys automatically to help you control and manage the disk\-encryption keys and secrets. So even if someone gets access to the VHD image and downloads it, they can't access the data on the VHD.

### Encryption in transit

Keep your data secure by enabling *transport\-level security* between Azure and the client. Always use *HTTPS* to secure communication over the public internet. When you call the REST APIs to access objects in storage accounts, you can enforce the use of HTTPS by requiring [secure transfer](/en-us/azure/storage/storage-require-secure-transfer) for the storage account. After you enable secure transfer, connections that use HTTP will be refused. This flag will also enforce secure transfer over SMB by requiring SMB 3\.0 for all file share mounts.

### CORS support

Contoso stores several website asset types in Azure Storage. These types include images and videos. To secure browser apps, Contoso locks GET requests down to specific domains.

Azure Storage supports cross\-domain access through cross\-origin resource sharing (CORS). CORS uses HTTP headers so that a web application at one domain can access resources from a server at a different domain. By using CORS, web apps ensure that they load only authorized content from authorized sources.

CORS support is an optional flag you can enable on Storage accounts. The flag adds the appropriate headers when you use HTTP GET requests to retrieve resources from the Storage account.

### Role\-based access control

To access data in a storage account, the client makes a request over HTTP or HTTPS. Every request to a secure resource must be authorized. The service ensures that the client has the permissions required to access the data. You can choose from several access options. Arguably, the most flexible option is role\-based access.

Azure Storage supports Microsoft Entra ID and role\-based access control (RBAC) for both resource management and data operations. For security principals, you can assign RBAC roles that are scoped to the storage account. You can use Microsoft Entra ID to authorize resource management operations, such as configuration. Microsoft Entra ID is supported for data operations on Blob, File, Queue, and Table storage.

You can assign RBAC roles to a security principal or a managed identity for Azure resources that are scoped to a subscription, a resource group, a storage account, or an individual container or queue.

Tip

For optimal security, Microsoft recommends using Microsoft Entra ID with managed identities to authorize requests against blob, queue, table, and file data whenever possible. Authorization with Microsoft Entra ID and managed identities provides superior security and ease of use over Shared Key authorization.

### Auditing access

Auditing is another part of controlling access. You can audit Azure Storage access by using the built\-in Storage Analytics service.

Storage Analytics logs every operation in real time, and you can search the Storage Analytics logs for specific requests. You can filter based on the authentication mechanism, the success of the operation, or the resource that was accessed.

---

## Understand storage account keys

Much of Contoso's data is generated or consumed by custom applications. The applications are written in various languages.

Azure Storage accounts can create authorized apps in Active Directory to control access to the data in blobs and queues. This authentication approach is the best solution for apps that use Blob storage or Queue storage.

For other storage models, clients can use a *shared key*, or shared secret. This authentication option is one of the easiest to use, and it supports blobs, files, queues, and tables. The client embeds the shared key in the HTTP `Authorization` header of every request, and the Storage account validates the key.

For example, an application can issue a `GET` request against a blob resource:

```
GET http://myaccount.blob.core.windows.net/?restype=service&comp=stats

```

HTTP headers control the version of the REST API, the date, and the encoded shared key:

```
x-ms-version: 2018-03-28  
Date: Wed, 23 Oct 2018 21:00:44 GMT  
Authorization: SharedKey myaccount:CY1OP3O3jGFpYFbTCBimLn0Xov0vt0khH/E5Gy0fXvg=

```

### Storage account keys

In Azure Storage accounts, shared keys are called *storage account keys*. Azure creates two of these keys (primary and secondary) for each storage account you create. The keys allow access to *everything* in the account.

You'll find the storage account keys in the Azure portal view of the storage account. In the left menu pane of your storage account, select **Security \+ networking** \> **Access keys**.

### Protect shared keys

The storage account has only two keys, and they provide full access to the account. Because these keys are powerful, use them only with trusted in\-house applications that you control completely.

If the keys are compromised, change the key values in the Azure portal. Here are several reasons to regenerate your storage account keys:

* For security reasons, you might regenerate keys periodically.
* If someone hacks into an application and gets the key that was hard\-coded or saved in a configuration file, regenerate the key. The compromised key can give the hacker full access to your storage account.
* If your team is using a Storage Explorer application that keeps the storage account key, and one of the team members leaves, regenerate the key. Otherwise, the application will continue to work, giving the former team member access to your storage account.

To refresh keys:

* Change each trusted app to use the secondary key.
* Refresh the primary key in the Azure portal. This will be the new secondary key value.

Important

After you refresh keys, any client that attempts to use the old key value will be refused. Make sure you identify all clients that use the shared key and update them to keep them operational.

### Disable Shared Key authorization

Beyond rotating keys, you can remove Shared Key authorization entirely. When you set **Allow storage account key access** to **Disabled** in the storage account's **Configuration** settings, Azure Storage rejects all subsequent requests that use an account access key. Only requests authorized through Microsoft Entra ID succeed.

Disabling Shared Key is the strongest protection against unauthorized key use, and it's a required step before you can apply Microsoft Entra Conditional Access policies to a storage account. Before disabling, migrate your applications to use Microsoft Entra ID\-based authorization (preferably with managed identities) so that their access isn't interrupted.

Tip

Microsoft recommends disabling Shared Key access if it isn't required to prevent its inadvertent use. Use Microsoft Entra ID with managed identities for workloads that support OAuth, Kerberos for Azure Files over SMB, and user delegation SAS tokens for other scenarios.

---

## Understand shared access signatures

As a best practice, you shouldn't share storage account keys with external third\-party applications. If these apps need access to your data, you need to secure their connections without using storage account keys.

For untrusted clients, use a *shared access signature* (SAS). A SAS is a string that contains a security token that can be attached to a URI. You can use a SAS to delegate access to storage objects and specify constraints, such as the permissions and the time range of access.

You can give a customer a SAS token, for example, so they can upload pictures to a file system in Blob storage. Separately, you can give a web app permission to read those pictures. In both cases, you allow only the access that the application needs to do the task.

### Types of shared access signatures

Azure Storage supports three types of shared access signatures.

#### User delegation SAS

A *user delegation SAS* is secured with Microsoft Entra credentials rather than a storage account key. This makes it the most secure type of SAS. Microsoft recommends using a user delegation SAS whenever possible, because it ties the SAS to the identity of the user or service principal that created it. A user delegation SAS is supported for Blob Storage (including Data Lake Storage), Queue Storage, Table Storage, and Azure Files.

#### Service SAS

A *Service SAS* (formerly called service\-level SAS) allows access to a resource in a single Azure Storage service. Use this type of SAS, for example, to allow an app to retrieve a list of files in a file system, or to download a file. A service SAS is signed with the storage account key.

#### Account SAS

An *Account SAS* (formerly called account\-level SAS) allows access to anything that a Service SAS can allow, plus additional resources and abilities. For example, you can use an Account SAS to allow the ability to create file systems. An Account SAS is also signed with the storage account key.

Important

For scenarios where a SAS is needed, Microsoft recommends using a user delegation SAS when possible. A user delegation SAS is more secure because it uses Microsoft Entra credentials instead of the account key, which could otherwise be compromised.

You'd typically use a SAS for a service where users read and write their data to your storage account. Accounts that store user data have two typical designs:

* Clients upload and download data through a front\-end proxy service, which performs authentication. This front\-end proxy service has the advantage of allowing validation of business rules. But, if the service must handle large amounts of data or high\-volume transactions, you might find it complicated or expensive to scale this service to match demand.
* A lightweight service authenticates the client, as needed. Next, it generates a SAS. After receiving the SAS, the client can access storage account resources directly. The SAS defines the client's permissions and access interval. It reduces the need to route all data through the front\-end proxy service.

---

## Control network access to your storage account

By default, storage accounts accept connections from clients on any network. To limit access to selected networks, you must first change the default action. You can restrict access to specific IP addresses, ranges, or virtual networks.

### Private endpoints

For maximum network isolation, use a *private endpoint* for your storage account. A private endpoint assigns a private IP address from your virtual network to the storage account. Network traffic between clients in the virtual network and the storage account travels over the virtual network and a private link on the Microsoft backbone network—it never reaches the public internet.

With a private endpoint, you can also configure the storage account firewall to block all access over the public endpoint, ensuring data is reachable only from within your virtual network or connected on\-premises networks (via VPN or ExpressRoute). Private endpoints incur extra costs but provide the strongest network isolation option.

Note

Creating a private endpoint doesn't automatically block the public endpoint. You must explicitly configure the storage firewall to deny public access if you want all traffic to flow only through the private endpoint.

Important

Changing network rules can affect your application's ability to connect to Azure Storage. If you set the default network rule to *deny*, you block all access to the data unless specific network rules *grant* access. Before you change the default rule to deny access, be sure to use network rules to grant access to any allowed networks.

### Manage default network access rules

You can manage default network access rules for storage accounts through the Azure portal, PowerShell, or the Azure CLI.

Follow these steps to change default network access in the Azure portal.

1. Go to the storage account you want to secure.
2. Select **Networking** in the left\-hand pane.
3. To restrict access to only selected networks and IPs, select **Enabled from selected virtual networks and IP addresses**. To enable public network access for all networks, including the internet, select **Enabled from all networks**.
4. To apply your changes, select **Save**.

---

## Understand Advanced Threat Protection for Azure Storage

Microsoft Defender for Storage provides an extra layer of security intelligence that detects unusual and potentially harmful attempts to access or exploit storage accounts. This layer of protection allows you to address threats without being a security expert or managing security\-monitoring systems.

Security alerts are triggered when anomalies in activity occur. These security alerts are integrated with Microsoft Defender for Cloud, and are also sent via email to subscription administrators, with details of suspicious activity and recommendations on how to investigate and remediate threats.

Microsoft Defender for Storage is currently available for Blob storage, Azure Files, and Azure Data Lake Storage Gen2\. Account types that support Microsoft Defender for Cloud include general\-purpose v2, block blob, and Blob storage accounts. Microsoft Defender for Storage is available in all public clouds and US government clouds, but not in other sovereign or Azure Government cloud regions.

The recommended approach is to enable Microsoft Defender for Storage at the subscription level, which automatically protects all existing and new storage accounts in that subscription. Follow these steps.

1. Launch the Azure portal and go to **Microsoft Defender for Cloud**.
2. Select **Environment settings** and choose the subscription you want to protect.
3. On the **Defender plans** pane, locate **Storage** in the list, set the toggle to **On**, and select **Save**.

Note

The classic per\-transaction Defender for Storage plan is no longer available for new subscriptions as of February 5, 2025\. The current plan charges per storage account and includes malware scanning and sensitive data threat detection. Subscription\-level enablement may take up to 24 hours to apply across all storage accounts.

### Explore security anomalies

When storage activity anomalies occur, you'll receive an email notification with information about the suspicious security event. Details of the event include:

* Nature of the anomaly
* Storage account name
* Event time
* Storage type
* Potential causes
* Investigation steps
* Remediation steps
* Email also includes details about possible causes and recommended actions to investigate and mitigate the potential threat

You can review and manage your current security alerts from Microsoft Defender for Cloud's Security alerts tile. Selecting a specific alert provides details and actions for investigating the current threat and addressing future threats.

---

## Explore Azure Data Lake Storage security features

Azure Data Lake Storage Gen2 provides a first\-class data lake solution that enables enterprises to consolidate their data. It's built on Azure Blob storage, so it inherits all of the security features we've reviewed in this module.

Along with role\-based access control (RBAC), Azure Data Lake Storage Gen2 provides access control lists (ACLs) that are POSIX\-compliant, and that restrict access to only authorized users, groups, or service principals. It applies restrictions in a way that's flexible, fine\-grained, and manageable. Azure Data Lake Storage Gen2 authenticates through Microsoft Entra ID OAuth 2\.0 bearer tokens. This allows for flexible authentication schemes, including federation with Microsoft Entra Connect and multifactor authentication that provides stronger protection than just passwords.

More significantly, these authentication schemes are integrated into the main analytics services that use the data. These services include Azure Databricks, HDInsight, and Azure Synapse Analytics. Management tools, such as Azure Storage Explorer, are also included. After authentication finishes, permissions are applied at the finest granularity to ensure the right level of authorization for an enterprise's large\-data assets.

The Azure Storage end\-to\-end encryption of data and transport layer protections complete the security shield for an enterprise data lake. The same set of analytics engines and tools can take advantage of these additional layers of protection, resulting in complete protection of your analytics pipelines.

---

## Summary

Azure Storage provides a layered security model. You can use this model to secure your storage accounts to a specific set of supported networks. When you set up network rules, only applications that request data over the specified networks can access your storage account.

Authorization is supported by Microsoft Entra credentials (for blobs, files, queues, and tables), a valid account access key, or a shared access signature (SAS) token. Data encryption is enabled by default, and you can proactively monitor systems by using Advanced Threat Protection.

### Check your knowledge

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/_

## Fuentes
- [Secure your Azure Storage account](https://learn.microsoft.com/en-us/training/modules/secure-azure-storage-account/?WT.mc_id=api_CatalogApi)
