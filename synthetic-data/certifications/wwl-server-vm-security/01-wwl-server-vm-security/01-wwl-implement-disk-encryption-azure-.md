# Implement disk encryption for Azure virtual machines

> Curso: Implement security for servers and virtual machines (wwl-server-vm-security) · Seccion: Implement security for servers and virtual machines
> Duracion estimada: 25 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Manufacturing operates factory management systems on Azure virtual machines. During a recent ISO 27001 compliance audit, assessors identified a critical security gap: production VMs lack full disk encryption. While the OS and data disks use Azure's default server\-side encryption, temporary disks and disk caches remain unencrypted. This gap exposes sensitive manufacturing process data—including programmable logic controller (PLC) configurations, supply chain logistics, and proprietary formulas—to potential access if physical hardware or hypervisor\-level compromise occurs.

As Contoso's security engineer, you need to close this compliance gap while maintaining operational efficiency. You also need to plan for the September 15, 2028 retirement of Azure Disk Encryption (ADE), the legacy BitLocker/DM\-Crypt solution that many existing workloads currently use. Modern encryption approaches provide better coverage and align with Zero Trust principles requiring data protection at rest across all storage locations.

In this module, you:

* Compare Azure managed disk encryption options and select the appropriate approach for new and existing VMs
* Configure encryption at host with customer\-managed keys using a Disk Encryption Set and Azure Key Vault
* Apply confidential disk encryption to confidential virtual machines
* Enforce disk encryption compliance using Azure Policy

### Prerequisites

* Experience deploying and managing Azure virtual machines
* Understanding of encryption concepts including symmetric encryption and key management
* Familiarity with Azure Key Vault and managed identities

Now that you understand the compliance challenge Contoso faces, you explore the available disk encryption options and determine which approach addresses their audit finding.

---

## Choose the right disk encryption option for Azure VMs

Azure provides four disk encryption options for virtual machines. Each addresses different security requirements and coverage scopes. Understanding these options helps you select the approach that meets your compliance obligations while preparing for upcoming platform changes.

| Option | What it encrypts | Key management | Status |
| --- | --- | --- | --- |
| Server\-side encryption (SSE) | OS and data disks only | Platform\-managed or customer\-managed | Current default |
| Encryption at host | OS disks, data disks, temp disks, caches | Platform\-managed or customer\-managed | Recommended for new VMs |
| Azure Disk Encryption (ADE) | OS and data disks | Customer\-managed via Key Vault | Retiring September 15, 2028 |
| Confidential disk encryption | OS disk (confidential VMs only) | vTPM\-bound | For confidential computing workloads |

### Server\-side encryption: The baseline

Server\-side encryption (SSE) runs automatically on all Azure managed disks. When you create a virtual machine, Azure encrypts the OS and data disks at the storage platform level using AES\-256 encryption. This protection requires no configuration and provides defense against physical disk theft or improper disposal.

SSE doesn't encrypt temporary disks or disk caches. For Contoso Manufacturing, this limitation creates the compliance gap identified during their audit. Production data written to temp storage or cached during high\-throughput operations remains unencrypted, violating ISO 27001 requirements for comprehensive data protection at rest.

### Encryption at host: The current recommendation

Encryption at host extends SSE coverage to include temporary disks and disk caches. Azure encrypts data flows end\-to\-end from the VM through the storage layer, addressing the exact gap in Contoso's environment. This approach provides the most comprehensive encryption available for standard VMs.

With encryption at host enabled, all data leaving the VM undergoes encryption before reaching Azure Storage. This includes:

* OS disk read/write operations
* Data disk I/O
* Temporary disk storage (D: drive on Windows, /dev/sdb1 on Linux)
* Disk controller cache operations

You enable encryption at host as a VM property during creation or by stopping an existing VM, enabling the feature, then restarting. The encryption layer sits between the VM and the storage subsystem, requiring no changes to guest OS configurations or application code. For workloads migrating from Azure Disk Encryption before the September 2028 retirement deadline, encryption at host provides a seamless replacement with broader protection coverage.

### Azure Disk Encryption: Legacy option with retirement deadline

Azure Disk Encryption (ADE) uses BitLocker (Windows) or DM\-Crypt (Linux) to encrypt disks from within the guest operating system. Many existing Azure workloads currently use this approach. However, Microsoft announced that ADE retires on September 15, 2028\.

On September 15, 2028, ADE\-enabled workloads will continue to run, but encrypted disks will fail to unlock after VM reboots, causing service disruption. All ADE\-enabled VMs and their backups must migrate to encryption at host before the retirement date to avoid this disruption.

