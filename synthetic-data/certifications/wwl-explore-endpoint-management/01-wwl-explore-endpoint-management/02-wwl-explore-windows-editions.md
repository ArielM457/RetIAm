# Explore Windows Editions

> Curso: MD-102 Explore endpoint management (wwl-explore-endpoint-management) · Seccion: MD-102 Explore endpoint management
> Duracion estimada: 36 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You can use Windows 10 and 11 on various computing devices. These range from traditional platforms to the latest tablets, phones, and gaming platforms. This module introduces the different editions of Windows client OS and their features. We'll describe why and when you might select a specific Windows edition. This module also covers the various methods of installing the Windows client OS.

#### Objectives

After completing this module, you'll be able to:

* Explain the differences between the different editions of Windows.
* Select the most suitable Windows device for your needs.
* Describe the recommended minimum hardware requirements for installing Windows 10 and 11\.

---

## Examine Windows client editions and capabilities

It's essential that you select the most suitable edition for your organization before you install Windows. The different editions of Windows address the needs of consumers, from individuals to large enterprises. This unit describes the various features of each edition available for Windows 10 and later.

| **Windows 10 / Windows 11 Edition** | **Audience** | **Availability** |
| --- | --- | --- |
| Home | Individual home use | Everyone |
| Pro | Small and mid\-sized businesses, advanced users | Everyone |
| Pro for Workstations | Users with advanced performance and storage requirements | Everyone |
| Enterprise | Large enterprise organizations | Available to Volume LicenseMicrosoft Volume Licensing, Microsoft Enterprise Agreement, Microsoft Store for Education or Microsoft Cloud Solution Provider program |
| Enterprise LTSC | Large enterprise organizations with restrictive change requirements | Microsoft Volume Licensing, Microsoft Enterprise Agreement, or Microsoft Cloud Solution Provider program |
| Pro Education | Comparable to Pro for school staff, administrators, teachers, and students | Available to academic Volume License customers |
| Education | Comparable to Enterprise for school staff, administrators, teachers, and students | Available to academic Volume License customers |
| IoT Core/Enterprise | Fixed purpose and appliance devices | Available through Windows IoT Distributors |

#### Windows edition details

##### Home

Home is the consumer\-oriented desktop edition of Windows. It offers the familiar Windows experience for PCs, tablets, and the new hybrid laptop/tablets. Features with Home edition include:

* Microsoft Edge
* Windows Hello
* Virtual Desktops
* Photos, Maps, Mail, Calendar, Music and Video, and other built\-in universal Windows apps
* Device encryption
* Firewall and virus protection
* Always On VPN
* New updates and features received automatically

##### Pro

Pro edition builds on the features of Windows Home, with many extra features to meet the needs of small and medium\-sized businesses. Pro edition is also suitable for advanced consumers looking for features like BitLocker and virtualization.

Some of the features Pro edition provides:

* **Windows Autopilot:** Windows Autopilot uses an existing Windows installation to transform or reset the device to a “business\-ready” state, applying settings, policies, apps, and edition changes without reimaging.
* **Dynamic Provisioning:** Dynamic Provisioning allows an organization's out\-of\-the\-box PC to be configured with minimal effort.
* **Mobile Device Management (MDM) support:** Mobile Device Management support allows devices to be managed through an MDM service instead of traditional management solutions.
* **Domain Join:** Computers can join the Active Directory domain.
* **Ability to join Microsoft Entra ID:** This ability enables users to perform single sign\-on across Windows, Microsoft 365, and other cloud\-hosted apps and services.
* **Group Policy Management:** Domain joined computers support the Group Policy Management feature.
* **BitLocker:** BitLocker functions as a complete volume encryption and boot environment protection solution.
* Windows Information Protection (with MDM management) helps protects apps and data leaks on organization and personally owned devices.
* **Assigned Access:** Allows devices to run different applications based on the user.
* **Remote Desktop:** This feature enables Remote Desktop connections from compatible Remote Desktop Connection clients.
* **Client Hyper\-V:** Client Hyper\-V allows you to host virtual machines on a client computer with sufficient hardware resources.
* **Microsoft Store for Business:** Single store for finding and managing apps in an organization.
* **Windows Update for Business:** A cloud\-based Windows Update solution can configure distribution rings, maintenance windows, peer\-to\-peer delivery, and integration with tools like Microsoft Intune.
* **Enterprise Data Protection:** This new Windows feature lets organizations control which applications can access sensitive data.
* **Granular user\-interface Control:** This feature enables administrators to lock the user interface so that users can perform specific tasks only. This feature is useful when deploying Windows as a kiosk.
* **Enterprise State Roaming:** Enterprise State Roaming provides users a unified experience across organizational Windows devices.

