# Extend a pipeline to use multiple templates

> Curso: Implement security through a pipeline using Azure DevOps (wwl-implement-security-through-pipeline-using-devo) · Seccion: Implement security through a pipeline using Azure DevOps
> Duracion estimada: 63 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Separating YAML pipeline files in multiple repositories, projects, or templates is essential to help improve Azure DevOps security.

Implementing nested templates and tokens, and sensitive information such as credentials, secrets, and other configuration settings, helps abstract the main deployment pipeline and store it in a more secure location. This approach helps to limit the exposure of sensitive information to unauthorized users, reduce the risk of data breaches and prevent unauthorized access to critical resources.

In addition, by separating the pipeline configuration into smaller, more manageable pieces, it's easier to manage changes and version control, which can help to prevent errors and conflicts that can lead to security issues. By applying the power of nested templates, it's also possible to reduce duplication in the pipeline configuration, which can help simplify the pipeline's maintenance and management over time.

In this module, learners can work with Azure DevOps to create nested templates and configure pipelines to use tokenization while also learning to secure pipelines and protect their organization's sensitive information.

#### Learning objectives

After completing this module, students and professionals can:

* Create nested templates.
* Rewrite the main deployment pipeline.
* Configure the pipeline and the application to use tokenization.
* Remove plain text secrets.
* Restrict agent logging.
* Identify and conditionally remove script tasks in Azure DevOps.

By the end of this module, you'll know how to extend a pipeline to use multiple templates and how to secure pipelines to protect their organization's sensitive information.

#### Prerequisites

You must create an Azure DevOps Organization and a Team Project for some exercises. If you don't have them yet, see:

* [Create an organization \- Azure DevOps.](/en-us/azure/devops/organizations/accounts/create-organization)
* [Create a project in Azure DevOps.](/en-us/azure/devops/organizations/projects/create-project)

To get the most out of this course, we recommend that you understand Azure DevOps and pipeline management.

Ensure you have all the necessary resources and access to Azure DevOps before starting the course.

Let's begin!

---

## Create a nested template

A nested template is a reusable YAML file that contains a set of tasks that can be called from another YAML file. This approach can simplify the pipeline's maintenance and management over time and reduce the amount of duplication in the pipeline configuration.

In this unit, learn how to create a nested template using YAML pipelines in Azure DevOps.

### YAML templates and security benefits

Using templates in YAML pipelines can provide several security advantages, such as:

* **Improved secret management:** Nested templates can help you abstract sensitive information such as credentials, secrets, and other configuration settings from the main deployment pipeline, making managing and securing these sensitive items easier. These can be stored in a more secure location or Azure Key Vault, reducing the exposure of sensitive information to unauthorized users and preventing unauthorized access to critical resources.
* **Reduced risk of data breaches:** By abstracting sensitive information from the main deployment pipeline, you reduce the risk of data breaches that can occur when sensitive information is exposed to unauthorized users or stored in an insecure location.
* **Easier permissions management and access:** With nested templates, you can better manage access control to the templates and configuration files, giving you granular control over who can access and modify specific pipeline components.
* **Better pipeline version control:** Separating pipeline configuration into smaller, more manageable pieces makes it easier to manage changes and version control, which can help prevent errors and conflicts that can lead to security issues.
* **Simplified pipeline maintenance:** By applying the power of nested templates, it's possible to reduce duplication in the pipeline configuration, which can help simplify the pipeline's maintenance and management over time.

### Create a YAML file for the nested template

Create a YAML file in your Git repository called `secure-template.yaml`. This file contains the pipeline's tasks that you want to reuse in other YAML files.

```
parameters:
  message: ''

steps:
- task: PowerShell@2
  inputs:
    targetType: Inline
    script: |
      Write-Host "${{ parameters.message }}"
      Write-Host "$(Secure)"

```

In this example, we define one parameter `message`, and a single PowerShell task that prints the values of the parameter. We also print the value of the `Secure` variable, which is a variable that we'll define in the next step.

### Create a YAML file for the main pipeline

Create a YAML file called `main-pipeline.yaml` for the pipeline that calls the nested template. You can use the `template` property to call the nested template.