Organizations using ADE must migrate to encryption at host or another supported option before the retirement date. The migration involves:

1. Creating snapshots of encrypted disks
2. Creating new VMs with encryption at host enabled
3. Restoring data from snapshots to the new encrypted environment
4. Validating application functionality
5. Decommissioning the ADE\-protected VMs

Unlike encryption at host, ADE requires guest OS integration, consumes VM compute resources for encryption operations, and doesn't encrypt temporary disks. These limitations make encryption at host the superior replacement for most workloads.

### Confidential disk encryption: Hardware\-isolated protection

Confidential virtual machines provide hardware\-based isolation using AMD SEV\-SNP (Secure Encrypted Virtualization \- Secure Nested Paging) technology. When you create a confidential VM, you can enable confidential disk encryption, which binds the OS disk encryption key to the VM's virtual Trusted Platform Module (vTPM).

This binding ensures that only that specific VM instance can decrypt the OS disk. If an attacker copies the encrypted disk to another system or even another Azure VM, decryption fails because the vTPM key remains isolated within the original VM's hardware\-protected boundary. Confidential disk encryption targets workloads processing highly sensitive data subject to regulatory requirements like ITAR, HIPAA, or trade secret protection.

Confidential VMs use DCasv5 or ECasv5 series sizes and require the security type set to "Confidential virtual machine" at creation time. You can't convert existing standard VMs to confidential VMs. For Contoso Manufacturing, confidential disk encryption applies to systems processing proprietary formulas or intellectual property. The systems require defense against both external attackers and insider threats with administrative access.

### Enforce compliance with Azure Policy

Azure provides built\-in policies to enforce disk encryption requirements across your VM fleet. Two key policies address encryption compliance:

* **Windows virtual machines should enable Azure Disk Encryption or EncryptionAtHost** \- Audits Windows VMs where ADE and encryption at host isn't enabled
* **Linux virtual machines should enable Azure Disk Encryption or EncryptionAtHost** \- Audits Linux VMs where ADE and encryption at host isn't enabled

Both policies use the `AuditIfNotExists` effect—they flag noncompliant VMs in the compliance dashboard but don't block VM deployment.

These policies accommodate both legacy ADE deployments and modern encryption at host configurations, allowing gradual migration while maintaining compliance oversight. You assign policies at subscription or resource group scope, then monitor compliance through Microsoft Defender for Cloud's regulatory compliance dashboard. For Contoso's ISO 27001 certification maintenance, these policies provide continuous evidence that all production VMs meet encryption requirements.

### Choose the right option for Contoso Manufacturing

For Contoso's compliance gap, encryption at host provides the optimal solution. It encrypts temporary disks and caches that SSE misses, directly addressing the audit finding. New production VMs enable encryption at host at deployment time. Existing VMs undergo a planned migration window where each system stops, enables encryption at host, then restarts with full protection coverage.

Contoso can implement customer\-managed keys (CMK) through a Disk Encryption Set to maintain organizational control over encryption key lifecycle, rotation policies, and access logging. This approach satisfies the ISO 27001 requirement for documented key management procedures while preparing the environment for future growth.

With encryption options understood, you're ready to configure encryption at host using customer\-managed keys stored in Azure Key Vault.

---

## Configure encryption at host with customer\-managed keys

Encryption at host addresses the specific gap in Contoso Manufacturing's environment: unencrypted temporary disks and caches. Configuring this protection involves enabling a VM\-level property and, for compliance scenarios requiring organizational key control, creating a Disk Encryption Set linked to Azure Key Vault.

### What encryption at host protects

Server\-side encryption (SSE) encrypts managed disks at the storage layer but leaves two critical data paths unprotected. Temporary disks (the D: drive on Windows VMs or /dev/sdb1 on Linux) use local SSD storage attached directly to the physical host. Applications frequently write cache files, page files, or temp databases to these high\-speed volumes. Disk caches buffer I/O operations between VMs and persistent storage, accelerating read and write performance. Temp disks and caches don't undergo encryption in a standard SSE\-only configuration.

With encryption at host enabled, Azure encrypts data at the compute host level before it reaches any storage medium. This protection covers:

* All managed disk I/O (OS and data disks)
* Temporary disk writes and reads
* Disk controller read and write caches
* Data in transit between the VM and storage subsystem

For Contoso's factory management systems, this means PLC configuration files temporarily staged to local storage and supply chain data cached during high\-volume batch operations receive the same encryption protection as data persisted to managed disks.

