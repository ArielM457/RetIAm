# Just Enough Administration in Windows Server

> Curso: Manage Windows Servers and workloads in a hybrid environment (wwl-manage-windows-servers-workloads-hybrid-enviro) · Seccion: Manage Windows Servers and workloads in a hybrid environment
> Duracion estimada: 44 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Just Enough Administration (JEA) is an administrative technology that allows you to apply role\-based access control (RBAC) and the least privilege principles to Windows PowerShell remote sessions. Instead of assigning users broad roles that enable them to perform tasks that aren't directly related to a specific work requirement, JEA allows you to configure special Windows PowerShell endpoints that provide only the functionality necessary to perform a specific task.

### Learning objectives

After completing this module, you'll be able to:

* Describe JEA.
* Explain the limitations of JEA.
* Describe role capabilities files and their use in JEA.
* Describe sessions configuration files and their use in JEA.
* Register JEA endpoints.
* Connect to JEA endpoints.

### Prerequisites

To get the best learning experience from this module, you should have:

* Familiarity with PowerShell commands and syntax
* Experience using PowerShell to administer Windows Server
* Ability to create and edit PowerShell scripts
* Ability to enable remote management and connect to a remote system

---

## Define role capabilities for a JEA endpoint

Role capability files help you specify what can be done in a Windows PowerShell session. Anything that's not explicitly allowed in a role capability file or a session configuration file isn't allowed.

You can create a new, blank, role capability file by using the **New\-PSRoleCapabilityFile** cmdlet. (Role capability files use the.psrc extension.) You then edit the role capability file, adding cmdlets, functions, and external commands as necessary. You can allow entire Windows PowerShell cmdlets or functions, or you can list which parameters and parameter values can be used.

When you create a role capability file, you can define the following limitations for the Windows PowerShell session:

* VisibleAliases. This setting lists which aliases to make available in the JEA (Just Enough Administration) session.
* VisibleCmdlets. This setting lists which Windows PowerShell cmdlets are available in the session. You can choose either to list cmdlets, allowing all parameters and parameter values to be used, or limit cmdlets to particular parameters and parameter values.
* VisibleFunctions. This setting lists which Windows PowerShell functions are available in the session. Again, you can choose to list functions, allowing all parameters and parameter values to be used, or you can limit functions to particular parameters and parameter values.
* VisibleExternalCommands. This setting allows users who are connected to the session to run external commands. For example, you can use this field to allow access to c:\\windows\\system32\\ whoami.exe so that users connected to the JEA session can identify their security context.
* VisibleProviders. This setting lists Windows PowerShell providers that are visible to the session.

You can also configure other settings such as which modules to import, which assemblies are loaded, and data types that are available. For a list of all the options when creating a role capabilities file, see [New\-PSRoleCapabilityFile](/en-us/powershell/module/microsoft.powershell.core/new-psrolecapabilityfile).

### Which commands should you allow?

It's important to properly configure your role capability files. If you give users too few tools, they can't get their work done. If you give them too many tools, then you increase the attack surface of the Windows PowerShell session.

Using the following process can help you decide how to configure your role capabilities files:

1. Working with your IT team, survey your current tools and processes to identify which commands are needed.
2. Whenever possible, move away from command\-line tools to PowerShell cmdlets.
3. Restrict which cmdlet parameters and values can be used to only those that are necessary to complete specific tasks.
4. Prevent the use of commands that let users elevate their permissions or that allows them to run arbitrary code.
5. Create custom functions with validation logic to replace complex commands.
6. Test and monitor the list of allowed commands over time and modify as needed.

---

## Create a session configuration file to register a JEA endpoint

Session configuration files are used to register a JEA (Just Enough Administration) endpoint. The session configuration file is responsible for naming the JEA endpoint. It also controls:

* Who can access the JEA endpoint
* What roles the user is assigned
* Which identity is used by JEA's virtual account.

Session configuration files use the .pssc file extension, and you create new session configuration files by using the **New\-PSSessionConfigurationFile** cmdlet.

You can also use session configuration files to define which cmdlets and functions are available in a JEA session, just like you can with role capabilities files. In addition, you can configure the following settings unique to session configure files:

* SessionType. This setting allows you to configure the sessions default settings. The SessionType of RestrictedRemoteServer is used for sessions used by JEA for secure management.
* RoleDefinitions. This setting is used to assign role capabilities to specific security groups.
* RunAsVirtualAccount. This setting allows JEA to use the privileged virtual account created just for the JEA session. This account is a member of the local Administrators group and the Domain Admins group on domain controllers.
* TranscriptDirectory. This setting specifies where JEA activity transcripts are stored.
* RunAsVirtualAccountGroup. This setting allows you to specify the groups that the virtual account is a member of, instead of the default Administrators or Domain Admins groups.

For a list of all the options when creating session configuration files, see [New\-PSSessionConfigurationFile](/en-us/powershell/module/microsoft.powershell.core/new-pssessionconfigurationfile).

---

## Describe how JEA endpoints work to limit access to a PowerShell session

A JEA (Just Enough Administration) endpoint is a Windows PowerShell endpoint that is configured so only specific authenticated users can connect to it. Once connected, those users only have access predefined sets of Windows PowerShell cmdlets, parameters, and values, based on security group and role capability definitions.

Servers can have multiple JEA endpoints. Each JEA endpoint should be configured so it's used for a specific administrative task. For example, you might have a Domain Name System Operations (DNSOps) endpoint to perform DNS administrative tasks, and a DHCPOps endpoint to perform Dynamic Host Configuration Protocol (DHCP) administrative tasks.