```
name: 'Pipeline templates'
stages:
- stage: Build
  displayName: 'Securing pipelines with templates'
  jobs:
  - job: Build
    pool:
      vmImage: windows-latest
    variables:
    - name: Secure
      value: 'Secret!'
    steps:
    - template: '../.secure/secure-template.yaml'
      parameters:
        message: 'This is from the main template!'

```

In this example, we call the `secure-template.yaml` file from a ".secure" folder using the `template` property and pass the values of the `message` and `Secure` parameters to the nested template.

### Create a new pipeline

Navigate to your Azure DevOps project and create a new pipeline. Select the repository and branch where you committed the changes. Select the YAML file for the main pipeline (`main-pipeline.yaml` in our example) and run the pipeline.

Verify that the nested template is called and the values of the parameters are printed.

### Challenge yourself

Create a reusable template for a common task in your organization's deployment pipeline. It can be anything from creating a resource group to deploying a specific application.

1. Identify a task that is performed frequently in your organization's deployment pipeline.
2. Create a template that can be used to automate that task.
3. Test the template by using it in a simple deployment pipeline.
4. (Optional) Consider creating a new YAML pipeline that uses the template you created and configure it to use tokenization to secure sensitive information.

For more information about templates and YAML pipelines, see:

* [Security through templates.](/en-us/azure/devops/pipelines/security/templates)
* [Template types \& usage.](/en-us/azure/devops/pipelines/process/templates/)
* [Securing Azure Pipelines.](/en-us/azure/devops/pipelines/security/overview/)
* [Recommendations to securely structure projects in your pipeline.](/en-us/azure/devops/pipelines/security/projects/)

---

## Rewrite the main deployment pipeline

Azure Pipelines allows you to define build and release processes using YAML templates. Templates are reusable and enable you to define your pipelines declaratively. It means you can define your pipelines as code, commit the code to your source control repository, and have it versioned and managed like any other code.

In this unit, examine the template types to use YAML templates in Azure Pipelines and rewrite the main deployment pipeline with examples of template usage.

### Template types and usage

Azure Pipelines supports four types of templates:

* **Stage template** \- You can use a stage template to define a stage you want to reuse in multiple pipelines. For example, you can specify a stage template that deploys an application to a specific environment. You can reuse the stage template in multiple pipelines to deploy the application to different environments.
* **Job template** \- You can define a job template that builds a specific application. You can reuse the job template in multiple pipelines to build the application for different platforms.
* **Step template** \- You can define a step template that creates a resource group. You can reuse the step template in multiple pipelines to create a resource group for different applications.
* **Variable template** \- You can define a variable template that establishes a connection string to a database. You can reuse the variable template in multiple pipelines to connect to the database.

#### Stage template

You can define a set of stages in one file and use it multiple times in other files.

In this example, a stage is repeated twice for two testing regimes. The stage itself is specified only once.

```
## File: stages/test.yaml

parameters:
  name: ''
  testFile: ''

stages:

- stage: Test_${{ parameters.name }}
  jobs:

  - job: ${{ parameters.name }}_Windows
    pool:
      vmImage: windows-latest
    steps:

    - script: npm install
    - script: npm test -- --file=${{ parameters.testFile }}

  - job: ${{ parameters.name }}_Mac
    pool:
      vmImage: macOS-latest
    steps:

    - script: npm install
    - script: npm test -- --file=${{ parameters.testFile }}

```

Templated pipeline:

```
## File: azure-pipelines.yaml
stages:

- template: stages/test.yaml # Template reference
  parameters:
    name: Mini
    testFile: tests/miniSuite.js

- template: stages/test.yaml
  parameters:
    name: Full
    testFile: tests/fullSuite.js

```

#### Job templates

You can define a set of jobs in one file and use it multiple times in others.

In this example, a single job is repeated on three platforms. The job itself is specified only once.

```
## File: jobs/build.yaml

parameters:
  name: ''
  pool: ''
  sign: false

jobs:

- job: ${{ parameters.name }}
  pool: ${{ parameters.pool }}
  steps:

  - script: npm install
  - script: npm test

  - ${{ if eq(parameters.sign, 'true') }}:
    - script: sign

```

