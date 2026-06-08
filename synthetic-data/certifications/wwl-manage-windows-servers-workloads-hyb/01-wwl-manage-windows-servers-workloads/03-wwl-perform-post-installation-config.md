# Perform post-installation configuration of Windows Server

> Curso: Manage Windows Servers and workloads in a hybrid environment (wwl-manage-windows-servers-workloads-hybrid-enviro) · Seccion: Manage Windows Servers and workloads in a hybrid environment
> Duracion estimada: 46 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Learn to perform post\-installation configuration of Windows Server by using several methods and tools.

### Scenario

Contoso, Ltd. is a financial services company in Seattle with major offices located throughout the world. Most of its compute environment runs on\-premises on Windows Server. This includes virtualized workloads on Windows Server 2016 hosts.

Contoso IT staff are migrating Contoso on\-premises servers to Windows Server 2022\. As a Windows Server administrator, you are responsible for managing and maintaining the server infrastructure that will help Contoso achieve its business goals. After you deploy the first Windows Server 2022 server computer, you must complete the configuration. You know that there are several tools available to complete this post\-installation configuration, but you must learn how best to use them.

After completing this module, you’ll be able to select the appropriate post\-installation configuration tool and use it to complete the configuration of your Windows Server computers.

### Learning objectives

After completing this module, you'll be able to:

* Explain post\-installation configuration and describe the available post\-installation configuration tools.
* Use Sconfig to configure Windows Server.
* Describe Desired State Configuration (DSC) and explain how to use it to configure Windows Server.
* Use Windows Admin Center to perform post\-installation configuration.
* Implement answer files to complete the configuration.

### Prerequisites

To get the best learning experience from this module, you should have knowledge and experience of:

* Windows Server.
* Working with command\-line tools.

---

## List the available post\-installation configuration tools

Contoso is in the process of deploying Windows Server server computers throughout their organization. As a Windows Server administrator, it's your task to perform post\-installation configuration on the newly deployed servers. You decide to investigate the available post\-configuration options.

### What must you configure?

When you install Windows Server using the defaults from the local installation media, a number of settings are configured automatically, as described in the following table.

| Setting | Description |
| --- | --- |
| Computer name | The computer name is automatically generated. You'll need to change the name to something meaningful, and unique, within your organization. |
| Workgroup | The server is added to a workgroup called WORKGROUP. Typically, you'll want your server computers to be part of your Active Directory Domain Services (AD DS) domain. |
| Network settings | By default, both IPv4 and IPv6 are enabled and bound to the installed network interface cards (NICs). In the case of IPv4, a Dynamic Host Configuration Protocol (DHCP) configuration is assigned. For IPv6, stateless autoconfiguration is enabled. Both these defaults are probably suitable. |
| Time zone | The time zone defaults to the (UTC\-08:00\) Pacific Time (US \& Canada) unless your installation media was based on a different locale. You'll need to change the time zone, and the computer's time and date, to those which are appropriate for your location. |
| Locale and language settings | The initial values are specified during an interactive installation, or are implied by the installation media locale. You'll need to update these settings to those which are appropriate for the server's physical location. |
| Roles and features | Very few roles or features are enabled by default in a standard installation. Typically, the Storage Services role service, and a number of features are enabled. These features include: elements of .NET Framework, Windows Defender Antivirus, and some elements of Windows PowerShell, including Windows PowerShell 5\.1 and Windows PowerShell ISE. |
| Firewall settings | The Windows Defender Firewall is enabled by default. Until you define them as otherwise, all NICs are assigned to the Public network location profile \- which is generally more restrictive that Private network connections. |
| Activation | Typically, the server will not be activated. |

After you have installed the server, you'll need to reconfigure some of these settings.

### Overview of available post\-installation configuration tools

You can choose from a number of available tools. The tool you choose to use depends on circumstances. For example, if you deployed Windows Server Core, because there is no graphical user interface installed, you'll need to rely on remote tools, for the most part, to reconfigure the server.

#### Server Manager

If the computer is installed with Windows Server with Desktop Experience, then you can use Server Manager to configure the required settings. Sign in as local administrator, and if necessary, open Server Manager. Select **Local Server** in the navigation pane, and then you can change the required settings.

Important

If you change the computer name or you add the computer to a domain, you'll need to restart the server for the setting to take effect.

Tip

To add a computer to a domain, the server will need to contact a domain controller. So, you'll have to configure the DNS name resolution settings before you attempt the domain\-join.

#### Windows Admin Center

