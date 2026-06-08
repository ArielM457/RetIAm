# Enable and enforce just-in-time VM access

> Curso: Implement security for servers and virtual machines (wwl-server-vm-security) · Seccion: Implement security for servers and virtual machines
> Duracion estimada: 24 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Manufacturing deployed Azure Bastion to provide secure, browser\-based access to factory floor virtual machines, eliminating the need for direct RDP and SSH connections. Despite this deployment, an internal security audit revealed a critical gap: network security group (NSG) rules still permanently allow inbound traffic on RDP port 3389 and SSH port 22 from broad source IP ranges. These open management ports create a persistent attack surface that malicious actors can discover and target. The audit finding requires immediate remediation: eliminate all permanently open management ports across the VM estate.

Microsoft Defender for Cloud's just\-in\-time (JIT) VM access provides the solution. JIT replaces permanent ALLOW rules with on\-demand, time\-limited, IP\-scoped access—management ports remain blocked until a verified user requests access for a specific purpose and duration. Here, you learn how to close Contoso Manufacturing's security gap using JIT VM access.

In this module, you:

* Examine how just\-in\-time VM access reduces the attack surface on management ports
* Enable JIT and configure per\-port access policies on Azure VMs
* Request and approve JIT access and audit access activity
* Enforce JIT adoption across a VM estate using Azure Policy

### Prerequisites

* Defender for Servers Plan 2 enabled on the subscription
* Intermediate\-level familiarity with Azure virtual machines and network security groups

---

## Examine just\-in\-time VM access requirements and VM eligibility

Permanently open management ports in network security groups represent one of the most common attack vectors against cloud infrastructure. Even with strong authentication mechanisms and Azure Bastion deployed for browser\-based access, a Network Security Group (NSG) rule that allows RDP port 3389 or SSH port 22 from any source remains a discoverable entry point. Attackers can target these ports with credential stuffing, brute force attacks, or exploit campaigns. Just\-in\-time VM access closes this vulnerability by replacing persistent ALLOW rules with on\-demand, time\-limited, IP\-scoped rules that grant access only when needed.

| VM State | Management Port Status | Attack Surface |
| --- | --- | --- |
| Before JIT | Permanently open via NSG ALLOW rule | Constant exposure to scanning and attack attempts |
| After JIT enabled | Blocked by default (DENY or no rule) | Port invisible to scanners; zero standing access |
| During JIT session | Temporarily open for specific IP and duration | Minimal exposure window; restricted source |

### How just\-in\-time access works

Just\-in\-time access modifies NSG rules dynamically to create temporary access windows. When you enable JIT on a virtual machine, Defender for Cloud immediately modifies the associated network security group to block the configured management ports. The port remains blocked until a user with appropriate permissions submits an access request.

When an access request is approved, Defender for Cloud inserts a temporary ALLOW rule into the NSG with three critical constraints: the rule permits traffic only from the requester's source IP address (or a specified IP range), only on the requested port, and only for the approved time window (maximum of 24 hours, typically much shorter). After the time window expires, Defender for Cloud automatically removes the temporary ALLOW rule, returning the port to a blocked state.

This lifecycle operates transparently to the user—the only visible change is that connection attempts succeed during the approved time window and fail before or after. With Azure Firewall, JIT modifies the DNAT (Destination Network Address Translation) table instead of NSG rules, but the access control model remains identical.

### Requirements for just\-in\-time access

JIT VM access requires specific infrastructure and licensing components to function correctly. Defender for Servers Plan 2 must be enabled on the subscription—Plan 1 doesn't include JIT capabilities. The virtual machine must be deployed through Azure Resource Manager; Classic deployment model VMs aren't supported and can't be migrated to JIT without redeployment.

The VM must have a network security group associated either directly with the VM's network interface or with the subnet where the VM resides. Alternatively, the VM can be protected by Azure Firewall deployed on the same virtual network—however, that firewall must be configured with Rules (Classic). VMs protected by Azure Firewall using Firewall Policies (managed through Azure Firewall Manager), VMs without an NSG or firewall, aren't supported for JIT access.

### Virtual machine eligibility states

Defender for Cloud categorizes virtual machines into three states visible in the just\-in\-time VM access interface. **Configured** VMs have JIT enabled and show request history and active policies. **Not configured** VMs meet all technical requirements but don't have JIT protection enabled—these machines represent the immediate remediation opportunity for Contoso Manufacturing's audit finding. **Unsupported** VMs can't use JIT due to Classic deployment, missing NSG or firewall association, or JIT being disabled in the security policy.

