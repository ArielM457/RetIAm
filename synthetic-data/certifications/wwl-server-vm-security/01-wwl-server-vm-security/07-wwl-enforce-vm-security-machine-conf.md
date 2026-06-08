# Enforce VM security configuration with Azure Machine Configuration

> Curso: Implement security for servers and virtual machines (wwl-server-vm-security) · Seccion: Implement security for servers and virtual machines
> Duracion estimada: 24 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Manufacturing closed critical security gaps across their server estate—encrypted disks protect data at rest, just\-in\-time access guards remote connections, and Defender for Servers detects runtime threats. One vulnerability remains unaddressed: operating system configuration drift. Factory servers and Arc\-enrolled on\-premises machines could have unnecessary services running, weak cryptographic settings, default accounts, or registry misconfigurations that enable lateral movement—none of which are currently audited or enforced.

Azure Machine Configuration provides policy\-driven auditing and enforcement of OS\-level security settings. In this module, you explore how to deploy and configure Machine Configuration to close Contoso's final security gap.

Here, you learn how to:

* Explore how Azure Machine Configuration audits and enforces OS\-level settings using Azure Policy
* Deploy the Azure Machine Configuration extension and configure required prerequisites
* Assign built\-in Windows and Linux security baseline policies in audit and enforce modes
* Author and publish a custom machine configuration for organization\-specific requirements

### Prerequisites

* Familiarity with Azure Policy concepts, including initiatives, assignments, and compliance reporting
* Understanding of Azure virtual machines and Azure Arc\-enabled servers
* Access to an Azure subscription with virtual machines or Arc\-enrolled servers to configure

---

## Explore Azure Machine Configuration extension capabilities and modes

Azure Machine Configuration extends Azure Policy from cloud resource management into guest operating system configuration. While standard Azure Policy governs resource\-level settings like network rules and disk encryption, Machine Configuration reaches inside the guest OS to audit and enforce security configurations at the operating system level.

| Aspect | Description |
| --- | --- |
| **Scope** | Audits and enforces OS\-level settings (registry, services, files, permissions) |
| **Platform** | Azure VMs (Windows and Linux) and Azure Arc\-enabled servers |
| **Delivery mechanism** | Azure Machine Configuration extension running inside the VM |
| **Compliance reporting** | Results appear as Azure Policy compliance data |
| **Authentication** | System\-assigned managed identity authenticates to Azure |

### How Machine Configuration works

The Azure Machine Configuration extension runs as a guest agent inside each virtual machine. The extension evaluates OS settings against a configuration definition—either a built\-in Microsoft baseline or a custom configuration you author. Configuration definitions specify required states for registry keys, running services, file permissions, security policies, and application settings.

When the extension completes an evaluation cycle, it reports results to Azure Policy using the VM's system\-assigned managed identity. These results populate the same compliance dashboard you use for resource\-level policies, providing unified visibility across both infrastructure and OS configuration.

The system\-assigned managed identity serves two purposes: it authenticates the extension to Azure when reporting compliance data, and it enables the extension to access Azure resources during remediation tasks. Both the extension and the managed identity are prerequisites—without them, compliance evaluation can't occur.

### Audit mode vs. enforce mode

Machine Configuration operates in two distinct modes, each using a different Azure Policy effect. Understanding the difference prevents unexpected service disruptions.

**Audit mode** uses the `AuditIfNotExists` policy effect. The extension evaluates settings and reports noncompliance, but never modifies the system. If a registry value is set incorrectly or a service that should be stopped is running, the policy marks the resource as noncompliant. No changes occur. This mode carries no risk of disrupting running workloads.

**Enforce mode** uses the `DeployIfNotExists` policy effect. The extension evaluates settings and automatically remediates noncompliance. If a required registry value is missing, the extension creates it. If a prohibited service is running, the extension stops it. While this provides automated hardening, it can disrupt applications that depend on the current configuration state.