### Platform\-managed keys versus customer\-managed keys

Encryption at host supports two key management approaches. Platform\-managed keys (PMK) use encryption keys that Microsoft generates, stores, and rotates automatically. This approach requires no configuration beyond enabling encryption at host and provides immediate protection with zero administrative overhead.

Customer\-managed keys (CMK) give your organization control over the encryption key lifecycle. You generate and store keys in Azure Key Vault or Azure Key Vault Managed HSM. Then you define rotation policies, set expiration dates, and maintain audit logs of every key access operation. Compliance frameworks like ISO 27001, PCI DSS, and FedRAMP often require documented evidence of organizational key control, making CMK essential for regulated workloads.

Contoso Manufacturing needs CMK to demonstrate key management governance during annual compliance audits. Their security policy requires encryption key rotation every 90 days with automated processes to prevent human error.

### Create a Disk Encryption Set

A Disk Encryption Set acts as the bridge between your encrypted VMs and Azure Key Vault. It references a specific key version, manages the system\-assigned managed identity used for key access, and applies to all disks on VMs configured to use it.

To create a Disk Encryption Set through the Azure portal:

1. Navigate to **Disk Encryption Sets** and select **Create**
2. Choose the subscription and resource group (use the same region as your VMs)
3. Provide a name like `contoso-mfg-des-eastus2`
4. Select **Encryption type**: Choose "Encryption at rest with a customer\-managed key"
5. Under **Key Vault**, select an existing vault or create a new one
6. Select or create an encryption key (RSA 2048\-bit minimum)
7. Enable **Auto\-key rotation** if your compliance policy requires automatic rotation
8. Review and create

After deployment completes, grant the Disk Encryption Set's managed identity access to your Key Vault:

```
## Get the Disk Encryption Set identity
desIdentity=$(az disk-encryption-set show \
  --name contoso-mfg-des-eastus2 \
  --resource-group contoso-security-rg \
  --query [identity.principalId] \
  --output tsv)

## Grant key permissions
az keyvault set-policy \
  --name contoso-mfg-vault \
  --resource-group contoso-security-rg \
  --object-id $desIdentity \
  --key-permissions wrapKey unwrapKey get

```

The Disk Encryption Set now has permission to retrieve and use your customer\-managed key for encryption operations.

### Enable encryption at host on new VMs

When creating a new virtual machine through the Azure portal, enable encryption at host in the **Disks** configuration section:

1. After selecting VM size and image, navigate to the **Disks** tab
2. Check **Enable encryption at host**
3. Under **Key management**, select **Customer\-managed keys**
4. Choose your Disk Encryption Set from the dropdown
5. Complete VM creation

When using Azure CLI, include the `--encryption-at-host` parameter and reference your Disk Encryption Set:

```
az vm create \
  --resource-group contoso-mfg-rg \
  --name plc-mgmt-vm-01 \
  --image Ubuntu2204 \
  --size Standard_D4s_v5 \
  --encryption-at-host true \
  --os-disk-encryption-set /subscriptions/{subscription-id}/resourceGroups/contoso-security-rg/providers/Microsoft.Compute/diskEncryptionSets/contoso-mfg-des-eastus2 \
  --admin-username azureuser \
  --generate-ssh-keys

```

The VM deploys with end\-to\-end encryption active from first boot.

### Enable encryption at host on existing VMs

Existing VMs require a stop/start cycle to enable encryption at host. The VM must be fully deallocated (stopped), not just shut down from within the guest OS.

Through Azure portal:

1. Navigate to the VM and select **Stop** (wait for full deallocation)
2. Go to **Disks** \> **Additional settings**
3. Enable **Encryption at host**
4. Select your Disk Encryption Set under **Key management**
5. Save changes and start the VM

Using Azure CLI:

```
## Stop and deallocate the VM
az vm deallocate \
  --resource-group contoso-mfg-rg \
  --name legacy-factory-vm-03

## Enable encryption at host
az vm update \
  --resource-group contoso-mfg-rg \
  --name legacy-factory-vm-03 \
  --set securityProfile.encryptionAtHost=true

## Update OS disk to use customer-managed key
az vm update \
  --resource-group contoso-mfg-rg \
  --name legacy-factory-vm-03 \
  --set storageProfile.osDisk.managedDisk.diskEncryptionSet.id=/subscriptions/{subscription-id}/resourceGroups/contoso-security-rg/providers/Microsoft.Compute/diskEncryptionSets/contoso-mfg-des-eastus2

## Start the VM
az vm start \
  --resource-group contoso-mfg-rg \
  --name legacy-factory-vm-03

```

