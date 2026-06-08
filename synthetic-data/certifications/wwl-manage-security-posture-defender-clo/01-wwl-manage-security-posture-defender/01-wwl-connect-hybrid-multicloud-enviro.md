# Connect hybrid and multicloud environments to Microsoft Defender for Cloud

> Curso: Manage security posture by using Microsoft Defender for Cloud (wwl-manage-security-posture-defender-cloud) · Seccion: Manage security posture by using Microsoft Defender for Cloud
> Duracion estimada: 52 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso's security team can see everything happening inside Azure. Virtual machines generate alerts. Misconfigurations surface as recommendations. The regulatory compliance dashboard tracks Azure resources against the Microsoft Cloud Security Benchmark. But outside the Azure boundary—in the Amazon Web Services (AWS) EC2 instances running production workloads, the Google Cloud Platform (GCP) Compute Engine virtual machines hosting development environments, and the on\-premises Windows and Linux servers powering the data centers—Defender for Cloud sees nothing. No recommendations surface. No secure score reflects those environments. No Cloud Workload Protection Platform (CWPP) plan covers those machines. The Chief Information Security Officer (CISO) mandated unified visibility and protection before the next compliance audit.

This module shows you how to close that gap. You connect Contoso's on\-premises servers, AWS accounts, and GCP projects to Microsoft Defender for Cloud using native connectors and Azure Arc–enabled servers. Then you extend Cloud Security Posture Management (CSPM) and CWPP protection across a unified hybrid and multicloud estate.

In this module, you:

* Explain the multicloud connectivity model in Defender for Cloud, including how federated authentication works for AWS and GCP connectors
* Plan a connector strategy for hybrid and multicloud environments, including scope, scan interval, and required permissions per environment type
* Connect on\-premises machines to Defender for Cloud using Azure Arc–enabled servers
* Connect AWS accounts to Defender for Cloud using the native cloud connector and CloudFormation template
* Connect GCP projects to Defender for Cloud using the native cloud connector and GCloud deployment script
* Verify multicloud connectivity health and confirm CSPM and CWPP coverage surfaces across connected environments

---

## Explore the Defender for Cloud multicloud connectivity model

Before you connect environments, understand the two distinct security coverage layers that Defender for Cloud delivers across connected environments, and how the authentication architecture makes multicloud connectivity secure without exposing credentials.

### Explore two coverage layers

Defender for Cloud provides two layers of coverage for non\-Azure environments: **Cloud Security Posture Management (CSPM)** and **Cloud Workload Protection Platform (CWPP)**. These layers work differently and require different onboarding steps.

**CSPM is agentless** \- When you create a connector for an AWS account or GCP project, Defender for Cloud reads configuration data from those environments through cloud provider APIs. No agent installation is required on individual resources. You get security recommendations, asset inventory, and compliance posture within four to six hours of connector creation—the time required for the first scan cycle to complete.

The Security Posture Management plan that enables CSPM can't be turned off in a connector. It's always active. This design ensures that baseline posture visibility is guaranteed for every connected environment, regardless of which CWPP plans you choose. For Contoso, the moment the AWS and GCP connectors are created, the security team gains visibility into misconfigurations, compliance gaps, and asset inventory. The visibility starts even before Arc agents are deployed on EC2 instances or Compute Engine VMs.

**CWPP requires Azure Arc** \- CWPP plans—such as Defender for Servers, Defender for Containers, and Defender for Databases—provide active threat detection and runtime protection. These plans need access to the machine or workload running in the non\-Azure environment. For virtual machines (EC2 instances, GCP Compute Engine VMs, and on\-premises servers), this means installing the **Azure Connected Machine agent**, which Arc\-enables the machine and registers it as an Azure resource.

Once a machine is Arc\-enabled, it appears in Defender for Cloud's inventory alongside native Azure VMs. Any Defender plan enabled on the Azure subscription extends coverage to that machine. This two\-step model—connector for posture, Arc for protection—is the foundation of how Defender for Cloud treats non\-Azure workloads.

### Review capabilities available after connecting

A successful connector onboarding unlocks several security capabilities for the connected environment:

* **Unified asset inventory**: AWS and GCP resources appear in Defender for Cloud's Inventory alongside Azure resources, each tagged with their source cloud provider.
* **Cross\-cloud secure score contribution**: Security recommendations from AWS and GCP environments contribute to your Defender for Cloud secure score, giving a unified posture view across all clouds.
* **CSPM recommendations per environment**: Configuration findings for AWS and GCP resources surface in the Recommendations page, filterable by environment.
* **Auto\-assigned compliance standards**: When you create an AWS connector, the **AWS Foundational Security Best Practices** standard is automatically assigned to the subscription containing that connector. For GCP, the **GCP Default** benchmark is assigned. The results of benchmarks appear in the Regulatory Compliance dashboard without any manual configuration.
* **CWPP plan availability**: Defender plans you select during connector creation—Defender for Servers, Defender for Containers, Defender for Databases—become available for resources in the connected environment. Prerequisites per plan are covered in later units.
* **AI workload visibility**: If you enable the AI Security Posture Management (AI SPM) feature of Defender CSPM, Defender for Cloud surfaces security recommendations for AI workloads in connected AWS accounts and GCP projects. The protections include Amazon Sage Maker and Google Vertex AI deployments.

