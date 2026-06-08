# Configure and validate permissions

> Curso: Implement security through a pipeline using Azure DevOps (wwl-implement-security-through-pipeline-using-devo) · Seccion: Implement security through a pipeline using Azure DevOps
> Duracion estimada: 57 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure DevOps is a robust platform that can help streamline software development and deployment processes. However, ensuring only authorized users can access the pipelines, environments, and other resources is crucial. Failure to properly manage and validate user permissions can result in serious security issues and potentially put an organization at risk.

Azure Pipelines also involves security risks you must be aware of and mitigate. For example, to protect secrets, control access to pipelines and resources, and monitor pipeline activities for anomalies.

This module explores the key concepts and best practices for configuring and validating permissions in Azure DevOps. Learn how to configure user permissions, pipeline permissions, approval, branch checks, and auditing and managing permissions.

#### Learning objectives

After completing this module, students and professionals can:

* Configure and validate user permissions.
* Configure and validate pipeline permissions.
* Configure and validate approval and branch checks.
* Manage and audit permissions in Azure DevOps.

#### Prerequisites

You must create an Azure DevOps Organization and a Team Project for some exercises. If you don't have them yet, see:

* [Create an organization \- Azure DevOps.](/en-us/azure/devops/organizations/accounts/create-organization)
* [Create a project in Azure DevOps.](/en-us/azure/devops/organizations/projects/create-project)

To get the most out of this course, we recommend that you understand Azure DevOps and pipeline management.

Ensure you have all the necessary resources and access to Azure DevOps before starting the course.

Let's begin!

---

## Configure and validate user permissions

By validating user permissions, you can check that only authorized users can access and modify your pipelines and that unauthorized users are blocked from performing actions that could compromise your code or resources. Validating user permissions can help you identify and fix security gaps or pipeline issues.

There are many ways to configure user permissions in Azure DevOps. You can use the Azure DevOps web interface or the Azure DevOps REST API. You can also use the Azure DevOps CLI to manage user permissions.

When you decide how to add permissions, you should consider the following factors:

* The number of users and groups you need to add to your project.
* The users who need temporary access to a specific resource or pipeline.
* Whether you want to add users and groups to a specific project or the entire organization.
* Whether you want to add users and groups to a specific pipeline, resource, approval, branch check, audit, environment, etc.

For every user and group you add to your project, you can specify the permissions they have for the project. Azure DevOps provides a set of predefined permissions that you can use to control access to your project. You can also create custom permissions to meet your specific needs.

It's recommended to follow the principle of least privilege, granting users only the minimum level of access required to perform their job functions and regularly reviewing and updating permissions as needed.

### Add users or groups to the project

1. Open the Azure DevOps project and select the Project settings.
2. In the Project Settings menu, select the Permissions option under General.
3. You can view and manage the security groups, users, and their permissions.
4. Select the group you want to add users.

Note

To understand the different types of groups and permissions, see [Security groups, service accounts, and permissions in Azure DevOps](/en-us/azure/devops/organizations/security/permissions/).
5. Select the "Members" tab to view the list of users in the group.
6. Click on the "\+ Add" button, then select the user or group you want to add.
7. To specify permissions for the user, you can open the new added user and make changes to the default inherited permissions.

### Add users to specific teams

You can create teams or groups based on your organizational structure if you have many users and groups. Teams are a collection of users and groups with access to a specific project. You can add users to a team and then add the team to a particular pipeline. This way, you can manage permissions for many users and groups in a single place.

1. Open the Azure DevOps project and select the Project settings.
2. In the Project Settings menu, select the Teams option under General.
3. You can view and manage the teams and their permissions.
4. Select the team you want to add users.
5. Select the "Members" tab to view the list of users in the team.
6. Click on the "\+ Add" button, then select the user or group you want to add.
7. To specify permissions for the user, you can open the new added user and make changes to the default inherited permissions.

### Tips for validating user permissions

* Use test cases to verify that users have access to the resources they need to complete their tasks.
* Perform a thorough review of your user permissions at regular intervals to ensure that they're up to date and reflect the project's current state.
* Use the Azure DevOps audit logs to monitor changes to user permissions and track any unauthorized changes.

### Challenge yourself

You're a DevOps engineer responsible for managing a team project in Azure DevOps. The project has several teams, and you must set up specific permissions for each group.

Team A should be able to create and manage projects but can't delete or rename them. Team B should be able to manage work items but need permission to move out of the project and view analytics. Team C should have full access to everything. How would you configure the user permissions for each team in Azure DevOps?

For more information about permissions, security groups, and accounts, see:

* [Security groups, service accounts, and permissions in Azure DevOps](/en-us/azure/devops/organizations/security/permissions/)
* [Add organization users and manage access](/en-us/azure/devops/organizations/accounts/add-organization-users)
* [About access levels](/en-us/azure/devops/organizations/security/access-levels)
* [Troubleshoot access and permission issues](/en-us/azure/devops/organizations/security/troubleshoot-permissions)

