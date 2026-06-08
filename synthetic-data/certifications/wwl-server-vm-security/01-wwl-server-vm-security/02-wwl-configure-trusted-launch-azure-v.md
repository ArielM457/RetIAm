# Configure trusted launch security features for Azure virtual machines

> Curso: Implement security for servers and virtual machines (wwl-server-vm-security) · Seccion: Implement security for servers and virtual machines
> Duracion estimada: 28 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Manufacturing operates dozens of Azure virtual machines that control production systems on the factory floor. These VMs were deployed before Trusted Launch became the default security configuration for Generation 2 (Gen2\) Azure VMs. A recent security audit revealed a critical gap: no boot integrity controls are in place, which means rootkit or boot\-kit malware could compromise the operating system before any endpoint protection software loads. Several of the factory VMs are still Generation 1 (Gen1\), which further limits security options.

In this module, you learn how Trusted Launch protects Azure VMs from boot\-level threats using three integrated security components: Secure Boot, virtual Trusted Platform Module (vTPM), and integrity monitoring. You explore how to enable Trusted Launch on new and existing virtual machines. Then you learn to upgrade Gen1 VMs to Gen2 with Trusted Launch enabled, and enforce Trusted Launch adoption across your VM estate using Azure Policy.

### Learning objectives

In this module, you:

* Identify how Trusted Launch protects against boot\-level threats using Secure Boot, vTPM, and integrity monitoring
* Enable Trusted Launch and configure its security components on new and existing Azure VMs
* Upgrade existing Gen1 VMs to Gen2 with Trusted Launch enabled
* Enforce Trusted Launch adoption using built\-in Azure Policy

### Prerequisites

* Familiarity with Azure virtual machines and basic VM management tasks
* Understanding of Azure Policy concepts and policy assignment
* Access to an Azure subscription with permissions to create and modify virtual machines

---

## Identify Trusted Launch components and VM security types

Boot\-level threats represent one of the most difficult security challenges in cloud computing. Malware that compromises the boot process loads before any security software, making it nearly impossible to detect or remove. For Contoso Manufacturing, this risk is especially critical—factory floor systems run 24/7 and often execute with elevated privileges to control industrial equipment. A rootkit infection could go undetected for months while manipulating production data or creating safety hazards.

Trusted Launch addresses this challenge by establishing a hardware\-backed chain of trust from the moment a VM powers on. You explore the three security components that work together to verify boot integrity and detect tampering.

| Component | Protection Layer | Key Capability |
| --- | --- | --- |
| Secure Boot | Firmware and boot loader | Blocks unsigned boot code |
| vTPM | Boot measurement | Cryptographically records boot chain |
| Integrity monitoring | Attestation and alerting | Surfaces boot integrity failures |

### Compare VM security types

Azure virtual machines support three security types that determine the level of boot and runtime protection. The security type you select dictates which security features are available and how the VM interacts with Azure platform security services.

**Standard security** represents the traditional VM configuration with no built\-in boot integrity protection. Gen1 virtual machines use Standard security by default and can't be upgraded to other security types without first migrating to Gen2\. Standard VMs rely entirely on operating system and application\-layer security controls—the boot process remains unverified and unmonitored.

**Trusted Launch security** provides boot integrity verification through Secure Boot, vTPM, and integrity monitoring. This security type is now the default for new Gen2 virtual machines created in the Azure portal. Trusted Launch VMs measure and verify the boot process but don't encrypt memory or provide confidential computing guarantees.

**Confidential VM security** extends Trusted Launch protections by adding memory encryption and isolation using AMD SEV\-SNP or Intel TDX technology. Confidential VMs protect data in use, not just at boot time. This security type requires specific VM sizes and incurs higher compute costs.

For Contoso Manufacturing's factory floor VMs, Trusted Launch provides the necessary boot integrity protection without the cost premium or size restrictions of Confidential VMs. The factory systems process sensitive production data but don't require memory encryption—protecting the boot chain addresses the immediate rootkit and boot kit risks identified in the security audit.

### Examine the three Trusted Launch components

Trusted Launch combines three security technologies that work together to establish and verify boot integrity. Each component plays a specific role in the defense\-in\-depth strategy.