Templated pipeline:

```
## File: azure-pipelines.yaml

jobs:

- template: jobs/build.yaml  # Template reference
  parameters:
    name: macOS
    pool:
      vmImage: 'macOS-latest'

- template: jobs/build.yaml  # Template reference
  parameters:
    name: Linux
    pool:
      vmImage: 'ubuntu-latest'

- template: jobs/build.yaml  # Template reference
  parameters:
    name: Windows
    pool:
      vmImage: 'windows-latest'
    sign: true  # Extra step on Windows only

```

#### Step templates

You can define a set of steps in one file and use it multiple times in another.

```
## File: steps/build.yaml

steps:

- script: npm install
- script: npm test

```

Templated pipeline:

```
## File: azure-pipelines.yaml

jobs:

- job: macOS
  pool:
    vmImage: 'macOS-latest'
  steps:

  - template: steps/build.yaml # Template reference

- job: Linux
  pool:
    vmImage: 'ubuntu-latest'
  steps:

  - template: steps/build.yaml # Template reference

- job: Windows
  pool:
    vmImage: 'windows-latest'
  steps:

  - template: steps/build.yaml # Template reference
  - script: sign              # Extra step on Windows only

```

#### Variable templates

You can define a set of variables in one file and use it multiple times in other files.

In this example, a set of variables is repeated across multiple pipelines. The variables are specified only once.

```
## File: variables/build.yaml
variables:

- name: vmImage
  value: windows-latest

- name: arch
  value: x64

- name: config
  value: debug

```

Templated pipelines:

```
## File: component-x-pipeline.yaml
variables:

- template: variables/build.yaml  # Template reference
pool:
  vmImage: ${{ variables.vmImage }}
steps:

- script: build x ${{ variables.arch }} ${{ variables.config }}

```

```
## File: component-y-pipeline.yaml
variables:

- template: variables/build.yaml  # Template reference
pool:
  vmImage: ${{ variables.vmImage }}
steps:

- script: build y ${{ variables.arch }} ${{ variables.config }}

```

### Challenge yourself

Create a reusable template for a common task in your organization's deployment pipeline. It can be anything from creating a resource group to deploying a specific application.

For more information about templates and YAML pipelines, see:

* [Security through templates.](/en-us/azure/devops/pipelines/security/templates)
* [Template types \& usage.](/en-us/azure/devops/pipelines/process/templates/)

---

## Configure the pipeline and the application to use tokenization

Azure Key Vault is a secure secret, key, and certificate store. Azure Key Vault can ensure that your tokens and secrets are stored securely and easily accessed by your pipeline without exposing them in plain text. Azure Pipelines provides built\-in tasks that enable you to retrieve secrets from Azure Key Vault during pipeline execution.

In this unit, learn ways to use Azure Key Vault with YAML pipelines for security tokens and secrets management.

### Prerequisite

Azure Key Vault, Service Principal and YAML Pipeline. Follow the steps to create the resources: [Use Azure Key Vault to secure secrets](/en-us/training/modules/configure-secure-access-azure-repos-from-pipelines/5-use-azure-key-vault-secure-secrets)

### Reference Azure Key Vault in a variable group

One way to use Azure Key Vault with YAML pipeline templates is to create a variable group that references the Key Vault. Here are the steps:

1. In Azure DevOps, click on Library under Pipelines.
2. Create a new variable group or use existing groups.
3. Give the variable group a name and description.
4. Under Variables, add a new variable and set its value to `$(keyVaultSecret)`. Use this variable to retrieve the secret from Azure Key Vault.
5. Under Link secrets, link the variable group to your Azure Key Vault and grant read access to the service principal that will be used to access the Key Vault.
6. Save the variable group.

Now, you can reference the variable group in your YAML pipeline templates using the following syntax:

```
variables:
- group: <variable group name>

steps:
- task: AzureKeyVault@2
  inputs:
    azureSubscription: '<Azure subscription service connection>'
    KeyVaultName: '<Key Vault name>'
    SecretsFilter: '*'
    RunAsPreJob: true

```

### Pass Azure Key Vault secret as a parameter

Another way to use Azure Key Vault with YAML pipeline templates is to pass the secret as a parameter to the template.