For production deployments, always assign policies in audit mode first. Review which settings are noncompliant, assess whether remediation would break application functionality, and document any exceptions required for business operations. Only after this review should you promote the policy to enforce mode. This audit\-to\-enforce promotion path protects against unintended outages.

### Configuration scope and capabilities

Machine Configuration can audit and enforce a wide range of OS\-level settings. On Windows systems, this includes registry keys and values, Windows services (required running state or prohibited state), local security policies (password complexity, account lockout thresholds, audit policies), user rights assignments, and Windows Defender configuration. On Linux systems, the extension manages SSH daemon configuration, filesystem permissions and ownership, kernel parameters via sysctl, systemd service states, and package installation requirements.

The same configuration definitions work across both Azure VMs and Azure Arc\-enabled servers. Contoso's factory environment includes both Azure\-native Windows Server VMs running manufacturing dashboards and Arc\-enrolled Ubuntu servers controlling programmable logic controllers on the factory floor. A single policy assignment at the management group scope applies the appropriate baseline to both platform types.

### Integration with Defender for Servers

When you enable Microsoft Defender for Servers Plan 2, the OS configuration assessment capability uses Azure Machine Configuration to evaluate security baselines. The "Machines should have a vulnerability assessment solution" and related OS misconfiguration recommendations in Defender for Cloud rely on the same extension and managed identity prerequisites covered in this module.

This integration means deploying Machine Configuration provides value beyond policy compliance—it powers Defender for Cloud's security posture assessment and contributes to your overall secure score.

### Contoso's deployment approach

Contoso Manufacturing operates a mixed environment: Windows Server VMs in Azure running ERP systems, and Ubuntu servers enrolled through Azure Arc that interfaces with factory automation equipment. Both platform types require consistent security baselines to prevent configuration drift.

The security team deploys Machine Configuration at the management group level, ensuring every subscription hosting factory infrastructure receives the same baseline policies. Because Arc\-enrolled servers already have the Azure Connected Machine agent installed, they automatically gain the managed identity prerequisite—only the Machine Configuration extension needs deployment.

With this foundation in place, you're ready to deploy the extension prerequisites and assign the first baseline policies.

---

## Apply built\-in security baseline policies

Built\-in security baseline policies provide immediate coverage of industry\-standard OS hardening controls. These Microsoft\-curated baselines map to the Microsoft Cloud Security Benchmark (MCSB) control PV\-4: Audit and enforce secure configurations for compute resources.

| Deployment step | Action |
| --- | --- |
| 1\. Deploy prerequisites | Assign initiative to install extension and managed identity |
| 2\. Create remediation task | Deploy prerequisites to existing VMs |
| 3\. Assign Windows baseline | Apply built\-in security baseline policy in audit mode |
| 4\. Assign Linux baseline | Apply built\-in security baseline policy in audit mode |
| 5\. Review compliance | Wait 24 hours, then assess noncompliance findings |
| 6\. Promote to enforce | Reassign policies with DeployIfNotExists effect (optional) |

### Deploy prerequisite infrastructure

Before any baseline policy can evaluate compliance, two components must exist on each virtual machine: the Azure Machine Configuration extension and a system\-assigned managed identity. The built\-in initiative "Deploy prerequisites to enable Guest Configuration policies on virtual machines" automates this deployment.

Assign this initiative at the management group scope that covers Contoso's factory subscriptions. The initiative uses the `DeployIfNotExists` effect, which means it deploys the extension and identity automatically to new VMs. For existing VMs, you must create a remediation task after assignment to trigger the deployment.

The policy assignment itself requires a managed identity with permissions to deploy VM extensions and assign managed identities. During the assignment process, select "System assigned managed identity" in the remediation settings and specify the appropriate region. Azure automatically grants the required permissions.

For Arc\-enabled servers, the deployment pattern differs slightly. The Azure Connected Machine agent already provides the system\-assigned managed identity—no other identity deployment is needed. You only need to deploy the Machine Configuration extension. The same prerequisite initiative handles this automatically, detecting the Arc platform and skipping identity deployment.

### Assign the Windows security baseline