#### Secure Boot

Secure Boot enforces a signed boot chain by verifying digital signatures at each stage of the boot process. The Unified Extensible Firmware Interface (UEFI) firmware validates the boot loader signature before execution. The boot loader validates the kernel signature. The kernel validates all kernel\-mode driver signatures. Any component without a valid signature from a trusted authority can't load.

This protection blocks unsigned or maliciously modified boot components from executing. Rootkits and boot kits that modify the boot loader, kernel, or early\-loading drivers fail signature validation and can't compromise the system. Secure Boot establishes trust at the firmware level—the earliest possible enforcement point in the boot sequence.

#### Virtual Trusted Platform Module (vTPM)

The virtual Trusted Platform Module provides a dedicated, hardware\-backed secure vault for each VM. The vTPM is fully compliant with TPM 2\.0 specifications and operates independently from the guest operating system. It measures the entire boot chain—from UEFI firmware through the operating system loader, kernel, system drivers, and boot components—by creating cryptographic hashes of each element.

These measurements are stored in Platform Configuration Registers (PCRs) inside the vTPM. Because the vTPM is isolated from the guest OS, malware can't tamper with the measurements. The cryptographic record provides irrefutable evidence of what code executed during boot.

The vTPM enables remote attestation, a process where the VM cryptographically proves to an external verifier that it booted with authorized components. The attestation service compares the vTPM measurements against known\-good baselines. If any component differs—even by a single byte—attestation fails.

For Contoso Manufacturing, vTPM measurements provide forensic evidence if a boot integrity failure occurs. Security teams can review the PCR values to identify exactly which component failed attestation and investigate whether the change was authorized or malicious.

#### Integrity monitoring

Integrity monitoring connects the vTPM measurements to Microsoft Defender for Cloud by installing the Guest Attestation extension on the VM. This extension continuously retrieves boot measurements from the vTPM and sends them to Azure's attestation service for validation.

When boot integrity fails—for example, if Secure Boot is disabled or an unmeasured component loads—the attestation service detects the mismatch between actual and expected measurements. Defender for Cloud generates a security alert that appears in the Azure portal and triggers any configured alert actions such as email notifications or Logic App workflows.

Integrity monitoring transforms the vTPM's local measurements into actionable security intelligence. Without this component, boot integrity failures would remain invisible to security operations teams.

For Contoso Manufacturing, integrity monitoring provides the operational visibility needed to maintain factory floor security at scale. When one of dozens of production VMs experiences a boot integrity failure, Defender for Cloud immediately alerts the security team rather than requiring manual checks on each VM.

### Analyze how the components work together

The three Trusted Launch components create a layered defense against boot\-level threats. Secure Boot prevents unauthorized code from executing. vTPM measures what executed during boot. Integrity monitoring surfaces failures to security teams.

Consider a scenario where an attacker attempts to install a boot kit on one of Contoso's factory VMs. If the attacker modifies the boot loader, Secure Boot blocks execution because the modified boot loader lacks a valid signature—the attack fails immediately. If the attacker somehow disables Secure Boot to bypass signature verification, the vTPM measures the configuration change. The attestation service detects that Secure Boot is disabled, and integrity monitoring triggers a Defender for Cloud alert. The security team investigates before the attacker can use the compromised boot environment.

### Identify default behavior and migration paths

Trusted Launch is now the default security type for new Gen2 virtual machines created through the Azure portal. When you create a Gen2 VM, Secure Boot and vTPM are enabled by default. Integrity monitoring requires explicit enablement during VM creation. You can disable individual components if needed, but enabling all three provides maximum protection.

Gen1 virtual machines use Standard security and require migration to Gen2 before Trusted Launch can be enabled. Azure doesn't support upgrading a Gen1 VM to Trusted Launch while remaining Gen1—you must migrate the VM to Gen2 architecture first.

---

## Enable Trusted Launch on new and existing Gen2 VMs

Enabling Trusted Launch on a new Gen2 virtual machine is largely automatic—Azure defaults Trusted Launch as the security type. Upgrading an existing Gen2 VM requires a few deliberate steps. Gen1 migration and final configuration verification are covered in the next unit.