1. In Azure DevOps, create a new pipeline and choose YAML.
2. In the pipeline, define a parameter for the secret:

```
parameters:
  - name: keyVaultSecret
    type: string

```
3. In the pipeline, use the AzureKeyVault task to retrieve the secret:

```
steps:
- task: AzureKeyVault@2
  inputs:
    azureSubscription: '<Azure subscription service connection>'
    KeyVaultName: '<Key Vault name>'
    SecretsFilter: '$(keyVaultSecret)'

```
4. In the pipeline, pass the secret as a parameter to the template:

```
- template: template.yaml
  parameters:
    keyVaultSecret: $(keyVaultSecret)

```

Replace `<Azure subscription service connection>` and `<Key Vault name>` with your own values.

### Use Azure Key Vault with variables and tokens

A third way to use Azure Key Vault with YAML pipeline templates is to combine variables, tokens, and Azure Key Vault.

1. Set the value of the variable to `$(keyVaultSecret)` and mark it as a secret. Use variable to retrieve the secret from Azure Key Vault.
2. In your YAML pipeline template, use the `$(keyVaultSecret)` variable to retrieve the secret from Azure Key Vault:

```
steps:
- task: AzureKeyVault@2
  inputs:
    azureSubscription: '<Azure subscription service connection>'
    KeyVaultName: '<Key Vault name>'
    SecretsFilter: '$(keyVaultSecret)'

```
3. To tokenize the value of the secret, use the `$(keyVaultSecret)` variable in your pipeline:

```
steps:
- script: |
    echo $(keyVaultSecret)

```

This outputs the value of the secret at runtime.
4. If you want to use the secret as an environment variable in your pipeline, you can set the environment variable in a script step:

```
steps:
- task: AzureKeyVault@2
  inputs:
    azureSubscription: '<Azure subscription service connection>'
    KeyVaultName: '<Key Vault name>'
    SecretsFilter: '$(keyVaultSecret)'
- script: |
    export MY_SECRET=$(keyVaultSecret)    

```

This sets the `MY_SECRET` environment variable to the value of the secret.

### Best practices for using Azure Key Vault with YAML pipelines

1. Use a separate Key Vault for each environment. For example, use one Key Vault for production secrets and another for development secrets.
2. Assign minimum required permissions to the service principal that accesses the Key Vault.
3. Use the latest version of the AzureKeyVault task in your pipeline.
4. Ensure Azure Key Vault soft delete is enabled to protect against accidental deletion of secrets and keys.

### Challenge yourself

Create a new YAML pipeline that deploys an Azure Resource Manager template that references a secret stored in Azure Key Vault. Use the AzureKeyVault task to retrieve the secret and pass it as a parameter to the template. Verify that the pipeline can successfully deploy the template without exposing the secret in plain text.

**Suggested Lab:** [Integrate Azure Key Vault with Azure DevOps](/en-us/training/modules/manage-application-configuration-data/11-integrate-azure-key-vault-with-azure-devops/)

For more information about Azure Key Vault and YAML pipelines, see:

* [Manage application configuration data.](/en-us/training/modules/manage-application-configuration-data/)
* [Use Azure Key Vault secrets in Azure Pipelines.](/en-us/azure/devops/pipelines/release/azure-key-vault/)
* [Use Azure Key Vault in your YAML Pipeline.](/en-us/azure/devops/pipelines/release/key-vault-in-own-project/)
* [Azure Key Vault recovery management with soft delete and purge protection.](/en-us/azure/key-vault/general/key-vault-recovery)
* [Add \& use variable groups.](/en-us/azure/devops/pipelines/library/variable-groups)

---

## Remove plain text secrets

Disclosing sensitive information like passwords, API keys, or database connection strings can lead to serious security risks, such as data breaches, unauthorized access to systems, or even financial losses. It's essential to ensure plain text secrets aren't stored or transmitted insecurely.

Removing plain text secrets and replacing them with variables or tokens is a best practice that allows teams to securely store and manage their sensitive information while still being able to use it in their pipelines or applications.