For Contoso's production environment, schedule this maintenance during planned outage windows to minimize challenges on manufacturing operations.

### Enforce encryption at host with Azure Policy

Rather than manually configuring each VM, use Azure Policy to automatically enable encryption at host on all new deployments. The built\-in policy definition **Virtual machines should enable encryption at host** operates in DeployIfNotExists (DINE) mode.

Assign this policy at subscription scope:

1. Navigate to **Azure Policy** \> **Assignments**
2. Select **Assign policy**
3. Search for "Virtual machines should enable encryption at host"
4. Set **Effect** to **DeployIfNotExists**
5. Optionally exclude specific resource groups (for example, test environments)
6. Create a remediation task to fix existing noncompliant VMs

The policy automatically enables encryption at host when new VMs deploy, ensuring Contoso maintains compliance as the environment grows without requiring manual verification of each deployment.

### Verify encryption is active

After enabling encryption at host, verify protection is active by checking the VM's security profile:

```
az vm show \
  --resource-group contoso-mfg-rg \
  --name plc-mgmt-vm-01 \
  --query securityProfile.encryptionAtHost

```

A `true` response confirms encryption at host is enabled. For disk\-level verification, check the encryption settings on the OS disk:

```
az disk show \
  --resource-group contoso-mfg-rg \
  --name plc-mgmt-vm-01_OsDisk \
  --query [encryption.type,encryption.diskEncryptionSetId] \
  --output table

```

The output displays `EncryptionAtRestWithCustomerKey` and the Disk Encryption Set resource ID, confirming customer\-managed key protection.

When encryption at host is configured, Contoso's VMs now encrypt temporary disks and caches alongside persistent storage, closing the compliance gap identified in their ISO 27001 audit. For workloads requiring hardware\-level isolation, you next explore confidential disk encryption for confidential virtual machines.

---

## Apply confidential disk encryption to confidential virtual machines

Confidential virtual machines provide hardware\-enforced isolation for workloads processing highly sensitive data. When you enable confidential disk encryption on these VMs, the OS disk encryption key binds to the virtual machine's Trusted Platform Module (vTPM), creating protection that prevents disk access even by privileged administrators with physical hardware access.

### What makes a VM confidential

Azure confidential VMs run on DCasv5\-series and ECasv5\-series hardware with AMD EPYC processors supporting Secure Encrypted Virtualization\-Secure Nested Paging (SEV\-SNP). This technology encrypts VM memory at the hardware level using a key inaccessible to the hypervisor, Azure operators, or other VMs on the same physical host.

Unlike standard VMs where Azure operators can theoretically access memory during maintenance operations, confidential VMs maintain cryptographic isolation enforced by the CPU. The processor generates attestation reports proving the VM runs in a protected environment without tampering or unauthorized access. For Contoso Manufacturing, this protection matters for systems processing trade secrets, proprietary chemical formulas, or intellectual property subject to industrial espionage concerns.

### Security types in Azure

When creating a virtual machine, you select a security type that determines available protection features:

| Security type | Boot integrity | Memory encryption | Disk encryption options |
| --- | --- | --- | --- |
| Standard | None | None | SSE, Encryption at host, ADE |
| Trusted launch | Secure Boot, vTPM, integrity monitoring | None | SSE, Encryption at host, ADE |
| Confidential | Secure Boot, vTPM required | Hardware\-enforced (SEV\-SNP) | Confidential disk encryption, Encryption at host |

Confidential VM is a distinct security type that you must select at VM creation. You can't convert a Standard or Trusted launch VM to a Confidential VM after deployment. This restriction exists because confidential computing requires specific CPU features and firmware configurations initialized during VM provisioning.

### How confidential disk encryption works

Confidential disk encryption binds the OS disk encryption key to the VM's vTPM. The vTPM is a virtualized Trusted Platform Module that stores cryptographic keys in a hardware\-protected environment isolated from the guest operating system and Azure management plane.

When the VM boots, the vTPM releases the disk encryption key only after verifying the boot chain integrity. If an attacker modifies boot components, copies the disk to another VM, or attempts offline access to the encrypted volume, decryption fails because the vTPM key binding validation fails.