| Scenario | VM Generation | Process Complexity | Downtime Required |
| --- | --- | --- | --- |
| New VM deployment | Gen2 | Low (automatic) | N/A |
| Existing Gen2 upgrade | Gen2 | Medium (manual) | Yes (deallocate) |

### Enable Trusted Launch on new virtual machines

When you create a new Gen2 virtual machine through the Azure portal, Trusted Launch is automatically selected as the security type. The portal defaults Secure Boot and vTPM to enabled value. Integrity monitoring requires explicit enablement by selecting the **Integrity monitoring** checkbox during VM creation.

During VM creation, on the **Basics** tab under **Instance details**, locate the **Security type** field. Verify that **Trusted launch** is selected and confirm the checkboxes:

* **Enable Secure Boot**: Enforces signature validation for boot components
* **Enable vTPM**: Activates the virtual Trusted Platform Module
* **Integrity monitoring**: Must be explicitly selected to install the Guest Attestation extension

You can disable individual components if your application has compatibility issues, but this reduces boot integrity protection. For Contoso Manufacturing's new factory floor VMs, keeping all three components enabled ensures consistent security posture across the entire production environment.

After the VM deploys, the Guest Attestation extension installs automatically if integrity monitoring is enabled. The extension begins sending boot measurements to Azure's attestation service within minutes of first boot. You can verify extension installation by navigating to the VM's **Extensions \+ applications** screen in the Azure portal.

### Upgrade an existing Gen2 VM to Trusted Launch

Existing Gen2 virtual machines with Standard security can be upgraded to Trusted Launch without migrating to a new VM. This in\-place upgrade changes the security type while preserving the VM's identity, disks, and network configuration.

Before upgrading, verify that the VM meets all prerequisites. The VM must use an operating system that supports Trusted Launch—most modern Windows Server and Linux distributions qualify. The VM size must support Trusted Launch—most current\-generation VM sizes do, but legacy sizes can’t. Check the Trusted Launch documentation for the current compatibility matrix.

If the VM uses Azure Backup, verify that it uses an Enhanced backup policy rather than a Standard backup policy. The Trusted Launch security type can't be enabled for VMs configured with Standard policy backup protection via the Azure portal—you must upgrade the backup policy before enabling Trusted Launch. Standard policy now supports Trusted Launch VMs for new backups via Azure CLI (v2\.73\.0\+), PowerShell (Az 14\.0\.0\+), and REST API (v2025\-01\-01\+), but the portal experience requires Enhanced policy.

The upgrade process requires stopping and deallocating the VM. For Contoso Manufacturing, this means scheduling the upgrade during a planned maintenance window to avoid disrupting production systems. Coordinate with operations teams to ensure no active production jobs are running when the upgrade begins.

To upgrade the VM through the Azure portal:

1. Navigate to the virtual machine and select **Stop** to deallocate the VM
2. After the VM status shows **Stopped (deallocated)**, select **Configuration** from the left navigation
3. Under **Security type**, change the dropdown from **Standard** to **Trusted launch**
4. Enable the three security components:
	* **Enable Secure Boot**
	* **Enable vTPM**
	* **Integrity monitoring**
5. Select **Save** to apply the configuration
6. Start the VM

The VM restarts with Trusted Launch enabled. During the first boot, the vTPM measures the boot chain and establishes the baseline measurements. The Guest Attestation extension installs automatically if integrity monitoring is enabled. Within 10\-15 minutes, the VM appears in Defender for Cloud with boot integrity monitoring active.

You can also perform this upgrade using Azure CLI or PowerShell, which is useful when scripting upgrades across multiple VMs.

After the upgrade completes, verify the configuration by reviewing the VM's **Overview** page. The **Properties** section displays the security type as **Trusted Launch**. Check the **Extensions \+ applications** tab to confirm that the Guest Attestation extension shows a **Provisioning succeeded** status.

---

## Migrate Gen1 VMs and configure Trusted Launch components

Gen1 virtual machines require migration to Gen2 architecture before Trusted Launch can be enabled. Once Trusted Launch is active, you can also adjust individual security components independently. You complete both scenarios and verify the final Trusted Launch configuration.

### Migrate a Gen1 VM to Gen2 with Trusted Launch

