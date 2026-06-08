# Secure Windows Server user accounts

> Curso: Secure Windows Server on-premises and hybrid infrastructures (wwl-secure-windows-server-premises-hybrid-infrastr) · Seccion: Secure Windows Server on-premises and hybrid infrastructures
> Duracion estimada: 38 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

The first step in securing Windows Server is to ensure that you've properly configured user accounts. First, confirm the accounts have only the privileges needed to perform necessary tasks by using the principal of least privilege. Additionally, you need to protect user account credentials from compromise by restricting resources that accounts can use to authenticate against, and the protocols that can be used for that authentication

### Learning objectives

After completing this module, you'll be able to:

* Configure and manage user accounts to limit security threats across an organization
* Apply Protected Users settings, policies, and authentication silos to protect highly privileged user accounts
* Describe and configure Windows Defender Credential Guard
* Configure Group Policy to block the use of NTLM for authentication
* Disable inactive accounts and require periodic password updates

### Prerequisites

To get the best learning experience from this module, you should have:

* Familiarity with managing Active Directory Domain Services security principals
* Ability to edit Active Directory Group Policy settings
* Experience performing basic Windows Server administration tasks

---

## Locate problematic accounts

You should check your AD DS environment for accounts that haven't signed in for a specific period of time, or that have passwords with no expiration date.

Inactive user accounts usually indicate a person that has left the organization and organization processes have failed to remove or disable the account. The account might also have originally been shared by IT staff, but is no longer in use. These extra accounts represent additional opportunities for unauthorized users to gain access to your network resources.

Accounts with fixed passwords are less secure than accounts that are required to update their password periodically. If a third\-party user obtains a user’s password, that knowledge is only valid until the user updates the password. If you configure an account with a password that the user doesn't have to update periodically, then a potential cybercriminal could have access to your network indefinitely. Ensuring regular password updates is especially important for highly privileged accounts.

When you find accounts that haven’t signed in for a specified number of days, you can disable those accounts. Disabling them allows you to reenable them should the person return. After you’ve located accounts that are configured with passwords that don't expire, you can take steps to ensure that an appropriate password update policy is enforced.

Note

User accounts with credentials shared by multiple IT staff members should be avoided, even if they have a strong password policy. Shared accounts make it hard to track which individual performed a specific administrative task.

You can use Windows PowerShell or the AD DS Administrative Center to find problematic users. To use Windows PowerShell to find active users with passwords set to never expire, use the following command:

```
Get-ADUser -Filter {Enabled -eq $true -and PasswordNeverExpires -eq $true}

```

Use the following Windows PowerShell command to find users that haven't signed in within the last 90 days, using Windows PowerShell:

```
Get-ADUser -Filter {LastLogonTimeStamp -lt (Get-Date).Adddays(-(90))-and enabled -eq $true} -Properties LastLogonTimeStamp

```

---

## Module assessment

Choose the best response for each of the questions below.

---

### Check your knowledge

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/secure-windows-server-user-accounts/_

## Fuentes
- [Secure Windows Server user accounts](https://learn.microsoft.com/en-us/training/modules/secure-windows-server-user-accounts/?WT.mc_id=api_CatalogApi)
