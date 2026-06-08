# Implement Azure Container Apps

> Curso: Implement containerized solutions (wwl-az-204-implement-iaas-solutions) · Seccion: Implement containerized solutions
> Duracion estimada: 45 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Container Apps is a serverless container service that supports microservice applications and robust autoscaling capabilities without the overhead of managing complex infrastructure.

After completing this module, you'll be able to:

* Describe the features benefits of Azure Container Apps

* Deploy container app in Azure by using the Azure CLI
* Utilize Azure Container Apps built\-in authentication and authorization
* Create revisions and implement app secrets

---

## Explore Azure Container Apps

Azure Container Apps enables you to run microservices and containerized applications on a serverless platform that runs on top of Azure Kubernetes Service. Common uses of Azure Container Apps include:

* Deploying API endpoints
* Hosting background processing applications
* Handling event\-driven processing
* Running microservices

Applications built on Azure Container Apps can dynamically scale based on: HTTP traffic, event\-driven processing, CPU or memory load, and any [KEDA\-supported scaler](https://keda.sh/docs/scalers/).

With Azure Container Apps, you can:

* Run multiple container revisions and manage the container app's application lifecycle.
* Autoscale your apps based on any KEDA\-supported scale trigger. Most applications can scale to zero. (Applications that scale on CPU or memory load can't scale to zero.)
* Enable HTTPS ingress without having to manage other Azure infrastructure.
* Split traffic across multiple versions of an application for Blue/Green deployments and A/B testing scenarios.
* Use internal ingress and service discovery for secure internal\-only endpoints with built\-in DNS\-based service discovery.
* Build microservices with [Dapr](https://docs.dapr.io/concepts/overview/) and access its rich set of APIs.
* Run containers from any registry, public or private, including Docker Hub and Azure Container Registry (ACR).
* Use the Azure CLI extension, Azure portal, or ARM templates to manage your applications.
* Provide an existing virtual network when creating an environment for your container apps.
* Securely manage secrets directly in your application.
* Monitor logs using Azure Log Analytics.

### Azure Container Apps environments

Individual container apps are deployed to a single Container Apps environment, which acts as a secure boundary around groups of container apps. Container Apps in the same environment are deployed in the same virtual network and write logs to the same Log Analytics workspace. You might provide an existing virtual network when you create an environment.

Reasons to deploy container apps to the same environment include situations when you need to:

* Manage related services
* Deploy different applications to the same virtual network
* Instrument [Dapr](https://docs.dapr.io/concepts/overview/) applications that communicate via the Dapr service invocation API
* Have applications to share the same Dapr configuration
* Have applications share the same log analytics workspace

Reasons to deploy container apps to different environments include situations when you want to ensure:

* Two applications never share the same compute resources
* Two Dapr applications can't communicate via the Dapr service invocation API

### Microservices with Azure Container Apps

Microservice architectures allow you to independently develop, upgrade, version, and scale core areas of functionality in an overall system. Azure Container Apps provides the foundation for deploying microservices featuring:

* Independent scaling, versioning, and upgrades
* Service discovery
* Native [Dapr](https://docs.dapr.io/concepts/overview/) integration

### Dapr integration

When you implement a system composed of microservices, function calls are spread across the network. To support the distributed nature of microservices, you need to account for failures, retries, and timeouts. While Container Apps features the building blocks for running microservices, use of Dapr provides an even richer microservices programming model. Dapr includes features like observability, pub/sub, and service\-to\-service invocation with mutual TLS, retries, and more.

---

## Exercise \- Deploy a container to Azure Container Apps with the Azure CLI

In this exercise, you deploy a containerized application to Azure Container Apps using the Azure CLI. You learn how to create a container app environment, deploy your container, and verify that your application is running in Azure.

Tasks performed in this exercise:

* Create resources in Azure
* Create an Azure Container Apps environment
* Deploy a container app to the environment

This exercise takes approximately **15** minutes to complete.

### Before you start

To complete the exercise, you need:

* An Azure subscription. If you don't already have one, you can [sign up for one](https://azure.microsoft.com/).

### Get started

Select the **Launch Exercise** button to open the exercise instructions in a new browser window. When you're finished with the exercise, return here to:

* Complete the module
* Earn a badge for completing this module

---

## Explore containers in Azure Container Apps

Azure Container Apps manages the details of Kubernetes and container orchestration for you. Containers in Azure Container Apps can use any runtime, programming language, or development stack of your choice.

Azure Container Apps supports any Linux\-based x86\-64 (`linux/amd64`) container image. There's no required base container image, and if a container crashes it automatically restarts.

### Configuration

The following code is an example of the `containers` array in the `properties.template` section of a container app resource template. The excerpt shows some of the available configuration options when setting up a container when using Azure Resource Manager (ARM) templates. Changes to the template ARM configuration section trigger a new container app revision.

```
"containers": [
  {
       "name": "main",
       "image": "[parameters('container_image')]",
    "env": [
      {
        "name": "HTTP_PORT",
        "value": "80"
      },
      {
        "name": "SECRET_VAL",
        "secretRef": "mysecret"
      }
    ],
    "resources": {
      "cpu": 0.5,
      "memory": "1Gi"
    },
    "volumeMounts": [
      {
        "mountPath": "/myfiles",
        "volumeName": "azure-files-volume"
      }
    ]
    "probes":[
        {
            "type":"liveness",
            "httpGet":{
            "path":"/health",
            "port":8080,
            "httpHeaders":[
                {
                    "name":"Custom-Header",
                    "value":"liveness probe"
                }]
            },
            "initialDelaySeconds":7,
            "periodSeconds":3
// file is truncated for brevity

```

### Multiple containers

You can define multiple containers in a single container app to implement the [sidecar pattern](/en-us/azure/architecture/patterns/sidecar). The containers in a container app share hard disk and network resources and experience the same application lifecycle.

Examples of sidecar containers include:

* An agent that reads logs from the primary app container on a shared volume and forwards them to a logging service.
* A background process that refreshes a cache used by the primary app container in a shared volume.

Note

Running multiple containers in a single container app is an advanced use case. In most situations where you want to run multiple containers, such as when implementing a microservice architecture, deploy each service as a separate container app.

To run multiple containers in a container app, add more than one container in the containers array of the container app template.

### Container registries

You can deploy images hosted on private registries by providing credentials in the Container Apps configuration.

To use a container registry, you define the required fields in registries array in the properties.configuration section of the container app resource template. The passwordSecretRef field identifies the name of the secret in the secrets array name where you defined the password.

```
{
  ...
  "registries": [{
    "server": "docker.io",
    "username": "my-registry-user-name",
    "passwordSecretRef": "my-password-secret-name"
  }]
}

```

With the registry information added, the saved credentials can be used to pull a container image from the private registry when your app is deployed.

### Limitations

Azure Container Apps has the following limitations:

* **Privileged containers**: Azure Container Apps can't run privileged containers. If your program attempts to run a process that requires root access, the application inside the container experiences a runtime error.
* **Operating system**: Linux\-based (`linux/amd64`) container images are required.

---

## Implement authentication and authorization in Azure Container Apps

Azure Container Apps provides built\-in authentication and authorization features to secure your external ingress\-enabled container app with minimal or no code. The built\-in authentication feature for Container Apps can save you time and effort by providing out\-of\-the\-box authentication with federated identity providers, allowing you to focus on the rest of your application.

* Azure Container Apps provides access to various built\-in authentication providers.
* The built\-in auth features don’t require any particular language, SDK, security expertise, or even any code that you have to write.

This feature should only be used with HTTPS. Ensure `allowInsecure` is disabled on your container app's ingress configuration. You can configure your container app for authentication with or without restricting access to your site content and APIs.

* To restrict app access only to authenticated users, set its *Restrict access* setting to **Require authentication**.
* To authenticate but not restrict access, set its *Restrict access* setting to **Allow unauthenticated** access.

### Identity providers

Container Apps uses federated identity, in which a third\-party identity provider manages the user identities and authentication flow for you. The following identity providers are available by default:

| Provider | Sign\-in endpoint | How\-To guidance |
| --- | --- | --- |
| Microsoft Identity Platform | `/.auth/login/aad` | [Microsoft Identity Platform](/en-us/azure/container-apps/authentication-azure-active-directory) |
| Facebook | `/.auth/login/facebook` | [Facebook](/en-us/azure/container-apps/authentication-facebook) |
| GitHub | `/.auth/login/github` | [GitHub](/en-us/azure/container-apps/authentication-github) |
| Google | `/.auth/login/google` | [Google](/en-us/azure/container-apps/authentication-google) |
| X | `/.auth/login/twitter` | [X](/en-us/azure/container-apps/authentication-twitter) |
| Any OpenID Connect provider | `/.auth/login/<providerName>` | [OpenID Connect](/en-us/azure/container-apps/authentication-openid) |

When you use one of these providers, the sign\-in endpoint is available for user authentication and authentication token validation from the provider. You can provide your users with any number of these provider options.

### Feature architecture

The authentication and authorization middleware component is a feature of the platform that runs as a sidecar container on each replica in your application. When enabled, every incoming HTTP request passes through the security layer before being handled by your application.

The platform middleware handles several things for your app:

* Authenticates users and clients with the specified identity providers
* Manages the authenticated session
* Injects identity information into HTTP request headers

The authentication and authorization module runs in a separate container, isolated from your application code. As the security container doesn't run in\-process, no direct integration with specific language frameworks is possible. However, relevant information your app needs is provided in request headers.

### Authentication flow

The authentication flow is the same for all providers, but differs depending on whether you want to sign in with the provider's SDK:

* **Without provider SDK** (server\-directed flow or server flow): The application delegates federated sign\-in to Container Apps. Delegation is typically the case with browser apps, which presents the provider's sign\-in page to the user.
* **With provider SDK** (client\-directed flow or client flow): The application signs users in to the provider manually and then submits the authentication token to Container Apps for validation. This approach is typical for browser\-less apps that don't present the provider's sign\-in page to the user. An example is a native mobile app that signs users in using the provider's SDK.

---

## Manage revisions and secrets in Azure Container Apps

Azure Container Apps implements container app versioning by creating revisions. A revision is an immutable snapshot of a container app version. You can use revisions to release a new version of your app, or quickly revert to an earlier version of your app. New revisions are created when you update your application with [revision\-scope changes](/en-us/azure/container-apps/revisions#revision-scope-changes). You can also update your container app based on a specific revision.

You can control which revisions are active, and the external traffic that is routed to each active revision. Revision names are used to identify a revision, and in the revision's URL. You can customize the revision name by setting the revision suffix.

By default, Container Apps creates a unique revision name with a suffix consisting of a semi\-random string of alphanumeric characters. For example, for a container app named *album\-api*, setting the revision suffix name to *1st\-revision* would create a revision with the name *album\-api\-\-1st\-revision*. You can set the revision suffix in the ARM template, through the Azure CLI `az containerapp create` and `az containerapp update` commands, or when creating a revision via the Azure portal.

#### Updating your container app

With the `az containerapp update` command you can modify environment variables, compute resources, scale parameters, and deploy a different image. If your container app update includes [revision\-scope changes](/en-us/azure/container-apps/revisions#revision-scope-changes), a new revision is generated.

```
az containerapp update \
  --name <APPLICATION_NAME> \
  --resource-group <RESOURCE_GROUP_NAME> \
  --image <IMAGE_NAME>

```

You can list all revisions associated with your container app with the `az containerapp revision list` command.

```
az containerapp revision list \
  --name <APPLICATION_NAME> \
  --resource-group <RESOURCE_GROUP_NAME> \
  -o table

```

For more information about Container Apps commands, visit the [`az containerapp`](/en-us/cli/azure/containerapp) reference.

### Manage secrets in Azure Container Apps

Azure Container Apps allows your application to securely store sensitive configuration values. Once secrets are defined at the application level, secured values are available to container apps. Specifically, you can reference secured values inside scale rules.

* Secrets are scoped to an application, outside of any specific revision of an application.
* Adding, removing, or changing secrets doesn't generate new revisions.
* Each application revision can reference one or more secrets.
* Multiple revisions can reference the same secrets.

An updated or deleted secret doesn't automatically affect existing revisions in your app. When a secret is updated or deleted, you can respond to changes in one of two ways:

1. Deploy a new revision.
2. Restart an existing revision.

Before you delete a secret, deploy a new revision that no longer references the old secret. Then deactivate all revisions that reference the secret.

Note

Container Apps supports native Azure Key Vault integration. Enable managed identity in the container app, grant the identity the **Key Vault Secrets User** role, and define secrets as Key Vault references using the secret's URI. Container Apps automatically retrieves and refreshes the secret value.

#### Defining secrets

When you create a container app, secrets are defined using the `--secrets` parameter.

* The parameter accepts a space\-delimited set of name/value pairs.
* Each pair is delimited by an equals sign (`=`).

In the following example, a connection string to a queue storage account is declared in the `--secrets` parameter. The value for queue\-connection\-string comes from an environment variable named `$CONNECTION_STRING`.

```
az containerapp create \
  --resource-group "my-resource-group" \
  --name queuereader \
  --environment "my-environment-name" \
  --image demos/queuereader:v1 \
  --secrets "queue-connection-string=$CONNECTION_STRING"

```

After declaring secrets at the application level, you can reference them in environment variables when you create a new revision in your container app. When an environment variable references a secret, its value is populated with the value defined in the secret. To reference a secret in an environment variable in the Azure CLI, set its value to `secretref:`, followed by the name of the secret.

The following example shows an application that declares a connection string at the application level. This connection is referenced in a container environment variable.

```
az containerapp create \
  --resource-group "my-resource-group" \
  --name myQueueApp \
  --environment "my-environment-name" \
  --image demos/myQueueApp:v1 \
  --secrets "queue-connection-string=$CONNECTIONSTRING" \
  --env-vars "QueueName=myqueue" "ConnectionString=secretref:queue-connection-string"

```

---

## Explore Dapr integration with Azure Container Apps

The Distributed Application Runtime (Dapr) is a set of incrementally adoptable features that simplify the authoring of distributed, microservice\-based applications. Dapr provides capabilities for enabling application intercommunication through messaging via pub/sub or reliable and secure service\-to\-service calls.

Dapr is an open source, [Cloud Native Computing Foundation (CNCF)](https://www.cncf.io/projects/dapr/) project. The CNCF is part of the Linux Foundation and provides support, oversight, and direction for fast\-growing, cloud native projects. As an alternative to deploying and managing the Dapr OSS project yourself, the Container Apps platform:

* Provides a managed and supported Dapr integration
* Handles Dapr version upgrades seamlessly
* Exposes a simplified Dapr interaction model to increase developer productivity

### Dapr APIs

| Dapr API | Description |
| --- | --- |
| [Service\-to\-service invocation](https://docs.dapr.io/developing-applications/building-blocks/service-invocation/service-invocation-overview/) | Discover services and perform reliable, direct service\-to\-service calls with automatic mTLS authentication and encryption. |
| [State management](https://docs.dapr.io/developing-applications/building-blocks/state-management/state-management-overview/) | Provides state management capabilities for transactions and CRUD operations. |
| [Pub/sub](https://docs.dapr.io/developing-applications/building-blocks/pubsub/pubsub-overview) | Allows publisher and subscriber container apps to intercommunicate via an intermediary message broker. |
| [Bindings](https://docs.dapr.io/developing-applications/building-blocks/bindings/bindings-overview/) | Trigger your applications based on events |
| [Actors](https://docs.dapr.io/developing-applications/building-blocks/actors/actors-overview/) | Dapr actors are message\-driven, single\-threaded, units of work designed to quickly scale. For example, in burst\-heavy workload situations. |
| [Observability](/en-us/azure/container-apps/observability) | Send tracing information to an Application Insights backend. |
| [Secrets](https://docs.dapr.io/developing-applications/building-blocks/secrets/secrets-overview/) | Access secrets from your application code or reference secure values in your Dapr components. |
| [Configuration](https://docs.dapr.io/developing-applications/building-blocks/configuration/) | Retrieve and subscribe to application configuration items for supported configuration stores. |

Note

The table covers stable Dapr APIs. To learn more about using alpha APIs and features, [visit limitations](/en-us/azure/container-apps/dapr-overview?tabs=bicep1%2Cyaml#unsupported-dapr-capabilities).

### Dapr core concepts

The following example based on the Pub/sub API is used to illustrate core concepts related to Dapr in Azure Container Apps.

| Label | Dapr settings | Description |
| --- | --- | --- |
| 1 | Container Apps with Dapr enabled | Dapr is enabled at the container app level by configuring a set of Dapr arguments. These values apply to all revisions of a given container app when running in multiple revisions mode. |
| 2 | Dapr | The fully managed Dapr APIs are exposed to each container app through a Dapr sidecar. The Dapr APIs can be invoked from your container app via HTTP or gRPC. The Dapr sidecar runs on HTTP port 3500 and gRPC port 50001\. |
| 3 | Dapr component configuration | Dapr uses a modular design where functionality is delivered as a component. Dapr components can be shared across multiple container apps. The Dapr app identifiers provided in the scopes array dictate which dapr\-enabled container apps load a given component at runtime. |

### Dapr enablement

You can configure Dapr using various [arguments and annotations](https://docs.dapr.io/reference/arguments-annotations-overview/) based on the runtime context. Azure Container Apps provides three channels through which you can configure Dapr:

* Container Apps CLI
* Infrastructure as Code (IaC) templates, as in Bicep or Azure Resource Manager (ARM) templates
* The Azure portal

### Dapr components and scopes

Dapr uses a modular design where functionality is delivered as a component. The use of Dapr components is optional and dictated exclusively by the needs of your application.

Dapr components in container apps are environment\-level resources that:

* Can provide a pluggable abstraction model for connecting to supporting external services.
* Can be shared across container apps or scoped to specific container apps.
* Can use Dapr secrets to securely retrieve configuration metadata.

By default, all Dapr\-enabled container apps within the same environment load the full set of deployed components. To ensure components are loaded at runtime by only the appropriate container apps, application scopes should be used.

---

## Summary

In this module, you learned how to:

* Describe the features benefits of Azure Container Apps
* Deploy container app in Azure by using the Azure CLI
* Utilize Azure Container Apps built\-in authentication and authorization
* Create revisions and implement app secrets

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/implement-azure-container-apps/_

## Fuentes
- [Implement Azure Container Apps](https://learn.microsoft.com/en-us/training/modules/implement-azure-container-apps/?WT.mc_id=api_CatalogApi)