##### Pro for Workstations

Pro for Workstations edition offers the same features as the Pro edition. It includes more features intended for workloads that require higher performance and resilience.

* **ReFS (Resilient File System):** ReFS provides cloud\-grade resiliency for data on fault\-tolerant storage spaces and manages large volumes.
* **Persistent memory:** Support for non\-volatile memory modules (NVDIMM\-N). When turning off the workstation, data and files in memory persist.
* **SMB Direct:** SMB Direct supports network adapters that have Remote Direct Memory Access capability. SMB Direct offers improved performance when transferring large amounts of data on remote SMB file shares.
* **Expanded Hardware Support:** Expanded Hardware Support takes full advantage of high\-performance hardware such as server\-grade Intel Xeon and AMD Opteron processors, with support for up to 4 CPUs and 6 TB of memory.

##### Enterprise

Enterprise edition builds on the features of the Pro edition, with extra features that meet the needs of large enterprises. Enterprise edition is available to Volume Licensing customers only. They can choose the pace at which they adopt new technology. Enterprise edition also supports a broad range of options for operating system deployment and device and app management.

Some of the features Enterprise edition provides:

* **BranchCache:** Allows content from file and web servers on a wide area network (WAN) to be cached on computers at a local branch office.
* **Start menu layout control:** This feature enables you to use MDM policies or Group Policies to customize the appearance and content of the start menu.
* **Microsoft Defender Credential Guard:** Virtualization\-based security isolates secrets, so only privileged users can access them.
* **Microsoft Defender Application Control:** Controls what applications run within your environment to help block against malware and untrusted apps.
* **Microsoft Defender Application Guard:** Opens untrusted websites in a Hyper\-V container to isolate in case the site is malicious.
* **Microsoft Application Virtualization (App\-V):** Enables organizations to deliver Win32 applications to users as virtual applications.
* **Microsoft User Experience Virtualization (UE\-V):** Capture user\-customized Windows and application settings and store them on a centrally managed network.
* **License rights:** For virtual desktops and edition step\-up from Pro edition using cloud activation.
* **DirectAccess:** While this feature is supported, it’s recommended that organizations use “Always On VPN,” which is available in Pro, Enterprise, and Education editions.

##### Enterprise LTSC

Enterprise Long Term Servicing Channel (LTSC) is a special edition of Enterprise that Microsoft won't update with any new features. Enterprise LTSC only gets security updates and other important updates. You can install Enterprise LTSC to devices that run in a known environment that doesn't change. A typical example would be a PC used as part of a medical or industrial system. These environments are typically closed systems designed to a particular specification that traditional updates would affect. The differences between Enterprise LTSC and the standard Enterprise edition include:

* Doesn't receive feature upgrades
* No Microsoft Edge browser (can be installed separately)
* No Microsoft Store client
* Many built\-in universal Windows apps are missing

Microsoft releases an updated version of the LTSC edition approximately every three years. Windows Enterprise LTSC 2021 is the current release and includes the cumulative updates provided up to and including version 21H2\.

