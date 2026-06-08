# Implement access management for Azure resources

> Curso: Deploy and administer Linux virtual machines on Azure (wwl-deploy-administer-linux-virtual-machines-azure) · Seccion: Deploy and administer Linux virtual machines on Azure
> Duracion estimada: 30 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

This module will cover how to assign and manage access to resources in Azure using Azure roles. When you create a resource, you want to know that only specific access is granted to users and groups. Only allow users that need to access data or a resource, the permissions to do so. How can you control access? By assigning a role with the specific permissions needed. There are built\-in Azure roles and you can create custom\-roles as needed.

An application might also need to have permission to access data or other Azure resources. Learn how to set up managed identities, which allow the application to gain access to only resources you allow. You can give granular access to secrets, keys, and certificates stored in a key vault to your users and applications. You protect both the items stored in the key vault, and who can use them. And finally, you'll look at the new tool Microsoft Entra Permission Management. Learn to gather, review, and restrict the permission assigned across your cloud solutions.

#### Learning objectives

By the end of this module will be able to:

* Assign Azure roles and custom roles to access Azure resources.
* Create and manage application access with managed identities.
* Configure and manage access into Azure Key Vault.
* Retrieve object from a key vault securely.
* Explore the capabilities of Microsoft Entra Permissions Management.

#### Prerequisites

None

---

## Assign Azure roles

Azure role\-based access control (Azure RBAC) is the authorization system you use to manage access to Azure resources. To grant access, you assign roles to users, groups, service principals, or managed identities at a particular scope. Primary steps to follow when assigning an Azure role:

1. Who needs access?

	* **User** \- Only a single person is needed for the task. You can assign a role to users in other tenants.
	* **Group** \- Use when you need to grant a set of users the same role.
	* **Service Principal** \- Assign a role to a service principal when you want to grant an application access to an Azure resource.
	* **Managed Identity** \- Use the managed identity when you want an application to manage credentials for authentication.
2. Select the right role. Use the built\-in roles or create a custom role with the specific capabilities you need.

* Built\-in Azure roles

	+ Owner \- full access to all resources.
	+ Contributor \- Can create and manage all types of Azure resources, but can't grant access.
	+ Reader \- Can view the available Azure resources.
	+ User Access Administrator \- Assign access to Azure resources.
	+ Other task specific roles, like Virtual Machine Contributor, can be assigned.

3. Identify what level to assign the role (the Scope). Scope is the set of resources that the access applies to. In Azure, you can specify a scope at four levels: management group, subscription, resource group, and resource. Scopes are structured in a parent\-child relationship. Each level of hierarchy makes the scope more specific. You can assign roles at any of these levels of scope. The level you select determines how widely the role is applied. Lower levels inherit role permissions from higher levels. Example:

	* If you assign the **Reader role** to a user at the **management group scope**, that user can read everything in all subscriptions in the management group.
	* If you assign the **Billing Reader role** to a group at the **subscription scope**, the members of that group can read billing data for every resource group and resource in the subscription.
	* If you assign the **Contributor role** to an application at the **resource group scope**, it can manage resources of all types in that resource group, but not other resource groups in the subscription. It's a best practice to grant security\-principals the least privilege they need to perform their job. Avoid assigning broader roles at broader scopes even if it initially seems more convenient. By limiting roles and scopes, you limit what resources are at risk if the security\-principal is ever compromised. For more information, see Understand scope.
4. Confirm the currently logged in user has the rights need to assign the Azure role.
5. Assign the role. Once you know the security\-principal, role, and scope, you can assign the role. You can assign roles using the Azure portal, Azure PowerShell, Azure CLI, Azure SDKs, or REST APIs. You can have up to 4,000 role assignments in each subscription. This limit includes role assignments at the subscription, resource group, and resource scopes. You can have up to 500 role assignments in each management group.

#### Assign an Azure role from the portal

Whether you are in the User, Group, Resource Group, or Subscription you use the Access content (IAM) page to make the assign. The official name is identity and access management (IAM) and appears in several locations in the Azure portal.

#### Assign an Azure role with script

PowerShell using the Microsoft Graph PowerShell cmdlet

```
New-AzRoleAssignment -ObjectId <objectId> `
-RoleDefinitionName <roleName> `
-Scope /subscriptions/<subscriptionId>/resourcegroups/<resourceGroupName>/providers/<providerName>/<resourceType>/<resourceSubType>/<resourceName>

```

CLI scripting

```
az role assignment create --assignee "{assignee}" \
--role "{roleNameOrId}" \
--resource-group "{resourceGroupName}"

```

---

## Configure custom Azure roles

