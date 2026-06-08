# Perform Windows Server secure administration

> Curso: Manage Windows Servers and workloads in a hybrid environment (wwl-manage-windows-servers-workloads-hybrid-enviro) · Seccion: Manage Windows Servers and workloads in a hybrid environment
> Duracion estimada: 40 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Understand the principle of least privilege, know when to use privileged access workstations, and be able to identify built\-in privileged accounts.

### Scenario

Contoso, Ltd. is a financial services company in Seattle with major offices located throughout the world. Most of its compute environment runs on\-premises on Windows Server. This includes virtualized workloads on Windows Server 2016 hosts.

Contoso's IT staff are migrating Contoso on\-premises servers to Windows Server 2025\. As part of the migration, Contoso plans to expand into additional sites and use virtualization to help expedite bringing a new site online. The company is also generating larger volumes of data with plans for even more data in the future. Because of this, the company needs flexible storage options. Finally, Contoso plans to increase the use of virtualization to optimize their computing environment because many physical servers are underutilized.

As a Windows Server administrator, you're responsible for managing and maintaining the server infrastructure that will help Contoso achieve its business goals. Your first task is to determine how best to administer Windows Server. In the past, you’ve mostly signed in as an administrator at the server you wanted to administer. However, you now want to perform administration remotely, and use the principle of least privilege.

By the end of this module, you know which user accounts you should use to perform administrative tasks, and you understand how to perform Windows Server administration securely.

### Learning objectives

After completing this module, you'll be able to:

* Explain least privilege administrative models.
* Implement delegated privilege.
* Describe privileged access workstations.
* Describe jump servers.

### Prerequisites

To get the best learning experience from this module, you should have knowledge and experience of:

* Windows Server.
* Basic security best practices.
* Windows client operating systems such as Windows 10\.
* Working with command\-line tools.

---

## Define least privilege administration

A firm of IT security specialists have been working at Contoso. They've produced a report for the main board. The report identifies that most security breaches or data loss incidents at Contoso in the recent past were the result of human error, malicious activity, or both.

The report gave numerous examples, including signing in with administrative privilege and performing standard user tasks. In one cited example, a user signed in with Enterprise Admins rights and opened an email attachment that ran malicious code. That code then had full administrative rights across the Contoso enterprise because the user that ran it had full administrative rights.

### Overview

Least privilege is the concept of restricting access rights to only those rights needed to perform a specific task or job role. You can apply this principle to:

* User accounts.
* Service accounts.
* Computing processes.

Although this principle is easy to understand, it can be complex to implement. As a result, in many cases, least privilege isn't adhered to.

The principle states that all users should sign in with a user account that has the minimum permissions necessary to complete the current task and nothing more. This principle provides protection against malicious code, among other attacks. It applies to computers and the users of those computers.

The problem, of course, is that administrators typically don't want to sign in with a standard user account for their day\-to\-day tasks, and then sign out and back in as an administrator when they need to reset a user's password. It's time\-consuming and it's a hassle. To solve this problem, you must find a way to identify the typical security risks. You must then plan a less intrusive principle of least privilege.

### Identify security principals

In an on\-premises environment, you should determine which security principals (users and groups) belong to administrative groups. In Active Directory Domain Services (AD DS), there are several sensitive administrative groups. These are described in the following table.

| Group | Description |
| --- | --- |
| Enterprise Admins | This universal security group resides in the Users folder of the AD DS forest root domain. Members can perform any administrative task anywhere in the forest. There are few management tasks that require Enterprise Admins membership. By default, only the Administrator user account from the forest root domain belongs to Enterprise Admins. |
| Domain Admins | This global security group resides in the Users folder of every domain in your AD DS forest. Members can perform any administrative task anywhere in the local domain. By default, only the Administrator user account from the local domain belongs to Domain Admins. |
| Schema Admins | This universal security group resides in the Users folder of the forest root domain. Members can modify the properties of the AD DS schema. Schema changes are infrequent, but significant in their effect. By default, only the Administrator user account from the forest root domain belongs to Schema Admins. |
| Administrators | This domain local security group resides in the Builtin folder in AD DS. The Administrators local group also exists in all computers in your AD DS forest. Administrators have complete and unrestricted access to the domain (or computer). Typically, the Enterprise Admins and Domain Admins groups are added to the Administrators groups on all computers in your forest. |