---

## Configure and validate pipeline permissions

Configuring and validating permissions in Azure Pipelines is crucial to ensure that only authorized users can access the pipelines, environments, and other resources. Failure to properly manage and validate user permissions can result in serious security issues and potentially put your organization at risk.

If unauthorized users have access to your pipelines, they can make changes to your code, steal your secrets, and even access your production environment.

In this unit, you'll learn how to set up and manage pipeline permissions using Azure Pipelines with YAML. Pipeline permissions control who can create, edit, view, queue, or delete pipelines in your project.

### Set organization\-level pipeline permissions

Organization\-level pipeline permissions control who can create, edit, delete, or view pipelines across all projects in your organization. You can set these permissions for Azure DevOps groups or individual users.

1. Sign in to your organization.
2. Click on Organization Settings at the bottom left and in Permissions under the Security section.
3. Select a group or user from the list, or use the search box to find one.
4. Select Permissions and then find Pipelines.
5. Modify the permissions as needed, such as allowing or denying manage pipeline policies, view build resources, etc.

### Set project\-level pipeline permissions

Project\-level pipeline permissions apply to all pipelines in your project. You can grant or deny access to specific Azure DevOps groups or individual users.

To set project\-level pipeline permissions:

1. Sign in to your Azure DevOps organization.
2. From your project, select Pipelines under Pipelines.
3. Select the three dots in the top right corner (...), and click Manage security.
4. Modify the group or user permissions as you need.
5. Select Allow or Deny the permission for a security group or an individual user, and then exit the screen.

Some common permissions are:

* **Edit build pipeline:** Allows editing existing pipelines.
* **View build pipeline:** Allows viewing existing pipelines and their runs.
* **Queue builds:** Allows queuing new runs for existing pipelines.

### Set folder\-level pipeline permissions

1. Open your Azure DevOps project and select Pipelines under Pipelines.
2. Select a folder from the list of folders, or create a new one by selecting New folder.
3. Select the three dots in the top right corner (...), and click Manage security for the folder you want to modify.
4. Modify the permissions associated with an Azure DevOps group or an individual user.

### Challenge yourself

1. Set organization\-level pipeline permissions to allow only Project Administrators to create new pipelines across all projects in your organization.
2. Set folder\-level pipeline permissions to deny Project Contributors from deleting or moving pipelines within a folder named “Production” in your project.
3. Set branch\-level pipeline triggers to include only main and develop branches for a YAML pipeline.

For more information about pipeline permissions, see:

* [Set pipeline permissions](/en-us/azure/devops/pipelines/policies/permissions)
* [About pipeline security roles](/en-us/azure/devops/organizations/security/about-security-roles)
* [Use Azure Resource Manager service connections](/en-us/azure/devops/pipelines/library/service-endpoints)

---

## Configure and validate approval and branch checks

In Azure DevOps, you can configure and validate approvals and branch checks to ensure that changes to your code are reviewed and approved before being deployed to production. It helps to prevent errors and vulnerabilities in your code from reaching production and causing issues.

Approval and branch checks are critical components of a secure software development process. By requiring approvals for code changes and validating branch names and versions, you can prevent unauthorized changes from being deployed to production.

In this unit, learn how to configure and validate approvals and branch checks in Azure DevOps.

### Set up approvals and checks

1. In your Azure DevOps project, click on Environments under Pipelines.
2. Select the environment for which you want to create the approval or branch check. If you don't have an environment, you can create one by clicking on the "New environment" button.
3. Click on the "Approvals and checks" tab next to "Deployments" tab.
4. To add an approval check, select the "Approvals".
5. In the "Add Approvals" dialog box, you can configure the details of the approval check, such as the approvers, the instructions to approvers, if the approver can approve their own runs, and the approval timeout.
6. Click on the Create button to create the approval check.
7. Back to "Approvals and Checks" to add a branch check, select the "Branch control".
8. In the "Branch control" dialog box, you can configure the details of the branch check, such as the allowed branches, a check to verify branch protection, and the timeout.
9. Click on the "Create" button to save your changes.

There are other types of checks that you can add to your environment. It's important to understand the purpose of each check and how it can help you to secure your software development process.

For example:
Business Hours, Evaluate artifact, Exclusive Lock, Invoke Azure Function, Invoke REST API, Query Azure Monitor alerts, Required template, ServiceNow Change Management, etc.

### Challenge yourself

Create a pipeline in Azure DevOps and configure approval and branch checks to ensure that code changes are reviewed and approved before being deployed to production. Then, validate the approval and branch checks to ensure that they're working as expected.

For more information about approvals and checks, see:

* [Explore release recommendations](/en-us/training/modules/explore-release-strategy-recommendations/)
* [Define approvals and checks](/en-us/azure/devops/pipelines/process/approvals)
* [Use gates and approvals to control your deployment](/en-us/azure/devops/pipelines/release/deploy-using-approvals)