If the Azure built\-in roles don't meet the specific needs of your organization, you can create your own Azure custom roles. Just like built\-in roles, you can assign custom roles to users, groups, and service principals at management group (in preview only), subscription and resource group scopes. Custom roles are stored in a Microsoft Entra ID and can be shared across subscriptions. Each directory can have up to 5000 custom roles. Custom roles can be created using the Azure portal, Azure PowerShell, Azure CLI, or the REST API.

#### Create the custom role from the user interface

You would assign a custom role to a user, group, or other resource the same as you do for built\-in. Your admin gets to control exactly with capabilities the custom role has access to. The principle of least privilege let's you pick just the capabilities you need. To create the custom role:

1. Open Microsoft Entra admin center.
2. From the **Identity** menu, Select **Roles and administration**.
3. Select **\+ New custom role**.
4. Then name and assign the capabilities needed.

#### Create a custom role from a JSON template

You can use a JSON file to create a custom role. Here's a sample:

```
{
    "properties": {
        "roleName": "Billing Reader Plus",
        "description": "Read billing data and download invoices",
        "assignableScopes": [
            "/subscriptions/your-subscription-number"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.Authorization/*/read",
                    "Microsoft.Billing/*/read",
                    "Microsoft.Commerce/*/read",
                    "Microsoft.Consumption/*/read",
                    "Microsoft.Management/managementGroups/read",
                    "Microsoft.CostManagement/*/read",
                    "Microsoft.Support/*"
                ],
                "notActions": [],
                "dataActions": [],
                "notDataActions": []
            }
        ]
    }
}

```

The asterisk (`*`) is used as a wildcard. If you need to assign all of the **read** permissions from the **Billing** resource that use this command **Microsoft/Billing/\*/read**. The wildcard can exist at any level.

---

## Create and configure managed identities

A common challenge when creating a cloud solution is the management of secrets, credentials, certificates, and keys. These secure elements are used to secure communication between services. Managed identities eliminate the need for developers to manage these credentials.

While developers can securely store the secrets in Azure Key Vault, services need a way to access Azure Key Vault. Managed identities provide an automatically managed identity in Microsoft Entra ID for applications to use when connecting to resources. The managed identity supports authentication via Microsoft Entra ID. Applications can use managed identities to obtain Microsoft Entra tokens without having to manage any credentials.

#### Benefits of using managed identities

* You don't need to manage credentials. Credentials aren’t even accessible to you.
* You can use managed identities to authenticate to any resource that supports Microsoft Entra authentication, including your own applications. Managed identities can be used without any extra cost.

#### Types of managed identity

| **Identity type** | **Description and usage** |
| --- | --- |
| System\-assigned | Some Azure services allow you to enable a managed identity directly on a service instance. When you enable a system\-assigned managed identity, an identity is created in Microsoft Entra ID. The identity is tied to the lifecycle of that service instance. When the resource is deleted, Azure automatically deletes the identity for you. By design, only that Azure resource can use this identity to request tokens from Microsoft Entra ID. |
| User\-assigned | You might also create a managed identity as a standalone Azure resource. You can create a user\-assigned managed identity and assign it to one or more instances of an Azure service. For user\-assigned managed identities, the identity is managed separately from the resources that use it. |

Always remember that managed identities are assigned to an application. So, you need to configure and manage the identity within the services they're being used. If you have an application running in a virtual machine (Linux or Windows), then you add and configure the identity there. If you're using a managed identity with a cloud\-app, function, or app service, then you configure and manage it there. Let's look at adding a managed identity to a cloud\-built app using the App Service.

#### Managed identity in Azure portal for an App Service

The basic steps, to create and add an identity to your app, are:

1. Build your App.
2. Open the App in the Azure portal.
3. Select **Identity** from the menu then select either **System assigned** or **User assigned**.
4. Select the **\+ Add** item and complete the wizard.

You can perform a similar action using script within the CLI, PowerShell, or with a template. Sample could look like:

**Using the CLI**

```
az webapp identity assign --resource-group <group-name> --name <app-name> --identities <identity-name>

```

Or using **PowerShell** with the AZ.ManagedServiceIdentity module installed

```
Update-AzFunctionApp -Name <app-name> -ResourceGroupName <group-name> -IdentityType UserAssigned -IdentityId $userAssignedIdentity.Id

```

Or within a **template**

```
"identity": {
    "type": "UserAssigned",
    "userAssignedIdentities": {
        "<RESOURCEID>": {}
    }
}

```

#### Value of managed identity

As stated at the beginning of this page, when you build an app, you need a method to grant it access to resources. To take advantage of the concepts of **zero trust** you can use managed identities. You only assign the minimum privileges that the managed identity needs. Then only assign access the minimum resources needed. Least\-privilege will keep your applications and data protected.

---

## Access Azure resources with managed identities

