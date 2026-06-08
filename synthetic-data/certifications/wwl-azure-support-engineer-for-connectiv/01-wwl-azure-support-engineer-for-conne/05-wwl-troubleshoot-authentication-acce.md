# Troubleshoot authentication and access control issues in Microsoft Azure

> Curso: Azure Support Engineer for Connectivity Specialty (wwl-azure-support-engineer-for-connectivity-specia) · Seccion: Azure Support Engineer for Connectivity Specialty
> Duracion estimada: 32 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You work as an administrator looking after your company’s Microsoft Entra authentication and access control. Because authentication and access control is crucial to the robust, secure, and effective functioning of both Azure\-based and hybrid systems, you can react both proactively and reactively to any authentication and authorization issues.

Microsoft Azure has a sophisticated authentication and access control system to provide high security. Microsoft Entra authentication includes self\-service password reset, multifactor authentication, hybrid integration, and passwordless authentication.

In this module, you’ll learn how to troubleshoot a deployment of Microsoft Entra ID that is based entirely in the cloud and a hybrid deployment of Microsoft Entra ID that is part cloud\-based and part on\-premises. You'll also learn how to troubleshoot authorization issues when using Microsoft Azure.

### Learning objectives

After completing this module, you’ll be able to:

* Troubleshoot Microsoft Entra authentication.
* Troubleshoot hybrid authentication.
* Troubleshoot authorization issues.

### Prerequisites

* Demonstrate an understanding of the OSI model
* Demonstrate an understanding of PowerShell
* Demonstrate an understanding of Azure CLI

---

## Troubleshoot hybrid authentication in Microsoft Azure

Many systems have a mixture of Azure and on\-premises and use a hybrid identity solution. Microsoft Entra Connect is an on\-premises application that synchronizes Microsoft Entra ID with on\-premises Active Directory.

Determine why on\-premises systems cannot connect to Microsoft Entra resources