Note

The AD DS schema is a collection of objects and their properties, sometimes also called classes, and attributes.

Other built\-in groups that have security privileges include:

* Account Operators.
* Server Operators.
* Key Admins.
* Enterprise Key Admins.

### Modify group memberships

After you've determined which users and groups belong to administrative groups, you can make any necessary changes. You can use Group Policy Objects (GPOs) in an AD DS environment to expedite this process. Use the **Restricted Groups** feature to control the membership of groups on all computers affected by the GPO. Use the following procedure:

1. Open **Group Policy Management**, and then create and link a GPO to the domain object.
2. Open the GPO for editing.
3. Locate **Computer Configuration**, **Policies**, **Windows Settings**, **Security Settings**, **Restricted Groups**.
4. Right\-click or activate the context menu for **Restricted Groups** and select **Add Group**.
5. In the **Add Group** dialog box, add the required group.
6. Add the members to the group or add the group to another group as a member.
7. Select **OK** to complete the process.

### Determine currently assigned rights

After you've modified the security principals in your environment, you must determine what rights those principals already have. Clearly, if a user belongs to a sensitive administrative group, such as Administrators, that user can perform any task and exercise any right on the computer or domain where the group exists.

Note

A right is the ability to perform an administrative task. A permission is the ability to access an object in the file system, in AD DS, or elsewhere.

However, a user might belong to other groups that have been assigned rights or privileges. It might also be the case that a user is directly assigned a right.

You can use the **Local Security Policy** console to determine what rights are assigned. Use the following procedure:

1. Select **Start**, and then select **Windows Administrative Tools**.
2. Select **Local Security Policy**.
3. In **Local Security Policy**, expand **Local Policies**, and then expand **User Rights Assignment**.
4. Review, and if necessary, edit the **Security Setting** value for each **Policy** listed.

Tip

Always assign a policy to a group, and not directly to a user. This helps with ongoing management. When someone's job role changes, you need only change their group memberships rather than revisit all the user rights assignments you assigned to their user account.

### Implement User Account Control

User Account Control (UAC) is a security feature that provides a way for users to limit the status of their administrative account to that of a standard user account. However, when the user wants to perform a task that requires administrative capability, referred to as *elevation*, the user is prompted to confirm that elevation. By default, UAC prompts the user when they attempt elevation, as follows:

* If the user is an administrator, they're prompted to confirm the elevation.
* If the user is a standard user, they're prompted for administrative credentials.

You can control UAC prompts and behavior by using GPOs.

1. Open an appropriately linked GPO for editing, and navigate to **Computer Configuration**, **Policies**, **Windows Settings**, **Security Settings**, **Local Policies**, **Security Options**.
2. For administrative accounts, open the **User Account Control: Behavior of the elevation prompt for administrators in Admin Approval Mode** setting, select **Define this policy setting**, and then select the required setting.
3. For standard users, open the **User Account Control: Behavior of the elevation prompt for standard users** setting, select **Define this policy setting**, and then select the required setting.

### Implement Just Enough Administration

Just Enough Administration (JEA) is an administrative technology that allows you to apply role\-based access control (RBAC) principles through Windows PowerShell remote sessions. Instead of allowing users general roles that often allow them to perform tasks that aren't directly related to their work requirements, JEA enables you to configure special Windows PowerShell endpoints that provide the functionality necessary to perform a specific task.

JEA allows you to lock down administrative sessions so that only a specific set of tasks can be performed through a remote Windows PowerShell session. JEA increases security by limiting the tasks that can be performed. You configure JEA by creating and modifying role\-capability files and session\-configuration files.