### AWS authentication architecture: federated trust and no stored secrets

When Defender for Cloud communicates with your AWS account, it never stores long\-lived credentials—no access keys, no stored secrets. Instead, it uses **federated trust with short\-lived credentials** through a cross\-cloud trust relationship between Microsoft Entra ID and AWS Identity and Access Management (IAM).

During AWS onboarding, the CloudFormation template you download and run in your AWS account creates two authentication resources:

* An **OpenID Connect (OIDC) identity provider** bound to a Microsoft\-managed Microsoft Entra application
* One or more **IAM roles** that Defender for Cloud is authorized to assume through web identity federation

The authentication flow works as follows. Defender for Cloud requests a token from Microsoft Entra ID. It presents this token to AWS Security Token Service (STS), which validates it against the trust conditions defined in the IAM role. If all conditions are met, AWS STS returns short\-lived credentials valid only during that scan operation. Defender for Cloud uses these temporary credentials to read asset configuration data and never stores them.

AWS performs audience, signature, thumbprint, and role\-level checks before issuing credentials, ensuring only the specific Microsoft\-managed application can assume the connector role.

This architecture means that even if an attacker gained access to the Azure environment, there are no stored AWS credentials to exfiltrate. The trust is used by the specific Microsoft\-managed application, during a valid authentication transaction.

The IAM permissions granted to these roles depend on which Defender plans you select. CSPM requires read\-only permissions across AWS services. Adding CWPP plans such as Defender for Servers adds permissions needed to manage Arc agent deployment and AWS Systems Manager (SSM) access on EC2 instances.

### GCP authentication architecture: workload identity federation

For GCP, Defender for Cloud uses **workload identity federation and service account impersonation** \- a GCP\-native approach to federated authentication. Like AWS, this model stores no private keys or long\-lived credentials in Azure.

During GCP onboarding, the GCloud script you run in your GCP project creates the following resources:

* A **workload identity pool**: the container for external identity providers
* **Workload identity providers** (one per enabled Defender plan): each configured to trust tokens from Microsoft Entra ID
* **Service accounts** with scoped project\-level policy bindings: the GCP identities that Defender for Cloud impersonates

When Defender for Cloud scans a GCP project, it exchanges a Microsoft Entra token with Google Cloud Security Token Service (STS). Then STS validates it against the workload identity provider configuration and returns a short\-lived Google STS token. Defender for Cloud uses that token to impersonate the service account and read GCP resource configuration—no private keys stored in Azure.

Because the service account's policy bindings are scoped to the connected project (or organization), Defender for Cloud can only access the resources you explicitly onboarded. Individual plans get separate workload identity providers, so the permissions granted to each plan are independently scoped and auditable.

---

## Plan a connector strategy for hybrid and multicloud environments

With a clear picture of how Defender for Cloud covers multicloud environments, you're ready to plan a connector strategy. Before you create any connectors, make three key decisions for each cloud environment: the scope of each connector, the scan interval, and the permission model. These decisions affect operational overhead, coverage completeness, API call volume, and audit trail quality.

### Plan your AWS connector

For AWS, **one connector corresponds to one AWS account**. You have two scope options depending on your organizational structure.

#### Select AWS connector scope

An **organization\-level connector** connects your AWS management account. Defender for Cloud uses AWS StackSets to automatically create connectors for all child accounts under that management account—including new accounts added later. This is the right choice for central security teams that need consistent coverage across accounts they can’t directly manage, without creating and maintaining dozens of individual connectors.

An **account\-level connector** covers a single AWS account and gives granular control over scan intervals, plan selection, and permission configuration for that account. The account\-level approach is appropriate when:

* Security requirements differ meaningfully across accounts (production vs. dev/test)
* You can't yet onboard the full organization due to ownership or approval constraints
* You need to start with a limited pilot before rolling out organization\-wide

#### Define AWS scan interval

Defender for Cloud offers four scan intervals for AWS connectors: **4, 6, 12, or 24 hours**. The interval controls how frequently Defender for Cloud polls AWS APIs for resource configuration changes.

A shorter interval catches configuration drift faster—important for environments where resources are frequently created, modified, or deleted. However, scan interval only controls the *configurable* data collectors. Several AWS data collectors run on **fixed intervals** regardless of your setting:

| Fixed scan interval | AWS data collected |
| --- | --- |
| Every 1 hour | EC2 instances, ECR images, ECR repositories, S3 buckets, EKS clusters, Auto Scaling groups |
| Every 12 hours | IAM policy versions, IAM entities for policies, S3 bucket policies, S3 access control lists, S3 replication configuration |

EC2 instances—the workloads most commonly protected by Defender for Servers—refresh every hour regardless of the interval you set. IAM configuration data, which feeds Cloud Security Posture Management (CSPM) recommendations on over\-permissive roles, refreshes every 12 hours. For most production environments, a **4\-hour scan interval** is the right starting point.

#### Explore AWS permission requirements

The IAM permissions Defender for Cloud needs in your AWS environment depends on which Defender plans you enable.

**CSPM** (always required) uses read\-only API calls to assess posture. It needs read\-only permissions across services like EC2, IAM, S3, RDS, and CloudTrail—no write access, no changes to your environment.

