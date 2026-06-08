# Configure secure access to Azure Repos from pipelines

> Curso: Implement security through a pipeline using Azure DevOps (wwl-implement-security-through-pipeline-using-devo) · Seccion: Implement security through a pipeline using Azure DevOps
> Duracion estimada: 74 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

It's essential to have a secure environment where pipelines can access resources, such as packages, secrets, and services, without exposing sensitive information. In this module, you'll learn the best practices to ensure secure access to resources when working with Azure DevOps.

In this module, we cover the steps to configure secure access to packages and configure credential secrets and secrets for services in Azure DevOps. Finally, we cover how to use the service connection in a YAML pipeline to access packages securely.

#### Learning objectives

After completing this module, students and professionals can:

* Configure pipeline access to packages.
* Configure credential secrets, and secrets for services.
* Ensure that the secrets are in the Azure Key Vault.
* Ensure that secrets aren't in the logs.

#### Prerequisites

You must create an Azure DevOps Organization and a Team Project for some exercises. If you don't have them yet, see:

* [Create an organization \- Azure DevOps.](/en-us/azure/devops/organizations/accounts/create-organization)
* [Create a project in Azure DevOps.](/en-us/azure/devops/organizations/projects/create-project)

To get the most out of this course, we recommend that you understand Azure DevOps and pipeline management.

Ensure you have all the necessary resources and access to Azure DevOps before starting the course.

Let's begin!

---

## Configure pipeline access to packages

In this unit, learn how to configure pipeline access to packages stored in Azure Artifacts. It involves creating and managing feed permissions, which allow you to control who can access and manage your packages. By controlling access to these packages, you can ensure that only authorized users can access and use the packages in your projects.

### Configure pipeline access to packages in YAML

1. Navigate to your Azure DevOps organization and select the project that contains the Azure Artifacts repository you want to configure.
2. In the left\-side menu, select Artifacts.
3. If you don't have any feed, [Create a feed](/en-us/azure/devops/artifacts/get-started-nuget).
4. In the Artifacts menu, select Feed Settings.
5. Click on the Permissions tab.
6. Add users or groups to the repository.
7. Select the permissions you want to assign to each user or group (for example, Owner, Reader, Contributor, or Collaborator).
8. Select Add users/groups, and then add your build identity as a Contributor. The project\-level build identity is named as follows: \[Project name] Build Service (\[Organization name]).
Example: Implement security through a pipeline using DevOps Build Service (contoso).

Note

To access packages from your pipelines, the appropriate build identity must have access to your feed. By default, feeds have the Project Collection Build Service role set to Collaborator.
9. Save your changes.

### Consume packages from Azure Artifacts in a pipeline

In Azure Pipelines, you can use the classic editor or the YAML tasks to publish your NuGet or other packages within your pipeline to your Azure Artifacts feed or public registries such as nuget.org.

To configure pipeline access to packages stored in Azure Artifacts repositories using YAML:

```
steps:
    - task: NuGetCommand@2
      inputs:
        command: 'restore'
        restoreSolution: '**/*.sln'
        feedsToUse: 'select'
        vstsFeed: 'SecurePipelineFeed'

```

Replace your Azure Artifacts feed name with the name of your Azure Artifacts feed and your solution file.sln with the name of your solution file.

### Challenge yourself

If you want to take your learning to the next level, try setting up a pipeline that restores packages from multiple Azure Artifacts repositories. You can also try setting up a pipeline that restores packages based on the branch being built.

For more information about Artifacts, see:

* [Create and target an environment.](/en-us/azure/devops/artifacts/start-using-azure-artifacts)
* [Configure permissions.](/en-us/azure/devops/artifacts/feeds/feed-permissions)
* [Set pipeline permissions.](/en-us/azure/devops/pipelines/policies/permissions)

---

## Configure pipeline access to credential secrets

In this unit, you'll learn how to secure your pipeline secrets using Azure DevOps variables and hidden secrets. It's essential to ensure that your pipeline is secure and your secrets are protected. You'll also learn how to use Azure DevOps variables to store your secrets and how to access them within your pipeline.

### Use variables to store values or encrypted secrets

1. Open your Azure DevOps project and navigate to the Pipelines section.
2. Click on Pipelines in the left\-hand menu.
3. Open your pipeline (for example "eShopOnWeb"), or create a new one.
4. Click the Edit button in the right\-top corner to edit your pipeline.
5. Click the Variables button.
6. Click the New variable button to create a new variable.
7. Enter the name and value for your secret.
8. Check the "Keep this value secret" checkbox to encrypt your secret.
9. (Optional) Check the "Let users override this value when running this pipeline" checkbox to allow users to override the value of your variable at queue time.
10. Click the OK button to save your variable.
11. Click the Save button to save your pipeline.