Managed identities for Azure resources are a feature of Microsoft Entra ID. Each Azure service that supports managed\-identities are subject to their own timeline. Make sure you review the availability status of managed identities for your resource and known issues before you begin. After you've configured an Azure resource with a managed identity, you can give the managed identity access to another resource.

#### Add access to other resources

After you've enabled managed identity on an Azure resource, such as an Azure App Service application or Azure virtual machine, you might need to grant access to more resources. Let's say you want add access to a storage account to your managed identity.

1. Sign in to the Azure portal using an account associated with the Azure subscription under which you've configured the managed identity.
2. Navigate to the desired resource on which you want to modify access control. In this example, we're giving an Azure virtual machine access to a storage account, so we navigate to the storage account.
3. Select Access control (IAM).
4. Select Add \> Add role assignment to open the Add role assignment page.
5. Pick the Owner, Contributor, or Reader based on the least privilege rules for your applications needs.
6. Select the managed identity you want assigned.
7. Complete the assignment with the **Review \+ assign** option.

---

## Analyze Azure role permissions

What is a permission? The dictionary definition of permission is the **consent or authorization to perform a specific action**. In Microsoft Entra ID, you've permissions for each of the operations you're able to do. Permission can range from viewing your settings, to be able to change your setting. Then move on to granting permission to add or remove users and beyond. There are two primary places where permission can be assigned, at a user or group level. However, they all pass down to the user at the final point. When dealing with users, you've both a member\-user and a guest\-user. The default permissions for the guest\-user are slightly less than the member.

#### What is a sample of the default permissions for users?

| **Member Users** | **Guest Users** |
| --- | --- |
| Enumerate list of users and their contacts | Read own properties |
| Invite guest users | Invite guest users |
| Can create Security and Microsoft 365 Groups | Can search for nonhidden groups by name |
| Register new applications | Read properties of registered and enterprise applications |

Note

This is just a small subset, to show differences. If you want a full list of the [Default User Permissions](/en-us/azure/active-directory/fundamentals/users-default-permissions)

#### Controlling permissions \- add and restrict

| **User settings** | **Roles and administrators** |
| --- | --- |
|  |  |

You can use the **User Settings** inside of Microsoft Entra ID – Manage menu to restrict or control the default permissions of the default users. Or you can use Roles and administrators to add new permissions onto your users and group. Always use the concept of Least Privilege and make sure the users only have the rights they need. In User settings you can restrict the user's ability to:

* Register applications
* Access the Azure portal
* Block LinkedIn connections
* Manage settings for external collaboration

By adding roles to a given user account or group, you can add permissions on to member users, guest users, and service principals. Adding roles gives permissions to perform specific activities. Actions are limited, which allows the rule of least privilege.

#### Exploring available permissions

You only want to grant the permissions a user needs. So be careful to know what all permissions are granted when you assign a role. You can see the list of permissions in the **Attribute definition reader**. To open it, launch Microsoft Entra ID, then open the **Roles and administrators** screen. Next select a role, and open its description page from the ellipsis (...) menu. Depending on the role you chose, you'll see a large number of permissions or possibly a small number. Two sets of permissions:

* Role permissions
* Guest and service principal basic read permissions

---

## Retrieve objects from Azure Key Vault

Azure Key Vault is a secure tool for storing secrets, keys, and certificate. Once stored, these items can be used by users and applications to perform actions and operations in a secure method. The process to retrieve any of these resources is common. So we'll look at how to review a secret from a key vault.

#### Add a secret to your key vault

To add a secret to the vault, follow the steps:

1. Navigate to your new key vault in the Azure portal
2. On the Key Vault settings pages, select **Secrets**.
3. Select on **Generate/Import**.
4. On the Create a secret screen choose the following values:

| **Setting** | **Value to enter** |
| --- | --- |
| Upload options | Manual |
| Name | mySC300keyvaultSecret |
| Value | This is my secret |
5. Select **Create**.

#### Retrieve a secret using the Azure portal

This process is simple. Open your key vault, then open the secret you created. Select the **Show secret value** button.

#### Retrieve a secret using CLI or PowerShell

You can quickly and easily grab a secret from your key vault using scripting languages.

**CLI**

```
az keyvault secret show --name "mySC300keyvaultSecret" --vault-name "<your-unique-keyvault-name>" --query "value"

```

***PowerShell***

```
$secret = Get-AzKeyVaultSecret -VaultName "<your-unique-keyvault-name>" -Name "mySC300keyvaultSecret" -AsPlainText

```

#### Retrieve a secret in an application

If you're building an application that needs access to your key vault secrets, certificates, and keys that can be done. You can access the key vault using .NET, Node.js, Python, and other languages.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/implement-access-management-for-azure-resources/_

## Fuentes
- [Implement access management for Azure resources](https://learn.microsoft.com/en-us/training/modules/implement-access-management-for-azure-resources/?WT.mc_id=api_CatalogApi)
