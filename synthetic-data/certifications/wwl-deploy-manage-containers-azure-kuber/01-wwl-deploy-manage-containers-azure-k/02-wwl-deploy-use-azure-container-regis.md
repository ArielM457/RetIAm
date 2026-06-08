# Deploy and use Azure Container Registry

> Curso: Deploy containers by using Azure Kubernetes Service (AKS) (wwl-deploy-manage-containers-azure-kubernetes-serv) · Seccion: Deploy containers by using Azure Kubernetes Service (AKS)
> Duracion estimada: 39 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

This module covers the creation of an Azure Container Registry instance with the Azure portal.

### Scenario

In this scenario, you learn how to create a private registry service for building, storing, and managing container images and related artifacts. You use Docker commands to push a container image into the registry, and finally pull and run the image from your registry.

### Prerequisites

To complete the hands\-on steps, you need:

* An Azure subscription.
* Permissions to create the registry and assign Azure roles in the subscription. If you can't assign roles, ask an administrator to assign you the Container Registry Repository Writer role for push/pull and the Container Registry Repository Catalog Lister role for portal repository listing after the registry is created.
* Azure CLI installed on your local machine. You sign in during the exercise and use it to authenticate to the registry.
* Docker installed locally with the Docker daemon running so `az acr login` and the Docker commands can work with the registry.

### Learning objectives

After completing this module, you'll be able to:

* Describe Azure Container Registry as a private registry service for building, storing, and managing container images and related artifacts.
* Create an Azure container registry instance with the Azure portal.
* Sign in to the registry instance using the Azure CLI on your local machine.
* Push an image to the registry instance.
* Remove the registry\-tagged local image reference from your local Docker environment.
* View the image in your registry.
* Pull and run the container image from your container registry.

### Goals

The goal of this module is to teach you how to create and manage an Azure Container Registry instance, and to push, pull, and run container images from the registry.

---

## Try\-This exercise \- Create a container registry

Use this Try\-This exercise to gain some hands\-on experience with Azure Container Registry.

Azure Container Registry is a private registry service for building, storing, and managing container images and related artifacts. In this module, you create an Azure container registry instance with the Azure portal.

Note

To complete this procedure, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). The repository role assignment step also requires **Owner**, **Role Based Access Control Administrator**, or equivalent `Microsoft.Authorization/roleAssignments/write` permission. If you don't have that permission, ask an administrator to assign the needed Azure Container Registry repository roles.