Windows 11 LTSC isn't yet available. Microsoft recommends that customers with devices best suited for LTSC scenarios continue using Windows 10 Enterprise LTSC.

Note

The Long\-Term Servicing Channel edition was previously called the Long Term Servicing Branch (LTSB).

##### Pro Education and Education

Pro Education and Education offer the same features as Pro and Enterprise editions, respectively, except for the Long\-Term Servicing Channel. These editions of Windows have configurations more suitable for school staff, administrators, teachers, and students. Pro Education and Education editions are only available through academic Volume Licensing.

##### IoT Core/Enterprise

The IoT Edition of Windows is designed for fixed\-purpose devices. Examples include automated teller machines, point\-of\-sale terminals, and industrial and medical devices. Windows 10 IoT Core is a smaller OS designed to run a single app, while Windows 10/11 IoT Enterprise is a full version of Windows Enterprise with specialized features.

IoT and LTSC, while they might sound similar, are intended for different purposes. LTSC is deployed to a computer for a specific process. It's installed by and licensed by the company using it. IoT is embedded on a particular device or appliance by the manufacturer. A consumer might purchase the device, but the manufacturer has already purchased the license.

---

## Select client edition

Windows 11 and previous editions run on several devices or form factors. However, not all editions of Windows can run on all device types. This discussion will help you decide which form factor and edition of Windows to choose in different scenarios.

#### Form factors

Microsoft designed Windows to run on several form factors. Here’s a list of the different form factors and their typical use in a work environment:

* **Desktop PC:** The desktop PC is the form factor of choice in businesses where the need for high performance is predominant, such as computer\-aided design (CAD).
* **Laptop:** Traditionally, traveling users were the primary users of laptops. However, recently laptop sales have surpassed desktop PC sales because of increasing workforce mobility, many employees shifting to work at home scenarios, and superior laptop performance. When a consumer uses a laptop as an office computer, adding an external keyboard, mouse, and monitor can remedy the lack of workplace ergonomics.
* **Tablet:** Tablets are famous for reading emails, doing presentations, or as entertainment devices. The latest developments bring improved performance but still lack the possibility of expansion.
* **Hybrid:** The popularity of tablets has led to the innovation of a hybrid device. A hybrid device converts from a standard laptop to a tablet. Hybrid devices are more popular than tablets among users whose work involves more typing. These devices also offer better performance than typical tablets. Devices like the Surface Pro have a tablet form factor, but the keyboard cover allows the device to become a laptop.
* **Xbox:** The Xbox is a device that is most popular for gaming and entertainment.
* **HoloLens:** The HoloLens is one of the first holographic computers. It has many uses for educational purposes, design, and constructing businesses.
* **Surface Hub:** The Surface Hub is a large\-format, touch friendly monitor used in meetings.

#### 32\-bit and 64\-bit editions

Windows 11 is only available in 64\-bit. Desktop editions of Windows 10 are available in both 32\-bit and 64\-bit versions. However, starting with Windows 10 2004 update, OEMs selling new devices are only sold with 64\-bit editions. Existing devices with Windows 10 32\-bit installations will continue to receive updates. Most devices in use today that can run Windows have 64\-bit architectures. Devices running 32\-bit installations of Windows are becoming increasingly rare.
Whether you use Windows 10 or 11, install or upgrade to the 64\-bit version of Windows to take advantage of the increased performance, memory, and security capabilities available with 64\-bit hardware. Some reasons include:

* Most devices in use today have 64\-bit architectures.
* If you install a 32\-bit edition of Windows 10 on 64\-bit processor architecture, the operating system doesn’t take advantage of any 64\-bit processor architecture features or functionality. Most notable is that 32\-bit editions of Windows can’t address over 4 GB of memory.
* 64\-bit editions of Windows require 64\-bit drivers. Most device manufacturers no longer offer a 32\-bit driver on new products. You can’t install a 64\-bit driver on a 32\-bit edition of Windows, even if the device’s architecture is 64\-bit.
* The 64\-bit edition of Windows supports running native 32\-bit and 64\-bit applications. 64\-bit applications can’t run on the 32\-bit edition of Windows 10\. 16\-bit applications won’t run natively on Windows 10 64\-bit editions.