You can use Windows Admin Center to perform post\-installation configuration for both Windows Server with Desktop Experience and Server Core installations.

Note

You'll only be able to connect to a server if you can resolve its name into an IP address, and if the IP address is accessible. Typically, a newly deployed computer uses DHCP to obtain an IP configuration, and so should be configured with an appropriate IP address and DNS client settings.

Download and install Windows Admin Center. Then, open Microsoft Edge, and navigate to the Windows Admin Center website.

Note

To connect to a server, you'll need to know it's name and the local administrator account credentials.

Add the server as a connection, and then select the server from the list of servers. Use the navigation pane to select the appropriate tool with which to make configuration changes. We'll discuss Windows Admin Center in more detail later in this module.

Note

Windows Admin Center is not included in Windows Server. You must download and install it.

#### Desired state configuration

You can use DSC to reconfigure your Windows Server. DSC is a management platform that leverages Windows PowerShell, enabling you to manage your IT infrastructure. As PowerShell Desired State Configuration is included with Windows Server, you don't need to install anything before you can use it. However, you'll need to be comfortable with Windows PowerShell, PowerShell scripts, and PowerShell remoting. We'll discuss DSC in more detail later in this module.

#### Answer files

You can use answer files to complete the installation process. Typically, these are used to help to automate the entire installation process, including post\-installation settings.

You can create answer files by downloading the Windows Assessment and Deployment Kit (Windows ADK). Then, using the Windows System Image Manager (Windows SIM) you can create and configure the required answer file. The final step is to distribute the answer file to your servers, often on removable media.

Note

The answer file is an .xml text file.

We'll discuss how to implement server configuration with answer files in more detail later in this module.

---

## Configure Server Core using Sconfig

Most of the Windows Server computers being deployed at Contoso are Server Core. Server Core has no GUI, so after the initial installation, you're presented with only a command prompt.

### What is Sconfig?

Sconfig is a text\-based tool that allows you to do the basic configuration of Server Core to prepare it for use in your production environment.

Note

Sconfig is included in both Windows Server Desktop Experience and Server Core.

You typically use Sconfig to perform the initial configuration directly after the installation completes, but you can run it at any time to change the settings as required.

Sconfig provides several options, which are described in the following table.

| Option | Description |
| --- | --- |
| Domain/Workgroup | Join the domain or workgroup of choice |
| Computer Name | Set the computer name |
| Add Local Administrator | Add users to the local Administrators group |
| Configure Remote Management | Remote management is enabled by default. This setting allows you to enable or disable remote management and configure the server to respond to a ping. |
| Windows Update Settings | Configure the server to use automatic, download only or manual updates. |
| Download and Install Updates | Perform an immediate search for all updates or only recommended updates. |
| Network Settings | Configure the IP address to be assigned automatically by a Dynamic Host Configuration Protocol (DHCP) Server or you can assign a static IP address manually. This option also allows you to configure Domain Name System (DNS) Server settings for the server. |
| Date and Time | Brings up the GUI for changing the date, time, and time zone. It also has tabs to add clocks and choose an Internet time server to sync with. |
| Telemetry Settings | Allows Windows to periodically collect and upload statistical information about the server and upload it to Microsoft. |
| Windows Activation | Provides three options—Display license info, Activate Windows, and Install product key |
| Log Off User | Signs out the current user |
| Restart Server | Restarts the server |
| Shut Down Server | Shuts down the server |
| Exit to Command Line | Returns to the command prompt |
| Remote Desktop | Enable Remote Desktop |

### Demonstration

The following video demonstrates how to implement complete post\-installation configuration by using Sconfig. The main steps in the process are:

1. Run the Sconfig.exe command.
2. Review the available options.
3. Reconfigure the date and time.
4. Review the network settings.

---

---

### Quick review

---

## Configure a server with answer files

You decide to automate the post\-installation configuration for Windows Server servers being deployed in Contoso. You can use Windows SIM to create answer files that contain the settings you need to complete the configuration of Contoso's Windows Server servers.

### What are answer files?

Answer files are .xml text files that contain settings that enable you to customize and automate the deployment process of Windows. Although you can use a text editor to create and edit your .xml files, this can be challenging. So, it's usually easier to download and install the [Windows Assessment and Deployment Kit](/en-us/windows-hardware/get-started/adk-install?azure-portal=true), and then use the Windows SIM tool to create and edit your unattend answer files.

Answer files are organized into two sections, as described in the following table.