The Not configured state is the primary focus for security operations teams during JIT deployment. These eligible but unprotected VMs have permanently open management ports and should be prioritized for JIT enablement. The Configured state represents the target end state where management ports are blocked by default and accessible only through approved JIT requests.

### Supported environments

JIT VM access supports Azure virtual machines deployed through Azure Resource Manager across all Azure regions where Defender for Cloud is available. JIT also supports AWS EC2 instances connected through Defender for Cloud's multicloud capabilities, though this integration is currently in preview.

Contoso Manufacturing's factory floor VMs are deployed using Azure Resource Manager templates with network security groups attached at the subnet level. This configuration makes them eligible for JIT protection. The organization has a few legacy Classic VMs that require migration to the Resource Manager deployment model before JIT can be applied—these VMs remain in the Unsupported state until redeployment.

Now that you understand JIT eligibility requirements and the access control model, you're ready to enable JIT on eligible virtual machines and configure port\-specific access policies.

---

## Enable and configure JIT access policies

Enabling just\-in\-time access on eligible virtual machines moves them from the Not configured state to the Configured state, immediately closing the attack surface on management ports. Defender for Cloud provides multiple enablement paths designed for different operational workflows—bulk enablement from the centralized Just\-in\-Time (JIT) interface for large\-scale deployment, or individual VM enablement for targeted protection.

| Enablement Method | Best For | Starting Point |
| --- | --- | --- |
| Defender for Cloud bulk enables | Initial deployment across multiple VMs | Workload protections → Just\-in\-time VM access → Not configured tab |
| Individual VM enables | Single VM or per\-VM workflow | VM → Configuration → Just\-in\-time access |
| Programmatic enable | Automation and infrastructure\-as\-code | PowerShell `Set-AzJitNetworkAccessPolicy` or REST API |

### Enable JIT from Defender for Cloud

The centralized JIT interface in Defender for Cloud provides the most efficient path for protecting multiple virtual machines simultaneously. Navigate to Defender for Cloud, select **Workload protections**, then select **Just\-in\-time VM access**. The interface displays three tabs: Configured, Not configured, and Unsupported. Select the **Not configured** tab to view all eligible VMs that currently lack JIT protection.

Select the virtual machines you want to protect using the checkboxes in the left column. For Contoso Manufacturing's initial deployment, the security team selects all factory floor VMs in the primary production resource group. After selecting VMs, select **Enable JIT on VMs** from the command bar. Defender for Cloud immediately applies the default JIT policy and modifies the associated network security groups to block management ports.

The default policy configuration includes commonly targeted management ports with conservative access parameters:

* **RDP (3389\)**: Maximum request time 3 hours, allowed source IPs: Any, protocol: TCP
* **SSH (22\)**: Maximum request time 3 hours, allowed source IPs: Any, protocol: TCP
* **WinRM (5985\)**: Maximum request time 3 hours, allowed source IPs: Any, protocol: TCP
* **WinRM over HTTPS (5986\)**: Maximum request time 3 hours, allowed source IPs: Any, protocol: TCP

Linux VMs receive JIT protection on port 22, while Windows VMs are protected on ports 3389, 5985, and 5986\. This automatic port selection aligns with the most common remote management protocols. When admins enable JIT from the individual VM Configuration page rather than the Defender for Cloud interface, only port 3389 appears as the Windows default. Other ports like the WinRM ports (5985, 5986\) are included only when enabling through the Defender for Cloud bulk path or programmatically.

### Enable JIT from an individual virtual machine

For operators who manage VMs individually rather than through centralized security operations, the VM Configuration page provides direct JIT enablement. Navigate to the virtual machine in the Azure portal, select **Configuration** from the left navigation menu, then locate the **Just\-in\-time access** section.

Select **Enable just\-in\-time**. Defender for Cloud applies the default policy with the same port configurations described. This approach works well for newly deployed VMs or when JIT enablement is part of a VM\-specific security review process.

### Customize the JIT policy

The default JIT policy provides broad protection but allows access from any source IP address, which can’t align with organizational security requirements. Contoso Manufacturing's security standards require restricting JIT access to connections originating from the corporate office IP range (203\.0\.113\.0/24\) and the VPN concentrator IP range (198\.51\.100\.0/24\).

