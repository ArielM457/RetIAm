# Configure pipelines to securely use variables and parameters

> Curso: Implement security through a pipeline using Azure DevOps (wwl-implement-security-through-pipeline-using-devo) · Seccion: Implement security through a pipeline using Azure DevOps
> Duracion estimada: 44 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Using variables and parameters is a crucial part of Azure DevOps. They allow you to store and manage values that can be used across your pipelines, making managing your resources and configurations easier. However, if not used securely, they can pose a significant risk to your organization's security and confidentiality.

In this module, learn the fundamental concepts of variables and parameters, identify and restrict the insecure use of variables and parameters and move parameters into a YAML file that protects their kind. Explore limiting variables that can be set at queue time and validate that mandatory variables are present and set correctly.

#### Learning objectives

After completing this module, students and professionals can:

* Ensure that parameters and variables retain their type.
* Identify and restrict insecure use of parameters and variables.
* Move parameters into a YAML file that protects their type.
* Limit variables that can be set at queue time.
* Validate that mandatory variables are present and set correctly in Azure DevOps.

#### Prerequisites

For some exercises, you must create an Azure DevOps Organization and a Team Project. If you don't have them yet, see the following:

* [Create an organization \- Azure DevOps.](/en-us/azure/devops/organizations/accounts/create-organization)
* [Create a project in Azure DevOps.](/en-us/azure/devops/organizations/projects/create-project)

We recommend you understand Azure DevOps and pipeline management to get the most out of this course.

Ensure you have all the necessary resources and access to Azure DevOps before starting the course.

Let's begin!

---

## Ensure parameter and variable types

Parameters and variables are essential components for customizing pipeline behavior. These enable passing runtime values to pipeline tasks and scripts and defining variables for use across different pipeline stages. When using parameters and variables in pipelines, it's crucial to define their data types correctly to avoid any unexpected behavior that could affect the project's security or pipeline execution.

### Parameter and variable types

Parameters and variables are critical to pipeline customization, as they allow for flexibility and enable pipeline scripts to be more dynamic. You can use them to store values such as connection strings, environment variables, and other sensitive data. Properly defining their data types is also essential to avoid unexpected errors or vulnerabilities arising from incorrect usage.

### Add a parameter or variable to your pipeline

```
parameters:
- name: myParameterName
  type: myDataType
  default: myDefaultValue

variables:
- name: myReadOnlyVar
  value: myValue
  readonly: true

```

Replace `myParameterName`, `myDataType`, `myDefaultValue`, `myReadOnlyVar`, and `myValue` with your desired values.

Example:

```
parameters:
- name: image
  displayName: Pool Image
  type: string
  default: ubuntu-latest
  values:
  - windows-latest
  - ubuntu-latest
  - macOS-latest

variables:
 - name: eShopOnWeb
   value: myValue   

```

### Use the correct data types when defining your parameters

Azure Pipelines supports the following data types:

* string
* boolean
* number
* object
* step

Unlike variables, pipeline parameters can't be changed by a pipeline while it's running. Parameters have data types such as `number` and `string`, and they can be restricted to a subset of values. Restricting the parameters is useful when a user\-configurable part of the pipeline should take a value only from a constrained list. The setup ensures that the pipeline won't take arbitrary data.

### Define secrets as secret variables or as a part of a variable group

You can use Azure Key Vault to store secrets and then reference them in your pipeline script.

Example:

```
variables:
 - name: eShopOnWeb
   value: myValue

## You can define variable groups to reuse variables across pipelines
## and to manage sensitive data centrally.

variables:
- group: eShopOnWeb
- name: ConnectionStrings.CatalogConnection
  value: '$(CatalogConnectionToken)'

```

### Use the `readonly` property to ensure that variables aren't changed by a pipeline while it's running

It's useful when you want to ensure that a variable isn't changed by a pipeline while it's running. For example, you can use this property to ensure that a variable isn't changed by a pipeline while it's running.

Example:

```
variables:
- name: eShopOnWeb
  value: myValue
  readonly: true

```

### Challenge yourself

A great way to practice ensuring parameter and variable types is to create a pipeline that uses parameters and variables. Define your parameters and variables using the correct syntax and type\-safe language. Then, use parameter validation to ensure that the pipeline runs correctly. Finally, use secure variable groups to protect any sensitive information. Test your pipeline to ensure it works as expected, and use the pipeline logs to troubleshoot any issues.