By using secure methods like FileTransform, Azure Key Vault, or other tools, teams can ensure pipelines and applications are built and deployed securely and reliably while keeping their sensitive information safe from prying eyes.

There are many ways to create a secure application using Azure Pipelines for each technology and type of application you're building.

In this unit, learn to use Azure Pipelines to create a secure .NET application. You'll create tokens for database connections or variables, create a YAML pipeline, and remove plain text secrets.

### Prerequisites

* An Azure DevOps organization.
* A .NET application or eShopOnWeb from Step 1\.
* [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/), VS Code or another IDE that supports .NET Core.
* An Azure subscription.

### Import eShopOnWeb to your Azure DevOps repository

The repository is organized the following way:

* .ado folder contains Azure DevOps YAML pipelines.
* .devcontainer folder container set up to develop using containers (either locally in VS Code or GitHub Codespaces).
* .Azure folder contains Bicep \& ARM template infrastructure as code templates.
* src folder contains the .NET 6 website used on the lab scenarios.

To import the repository to your Azure DevOps organization, follow these steps:

1. From your Azure DevOps organization, choose the project you want to import the eShopOnWeb application into.
2. Open the Repos tab and click on Import repository.
3. On the Import a repository page, click on Import a repository link (below the page title).
4. Add the following information:
Repository type: Git
Clone URL: <https://github.com/MicrosoftLearning/eShopOnWeb.git>
Name: eShopOnWeb
5. Click on Import and wait for your repository to be ready.

Note

For more information about how to import a git repository, see: [Import a Git repo](/en-us/azure/devops/repos/git/import-git-repository/)

### Create tokens for database connections or variables

The first step in creating a secure application is listing all the secrets you want to replace, such as database connections or variables with sensitive information stored securely and referenced in your code or pipeline.

1. Open your .NET application in VS Code or Visual Studio.
2. Find the secrets you want to replace. For example, you can find the database connection string in the `appsettings.json` file, inside the Web project from the src folder.
3. Add your database connection string or any other sensitive information to the JSON file using the following format:

```
{
    "ConnectionStrings": {
        "CatalogConnection": "Server=(localdb)\\mssqllocaldb;Integrated Security=true;Initial Catalog=Microsoft.eShopOnWeb.CatalogDb;",
        "IdentityConnection": "Server=(localdb)\\mssqllocaldb;Integrated Security=true;Initial Catalog=Microsoft.eShopOnWeb.Identity;"
      },
    "ReleaseVersion":  "1.0"
}

```
4. Replace the sensitive information with placeholders.

```
{
    "ConnectionStrings": {
        "CatalogConnection": "CatalogConnectionToken",
        "IdentityConnection": "IdentityConnectionToken"
      },
    "ReleaseVersion":  "ReleaseVersionToken"
}

```

Important

You can use the actual information, or a token like `ConnectionToken` or `ReleaseVersion` as value. It will be replaced in the pipeline.
5. Save the changes to the JSON file, and commit/push your changes to the repository.

### Create a new variable group

The next step is to create a new variable group in Azure DevOps to store the tokens you created in Step 1\.

1. Open Azure DevOps and navigate to your project.
2. Click on "Library" and then "Variable groups."
3. Click on "Create variable group" and add the variables you want to store securely and replace in your `appsettings.json`:
	* Name: eShopOnWeb
	* Variables:
		+ **CatalogConnectionToken**: Server\=MYSERVER;Integrated Security\=true;Initial Catalog\=Microsoft.eShopOnWeb.CatalogDb;
		+ **IdentityConnectionToken**: Server\=MYSERVER;Integrated Security\=true;Initial Catalog\=Microsoft.eShopOnWeb.Identity;
		+ **ReleaseVersionToken**: 1\.1
4. Make sure to click on the "Lock" icon to secure the variable.
5. Click on "Save" to create the variable group.

### Create a YAML pipeline and import the variable group

The next step is to create a YAML pipeline in Azure Pipelines or use existing definitions. This pipeline builds your application and references the tokens you created in Step 1\.