This protection differs fundamentally from encryption at host. Encryption at host encrypts data flows between the VM and storage but uses keys accessible to the Azure storage platform. Confidential disk encryption uses keys that only the specific VM instance can access, providing defense against disk theft scenarios including unauthorized copies by privileged insiders or government agencies with legal access to datacenter infrastructure.

### Supported disk types and configuration

Confidential disk encryption applies specifically to the OS disk on confidential VMs. Azure supports several OS disk encryption configurations:

**Confidential OS disk encryption**: The OS disk uses a vTPM\-bound key. This provides the strongest protection but limits some platform features like disk snapshots and some backup solutions that require offline disk access.

**Confidential OS disk encryption with customer\-managed key**: The vTPM\-bound key is itself encrypted with a customer\-managed key stored in Azure Key Vault. This configuration gives you organizational control over the root key while maintaining vTPM binding for the active encryption key.

For data disks attached to confidential VMs, use encryption at host. Confidential disk encryption doesn't extend to data disks, but encryption at host on a confidential VM provides comprehensive protection: hardware memory encryption (SEV\-SNP) \+ vTPM\-bound OS disk \+ encrypted data disks and temp storage.

### Create a confidential VM with confidential disk encryption

Through the Azure portal, confidential disk encryption configuration starts with security type selection:

1. Navigate to **Virtual machines** \> **Create**
2. Select a supported region and a DCasv5 or ECasv5 VM size
3. In the **Basics** tab, under **Security type**, select **Confidential virtual machines**
4. Navigate to the **Disks** tab
5. Under **OS disk**, choose **Confidential disk encryption**
6. Optionally enable **Encryption at host** for data disks and temp storage
7. Select **Customer\-managed keys** if organizational key control is required
8. Choose a Disk Encryption Set linked to your Key Vault
9. Complete VM creation

Using Azure CLI, specify security type and OS disk configuration explicitly:

```
az vm create \
  --resource-group contoso-research-rg \
  --name formula-vault-vm-01 \
  --image Ubuntu2204 \
  --size Standard_DC4as_v5 \
  --security-type ConfidentialVM \
  --os-disk-security-encryption-type DiskWithVMGuestState \
  --enable-vtpm true \
  --enable-secure-boot true \
  --encryption-at-host true \
  --admin-username azureuser \
  --generate-ssh-keys

```

The `DiskWithVMGuestState` value encrypts the OS disk along with the VM Guest State blob (vTPM and UEFI state), providing full confidential OS disk encryption with vTPM binding. Use `VMGuestStateOnly` only when you want a confidential VM without OS disk confidential encryption—it protects only the VM Guest State blob and leaves the OS disk using standard server\-side encryption. Combine `DiskWithVMGuestState` with `--encryption-at-host` to protect both the OS disk (confidential encryption) and data disks and temp storage (encryption at host) comprehensively.

### Key management for confidential disk encryption

When using customer\-managed keys with confidential disk encryption, create a Disk Encryption Set configured for confidential VM use:

```
## Create a Disk Encryption Set for confidential VMs
az disk-encryption-set create \
  --resource-group contoso-security-rg \
  --name contoso-confidential-des \
  --location eastus2 \
  --encryption-type ConfidentialVmEncryptedWithCustomerKey \
  --key-url https://contoso-mfg-vault.vault.azure.net/keys/confidential-vm-key/abc123 \
  --source-vault /subscriptions/{subscription-id}/resourceGroups/contoso-security-rg/providers/Microsoft.KeyVault/vaults/contoso-mfg-vault

```

The `ConfidentialVmEncryptedWithCustomerKey` encryption type indicates this Disk Encryption Set applies to confidential VM OS disks with CMK. After creation, grant the Disk Encryption Set managed identity appropriate Key Vault permissions (Get, WrapKey, UnwrapKey) as described in the previous unit.

### Limitations and considerations

Confidential VMs with confidential disk encryption have specific operational constraints:

**No disk snapshots**: Because the encryption key binds to the vTPM, you can't create snapshots of confidential OS disks using standard Azure snapshot tools. Plan backup strategies using application\-level backups or Azure Backup solutions that support confidential VMs.

**No cross\-VM disk movement**: You can't detach a confidential OS disk from one VM and attach it to another. The vTPM binding ensures only the original VM can decrypt the disk.

**Regional availability**: Confidential VMs require specific hardware. Verify your target Azure region supports DCasv5 or ECasv5 series before planning deployments.

**Size selection**: Confidential VM sizes typically cost more than equivalent standard sizes due to specialized hardware. Balance security requirements against budget constraints.