32\-bit editions of Windows should only be installed on legacy hardware or drivers that only support 32\-bit architectures or when 16\-bit Windows applications are used in the organization. Given the significant trade\-offs of not using 64\-bit, organizations should consider solutions such as virtualization to support legacy apps as an alternative.

#### Scenarios

* **Scenario 1**. Contoso Pharmaceuticals is considering purchasing new computers to control and supervise its production lines. The production lines require special hardware with sensors in the computers that employees will use to perform the supervision. The production line software is sensitive to significant changes in the operating system. Which edition of Windows would you recommend for purchase by Contoso Pharmaceuticals to supervise its production lines?
* **Scenario 2**. Samuel is an independent contractor. He often travels with his laptop, which contains sensitive customer financial data. He’s concerned about the impact on his business if his laptop is lost or stolen. Which edition of Windows would be best suited to protect his data?
* **Scenario 3**. Contoso Pharmaceuticals is expanding its remote workforce and wants to ensure that remote connections to the company's network are secure and managed efficiently. They are looking for advanced security features and management tools to handle remote desktop services. Which edition of Windows would you recommend for Contoso Pharmaceuticals?

##### Scenario Answers

* ***Scenario 1\.** Enterprise LTSC \- As it doesn't receive feature updates, this minimizes changes to the OS that may affect the sensitive application.*
* ***Scenario 2\.** Pro \- While Samuel can use any edition of Windows to take advantage of features such as OneDrive to minimize losing data, or Windows Hello for authentication, the extra benefits of Pro like BitLocker can protect his data from being accessed in the event his device is stolen.*
* ***Scenario 3\.** Enterprise \- The Windows Enterprise edition offers advanced security features such as DirectAccess, Windows Defender Credential Guard, and Windows Defender Application Guard. Additionally, it provides comprehensive management tools for remote desktop services, making it ideal for businesses with a growing remote workforce.*

---

## Examine hardware requirements

Windows 10 and 11 have similar requirements. Many computers in enterprises today easily meet the minimum hardware requirements.

#### OS requirements

The following section lists the minimum recommended hardware requirements for the Windows client. Windows will still install with some of these requirements not being met. However, you might compromise the user experience and operating system performance if the computer doesn't meet or exceed the following specifications:

##### Windows 10

* **Processor**: 1 gigahertz (GHz) or faster processor, or system on a chip (SOC)
* **RAM:** 1 GB for 32\-bit or 2 GB for 64\-bit
* **Hard disk space**: 16 GB for 32\-bit or 20 GB for 64\-bit
* **Graphics card**: DirectX 9 or newer with Windows Display Driver Model (WDDM) 1\.0 driver
* **Display**: 800x600 pixels

Note

Beginning with Windows 10 version 2004, new computers are no longer sold with a 32\-bit edition.

##### Windows 11

Devices must meet the following minimum hardware requirements to install or upgrade to Windows 11:

* **Processor**: 1 gigahertz (GHz) or faster with two or more cores on a compatible 64\-bit processor or system on a chip (SoC).
* **RAM**: 4 gigabytes (GB) or greater.
* **Storage**: 64 GB or greater available storage

	+ Extra storage space might be required to download updates and enable specific features.
* **Graphics card**: Compatible with DirectX 12 or later, with a WDDM 2\.0 driver.
* **System firmware**: UEFI, Secure Boot capable.
* **TPM**: Trusted Platform Module (TPM) version 2\.0\.
* **Display**: High definition (720p) display, 9" or greater monitor, 8 bits per color channel.
* **Internet connection**: Internet connectivity is necessary to perform updates, and to download and use some features.

	+ Windows 11 Home edition requires an internet connection and a Microsoft account to complete device setup on first use.