To troubleshoot Microsoft Entra Connect, you should use the Microsoft Entra Connect Health portal at [Microsoft Entra Connect Health](https://portal.azure.com/) to view performance monitors and alerts.

You can also install the Microsoft Entra Connect Administration Agent on a Microsoft Entra Connect server. The Microsoft Entra Connect Administration Agent presents diagnostic data to Microsoft support engineers. Microsoft Entra Connect Administration Agent is not installed by default and doesn’t store any data. It is specifically intended for live troubleshooting. You can disable the reporting of data by the Microsoft Entra Connect Administration Agent if you edit the service config file. For more information on the Microsoft Entra Connect Administration Agent and how to install and disable it, see [What is the Microsoft Entra Connect Admin Agent](/en-us/azure/active-directory/hybrid/whatis-aadc-admin-agent).

To troubleshoot connectivity issues, you should install Microsoft Entra Connect Health agents. There are Microsoft Entra Connect Health agents for AD FS, Azure ADFS, and Sync. For detailed steps on installing the Microsoft Entra Connect Health agents, see [Microsoft Entra Connect Health agent installation](/en-us/azure/active-directory/hybrid/how-to-connect-health-agent-install).

To troubleshoot connectivity issues, you must first have installed AD Connect in your on\-premises environment. For more information on installing Microsoft Entra Connect, see [Microsoft Entra Connect and Microsoft Entra Connect Health installation roadmap](/en-us/azure/active-directory/hybrid/how-to-connect-install-roadmap).

### Troubleshoot pass\-through authentication and password hash sync issues

To troubleshoot pass\-through authentication, you should first check that it is enabled and that the authentication agents are **Active**. To view the status, go to **Microsoft Entra Admin** Center and select **Microsoft Entra Connect**.

You should then check if the user is getting errors, or if errors are reported in the **Microsoft Entra admin center**. For more information, see [Troubleshoot Microsoft Entra pass\-through authentication](/en-us/azure/active-directory/hybrid/tshoot-connect-pass-through-authentication).

Troubleshooting password hash synchronization with Microsoft Entra Connect Sync depends on the version you use. There are different steps depending on whether one or many objects have password synchronization issues. Detailed steps for each scenario are available at [Troubleshoot password hash synchronization with Microsoft Entra Connect Sync](/en-us/azure/active-directory/hybrid/tshoot-connect-password-hash-synchronization).

### Review and resolve object synchronization with Microsoft Entra Connect Sync

To resolve object sync issues, start by running the troubleshooting task in the wizard. You should complete the following steps:

* On your Microsoft Entra Connect server, start a Windows PowerShell with the Run as Administrator option and run Set\-ExecutionPolicy RemoteSigned.
* Start the Microsoft Entra Connect wizard, select **Tasks**, select **Troubleshoot** then select **Next**.
* Click **Launch** and type **1** to **Troubleshoot Object Synchronization**.

For more information, see [Troubleshoot object synchronization with Microsoft Entra Connect Sync](/en-us/azure/active-directory/hybrid/tshoot-connect-objectsync).

### Troubleshoot Microsoft Entra application proxy connectivity issues

To troubleshoot Microsoft Entra application proxy connectivity issues, do the following steps:

On your on\-premises Active Directory server, open the Windows Services console and ensure that the **Microsoft AAD Application Proxy Conne**ctor service is enabled and running.

To discover events that could be causing problems, open Event Viewer and look for Application Proxy connector events in **Applications and Services** **Logs** \> **Microsoft** \> **AadApplicationProxy** \> **Connector** \> **Admin**.

For more information, see [Troubleshoot Application Proxy problems and error messages](/en-us/azure/active-directory/app-proxy/application-proxy-troubleshoot).

### Troubleshoot Active Directory Domain Service

When troubleshooting Microsoft Entra ID to Active Directory Domain Service integration, you need to troubleshoot Microsoft Entra Domain Services. Common issues for Microsoft Entra Domain Services include:

* Problems enabling Microsoft Entra Domain Services.
* Microsoft Graph is disabled—this must be enabled to synchronize your Microsoft Entra tenant.
* Users in your Microsoft Entra tenant are unable to sign into the managed domain.
* There are alerts in your managed domain.

For more information, see [Common errors and troubleshooting steps for Microsoft Entra Domain Services](/en-us/azure/active-directory-domain-services/troubleshoot).

---

## Troubleshoot authorization issues with Microsoft Azure

When a user has been authenticated, they must be authorized to carry out actions. If a user can't complete a required action, but their identity is correctly authenticated, you need to troubleshoot authorization issues.

### Troubleshoot Conditional Access

Conditional Access policies use numerous signals to decide whether a user should have access to a resource. For example, the user's geographic location, type of device, and application being used can all be considered, alongside the user's identity.

#### Troubleshoot Conditional Access policy changes

If Conditional Access was previously working successfully, but is now not functioning as expected, you should investigate policy changes. Audit log data is held for 30 days and this can be increased in Microsoft Entra Diagnostic settings.

To view the audit log in the Azure portal, select **Microsoft Entra ID** then select Audit logs. Select the relevant date range and, in **Activity**, select **Add conditional access policy**, or **Update conditional access policy**, or **Delete conditional access policy**.

#### Troubleshoot sign\-in problems with Conditional Access

To avoid sign\-in problems with Conditional Access, be very cautious if policies apply to all users, all cloud apps, or all devices. These policies could potentially block the entire organization.

To troubleshoot sign\-in problems, you should initially review the error message. This will typically list the policy that is causing the problem and allow you to identify the policy to update. By clicking **More details** on the error message you can find the specific sign\-in event.

When you have the details of the sign\-in event, you can open the Azure portal, select **Microsoft Entra ID** then select **Sign\-ins**. Add filters to find the correct type of events, such as Conditional Access failures, and find the specific event.

You can then select the event to view more details and the policy details for that event.

#### The What If tool

The What If tool is also available to help with troubleshooting.

Open the Azure portal, select **Microsoft Entra ID**, select **Conditional Access** then select **What If**. You can now add conditions and see which Conditional Access policies will be applied.

For more information, see [Microsoft Entra Conditional Access documentation](/en-us/azure/active-directory/conditional-access/).

### Troubleshoot role\-based access control

A wide range of issues could affect role\-based access control (RBAC). These issues include:

* A limit to the number of role assignments.
* Having correct permissions to work with roles.
* Losing role assignments when subscriptions are transferred to a different Microsoft Entra directory, or resources are moved.
* Security principals deleted or only recently created.
* Management capabilities requiring write access.

For more information, see [Troubleshoot Azure RBAC](/en-us/azure/role-based-access-control/troubleshooting).

### Troubleshoot issues when storing encrypted passwords in Azure Key Vault

Azure Key Vault uses access policies to authorize user actions. There are many steps to troubleshoot Azure Key Vault access policy issues. For more information, see [Troubleshooting Azure key vault access policy issues](/en-us/azure/key-vault/general/troubleshooting-access-issues).

---

## Demo: Troubleshoot authentication and access control issues

In this demonstration you will see how to proactively troubleshoot Conditional Access policies using the What if tool in the Azure portal:

---

## Module assessment

Choose the best answer for each of the questions below.

### Check your knowledge

---

## Summary

In this module, you learned how to troubleshoot a deployment of Microsoft Entra ID that is based entirely in the cloud and a hybrid deployment of Microsoft Entra ID that is part cloud\-based and part on\-premises. You also learned how to troubleshoot authorization issues when using Microsoft Azure.

Now that you've completed this module, you should be able to:

* Troubleshoot Microsoft Entra authentication.
* Troubleshoot hybrid authentication.
* Troubleshoot authorization issues.

### Learn more

For more information about the topics discussed in this module, see:

[How it works: Microsoft Entra self\-service password reset.](/en-us/azure/active-directory/authentication/concept-sspr-howitworks)

[Troubleshoot Microsoft Entra multifactor authentication issues.](/en-us/troubleshoot/azure/active-directory/troubleshoot-azure-mfa-issue)

[Tutorials for integrating SaaS applications with Microsoft Entra ID.](/en-us/azure/active-directory/saas-apps/tutorial-list)

[Quickstart: Add an enterprise application.](/en-us/azure/active-directory/manage-apps/add-application-portal)

[Configure how users consent to applications.](/en-us/azure/active-directory/manage-apps/configure-user-consent?tabs=azure-portal)

[Enable security audits for Microsoft Entra Domain Services.](/en-us/azure/active-directory-domain-services/security-audit-events)

[Troubleshoot account lockout problems with a Microsoft Entra Domain Services managed domain.](/en-us/azure/active-directory-domain-services/troubleshoot-account-lockout)

[What is the Microsoft Entra Connect Admin Agent?](/en-us/azure/active-directory/hybrid/whatis-aadc-admin-agent)

[Microsoft Entra Connect Health agent installation.](/en-us/azure/active-directory/hybrid/how-to-connect-health-agent-install)

[Microsoft Entra Connect and Microsoft Entra Connect Health installation roadmap.](/en-us/azure/active-directory/hybrid/how-to-connect-install-roadmap).

[Troubleshoot Microsoft Entra pass\-through authentication.](/en-us/azure/active-directory/hybrid/tshoot-connect-pass-through-authentication).

[Troubleshoot password hash synchronization with Microsoft Entra Connect Sync.](/en-us/azure/active-directory/hybrid/tshoot-connect-password-hash-synchronization).

[Troubleshoot object synchronization with Microsoft Entra Connect Sync.](/en-us/azure/active-directory/hybrid/tshoot-connect-objectsync)

[Troubleshoot Application Proxy problems and error messages.](/en-us/azure/active-directory/app-proxy/application-proxy-troubleshoot)

[Common errors and troubleshooting steps for Microsoft Entra Domain Services.](/en-us/azure/active-directory-domain-services/troubleshoot)

[Microsoft Entra Conditional Access documentation.](/en-us/azure/active-directory/conditional-access/)

[Troubleshoot Azure RBAC.](/en-us/azure/role-based-access-control/troubleshooting)

[Troubleshooting Azure key vault access policy issues.](/en-us/azure/key-vault/general/troubleshooting-access-issues)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/troubleshoot-authentication-access-control/_

## Fuentes
- [Troubleshoot authentication and access control issues in Microsoft Azure](https://learn.microsoft.com/en-us/training/modules/troubleshoot-authentication-access-control/?WT.mc_id=api_CatalogApi)