For Contoso Manufacturing, these limitations require careful workload selection. Systems processing proprietary formulas justify confidential VM costs and operational constraints, while general factory management systems use standard encryption at host.

### When to use confidential disk encryption

Choose confidential disk encryption when your workload requires:

**Regulatory protection against privileged access**: Compliance frameworks like ITAR (International Traffic in Arms Regulations) or specific healthcare regulations can require technical controls preventing cloud provider access to sensitive data.

**Defense against physical theft**: Industries with extremely high\-value intellectual property (pharmaceutical research, defense applications, financial algorithms) benefit from hardware\-enforced protection that remains effective even if encrypted disks fall into adversary possession.

**Attestation requirements**: Applications needing cryptographic proof that they run in an uncompromised environment use the attestation capabilities built into confidential VMs.

**Zero Trust architecture**: Organizations implementing Zero Trust principles apply confidential VMs to protect high\-value assets from both external attackers and insider threats, reducing the trusted perimeter to only the workload itself.

For Contoso's factory systems processing publicly known manufacturing processes, encryption at host provides adequate protection. Confidential disk encryption applies to any future Azure workloads handling research data for proprietary chemical compounds or next\-generation product formulas.

Now that confidential disk encryption is configured, your most sensitive workloads benefit from hardware\-enforced isolation.

---

## Knowledge check

You explored Azure disk encryption options, configured encryption at host with customer\-managed keys, and applied confidential disk encryption to confidential VMs. Check your knowledge of these concepts before moving on.

### Check your knowledge

---

## Summary

In this module, you addressed Contoso Manufacturing's disk encryption compliance gap by implementing encryption at host to protect temporary disks and caches. You compared Azure's four managed disk encryption options, configured customer\-managed keys through Disk Encryption Sets, and explored confidential disk encryption for hardware\-isolated workloads.

### Key decisions for disk encryption

**Encryption at host is the recommended approach for new Azure VMs**. It provides end\-to\-end encryption covering OS disks, data disks, temporary storage, and disk caches—protection that server\-side encryption (SSE) alone can't deliver. For organizations like Contoso with compliance requirements demanding comprehensive data protection at rest, encryption at host directly addresses audit findings around unencrypted temp disks.

**Azure Disk Encryption (ADE) retires on September 15, 2028**. If your environment currently uses BitLocker\-based or DM\-Crypt\-based ADE, begin migration planning immediately. Create a disk snapshot inventory, identify maintenance windows for VM migration to encryption at host, and test workload compatibility with the new encryption architecture before the retirement deadline.

**Customer\-managed keys (CMK) give you organizational control over encryption key lifecycle**. When compliance frameworks like ISO 27001, PCI DSS, or FedRAMP require documented key management procedures, implement CMK through Disk Encryption Sets linked to Azure Key Vault. Enable automatic key rotation to reduce operational burden while maintaining audit evidence of key governance.

**Confidential disk encryption provides vTPM\-bound protection for regulated workloads**. Workloads subject to ITAR, trade secret regulations, or defense against insider threats with privileged access benefit from confidential VMs with OS disk encryption keys bound to the virtual Trusted Platform Module. The hardware\-enforced isolation ensures only the specific VM instance can decrypt its OS disk, defending against disk theft and unauthorized copying scenarios.

**Azure Policy enforces encryption compliance automatically**. Rather than manually verifying encryption settings on every VM, assign built\-in policies like "Virtual machines should enable encryption at host" to audit or automatically remediate noncompliant deployments. This approach scales across growing environments and provides continuous compliance evidence for auditors.

### Learn more

* [Overview of managed disk encryption options](/en-us/azure/virtual-machines/disk-encryption-overview)
* [Encryption at host – end\-to\-end encryption for VM data](/en-us/azure/virtual-machines/disk-encryption)
* [Migrate from Azure Disk Encryption to encryption at host](/en-us/azure/virtual-machines/disk-encryption-migrate)
* [Confidential VM overview](/en-us/azure/confidential-computing/confidential-vm-overview)
* [Customer\-managed keys for Azure managed disks](/en-us/azure/virtual-machines/disk-encryption-customer-managed-keys)
* [Azure Policy built\-in definitions for Azure Virtual Machines](/en-us/azure/virtual-machines/policy-reference)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/implement-disk-encryption-azure-virtual-machines/_

## Fuentes
- [Implement disk encryption for Azure virtual machines](https://learn.microsoft.com/en-us/training/modules/implement-disk-encryption-azure-virtual-machines/?WT.mc_id=api_CatalogApi)