Important

JEA only supports Windows PowerShell remoting.

### Quick review

---

## Implement delegated privileges

You study the report produced for Contoso by a firm of IT security specialists. You realize that user accounts that are members of high\-privilege groups, such as Enterprise Admins and Domain Admins, have full access to all systems and data. You recognize that those accounts must be closely guarded.

However, there are users that require certain admin rights to perform their duties. For example, help desk staff must be able to reset passwords and unlock accounts for ordinary users, while some IT staff will be responsible for installing applications on clients or servers, or performing backups.

Although Active Directory and member servers have built\-in groups that have predetermined privileges assigned, such as Backup Operators and Account Operators, these might not fit your needs. You now need to determine how best to provide this limited administrative access.

### Use the Delegation of Control Wizard

Delegated privilege provides a way to grant limited authority to specified users or groups. You can delegate more granular privileges to users or groups by using the **Delegation of Control Wizard**. The wizard allows you to assign permissions at the site, domain, or organization unit level. The wizard has the following predefined tasks that you can assign:

* Create, delete, and manage user accounts.
* Reset user passwords and force password change at next sign in.
* Read all user information.
* Create, delete, and manage groups.
* Modify the membership of a group.
* Join a computer to the domain (only available at the domain level).
* Manage Group Policy links.
* Generate Resultant Set of Policy (Planning).
* Generate Resultant Set of Policy (Logging).
* Create, delete, and manage inetOrgPerson accounts.
* Reset inetOrgPerson passwords and force password change at next sign in.
* Read all inetOrgPerson information.

You can also combine permissions to create and assign custom tasks.

To launch the **Delegation of Control Wizard**, open Active Directory Users and Computers and locate the organizational unit (OU) that you want to delegate control over.

Note

You can also delegate control on the domain object.

Tip

To delegate control over a site, use the Active Directory Sites and Services tool to delegate control.

Then use the following procedure:

1. Right\-click or activate the context menu to OU and select **Delegate Control**, and then select **Next**.
2. In the **Delegation of Control Wizard**, select the user or group to which you want to delegate control and then select **Next**.

Tip

You should avoid assigning rights to specific users. Instead, you should use groups, even if the group contains only one user. This makes ongoing administration easier.
3. On the **Tasks to Delegate** page, select from a list of common tasks, or else select a custom task to delegate. For example, to delegate the ability to manage user accounts, select the following:

	* Create, delete, and manage user accounts.
	* Reset user passwords and force password changes at next logon.
	* Read all user information.
4. Select **Finish**.

Important

After you have assigned delegated access, you can't use the **Delegation of Control Wizard** to review your settings.

To review previously configured delegated tasks:

1. In **Active Directory Users and Computers**, on the menu, select **View**, and then select **Advanced Features**.
2. Locate the OU that you delegated. Right\-click or activate the context menu and select **Properties**.
3. In the ***OU name* Properties** dialog box, select the **Security** tab, and then select **Advanced**.
4. Locate the security principal to which you delegated control and review the permissions. You can also change the delegated permissions here.

Note

The **Delegation of Control Wizard** provides a simple, wizard\-driven interface for the configuration of AD DS permissions on AD DS objects.

### Demonstration

The following video demonstrates how to use the **Delegation of Control Wizard** to implement delegated privileges. The main steps in the process are:

1. Open **Active Directory Users and Computers**.
2. Create a new group called **Sales Managers** in the **Managers** OU.
3. Add a user to the **Sales Managers** group.
4. Run the **Delegation of Control Wizard**, targeting the **Sales** OU.
5. Assign the **Sales Managers** group the **Reset user passwords and force password change at next logon** permission on the **Sales** OU.
6. Sign in as a member of the **Sales Managers** group and verify that the user can reset a password for users in the **Sales** OU but not in the **Research** OU.

### Quick review

---

## Use privileged access workstations

