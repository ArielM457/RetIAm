# Deploy applications to Azure Kubernetes Service

> Curso: Deploy containers by using Azure Kubernetes Service (AKS) (wwl-deploy-manage-containers-azure-kubernetes-serv) · Seccion: Deploy containers by using Azure Kubernetes Service (AKS)
> Duracion estimada: 58 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

In this module, you'll learn how to use Azure Policy to enforce organizational standards and assess compliance at scale for Azure Kubernetes Service (AKS) clusters. You explore the Azure Policy add\-on for AKS and learn how to assign a built\-in Azure Policy initiative to an AKS cluster.  

Azure Policy helps manage and report on the compliance state of your AKS environment. You also learn that Pod Security Admission can enforce namespace\-level security policies for individual AKS clusters without relying on Azure Policy. The module then introduces AKS storage options, including managed databases, Azure Disks, Azure Files, Azure NetApp Files, Azure Blob Storage, and Azure Container Storage, and shows how to configure persistent storage for pods by using StorageClasses and PersistentVolumeClaims. Finally, you learn why Kubernetes Deployments are preferred over individual pods for resilient workloads, and you create and update a Deployment in your AKS cluster.

### Learning objectives

After completing this module, you'll be able to:

* Provision an Azure Kubernetes Service cluster.
* Install the Azure Policy add\-on for Azure Kubernetes Service.
* Assign an Azure Policy initiative to an Azure Kubernetes Service cluster.
* Validate the effect of Azure Policy.
* Select storage options for AKS containerized workloads.
* Configure persistent storage for pods by using StorageClasses and PersistentVolumeClaims.
* Describe why Kubernetes Deployments are preferred over individual pods, and create and update a Deployment in AKS.

### Goals

By the end of this module, you provision an AKS cluster, install and use the Azure Policy add\-on for Azure Kubernetes Service, configure persistent storage for pods, and create and update a Kubernetes Deployment.

---

## Configure Azure Kubernetes pods using Azure Policy

You can apply and enforce security settings on pods hosted in Azure Kubernetes Service (AKS) clusters by using Azure Policy. Azure Policy helps enforce organizational standards and assess compliance at scale. After you install the Azure Policy add\-on for AKS, you can assign built\-in and custom policy definitions either individually or in groups referred to as policy initiatives.

#### Explore Azure Policy add\-on for AKS

[Azure Policy for Kubernetes](/en-us/azure/governance/policy/concepts/policy-for-kubernetes) extends Gatekeeper v3, an admission controller webhook for Open Policy Agent (OPA), to apply at\-scale enforcements and safeguards in a centralized, consistent manner. Current Azure Policy add\-on versions still use Gatekeeper v3\. On supported add\-on and Kubernetes versions, the add\-on can also generate Kubernetes\-native ValidatingAdmissionPolicy (VAP) resources for Common Expression Language (CEL)\-based policies. Azure Policy makes it possible to manage and report on the compliance state of your AKS environment.

Note

You can implement namespace\-level security policies for individual AKS clusters (without relying on Azure Policy) by using [Pod Security Admission](/en-us/azure/aks/use-psa). Pod Security Admission is enabled by default in AKS clusters running Kubernetes version 1\.23 or later, but AKS doesn't enforce baseline or restricted policies on namespaces automatically. To apply a profile, label the namespace (for example, `pod-security.kubernetes.io/enforce=restricted`). PSA replaces the Kubernetes PodSecurityPolicy feature, which was deprecated in Kubernetes 1\.21 and removed in Kubernetes 1\.25\. In enterprise scenarios, you should consider using Azure Policy\-based policies instead.

To implement Azure Policy for AKS, register the `Microsoft.PolicyInsights` resource provider in the subscription, verify that the cluster runs a supported AKS Kubernetes version, and then install the Azure Policy add\-on for AKS. The add\-on manages interaction between Azure Policy and Gatekeeper components, including the following tasks:

* Monitoring for Azure Policy assignments targeting the AKS cluster.
* Deploying policy definitions to the cluster as constraint templates and constraint custom resources, mutation template resources when applicable, and, on supported add\-on and Kubernetes versions, Kubernetes\-native ValidatingAdmissionPolicy resources for supported CEL policies.
* Reporting resulting auditing and compliance details back to Azure Policy.

To install the Azure Policy add\-on for AKS, you can use the Azure portal, Azure CLI, and Azure Resource Manager templates. Alternatively, you have the option of applying it by assigning the Azure Policy definition *Deploy Azure Policy Add\-on to Azure Kubernetes Service clusters* to target AKS clusters.

* The Azure Policy add\-on for Kubernetes can only be deployed to Linux node pools.
* Installations of Gatekeeper outside of the Azure Policy add\-on aren't supported. You need to uninstall any existing Gatekeeper components before enabling the Azure Policy add\-on.
* The Azure Policy add\-on Helm model and the add\-on for AKS Engine are deprecated; use the managed Azure Policy add\-on for AKS clusters.
* Some policy settings are operating system\-specific. For example, disallowing root privileges is applicable only to Linux pods.
* The add\-on automatically excludes the `kube-system` and `gatekeeper-system` namespaces from evaluation.