---

## Manage and audit permissions

Managing permissions is essential to maintaining security and control over your pipelines and resources. By setting permissions, you can restrict access to sensitive data and ensure that only authorized users can access certain features.

In this unit, learn how to manage and audit permissions using Azure DevOps.

### Manage organization permissions

You can also set permissions for specific projects. The steps and configuration are similar to the organization\-level permissions.

To configure permissions for an organization:

1. Sign in to your Azure DevOps organization.
2. Click on Organization Settings at the bottom left and in Permissions under the Security section.
3. Under "Permissions," select the group or user you want to manage permissions for.
4. Click on "Permissions," and select the type of permissions you want to set (for example, "General," "Repos," "Pipelines," "Auditing," etc.).
5. Choose the level of permission you want to assign (for example, "Allow," "Deny," or "Not set").

### Audit permissions

Audit logs provide a record of every operation that occurs in Azure DevOps, including all changes made to work items, builds, releases, and pipelines.

By reviewing audit logs, administrators and security professionals can identify unauthorized access attempts, suspicious activity, or compliance violations. This information can help prevent security breaches and ensure compliance with regulations and organizational policies.

In addition, audit logs can help teams identify issues and improve their processes by providing detailed information about what actions were taken and by whom. By regularly reviewing audit logs, teams can identify potential problems and take corrective measures to prevent them.

To configure auditing for your organization:

1. Sign in to your Azure DevOps organization.
2. Click on Organization Settings at the bottom left and in Policies under the Security section.
3. Under Security policies, enable Log Audit Events.
4. The Auditing section appears in the left navigation pane under General. Click on it.
5. The audit log provides a simple view into the audit events recorded for your organization.
6. You can filter the audit log by user, date range, or permission type to get a more specific view of the changes.
7. (Optional) You can export the audit log to a CSV or JSON file by clicking on the Export button, or you can view the details of a specific event by clicking on the event.

Consider sending your events downstream to a Security Information and Event Management (SIEM) tool using the [Audit Streaming feature](/en-us/azure/devops/organizations/audit/auditing-streaming) for long\-term storage and analysis of your auditing events. We recommend exporting the auditing logs for cursory data analysis.

Note

Auditing is only available for organizations backed by Microsoft Entra ID. For more information, see [Connect your organization to Microsoft Entra ID](/en-us/azure/devops/organizations/accounts/connect-organization-to-azure-ad).

### Challenge yourself

To reinforce your understanding of managing and auditing permissions, try the following challenge:

* Enable Auditing for your organization.
* Configure a group with permissions to manage the pipelines in the project.
* Use the audit log to confirm the permissions and configurations.

For more information about approvals and checks, see:

* [Access, export, and filter audit logs](/en-us/azure/devops/organizations/audit/azure-devops-auditing/)
* [Auditing events list](/en-us/azure/devops/organizations/audit/auditing-events/)
* [Security groups, service accounts, and permissions in Azure DevOps](/en-us/azure/devops/organizations/security/permissions/)

---

## Lab \- Configure and validate permissions

In this lab, set up a secure environment that adheres to the principle of least privilege, ensuring that members can access only the resources they need to perform their tasks and minimize potential security risks. It involves configuring and validating user and pipeline permissions and setting up approval and branch checks in Azure DevOps.

Note

To complete this lab, you will need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). You will also need to [validate your lab environment](https://aka.ms/mslearn-implement-security-through-pipeline-validate-lab-environment) to complete this lab.

Launch the exercise and follow the instructions.

Tip

To continue your learning journey, open the exercise in a new browser tab or window while staying on this page. To do this, right\-click the **Launch Exercise** button and select **Open link in new tab** or **Open link in new window**.

---

## Summary

In this module, you learned the key concepts and best practices for configuring and validating permissions in Azure DevOps. You learned to configure user permissions, pipeline permissions, approvals, branch checks, and auditing and managing permissions.

You learned how to:

* Configure and validate user permissions
* Configure and validate pipeline permissions
* Configure and validate approvals and branch checks
* Manage and audit permissions in Azure DevOps

### Learn more

* [Azure DevOps permissions](/en-us/azure/devops/organizations/security/permissions)
* [Securing Azure Pipelines](/en-us/azure/devops/pipelines/security/overview)
* [Security best practices](/en-us/azure/devops/organizations/security/security-best-practices)
* [Add organization users and manage access](/en-us/azure/devops/organizations/accounts/add-organization-users)
* [Grant or restrict access using permissions](/en-us/azure/devops/organizations/security/restrict-access)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-validate-permissions/_

## Fuentes
- [Configure and validate permissions](https://learn.microsoft.com/en-us/training/modules/configure-validate-permissions/?WT.mc_id=api_CatalogApi)