| Section | Description |
| --- | --- |
| Components | Contains all the component settings that your answer file applies during setup. This section is further divided into configuration passes, each of which represents a different setup phase. These phases are: windowsPE, offlineServicing, generalize, specialize, auditSystem, auditUser, and oobeSystem. |
| Packages | Defines the packages that are used to distribute updates and language packs. You use this section to enable or disable selected Windows features. |

Tip

When you create your answer file, you can specify to which setup phase to add your settings.

The following graphic displays the default console for an untitled answer file project in Windows SIM.

Important

Most settings that are relevant to post\-installation configuration reside in the **specialize** installation phase.

### Create and distribute answer files

The first step in creating answer files is to download the Windows ADK and perform a custom installation. When prompted, choose the **Deployment Tools** option (which includes Deployment Image Servicing and Management (DISM) tools, Windows SIM, and related components).

Then, use the following procedure:

1. Open **Windows SIM**. From the menu, select **File** and then select **New Answer File**.
2. In the **Windows System Image Manager** dialog box, select **Yes** when prompted to open a new Windows image now.
3. Browse and locate an image file.

Tip

You can use the **install.wim** image file from the Windows Server product DVD (located in the \\sources folder). Alternatively, you can use a custom image which you have previously created and generalized.
4. Next, if prompted in the **Select an Image** dialog box, choose the image you want to install and select **OK**.
5. In the **Windows System Image Manager** dialog box, select **Yes** to create a catalog file. This file is required.

Note

It takes around five minutes to create the catalog file.

After the catalog file is created, you can begin to configure the answer file. The basic process is as follows:

1. For each element you want to include in the answer file, in the Windows Image pane, locate the element (either in **Components** or **Packages**), right\-click or activate the context menu for the element, and then select **Add to Answer File**. This procedure adds the required setting(s) to the answer file pane, from where you can configure that setting to the required value using the **Properties** pane.
2. When all required items are added to the answer file, you should use the **Properties** pane to configure the desired values.
3. Next, you should verify the answer file. On the menu, select **Tools**, and then select **Validate Answer File**. Any problems are displayed in the Messages pane.
4. Then save the file. Select **File**, and then select **Save Answer File**.
5. Select an appropriate location, and then select **Save**.

Tip

You can save the file with any name, and you can place it in a number of locations. However, if you save the file as **Autounattend.xml** in the root of a removable storage device, setup can find the file without further configuration.

#### Typical settings to include

Although there are many settings you can configure in an answer file, only a subset of these deal with post\-installation configuration.

In the **Components** node, some of the more common settings are:

* **Microsoft\-Windows\-TCPIP**. Configures the TCP/IP networking settings.
* **Microsoft\-Windows\-DNS\-Client**. Contains settings for name resolution using DNS.
* **Microsoft\-Windows\-UnattendedJoin**. Enables you to add a computer to an AD DS domain.
* **Microsoft\-Windows\-Shell\-Setup**. Provides access to a number of settings, including computer name.

In the **Packages** node, add the **Product** settings to the answer file.

The end result is a simple text file that contains the XML syntax required to customize your Windows Server installation.

---

## Summary

Contoso IT staff are migrating Contoso on\-premises servers to Windows Server 2019\. As a Windows Server administrator, you are responsible for managing and maintaining the server infrastructure that will help Contoso achieve its business goals.

You deployed the first Windows Server 2019 server computer. Next, you identified available post\-installation configuration tools and completed the server configuration. You've learned how to select the appropriate post\-installation configuration tool and use it to complete the configuration of your Windows Server computers.

### Learn more

You can learn more by reviewing the following documents.

* [Get started with Desired State Configuration (DSC) for Windows](/en-us/powershell/scripting/dsc/getting-started/wingettingstarted?azure-portal=true).
* [Configure a Server Core installation of Windows Server 2016 or Windows Server, version 1709, with Sconfig.cmd](/en-us/windows-server/get-started/sconfig-on-ws2016?azure-portal=true).
* [Download and install the Windows ADK](/en-us/windows-hardware/get-started/adk-install?azure-portal=true).
* [Automate Windows Setup](/en-us/windows-hardware/manufacture/desktop/automate-windows-setup?azure-portal=true).
* [Course WS\-011T00\-A: Windows Server 2019 Administration](/en-us/certifications/courses/ws-011t00?azure-portal=true).

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/perform-post-installation-configuration-of-windows-server/_

## Fuentes
- [Perform post-installation configuration of Windows Server](https://learn.microsoft.com/en-us/training/modules/perform-post-installation-configuration-of-windows-server/?WT.mc_id=api_CatalogApi)