Gen1 virtual machines can't be directly upgraded to Trusted Launch—you must first migrate the VM from Gen1 to Gen2 architecture. This migration is more complex than the Gen2 security type upgrade because it changes fundamental VM characteristics, not just security settings.

The migration process uses Azure's built\-in migration tools to convert the Gen1 VM to Gen2 while simultaneously enabling Trusted Launch. Azure doesn't support migrating Gen1 to Gen2 without enabling Trusted Launch—the two changes must happen together.

Before migrating, complete a critical OS disk prerequisite. Gen1 VMs use a Main Boot Record (MBR) disk layout, but Gen2 requires GUID Partition Table (GPT) with an Extensible Firmware Interface (EFI) system partition. On Windows, use the built\-in `MBR2GPT.exe` utility to convert the disk layout before initiating the upgrade. Linux VMs require equivalent GPT conversion steps. Microsoft recommends upgrading a test Gen1 VM first to validate the process before upgrading production workloads.

Important

Windows Server 2016 doesn't include `MBR2GPT.exe` and isn't supported for the Gen1 to Trusted Launch upgrade path. If your VM runs Windows Server 2016, first perform an in\-place OS upgrade to Windows Server 2019 or 2022, then run MBR2GPT conversion. Azure Linux and Debian are also excluded from the Gen1 to Trusted Launch upgrade path.

Also understand the following limitations:

* Ephemeral OS disks are supported, but vTPM\-sealed keys and secrets can not persist across reimage or platform service healing events
* Certain legacy VM extensions can not be compatible with Gen2 architecture
* The VM's IP address can change if not using a reserved IP

The upgrade is performed in\-place on the existing VM—Azure upgrades the same VM resource to Gen2 architecture with Trusted Launch enabled. Plan the migration during a maintenance window, as the VM must be stopped and deallocated during the upgrade.

To migrate a Gen1 VM through the Azure portal:

1. Complete the MBR\-to\-GPT OS disk conversion on the running VM before proceeding
2. Stop and deallocate the VM
3. Navigate to **Configuration** in the left navigation
4. Under **Security type**, select **Trusted launch** from the dropdown
5. Enable **Secure Boot**, **vTPM**, and **Integrity monitoring**
6. Select **Save** \- Azure upgrades the VM in\-place to Gen2 architecture with Trusted Launch enabled
7. Start the VM and verify it boots successfully
8. Confirm application functionality before returning the VM to production

After migration completes, the VM runs as a Gen2 Trusted Launch VM within the same resource—no new resource is created. Verify that all application functionality works correctly after restart.

Important

The Gen1 to Trusted Launch upgrade can't be rolled back to Gen1 configuration. If rollback is needed, you must restore from a backup or restore point taken before the upgrade. Take a backup of the Gen1 VM before starting the migration.

### Configure individual security components

You can enable or disable Secure Boot, vTPM, and integrity monitoring independently even after the VM is running. This flexibility is useful when troubleshooting compatibility issues or adjusting security posture for specific workloads.

To modify individual components, navigate to the VM's **Configuration** screen and locate the **Security type** section. Each component appears as a separate toggle. If the VM is running, Azure prompts you to restart—a full stop and deallocate isn't required.

Disabling Secure Boot removes signature enforcement for boot components. Use this option only when running custom or unsigned kernel modules that can't obtain valid signatures. For Contoso Manufacturing, disabling Secure Boot should require security team approval because it eliminates the primary defense against boot\-level malware.

Disabling vTPM removes the ability to measure and attest boot integrity. Without vTPM, integrity monitoring can't function. Disable vTPM only if the VM experiences hardware compatibility issues with specific UEFI configurations.

Disabling integrity monitoring stops the Guest Attestation extension from reporting boot measurements to Defender for Cloud. Boot measurement still occurs via vTPM, but failures don't generate alerts. This configuration is useful for test environments where security alerting creates unnecessary noise.

### Verify Trusted Launch configuration

After enabling Trusted Launch, verify that all components are active and functioning correctly. Multiple verification points confirm successful configuration.

The VM's **Overview** page shows the security type in the **Properties** section. The value should display **Trusted Launch** rather than **Standard**. Trusted Launch value confirms the security type upgrades completed successfully.