1. Open Azure DevOps and navigate to your project.
2. Click on "Pipelines" and then "New pipeline."
3. Select Azure Repos Git as the source of the code and select the repository that contains the application. You can choose the eShopOnWeb repository you imported in Step 1\."
4. Select "Existing Azure Pipelines YAML file" and choose the existing `eshoponweb-ci.yml` from the `.ado` folder and Click on Continue.
5. In the YAML editor, import the variable group created in Step 2 by adding the following code to the top of the file:

```
variables:
- group: eShopOnWeb
- name: ConnectionStrings.CatalogConnection
  value: '$(CatalogConnectionToken)'
- name: ConnectionStrings.IdentityConnection
  value: '$(IdentityConnectionToken)'
- name: ReleaseVersion
  value: '$(ReleaseVersionToken)'

```

Important

You need to provide the correct variable names, starting with the root node name, in this example `ConnectionStrings.CatalogConnection` and `ConnectionStrings.IdentityConnection`. You can find the correct names in the `appsettings.json` file.
6. Add the File Transform task code to the steps:

```
variables:
- group: eShopOnWeb

- task: FileTransform@1
  inputs:
    folderPath: '$(System.DefaultWorkingDirectory)/src/web'
    fileType: 'json'
    targetFiles: 'appsettings.json'

```
7. Click on "Save" to save the pipeline file with the new task, and commit.

### Run your release pipeline

The last step is to run your release pipeline to build your application and replace the tokens with the values you stored in the variable group.

1. Click on "Pipelines" under the "Pipelines" tab and then click on the pipeline you created in Step 3\.
2. Click on "Run pipeline" and then click on "Run".
3. Once the pipeline is completed, you can see the tokens replaced with the values you stored in the variable group in the `appsettings.json` file. Check your pipeline log results to see the tokens replaced:

Important

In this example we did not encrypt the variable `CatalogConnectionToken` to show the value in the log. In a real scenario, you need to encrypt the variable to avoid exposing the value in the log.
4. Open the Artifacts from your pipeline execution results and download the **`Web.zip`** file.
5. Unzip the file and open the `appsettings.json` file. You can see the tokens replaced with the values you stored in the variable group.

For more information about file transformation and variables substitution in YAML pipelines, see:

* [File transforms and variable substitution reference.](/en-us/azure/devops/pipelines/tasks/transforms-variable-substitution)
* [FileTransform@1 \- File transform v1 task.](/en-us/azure/devops/pipelines/tasks/reference/file-transform-v1)
* [YAML schema reference for Azure Pipelines.](/en-us/azure/devops/pipelines/yaml-schema/)
* [Customize your pipeline.](/en-us/azure/devops/pipelines/customize-pipeline)

---

## Restrict agent logging

When building and deploying applications with Azure Pipelines, it's crucial to ensure pipeline agents don't inadvertently log sensitive information like passwords, API keys, or other secrets. It can happen if sensitive information is printed to the console during the build or deployment process, leading to serious security risks.

In this unit, learn and review how to configure Azure Pipelines and YAML pipelines to restrict agent logging of secrets using best practices and secure methods.

### Log of secrets

Azure Pipelines attempts to scrub secrets from logs wherever possible. This filtering is on a best\-effort basis and can't catch every way in which secrets can be leaked. Avoid echoing secrets to the console, using them in command line parameters, or logging them to files.

### Use the audit service

Many pipeline events are recorded in the Auditing service. Review the audit log periodically to ensure no malicious changes have slipped past. Visit `https://dev.azure.com/ORG-NAME/_settings/audit` to get started.

### Ways to restrict agent logging of secrets

When working with Azure Pipelines, it's common to use service connections, which add a new layer of security for sensitive information such as usernames, passwords, and API keys. Without service connections or other best practices, pipelines are left unsecured and their information can be easily accessed and exposed in pipeline logs, leading to potential data breaches and security risks.

By following these suggestions and the ones we covered in other units, you can ensure that your sensitive information is kept safe and your pipeline remains a trusted and reliable tool for your organization.