To customize a JIT policy, navigate to Defender for Cloud → **Just\-in\-time VM access** → **Configured** tab. Right\-click the virtual machine you want to modify and select **Edit**. The policy editor displays the current port configurations with options to add, remove, or modify rules.

To restrict source IP addresses, select the port row and modify the **Allowed source IPs** field. Replace **Any** with a CIDR notation range such as `203.0.113.0/24` or a comma\-separated list of ranges: `203.0.113.0/24,198.51.100.0/24`. This change ensures that JIT access requests succeed only when the requester's source IP falls within the approved corporate network ranges.

To add a custom port, select **Add** and specify the port number, protocol (TCP, UDP, or Any), allowed source IPs, and maximum request time. For example, Contoso Manufacturing adds port 5432 (PostgreSQL) for database administration access with a one\-hour maximum window and source IP restricted to the database team's subnet.

To remove a port from JIT protection, uncheck the port in the policy editor or delete the rule entirely. Removing a port from the JIT policy doesn't restore the previous NSG rule—the port remains blocked unless you manually create an NSG ALLOW rule.

The maximum request time parameter controls the longest duration a user can request for a single JIT session. Setting this value to 1 hour instead of the default 3 hours reduces the exposure window for each access grant. Contoso Manufacturing uses 1\-hour windows for production VMs and 3\-hour windows for development and testing environments where longer sessions support troubleshooting workflows.

### Enable JIT programmatically

Automation pipelines and infrastructure\-as\-code workflows can enable and configure JIT policies using PowerShell or REST API. The PowerShell approach uses the `Set-AzJitNetworkAccessPolicy` cmdlet:

```
$JitPolicy = (@{
    id="/subscriptions/SUBSCRIPTION_ID/resourceGroups/RESOURCE_GROUP/providers/Microsoft.Compute/virtualMachines/VM_NAME";
    ports=(@{
        number=22;
        protocol="*";
        allowedSourceAddressPrefixes=@("203.0.113.0/24");
        maxRequestAccessDuration="PT1H"
    })
})

$JitPolicyArr=@($JitPolicy)
Set-AzJitNetworkAccessPolicy -ResourceGroupName "RESOURCE_GROUP" -Location "eastus" -Kind "Basic" -Name "JIT_POLICY_NAME" -VirtualMachine $JitPolicyArr

```

This script creates a JIT policy protecting SSH port 22 with a one\-hour maximum window and source IP restricted to the Contoso Manufacturing office range. The `maxRequestAccessDuration` parameter uses ISO 8601 duration format (PT1H \= 1 hour).

### What happens after JIT is enabled

Immediately after JIT enablement, Defender for Cloud modifies the network security group associated with the virtual machine. Any existing NSG rules that allow inbound traffic on the JIT\-protected ports are overridden or replaced with DENY rules. The management ports become inaccessible from all sources, including previously permitted IP ranges.

Users who attempt to connect to the VM using RDP or SSH after JIT enablement receive connection timeout or connection refused errors until they submit a JIT access request. This immediate blocking behavior closes the attack surface instantly, which is why Contoso Manufacturing's security team coordinates JIT deployment with operations teams to ensure administrators understand the new access request workflow.

Note

The combined length of the JIT policy name and virtual machine name can't exceed 56 characters. If you encounter provisioning errors during JIT enablement, verify that resource names fall within this constraint and shorten names if necessary.

Now that you understand how to enable JIT and customize port policies, you're ready to submit access requests and audit JIT activity across your VM estate.

---

## Request Just\-in\-time (JIT) access and audit access activity

After Just\-in\-Time (JIT) is enabled on a virtual machine, connecting to the VM requires submitting an access request that specifies which ports to open, the source IP address, and the duration of access. Defender for Cloud evaluates the request against the configured JIT policy and, if approved, creates a temporary NSG ALLOW rule with the specified parameters. This request\-and\-grant workflow ensures that management ports remain closed except during verified administrative sessions.

| Request Parameter | Purpose | Example Value |
| --- | --- | --- |
| Ports | Which management ports to open | 3389 (RDP), 22 (SSH) |
| Source IP | IP address or range allowed to connect | 203\.0\.113\.45 or 203\.0\.113\.0/24 |
| Time window | How long the port remains open | One hour, 3 hours (up to 24 hours max) |