The **Extensions \+ applications** tab lists all installed extensions. When integrity monitoring is enabled, you should see the **GuestAttestation** extension (or **GuestAttestationLinuxExtension** on Linux VMs) with a **Provisioning succeeded** status. If the extension shows **Provisioning failed**, review the extension logs to identify configuration issues.

Microsoft Defender for Cloud provides the most comprehensive verification. Navigate to Defender for Cloud and select **Inventory** to view all protected resources. Filter the list to show only VMs with Trusted Launch enabled. Each VM should display boot integrity monitoring as active. If Defender for Cloud shows a recommendation to enable integrity monitoring, the Guest Attestation extension failed to install correctly.

---

## Enforce Trusted Launch adoption with Azure Policy

Manual configuration works for individual VMs but doesn't scale to enterprise environments with hundreds of virtual machines across multiple subscriptions. Contoso Manufacturing operates factory floor VMs in several Azure subscriptions, organized by geographic region and production line. Ensuring every VM has Trusted Launch enabled requires automated governance rather than manual checks.

Azure Policy provides the enforcement framework to audit Trusted Launch compliance, identify VMs eligible for upgrade, and remediate noncompliant resources at scale. You explore the built\-in policies that work together to govern Trusted Launch adoption.

| Policy Focus | Policy Name | Effect Options |
| --- | --- | --- |
| Eligibility assessment | Disks and OS image should support TrustedLaunch | Audit, Disabled |
| Security configuration | Virtual Machine should have TrustedLaunch enabled | Audit, Disabled |
| Secure Boot verification | Secure Boot should be enabled (preview) | Audit, Disabled |
| vTPM verification | vTPM should be enabled (preview) | Audit, Disabled |

### Recognize the Trusted Launch policy challenge

Contoso Manufacturing's factory environment presents a common policy challenge. The VMs span multiple subscriptions, were created over several years using different templates and processes, and have varying levels of Trusted Launch compatibility. Some VMs run on Gen2 architecture with supported operating systems and can be upgraded immediately. Others are Gen1 VMs that require full migration. Still others use legacy VM sizes or operating systems that can't support Trusted Launch at all.

A successful policy strategy must distinguish between these categories. Flagging every VM as noncompliant creates alert fatigue and obscures actionable findings. The policy framework must identify which VMs can be remediated, which require migration, and which can't support Trusted Launch under current configuration.

Azure provides built\-in policies designed to address this challenge. The policies work together as a multi\-stage assessment: first identify eligible VMs, then audit security configuration, then enforce compliance on capable resources.

### Use the Trusted Launch eligibility policy

The **"Disks and OS image should support TrustedLaunch"** policy identifies Gen2 virtual machines that have compatible operating systems and VM sizes for Trusted Launch upgrade. This eligibility assessment policy evaluates each VM's current configuration against Trusted Launch requirements without making assumptions about intent.

The policy checks:

* VM generation (must be Gen2\)
* Operating system compatibility (current OS supports Trusted Launch)
* VM size compatibility (current size supports Trusted Launch security features)

VMs that meet all criteria appear as **Compliant** in the policy compliance report. VMs that fail one or more checks appear as **Non\-compliant**. The policy uses an **Audit** effect, which means it evaluates and reports compliance but doesn't block VM creation or modification.

For Contoso Manufacturing, this policy provides the inventory needed to plan Trusted Launch rollout. The compliance report answers critical planning questions: How many VMs are already eligible for upgrade? Which subscriptions have the highest concentration of compatible VMs? Are there specific VM sizes or operating systems that dominate the noncompliant list?

Assign this policy first, before attempting to enforce Trusted Launch adoption. The eligibility data informs remediation priority and helps identify VMs that need migration versus simple security type upgrade.

### Use the Trusted Launch security configuration policy

The **"Virtual Machine should have TrustedLaunch enabled"** policy audits whether VMs actually have Trusted Launch configured as their security type. This policy focuses on security configuration rather than eligibility—it identifies VMs that could have Trusted Launch but currently use Standard security.

The policy evaluates the VM's security type property. VMs with security type set to **TrustedLaunch** appear as **Compliant**. VMs with security type set to **Standard** appear as **Non\-compliant**.