Also, try to create a YAML pipeline that includes a parameter with an incorrect type and run it. Then, correct the error by declaring the correct type for the parameter and rerunning the pipeline. It helps you understand the importance of retaining the type of parameters and variables in the pipeline code.

For more information about variables and parameters, see:

* [Securing Azure Pipelines.](/en-us/azure/devops/pipelines/security/overview/)
* [How to securely use variables and parameters in your pipeline.](/en-us/azure/devops/pipelines/security/inputs/)
* [Recommendations to secure shared infrastructure in Azure Pipelines.](/en-us/azure/devops/pipelines/security/infrastructure/)
* [Runtime parameters.](/en-us/azure/devops/pipelines/process/runtime-parameters/)
* [Use a variable group's secret and nonsecret variables in an Azure Pipeline.](/en-us/azure/devops/pipelines/scripts/cli/pipeline-variable-group-secret-nonsecret-variables)
* [Define variables.](/en-us/azure/devops/pipelines/process/variables/)

---

## Identify and restrict insecure use of parameters and variables

In Azure Pipelines, parameters and variables can be used to pass runtime values to pipeline tasks and scripts and to define variables that can be used across different pipeline stages. However, if not correctly secured, parameters and variables can become a security vulnerability, as they can store sensitive information such as connection strings, API keys, and other credentials.

In this unit, identify and restrict insecure use of parameters and variables in Azure Pipelines.

### Why is secure usage of parameters and variables important?

Secure usage of parameters and variables is essential to ensure the security of your pipeline and the projects it supports. Insecure parameters and variables can lead to data breaches, unauthorized access, and other security risks. They can also lead to unexpected behavior or errors that can impact the reliability and stability of your pipeline.

### Identify insecure use of parameters and variables

Here are some steps to identify insecure use of parameters and variables in Azure Pipelines:

* Check your pipeline YAML file for any parameters or variables storing sensitive information, such as connection strings or credentials.
* Check that the values of these parameters or variables aren't hard\-coded in the pipeline tasks or script used by your tasks, for example, bash, PowerShell, etc. Instead, they should be defined as secure pipeline inputs, such as a secure file or variable group.
* Use the Azure DevOps Pipeline Audit log to monitor the usage of parameters and variables in your pipeline and identify any potential security risks or vulnerabilities.
* Check your template files for any parameters or variables storing sensitive information.
* Check your repository for any parameters or variables storing sensitive information, for example, `appconfig.json`, `appsettings.json`, `secrets.json`, etc.

### Restrict insecure use of parameters and variables

Here are some steps to restrict the insecure use of parameters and variables in Azure Pipelines:

* Define your parameters and variables as secure pipeline inputs, such as a secure file, secret variables, or variable group.
* Use Azure Key Vault to store sensitive data, such as connection strings, API keys, or certificates and then reference them in your pipeline script.
* Link your Azure Key Vault to your Azure DevOps organization and then use the Azure Key Vault task to retrieve the secrets from your Azure Key Vault and use them in your pipeline.
* Use service connections with service principal authentication.
* Restrict access to sensitive data by setting appropriate permissions and access control policies. For example, limit access to pipeline variables and parameters to specific users or groups.

### Challenge yourself

Create a YAML pipeline that deploys a web application to an Azure App Service. Add parameters and variables to the pipeline that define the target environment, database connection string, and other sensitive data. Use the steps described in this unit to ensure that the parameter and variable usage is secure and that sensitive data is securely stored and managed. Test the pipeline, and make sure that the pipeline executes as expected while maintaining the security of the sensitive data in your log and validating the Audit Log.

For more information about variables and parameters, see:

* [Securing Azure Pipelines.](/en-us/azure/devops/pipelines/security/overview/)
* [Runtime parameters.](/en-us/azure/devops/pipelines/process/runtime-parameters/)
* [Security best practices.](/en-us/azure/devops/organizations/security/security-best-practices/)

---

## Move parameters into a YAML file

In Azure Pipelines, you can use YAML files to define your pipeline's configuration as code. Parameters in YAML files help you to reuse the pipeline and keep the code clean. In this unit, you'll learn how to move parameters into a YAML file.

### Why use parameters in YAML files?

Benefits of using parameters in YAML files:

* It helps in reusing the pipeline configuration.
* It enables you to define the pipeline as code, allowing you to track pipeline changes over time.
* It keeps the code clean and organized.

### Move parameters into a YAML file

You can enforce that a pipeline extends from a particular template to increase security.

In the following example, the file parameters.yml defines the parameter buildSteps, which is then used in the pipeline azure\-pipelines.yml. In parameters.yml, if a buildStep gets passed with a script step, it's rejected, and the pipeline build fails.

Create a file named `parameters.yml` in your repository, or other repository specific for your templates.

Define your parameters in this file using the YAML syntax:

```
## File: parameters.yml
parameters:
- name: buildSteps # the name of the parameter is buildSteps
  type: stepList # data type is StepList
  default: [] # default value of buildSteps
stages:
- stage: secure_buildstage
  pool:
    vmImage: windows-latest
  jobs:
  - job: secure_buildjob
    steps:
    - script: echo This happens before code 
      displayName: 'Base: Pre-build'
    - script: echo Building
      displayName: 'Base: Build'

    - ${{ each step in parameters.buildSteps }}:
      - ${{ each pair in step }}:
          ${{ if ne(pair.value, 'CmdLine@2') }}:
            ${{ pair.key }}: ${{ pair.value }}       
          ${{ if eq(pair.value, 'CmdLine@2') }}: 
            # Step is rejected by raising a YAML syntax error: Unexpected value 'CmdLine@2'
            '${{ pair.value }}': error         

    - script: echo This happens after code
      displayName: 'Base: Signing'

```

Create a file named `azure-pipelines.yml`, and reference the `parameters.yml` file:

```
## File: azure-pipelines.yml
trigger:
- main

extends:
  template: parameters.yml
  parameters:
    buildSteps:  
      - bash: echo Test #Passes
        displayName: succeed
      - bash: echo "Test"
        displayName: succeed
      # Step is rejected by raising a YAML syntax error: Unexpected value 'CmdLine@2'
      - task: CmdLine@2
        inputs:
          script: echo "Script Test"
      # Step is rejected by raising a YAML syntax error: Unexpected value 'CmdLine@2'
      - script: echo "Script Test"

```

Here you can see that the pipeline is extended from the template `parameters.yml`. The parameter `buildSteps` is passed to the template. The template checks if the value of the parameter `buildSteps` is a `stepList` type. If it is, the pipeline continues. If it isn't, the pipeline fails.

Try to run the pipeline. You should see the following error:

You can increase security by adding a [required template approval](/en-us/azure/devops/pipelines/security/templates) when extending from a template.

### Challenge yourself

Create a pipeline using parameters from a YAML template file that deploys a web app to different regions based on a user's choice of environment.

For more information about parameters and templates, see:

* [Securing Azure Pipelines.](/en-us/azure/devops/pipelines/security/overview/)
* [Runtime parameters.](/en-us/azure/devops/pipelines/process/runtime-parameters/)
* [Template types \& usage.](/en-us/azure/devops/pipelines/process/templates)

---

## Limit queue time variables

In this unit, learn how to limit variables set at queue time for Azure Pipelines.

### Why limit queue time variables?

In some scenarios, you may want to allow certain variables to be changed when you run a YAML pipeline. For example, you may have a variable that controls the target environment, such as dev, test, or prod. By allowing this variable to be set at queue time, you can reuse the same pipeline definition for different deployments without modifying the YAML file.

However, allowing variables to be set at queue time can also introduce some risks. For example, someone could change a variable value to access a sensitive resource, bypass a security check, or alter the behavior of the pipeline in an unexpected way. To prevent these risks, you should limit the variables that can be set at queue time to only those that are necessary and safe.

### Limit queue time variables

The setting is designed to work at the organization and project levels.

In Azure DevOps, you have a setting to limit variables that can be set at queue time. With this setting enabled, only those variables that are explicitly marked as "Settable at queue time" can be set. In other words, you can set any variables at queue time unless this setting is enabled.

* **Organization**: When the setting is on, it enforces that, for all pipelines in all projects in the organization, only those variables that are explicitly marked as "Settable at queue time" can be set. When the setting is off, each project can choose to restrict variables set at queue time. The setting is a toggle under Organization Settings \> Pipelines \> Settings. Only Project Collection Administrators can enable or disable it.
* **Project**: When the setting is on, it enforces that, for all pipelines in the project, only those variables that are explicitly marked as "Settable at queue time" can be set. If the setting is on at the organization level, it is on for all projects and can't be turned off. The setting is a toggle under Project Settings \> Pipelines \> Settings. Only Project Administrators can enable or disable it.

### Challenge yourself

Now that you have learned how to limit queue time variables, try to apply this concept to your own YAML pipeline.

* With the "Limit variables that can be set at queue time" enabled try to create a new variable at queue time.
* With the "Limit variables that can be set at queue time" disabled try to create a new variable at queue time.

For more information about queue time variables, see:

* [Define variables.](/en-us/azure/devops/pipelines/process/variables)
* [How to securely use variables and parameters in your pipeline](/en-us/azure/devops/pipelines/security/inputs)

---

## Validate mandatory variables

In YAML pipelines, variables store and retrieve values during pipeline runs. Ensuring all the required variables are present and set correctly is essential to ensure pipeline security.

In this unit, learn how to validate mandatory variables in Azure DevOps YAML pipelines.

### Define and validate mandatory variables

One way to validate mandatory variables is by using the assert expression function in YAML to validate required variables. The assert function allows us to check if a condition is true or false and return an error message if the condition is false. We can use the assert function to validate that the mandatory variables are present and set correctly.

Here's an example of how to validate a mandatory variable named 'myVariable':

```

variables:
- name: myVariable
  value: ''

steps:
- script: echo 'Validate required variable!'
  condition: eq(variables['myVariable'], 'myRequiredValue')

```

The variable 'myVariable' is set to an empty string in this example. The condition expression checks if the variable is equal to 'myRequiredValue'. The script task won't be executed if the variable isn't set to this value.

**output:**
Evaluating: `eq(variables['myVariable'], 'myRequiredValue')`
Expanded: `eq('', 'myRequiredValue')`
Result: False

You can also configure your pipeline to fail if the variable isn't set correctly (false).

### Challenge yourself

Create a YAML pipeline that validates the presence and correctness of the mandatory variables 'myVariable1' and 'myVariable2'. If either variable is missing or not set correctly, the pipeline should fail. Use the assert function to validate the variables.

For more information about expressions, see [Expressions.](/en-us/azure/devops/pipelines/security/overview/)

---

## Lab \- Configure pipelines to securely use variables and parameters

In this lab, learn how to configure pipelines to securely use variables and parameters.

Note

To complete this lab, you will need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). You will also need to [validate your lab environment](https://aka.ms/mslearn-implement-security-through-pipeline-validate-lab-environment) to complete this lab.

Launch the exercise and follow the instructions.

Tip

To continue your learning journey, open the exercise in a new browser tab or window while staying on this page. To do this, right\-click the **Launch Exercise** button and select **Open link in new tab** or **Open link in new window**.

---

## Summary

In this module, you learned the fundamental concepts of variables and parameters, identified and restricted insecure use of variables and parameters, and moved parameters into a YAML file that protects their kind. You also explored limiting variables that can be set at queue time and validated that mandatory variables are present and set correctly.

You learned how to:

* Ensure that parameters and variables retain their type.
* Identify and restrict insecure use of parameters and variables.
* Move parameters into a YAML file that protects their type.
* Limit variables that can be set at queue time.
* Validate that mandatory variables are present and set correctly in Azure DevOps.

### Learn more

* [Security through templates.](/en-us/azure/devops/pipelines/security/templates)
* [Template types \& usage.](/en-us/azure/devops/pipelines/process/templates/)
* [Securing Azure Pipelines.](/en-us/azure/devops/pipelines/security/overview/)
* [Set secret variables.](/en-us/azure/devops/pipelines/process/set-secret-variables)
* [How to securely use variables and parameters in your pipeline.](/en-us/azure/devops/pipelines/security/inputs/)
* [Plan how to secure your YAML pipelines.](/en-us/azure/devops/pipelines/security/approach/)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-pipelines-securely-use-variables-parameters/_

## Fuentes
- [Configure pipelines to securely use variables and parameters](https://learn.microsoft.com/en-us/training/modules/configure-pipelines-securely-use-variables-parameters/?WT.mc_id=api_CatalogApi)
