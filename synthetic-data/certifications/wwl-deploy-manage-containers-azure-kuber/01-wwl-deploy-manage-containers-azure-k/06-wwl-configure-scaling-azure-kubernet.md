# Configure scaling in Azure Kubernetes Service

> Curso: Deploy containers by using Azure Kubernetes Service (AKS) (wwl-deploy-manage-containers-azure-kubernetes-serv) · Seccion: Deploy containers by using Azure Kubernetes Service (AKS)
> Duracion estimada: 48 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

This module covers how to scale applications in Azure Kubernetes Service (AKS). You learn when to scale workload replicas, when to scale AKS node pools, and how to use Azure Container Instances (ACI) for burst capacity. You also see where event\-driven autoscaling and node auto\-provisioning fit for scenarios beyond the core exercises.

### Scenario

Imagine you're a platform engineer for a retail company that runs its checkout service on AKS. During weekday lunchtimes and seasonal promotions, traffic to the checkout service can grow tenfold within minutes, while traffic at night drops to a small fraction of peak. Today, your team responds to spikes by leaving extra VM\-backed nodes running around the clock, which inflates the cluster bill. During larger promotions, pods still spend several minutes in `Pending` while new VM\-backed nodes provision, which puts checkout SLAs at risk.

Your goal is to use AKS scaling features so the cluster matches demand at each layer: the right number of pod replicas for the current load, the right number of nodes to host those replicas, and a fast path for short\-lived bursts that can't wait for new VM\-backed nodes. This module helps you compare the available AKS scaling options and choose the right one for each scenario.

### Learning objectives

After completing this module, you'll be able to:

* Manually scale workload replicas and AKS node pools
* Use the horizontal pod autoscaler (HPA) to scale workload replicas
* Use the cluster autoscaler to scale AKS node pools
* Use virtual nodes to run burst workloads in Azure Container Instances (ACI)

---

## Scaling options in Azure Kubernetes Service

When running applications in Azure Kubernetes Service (AKS), you might need to increase or decrease compute resources. Most AKS scaling decisions act at one of two layers: workload replicas or node pool capacity. Scaling replicas changes how many pods run for an application. Scaling nodes changes the compute capacity available for Kubernetes to schedule those pods. For sudden or short\-lived demand, you can also use Azure Container Instances (ACI) through virtual nodes.

This module summarizes the core AKS application scaling concepts, including:

* Manual scaling of workload replicas and AKS node pools
* Horizontal pod autoscaler (HPA)
* Cluster autoscaler
* Virtual nodes and Azure Container Instances (ACI)

#### Manually scale pods or nodes

You can manually scale a workload's replica count or an AKS node pool to test how your application responds to more or less capacity. Manual scaling sets a fixed target, such as a specific replica count or node count, instead of reacting automatically to load. When you scale replicas, Kubernetes reconciles the desired replica count by creating or terminating pods. When you scale AKS nodes, use AKS scaling operations: for a single\-node\-pool cluster you can use `az aks scale`, and for a specific node pool or multi\-node\-pool cluster use `az aks nodepool scale` (or `az aks scale --nodepool-name`). Removing AKS nodes directly with `kubectl` isn't supported.