* **Use Azure Key Vault:** You can store sensitive information, such as passwords and API keys, separately from your pipeline in Azure Key Vault. You can reference these secrets in your pipeline without revealing them in the pipeline logs. To use Azure Key Vault, you can create a new Azure Key Vault instance, add your secrets to the vault, and then reference them in your pipeline using the Azure Key Vault task.
* **Use Variable Groups:** Variable Groups are a convenient way to store and manage variables used across multiple pipelines. You can create a new variable group, add sensitive information as variables, and then reference them in your pipeline. By marking these variables as "secret," you can ensure they aren't displayed in the pipeline logs.
* **Use Environment Variables:** You can also use environment variables to store your sensitive information. Environment variables are a way to store data that can be accessed by processes running on the same machine. In Azure Pipelines, you can define pipeline, job, or task environment variables. By marking these variables as "secret," you can ensure they aren't displayed in the pipeline logs.

Regardless of your chosen method, it's crucial to ensure that your sensitive information isn't easily accessible in your pipeline logs.

### Use agent\-level logging restrictions

Another way to restrict agent logging of secrets is to use agent\-level logging restrictions. These restrictions can prevent specific commands or log levels from being printed to the console, which can further reduce the risk of exposing sensitive information.

To use agent\-level logging restrictions, follow these steps:

1. Edit your pipeline.
2. Select Variables.
3. Add a new variable with the name `System.Debug` and value true.
4. Save the new variable.
5. Run your pipeline to see the logs.

The setting `System.Debug=False` turns off verbose logs for all runs. With the Enable system diagnostics checkbox, you can also configure verbose logs for a single run. For more information, see [Review logs to diagnose pipeline issues.](/en-us/azure/devops/pipelines/troubleshooting/review-logs)

### Use the issecret parameter

The `issecret` parameter allows you to mask secrets in the agent logs.

To set a variable as a script with a logging command, you need to pass the `issecret` flag.

When `issecret` is set to true, the value of the variable will be saved as secret and masked out from log.

Set the secret variable `mySecretVal`.

```
- powershell: |
    Write-Host "##vso[task.setvariable variable=mySecretVal;issecret=true]secretvalue"

```

Get the secret variable mySecretVal.

```
- powershell: |
    Write-Host "##vso[task.setvariable variable=mySecretVal;issecret=true]secretvalue"
- powershell: |
    Write-Host $(mySecretVal)

```

Output of PowerShell variable.

```
***
Finishing: Powershell

```

### Challenge yourself

Create a new YAML pipeline with a task that logs a secret variable to the agent logs. Configure the pipeline to mask the secret in the logs by using the `issecret` parameter.

For more information about secrets, see:

* [Set secret variables.](/en-us/azure/devops/pipelines/process/set-secret-variables)
* [How to securely use variables and parameters in your pipeline.](/en-us/azure/devops/pipelines/security/inputs/)
* [Plan how to secure your YAML pipelines.](/en-us/azure/devops/pipelines/security/approach/)
* [Recommendations to securely structure projects in your pipeline.](/en-us/azure/devops/pipelines/security/projects/)

---

## Identify and conditionally remove script tasks

Azure Pipelines allow the execution of custom scripts during pipeline run\-through script tasks. However, certain conditions may require the removal of script tasks, such as the pipeline stage or the branch being built. It can streamline pipeline execution and reduce unnecessary overhead.

Script tasks in pipelines pose a security risk by allowing the execution of arbitrary code on the agent machine, potentially leading to sensitive information exposure and malicious code execution.
Minimizing the risk of exposing sensitive information involves identifying and conditionally removing script tasks, for example, removing a script task altogether or replacing it with a more secure alternative when it includes a command that prints a password or a secret key.

Setting up conditions for script tasks can further reduce the risk of exposing sensitive information. For instance, removing a script task that is unnecessary for a specific pipeline stage can limit the attack surface for potential attackers and decrease the likelihood of a security breach.

This unit demonstrates how to identify and conditionally remove script tasks using Azure Pipelines and YAML pipelines.

### Identify the script tasks to be removed

To start, you need to identify the script tasks that require removal based on specific conditions. You can accomplish this by utilizing expressions in the YAML pipeline.

For instance, if a script task isn't necessary for a specific stage of the pipeline, you may want to remove it from that stage. To do this, you can use the "condition" property in the YAML pipeline to specify an expression that determines whether the script task should be executed.