With the JEA endpoints, your IT staff doesn't need to have privileged accounts that are members of groups such as the local Administrators group, to connect to an endpoint. Instead, users have the privileges assigned to the virtual account, which is configured in the session configuration file and could include the privileges of a local administrator or Domain Admin.

### Registering JEA on a single machine

On a single computer, you can create JEA endpoints by using the **Register\-PSSessionConfiguration** cmdlet. When using this cmdlet, you specify an endpoint name and a session configuration file located on the local machine. However, prior to creating the JEA endpoint you must ensure that the following prerequisites are met:

You must have defined one or more roles, and the role capabilities file (or files) must be placed in the RoleCapabilities folder of a Windows PowerShell module.

* You have created a session configuration file.
* The user registering JEA must be an administrator on the machine.
* You have decided on a name for the JEA endpoint

Windows Server ships with some predefined JEA endpoints, which have a name starting with Microsoft. You can find existing JEA endpoints using the following Windows PowerShell command:

```
Get-PSSessionConfiguration | Select-Object Name

```

For example, to register the endpoint DNSOps using the DNSOps.pssc session configuration file, use the following command:

```
Register-PSSessionConfiguration -Name DNSOps -Path .\DNSOps.pssc

```

### Registering JEA on multiple machines

You can register JEA on multiple machines by using Desired State Configuration (DSC). To use DSC to deploy JEA, the following prerequisites must be met:

* You must have defined one or more roles, and the role capabilities file (or files) must be placed in the RoleCapabilities folder of a Windows PowerShell module.
* The PowerShell module must be stored on a read\-only file share accessible by the machines.
* You have determined the session configuration settings. (You don't need to create a session configuration file though.)
* You have account credentials that have administrative access to each machine.
* You have downloaded the JEA DSC resource from [https://github.com/PowerShell/JEA/tree/master/DSC Resource](https://github.com/PowerShell/JEA/tree/master/DSC%20Resource)
* You have decided on a name for the JEA endpoint

You can apply the DSC configuration using the Local Configuration Manager or by updating the pull server configuration.

For more information about Registering JEA on multiple machines, see the GitHub page [JEA/DSC Resource/](/en-us/powershell/scripting/learn/remoting/jea/register-jea?view=powershell-7.1&preserve-view=true).

### Check your knowledge

Choose the best response for each of the questions below.

### Check your knowledge

---

## Create and connect to a JEA endpoint

You connect to a JEA endpoint by connecting interactively, using implicit remoting, programmatically, or through PowerShell Direct.

### Interactive JEA connections

You can use JEA the same way you would connect with a regular PowerShell remoting session. To use JEA interactively, you need:

* The remote computer name
* The JEA endpoint name
* An account with access to the desired endpoint

For example, if you have access to the JEA endpoint named DNSOps on the local server, you can connect to the JEA endpoint using the following PowerShell command:

```
Enter-PSSession -<ComputerName> localhost -ConfigurationName DNSOps

```

After you're connected, your command prompt will change to `[localhost]: PS`\>. If you're not sure what commands are available, you can use the **Get\-Command** cmdlet to review which ones are available.

One limitation of interactive JEA sessions is that they operate in **NoLanguage** mode. This means you cant use variables to store data. For example, the following commands to start a virtual machine won't work because of the user of variables:

```
$myvm = Get-VM -Name MyVM
Start-VM -vm $myvm

```

However, you can use piping to direct output of one command to another. This means that the following command would be the equivalent of the previous commands:

```
Get-VM -Name MyVM | Start-VM

```

### Implicit remoting and JEA

Implicit remoting lets you import proxy versions of cmdlets from a remote machine to your local Windows PowerShell environment. This lets you use Windows PowerShell features such as tab completion, variables, or even local scripts.

You can even prefix PowerShell commands with a unique string so you can differentiate between the remote commands and local ones. For example, you could use the following commands to import the DNSOps JEA session and prefix the commands with DNSOps:

```
$DNSOpssession = New-PSSession -ComputerName 'MyServer' -ConfigurationName 'DNSOps'
Import-PSSession -Session $DNSOpssession -Prefix 'DNSOps' Get-DNSOpsCommand

```

### Programmatic access to JEA

You can connect to JEA endpoints programmatically the same way you connect to other PowerShell endpoints programmatically. Programmatic access to JEA is often used in in\-house helpdesk apps and websites and uses the same approach as apps built to interact with unconstrained PowerShell endpoints.

For more information about connecting to JEA endpoints programmatically, see [Using JEA programmatically](/en-us/powershell/scripting/learn/remoting/jea/using-jea#using-jea-programmatically).

### JEA and PowerShell Direct

PowerShell Direct allows Hyper\-V administrators to connect to VMs from the Hyper\-V host. By doing this, they can ignore any network or remote management settings on the VM.

The Hyper\-V administrator connects to the VM the same way they would connect to any other server using PSRemoting, only specifying the \-VMName parameter or the \-VMId parameter. Whenever using JEA to manage VMs, you should create a dedicated JEA user account for the Hyper\-V administrator, and the accounts ability to sign\-in locally to the VM.

---

## Demonstration: Connect to a JEA endpoint

Watch this video to learn more about how to create a JEA endpoint and connect to it.

  

The video explains how to:

* Create a role capability file around DNS operations
* Create a session configuration file that allows members of a specific Active Directory group to use the privileges granted in the role capability file using a virtual account
* Testing that that JEA functions as expected by connecting using an unprivileged account to the JEA endpoint

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/just-enough-administration-windows-server/_

## Fuentes
- [Just Enough Administration in Windows Server](https://learn.microsoft.com/en-us/training/modules/just-enough-administration-windows-server/?WT.mc_id=api_CatalogApi)