### Create a secret in an Azure DevOps variable group

1. Open your Azure DevOps project and navigate to the Pipelines section.
2. Click on Library in the left\-hand menu.
3. Open your variable group (for example "eShopOnWeb"), or create a new one.
4. Click the Add button to add a new variable.
5. Give your variable a name (for example "eShopOnWeb Secret Key").
6. Enter the value for your secret in the Value field.
7. Click the Save button to save your variable group.

### Allow variable groups use in your pipeline

1. Open your Variable Group.
2. Click on the Pipeline permissions button.
3. Add the pipelines that will use this Variable Group.
4. Click the Save button to save your Variable Group.

### Access secrets within your pipeline

1. Open your pipeline YAML file.
2. Add the following code to the top of your YAML file:

```
variables:
  - group: eShopOnWeb

```
3. Replace "eShopOnWeb" with the name of your variable group.
4. Use the following syntax to access your secrets within your pipeline:

```
$(eShopOnWeb Secret Key)

```
5. Replace "eShopOnWeb Secret Key" with the name of your secret.
6. If you want to use your pipeline variables, you can use the following:

```
$(New Credential Secret)

```

Note

The variable use will be the same, but one is coming from Variable Groups, and others from Variables from your pipeline UI.
7. Save your YAML file.

Secret variables are encrypted at rest with a 2048\-bit RSA key. Secrets are available on the agent for tasks and scripts to use. Be careful about who has access to alter your pipeline.

You must decide whether to use the Variable Groups or the pipeline UI variables. The advantage of using the Variable Groups is that you can use the same variables in multiple pipelines. The advantage of using the pipeline UI variables is that you can override the variable's value at queue time.

Important

We try to mask secrets from appearing in Azure Pipelines output, but you still need to take precautions. Never echo secrets as output. Some operating systems log command line arguments. Never pass secrets on the command line. Instead, we suggest that you map your secrets into environment variables.
We never mask the substrings of secrets. If, for example, "abc123" is set as a secret, "ABC" isn't masked from the logs. This is to avoid masking secrets at too granular of a level, making the logs unreadable. For this reason, secrets should not contain structured data. If, for example, "{ "foo": "bar" }" is set as a secret, "bar" isn't masked from the logs.

### Challenge yourself

* Create a pipeline that retrieves a password from Azure DevOps Variable Group.
* Store a variable using a secret variable and use it in your pipeline.
* Override the variable of your variable in your pipeline with the secret variable at queue time.

For more information about secret variables, see:

* [Manage and modularize tasks and templates.](/en-us/training/modules/manage-modularize-tasks-templates/)
* [Set secret variables.](/en-us/azure/devops/pipelines/process/set-secret-variables)
* [Add \& use variable groups.](/en-us/azure/devops/pipelines/library/variable-groups)
* [Set pipeline permissions.](/en-us/azure/devops/pipelines/policies/permissions)

---

## Configure pipeline access to secrets for services

Securing access to services is essential when working with pipelines in Azure DevOps. Service connections allow you to store your pipelines' credentials to access external resources, such as databases, web APIs, and other systems.

In this unit, learn how to use secrets for services and service connection secrets in Azure Pipelines using YAML.

### Create a service connection

1. Go to your Azure DevOps project.
2. Navigate to the Project settings.
3. Click on Service connections under Pipelines.
4. Click on New service connection.
5. Select the type of service connection you want to create (for example, Azure Service Bus, Kubernetes, Apple App Store or other).
6. Enter the required information for the service connection.
7. Click on Save.

### Store the service connection using variables

1. Go to your pipeline definition.
2. Click on Edit.
3. Click on Variables.
4. Create a new variable with the name that represents the service connection (for example, service\_bus\_connection).
5. Enter the value of the service connection.
6. Check the checkbox "Keep this value secret" to encrypt the variable.
7. Click on Save.

Important

Unlike normal variables, they are not automatically decrypted into script environment variables. You need to map secret variables explicitly.

### Use the service connection in YAML

In your pipeline definition, add the following YAML code to use the service connection secrets:

```
    steps:
    - powershell: |
        Write-Host "Using the mapped env var for this task works and is recommended: $env:MY_MAPPED_ENV_VAR"
      env:
        MY_MAPPED_ENV_VAR: $(service_bus_connection) # the recommended way to map to an env variable
    
    - task: PublishToAzureServiceBus@1
      inputs:
        azureSubscription: $(service_bus_connection)
        messageBody: '"hello world!"'
        signPayload: false
        waitForCompletion: true

```

In the above example, the variable service\_bus\_connection is used in the pipeline to access the Azure Service Bus service connection name.

### Challenge yourself

* Create a new pipeline that deploys a sample web application to an Azure App Service using a service connection for Azure.
* Store the Azure App Service password as a variable and use it in the pipeline.
* Add a step to the pipeline that updates the Azure App Service configuration with the connection string to a database.
* Add the service connection to a pipeline using the service connection name as a secret variable.

For more information about secret variables, see:

* [Define variables.](/en-us/azure/devops/pipelines/process/variables/)
* [Manage service connections.](/en-us/azure/devops/pipelines/library/service-endpoints/)
* [Provision and test environments.](/en-us/training/modules/configure-provision-environments/)

---

## Use Azure Key Vault to secure secrets

Securing access to sensitive information, such as passwords and API keys, is essential to DevOps.

In this unit, learn how to configure pipeline access to credential secrets using Azure DevOps and Azure Key Vault.

By following the steps outlined in this unit, you can keep your project secure and protected.

### Create an Azure Key Vault and Service Principal

The first step in securing access to credential secrets is to store them in Azure Key Vault. This service allows you to store and manage secrets, keys, and certificates securely and provides you with the ability to control access to these secrets.

1. To create an Azure Key Vault, go to the Azure portal and click on the "Create a resource" button.
2. Search and select the "Key Vault" option, click create and then fill out the required information to create a new vault.
3. Create a new Service Principal in Microsoft Entra ID to grant access to the Key Vault.

Note

Follow [this guide](/en-us/azure/active-directory/develop/howto-create-service-principal-portal) to create your service principal.
4. Assign the service principal to the Key Vault following [this guide](/en-us/azure/key-vault/general/assign-access-policy-portal).

Important

The service principal that you created will need to have **Secret permissions** access ("Get, List") to the Key Vault. If the service principal does not have access to the Key Vault, you will see an error message when you try to link the Variable Group to the Key Vault.
5. Once you've created your Key Vault, you need to store the secrets that you want to use in your pipeline. You can create secrets directly in your Key Vault, or from the Azure DevOps.

### Create secrets in Azure Key Vault

1. In the Azure portal, go to the Azure Key Vault that you created in step 1\.
2. Open the "Secrets" option and click on the "Generate/Import" button.
3. From the Azure Key Vault you can create manual secrets, or upload a certificate.
4. Once you've created your secret, you can use it in your pipeline.

### Create secrets in Azure DevOps

1. In Azure DevOps, go to the Azure DevOps organization and project that you want to use.
2. Click on Library and then open your Variable group.
3. Toggle the "Link to Key Vault" option and select the Key Vault and secret that you want to use.

Important

The service principal that you created in step 1 will need to have access ("Get, List") to the Key Vault and the secret that you want to use in your pipeline. If the service principal does not have access to the Key Vault, you will see an error message when you try to link the Variable Group to the Key Vault.
4. Click "Authorize" to enable Azure Pipelines to set these permissions or manage secret permissions in the Azure portal.
5. When authorization is complete, click Add under Variables to add the secret from your linked Key Vault to your Variable group.
6. Select the secret that you want to use in your pipeline and click OK to add it to your Variable group.
7. Save the Variable group.

### Grant Azure DevOps Access to Key Vault

Now that you've stored your secrets in Azure Key Vault, you need to grant Azure DevOps access to the Key Vault so that your pipeline can retrieve the secrets.

1. In the Azure portal, go to the Azure DevOps organization and project.
2. Go to the "Project Settings" and then "Service connections".
3. Click the "New service connection" button, and then select "Azure Resource Manager".
4. Fill out the required information to create the connection, including the name of the Key Vault and the secrets that you want to use in your pipeline.
5. After you've created the service connection, you'll need to grant Azure DevOps access to the Key Vault. To do this, go to the Azure Key Vault and click on the "Access policies" option.
6. Add a new policy, and then select the Azure DevOps service connection that you created in step 4\.
7. Assign the "Get" and "List" permissions to the service connection.

### Use secrets in your pipeline

Once you have granted Azure DevOps access to your Key Vault, you can now use the secrets in your pipeline.

1. Open your pipeline definition in Azure DevOps, and then add the following YAML code:

```
steps:
- task: AzureKeyVault@2
  inputs:
    azureSubscription: '<your_azure_subscription_name>'
    KeyVaultName: '<your_key_vault_name>'
    SecretsFilter: |
      <secret_name>

```

Replace \<your\_azure\_subscription\_name\> with the name of your Azure subscription, \<your\_key\_vault\_name\> with the name of your Key Vault, and \<secret\_name\> with the name of the secret that you want to use in your pipeline.
2. Save the pipeline definition, and then run the pipeline. The secret should now be available in your pipeline, and you can use it as needed.

### Challenge yourself

Try to implement a secure way of storing and accessing multiple secrets in your pipeline.

* Create a new pipeline for a sample project.
* Add a step to the pipeline that requires access to a service connection, for example, access to a database or API.
* Create a new Azure Key Vault and store the credentials for the service connection securely in the Key Vault.
* Update the pipeline to retrieve the credentials from the Key Vault.
* Verify that the pipeline can access the service connection successfully using the credentials stored in the Key Vault.

Note

To complete this challenge, you will need access to an Azure subscription and to Azure DevOps. You may need to create an Azure Key Vault and an Azure DevOps project if you do not have these resources available.

For more information about Azure Key Vault and pipeline integration, see:

* [Manage application configuration data.](/en-us/training/modules/manage-application-configuration-data/)
* [Use Azure Key Vault secrets in Azure Pipelines.](/en-us/azure/devops/pipelines/release/azure-key-vault/)
* [Azure Key Vault keys, secrets and certificates overview.](/en-us/azure/key-vault/general/about-keys-secrets-certificates)

---

## Explore and secure log files

This unit explores how to access and secure log files in Azure Pipelines and secure them from displaying secrets in plain text.

### Access log files in Azure Pipelines

The job details page provides detailed information about the pipeline run, including the tasks executed, their status, and any output generated.

You can access the logs for a specific pipeline run by following these steps:

1. In your Azure DevOps project, navigate to the pipelines section, under pipelines menu.
2. Select the pipeline for which you want to view the logs.
3. Click on a specific run of the pipeline.
4. In the run details page, find the Jobs tab and click on the job for which you want to view the logs.

You can also access the logs for a specific task by clicking on the task name, or download logs for the entire job by clicking on the "Download logs" link.

### Secure log files

Securing log files in Azure Pipelines is crucial to ensure that sensitive information, such as secrets and credentials, isn't displayed in plain text. Azure Pipelines attempts to scrub secrets from logs wherever possible. This filtering is on a best\-effort basis and can't catch every way that secrets can be leaked. Avoid echoing secrets to the console, using them in command line parameters, or logging them to files.

There are many ways to secure log files in Azure Pipelines, including:

* By using the `issecret=true` command in a script or task, you can ensure that specific values aren't displayed in the logs. When issecret is set to true, the variable's value is saved as secret and masked out from the log. Secret variables aren't passed into tasks as environment variables and must instead be passed as inputs.

Set a variable as a secret in a script or task:

```
    steps:
    - pwsh: |
        Write-Host "##vso[task.setvariable variable=nonSecretVar;]Now you can see me!"
        Write-Host "##vso[task.setvariable variable=secretVar;issecret=true]Now you don't!"
      name: SetVariables

```

Read the variables:

```
    - pwsh: |
        Write-Host "The magician says: $env:NONSECRETVAR = Not a secret."
        Write-Host "The magician says: $env:SECRETVAR = Yes, it's hidden, can't you see it? =)"
        Write-Host "The magician says: $(secretVar) = It's encrypted."

```

Output:

```
    The magician says: Now you can see me! = Not a secret.
    The magician says:  = Yes, it's hidden, can't you see it? =)
    The magician says: *** = It's encrypted.

```
* By using the `isoutput=false` command in a script or task, the variable's value is hidden out from the log.

Set a variable as a secret in a script or task:

```
    steps:
    - pwsh: |
        Write-Host "##vso[task.setvariable variable=outputVarTrue;isoutput=true]No, it's not a secret!"
        Write-Host "##vso[task.setvariable variable=outputVarFalse;isoutput=false]Yes, it's a secret!"
      name: SetVariables

```

Read the variables:

```
    - pwsh: |
        Write-Host "Hidden out from the log: $env:SETVARIABLES_OUTPUTVARTRUE"
        Write-Host "Hidden out from the log: $(SetVariables.outputVarTrue)"
        Write-Host "Hidden out from the log: $env:SETVARIABLES_OUTPUTVARFALSE = Yes, it's hidden."

```