When reviewing the security report produced by consultants for Contoso, you learned that malicious hackers focus on workstations that are regularly used by administrators with high\-level access to the infrastructure. Therefore, it's important to ensure that such workstations are secure.

### What is a privileged access workstation?

A privileged access workstation (PAW) is a computer that you can use for performing administration tasks, such as the administration of identity systems, cloud services, and other sensitive functions. This computer is protected from the internet and locked down so that only the required administration apps can run.

Caution

Ensure that administrative user accounts aren't used as standard user accounts.

You should never use this workstation for web browsing, email, and other common end\-user apps, and it should have strict application control. You shouldn't allow connection to wireless networks or to external USB devices. A PAW should implement security features such as multifactor authentication (MFA).

Tip

You must configure privileged servers to not accept connections from a nonprivileged workstation.

Microsoft recommends using Windows 11 Enterprise for your PAWs. This is because Windows 11 Enterprise supports security features that aren't available in other editions. These Windows Defender features are described in the following table.

| Feature | Description |
| --- | --- |
| Windows Defender Application Control | Moves away from the traditional application trust model where all applications are assumed trustworthy by default to one where applications must earn trust to run. |
| Windows Defender Credential Guard | Protects NTLM password hashes, Kerberos ticket\-granting tickets, and credentials stored by applications as domain credentials. Because they're no longer stored in the local security authority (LSA), credential theft can be blocked even on a compromised system. |
| Windows Defender Device Guard | Combines the features of Windows Application Control with the ability to use the Windows Hyper\-V hypervisor to protect Windows kernel\-mode processes against the injection and execution of malicious or unverified code. |
| Windows Defender Exploit Guard | Enables administrators to define and manage policies for reducing surface attacks and exploits, network protection, and protecting suspicious apps from accessing folders commonly targeted. |

### PAW hardware profiles

It's important to remember that administrators are also users. This means that they use email, browse the web, and run productivity apps like Microsoft Office. A correctly configured PAW severely impacts the user's ability to be productive in nonadministrative tasks.

Caution

It's worth remembering that users tend to abandon secure solutions that limit productivity in favor of insecure solutions that enhance productivity.

To maintain security, administrator users should be provided with two workstations. One workstation is a PAW, while the other is used for day\-to\-day tasks that don't require elevation. You can achieve this separation by using PAW hardware profiles. Microsoft recommends using one of the following hardware profiles:

* Dedicated hardware. Separate dedicated devices for user tasks versus administrative tasks. The admin workstation must support hardware security mechanisms such as a trusted platform module (TPM) and implement the Windows 10 Enterprise security features already discussed.
* Simultaneous use. A single device that can run user tasks and administrative tasks concurrently by running two operating systems, where one is a user system and the other is an administrator system. You can do this by running a separate operating system in a VM for daily use.

Caution

If you're using a single device, ensure that the PAW runs on the physical computer, while your regular workstation is running as a VM. This provides the correct security.

The following table describes the advantages and disadvantages of these approaches.

| Scenario | Advantages | Disadvantages |
| --- | --- | --- |
| Dedicated hardware | Strong security separation | Requires two devices. This requires more space and costs more to implement. |
| Simultaneous use | Reduced hardware costs | Sharing the same keyboard and mouse can result in errors and pose security risks. |

### Quick review

---

## Use jump servers

The security report produced for Contoso recommends implementing *jump servers* in addition to using PAWs. Having determined how to use PAWs, you decide to investigate jump servers further to figure out how they could benefit Contoso IT.

### What are jump servers?

A jump server is a hardened server used to access and manage devices in a different security zone, such as between an internal network and a perimeter network. The jump server can function as the single point of contact and management.

For medium\-sized organizations, jump servers can provide a means to help enhance security in locations where physical security is more challenging. For example, in branch offices where there's no datacenter. For large organizations, administrators can deploy datacenter\-housed jump servers; these jump servers can provide highly controlled access to servers and domain controllers.