This policy supports two effects:

* **Audit**: Evaluate and report compliance without blocking actions
* **Disabled**: Don't evaluate the policy

In **Audit** mode, the policy evaluates VMs and reports noncompliance but doesn't block VM creation or modification. This allows you to identify which VMs in your estate are using Standard security and are candidates for upgrade, without disrupting ongoing deployments.

For Contoso Manufacturing, assigning this policy in Audit mode across the factory subscriptions gives the security team a compliance baseline—a clear view of how many VMs have Standard security and need to be upgraded to Trusted Launch.

### Use individual Secure Boot and vTPM policies

Azure provides other built\-in policies that verify specific Trusted Launch components rather than the overall security type:

* **"\[Preview]: Secure Boot should be enabled on supported Windows virtual machines"**
* **"\[Preview]: vTPM should be enabled on supported virtual machines"**

These policies use the **Audit** effect. They evaluate whether Secure Boot or vTPM is enabled on VMs that support these features. VMs appear as noncompliant if the security type is Trusted Launch but individual components are disabled.

For Contoso Manufacturing, these policies catch a gap the configuration policy misses. A VM might have security type set to Trusted Launch but have Secure Boot disabled due to manual configuration changes. The configuration policy reports that VM as compliant; the Secure Boot policy flags it as noncompliant. Assign these policies alongside the eligibility and configuration policies so your compliance baseline covers both the security type setting and the individual component state.

### Assign the Trusted Launch policies

Azure doesn't provide a built\-in initiative that bundles the Trusted Launch policies. Assign each policy individually, or group them into a custom initiative to simplify management across multiple subscriptions.

Assigning at management group scope provides the broadest coverage. For Contoso Manufacturing, assigning at the **Factory Operations** management group covers all subscriptions used for production systems—including subscriptions created in the future, so new factories automatically inherit the compliance requirement.

To assign each policy:

1. Navigate to **Policy** in the Azure portal
2. Select **Definitions** and search for the policy by name
3. Select the policy and choose **Assign**
4. Set the scope to the appropriate management group or subscription
5. Configure the policy effect:
	* Set the eligibility policy to **Audit**
	* Set the configuration policy to **Audit** to evaluate and report compliance
6. Create the assignment
7. Repeat for each remaining Trusted Launch policy

Policy evaluation begins within minutes of assignment. Azure scans all VMs in scope and populates the compliance dashboard. The initial scan typically completes within an hour for environments with hundreds of VMs.

### Interpret the compliance dashboard

The policy compliance dashboard shows compliance percentage and resource counts for each policy in the initiative. Understanding how to interpret these results is essential for planning remediation.

To view the compliance dashboard:

1. Navigate to **Policy** in the Azure portal
2. Select **Compliance** from the left menu
3. Select a Trusted Launch policy assignment to open the detailed compliance view

The eligibility policy compliance report answers: "Which VMs are capable of running Trusted Launch?" Noncompliant VMs in this category require investigation. Are they Gen1 VMs that need migration? Do they use unsupported VM sizes that need to be resized? Do they run legacy operating systems that need to be upgraded?

The configuration policy compliance report answers: "Which capable VMs currently lack Trusted Launch?" Noncompliant VMs in this category are the primary remediation targets. These VMs meet all technical prerequisites but never configured for Trusted Launch yet.

For Contoso Manufacturing, the compliance dashboard reveals the remediation backlog. If 200 VMs are eligible but only 50 have Trusted Launch enabled, the gap of 150 VMs represents the immediate upgrade opportunity—no migration required, just a security type change.

### Create remediation tasks for noncompliant VMs

Azure Policy supports automated remediation for certain policy types through remediation tasks. For the Trusted Launch configuration policy, remediation tasks can automatically enable Trusted Launch on noncompliant Gen2 VMs that meet eligibility criteria.

To create a remediation task:

1. Navigate to the policy assignment in the Azure portal
2. Select **Create remediation task**
3. Choose the policy to remediate (select the configuration policy)
4. Review the list of noncompliant resources
5. Configure remediation options:
	* Remediate all noncompliant resources, or select specific VMs
	* Set the **managed identity** location (required for remediation to modify resources)