1. Sign in to the [Azure portal](https://portal.azure.com/).
2. Select **Create a resource** \> **Infrastructure services** \> **Container Registry** \> **Create**.
3. In the **Basics** tab, select the **Subscription** where you want to create the container registry.
4. For **Resource group**, create a new resource group, such as `myResourceGroup`.
5. Enter a **Registry name**, such as `newregistryapl` if it's available. ACR registry names must be globally unique and 5\-50 lowercase alphanumeric characters. Don't use uppercase letters or dash characters (`-`). If the sample name is taken, append a short random lowercase alphanumeric suffix. The registry resource name is used as the base of the login server DNS name.
6. Select a **Location**, such as **West US 2**.
7. For **Pricing plan**, select **Standard**.
8. For **Domain name label scope**, select **Tenant Reuse**, or choose another option if your organization requires it.

Important

The domain name label scope is permanent after the registry is created and can't be changed later.

For every DNL\-enabled option except **Unsecure**, including **Tenant Reuse**, the registry login server includes a generated hash suffix, such as `newregistryapl-<hash>.azurecr.io`. The registry resource name remains `newregistryapl`.
9. For **Role assignment permissions mode**, select **RBAC Registry \+ ABAC Repository Permissions**.
10. Leave **Admin user** disabled (the default). This module uses Microsoft Entra/RBAC repository permissions instead of admin credentials. Accept default values for the remaining settings. Then select **Review \+ create**. After reviewing the settings, select **Create**.
11. When the **Deployment succeeded** message appears, select **Go to resource** to open the registry overview.
12. Make a note of the registry resource name and the exact value of the **Login server**. Use the registry resource name to sign in with the Azure CLI. Use the exact portal **Login server** value for Docker tag, push, and run commands in later steps.
13. Because you selected **RBAC Registry \+ ABAC Repository Permissions**, the learner identity needs data\-plane repository permissions for later Docker and portal repository steps. In the registry menu, select **Access control (IAM)** \> **Add** \> **Add role assignment**, then assign the learner identity these roles on the registry:

	* **Container Registry Repository Writer**
	* **Container Registry Repository Catalog Lister**Assigning roles requires **Owner**, **Role Based Access Control Administrator**, or equivalent `Microsoft.Authorization/roleAssignments/write` permission on the registry. If you don't have that permission, ask an administrator to complete this step.

**Container Registry Repository Writer** without ABAC conditions grants registry\-wide read/write/update repository access in this lab registry. **Container Registry Repository Catalog Lister** grants list access to all repositories and can't be ABAC\-scoped. If the registry isn't dedicated to this lab, scope **Container Registry Repository Writer** with ABAC conditions for only the `hello-world` repository, or ask an administrator to do so.

Azure role assignment changes can take up to 10 minutes to take effect. If a later `az acr login`, `docker push`, or portal repository listing returns `401` or `403`, wait a few minutes and retry. If needed, sign out and sign in again or refresh your tokens.

---

## Try\-This exercise \- Sign in to the container registry

Use this Try\-This exercise to gain some hands\-on experience with Azure Container Registry.

Before pushing and pulling container images, you must sign in to Azure and then sign in to the registry instance. [Sign in to the Azure CLI](/en-us/cli/azure/get-started-with-azure-cli) on your local machine by using `az login`, then run the [az acr login](/en-us/cli/azure/acr#az-acr-login) command. Specify only the registry resource name when signing in with the Azure CLI.

Note

Don't use the fully qualified login server name, such as `newregistryapl.azurecr.io` or `newregistryapl-<hash>.azurecr.io`, with `az acr login --name`. Use the registry resource name, such as `newregistryapl`.

Important

Use a local terminal for this module's standard Docker workflow. You need the Azure CLI, Docker CLI, and Docker daemon running locally. Azure Cloud Shell isn't suitable because it doesn't run the Docker daemon.
Although `az acr login --expose-token` is available for environments without a Docker daemon, such as Azure Cloud Shell or scripts, this module's standard Docker workflow still requires a local Docker CLI and daemon.

Note

To complete this procedure, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Sign in to the Azure CLI on your local machine by running the `az login` command.

```
az login

```

Follow the browser or device\-code sign\-in prompts. When sign\-in completes, the Azure CLI either presents an interactive subscription selector (default subscription marked with `*`) or prints a list of your subscriptions (default marked with `isDefault: true`), depending on your CLI version and configuration. Use `az account show` to confirm the active subscription.

If you have access to multiple Azure subscriptions, verify that the Azure CLI is using the subscription that contains your registry.

```
az account show --query "{Name:name, SubscriptionId:id}" --output table

```

To change the active subscription, run:

```
az account set --subscription "<subscription-id-or-name>"

```

After repository roles are assigned, Azure role assignment changes can take up to 10 minutes to take effect. If `az acr login` fails with a 401 or 403 error shortly after assignment, wait and retry. If needed, sign out and in again to refresh your Azure CLI credentials.

Sign in to the registry using the registry resource name.

```
az acr login --name <registry-name>

```

Example:

```
az acr login --name newregistryapl

```

The command returns `Login Succeeded` when it completes.

---

## Try\-This exercise \- Push an image to the registry

Use this Try\-This exercise to gain some hands\-on experience with Azure Container Registry.

For this exercise, Docker commands are used to push a container image into the registry, and finally pull and run the image from your registry.

Important

Run this Docker\-based workflow in a local terminal with the Azure CLI, Docker CLI, and Docker daemon running. Azure Cloud Shell isn't suitable because it doesn't run the Docker daemon.

You must also have Docker installed locally with the Docker daemon running. Docker provides packages that easily configure Docker on any [Mac](https://docs.docker.com/desktop/setup/install/mac-install/), [Windows](https://docs.docker.com/desktop/setup/install/windows-install/), or [Linux](https://docs.docker.com/engine/install) system.

Note

To complete this procedure, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

To push an image to an Azure Container registry, you must first have an image. If you don't yet have any local container images, run the following [docker pull](https://docs.docker.com/engine/reference/commandline/pull/) command to pull an existing public image.

Pull the `hello-world` image from Microsoft Container Registry.

```
docker pull mcr.microsoft.com/hello-world

```

The command downloads the `hello-world` image to your local Docker environment. If the image already exists locally, Docker reports that it's up to date.

Before you can push an image to your registry, tag it with the fully qualified **Login server** value shown for your registry in the Azure portal. Use the exact portal value for the Docker tag, push, and run commands. The default Tenant Reuse/DNL registry created in this module uses a login server in the `<registry-name>-<hash>.azurecr.io` format. A registry created with the Unsecure/non\-DNL option uses `<registry-name>.azurecr.io` instead.

Tag the image using the [docker tag](https://docs.docker.com/engine/reference/commandline/tag/) command. Replace `<login-server>` with the exact **Login server** value of your ACR instance.

```
docker tag mcr.microsoft.com/hello-world <login-server>/hello-world:v1

```

Default Tenant Reuse/DNL example format (substitute your actual **Login server** value from the portal):

```
docker tag mcr.microsoft.com/hello-world <registry-name>-<hash>.azurecr.io/hello-world:v1

```

Unsecure/non\-DNL only: if you intentionally used that option, the equivalent target uses `<registry-name>.azurecr.io/hello-world:v1`. Don't use this format for the default Tenant Reuse/DNL path.

```
docker tag mcr.microsoft.com/hello-world <registry-name>.azurecr.io/hello-world:v1

```

A successful `docker tag` command typically returns no output.

Before pushing, make sure your Azure Container Registry authentication is still valid. `az acr login` caches credentials for Docker, and the ACR token is valid for 3 hours. Rerun `az acr login --name <registry-name>` if the token expired, Docker authentication fails, or you're unsure you're authenticated. Use the registry resource name, not the login server.

After repository roles are assigned, Azure role assignment changes can take up to 10 minutes to take effect. If `az acr login` or `docker push` fails with a 401 or 403 error shortly after assignment, wait and retry. If needed, sign out and in again or rerun `az acr login` to refresh credentials.

```
az acr login --name <registry-name>

```

Use [docker push](https://docs.docker.com/engine/reference/commandline/push/) to push the image to the registry instance. Replace `<login-server>` with the exact **Login server** value of your registry instance. This example creates the **hello\-world** repository, containing the `hello-world:v1` image.

```
docker push <login-server>/hello-world:v1

```

Default Tenant Reuse/DNL example format (substitute your actual **Login server** value from the portal):

```
docker push <registry-name>-<hash>.azurecr.io/hello-world:v1

```

Unsecure/non\-DNL only: if you intentionally used that option, the equivalent target uses `<registry-name>.azurecr.io/hello-world:v1`. Don't use this format for the default Tenant Reuse/DNL path.

```
docker push <registry-name>.azurecr.io/hello-world:v1

```

The push output lists image layers and confirms that the `v1` tag was pushed to your registry.

After pushing the image to your container registry, remove the registry\-tagged local image reference from your local Docker environment. The [docker rmi](https://docs.docker.com/engine/reference/commandline/rmi/) command removes the `<login-server>/hello-world:v1` local image reference. It doesn't remove the image from the **hello\-world** repository in your Azure container registry, and the underlying local image might remain if another tag still points to it.

```
docker rmi <login-server>/hello-world:v1

```

---

## Try\-This exercise \- View container images

Use this Try\-This exercise to gain some hands\-on experience with Azure Container Registry.

To verify the push in the portal, navigate to your registry. In the registry menu, under **Services**, select **Repositories**, open the **hello\-world** repository, and verify that the `v1` tag appears under **Tags**.

Note

When the registry uses **RBAC Registry \+ ABAC Repository Permissions**, listing repositories in the portal requires the **Container Registry Repository Catalog Lister** role. Viewing tags or repository content requires **Container Registry Repository Reader** or **Container Registry Repository Writer**. This module assigned **Container Registry Repository Writer** earlier.

Note

After repository roles are assigned, Azure role assignment changes can take up to 10 minutes to take effect. If the portal repository list or tag view fails with a 401 or 403 error shortly after assignment, wait and refresh. If needed, sign out and in again to refresh your portal session.

Note

To complete this procedure, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

1. From **Container registries**, select the registry you created in the previous unit.
2. In the registry menu, under **Services**, select **Repositories**.
3. Select the **hello\-world** repository. Under **Tags**, verify that the `v1` tag is listed.
4. Optionally, verify the repository and tag from the Azure CLI. Use the registry resource name for `<registry-name>`, not the **Login server** value.

```
az acr repository list -n <registry-name> --output table

```

```
az acr repository show-tags -n <registry-name> --repository hello-world --output table

```

---

## Try\-This exercise \- Run an image from the registry

Use this Try\-This exercise to gain some hands\-on experience with Azure Container Registry.

Now you can pull and run the `hello-world:v1` container image from your container registry by using [docker run](https://docs.docker.com/engine/reference/commandline/run/):

Important

Run these Docker commands in a local terminal with the Azure CLI, Docker CLI, and Docker daemon running. Azure Cloud Shell isn't suitable because it doesn't run the Docker daemon.

The `az acr login` command caches credentials for Docker, and the ACR token is valid for 3 hours. Rerun `az acr login --name <registry-name>` if the token expired, Docker authentication fails, or you're unsure you're authenticated. Use the registry resource name, not the login server.

After repository roles are assigned, Azure role assignment changes can take up to 10 minutes to take effect. If `az acr login`, `docker run`, or `docker pull` fails with a 401 or 403 error shortly after assignment, wait and retry. If needed, sign out and in again or rerun `az acr login` to refresh credentials.

```
az acr login --name <registry-name>

```

Replace `<login-server>` with the exact **Login server** value shown for your registry in the Azure portal. The default Tenant Reuse/DNL registry created in this module uses `<registry-name>-<hash>.azurecr.io`. A registry created with the Unsecure/non\-DNL option uses `<registry-name>.azurecr.io` instead.

```
docker run --rm <login-server>/hello-world:v1

```

Default Tenant Reuse/DNL example format (substitute your actual **Login server** value from the portal):

```
docker run --rm <registry-name>-<hash>.azurecr.io/hello-world:v1

```

Unsecure/non\-DNL only: if you intentionally used that option, the equivalent target uses `<registry-name>.azurecr.io/hello-world:v1`. Don't use this format for the default Tenant Reuse/DNL path.

```
docker run --rm <registry-name>.azurecr.io/hello-world:v1

```

The `hello-world` image prints output and then exits. It doesn't start a long\-running service or expose a public endpoint.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/deploy-use-azure-container-registry/_

## Fuentes
- [Deploy and use Azure Container Registry](https://learn.microsoft.com/en-us/training/modules/deploy-use-azure-container-registry/?WT.mc_id=api_CatalogApi)