Jump servers don't typically have any sensitive data, but user credentials are stored in the memory and malicious hackers can target those credentials. For that reason, jump servers must be hardened.

Tip

You typically use a PAW to access a jump server to help to ensure secure access.

This server runs on dedicated hardware that supports both hardware and software\-based security features such as:

* Windows Defender Credential Guard, to encrypt the domain credentials in memory.
* Windows Defender Remote Credential Guard, to prevent remote credentials from being sent to the jump server, instead using Kerberos version 5 single sign\-on tickets.
* Windows Defender Device Guard:
	+ Using Hypervisor Enforced Code Integrity (HVCI) to use virtualization\-based security to enforce kernel mode components to follow with the code integrity policy.
	+ Using Config Code Integrity to allow administrators to create a custom code integrity policy and specify trusted software.

By using jump servers, either with or without PAWs, you can create logical security zones. Within a zone, computers have similar security and connectivity configurations. You can use GPOs to configure these settings within a domain environment.

Tip

Administrative users can connect to your jump servers using Remote Desktop Protocol (RDP) and smart cards to perform administrative tasks.

### Implement jump servers

The following graphic depicts a typical jump server and PAW deployment. An administrative user uses a smart card to authenticate to a standard workstation using a standard account. The user can access standard apps to perform day\-to\-day office productivity tasks. The administrator also has an administrative account and uses a smart card to authenticate to their administrative PAW. This in turn connects to the configured administrative jump server, which has administrative access to the appropriate object.

There are several important considerations when implementing jump servers including:

* Remote Desktop Gateway. If an administrator must connect directly to a target server (using RDP), implement Remote Desktop Gateway. This enables you to implement restrictions on connections to the jump server, and to destination servers that it will be used to manage.
* Hyper\-V. Consider implementing VMs for each administrator on your jump servers. Each VM can be configured to allow a specific or subset of administrative tasks. Therefore, you should install Hyper\-V on your jump servers.

Tip

You can enforce shutdown of these VMs after administrative tasks are completed. By shutting down VMs when not in use, you reduce your attack surface.

* Server features. To implement jump servers, your server computers must support the following features:

	+ UEFI secure boot.
	+ Virtualization support.
	+ Signed Kernel mode drivers.
* Remote administration tools. You should always use remote administration tools to manage servers. Install Windows Admin Center and the Remote Server Administration Tools (RSAT) on your administrator's VMs (or the physical jump server if you don't implement Hyper\-V).

Caution

You should also prevent the use of remote administration tools on general\-purpose computers.
* RDP connectivity. Ensure that administrators connect using RDP to their VMs when they perform administrative tasks.

---

## Summary

As a Windows Server administrator at Contoso, you're responsible for managing and maintaining the on\-premises server infrastructure. Your first task was to determine how best to administer Windows Server using the principle of least privilege.

In this module, you learned which user accounts to use when performing administrative tasks, and how to perform Windows Server administration securely. You can now apply the principle of least privilege and identify built\-in privileged accounts. You also understand when to use privileged access workstations.

### Learn more

You can learn more by reviewing the following documents:

* [Just Enough Administration](/en-us/powershell/scripting/learn/remoting/jea/overview?azure-portal=true)
* [Implementing Least\-Privilege Administrative Models](/en-us/windows-server/identity/ad-ds/plan/security-best-practices/implementing-least-privilege-administrative-models?azure-portal=true)
* [Active Directory Security Groups](/en-us/windows/security/identity-protection/access-control/active-directory-security-groups?azure-portal=true)
* [Implementing Secure Administrative Hosts](/en-us/windows-server/identity/ad-ds/plan/security-best-practices/implementing-secure-administrative-hosts?azure-portal=true)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/perform-windows-server-secure-administration/_

## Fuentes
- [Perform Windows Server secure administration](https://learn.microsoft.com/en-us/training/modules/perform-windows-server-secure-administration/?WT.mc_id=api_CatalogApi)