##### Feature\-specific requirements

Windows client offers more options if the correct hardware is present. The following are some of the hardware and software requirements for various additional features:

* **Windows Hello:** Windows Hello requires a specialized illuminated infrared camera for facial recognition, iris detection, or a fingerprint reader that supports the Windows Biometric Framework.
* **Two factor authentication:** Two\-factor authentication requires using a PIN, fingerprint reader, illuminated infrared camera, or a phone with Wi\-Fi or Bluetooth capabilities.
* **Snap:** Windows might limit the number of simultaneously snapped applications depending on the monitor’s resolution. In Windows 11, three\-column layouts require a screen that is 1920 effective pixels or greater in width.
* **Secure boot:** Secure boot requires firmware that supports Unified Extensible Firmware Interface (UEFI) and has the Microsoft Windows Certification Authority in the UEFI signature database. The secure boot process takes advantage of UEFI to prevent the launching of unknown or unwanted operating\-system boot loaders between the system’s BIOS start and the Windows 10 operating system start. While the secure boot process isn't mandatory for Windows 10, it increases the integrity of the boot process.
* **DirectX:** Some applications may require a graphics card with a higher version of DirectX for optimal performance.
* **BitLocker to Go:** Requiring a USB flash drive. This feature is available in Windows Pro and above editions.
* **Client Hyper\-V:** Client Hyper\-V requires a processor with second\-level address translation (SLAT) capabilities and 4 GB (if Windows 10\). This feature is available in Windows Pro editions and above.
* **Miracast/Windows Projection:** Requires a display adapter that supports WDDM, and a Wi\-Fi adapter that supports Wi\-Fi Direct.
* **Wi\-Fi Direct Printing:** Requires a Wi\-Fi adapter that supports Wi\-Fi Direct and a device that supports Wi\-Fi Direct Printing.
* **InstantGo:** InstantGo works only with computers designed for connected standby. InstantGo allows network connectivity in standby mode and allows for receiving updates, mail, and Skype calls with the screen turned off.
* **DirectStorage:** DirectStorage requires an NVMe SSD to store and run games that use the Standard NVM Express Controller driver and a DirectX12 GPU with Shader Model 6\.0 support.

#### Device drivers

Windows will detect most hardware and install the driver to support the device. Many companies producing hardware have their drivers certified at the Windows Hardware Quality Labs and delivered through Windows updates.

However, you might not find a built\-in driver for a specific piece of hardware. Depending on your deployment method, you may need the driver deployment to complete parts of the OS installation. The best way to find hardware drivers is to search the manufacturer’s website.

#### Check for Hyper\-V compatibility

To verify compatibility, open PowerShell window or a command prompt and run **systeminfo.exe**. If all listed Hyper\-V requirements have a value of **Yes**, your system can run the Hyper\-V role. Below, you can see that we verified the hardware requirements highlighted above when **systeminfo.exe** is executed.

You'll see the following message from systeminfo.exe if Hyper\-V is already enabled on the system:

`Hyper-V Requirements: A hypervisor has been detected. Features required for Hyper-V will not be displayed.`

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary

In this module, you compared the different editions of Windows, the intended audiences, and the features they provide. You learned about the other form factors that Windows runs on and the scenarios that best fit the different editions offered. You examined the minimum hardware requirements for Windows 10 and 11 and how to check for Hyper\-V compatibility.

#### Learn more

* [Windows 11 requirements](/en-us/windows/whats-new/windows-11-requirements)
* [Windows 11 Specs and System Requirements](https://www.microsoft.com/windows/windows-11-specifications?r=1)
* [Windows 10 Hyper\-V System Requirements](/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/explore-windows-editions/_

## Fuentes
- [Explore Windows Editions](https://learn.microsoft.com/en-us/training/modules/explore-windows-editions/?WT.mc_id=api_CatalogApi)