**Cloud Workload Protection Platform (CWPP) plans** require extra permissions:

* **Defender for Servers** needs permissions to interact with AWS Systems Manager (SSM) to validate and trigger Arc agent installation on EC2 instances
* **Defender for Containers** needs permissions to create and manage CloudWatch log groups, SQS queues, Kinesis Data Fire Hose delivery streams, and S3 buckets in each monitored region

During connector creation, you choose between **default access** (current and anticipated future permissions) and **least privilege access** (only what your selected plans need today). For production environments, start with least privilege. If you add plans later, regenerate and redeploy the CloudFormation template with updated plan selections.

#### Configure AWS Arc automatic deployment

For AWS EC2 instances, the native cloud connector can **auto\-provision Azure Arc** as part of Defender for Servers activation. Defender for Cloud uses AWS Systems Manager (SSM) to install the Azure Connected Machine agent on discovered EC2 instances—no manual deployment needed at scale. For Contoso, with hundreds of EC2 instances across multiple AWS regions, autoprovisioning eliminates manual agent deployment while ensuring CWPP coverage extends to every new instance as it launches.

---

### Plan your GCP connector

For GCP, **one connector can cover a single project or an entire GCP organization**. The model is a more flexible model than AWS.

#### Choose GCP connector scope

An **organization\-level connector** covers all current and future projects within the GCP organization—individual projects don't require separate connectors. New projects added to the organization are covered automatically.

A **project\-level connector** covers a single GCP project and gives granular control over scan intervals, plan selection, and permission configuration for that project. Use when:

* Security requirements differ meaningfully across projects (production vs. dev/test)
* You can't yet onboard the full organization due to ownership or approval constraints
* You need to start with a scoped pilot

#### Configure GCP scan interval

Defender for Cloud offers the same four scan intervals for GCP connectors: **4, 6, 12, or 24 hours**. GCP Compute Engine VMs and Container clusters refresh hourly regardless of the configured interval—the same fixed\-interval pattern as EC2 on AWS. For most production environments, use a **4\-hour** starting interval.

#### Explore GCP permission requirements

**CSPM** (always required) uses read\-only access to Compute, Storage, IAM, and BigQuery APIs—no write access, no changes to your GCP environment.

**CWPP plans** require extra permissions:

* **Defender for Servers** needs permissions to interact with Compute Engine metadata and Google Cloud OS Config to validate and trigger Arc agent installation on Compute Engine VMs

During connector creation, choose between **default access** and **least privilege access**. The GCloud script generated by the portal is customized to the plans you select and the permission type you choose. For production environments, use least privilege. If you add plans later, rerun the updated GCloud script to add the new permissions.

Note

If this GCP connector already uses **Least privilege access** and you want to enable AI Security Posture Management (AI SPM) for AI workload visibility—including Google Vertex AI—the existing service account bindings don't include the required permissions. Rerun the updated GCloud script to add them.

#### Configure GCP Arc autoprovisioning

For GCP Compute Engine VMs, the native cloud connector can also **auto\-provision Azure Arc** as part of Defender for Servers activation. Defender for Cloud uses Google Cloud OS Config to install the Azure Connected Machine agent on discovered Compute Engine VMs—the same operational advantage as AWS, without manual deployment at scale.

---

### Plan connector decisions and prioritization

With the AWS and GCP connector models in mind, a few decisions apply across both environments.

**On\-premises machines require a different path.** Unlike EC2 and Compute Engine VMs, on\-premises servers have no autoprovisioning capability. You must manually deploy the Azure Connected Machine agent on each server—either one at a time using the portal\-generated onboarding script. Or you can deploy at scale using a service principal with your organization's management tooling such as Group Policy, Ansible, or Microsoft Configuration Manager. This manual deployment step applies regardless of how many machines you have, so factor the deployment effort into your planning timeline before onboarding large on\-premises estates.

**Prioritize by attack surface risk.** Before creating connectors, identify which environments carry the greatest unmonitored risk. Internet\-facing EC2 instances, production databases on RDS, GKE clusters running multitenant applications, and storage buckets holding sensitive data are common high\-risk starting points. Start with connectors for those environments to get recommendations and secure score contribution as quickly as possible.

**Contoso's recommended path.** For Contoso's environment—defined production and sandbox AWS accounts and multiple GCP projects under a single GCP organization—use organization\-level connectors for each provider when organizational buy\-in exists. For an initial pilot, start with account\-level connectors for the highest\-risk production environments.

---

## Connect on\-premises machines using Azure Arc

On\-premises servers present a unique challenge in Defender for Cloud's multicloud strategy: unlike AWS or GCP, where native cloud connectors read resource configurations directly from cloud provider APIs, on\-premises machines have no API surface that Defender for Cloud can call. The solution is **Azure Arc–enabled servers**—a technology that installs a lightweight Azure Connected Machine agent on each machine, registering it as a native Azure resource with an Azure Resource ID, and making it manageable and monitorable through Azure services.

### How Azure Arc\-enabled servers work with Defender for Cloud