During node scale\-in, AKS cordons and drains nodes to minimize disruption before reducing the underlying compute capacity. For node pools backed by Virtual Machine Scale Sets, Azure determines which VM instances to remove during scale\-in. To learn more about how nodes are selected for removal, see the [Virtual Machine Scale Sets FAQ](/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-faq#if-i-reduce-my-scale-set-capacity-from-20-to-15--which-vms-are-removed-). To learn how to manually scale AKS nodes, see [Manually scale the node count in an AKS cluster](/en-us/azure/aks/scale-cluster).

#### Horizontal pod autoscaler

Kubernetes uses the horizontal pod autoscaler (HPA) to monitor demand and automatically scale the number of workload replicas. HPA can use resource metrics, such as CPU or memory, and it can use custom or external metrics when the required metric adapters are configured. For resource utilization targets, containers in the targeted workload must define requests for the resource being measured, such as CPU requests for CPU\-based scaling, so HPA can calculate utilization correctly.

By default, HPA evaluates each scaling target every 15 seconds, controlled by the kube\-controller\-manager `--horizontal-pod-autoscaler-sync-period` setting. Each evaluation uses the latest sample from the Metrics API. The current upstream Metrics Server reference manifests collect resource metrics from each Kubelet every 15 seconds (`--metric-resolution=15s`); the actual cadence depends on the deployed Metrics Server configuration in your cluster. HPA requires Metrics Server for resource metrics such as CPU and memory. To learn how to configure HPA in AKS, see [Autoscale pods in AKS](/en-us/azure/aks/tutorial-kubernetes-scale#autoscale-pods).

When you configure HPA for a workload such as a Deployment, you define the minimum and maximum number of replicas that can run. You also define the metric to monitor and base scaling decisions on, such as CPU usage.

Horizontal scaling is a reaction to an increased load that results in deploying more pods. Horizontal scaling differs from vertical scaling, where more resources are assigned to the pods that are already running a workload.

If the load decreases, and the number of pods is above the minimum, horizontal scaling adjusts the workload to scale back down.

#### Cooldown of scaling events

Because metric samples are refreshed over time and new pods need time to start receiving traffic, a previous scaling event might not be reflected before another HPA evaluation occurs. This behavior could cause HPA to change the number of replicas before the application workload and resource demands adjust to the previous change.

To minimize rapid oscillation, Kubernetes applies stabilization behavior to scaling decisions. By default, scale\-up uses a stabilization window of 0 seconds (subject to the default scale\-up rate policies), while scale\-down decisions are stabilized for *5 minutes* (`behavior.scaleDown.stabilizationWindowSeconds: 300`, also exposed by the kube\-controller\-manager `--horizontal-pod-autoscaler-downscale-stabilization` flag). For more information, see the Kubernetes documentation for [Horizontal Pod Autoscaler algorithm details](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#algorithm-details).

#### Cluster autoscaler

The cluster autoscaler adjusts the number of nodes in AKS node pools. It doesn't scale nodes directly from CPU or memory usage. Instead, it reacts when pods can't be scheduled because their resource requests don't fit on available nodes, and it removes nodes that have been underutilized long enough to be unnecessary. By default, the cluster autoscaler reevaluates the cluster every 10 seconds and considers nodes for scale\-in after they're unneeded for 10 minutes. Scale\-in requires pods on candidate nodes to be evictable and schedulable elsewhere, so design workloads with realistic resource requests, appropriate replica counts, and disruption budgets.

The cluster autoscaler is often used with HPA. HPA increases or decreases the number of pod replicas based on application demand, and the cluster autoscaler adds nodes when newly created pods are pending because the node pool lacks capacity. Configure minimum and maximum node counts on each autoscaled node pool, and let the cluster autoscaler manage the underlying scale settings. Don't configure separate Virtual Machine Scale Sets autoscale rules for AKS node pools that use the cluster autoscaler. For implementation details, see [Use the cluster autoscaler in AKS](/en-us/azure/aks/cluster-autoscaler).

#### Burst to Azure Container Instances

For sudden or short\-lived capacity needs, virtual nodes can let AKS schedule pods to run as ACI container groups. ACI\-backed pods can start without waiting for the cluster autoscaler to provision more VM\-backed nodes, and you pay per second for the container instances while they run. Virtual nodes are best for workloads that fit ACI's supported feature set; they aren't a replacement for every workload that runs on VM\-backed node pools. The AKS virtual nodes add\-on supports Linux pods and nodes only and requires Azure CNI advanced (VNet) networking. Clusters that use kubenet aren't supported, and not every Azure CNI mode is supported (for example, Azure CNI Overlay isn't recommended where features such as virtual nodes are required). Verify support for the specific Azure CNI mode in current documentation before adopting virtual nodes. Review current regional availability, networking requirements, quotas, and limitations before relying on virtual nodes. For more information, see [Virtual nodes on Azure Container Instances](/en-us/azure/container-instances/container-instances-virtual-nodes) and [Create and configure an AKS cluster to use virtual nodes](/en-us/azure/aks/virtual-nodes).

#### Other scaling options

AKS also supports additional scaling mechanisms that build on the concepts in this module:

* [Kubernetes Event\-driven Autoscaling (KEDA)](/en-us/azure/aks/keda-about) scales workloads in response to event sources such as queue length or external service metrics, instead of relying only on in\-cluster CPU or memory resource metrics. KEDA can scale supported workloads to zero. For `ScaledObject`\-based autoscaling, KEDA uses HPA in the background, so avoid configuring a KEDA `ScaledObject` and a separate HPA for the same workload unless the design explicitly accounts for that interaction.
* [Node auto\-provisioning (NAP)](/en-us/azure/aks/node-auto-provisioning), which uses the open\-source Karpenter project, dynamically provisions nodes of an appropriate VM SKU based on pending pod requirements. NAP is different from the cluster autoscaler because it can select suitable node configurations instead of only changing the count of an existing node pool. Check the current prerequisites and limitations before using NAP; for example, NAP can't be enabled on clusters that use the cluster autoscaler.

The remaining units focus on the cluster autoscaler and on bursting to Azure Container Instances with virtual nodes.

---

## Cluster autoscaler

To respond to changing pod demand, the Kubernetes cluster autoscaler adjusts the number of nodes in an autoscale\-enabled node pool. The cluster autoscaler doesn't scale because of CPU or memory pressure on running nodes. Instead, it periodically reevaluates the cluster and looks for pods that can't be scheduled because their resource requests don't fit on the available nodes. By default, the scan interval is 10 seconds.

If the cluster autoscaler determines that a change is required, the number of nodes in the affected node pool is increased or decreased within the minimum and maximum node counts that you configure. The maximum count limits scale\-out, and the minimum count prevents scale\-in below the capacity you require. Don't manually enable or change Virtual Machine Scale Set autoscaling for AKS nodes. Let the Kubernetes cluster autoscaler manage the node pool scale settings.

For more information about how the cluster autoscaler works in AKS and how to enable it by using Azure CLI parameters such as `--enable-cluster-autoscaler`, `--min-count`, and `--max-count`, see [Cluster autoscaling in AKS overview](/en-us/azure/aks/cluster-autoscaler-overview) and [Use the cluster autoscaler in AKS](/en-us/azure/aks/cluster-autoscaler).

The cluster autoscaler is typically used alongside the [horizontal pod autoscaler](/en-us/azure/aks/concepts-scale#horizontal-pod-autoscaler). When combined, the horizontal pod autoscaler increases or decreases the number of pods based on application demand, and the cluster autoscaler adjusts the number of nodes to run schedulable pods.

#### Scale out events

If a node doesn't have sufficient compute resources to run a requested pod, that pod can't progress through the scheduling process. The pod can't start unless more compute resources are available within the node pool.

When the cluster autoscaler notices pods in a `Pending` state because of node pool resource constraints, the number of nodes within the appropriate node pool is increased to provide extra compute resources. A pending pod doesn't always trigger scale\-out. The cluster autoscaler simulates whether a new node could schedule the pod, so scale\-out might not be triggered if the pod is blocked by constraints such as taints and tolerations, node affinity, restrictive topology spread rules, PersistentVolume node affinity or volume topology conflicts, pod PriorityClass values below `-10`, or the node pool maximum. Even when scale\-out is triggered, core vCPU quota exhaustion, subnet IP exhaustion, or request/API rate limits can cause node provisioning to fail or back off. When the new nodes are successfully deployed and marked **Ready**, the Kubernetes scheduler can place the pending pods on them.

If your application needs to scale rapidly, some pods might remain pending while the cluster autoscaler provisions more VM\-backed nodes. For applications that have high burst demands and compatible workload requirements, you can scale with virtual nodes and [Azure Container Instances](/en-us/azure/aks/concepts-scale#burst-to-azure-container-instances-aci).

#### Scale in events

The cluster autoscaler also evaluates whether nodes are underutilized and whether their pods can safely move to other nodes. This scenario indicates the node pool has more compute resources than required, and the number of nodes can be decreased. By default, nodes that are no longer needed for 10 minutes are eligible for deletion. When this situation occurs, the cluster autoscaler drains the selected nodes, the pods are rescheduled on other available nodes, and the node count decreases.

Your applications might experience some disruption as pods are scheduled on different nodes when the cluster autoscaler decreases the number of nodes. To minimize disruption, avoid relying on a single pod instance, configure appropriate replica counts, and use [pod disruption budgets](https://kubernetes.io/docs/tasks/run-application/configure-pdb/) that allow safe movement while preserving availability. Overly restrictive disruption budgets, pods that aren't managed by a controller, scheduling constraints that can't be satisfied elsewhere, pods with local storage when the autoscaler profile skips them, pods marked with `cluster-autoscaler.kubernetes.io/safe-to-evict: "false"`, or non\-DaemonSet, non\-mirror pods in the `kube-system` namespace when the profile skips system pods can prevent scale\-in.

---

## Burst to Azure Container Instances

To rapidly scale application workloads in AKS, you can integrate with Azure Container Instances (ACI). Kubernetes has built\-in components to scale the replica and node count. However, if your application needs to rapidly scale, the [horizontal pod autoscaler](/en-us/azure/aks/concepts-scale#horizontal-pod-autoscaler) might schedule more pods than the existing compute resources in the node pool can support. If configured, this scenario triggers the [cluster autoscaler](/en-us/azure/aks/concepts-scale#cluster-autoscaler) to deploy more VM\-backed nodes in the node pool, but it might take a few minutes for those nodes to successfully provision and allow the Kubernetes scheduler to run pods on them.

ACI lets you quickly deploy container instances without extra infrastructure overhead and uses per\-second billing, so burst capacity can scale with demand without paying for idle VM\-backed nodes. When you connect ACI with AKS, ACI becomes a secured, logical extension of your AKS cluster. The [virtual nodes](/en-us/azure/aks/virtual-nodes) component, which is based on [Virtual Kubelet](https://virtual-kubelet.io/), is installed in your AKS cluster and presents ACI as a virtual Kubernetes node. Kubernetes can then schedule pods that run as ACI container groups through virtual nodes, not as pods on VM\-backed nodes directly in your AKS cluster.

Your containerized application usually doesn't require code changes to use virtual nodes, but the workload must be compatible with ACI and the Kubernetes manifest must target the virtual node. At minimum, the pod spec needs a `nodeSelector` for `kubernetes.io/role: agent`, `kubernetes.io/os: linux`, and `type: virtual-kubelet`, plus tolerations for the `virtual-kubelet.io/provider` and `azure.com/aci` taints. Your deployments can then burst to ACI without waiting for the cluster autoscaler to finish deploying new VM\-backed nodes in your AKS cluster.

Virtual nodes use a delegated subnet, separate from the subnet that hosts your AKS agent nodes, in the same virtual network as your AKS cluster. This virtual network configuration secures the traffic between ACI and AKS. Like an AKS cluster, an ACI instance is a secure, logical compute resource isolated from other users.

Note

This unit covers the AKS virtual nodes add\-on as documented in the linked Microsoft Learn articles. Microsoft is also evolving the virtual nodes experience for ACI; check current documentation for newer experiences and the limitations that still apply before designing a production rollout.

#### Requirements and limitations for virtual nodes

Virtual nodes have specific requirements and limitations that you should understand before adopting them:

* **Operating system**: The AKS virtual nodes add\-on supports Linux pods and Linux nodes. Windows containers aren't supported through the add\-on.
* **Networking**: Virtual nodes require AKS clusters that use Azure CNI advanced (VNet) networking. Clusters that use kubenet aren't supported, and Azure CNI Overlay isn't recommended for clusters that need features such as virtual nodes. Verify support for the specific Azure CNI mode in current AKS virtual nodes documentation before adopting them.
* **Subnet**: Virtual nodes require a delegated subnet that's separate from the subnet that hosts the AKS agent nodes.
* **API server access**: Pods that run in ACI need outbound access to the AKS API server endpoint to configure networking.
* **Provider registration and availability**: The `Microsoft.ContainerInstance` resource provider must be registered in the subscription, and the deployment region must support ACI virtual network SKUs.
* **Subnet permissions**: The managed identity used by the virtual node add\-on needs the **Network Contributor** role on the delegated virtual node subnet.
* **Workload compatibility**: Virtual nodes are best suited for bursty, stateless Linux workloads. Review ACI quotas and limitations before depending on features such as persistent volumes (other than inline Azure Files mounts), init containers, DaemonSets, Kubernetes network policies, managed identities, IPv6, container lifecycle hooks, host aliases, or API server authorized IP ranges, because these features are limited or unsupported on virtual nodes. Some private image pull scenarios require Kubernetes image pull secrets instead of integrated AKS\-to\-ACR authentication.

To enable the add\-on with the Azure CLI, use `az aks enable-addons --resource-group <resource-group> --name <cluster-name> --addons virtual-node --subnet-name <virtual-node-subnet-name>` after you create the required subnet, then grant the add\-on identity access to that subnet as described in the procedure. For the full procedure, regional availability, and current limitations, see [Create and configure an AKS cluster to use virtual nodes](/en-us/azure/aks/virtual-nodes), [Create and configure virtual nodes by using Azure CLI](/en-us/azure/aks/virtual-nodes-cli), and [Virtual nodes on Azure Container Instances](/en-us/azure/container-instances/container-instances-virtual-nodes).

---

## When to use the cluster autoscaler

You may need to adjust the number of nodes that run your workloads. The cluster autoscaler component watches for pods in your cluster that can't be scheduled on existing nodes because of resource constraints. When unscheduled pods can run on more nodes and a node pool hasn't reached its configured maximum, the number of nodes in that node pool increases to meet application demand. The cluster autoscaler also checks whether underutilized nodes can be removed and their pods safely rescheduled, then decreases the number of nodes as needed. This ability to automatically scale up or down the number of nodes in your AKS cluster lets you run an efficient, cost\-effective cluster. For deeper guidance on how the cluster autoscaler behaves and the best practices to follow, see [Cluster autoscaling in AKS overview](/en-us/azure/aks/cluster-autoscaler-overview).

#### About the cluster autoscaler

To adjust to changing application demands, such as between the workday and evening or on a weekend, clusters often need a way to automatically scale. This module focuses on two complementary AKS autoscaling options:

* The **cluster autoscaler** periodically checks for pods that can't be scheduled on nodes because of resource constraints. By default, it reevaluates the cluster every 10 seconds. The cluster then automatically increases the number of nodes in an autoscale\-enabled node pool, up to the configured maximum.
* The **horizontal pod autoscaler** uses the Metrics Server in a Kubernetes cluster to monitor the resource demand of pods. If an application needs more resources, the number of pods is automatically increased to meet the demand.

Both the horizontal pod autoscaler and cluster autoscaler can decrease the number of pods and nodes as needed. The cluster autoscaler doesn't add nodes because a node has high CPU or memory use; it reacts when pods can't be scheduled and uses pod resource requests in its scheduling simulations. It decreases the number of nodes only after capacity has been unneeded for a configured period and the pods on the node can be evicted and rescheduled elsewhere. In the default autoscaler profile, `scale-down-unneeded-time` is 10 minutes, and scale\-down evaluation resumes 10 minutes after a node is added. Autoscaler profile settings apply cluster\-wide to all autoscale\-enabled node pools. For more information, see [Use the cluster autoscaler profile](/en-us/azure/aks/cluster-autoscaler#use-the-cluster-autoscaler-profile).

The cluster autoscaler might be unable to scale down in the following situations where pods can't move:

* A pod isn't backed by a controller object, such as a Deployment, ReplicaSet, Job, or StatefulSet.
* A pod disruption budget (PDB) would be violated by evicting the pod, such as when `minAvailable` or `maxUnavailable` is too restrictive for the current replica count.
* A pod uses scheduling constraints, such as node selectors, node affinity or anti\-affinity, topology spread constraints, persistent volume topology, resource requests, or host ports, that can't be honored on a different node.
* A pod has the `cluster-autoscaler.kubernetes.io/safe-to-evict: "false"` annotation.
* A pod uses local storage and the autoscaler profile is configured to skip nodes that run pods with local storage.
* A node has a non\-DaemonSet, non\-mirror pod in the `kube-system` namespace while the profile keeps the default `skip-nodes-with-system-pods=true` behavior.

Scale\-up can also be blocked or delayed by node pool and Azure infrastructure limits. Common AKS causes include the node pool maximum size, regional vCPU quota exhaustion, subnet IP address exhaustion, and API rate limits. Set maximum node counts that fit your subscription and network capacity, and request quota increases before relying on higher limits. For more information, see [Common issues and mitigation recommendations for cluster autoscaling in AKS](/en-us/azure/aks/cluster-autoscaler-overview#common-issues-and-mitigation-recommendations).

The cluster and horizontal pod autoscalers can work together and are often both deployed in a cluster. When combined, the horizontal pod autoscaler runs the number of pods required to meet application demand. The cluster autoscaler runs the number of nodes required to support the scheduled pods.

---

## Try\-this exercise \- Scale the node count in an Azure Kubernetes Service cluster

In this exercise, you use the Azure portal to enable the cluster autoscaler on a node pool of an existing AKS cluster. Enabling the cluster autoscaler lets the node pool automatically add or remove nodes in response to pod scheduling demand.

You can scale the number of nodes in your cluster to increase the total number of cores and memory available for your container applications.

AKS lets you manually set a fixed node count or enable the cluster autoscaler so the node pool grows and shrinks automatically within minimum and maximum limits. The cluster autoscaler scales up when pods can't be scheduled because the node pool doesn't have enough resources, and scales down when nodes are no longer needed and their pods can move elsewhere. When a node is removed, AKS cordons and drains the node to minimize disruption to running applications. When AKS adds nodes, it waits until nodes are marked **Ready** by the Kubernetes cluster before pods are scheduled on them. In this exercise, you enable the cluster autoscaler from the Azure portal.

Note

To complete this exercise, you need:

* An [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* An existing AKS cluster with at least one node pool. To create one, see [Quickstart: Deploy an Azure Kubernetes Service (AKS) cluster by using the Azure portal](/en-us/azure/aks/learn/quick-kubernetes-deploy-portal).
* A minimum and maximum node count that fits your workload, node pool mode, subscription vCPU quotas, and subnet IP capacity. The cluster autoscaler can't scale past the maximum count, and scale\-up can fail if Azure quota or network capacity is exhausted. For more information, see [Scale node pools in Azure Kubernetes Service (AKS)](/en-us/azure/aks/scale-node-pools) and [Common issues and mitigation recommendations for cluster autoscaling in AKS](/en-us/azure/aks/cluster-autoscaler-overview#common-issues-and-mitigation-recommendations).

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to your AKS cluster resource.
2. In the service menu, under **Settings**, select **Node pools**.
3. Select the node pool name to open its details.
4. Select **Scale node pool**.
5. Select **Autoscale** and set the minimum and maximum node count.

The autoscaler can change the node count only within these bounds. System node pools host critical system pods and can't scale to `0`. Use at least two nodes for system node pools; for a production AKS cluster with a single system node pool, use at least three nodes. User node pools can use a minimum of `0` if workloads can tolerate the time required to add nodes again. For more information, see [System and user node pools](/en-us/azure/aks/use-system-pools#system-and-user-node-pools).
6. Select **Apply** to enable node scaling.

After autoscale is enabled, the cluster autoscaler manages the node count for that node pool automatically, and manual scaling for the pool is disabled. To change the bounds later, update the minimum and maximum node count for the node pool instead of setting a fixed node count. The equivalent Azure CLI operation is `az aks nodepool update` with `--update-cluster-autoscaler`, `--min-count`, and `--max-count`. To return to a fixed node count, disable the cluster autoscaler on the node pool and then scale the node pool manually with `az aks nodepool scale --node-count`. Don't manually configure Virtual Machine Scale Set autoscaling for AKS nodes.

#### Clean up

If you only enabled autoscale to try the procedure, return the node pool to its previous configuration to avoid unintended cost. To revert, repeat the previous steps and either restore the previous fixed node count by selecting **Manual** and entering the original node count, or update the minimum and maximum values to match your standard configuration. Equivalent Azure CLI operations are `az aks nodepool update --disable-cluster-autoscaler` followed by `az aks nodepool scale --node-count <count>`.

For more information about how the cluster autoscaler works and recommended best practices, see [Cluster autoscaling in AKS overview](/en-us/azure/aks/cluster-autoscaler-overview).

---

## Automatically scale a cluster on Azure Kubernetes Service

The cluster autoscaler watches for pods in your cluster that can't be scheduled because the pods' requested resources don't fit on the available nodes. When it detects unschedulable pods that could run if the node pool had more capacity, it increases the number of nodes. It also evaluates underutilized nodes and, after pods can be safely moved, decreases the node count when capacity is no longer needed. This ability to automatically scale up or down the number of nodes in your AKS cluster lets you run an efficient, cost\-effective cluster.

The cluster autoscaler responds to Kubernetes scheduling decisions, not directly to CPU or memory pressure on running nodes. Define appropriate resource requests on workloads so the scheduler and the autoscaler can determine when more node capacity is required. When the horizontal pod autoscaler (HPA) creates more replicas, those new pods remain `Pending` if they can't fit on existing nodes. The cluster autoscaler can then add nodes, up to the node pool's `--max-count`, so the scheduler can place the pods.

Choose one of the following sections that matches your scenario. Don't run both procedures against the same cluster.

#### Enable the cluster autoscaler on a new cluster

The following procedure creates a new AKS cluster with a single (default) node pool that has the cluster autoscaler enabled. For multi\-node\-pool clusters, configure each node pool individually with `az aks nodepool` commands.

The cluster autoscaler is a Kubernetes component. Although the AKS cluster uses a virtual machine scale set for the nodes, don't manually enable or edit settings for scale set autoscale in the Azure portal or using the Azure CLI. Let the cluster autoscaler manage the required scale settings.

1. Create a resource group using the `az group create` command.

```
az group create --name myResourceGroup --location eastus

```
2. Create an AKS cluster using the `az aks create` command and enable and configure the cluster autoscaler on the node pool for the cluster using the `--enable-cluster-autoscaler` parameter and specifying `--min-count` and `--max-count` for the node pool. The default node pool is a system node pool. The Azure CLI accepts a `--min-count` of `1` for system node pools, but Microsoft recommends at least two nodes (and at least three nodes for a production cluster with a single system node pool) so that critical system pods remain healthy. The following example follows that recommendation by setting an initial node count and minimum of two nodes:

```
az aks create \
    --resource-group myResourceGroup \
    --name myAKSCluster \
    --node-count 2 \
    --enable-cluster-autoscaler \
    --min-count 2 \
    --max-count 3 \
    --generate-ssh-keys

```

Note

It takes a few minutes to create the cluster and configure the cluster autoscaler settings.

#### Enable the cluster autoscaler on an existing cluster

For a cluster with a single node pool, update the cluster with the `az aks update` command and enable the cluster autoscaler on the default node pool by using `--enable-cluster-autoscaler` and specifying `--min-count` and `--max-count`. For multi\-node\-pool clusters, use `az aks nodepool update --update-cluster-autoscaler --min-count --max-count` against each target node pool instead. The following example updates a single\-node\-pool AKS cluster to enable the cluster autoscaler on the default node pool with a minimum of two and maximum of three nodes:

```
az aks update \
    --resource-group myResourceGroup \
    --name myAKSCluster \
    --enable-cluster-autoscaler \
    --min-count 2 \
    --max-count 3

```

Note

It takes a few minutes to update the cluster and configure the cluster autoscaler settings.

#### Update the cluster autoscaler settings

After enabling the cluster autoscaler on a single\-node\-pool cluster, you can change the node `--min-count` and `--max-count` values at any time by using the `az aks update` command with the `--update-cluster-autoscaler` parameter. For multi\-node\-pool clusters, use `az aks nodepool update --update-cluster-autoscaler --min-count --max-count` against the target node pool. The following example updates a single\-node\-pool cluster so that the autoscaler keeps a minimum of two and a maximum of five nodes:

```
az aks update \
    --resource-group myResourceGroup \
    --name myAKSCluster \
    --update-cluster-autoscaler \
    --min-count 2 \
    --max-count 5

```

Note

The cluster autoscaler enforces the minimum count if the actual node count drops below the minimum because of external factors, such as a spot eviction.

Tip

In clusters with multiple node pools, enable or update the cluster autoscaler on each target node pool by using `az aks nodepool update` with `--update-cluster-autoscaler`, `--min-count`, and `--max-count`. Each autoscaled node pool has its own minimum and maximum bounds. For more information, see [Scale node pools in AKS](/en-us/azure/aks/scale-node-pools).

#### Disable the cluster autoscaler on a cluster

For a single\-node\-pool cluster, disable the cluster autoscaler using the `az aks update` command and the `--disable-cluster-autoscaler` parameter. For multi\-node\-pool clusters, use `az aks nodepool update --disable-cluster-autoscaler` against the target node pool.

```
az aks update \
    --resource-group myResourceGroup \
    --name myAKSCluster \
    --disable-cluster-autoscaler

```

Note

Nodes aren't removed when the cluster autoscaler is disabled.

After you disable the cluster autoscaler, you can manually set fixed counts for either the workload or the node pool. To set a fixed replica count for a workload, use `kubectl scale deployment <deployment-name> --replicas <replica-count>`. To set a fixed node count for a single\-node\-pool cluster, use `az aks scale --resource-group myResourceGroup --name myAKSCluster --node-count <count>`. For a specific node pool or for a multi\-node\-pool cluster, use `az aks nodepool scale --resource-group myResourceGroup --cluster-name myAKSCluster --name <nodepool-name> --node-count <count>`. If the horizontal pod autoscaler is still configured, it continues to adjust pod replicas, but additional replicas might remain pending if the node pool doesn't have enough capacity.

#### Beyond the cluster autoscaler: node auto\-provisioning

The cluster autoscaler scales an existing node pool of a fixed VM SKU between a minimum and maximum count. For workloads where the right VM SKU is hard to predict, AKS also offers [node auto\-provisioning (NAP)](/en-us/azure/aks/node-auto-provisioning), which uses the open\-source Karpenter project to dynamically choose the optimal VM SKU and provision nodes based on pending pod resource requirements. NAP is an alternative node\-scaling approach; choose either NAP or the cluster autoscaler for a cluster because NAP can't be enabled on clusters that already have the cluster autoscaler enabled.

For more information about cluster autoscaler commands and settings, see [Use the cluster autoscaler in AKS](/en-us/azure/aks/cluster-autoscaler).

Tip

If you created a resource group only to try this procedure, delete it with `az group delete --name myResourceGroup --yes --no-wait` to avoid unintended cost.

---

## Module assessment

Choose the best response for each question. The questions check whether you can choose the appropriate AKS scaling option for workload replicas, node pool capacity, and short\-lived burst demand.

### Check your knowledge

---

## Summary

In this module, you learned how to:

* Manually scale workload replicas or AKS node pools
* Use the horizontal pod autoscaler (HPA) to scale pod replicas based on metrics such as CPU utilization
* Use the cluster autoscaler to adjust node pool size when pods, including replicas created by HPA, can't be scheduled within existing capacity
* Integrate with Azure Container Instances (ACI) through virtual nodes for burst capacity

You also saw where Kubernetes Event\-driven Autoscaling (KEDA) and node auto\-provisioning (NAP) fit as related options.

### Learn more

To go deeper on the topics covered in this module, see the following Microsoft Learn articles:

* [Scaling options for applications in AKS](/en-us/azure/aks/concepts-scale)
* [Manually scale the node count in an AKS cluster](/en-us/azure/aks/scale-cluster)
* [Scale node pools in AKS](/en-us/azure/aks/scale-node-pools)
* [Autoscale pods in AKS with the horizontal pod autoscaler](/en-us/azure/aks/tutorial-kubernetes-scale#autoscale-pods)
* [Cluster autoscaling in AKS overview](/en-us/azure/aks/cluster-autoscaler-overview)
* [Use the cluster autoscaler in AKS](/en-us/azure/aks/cluster-autoscaler)
* [Virtual nodes on Azure Container Instances](/en-us/azure/container-instances/container-instances-virtual-nodes)
* [Create and configure an AKS cluster to use virtual nodes](/en-us/azure/aks/virtual-nodes)
* [Kubernetes Event\-driven Autoscaling (KEDA) overview](/en-us/azure/aks/keda-about)
* [Node auto\-provisioning (NAP) overview](/en-us/azure/aks/node-auto-provisioning)

If you don't have an Azure subscription yet, you can create one with the following options:

* [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_devrel) \| [Azure free account FAQ](https://azure.microsoft.com/pricing/purchase-options/azure-account#FAQ?cid=msft_learn)
* [Free account for Students](https://azure.microsoft.com/free/students/?cid=msft_devrel) \| [Azure for students FAQ](/en-us/azure/education-hub/azure-dev-tools-teaching/program-faq#azure-for-students/?azure-portal=true)
* [Create an Azure account](/en-us/training/modules/create-an-azure-account/?azure-portal=true) module on Learn.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-scaling-azure-kubernetes-service/_

## Fuentes
- [Configure scaling in Azure Kubernetes Service](https://learn.microsoft.com/en-us/training/modules/configure-scaling-azure-kubernetes-service/?WT.mc_id=api_CatalogApi)