#### Review built\-in Azure Policy for AKS initiative and policy definitions targeting pod configurations

Commonly used [Azure Policy built\-in initiatives](/en-us/azure/governance/policy/samples/built-in-initiatives#kubernetes) for AKS targeting pod security include:

* Kubernetes cluster pod security baseline standards for Linux\-based workloads.
* Kubernetes cluster pod security restricted standards for Linux\-based workloads.

#### Assign a policy definition

Once you have identified or authored the policy definition or initiative you want to implement, you need to assign it to the target AKS cluster or clusters. Your account must have a sufficient level of Azure role\-based access control (RBAC) permissions. These permissions are part of the built\-in **Resource Policy Contributor** and **Owner** roles.

Note

It might take up to 20 minutes for initial assignments to sync to a target cluster. Subsequent checks for changes in policy assignments take place every 15 minutes. Azure Policy compliance reports include all violations within the last 45 minutes.

A deny policy applied to a cluster doesn't affect the operational status of any existing non\-compliant resources. Gatekeeper or generated ValidatingAdmissionPolicy resources block creation or admission of new or replacement non\-compliant resources, including replacement Pods created by controllers.

---

## Try\-This exercise \- Apply Azure Kubernetes Service pod settings using Azure Policy

In this exercise, you step through the process of applying pod security settings to an Azure Kubernetes Service (AKS) cluster by using Azure Policy. The exercise consists of the following tasks:

* Deploy an AKS cluster.
* Install the Azure Policy add\-on for AKS.
* Assign an Azure Policy initiative to an AKS cluster.
* Validate the effect of Azure Policy.

#### Deploy an AKS cluster

In this exercise, you deploy an AKS cluster. You use this cluster throughout all exercises in the module. While you can deploy a cluster using the Azure portal, you can use Azure CLI instead for simplicity.

Note

To complete this exercise, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). Your account must have permission to create AKS resources, register the **Microsoft.PolicyInsights** resource provider, enable AKS add\-ons, and assign Azure Policy. Assigning Azure Policy typically requires the Owner or Resource Policy Contributor role at the assignment scope.