Once a machine is Arc\-enabled, it appears in Defender for Cloud's Inventory alongside native Azure VMs. The machine gets the same posture assessment, recommendation generation, and CWPP plan coverage as an Azure VM—because from Defender for Cloud's perspective, *it's* an Azure resource.

An Arc\-enabled server running Windows Server or Linux:

* Contributes to the subscription's secure score
* Receives CSPM recommendations for OS\-level configuration findings
* Becomes eligible for Defender for Servers protection when the plan is enabled on the subscription
* Appears in the Microsoft Defender XDR unified asset inventory alongside Azure VMs, AWS EC2 instances, and GCP Compute Engine VMs

The Azure Connected Machine agent sends heartbeats, configuration data, and security signals to Azure. For production environments with strict network controls, the agent supports proxy configuration and private endpoint communication through Azure Arc private link scope. For required endpoints and TLS inspection guidance, see the NOTE at the end of this unit.

### Choose a deployment path

Two deployment paths exist for Arc\-enabling on\-premises machines, suited to different deployment scales.

#### Single\-machine deployment

For individual machines or small\-scale pilots, use the Azure portal to generate a deployment script:

1. In Defender for Cloud, select **Environment settings** \> **Add environment** \> **On\-premises servers**.
2. Alternatively, go to **Azure Arc** \> **Azure Arc resources** \> **Machines** \> **Add/Create** \> **Add a single server**.
3. Follow the prompts to select the subscription, resource group, and operating system type.
4. The portal generates a PowerShell script (Windows) or Shell script (Linux).
5. Run the script on the target machine with local administrator privileges.

The script downloads the Connected Machine agent installer, installs the agent, and registers the machine with Azure. The script is valid for a short time window—typically 24 hours—so run it promptly after generation.

#### At\-scale deployment

For fleets of on\-premises servers, use a **service principal** to automate agent installation across machines without interactive credentials:

1. Create a service principal in Microsoft Entra ID and assign it the **Azure Connected Machine Onboarding** role.
2. Generate a deployment script from the Azure Arc portal that uses service principal authentication.
3. Distribute the script through your existing management tooling: Group Policy, System Center Configuration Manager (SCCM), Ansible, or any similar orchestration tool.
4. The script installs the Connected Machine agent on each machine and registers it using the service principal credentials.

The service principal approach means each machine installs the agent independently, with no manual intervention required per machine. You set the target subscription and resource group once in the script configuration, and all machines register there.

Tip

Create dedicated resource groups for Arc\-enabled on\-premises servers that mirror your physical location structure. For example, use a resource group named `rg-arc-datacenter-eastus` for machines in your East US data center. Dedicated resource groups let you apply Azure Policy and Defender plans at the resource group level with precision.

Note

**Azure VMware Solution (AVS) machines** follow the same Arc onboarding path. AVS machines don't have an Azure Resource ID by default and aren't automatically discovered by Defender for Cloud. Deploy the Connected Machine agent on each AVS machine using the single\-machine or at\-scale approach.

### Retire monitoring agent: Arc is now the required path

A critical change affects on\-premises server onboarding: the **Microsoft Monitoring Agent (MMA)**, also known as the Log Analytics agent, retired in August 2024\. Any Defender for Cloud guidance that references MMA\-based onboarding for on\-premises servers is outdated. The current and supported path is Azure Arc.

* **Defender for Servers Plan 1**: Direct Microsoft Defender for Endpoint (MDE) onboarding provides some Plan 1 capabilities—including threat detection and vulnerability assessment—without Arc.
* **Defender for Servers Plan 2**: Requires Azure Arc for full feature availability, including just\-in\-time (JIT) VM access, file integrity monitoring, agentless scanning, and 500\-MB daily free log ingestion per server.

For Contoso's compliance audit requirements, Plan 2 features are essential. Arc is required for on\-premises servers that need full CWPP coverage.

Tip

After deploying the Arc agent, verify connectivity by opening **Inventory** in Defender for Cloud and filtering for Arc\-enabled server resources. If a machine shows no Defender for Servers coverage, confirm that Defender for Servers Plan 1 or Plan 2 is active on the target subscription.

Note

The Connected Machine agent requires outbound HTTPS (port 443\) to `management.azure.com`, `login.microsoftonline.com`, `guestconfiguration.azure.com`, and `*.his.arc.azure.com`. In environments with TLS inspection, exclude these endpoints—the agent uses its own certificate store.

---

## Connect AWS accounts to Defender for Cloud

With on\-premises servers Arc\-enabled and reporting to Defender for Cloud, you turn to Contoso's AWS environment. The native AWS connector uses API\-based integration—you don't need to deploy agents on AWS infrastructure to activate CSPM coverage. The CloudFormation template that Defender for Cloud generates handles all authentication resource creation automatically, giving you a secure, federated connection within minutes.

### Plan the AWS connector

Confirm these prerequisites before starting:

* You have **Contributor or Owner** permissions on the Azure subscription where the connector is created.
* **Microsoft Defender for Cloud** is enabled on that subscription.
* You have **administrator access** to the AWS account being connected.
* If you plan to enable Cloud Infrastructure Entitlement Management (CIEM) as part of Defender CSPM, you need the **Application Administrator** or **Cloud Application Administrator** role in Microsoft Entra ID.

Important