The built\-in initiative "Windows machines should meet requirements of the Azure compute security baseline" evaluates over 250 Windows security settings. This baseline covers account policies (password length, complexity, history), and audit policies (sign\-in events, privilege use, system events). It also covers security options (network access controls, user account control behavior), user rights assignments (who can sign\-in locally, shut down the system, take ownership of files), and Windows Defender configuration.

Assign this initiative at the same management group scope where you deployed prerequisites. The initiative uses `AuditIfNotExists` by default—it reports noncompliance without modifying any settings. This audit\-first approach gives Contoso's team visibility into current configuration state without risk of disrupting factory systems.

After assignment, Azure Policy begins evaluating Windows VMs within the scope. Initial compliance data appears within 30 minutes for new VMs, but a complete compliance scan of existing infrastructure can take up to 24 hours. The evaluation runs on a recurring schedule—every 24 hours for audit policies, and when configuration drift is detected for enforce policies.

### Assign the Linux security baseline

The companion initiative "Linux machines should meet requirements for the Azure compute security baseline" provides equivalent coverage for Linux systems. This baseline evaluates:

* SSH daemon configuration (PermitRootLogin disabled, protocol version, strong ciphers)
* Filesystem permissions and ownership on sensitive directories
* Kernel parameters affecting network security (IP forwarding, SYN cookies, ICMP redirect handling)
* Systemd service states (unnecessary services disabled)
* Package security configurations

Use the same assignment scope and policy settings as the Windows baseline. The initiative automatically applies only to Linux VMs—Windows systems are excluded from evaluation. Contoso's Arc\-enrolled Ubuntu servers controlling factory automation equipment are covered by this single assignment.

Both baselines work together to provide platform\-appropriate security controls across the entire server estate. A single compliance dashboard in Azure Policy shows aggregate compliance across both operating system families.

### Interpret compliance results

After the initial evaluation cycle completes, navigate to Azure Policy \> Compliance and filter for your baseline policy assignments. Each initiative displays an overall compliance percentage and a count of noncompliant resources.

Drill into a noncompliant resource to see which specific settings failed evaluation. The compliance detail view shows the expected value (from the baseline definition) and the current value (detected on the VM). For example, a Windows Server might show "Audit: Force audit policy subcategory settings" expected as "Enabled" but currently set to "Disabled."

This detail is valuable when assessing whether to promote the policy to enforce mode. Some noncompliance findings represent genuine security gaps—default configurations that should be hardened. Other findings might indicate intentional configuration choices required for application compatibility. A service marked as "should be disabled" might be a legitimate requirement for manufacturing software to function.

Common noncompliance patterns in factory environments include:

* Services running that the baseline expects to be stopped (Remote Registry, Server service on workstations)
* Password policies that were never hardened post\-deployment (minimum length set to 7 instead of 14\)
* Audit policy gaps where critical event categories aren't logged
* User rights assignments that grant excessive privileges to default user groups.

### Create remediation tasks and promote to enforce mode

For the prerequisites initiative, create a remediation task immediately after assignment. This task deploys the Machine Configuration extension and managed identity to existing VMs that were deployed before the policy assignment. Navigate to Azure Policy \> Remediation \> Create remediation task, select the prerequisites initiative, and choose the specific policies to remediate. The task runs asynchronously and reports progress in the remediation view.

For the baseline initiatives themselves, remediation is a decision, not an automatic step. Because the built\-in baseline policies use `AuditIfNotExists` by default, they never modify settings. The effect of built\-in baseline policies is fixed—these policies can't be reassigned with a `DeployIfNotExists` effect.

To automatically remediate specific noncompliant settings, review the compliance findings and author custom Machine Configuration packages targeting those settings, then assign them in enforce mode. This approach is covered in the next unit. Before authoring custom remediation packages, export the compliance report, identify noncompliant settings, and work with application owners to validate that remediation won't disrupt operations. Settings that would cause application failures are documented as exceptions and addressed through custom configurations or application updates.

### Contoso's baseline deployment workflow