Output:

```
    Hidden out from the log: No, it's not a secret!
    Hidden out from the log: No, it's not a secret!
    Hidden out from the log:  = Yes, it's hidden

```

A few other ways to secure log files in Azure Pipelines include:

* Use Secure Files type to upload a file to Azure Pipelines and then download it to the pipeline using the "Download secure file" task. This is useful for uploading certificates and other files that are required by tasks in the pipeline, but shouldn't be displayed in plain text.
* Azure Pipelines will automatically delete log files after a certain amount of time, or by the **retention settings**. This is useful for ensuring that secrets and other sensitive information aren't stored indefinitely.
* Azure Key Vault integration is another way to secure your secrets from log files.
* Secure files, Secret variables, and Variable groups are another way to secure log files in Azure Pipelines.

### Challenge yourself

1. Create a new pipeline in your Azure DevOps project.
2. Add a task that prints a secret value to the console.
3. Run the pipeline and confirm that the secret value is displayed in the logs.
4. Modify the pipeline to secure the logs, following the suggestions outlined in this unit.
5. Rerun the pipeline and confirm that the secret value is no longer displayed in the logs.

This challenge helps reinforce your understanding of log files in Azure Pipelines and how to secure them from displaying secrets in plain text.

Note

To complete this challenge, you will need access to an Azure subscription and to Azure DevOps. You may need to create an Azure Key Vault and an Azure DevOps project if you do not have these resources available.

For more information about Azure Key Vault and pipeline integration, see:

* [Manage application configuration data.](/en-us/training/modules/manage-application-configuration-data/)
* [Use Azure Key Vault secrets in Azure Pipelines.](/en-us/azure/devops/pipelines/release/azure-key-vault/)
* [Azure Key Vault keys, secrets and certificates overview.](/en-us/azure/key-vault/general/about-keys-secrets-certificates)
* [Repository protection](/en-us/azure/devops/pipelines/security/repos/)
* [Plan how to secure your YAML pipelines](/en-us/azure/devops/pipelines/security/approach)
* [Other security considerations](/en-us/azure/devops/pipelines/security/misc)
* [Recommendations to securely structure projects in your pipeline](/en-us/azure/devops/pipelines/security/projects/)

---

## Lab \- Integrate Azure Key Vault with Azure Pipelines

Azure Key Vault provides secure storage and management of sensitive data, such as keys, passwords, and certificates. Azure Key Vault includes support for hardware security modules and a range of encryption algorithms and key lengths. By using Azure Key Vault, you can minimize the possibility of disclosing sensitive data through source code, a common mistake developers make. Access to Azure Key Vault requires proper authentication and authorization, supporting fine\-grained permissions to its content.

In this lab, learn how you can integrate Azure Key Vault with Azure Pipelines.

Note

To complete this lab, you will need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). You will also need to [validate your lab environment](https://aka.ms/mslearn-implement-security-through-pipeline-validate-lab-environment) to complete this lab.

Launch the exercise and follow the instructions.

Tip

To continue your learning journey, open the exercise in a new browser tab or window while staying on this page. To do this, right\-click the **Launch Exercise** button and select **Open link in new tab** or **Open link in new window**.

---

## Summary

In this module, we covered the steps to configure secure access to packages and configure credential secrets and secrets for services in Azure DevOps. Finally, we covered how to use the service connection in a YAML pipeline to access packages securely.

You learned how to:

* Configure pipeline access to packages.
* Configure credential secrets and secrets for services.
* Ensure that the secrets are in the Azure Key Vault.
* Ensure that secrets are not in the logs.

### Learn more

* [Configure permissions.](/en-us/azure/devops/artifacts/feeds/feed-permissions)
* [Set pipeline permissions.](/en-us/azure/devops/pipelines/policies/permissions)
* [Set secret variables](/en-us/azure/devops/pipelines/process/set-secret-variables)
* [Publish and download pipeline Artifacts](/en-us/azure/devops/pipelines/artifacts/pipeline-artifacts)
* [Use Azure Key Vault secrets in Azure Pipelines](/en-us/azure/devops/pipelines/release/azure-key-vault)
* [Review logs to diagnose pipeline issues](/en-us/azure/devops/pipelines/troubleshooting/review-logs)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-secure-access-azure-repos-from-pipelines/_

## Fuentes
- [Configure secure access to Azure Repos from pipelines](https://learn.microsoft.com/en-us/training/modules/configure-secure-access-azure-repos-from-pipelines/?WT.mc_id=api_CatalogApi)