```
jobs:
- job: Build
  steps:
  - script: |
      echo "This script task should only run during the Build stage"
    condition: eq(variables['System.StageName'], 'Build')
  - script: |
      echo "This script task should run during all stages"

```

In this example, the first script task will only run if the stage name is "Build", while the second script task runs during all stages.

It allows you to remove the first script task from the pipeline without removing the second script task. It also allows you to reuse the second script task in other pipeline stages. It's helpful to run the same script task in multiple stages. For example, you may want to run a script task to build a project in the "Build" stage and then run the same script task to deploy the project in the "Deploy" stage.

### Use the condition property

To conditionally remove a script task, utilize the "condition" property in the YAML pipeline. This property empowers you to define an expression that determines whether the script task should execute.

For instance, to remove a script task if a specific variable is unset, utilize the following expression:

```
jobs:
- job: Build
  steps:
  - script: |
      echo "This script task will only run if MY_VARIABLE is set"
    condition: ne(variables['MY_VARIABLE'], '')

```

In this example, the script task will only run if the `MY_VARIABLE` variable is set.

### Test the pipeline

Once you have made changes to the YAML pipeline, it's crucial to test it to guarantee that the script tasks are correctly removed.

Testing the pipeline entails running it and validating that the script tasks aren't executed when they should be removed.

### Challenge yourself

Create a new YAML pipeline that conditionally removes a script task based on the branch being built. Verify that the script task isn't executed when building the specified branch.

For more information about pipeline conditions and decorators, see:

* [Specify conditions.](/en-us/azure/devops/pipelines/process/conditions/)
* [Pipeline decorator expression context.](/en-us/azure/devops/extend/develop/pipeline-decorator-context/)
* [Runtime parameters.](/en-us/azure/devops/pipelines/process/runtime-parameters/)
* [Expressions.](/en-us/azure/devops/pipelines/process/expressions/)

---

## Lab \- Extend a pipeline to use multiple templates

In this lab, explore the importance of extending a pipeline to multiple templates and how to do it using Azure DevOps. This lab covers fundamental concepts and best practices for creating a multi\-stage pipeline, creating a variables template, creating a job template, and creating a stage template.

Note

To complete this lab, you will need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). You will also need to [validate your lab environment](https://aka.ms/mslearn-implement-security-through-pipeline-validate-lab-environment) to complete this lab.

Launch the exercise and follow the instructions.

Tip

To continue your learning journey, open the exercise in a new browser tab or window while staying on this page. To do this, right\-click the **Launch Exercise** button and select **Open link in new tab** or **Open link in new window**.

---

## Summary

In this module, you learned the importance of extending a pipeline to multiple templates and how to do it using Azure DevOps. The module covered fundamental concepts and best practices for creating nested templates, rewriting the main deployment pipeline, configuring the pipeline and the application to use tokenization, removing plain text secrets, restricting agent logging, and identifying and conditionally removing script tasks.

You learned how to:

* Create nested templates.
* Rewrite the main deployment pipeline.
* Configure the pipeline and the application to use tokenization.
* Remove plain text secrets.
* Restrict agent logging.
* Identify and conditionally remove script tasks in Azure DevOps.

### Learn more

* [Security through templates.](/en-us/azure/devops/pipelines/security/templates)
* [Template types \& usage.](/en-us/azure/devops/pipelines/process/templates/)
* [Securing Azure Pipelines.](/en-us/azure/devops/pipelines/security/overview/)
* [Recommendations to securely structure projects in your pipeline.](/en-us/azure/devops/pipelines/security/projects/)
* [File transforms and variable substitution reference.](/en-us/azure/devops/pipelines/tasks/transforms-variable-substitution)
* [Set secret variables.](/en-us/azure/devops/pipelines/process/set-secret-variables)
* [How to securely use variables and parameters in your pipeline.](/en-us/azure/devops/pipelines/security/inputs/)
* [Plan how to secure your YAML pipelines.](/en-us/azure/devops/pipelines/security/approach/)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/extend-pipeline-use-multiple-templates/_

## Fuentes
- [Extend a pipeline to use multiple templates](https://learn.microsoft.com/en-us/training/modules/extend-pipeline-use-multiple-templates/?WT.mc_id=api_CatalogApi)