### Request JIT access from Defender for Cloud

The centralized JIT interface provides a streamlined workflow for requesting access to protected virtual machines. Navigate to Defender for Cloud → **Workload protections** → **Just\-in\-time VM access** → **Configured** tab. This view displays all VMs with active JIT policies.

Select the virtual machine you want to access and select **Request access** from the command bar. The request form displays the ports configured in the JIT policy with toggles to enable or disable each port. Select the ports you need—for a Windows VM, you typically select only port 3389 (RDP); for Linux, only port 22 (SSH).

The **My IP** field autopopulates with your current public IP address as detected by Azure. This value works correctly for direct internet connections but requires adjustment if you connect through a corporate proxy or VPN. For Contoso Manufacturing administrators working from the office, the source IP must be set to the office network's public IP range (203\.0\.113\.0/24\) rather than the individual workstation's private IP address.

The **Time range** field specifies how long the port remains open. Select a duration appropriate for your task—one hour for a quick configuration check, 3 hours for troubleshooting sessions. The maximum value is constrained by the JIT policy's `maxRequestAccessDuration` parameter. After setting all parameters, select **Open ports**.

Defender for Cloud creates the temporary NSG ALLOW rule within seconds. The connection details panel updates to show the open ports and the approved time window. You can now connect to the VM using RDP, SSH, or the specified protocol. The connection succeeds only from the approved source IP and only until the time window expires.

### Request JIT access from the VMConnect page

For operators who start their workflow from the virtual machine view rather than the Defender for Cloud security center, the VMConnect page provides an integrated JIT request interface. Navigate to the virtual machine in the Azure portal. Next select **Connect** from the command bar, then choose your connection method (RDP, SSH, or Bastion).

If the VM has JIT enabled, the connection page displays a **Request access** option before showing connection details. Select **Request access**, specify the time window and source IP (ports are preselected based on the connection type), then select **Request**. After Defender for Cloud grants access, the connection details page updates with the RDP file download link or SSH connection string.

This workflow reduces friction for administrators who manage VMs individually and expect to connect directly from the VM's overview page. The experience feels similar to non\-JIT VMs, with the access request step inserted transparently into the connection workflow.

### Request JIT access programmatically

Automation scripts and deployment pipelines can request JIT access using the `Start-AzJitNetworkAccessPolicy` PowerShell cmdlet. This capability supports scenarios where administrative tasks run on a scheduled basis or require scripted access:

```
Start-AzJitNetworkAccessPolicy `
    -ResourceGroupName "contoso-factory-rg" `
    -Location "eastus" `
    -Name "JIT_POLICY_NAME" `
    -VirtualMachine @(@{
        id="/subscriptions/SUBSCRIPTION_ID/resourceGroups/contoso-factory-rg/providers/Microsoft.Compute/virtualMachines/factory-vm-01";
        ports=@(@{
            number=22;
            allowedSourceAddressPrefix=@("203.0.113.50");
            endTimeUtc=(Get-Date).AddHours(1).ToUniversalTime()
        })
    })

```

This script requests SSH access (port 22\) from source IP 203\.0\.113\.50 for a one\-hour window. The `endTimeUtc` parameter specifies when the access expires using UTC time. Automation accounts running this script must have the appropriate Azure RBAC permissions to request JIT access (Security Reader role at minimum, or a custom role with `Microsoft.Security/locations/jitNetworkAccessPolicies/initiate/action` permission).

### Audit JIT access activity

Each JIT access request (approval, and port opening event) is recorded in the Azure Activity Log, providing a complete audit trail for security reviews and compliance reporting. Navigate to the virtual machine or resource group, select **Activity log** from the left navigation, then filter for **Resource type: JitNetworkAccessPolicy**.

The Activity Log displays entries for each JIT event:

* **Initiate JIT Network Access**: User submitted a JIT access request
* **Update JIT Network Access Policy**: Policy configuration was modified
* **Delete JIT Network Access Policy**: JIT was disabled on the VM

Each entry includes the caller identity (who requested access), timestamp, source IP address, ports opened, and the approved time window. For Contoso Manufacturing's compliance requirements, this audit data feeds into the quarterly security review process, where the security team validates that JIT access patterns align with approved maintenance schedules.