1. From your computer, open a web browser window and navigate to the Azure portal at [https://portal.azure.com](https://portal.azure.com/).
2. In the Azure portal, select the **Azure Cloud Shell** icon.
3. If prompted to select either **Bash** or **PowerShell**, select **Bash**.
4. Ensure that **Bash** appears in the drop\-down menu in the upper\-left corner of the Cloud Shell pane.
5. To create a resource group to host the AKS cluster, in the Bash session in the Azure Cloud Shell, run the following commands. You can replace eastus with the name of another Azure region where you can create AKS clusters:

```
AKSRG='aks-01-RG'
LOCATION='eastus'
az group create --name $AKSRG --location $LOCATION

```
6. To create an AKS cluster, run the following commands:

```
AKSNAME='aks-01'
az aks create --resource-group $AKSRG --name $AKSNAME --node-count 1 --generate-ssh-keys

```

Note

The `--generate-ssh-keys` flag creates SSH key files in `~/.ssh` if they don't already exist. In Azure Cloud Shell, those files persist in your Cloud Shell home directory and are reused on subsequent runs.
7. Once the cluster provisioning completes, to connect to the AKS cluster, run the following command:

```
az aks get-credentials --resource-group $AKSRG --name $AKSNAME

```
8. To verify that the connection was successful, run the following command:

```
kubectl get nodes

```

The output of the command should include the listing of the AKS nodes.

#### Install the Azure Policy add\-on for AKS

In this task, you install the Azure Policy add\-on for AKS.

1. To install the Azure Policy add\-on, you need to ensure that the **Microsoft.PolicyInsights** resource provider is registered in your subscription. From the Bash session in the Azure Cloud Shell in the Azure portal, run the following commands to register the provider and verify its status:

```
az provider register --namespace Microsoft.PolicyInsights --wait
az provider show --namespace Microsoft.PolicyInsights --query "{Provider:namespace,State:registrationState}" --output table

```
2. Review the output and confirm that the provider status is **Registered**.
3. To install the add\-on, run the following commands:

```
AKSRG='aks-01-RG'
AKSNAME='aks-01'
az aks enable-addons --addons azure-policy --name $AKSNAME --resource-group $AKSRG

```

Note

You can also enable the Azure Policy add\-on during cluster deployment by adding `--enable-addons azure-policy` to the `az aks create` command.
4. To validate that the add\-on installation was successful and that the *azure\-policy* and *gatekeeper* pods are operational, run the following commands:

```
kubectl get pods --namespace kube-system
kubectl get pods --namespace gatekeeper-system

```

Note

The Azure Policy add\-on can take several minutes to roll out. If the `azure-policy` or Gatekeeper pods aren't yet `Running`, wait a moment and re\-run the previous `kubectl get pods` commands until both sets of pods report `Running` and `Ready`.
5. To verify that, at this point, no Azure Policy constraint templates are present on the target cluster, run the following command:

```
kubectl get constrainttemplates

```

The command should generate output `No resources found` only if no inherited or automatically applied Kubernetes policy assignments, such as assignments from Microsoft Defender for Cloud, already target the cluster.

#### Assign an Azure Policy initiative to an AKS cluster

In this task, you assign an Azure Policy initiative to an AKS cluster. You use one of the built\-in initiatives named *Kubernetes cluster pod security baseline standards for Linux\-based workloads*.

1. In the Azure portal, in the **Search** text box, search for and select **Policy**.
2. In the left pane of the **Azure Policy** page, select **Definitions**.
3. From the **Category** dropdown list box, use **Select all** to clear the filter and then select **Kubernetes**.
4. In the **Definition type** dropdown list, select **Initiative**.
5. In the list of filtered definitions, select the policy initiative named **Kubernetes cluster pod security baseline standards for Linux\-based workloads**, and then select **Assign**.
6. On the **Basics** tab of the **Assign initiative** page, set the **Scope** to your Azure subscription and the resource group named **aks\-01\-RG**, which hosts the newly deployed AKS cluster.
7. Ensure that the **Policy enforcement** is set to **Enabled**, and then select **Next** until you reach the **Parameters** tab.
8. On the **Parameters** tab, if **Effect** isn't visible, clear the **Only show parameters that need input or review** checkbox. In the **Effect** drop\-down list, select **Deny**, and then select **Review \+ create**.

Note

You can apply exclusions and inclusions to individual namespaces.
9. On the **Review \+ create** tab, select **Create**.
10. Wait until the assignment takes effect (about 20 minutes). In the Azure portal, navigate to the **Azure Policy** page, select **Compliance**, and check the compliance status for the newly created policy assignment. You can also rerun the `kubectl get constrainttemplates` command to verify that Gatekeeper constraint templates were downloaded to the cluster, but use Azure Policy compliance results to determine compliance status.

#### Validate the effect of Azure Policy

In this task, you validate the effects of Azure Policy.

1. In the Azure portal, in the Bash session of Azure Cloud Shell, use a text editor, such as the built\-in Cloud Shell editor, nano, or vi, to create a file named *nginx\-privileged.yaml* and copy into it the following YAML manifest:

```
apiVersion: v1
kind: Pod
metadata:
  name: nginx-privileged
spec:
  containers:
    - name: nginx-privileged
      image: mcr.microsoft.com/azurelinux/base/nginx:1.28
      securityContext:
        privileged: true

```
2. Save the changes to the file and close it to return to the Bash prompt.
3. Attempt deploying a pod based on the YAML manifest by running the following command:

```
kubectl apply -f nginx-privileged.yaml

```
4. Verify that pod creation fails with an error message that resembles the following one.

```
Error from server ([denied by azurepolicy-container-no-privilege-00edd87bf80f443fa51d10910255adbc4013d590bec3d290b4f48725d4dfbdf9] Privileged container is not allowed: nginx-privileged, securityContext: {"privileged": true}): error when creating "nginx-privileged.yaml": admission webhook "validation.gatekeeper.sh" denied the request: [denied by azurepolicy-container-no-privilege-00edd87bf80f443fa51d10910255adbc4013d590bec3d290b4f48725d4dfbdf9] Privileged container is not allowed: nginx-privileged, securityContext: {"privileged": true}

```

---

## Configure storage for applications running on Azure Kubernetes Service

To optimize container orchestration environments, your organization needs to be able to control platform\-level capabilities, including not only compute but also storage. Choosing the most suitable storage solution for Azure Kubernetes Service (AKS) workloads must account for many factors, including performance, availability, recoverability, security, and cost.

AKS supports both stateless and stateful workloads. Stateful workloads typically require a storage solution for storing and retrieving data. To accommodate this requirement, you can apply a range of native Azure services, including managed databases, disks, and file and blob storage. Each of these options offers different SKUs, sizes, and performance characteristics. Selecting the right option requires careful consideration.

#### Select the right storage service

When choosing the optimal storage for AKS containerized workloads, review [AKS storage concepts](/en-us/azure/aks/concepts-storage) and choose from the following options:

* **Application\-level access to structured or semi\-structured data**. For structured or semi\-structured data, use a platform managed database, such as Azure SQL, Azure Database for MySQL, Azure Database for PostgreSQL, and Azure Cosmos DB.
* **File\-level access to data**. For shared application data that requires high performance, use Azure NetApp Files or Azure Files SSD provisioned v2 shares (`PremiumV2_LRS` or `PremiumV2_ZRS`). The earlier `Premium_LRS` and `Premium_ZRS` SSD shares are still supported, but provisioned v2 is recommended for new deployments. For shared data that requires moderate performance, use Azure Files HDD pay\-as\-you\-go or HDD provisioned v2 shares.
* **Block\-level access to data (self\-managed)**. For applications requiring consistently low latency, high IOPS, and high throughput, use Azure Premium SSD, Azure Premium SSD v2, or Azure Ultra Disk Storage. These options provide flexibility when you want to manage storage characteristics yourself.
* **Object\-level access to data**. For large unstructured data, interact with Azure Blob Storage directly, or mount Blob Storage by using the Azure Blob CSI driver with NFS v3\.0 or BlobFuse.
* **Block\-level access to data (fully managed)**. For a fully managed, cloud\-based volume management and orchestration solution, consider [Azure Container Storage](/en-us/azure/storage/container-storage/container-storage-introduction). It integrates with Kubernetes, allowing dynamic and automatic provisioning of persistent volumes. Azure Container Storage 2\.0\.x supports local NVMe disks; 2\.1\.x and later add support for Azure Elastic SAN. Use Azure Container Storage 2\.1\.x or later for local NVMe or Azure Elastic SAN, and a supported 1\.x release for Azure Disks, because the 2\.x line doesn't support Azure Disks.

#### Plan for pod volumes

AKS typically treats individual pods as ephemeral, disposable resources. Kubernetes volumes let pods store and share data while containers are running. Some volume types, such as `emptyDir`, are ephemeral and exist only for the lifetime of a pod. For data that must persist beyond the lifetime of a pod or across pod rescheduling, use PersistentVolume (PV) resources accessed through PersistentVolumeClaim (PVC)\-backed volumes. When selecting the underlying storage for AKS persistent volumes, your choices include Azure Disks, Azure Files, Azure NetApp Files, Azure Blobs, and, through Azure Container Storage, local NVMe disks and Azure Elastic SAN. Local NVMe storage provides the highest performance but is node\-local and ephemeral, with no built\-in data durability. Pods that consume it through a PersistentVolumeClaim must opt in by setting the `localdisk.csi.acstor.io/accept-ephemeral-storage: "true"` annotation, and the data is lost if the node is deleted or the pod is rescheduled to another node. Use local NVMe only for workloads that can tolerate data loss or that provide their own replication.

AKS volume types include:

* `emptyDir` is used as temporary space for pods. All containers within a pod can access the data on the volume. Data written to this volume type persists only for the lifespan of the pod. Once you delete the pod, the volume is deleted. This volume typically uses the underlying local node disk storage, though it's possible to host it in the node's memory.
* `secret` is used to inject sensitive data, such as passwords, into pods.
* `configMap` is used to inject key\-value pair properties into pods, frequently referencing application configuration settings.
* `persistentVolumeClaim` is used to mount storage requested by a PersistentVolumeClaim. The claim binds to a PersistentVolume, which has a lifecycle independent of any individual pod.

#### Implement AKS persistent volumes

You can use Azure Disk, Azure Files, Azure Blob Storage, Azure NetApp Files, or Azure Container Storage resources to implement PersistentVolume resources in AKS clusters. Azure Blob Storage uses the Azure Blob CSI driver, and Azure NetApp Files dynamic provisioning uses NetApp Trident. The choice is typically based on the desired performance characteristics and whether the workload requires shared or exclusive access to the underlying storage.

To ensure the availability of persistent volumes, you can precreate PersistentVolume resources. Alternatively, you can rely on Kubernetes to create them dynamically. If a pod awaiting scheduling requires storage that is unavailable, Kubernetes can dynamically provision a supported underlying storage resource, such as an Azure Disk, Azure Files share, Azure Blob container, or Azure Container Storage volume, through the relevant CSI driver and StorageClass. Dynamic provisioning relies on the *StorageClass* specification to determine the type of Azure storage to create.

##### Create StorageClasses

The StorageClass is a Kubernetes construct that defines storage characteristics. In AKS, these characteristics map to specific Azure Storage resources.

The StorageClass also defines the *reclaimPolicy*. When a PersistentVolumeClaim that uses the StorageClass is deleted, the reclaimPolicy controls whether the dynamically provisioned underlying Azure storage resource is deleted or, with `Retain`, kept for manual recovery and reclamation. Retained storage isn't automatically reusable until it's manually reclaimed. Starting with Kubernetes version 1\.21, AKS uses Container Storage Interface (CSI) drivers by default and enables CSI migration for supported in\-tree Azure Disk and Azure Files volume types. In Kubernetes version 1\.26 and later, the in\-tree Azure Disk and Azure Files volume types are deprecated and unsupported for new use. Existing in\-tree persistent volumes and StorageClasses can continue to function through CSI migration, but workloads should migrate to CSI drivers. AKS includes built\-in CSI\-based disk and file StorageClasses, such as `managed-csi`, `managed-csi-premium`, `azurefile-csi`, and `azurefile-csi-premium`. When you enable the Azure Blob CSI driver, it provides built\-in `azureblob-nfs-premium` and `azureblob-fuse-premium` StorageClasses. Starting with Kubernetes version 1\.29, built\-in disk StorageClasses in multi\-zone AKS clusters use zone\-redundant storage (ZRS).

##### Configure PersistentVolumeClaims

A PersistentVolumeClaim is a request for a particular `StorageClass`, access mode, and size. The access mode requests how the volume can be mounted — `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`, or `ReadWriteOncePod` — and must be supported by the bound PersistentVolume. As mentioned earlier, Kubernetes can dynamically provision the underlying Azure storage resource if no existing resource can fulfill the claim based on the defined StorageClass.

When a matching PersistentVolume is found or dynamically provisioned, Kubernetes *binds* the PersistentVolume to the PersistentVolumeClaim. The pod then mounts the PersistentVolumeClaim as a volume.

The following YAML manifest describes a PersistentVolumeClaim that uses the custom *managed\-premium\-retain* StorageClass and requests an Azure Disk *5Gi* in size. The *managed\-premium\-retain* StorageClass is created later in the module; modern AKS built\-in StorageClasses are CSI\-based and use names such as *managed\-csi* and *managed\-csi\-premium*:

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: azure-managed-disk
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: managed-premium-retain
  resources:
    requests:
      storage: 5Gi

```

When you create a pod definition, you also specify:

* the PersistentVolumeClaim to request the desired storage.
* the *volumeMount* for your applications to read and write data.

The following YAML manifest illustrates how the PersistentVolumeClaim defined earlier is used to mount a volume on the */mnt/azure* directory:

```
kind: Pod
apiVersion: v1
metadata:
  name: nginx
spec:
  containers:
    - name: myfrontend
      image: mcr.microsoft.com/azurelinux/base/nginx:1.28
      volumeMounts:
      - mountPath: "/mnt/azure"
        name: volume
  volumes:
    - name: volume
      persistentVolumeClaim:
        claimName: azure-managed-disk

```

---

## Deploy an application to an Azure Kubernetes Service cluster

So far, you've been provisioning individual pods to illustrate security\- and storage\-related Azure Kubernetes Service (AKS) concepts. However, for stateless workloads, the recommended approach is to manage pods by using Kubernetes Deployments. Stateful workloads can use StatefulSets when they require stable identities or persistent storage. In this unit, we examine the differences between pods and Deployments and describe the benefits associated with Deployments.

#### Explore Kubernetes pods

Kubernetes uses *pods* to run individual instances of containerized applications. A pod is a logical Kubernetes resource, but application workloads run within a container. There's typically a 1:1 mapping between a pod and a container, although there are scenarios in which a pod may contain multiple, closely integrated containers. All containers that are part of the same pod run on the same node and share networking and storage resources.

When you author a pod, you specify *resource requests* and *limits* on each container. The Kubernetes Scheduler places the pod on a node with sufficient unallocated CPU and memory based on the pod's effective request, which is the sum of its regular container requests, or the highest individual init container request if that's greater, plus any pod overhead. Limits cap the resources a container can consume at runtime: CPU usage is throttled to the limit, while memory limits are enforced reactively, and a container or one of its processes that exceeds the limit can be terminated by the kernel out\-of\-memory killer when the node is under memory pressure. Setting requests and limits prevents a pod from starving the node or other workloads.

Because pods are ephemeral and disposable by default, deploying them as individual resources considerably limits their resiliency and is typically not suitable for production environments. To realize the high availability and redundancy benefits offered by the AKS platform, you should deploy and manage pods by using Kubernetes *controllers*, such as the Deployment Controller.

#### Explore Kubernetes Deployments

A *Deployment* manages a set of pods through ReplicaSets, working to maintain a desired state defined by a pod template. At steady state the replicas share that template, but during rolling updates a Deployment can manage multiple ReplicaSets with different templates, so old and new pods coexist briefly. A Deployment defines the number of pod *replicas* to create, manages ReplicaSets, and lets each ReplicaSet maintain the requested number of pod replicas. If a pod or node fails, the controller creates replacement pods, and the Kubernetes Scheduler places them on healthy nodes with available resources.

You can update Deployments to change the pod template, including the configuration of pods, their container image, or attached storage. During a rolling update, the Deployment Controller:

* Creates a new ReplicaSet that uses the updated pod template.
* Gradually scales down the old ReplicaSet while scaling up the new ReplicaSet, in line with the Deployment's `maxSurge` and `maxUnavailable` settings.
* Continues the process until the new ReplicaSet has fully replaced the old one.

By default, Deployments use 25% `maxUnavailable` and 25% `maxSurge`. Kubernetes rounds percentage values during a rollout (`maxUnavailable` down and `maxSurge` up), so the 75% available and 125% surge figures are a rule of thumb that depends on the replica count; with four replicas, the controller keeps at least three pods available and allows up to five non\-terminating pods. Pods that are terminating can continue to exist and use resources until their grace periods expire, so observed pod counts or resource use can briefly exceed `replicas + maxSurge`.

In addition, if your application requires a minimum number of available instances, you can use *Pod Disruption Budgets* to define how many replicas of a replicated application can be unavailable during voluntary disruptions, such as node drains or AKS node upgrades. Pod Disruption Budgets don't control Deployment rolling updates; use `maxSurge` and `maxUnavailable` for rollout behavior, although pods unavailable during a rollout count against the budget.

Stateful workloads that require stable network identities, ordered deployment or scaling, or stable persistent storage should use *StatefulSets* instead of Deployments.

Most stateless applications in AKS should be managed by Deployments rather than as individually scheduled pods. Kubernetes can monitor Deployment health and status to ensure that the required number of replicas run within the cluster. When scheduled individually, pods don't have a controller to create a replacement if the pod is deleted or the node fails. The kubelet might restart containers on the same node according to the pod's restart policy, but Kubernetes doesn't recreate the pod elsewhere. In addition, Deployments support controlled rollouts and rollbacks.

To help define the Deployment, you use a manifest file in YAML format. You reference the manifest file when running the `kubectl create` or `kubectl apply` commands. For more information, see [AKS cluster and workload concepts](/en-us/azure/aks/concepts-clusters-workloads).

#### Deploy AKS workloads with Helm

Rather than authoring and managing YAML manifests directly, you might want to consider using Helm. Helm is an open\-source package manager for Kubernetes. It automates management of containerized applications by installing reusable packages referred to as Helm *charts* that contain Kubernetes resource definitions, templated manifests, and default configuration values. Each chart installation creates a *release* that Helm can track, upgrade, or roll back. You can store Helm charts either locally or in a remote repository, such as an Azure Container Registry.

#### Namespaces

Kubernetes resources, such as pods and Deployments, are logically grouped into *namespaces*, which helps with organizing them in the manner that reflects their intended use. Namespaces scope resource names and can be used with RBAC, resource quotas, and network policies, but they aren't a hard security boundary by themselves.

When you create an AKS cluster, the following namespaces are created by default:

* **default**: serves as the default namespace for resources that weren't allocated to another namespace during their creation. When you interact with the Kubernetes API (for example, when running `kubectl get pods`), the default namespace is used when none is specified.
* **kube\-node\-lease**: enables nodes to communicate their availability to the control plane.
* **kube\-public**: isn't typically used, but you can use it so that resources are readable across the entire cluster by any client.
* **kube\-system**: hosts core resources, including `CoreDNS`, `konnectivity-agent`, and `metrics-server`, and — when the cluster networking mode uses it — `kube-proxy`. AKS clusters that use Azure CNI powered by Cilium don't run `kube-proxy`. When using AKS, you don't deploy your own applications into this namespace.

Note

`kube-root-ca.crt` is a ConfigMap that Kubernetes creates in namespaces so pods can verify internal Kubernetes API endpoints; it isn't a namespace. AKS add\-ons can create additional namespaces. The Azure Policy add\-on runs the `azure-policy` pods in `kube-system` and the Gatekeeper pods in `gatekeeper-system`. The Istio\-based service mesh add\-on uses `aks-istio-system` for control plane components and, when ingress gateways are enabled, `aks-istio-ingress` for the ingress gateway. Don't deploy application workloads into AKS\-managed namespaces unless the documentation for that feature instructs you to.

---

## Try\-This exercise \- Configure storage for applications that run on Azure Kubernetes Service

In this exercise, you step through the process of configuring a persistent volume for a pod on an Azure Kubernetes Service (AKS) cluster. You use the AKS cluster provisioned in the first exercise of this module.

Note

To complete this exercise, you need an [Azure Subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

#### Create a custom StorageClass in an AKS cluster

In this task, you create a custom StorageClass in the target AKS cluster.

1. From the Azure portal, open a Bash session in Azure Cloud Shell. To make sure that the AKS cluster name and credentials are available in the current session (Cloud Shell variables don't persist between sessions), run the following commands:

```
AKSRG='aks-01-RG'
AKSNAME='aks-01'
az aks get-credentials --resource-group $AKSRG --name $AKSNAME --overwrite-existing

```
2. In the Azure portal, in the Bash session of Azure Cloud Shell, use the built\-in editor to create a file named *premium\-storage\-class.yaml* and copy into it the following YAML manifest:

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-premium-retain
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_LRS
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true

```

Note

The `provisioner` is set to **disk.csi.azure.com**, the Azure Disk CSI driver included with modern AKS clusters. The `skuName` value uses Premium SSD locally redundant storage (LRS). The `reclaimPolicy` is set to **Retain**, so the underlying Azure Disk isn't deleted automatically when the PersistentVolumeClaim is deleted.
3. Save the changes to the file and close it to return to the Bash prompt.
4. To create the custom StorageClass, from the Bash session in the Azure Cloud Shell, run the following command:

```
kubectl apply -f premium-storage-class.yaml

```

#### Create a PersistentVolumeClaim in an AKS cluster

In this task, you create a PersistentVolumeClaim in the target AKS cluster.

1. From the Bash session in the Azure Cloud Shell, use the built\-in editor to create a file named *persistent\-volume\-claim\-5g.yaml* and copy into it the following YAML manifest:

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: azure-managed-disk
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: managed-premium-retain
  resources:
    requests:
      storage: 5Gi

```

Note

The `storageClassName` is set to **managed\-premium\-retain**.
2. Save the changes to the file and close it to return to the Bash prompt.
3. To create the PersistentVolumeClaim, from the Bash session in the Azure Cloud Shell, run the following command:

```
kubectl apply -f persistent-volume-claim-5g.yaml

```

#### Deploy a pod with a persistent volume mount in an AKS cluster

In this task, you deploy a pod with a persistent volume mount in the target AKS cluster.

1. From the Bash session in the Azure Cloud Shell, use the built\-in editor to create a file named *pod\-with\-storage\-mount.yaml* and copy into it the following YAML manifest:

```
kind: Pod
apiVersion: v1
metadata:
  name: nginx
spec:
  containers:
    - name: myfrontend
      image: mcr.microsoft.com/azurelinux/base/nginx:1.28
      volumeMounts:
      - mountPath: "/mnt/azure"
        name: volume
  volumes:
    - name: volume
      persistentVolumeClaim:
        claimName: azure-managed-disk

```

Note

The `mountPath` is set to **/mnt/azure** and `claimName` is set to **azure\-managed\-disk**.
2. Save the changes to the file and close it to return to the Bash prompt.
3. To deploy the pod, from the Bash session in the Azure Cloud Shell, run the following command:

```
kubectl apply -f pod-with-storage-mount.yaml

```

#### Validate the effect of the volume mount

In this task, you validate that the volume mount was successful.

1. To verify that the nginx pod was provisioned and wait until it's ready, from the Bash session in the Azure Cloud Shell, run the following commands:

```
kubectl get pods
kubectl wait --for=condition=Ready pod/nginx --timeout=120s

```
2. To write a test file to the **/mnt/azure** directory and confirm it exists, run the following commands:

```
kubectl exec -i nginx -- sh -c "echo 'persistent-volume-test' > /mnt/azure/test.txt"
kubectl exec -i nginx -- sh -c "ls /mnt/azure"

```
3. To delete the nginx pod, run the following command:

```
kubectl delete pod nginx

```
4. Now, re\-create the nginx pod and wait until it's ready by running the following commands:

```
kubectl apply -f pod-with-storage-mount.yaml
kubectl wait --for=condition=Ready pod/nginx --timeout=120s

```
5. Finally, verify that the test file persisted on the underlying Azure Disk by running the following commands:

```
kubectl exec -i nginx -- sh -c "ls /mnt/azure"
kubectl exec -i nginx -- sh -c "cat /mnt/azure/test.txt"

```

#### Delete the resources provisioned in the exercise

In this task, you delete the resources you provisioned in this exercise.

1. To delete the nginx pod, record the PersistentVolume and managed disk created for the claim, and then delete the PersistentVolumeClaim and retained PersistentVolume, from the Bash session in the Azure Cloud Shell, run the following commands:

```
kubectl delete pod nginx
kubectl wait --for=delete pod/nginx --timeout=120s
PV_NAME=$(kubectl get pvc azure-managed-disk -o jsonpath='{.spec.volumeName}')
DISK_ID=$(kubectl get pv $PV_NAME -o jsonpath='{.spec.csi.volumeHandle}')
kubectl get pvc
kubectl delete pvc azure-managed-disk
kubectl delete pv $PV_NAME

```

To wait for the retained Azure Disk to detach and then delete it, run the following commands:

```
az disk wait --ids "$DISK_ID" --custom "managedBy==null" --timeout 600
az disk delete --ids "$DISK_ID" --yes

```

Note

Because the StorageClass uses the **Retain** reclaim policy, deleting the PersistentVolumeClaim doesn't delete the PersistentVolume or the underlying Azure Disk. Deleting the PersistentVolume object also doesn't delete the external Azure Disk — only `az disk delete` does that. To keep the disk for later manual recovery, skip only `az disk delete`; you can keep or delete the PV object independently based on your recovery plan.
2. To list and delete the StorageClass, run the following commands:

```
kubectl get sc
kubectl delete sc managed-premium-retain

```

Note

This keeps the AKS cluster because you use it in the next exercise.

---

## Try\-This exercise \- Deploy an application to Azure Kubernetes Service cluster

In this exercise, you walk through the process of creating and updating a Deployment in an Azure Kubernetes Service (AKS) cluster. You use the cluster you provisioned in the first exercise of this module.

Note

To complete this exercise, you need an [Azure Subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).  

#### Prepare for creating a Deployment in an Azure Kubernetes Service cluster

In this task, you prepare to create a Deployment in an AKS cluster by creating a namespace using Azure Cloud Shell.

1. From the Azure portal, open a Bash session in the Azure Cloud Shell. To make sure that the AKS cluster name and credentials are available in the current session (Cloud Shell variables don't persist between sessions), run the following commands:

```
AKSRG='aks-01-RG'
AKSNAME='aks-01'
az aks get-credentials --resource-group $AKSRG --name $AKSNAME --overwrite-existing

```
2. To create a namespace and list the existing namespaces, run the following commands:

```
kubectl create namespace demo-deployment
kubectl get namespaces

```
3. Run the following commands to review the node pool name and scale the node pool to two nodes. Because the cluster currently has one node, this scales the node pool by adding one node. The `--node-count` value is the absolute target node count, not an increment.

```
az aks show --resource-group $AKSRG --name $AKSNAME --query "agentPoolProfiles[].{Name:name,Count:count}" -o table
NODEPOOL=$(az aks show --resource-group $AKSRG --name $AKSNAME --query "agentPoolProfiles[0].name" -o tsv)
az aks scale --resource-group $AKSRG --name $AKSNAME --node-count 2 --nodepool-name $NODEPOOL

```
4. To wait until the extra node is fully provisioned and confirm both nodes appear as **Ready**, run the following commands:

```
kubectl wait --for=condition=Ready nodes --all --timeout=300s
kubectl get nodes

```

#### Create a Deployment

In this task, you create a Deployment in the target AKS cluster.

1. In the Azure portal, in the Bash session of Azure Cloud Shell, use the built\-in editor to create a file named *nginx\-deployment.yaml* and copy into it the following YAML manifest:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: mcr.microsoft.com/azurelinux/base/nginx:1.25
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 250m
            memory: 64Mi
          limits:
            cpu: 500m
            memory: 256Mi

```
2. Save the changes to the file and close it to return to the Bash prompt.
3. To create the Deployment, from the Bash session in the Azure Cloud Shell, run the following command:

```
kubectl apply -f nginx-deployment.yaml --namespace demo-deployment

```
4. To validate the Deployment rollout and enumerate Deployments, pods, and ReplicaSets, run the following commands:

```
kubectl rollout status deployment/nginx-deployment --namespace demo-deployment
kubectl get deployments --namespace demo-deployment
kubectl get pods --namespace demo-deployment
kubectl get rs --namespace demo-deployment

```

#### Update the Deployment

In this task, you update the Deployment by replacing the image used by its pods.

1. To replace the image used by the Deployment, from the Bash session in the Azure Cloud Shell, run the following command:

```
kubectl set image deployment/nginx-deployment nginx=mcr.microsoft.com/azurelinux/base/nginx:1.28 --namespace demo-deployment

```
2. To validate the Deployment rollout and enumerate Deployments, pods, and ReplicaSets, run the following commands:

```
kubectl rollout status deployment/nginx-deployment --namespace demo-deployment
kubectl get deployments --namespace demo-deployment
kubectl get pods --namespace demo-deployment
kubectl get rs --namespace demo-deployment

```

#### Delete the resources provisioned in the module

In this task, you delete the resource group that contains the AKS cluster and related resources.

1. Since this is the last exercise in the module, from the Bash session in the Azure Cloud Shell, run the following commands. The `AKSRG` variable is reset in case it isn't defined in the current Cloud Shell session:

```
AKSRG='aks-01-RG'
az group delete --name $AKSRG --yes --no-wait

```

---

## Module assessment

Choose the best response for each question.

### Check your knowledge

---

## Summary

### In this module, you learned how to:

* Provision an Azure Kubernetes Service (AKS) cluster.
* Install the Azure Policy add\-on for AKS.
* Assign an Azure Policy initiative to an AKS cluster.
* Validate the effect of Azure Policy.
* Select storage options for AKS containerized workloads.
* Configure persistent storage for pods by using StorageClasses and PersistentVolumeClaims.
* Describe why Kubernetes Deployments are preferred over individual pods, and create and update a Deployment in AKS.

### Learn more

* [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) \| [Azure free account FAQ](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn#FAQ)
* [Free account for Students](https://azure.microsoft.com/free/students/?cid=msft_learn) \| [Azure for students FAQ](/en-us/azure/education-hub/azure-dev-tools-teaching/program-faq#azure-for-students)
* [Create an Azure account](/en-us/training/modules/create-an-azure-account/?azure-portal=true) module on Learn.
* [What is Azure Kubernetes Service (AKS)?](/en-us/azure/aks/intro-kubernetes)
* [Use Pod Security Admission in AKS](/en-us/azure/aks/use-psa)
* [Understand Azure Policy for Kubernetes clusters](/en-us/azure/governance/policy/concepts/policy-for-kubernetes)
* [Storage options for applications in AKS](/en-us/azure/aks/concepts-storage)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/deploy-applications-azure-kubernetes-service/_

## Fuentes
- [Deploy applications to Azure Kubernetes Service](https://learn.microsoft.com/en-us/training/modules/deploy-applications-azure-kubernetes-service/?WT.mc_id=api_CatalogApi)