Contoso assigns the prerequisites initiative at their "Factory Infrastructure" management group, which contains three subscriptions hosting production factory systems. They create a remediation task targeting all three subscriptions, deploying the extension to 47 existing Azure VMs and 23 Arc\-enrolled servers.

After the extension deployment completes, they assign both Windows and Linux baseline initiatives in audit mode. The initial compliance report shows 68% compliance—32 VMs have at least one noncompliant setting. Most findings are password policy gaps and unnecessary services. The team reviews each finding, documents legitimate exceptions (one service required by PLC software), and schedules a maintenance window to address the rest.

With your built\-in baselines deployed and compliance visibility established, you're ready to extend coverage with custom configurations for Contoso\-specific requirements.

---

## Author and assign custom machine configurations

Built\-in security baselines cover industry\-standard hardening controls, but every organization has specific requirements that fall outside these standard configurations. Custom machine configurations address organization\-specific needs while maintaining the same audit\-to\-enforce workflow and compliance reporting as built\-in policies.

| Workflow step | Tool/Action |
| --- | --- |
| **Author configuration** | Write PowerShell DSC (Windows) or Chef InSpec (cross\-platform) definition |
| **Package configuration** | `New-GuestConfigurationPackage` creates .zip package |
| **Test locally** | `Get-GuestConfigurationPackageComplianceStatus` validates before publishing |
| **Publish to Azure** | Upload .zip to Azure Blob Storage (publicly accessible URL) |
| **Create policy definition** | `New-GuestConfigurationPolicy` generates custom policy JSON |
| **Import to Azure** | Add custom policy definition to management group or subscription |
| **Assign policy** | Standard Azure Policy assignment process |

### When to use custom configurations

Contoso Manufacturing has requirements that built\-in baselines don't address. The factory automation software communicates with programmable logic controllers through a specific network protocol that requires a custom registry key value on each Windows Server VM. The manufacturing execution system relies on a Windows service—the "Contoso Manufacturing Scheduler"—that must always be running for production tracking to function. On Linux systems interfacing with factory equipment, specific TLS cipher suites must be enabled for secure communication with legacy industrial control systems.

Custom configurations fill these gaps. Use them when you need to enforce organization\-specific registry values, and verify required services are running (or prohibited services are stopped). You can also validate custom application settings, check for existence and permissions of specific files or directories, or enforce security settings not covered by Microsoft baselines.

### Authoring tools and languages

The GuestConfiguration PowerShell module provides packaging and testing capabilities. Install it from the PowerShell Gallery: `Install-Module GuestConfiguration -Scope CurrentUser`. This module is required regardless of which authoring language you choose.

For Windows\-focused configurations, PowerShell Desired State Configuration (DSC) provides the authoring syntax. DSC uses declarative configuration blocks that describe the desired state—a registry key must have a specific value. There must be a service must be running, and a file must exist with specific permissions. DSC resources handle the implementation details. Windows administrators familiar with DSC can apply that knowledge directly to Machine Configuration authoring.

For cross\-platform configurations or audit\-focused checks, Chef InSpec offers an alternative authoring approach. InSpec uses a Ruby\-based domain\-specific language that reads naturally: `describe registry_key('HKLM\Software\Contoso') do its('FactoryProtocol') { should eq 'Enabled' } end`. InSpec works on both Windows and Linux, making it valuable when the same security control applies across both operating systems.

### Author a PowerShell DSC configuration

A typical Windows configuration starts with a DSC configuration block. For Contoso's factory protocol registry requirement, the configuration declares that a specific registry value must exist with a specific data value:

```
Configuration ContosoFactoryBaseline
{
    Import-DscResource -ModuleName 'PSDscResources'
    
    Node localhost
    {
        Registry FactoryProtocolEnabled
        {
            Key       = 'HKLM:\Software\Contoso\Factory'
            ValueName = 'ProtocolEnabled'
            ValueData = '1'
            ValueType = 'Dword'
            Ensure    = 'Present'
        }
        
        Service ManufacturingScheduler
        {
            Name   = 'ContosoScheduler'
            State  = 'Running'
            Ensure = 'Present'
        }
    }
}

```