Defender for Cloud also provides a connection history view directly in the JIT interface. Navigate to **Just\-in\-time VM access** → **Configured** tab, select a virtual machine, and review the **Request history** section. This view summarizes recent access requests with approval status, requester identity, and time windows, providing quick visibility into access patterns without navigating to the Activity Log.

### Enforce JIT adoption with Azure Policy

Manual JIT enablement addresses existing virtual machines but doesn't prevent new VMs from being deployed with permanently open management ports. Azure Policy provides the enforcement mechanism to drive organization\-wide JIT adoption and identify noncompliant resources at scale.

The built\-in policy **"Management ports of virtual machines should be protected with just\-in\-time network access control"** audits all virtual machines in the assigned scope and identifies VMs that have management ports open without JIT protection. This policy uses the AuditIfNotExists effect—it doesn't automatically enable JIT, but it surfaces noncompliant resources in the Policy compliance dashboard.

To assign this policy, navigate to **Azure Policy** → **Definitions**, search for "just\-in\-time network access," and select the built\-in policy. Select **Assign** and choose the scope—Contoso Manufacturing assigns the policy at the management group level to cover all factory subscriptions automatically, including future subscriptions added to the hierarchy.

After assignment, Azure Policy evaluates all VMs in scope during the next evaluation cycle (typically within 30 minutes, with full scans every 24 hours). Navigate to **Azure Policy** → **Compliance** to view the compliance state. Noncompliant VMs appear in the resource list with details about which management ports are open without JIT protection.

The security operations team uses this compliance report to prioritize JIT enablement. Each week, the team exports the noncompliant VM list, groups VMs by resource group and owner, and sends remediation requests to the responsible teams. This workflow ensures that JIT adoption remains current as new VMs are deployed, with the policy assignment acting as a continuous control rather than a one\-time deployment effort.

---

## Knowledge check

You configured just\-in\-time VM access for Contoso Manufacturing's factory floor virtual machines, replacing permanently open management ports with on\-demand, time\-limited access. Test your understanding of JIT configuration and access workflows with the following questions.

### Check your knowledge

---

## Summary

Contoso Manufacturing eliminated the security audit finding by implementing just\-in\-time VM access across the factory floor VM estate. Permanently open management ports in network security groups—the original attack surface—are now replaced with on\-demand, time\-limited, IP\-scoped ALLOW rules that grant access only during verified administrative sessions.

You accomplished the following objectives in this module:

* **Examined JIT access requirements**: JIT requires Defender for Servers Plan 2, Azure Resource Manager–deployed VMs, and an associated NSG or Azure Firewall. VMs in the Not configured state represent the remediation opportunity.
* **Enabled and configured JIT policies**: The default policy protects RDP (3389\), SSH (22\), and WinRM (5985/5986\) with three\-hour maximum windows and any source IP. Customizing the policy to restrict source IPs to corporate network ranges significantly reduces the exposure window.
* **Requested access and audited activity**: JIT access requests specify ports, source IP, and time window. Azure Activity Log captures all JIT events, providing a complete audit trail for compliance and security review.
* **Enforced JIT adoption with Azure Policy**: The built\-in audit policy identifies VMs with open management ports and no JIT protection, enabling continuous compliance monitoring as new VMs are deployed.

### Key decisions

* **JIT replaces standing access with on\-demand access**: Management ports remain blocked until a user requests access for a specific purpose and duration.
* **Default ports include 22, 3389, 5985, 5986**: Customize the policy to add application\-specific ports or remove unnecessary ports.
* **Restrict source IPs for tighter control**: Replace "Any" with corporate IP ranges to limit access to trusted networks.
* **Azure Activity Log provides the audit trail**: All JIT requests, approvals, and policy changes are recorded for compliance reporting.
* **Azure Policy drives scale adoption**: The audit policy identifies noncompliant VMs, enabling continuous enforcement as the VM estate grows.

### Learn more

* [Just\-in\-time VM access overview](/en-us/azure/defender-for-cloud/just-in-time-access-overview)
* [Enable just\-in\-time access](/en-us/azure/defender-for-cloud/enable-just-in-time-access)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/enable-enforce-just-in-time-vm-access/_

## Fuentes
- [Enable and enforce just-in-time VM access](https://learn.microsoft.com/en-us/training/modules/enable-enforce-just-in-time-vm-access/?WT.mc_id=api_CatalogApi)
