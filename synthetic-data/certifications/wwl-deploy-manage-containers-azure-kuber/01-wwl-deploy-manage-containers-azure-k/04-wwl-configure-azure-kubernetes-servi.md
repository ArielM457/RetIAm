# Configure an Azure Kubernetes Service cluster

> Curso: Deploy containers by using Azure Kubernetes Service (AKS) (wwl-deploy-manage-containers-azure-kubernetes-serv) · Seccion: Deploy containers by using Azure Kubernetes Service (AKS)
> Duracion estimada: 41 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Policy is an add\-on that enables centralized, consistent enforcement of policies and safeguards on Kubernetes clusters at scale.

### Scenario

Imagine you have a large Kubernetes cluster with hundreds or thousands of pods and deployments. You need to ensure that all resources are compliant with your organization's policies and regulations. Azure Policy makes it possible to manage and report on the compliance state of your Azure Kubernetes Service clusters from one place. For example, you can use Azure Policy to enforce policies such as disallowing root privileges or requiring specific labels on pods. Azure Policy ensures that your cluster is secure and compliant with your organization's standards. With Azure Policy, you can also create custom policies that meet your specific needs. For instance, you can create a policy that requires all pods to use a specific container image or that limits the number of replicas for a deployment. By using Azure Policy, you can ensure that your Kubernetes cluster is secure, compliant, and consistent across your organization.

### Learning objectives

After completing this module, you'll be able to:

* Enable and configure Azure Policy for Azure Kubernetes Service.
* Assign policy definitions to an Azure Kubernetes Service cluster.
* Use namespaces to logically isolate workloads and resources.
* Enable host\-based encryption for Azure Kubernetes Service agent nodes.

### Goals

The goal of this module is to teach you how to use Azure Policy to enforce policies and safeguards on your Kubernetes clusters at scale. Azure Policy Ensures that your cluster is secure, compliant, and consistent across your organization.

---

## Understand Azure Policy for Kubernetes clusters

Azure Policy extends Gatekeeper v3, an *admission controller webhook* for Open Policy Agent (OPA), to apply at\-scale enforcements and safeguards on your clusters in a centralized, consistent manner. Azure Policy makes it possible to manage and report on the compliance state of your Kubernetes clusters from one place. The add\-on enacts the following functions:

* Checks with Azure Policy service for policy assignments to the cluster.
* Deploys policy definitions into the cluster as [constraint template](https://open-policy-agent.github.io/gatekeeper/website/docs/howto/#constraint-templates) and [constraint](https://open-policy-agent.github.io/gatekeeper/website/docs/howto/#constraints) custom resources.
* Reports auditing and compliance details back to Azure Policy service.

### Overview

To enable and use Azure Policy with your Kubernetes cluster, take the following actions:

1. Configure your Kubernetes cluster and install the Azure Kubernetes Service add\-on.
2. Understand the Azure Policy language for Azure Kubernetes Service Kubernetes.
3. Assign a definition to your Azure Kubernetes Service cluster.
4. Wait for validation.

### Recommendations

The following are general recommendations for using the Azure Policy Add\-on:

* The Azure Policy Add\-on requires three Gatekeeper components to run: One audit pod and two webhook pod replicas. These components consume more resources as the count of Kubernetes resources and policy assignments increases in the cluster, which requires audit and enforcement operations.

	+ For fewer than 500 pods in a single cluster with a max of 20 constraints: two vCPUs and 350\-MB memory per component.
	+ For more than 500 pods in a single cluster with a max of 40 constraints: three vCPUs and 600\-MB memory per component.

The following recommendation applies only to AKS and the Azure Policy Add\-on:

* Use system node pool with CriticalAddonsOnly taint to schedule Gatekeeper pods.
* Secure outbound traffic from your AKS clusters.
* If the cluster has aad\-pod\-identity enabled, Node Managed Identity (NMI) pods modify the nodes' iptables to intercept calls to the Azure Instance Metadata endpoint.

---

## Try\-This exercise \- Enable Azure Policy add on for Azure Kubernetes Service

Use this Try\-This exercise to gain some hands\-on experience with Azure Kubernetes Service.

This exercise you enable Azure Policy add on for an Azure Kubernetes Service cluster and verify the assignment is being enforced.

Note

To complete this exercise you'll need an [Azure Subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

1. Sign in to the [Azure portal](https://portal.azure.com/).
2. Select the Kubernetes cluster.
3. Select **Policies**, and select **Enable add\-on**. 

Note

The configuration of Azure Policy takes a few minutes.
4. The status for enabling Azure policy add\-on for the cluster appears as enabled.
5. On the Azure portal menu, search for **Subscriptions**. Select your Azure subscription.
6. Select Resource providers, and search for **Microsoft.PolicyInsights**.

Verify that the **Microsoft.PolicyInsights** Resource provider is registered.

---

## Try\-This exercise \- Assign a policy definition to an Azure Kubernetes cluster

Use this Try\-This exercise to gain some hands\-on experience with Azure Kubernetes Service.

To assign a policy definition to your Kubernetes cluster, you must be assigned the appropriate Azure role\-based access control (Azure RBAC) policy assignment operations. The Azure built\-in roles **Resource Policy Contributor** and **Owner** have these operations.

Find the built\-in policy definitions for managing your cluster using the Azure portal with the following steps. If using a custom policy definition, search for it by name or the category that you created it with.

Note

To complete this exercise you'll need an [Azure Subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

1. Select in the left pane and then search for and select **Policy**.
2. In the left pane of the Azure Policy page, select **Definitions**.
3. From the Category dropdown list box, use **Select all** to clear the filter and then select **Kubernetes**.
4. Select the policy definition, then select the **Assign** button.
5. Set the **Scope** to the management group, subscription, or resource group of the Kubernetes cluster where the policy assignment applies.

Note

The **Scope** must include the cluster resource when assigning the Azure Policy for Kubernetes definition.
6. Give the policy assignment a **Name** and **Description** that you can use to identify it easily.
7. Set the Policy enforcement to one of the values.

	* **Enabled** \- Enforce the policy on the cluster. Kubernetes admission requests with violations are denied.
	* **Disabled** \- Don't enforce the policy on the cluster. Kubernetes admission requests with violations aren't denied. Compliance assessment results are still available. The *Disabled* option is helpful for testing the policy definition as admission requests with violations aren't denied.
8. Select **Next**.
9. Set **parameter values**
10. Select **Review \+ create**, and select **Create**.
11. Select **Overview** in the left pane and then search for and select **Policy**.
12. Under **Name**, view the compliance for the Policy definition.

---

## Host\-based encryption on Azure Kubernetes Service

With host\-based encryption, the data stored on the VM host of your AKS agent nodes' VMs is encrypted at rest and flows encrypted to the Storage service. The temp disks are encrypted at rest with platform\-managed keys. The cache of OS and data disks is encrypted at rest with either platform\-managed keys or customer\-managed keys depending on the encryption type set on those disks.

By default, when using AKS, OS and data disks use server\-side encryption with platform\-managed keys. The caches for these disks are encrypted at rest with platform\-managed keys. You can specify your own managed keys using *bring your own keys* (BYOK) with Azure disks in Azure Kubernetes Service. The caches for these disks are also encrypted using the key you specify.

Host\-based encryption is different than server\-side encryption (SSE), which is used by Azure Storage. Azure\-managed disks use Azure Storage to automatically encrypt data at rest when saving data. Host\-based encryption uses the host of the VM to handle encryption before the data flows through Azure Storage.

#### Limitations

* This feature can only be set at cluster or node pool creation time.
* This feature can only be enabled in Azure regions that support server\-side encryption of Azure managed disks and only with specific [supported VM sizes](/en-us/azure/virtual-machines/disk-encryption#supported-vm-sizes).
* This feature requires an AKS cluster and node pool based on Virtual Machine Scale Sets as *VM set type*.

A list of examples enabling host\-based encryption on new and existing clusters using Azure CLI commands.

#### Use host\-based encryption on new clusters.

* Create a new cluster and configure the cluster agent nodes to use host\-based encryption using `--enable-encryption-at-host` flag.

```
az aks create --name myAKSCluster --resource-group myResourceGroup -s Standard_DS2_v2 -l westus2 --enable-encryption-at-host

```

#### Use host\-based encryption on existing clusters.

* Enable host\-based encryption on an existing cluster by adding a new node pool using the `--enable-encryption-at-host` flag.

```
az aks nodepool add --name hostencrypt --cluster-name myAKSCluster --resource-group myResourceGroup -s Standard_DS2_v2 --enable-encryption-at-host

```

---

## Create a custom namespace for Azure Kubernetes clusters

Kubernetes resources, such as pods and deployments, are logically grouped into a namespace to divide an AKS cluster and create, view, or manage access to resources. For example, you can create namespaces to separate business groups. Users can only interact with resources within their assigned namespaces.

Namespaces are intended for environments with multiple users spanning multiple teams or organizations. Namespaces are suited medium, large, and enterprise organizations that have hundreds or thousands of users to manage.

Namespaces provide a scope for names. Names of resources should be unique within a namespace, but not across namespaces. Namespaces can't be nested inside one another and each Kubernetes resource can only be in one namespace.

When you create an AKS cluster, the following namespaces are available:  

| **Namespace** | **Description** |
| --- | --- |
| default | Where pods and deployments are created by default when none is provided. In smaller environments, you can deploy applications directly into the default namespace without creating more logical separations. When you interact with the Kubernetes API, such as with kubectl get pods, the default namespace is used when none is specified. |
| kube\-system | Where core resources exist, such as network features like DNS and proxy, or the Kubernetes dashboard. You typically don't deploy your own applications into this namespace. |
| kube\-public | Typically not used, but can be used for resources to be visible across the whole cluster, and viewed by any user. |

#### Logically isolated clusters using namespaces

With logical isolation, you can use a single AKS cluster for multiple workloads, teams, or environments. Kubernetes Namespaces form the logical isolation boundary for workloads and resources.

Logical separation of clusters usually provides a higher pod density than physically isolated clusters, with less excess compute capacity sitting idle in the cluster. When combined with the Kubernetes cluster autoscaler, you can scale the number of nodes up or down to meet demands. This best practice approach minimizes costs by running only the required number of nodes.

#### Create a custom namespace

1. Sign in to the Azure portal at [https://portal.azure.com](https://portal.azure.com/).
2. On the Azure portal menu or from the **Home** page, select the Azure Kubernetes cluster used in previous exercises.
3. Select **Namespaces**.
4. Select **Create**, and then select **Namespace**.
5. In **Create a namespace**, enter a name for the namespace, and select **Create**.
6. Select the new namespace.
7. To edit the namespace, select **YAML**.
8. Select **Review \+ save** to save YAML updates to the namespace.

---

## Module assessment

Choose the best response for each question.

### Check your knowledge

---

## Summary

In this module, you learned how to:

* Enable and configure Azure Policy for Azure Kubernetes Service.
* Assign policy definitions to an Azure Kubernetes Service cluster.
* Use namespaces to logically isolate workloads and resources.
* Enable host\-based encryption for Azure Kubernetes Service agent nodes.

### Learn more

* [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) \| [Azure free account FAQ](https://azure.microsoft.com/pricing/purchase-options/azure-account#FAQ?cid=msft_learn)
* [Free account for Students](https://azure.microsoft.com/free/students/?cid=msft_learn) \| [Azure for students FAQ](/en-us/azure/education-hub/azure-dev-tools-teaching/program-faq#azure-for-students/?azure-portal=true)
* [Create an Azure account](/en-us/learn/modules/create-an-azure-account/?azure-portal=true) module on Learn.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-azure-kubernetes-service-cluster/_

## Fuentes
- [Configure an Azure Kubernetes Service cluster](https://learn.microsoft.com/en-us/training/modules/configure-azure-kubernetes-service-cluster/?WT.mc_id=api_CatalogApi)