Compile this configuration using `ContosoFactoryBaseline -OutputPath ./output`. DSC generates a `.mof` file containing the compiled configuration. The `.mof` becomes the input to the packaging step.

### Package and test locally

Create a guest configuration package using `New-GuestConfigurationPackage`. Specify the configuration name, the path to the compiled .mof file, and the type (Audit or AuditAndSet):

```
New-GuestConfigurationPackage `
    -Name 'ContosoFactoryBaseline' `
    -Configuration './output/localhost.mof' `
    -Type Audit `
    -Path './packages'

```

The command creates `ContosoFactoryBaseline.zip` in the packages folder. The `.zip` contains the configuration definition, required DSC resources, and metadata.

Before publishing to Azure, test the package locally. Run `Get-GuestConfigurationPackageComplianceStatus -Path './packages/ContosoFactoryBaseline.zip'` on a test VM. The command evaluates the configuration and returns compliance status—compliant or noncompliant, with details about which resources passed or failed. This local testing catches errors before deployment and validates that the configuration detects the expected conditions.

### Publish to Azure Storage

Machine Configuration policies reference configuration packages by URL. Upload the .zip package to Azure Blob Storage in a publicly accessible container, or generate a shared access signature (SAS) URL with read permissions.

Create a storage account and container if you don't have one already. Upload the package using Azure Storage Explorer, the Azure portal, or Azure CLI: `az storage blob upload --account-name contosofactory --container-name configurations --name ContosoFactoryBaseline.zip --file ./packages/ContosoFactoryBaseline.zip`.

Record the blob URL—you need it for policy creation. The URL follows the pattern `https://contosofactory.blob.core.windows.net/configurations/ContosoFactoryBaseline.zip`. If using SAS, append the SAS token to the URL.

### Create and import the custom policy definition

The `New-GuestConfigurationPolicy` command generates a custom Azure Policy definition that references your configuration package. Provide the configuration name, the package URL, the platform (Windows or Linux), the policy version, and whether the policy should audit or enforce:

```
New-GuestConfigurationPolicy `
    -PolicyId $(New-Guid) `
    -ContentUri 'https://contosofactory.blob.core.windows.net/configurations/ContosoFactoryBaseline.zip' `
    -DisplayName 'Factory VMs should meet Contoso baseline requirements' `
    -Description 'Validates registry settings and services required for factory automation software' `
    -Platform 'Windows' `
    -PolicyVersion '1.0.0' `
    -Mode Audit `
    -Path './policies' `
    -OutVariable Policy