6. Create the remediation task

Azure queues the remediation task and begins processing VMs. The task stops and deallocates each VM, updates the security type to Trusted Launch, enables Secure Boot and vTPM, and restarts the VM. This process takes several minutes per VM.

**Critical consideration**: VMs must be stopped and deallocated for remediation to succeed. Remediation tasks don't automatically stop running VMs—if the VM is running when the task executes, remediation fails. For Contoso Manufacturing's production environment, this means remediation tasks should target stopped VMs first. Then other maintenance should be scheduled during maintenance windows when VMs can be safely stopped.

Monitor remediation task progress through the **Remediation** tab in the policy assignment. The dashboard shows how many VMs were successfully remediated, how many failed, and detailed error messages for failures. Common failure reasons include: VM was running when remediation executed, VM uses Azure Backup with Standard policy, or VM size doesn't fully support Trusted Launch despite passing eligibility checks.

---

## Knowledge check

You explored how Trusted Launch protects Azure VMs from boot\-level threats through Secure Boot, vTPM, and integrity monitoring. You learned how to enable these protections on new and existing VMs and how to enforce adoption using Azure Policy. Test your knowledge of these concepts with the following questions.

### Check your knowledge

---

## Summary

Contoso Manufacturing faced a critical security gap: factory floor VMs lacked boot integrity protection, which left them vulnerable to rootkits and boot\-kits that could compromise systems before endpoint protection loads. Several VMs were still Generation 1, further limiting security options.

In this module, you learned how Trusted Launch addresses boot\-level threats through three integrated security components. Secure Boot enforces signature validation for boot components, blocking unsigned malware from executing. The virtual Trusted Platform Module (vTPM) measures the entire boot chain and creates cryptographic evidence of boot integrity. Integrity monitoring connects vTPM measurements to Microsoft Defender for Cloud, generating security alerts when boot integrity fails.

You explored how to enable Trusted Launch in multiple scenarios: automatically on new Gen2 VMs, through security type upgrade on existing Gen2 VMs, and through migration for Gen1 VMs. You learned that enabling Trusted Launch on existing VMs requires stopping and deallocating the VM, and that Azure Backup configurations must use Enhanced policies to support Trusted Launch.

Finally, you examined how Azure Policy enforces Trusted Launch adoption at scale. The built\-in eligibility policy identifies Gen2 VMs capable of running Trusted Launch. The configuration policy audits which VMs actually have Trusted Launch enabled. Together, these policies provide the governance framework to assess compliance, plan remediation, and prevent configuration drift through management group assignments.

For Contoso Manufacturing, implementing Trusted Launch across factory floor VMs establishes a hardware\-backed root of trust at the boot layer. Boot integrity monitoring through Defender for Cloud ensures that any tampering attempt triggers immediate security team response. Gen1 VMs now have a clear migration path to modern security controls. Azure Policy assignment at management group scope ensures that all future factory systems automatically inherit Trusted Launch protection.

In this module, you:

* Identified how Trusted Launch protects against boot\-level threats using Secure Boot, vTPM, and integrity monitoring
* Enabled Trusted Launch and configured its security components on new and existing Azure VMs
* Upgraded existing Gen1 VMs to Gen2 with Trusted Launch enabled
* Enforced Trusted Launch adoption using built\-in Azure Policy

### Learn more

* [Trusted launch for Azure VMs](/en-us/azure/virtual-machines/trusted-launch)
* [Enable Trusted Launch on existing Gen2 VMs](/en-us/azure/virtual-machines/trusted-launch-existing-vm)
* [Upgrade Gen1 VMs to Trusted Launch](/en-us/azure/virtual-machines/trusted-launch-existing-vm-gen-1)
* [Boot integrity monitoring overview](/en-us/azure/virtual-machines/boot-integrity-monitoring-overview)
* [Trusted Launch built\-in policies](/en-us/azure/virtual-machines/trusted-launch-portal)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-trusted-launch-azure-virtual-machines/_

## Fuentes
- [Configure trusted launch security features for Azure virtual machines](https://learn.microsoft.com/en-us/training/modules/configure-trusted-launch-azure-virtual-machines/?WT.mc_id=api_CatalogApi)