The AWS connector isn't available on the national government clouds: Azure Government and Microsoft Azure operated by 21Vianet. If you operate in those cloud environments, the AWS native connector isn't supported.

If your AWS account is already connected to **Microsoft Sentinel**, review the Microsoft documentation on connecting Sentinel\-connected AWS accounts to Defender for Cloud before proceeding. Simultaneous connections can cause deployment or ingestion conflicts that require configuration changes to resolve.

### Create the AWS connector

1. In the Azure portal, open **Microsoft Defender for Cloud** and select **Environment settings** from the left menu.
2. Select **Add environment** \> **Amazon Web Services**.
3. On the **Account details** tab, enter:
	* **Connector name**: a descriptive name, for example, `contoso-aws-prod`
	* **Subscription**: the Azure subscription that owns this connector resource
	* **Resource group**: an existing or new resource group for the connector
	* **Location**: the Azure region where connector metadata is stored
	* **AWS account ID**: your 12\-digit AWS account number
4. Select **AWS regions** to monitor using the dropdown. Defender for Cloud makes API calls only to the regions you select. Resources in deselected regions receive no coverage—misconfigurations and vulnerable resources in those regions remain invisible. Select all regions where Contoso runs production workloads.
5. Set the **Scan interval**: choose 4, 6, 12, or 24 hours. For initial deployment, 4 hours provide the fastest first scan results.
6. Select **Next: Select plans**.

#### Select Defender plans

On the **Select plans** tab, choose the Defender plans to enable for the AWS account.

**Defender CSPM** is always on and can't be disabled. It provides agentless posture assessment across all selected AWS regions.

Optional CWPP plans to consider for Contoso's AWS environment:

| Plan | What it protects | Azure Arc required |
| --- | --- | --- |
| Defender for Servers | EC2 instances | Yes (autoprovisioned) |
| Defender for Containers | EKS clusters | No |
| Defender for SQL on EC2 | SQL Server on EC2 and RDS Custom | Yes |
| Defender for Databases (RDS) | RDS with open\-source engines | No |

Enable Defender for Servers to extend CWPP coverage to Contoso's EC2 workloads. The CloudFormation template that the portal generates includes the SSM\-related permissions needed for Arc agent autoprovisioning on EC2 instances.

Note

The plans you select determine what IAM permissions the CloudFormation template includes. Adding or removing plans after template generation requires downloading a new template and updating the CloudFormation stack.

Note

If this AWS account is already connected with **Least privilege access** and you want to add AI Security Posture Management (AI SPM) for AI workload visibility, the existing connector doesn't automatically receive the required permissions. Download an updated CloudFormation template with AI SPM permissions included and redeploy it as a stack update.

#### Configure access

On the **Configure access** tab:

1. Select **Default access** or **Least privilege access**. For production environments, select **Least privilege access** to follow the principle of least privilege.
2. Select the deployment method: **AWS CloudFormation** or **Terraform**. For most environments, CloudFormation is the standard path.
3. Select **Download** to get the CloudFormation template. The template file is customized to the plans you selected.

### Deploy the CloudFormation template

The CloudFormation template creates the authentication resources required for Defender for Cloud to access your AWS account using federated credentials.

1. Open the **AWS Management Console** and navigate to **CloudFormation**.
2. Select **Create stack** \> **With new resources (standard)**.
3. Upload the template file you downloaded, or provide its S3 URL if you staged it in a bucket.
4. Review the IAM resources the template creates:
	* An **OpenID Connect identity provider** for the Microsoft\-managed Microsoft Entra application
	* IAM roles that Defender for Cloud assumes through web identity federation
	* SSM\-related resources for Arc autoprovisioning (included when Defender for Servers is selected)
5. Accept the IAM resource creation acknowledgment.
6. Deploy the stack. Deployment takes two to five minutes.

Important

If you stage the template in your own S3 bucket before deployment, apply a bucket policy that requires SSL requests only. Staged templates prevent an AWS CSPM recommendation about S3 SSL enforcement from flagging your own onboarding infrastructure.

Once the stack shows **CREATE\_COMPLETE**, return to the Azure portal and complete the connector:

1. Return to the **Configure access** tab in the Defender for Cloud connector wizard.
2. Select **Next: Review and generate**.
3. Review your connector configuration—account details, plans, and access settings.
4. Select **Create**.

Defender for Cloud begins its first scan of the connected AWS account. The connector resource appears in Environment Settings immediately. CSPM recommendations surface within four to six hours after the first scan completes.

### Validate AWS connector health

After creating the connector, verify that it's operating correctly before waiting for the first scan results.

1. In Defender for Cloud, select **Environment settings**.
2. Locate the AWS connector in the environment list.
3. Review the **Connectivity status** column:
	* **Healthy**: authentication succeeds and scans run normally
	* **Has issues**: a configuration or permission problem is preventing correct operation
	* **Connecting**: initial handshake in progress—normal for the first few minutes
4. Select the status value to open the **Environment details** page.

The Environment details page lists specific issues affecting connector health and provides remediation guidance. Common issues at this stage include:

* **Missing IAM permissions**: the CloudFormation template didn't deploy completely, or a plan was added after template generation. Fix by generating a new template with updated plan selection and redeploying as a stack update.
* **IAM role trust policy mismatch**: manual edits to the CloudFormation\-created roles broke the trust policy. Fix by rerunning the CloudFormation template to restore original trust conditions.

Note

Once the connector shows healthy status and the first scan completes, AWS resources appear in **Inventory** tagged with the AWS origin icon, CSPM recommendations surface in the **Recommendations** screen, and the **AWS Foundational Security Best Practices** compliance standard is autoassigned in the **Regulatory Compliance** dashboard.

Tip

If Defender for Servers is enabled and EC2 instances aren't completing Arc provisioning, verify that the SSM Agent is installed and that each EC2 instance profile includes the `AmazonSSMManagedInstanceCore` IAM policy.

---

## Connect GCP projects to Defender for Cloud

With AWS connected, you now onboard Contoso's Google Cloud Platform environment. The GCP connector workflow follows a similar structure to AWS: configure the connector in the Azure portal, select Defender plans, and then execute a provisioning script in GCP that creates the authentication resources. The key difference is the deployment mechanism—GCP uses a **GCloud shell script** instead of a CloudFormation template, and authentication uses **workload identity federation** instead of OIDC federation.

### Before you create the connector

Confirm these prerequisites:

* You have **Contributor or Owner** permissions on the Azure subscription where the connector resource is created.
* **Microsoft Defender for Cloud** is enabled on that subscription.
* You have **project owner** or sufficient access to the GCP project or organization being connected.
* The following APIs must be enabled on the GCP project **where you run the onboarding script**. If they aren't enabled, the GCloud script enables them automatically:
	+ `iam.googleapis.com`
	+ `sts.googleapis.com`
	+ `cloudresourcemanager.googleapis.com`
	+ `iamcredentials.googleapis.com`
	+ `compute.googleapis.com`

Note

For organization\-level onboarding, enable these APIs on the **management project**, not on each individual child project.

### Create the GCP connector

1. In the Azure portal, open **Microsoft Defender for Cloud** and select **Environment settings**.
2. Select **Add environment** \> **Google Cloud Platform**.
3. On the **Account details** tab, enter:
	* **Connector name**: a descriptive name, for example, `contoso-gcp-prod`
	* **Scope**: **Single project** or **Organization**
		+ Select **Organization** if you have org\-level IAM access and want to cover all current and future projects under the GCP organization
		+ Select **Single project** for a targeted pilot or for projects that don't belong to a managed organization
	* **Subscription**: the Azure subscription that owns this connector
	* **Resource group**: resource group for the connector resource
	* **Location**: Azure region for connector metadata storage
	* **Scan interval**: 4, 6, 12, or 24 hours
	* For **Organization** scope: your GCP **organization ID**
	* For **Single project** scope: your GCP **project number** and **project ID**
4. Select **Next: Select plans**.

#### Select Defender plans

Toggle plans on or off based on the GCP workloads you want to protect.

**Defender CSPM** is always enabled. It provides configuration posture assessment across all GCP resources in the connected project or organization.

Available CWPP plans for GCP:

| Plan | What it protects | Azure Arc required |
| --- | --- | --- |
| Defender for Servers | GCP Compute Engine VMs | Yes (autoprovisioned) |
| Defender for Containers | GKE clusters | No |
| Defender for Databases | Cloud SQL instances | No |

For Contoso's GCP environment, enable Defender for Servers to extend CWPP coverage to GCP Compute Engine VMs. The GCloud script generated includes Compute Engine management permissions and Google Cloud OS Config API access needed for Arc autoprovisioning.

#### Configure access

1. Select **Next: Configure access**.
2. Select the permission type:
	* **Default access**: broader permissions that support current and anticipated future Defender capabilities. Easier to configure initially.
	* **Least privilege access**: grants only the minimum permissions required by the plans you selected. Least access is the recommended choice for production environments and aligns with Contoso's security policy.
3. The portal displays the GCloud script, customized to your plan selections and permission type.

Note

If this GCP connector already uses **Least privilege access** and you want to enable AI Security Posture Management (AI SPM) for AI workload visibility—including Google Vertex AI—the existing service account bindings don't include the required permissions. Rerun the updated GCloud script to add them.

### Run the GCloud script

The GCloud script creates all authentication resources in your GCP environment. Unlike the AWS CloudFormation template, you don't download the GCloud script as a file—you run it directly in **Google Cloud Shell** from your browser, or copy and run it locally in an environment where the `gcloud` CLI is installed.

To run in Google Cloud Shell:

1. Open the [GCP Console](https://console.cloud.google.com) and activate Cloud Shell.
2. Copy the GCloud script from the Defender for Cloud portal.
3. Paste and run the script in the Cloud Shell terminal.
4. When prompted, confirm permission to create resources.

The script creates:

* A **workload identity pool** named after your connector
* \*\*Workload identity providers—one for each enabled Defender plan—each configured to trust tokens from Microsoft Entra ID
* **Service accounts** with IAM policy bindings scoped to the connected project (or organization for org\-level onboarding)

The permissions granted to each service account depend on which plans you selected and whether you chose default or least privilege access. The script output confirms each resource created and highlights any errors.

Tip

Save the GCloud script output for your deployment records. The service account names, workload identity pool ID, and provider IDs are useful when troubleshooting connector health issues later.

For organization\-level connectors, the script creates resources at the organization level and configures policy bindings that apply across all projects. Individual projects within the organization don't require separate script runs.

### Complete connector creation

1. After the GCloud script completes successfully, return to the Azure portal.
2. Select **Next: Review and generate**.
3. Review your selections—connector name, scope, plan configuration, and permission type.
4. Select **Create**.

Defender for Cloud creates the connector resource and schedules the first scan. GCP first scan results appear within up to six hours. Allow that time window before evaluating the connector's recommendation output.

### Validate GCP connector health

1. In Defender for Cloud, select **Environment settings**.
2. Locate the GCP connector.
3. Check the **Connectivity status** column.
4. Select the status value to open the **Environment details** page, which lists any specific issues and remediation steps.

Common GCP connector health issues at initial deployment:

* **Required APIs not enabled**: the GCloud script typically enables APIs automatically, but network restrictions or org policy constraints can prevent API enablement. Manually enable the five required APIs in the GCP Console or org policy.
* **Workload identity pool creation failed**: typically caused by organization policy constraints on workload identity pool creation. Review GCP org policies that restrict IAM or resource creation.
* **Service account permission denied**: IAM permissions on the GCP project or organization didn't propagate before Defender for Cloud's first authentication attempt. Wait a few minutes and select **Rescan** in the Environment details page.

Note

After the GCloud script completes and the connector is healthy, verify coverage for all connected environments in the next unit.

---

## Verify multicloud coverage and validate protection

After Contoso creates connectors for on\-premises, AWS, and GCP environments, your next step is confirming that coverage is active. You want to ensure posture assessment is running, CWPP plans are active, compliance standards are assigned, and resources are visible in inventory. The output is what you bring to the CISO before the compliance audit.

### Review connector health in Environment Settings

The primary health dashboard for all multicloud connections is **Defender for Cloud** \> **Environment settings**. Every connector you create appears here, mapped to its Azure subscription.

Each connector row shows a **Connectivity status** column with one of three states:

| Status | Meaning |
| --- | --- |
| **Healthy** | Authentication succeeds and scans complete without errors |
| **Has issues** | A configuration or permission problem is preventing full coverage |
| **Connecting** | Initial handshake in progress (normal for newly created connectors) |

Select the status value for any connector to open the **Environment details** page. This page is the primary troubleshooting view—it lists each specific issue detected, describes the cause, and in many cases provides a downloadable remediation script.

Tip

After creating a new connector, check Environment details within the first hour. Configuration issues appear before the first scan completes, letting you resolve problems early rather than waiting hours to discover missing coverage.

### Verify the asset inventory

After connector creation, allow up to six hours for the first scan to complete, then navigate to **Defender for Cloud** \> **Inventory** to verify resources from all connected environments appear.

Each resource shows an icon indicating its source cloud. Filter by **Cloud** to scope the view to AWS or GCP resources. Verify:

* EC2 instances appear for the AWS connector, tagged with the correct AWS account ID and region
* GCP Compute Engine VMs appear for the GCP connector, tagged with the GCP project
* Arc\-enabled servers appear for on\-premises machines with Arc deployed
* Each resource shows a populated **Health state** column

An empty health state column indicates the resource was discovered and awaits its first posture assessment. Health state populates after the first full scan cycle completes.

### Confirm CSPM recommendations surface

CSPM recommendations for AWS and GCP resources appear in **Defender for Cloud** \> **Recommendations** alongside Azure recommendations. In the **Recommendations** screen, use the **Cloud** filter to scope the view to **AWS** or **GCP** and verify findings appear for resources in your connected accounts.

For a newly connected AWS account, expect findings across EC2, S3, IAM, and CloudTrail configuration. For GCP, expect findings across Compute Engine, Cloud Storage, IAM, and GKE if Defender for Containers is enabled.

If no recommendations appear after six hours, return to Environment Settings and verify the connector shows Healthy status. Missing recommendations typically indicate a scan failure caused by missing IAM permissions.

### Check autoassigned compliance standards

Two compliance standards are automatically assigned when connectors are created, with no manual setup required:

* **AWS Foundational Security Best Practices**: applied to every subscription containing an AWS connector
* **GCP Default**: applied to every subscription containing a GCP connector

Verify both appear in **Defender for Cloud** \> **Regulatory Compliance**, each showing a compliance score calculated from CSPM findings across your connected accounts.

Note

Compliance data freshness for AWS and GCP resources updates on a 4\-hour minimum interval. Newly onboarded environments can show incomplete compliance data until several scan cycles complete. Allow 12 to 24 hours after initial onboarding for stable compliance posture data.

### Validate CWPP plan activation

CWPP plan validation requires verifying that plans are active at the connector level—not just that they were selected during connector creation.

In **Environment settings**, select a connector to view its configuration. The connector detail view shows which Defender plans are toggled on for that connector. Confirm:

* **Defender for Servers**: shows as active if you enabled it
* **Defender for Containers**: shows as active for EKS (AWS) or GKE (GCP) if selected
* **Auto\-provisioning settings**: verify Arc autoprovisioning for virtual machines shows as enabled

Connector\-level plan settings override subscription\-level defaults for resources in the connected environment. A plan disabled at the subscription level can still be active for AWS or GCP resources when enabled on the connector.

### Resolve common connectivity issues

| Issue | Environment | Remediation |
| --- | --- | --- |
| Missing IAM permissions | AWS | Generate an updated CloudFormation template with current plan selection and redeploy as a stack update |
| Required APIs not enabled | GCP | Enable the five required APIs manually in the GCP Console, or allow the GCloud script to run again |
| SSM Agent missing | AWS (Defender for Servers) | Install AWS SSM Agent on EC2 instances and attach the `AmazonSSMManagedInstanceCore` policy |
| OS Config agent disabled | GCP (Defender for Servers) | Enable the Google Cloud OS Config API and ensure Compute Engine VMs have OS Config enabled |
| Partial regional coverage | AWS | Add missing regions to the AWS connector configuration in Environment Settings |
| Arc agent not deploying | AWS or GCP | Verify SSM Agent (AWS) or OS Config (GCP) is operational; check for org policy restrictions blocking agent installation |

For Arc\-enabled on\-premises servers showing as disconnected in Inventory, verify outbound connectivity to Azure Arc endpoints on port 443 and check that the Connected Machine agent service is running on the machine.

With all environments validated and showing active coverage, Contoso's security team delivered what the CISO requested: unified visibility and protection across on\-premises, AWS, and GCP environments in a single Defender for Cloud view. In the next unit, you check your understanding of connecting hybrid and multicloud environments to Defender for Cloud.

---

## Knowledge check

Answer the following questions to check your understanding of connecting hybrid and multicloud environments to Microsoft Defender for Cloud.

### Check your knowledge

---

## Summary

Contoso's security team now has what the Security Officer (CISO) asked for: a single Defender for Cloud view covering Azure, on\-premises, AWS, and GCP environments. Arc\-enabled on\-premises servers appear beside Azure VMs in the Inventory. AWS EC2 instances and GCP Compute Engine VMs contribute to the secure score. The AWS Foundational Security Best Practices and GCP Default compliance standards run automatically. Defender for Servers plans protect cloud VMs through Arc autoprovisioning, and Defender CSPM identifies misconfigurations across all three clouds continuously—without agents.

### Key technical decisions in this module

The connections you built in this module involved several architectural choices that affect security posture, operational overhead, and compliance audit readiness.

**Federated authentication eliminates stored credential risk.** Both the AWS CloudFormation template and GCP GCloud script establish federated trust relationships—OIDC federation for AWS and workload identity federation for GCP. Defender for Cloud never stores long\-lived credentials in Azure. Even if a connector resource were compromised, there are no access keys or private keys to exfiltrate.

**CSPM activates immediately; CWPP requires Arc.** The Security Posture Management plan is always active on every connector and runs agentlessly through cloud provider APIs. Asset inventory, recommendations, compliance standards, and Defender CSPM capabilities are available within hours of connector creation—before any agent deployment. CWPP plans (Defender for Servers threat detection, JIT VM access, file integrity monitoring) require Azure Arc on each VM. For AWS and GCP, Arc autoprovisioning handles scale; for on\-premises servers, deliberate deployment planning is required.

**Connector scope defines coverage boundaries.** Organization\-level connectors (AWS management account, GCP organization) provide enterprise\-wide coverage with automated child account or project discovery. Account\-level and project\-level connectors provide granular control. Unselected AWS regions and unconnected GCP projects remain unguarded sides—coverage is exactly as wide as your connectors define.

**Least privilege access reduces blast radius.** Selecting least privilege access during connector creation ensures Defender for Cloud has only the permissions required for the plans active today. If you add plans later, you must regenerate and redeploy the onboarding script with updated plan selections to add the new permissions.

**The MMA path is retired.** On\-premises servers must use Azure Arc for full Defender for Servers Plan 2 coverage. The Microsoft Monitoring Agent retired in August 2024\.

### Learn more

To continue building your knowledge on multicloud security in Defender for Cloud, review these resources:

* [Connect your AWS account to Microsoft Defender for Cloud](/en-us/azure/defender-for-cloud/quickstart-onboard-aws)
* [Connect your GCP project to Microsoft Defender for Cloud](/en-us/azure/defender-for-cloud/quickstart-onboard-gcp)
* [Connect non\-Azure machines to Microsoft Defender for Cloud](/en-us/azure/defender-for-cloud/quickstart-onboard-machines)
* [Authentication architecture for AWS connectors](/en-us/azure/defender-for-cloud/concept-authentication-architecture-aws)
* [Authentication architecture for GCP connectors](/en-us/azure/defender-for-cloud/authentication-architecture-google-cloud)
* [Plan multicloud security in Defender for Cloud](/en-us/azure/defender-for-cloud/plan-multicloud-security-get-started)
* [Azure Arc\-enabled servers overview](/en-us/azure/azure-arc/servers/overview)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/connect-hybrid-multicloud-environments-defender/_

## Fuentes
- [Connect hybrid and multicloud environments to Microsoft Defender for Cloud](https://learn.microsoft.com/en-us/training/modules/connect-hybrid-multicloud-environments-defender/?WT.mc_id=api_CatalogApi)