```

The command generates a JSON policy definition file. This file contains the policy rule logic, the configuration package reference, and metadata. Import the definition to your management group or subscription using `New-AzPolicyDefinition -Name 'contoso-factory-baseline' -Policy $Policy.Path -ManagementGroupName 'Factory'`.

### Assign the custom policy

With the policy definition imported, assign it using the standard Azure Policy assignment process. Navigate to Azure Policy \> Definitions, filter for your custom policy, and select Assign. Choose the management group scope that covers factory infrastructure, configure assignment settings, and deploy.

Like built\-in baselines, assign custom policies in audit mode first. After the initial compliance evaluation, review findings, validate that the configuration detects the expected conditions, and address any unexpected noncompliance. Then, if automatic remediation is desired, create a new assignment with the enforce\-mode policy definition (generated with `-Mode ApplyAndAutoCorrect` instead of `-Mode Audit`). The `-Mode` parameter controls the policy behavior: `Audit` generates an `AuditIfNotExists` definition that reports without acting; `ApplyAndAutoCorrect` generates a `DeployIfNotExists` definition that automatically corrects drift. This is distinct from the `-Type AuditAndSet` parameter on `New-GuestConfigurationPackage`, which determines whether the package itself can apply changes.

### Contoso's custom configuration application

Contoso creates three custom configurations. The first validates that the factory protocol registry key is set correctly on Windows Server VMs running the automation dashboard. The second ensures the manufacturing scheduler service is in a running state—noncompliance triggers alerts to the operations team. The third, authored in Chef InSpec for cross\-platform coverage, validates specific TLS cipher suite configurations on both Windows and Linux systems that communicate with legacy industrial controllers.

All three configurations are published to the same Azure Storage container, imported as custom policy definitions, and assigned at the Factory Infrastructure management group scope. Compliance data flows into the same dashboard Contoso uses for built\-in baselines, providing unified visibility across both Microsoft\-curated and organization\-specific security controls.

With both built\-in and custom machine configurations deployed, Contoso closed the final gap in their server security posture—operating system configuration is now continuously audited and can be automatically enforced across their entire compute estate.

---

## Knowledge check

You explored how Azure Machine Configuration audits and enforces OS\-level security settings through Azure Policy. Test your understanding of prerequisite deployment, baseline policy assignment, and custom configuration authoring.

### Check your knowledge

---

## Summary

In this module, you deployed Azure Machine Configuration to audit and enforce operating system security settings across Contoso Manufacturing's server estate. You configured the prerequisite infrastructure—the Azure Machine Configuration extension and system\-assigned managed identities—assigned built\-in Windows and Linux security baseline policies in audit mode, and authored custom configurations for organization\-specific requirements.

### Key decisions and deployment principles

Always start policy assignments in audit mode before promoting to enforce mode. This review period identifies configuration conflicts that could disrupt running applications and allows you to document legitimate exceptions. Promoting directly to enforce mode risks unintended service outages when automated remediation changes settings required by factory software.

Both the Azure Machine Configuration extension and a system\-assigned managed identity are mandatory prerequisites for compliance evaluation. Without these components, the policy can't assess OS settings. Deploy prerequisites using the built\-in initiative before assigning baseline policies, and create remediation tasks to cover existing VMs.

Built\-in security baselines provide immediate coverage of Microsoft Cloud Security Benchmark controls. These baselines address industry\-standard hardening requirements across password policies, audit configuration, service states, and security options. Custom configurations extend this foundation to organization\-specific needs—proprietary software requirements, legacy system compatibility settings, or internal security standards not covered by Microsoft baselines.

The same policy mechanism covers both Azure VMs and Azure Arc\-enabled servers. A single assignment at management group scope applies platform\-appropriate configurations to Windows Server VMs in Azure and Arc\-enrolled Linux servers on the factory floor.

### Learning path completion

With this module, you completed the implementation of layered security controls across Contoso Manufacturing's server estate. You started with Azure Disk Encryption to protect data at rest, and added boot integrity monitoring through trusted launch. Next you implemented just\-in\-time access to guard remote connections, enabled runtime threat detection with Microsoft Defender for Servers, and concluded with OS configuration enforcement through Machine Configuration. Each layer addresses a specific attack surface—together they provide defense in depth across the entire compute platform.

Factory servers that were vulnerable to configuration drift, weak OS settings, and unaudited system changes are now continuously evaluated against both industry baselines and Contoso\-specific requirements. The security team gains compliance visibility through the Azure Policy dashboard, and automated remediation—deployed carefully after audit\-first review—prevents configuration drift.

### Learn more

* [Azure Machine Configuration overview](/en-us/azure/governance/machine-configuration/overview)
* [Author a custom machine configuration](/en-us/azure/governance/machine-configuration/how-to/create-configuration)
* [Built\-in machine configuration policies](/en-us/azure/governance/policy/samples/built-in-policies#guest-configuration)
* [OS configuration assessment in Defender for Servers](/en-us/azure/defender-for-cloud/operating-system-misconfiguration)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/enforce-vm-security-machine-configuration/_

## Fuentes
- [Enforce VM security configuration with Azure Machine Configuration](https://learn.microsoft.com/en-us/training/modules/enforce-vm-security-machine-configuration/?WT.mc_id=api_CatalogApi)
