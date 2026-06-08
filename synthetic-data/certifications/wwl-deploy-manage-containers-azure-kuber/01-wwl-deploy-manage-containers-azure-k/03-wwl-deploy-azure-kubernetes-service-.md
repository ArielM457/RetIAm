# Deploy an Azure Kubernetes Service cluster

> Curso: Deploy containers by using Azure Kubernetes Service (AKS) (wwl-deploy-manage-containers-azure-kubernetes-serv) · Seccion: Deploy containers by using Azure Kubernetes Service (AKS)
> Duracion estimada: 70 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

This module covers the deployment of a managed Kubernetes cluster in Azure using Azure Kubernetes Service (AKS).

### Scenario

Imagine you work for a company that needs to deploy and manage a Kubernetes cluster. You have heard about Azure Kubernetes Service and want to learn how to use it to simplify the process. In this module, you learn how to create an Azure Kubernetes Service cluster, configure its components, and connect to it using kubectl commands. You learn how to use advanced networking, plan virtual network topology and IP addressing, configure Microsoft Entra ID integration, and review scaling considerations. This module provides a recommended baseline infrastructure architecture to deploy an Azure Kubernetes Service cluster on Azure.

### Learning objectives

After completing this module, you'll be able to:

* Create an Azure Kubernetes Service cluster.
* Configure Azure Kubernetes Service components.
* Connect to an Azure Kubernetes Service cluster.
* Configure Microsoft Entra ID integration.
* Plan virtual network topology and IP addressing for an AKS cluster.
* Review node and pod scaling options for an AKS cluster.

---

## Azure Kubernetes Service cluster architecture

This module provides a recommended baseline infrastructure architecture to deploy an Azure Kubernetes Service (AKS) cluster on Azure. The design principles are based on our [architectural best practices](/en-us/azure/well-architected/service-guides/azure-kubernetes-service) from the [Azure Well\-Architected Framework](/en-us/azure/well-architected/) to guide interdisciplinary teams across networking, security, and identity disciplines.

AKS separates the Microsoft\-managed control plane from the customer\-managed nodes (the node plane). Azure operates and abstracts Kubernetes control plane components, such as the API server (kube\-apiserver), etcd, scheduler (kube\-scheduler), controller manager (kube\-controller\-manager), and cloud controller manager (cloud\-controller\-manager). Your nodes are organized into node pools in your subscription. AKS supports node pools backed by Virtual Machine Scale Sets and the newer Virtual Machines node pool type. With the Virtual Machines node pool type, AKS directly manages provisioning and bootstrapping of each node. Each node runs the kubelet and a container runtime, which is containerd on supported AKS node pools. In non\-Cilium dataplanes, nodes also run kube\-proxy. When Azure CNI Powered by Cilium is the network dataplane, AKS doesn't run kube\-proxy; Cilium's eBPF dataplane handles service routing instead. Networking is provided by a configurable Azure Container Networking Interface (CNI) plugin. Azure CNI Overlay is the recommended option for most clusters; other Azure CNI variants are also supported. For more information, see [Core Kubernetes concepts for AKS](/en-us/azure/aks/core-aks-concepts).

In the baseline architecture, node pools are separated by role:

* **System node pools** are intended to host critical AKS system pods, such as CoreDNS and metrics\-server. AKS prefers scheduling these pods on nodes labeled as system; use the `CriticalAddonsOnly=true:NoSchedule` taint to keep application pods off system pools. These and other cluster resources, including `konnectivity-agent`, run in the `kube-system` namespace.
* **User node pools** host application workload pods. Ingress controllers can run on a general\-purpose user node pool or, in larger clusters, on a dedicated ingress node pool.

This architecture is focused on the AKS cluster itself, and not workload\-specific. The information in this module is the minimum recommended baseline for most AKS clusters. It integrates with Azure services that deliver observability, provide a network topology that supports multi\-regional growth, and secure in\-cluster traffic. For more information, see [Use system node pools in AKS](/en-us/azure/aks/use-system-pools) and the [AKS baseline architecture](/en-us/azure/architecture/reference-architectures/containers/aks/baseline-aks).

The target architecture is based on business requirements, and as a result it can vary between different application contexts. It should be considered as your starting point for preproduction and production stages.

---

## Network topology

One recommended architecture for an Azure Kubernetes Service (AKS) cluster is the hub\-spoke network topology. The hub and spoke(s) are deployed in separate virtual networks connected through peering. Some advantages of this topology are:

* Segregated management. Enables a way to apply governance and adhere to the principle of least privilege. It also supports the concept of an [Azure landing zone](/en-us/azure/cloud-adoption-framework/ready/landing-zone/) with separation of duties.
* Minimizes direct exposure of Azure resources to the public internet.
* Organizations often operate with regional hub\-spoke topologies. Hub\-spoke network topologies can be expanded in the future and provide workload isolation.
* Internet\-facing or high\-risk web applications should use a web application firewall (WAF) service to help govern HTTP traffic flow.
* A natural choice for workloads that span multiple subscriptions.
* It makes the architecture extensible. To accommodate new features or workloads, new spokes can be added instead of redesigning the network topology.
* Certain resources, such as a firewall and DNS can be shared across networks.

### Hub

The hub centralizes connectivity and observability. It contains an Azure Firewall with global firewall policies defined by your central IT teams to enforce organization\-wide firewall policy, and Azure Bastion. The hub also serves as the focal point for network observability, with diagnostics and metrics flowing to Azure Monitor and topology and connectivity data collected by Network Watcher.

Within the network, three subnets are deployed.

#### Subnet to host Azure Firewall

Azure Firewall is firewall as a service. The firewall instance secures outbound network traffic. Without this layer of security, this traffic might communicate with a malicious third\-party service that could exfiltrate sensitive company data. [Azure Firewall Manager](/en-us/azure/firewall-manager/overview) enables you to centrally deploy and configure multiple Azure Firewall instances and manage Azure Firewall policies for this *hub virtual network* architecture type. Azure Firewall requires this subnet to be named exactly AzureFirewallSubnet with a minimum size of /26\. The Azure Firewall Basic SKU **always** requires an `AzureFirewallManagementSubnet` (minimum size /26\) for the **Firewall Management network interface**. For the Standard and Premium SKUs, you must also create this subnet when you enable forced tunneling or other features that require the management network interface. The Management network interface (the feature that previously required this subnet was called Forced Tunneling) has been decoupled from forced tunneling and is now required by additional Azure Firewall features. For more information, see [Azure Firewall Management network interface](/en-us/azure/firewall/management-nic).

#### Subnet to host a gateway

This subnet is a placeholder for a VPN or ExpressRoute gateway. The gateway provides connectivity between the routers in your on\-premises network and the virtual network. Azure requires this subnet to be named exactly GatewaySubnet. For VPN gateways, the minimum supported size is /29 for the Basic SKU, and /27 for all other SKUs (with /27 or larger recommended). Note that since October 1, 2023, new policy\-based VPN gateways can only be configured by using PowerShell or the Azure CLI. Separately, the Basic VPN gateway SKU is no longer available in the Azure portal and must be configured by using PowerShell or the Azure CLI; the Basic gateway SKU is not retiring. For ExpressRoute gateways, /27 or larger is recommended; if you plan to connect 16 ExpressRoute circuits to the gateway, you must use /26 or larger.

#### Subnet to host Azure Bastion

This subnet is a placeholder for Azure Bastion. You can use Bastion to securely access Azure resources without exposing the resources to the internet. This subnet is used for management and operations only. For Azure Bastion deployments other than the Developer offering, Azure Bastion requires a dedicated subnet named exactly `AzureBastionSubnet` with a minimum size of `/26`.

### Spoke

The spoke virtual network contains the AKS cluster and other related resources. The spoke has five subnets:

* `snet-clusternodes` for AKS node IPs.
* `snet-clusteringressservices` for internal load balancers that support ingress services.
* `snet-applicationgateway` for Azure Application Gateway.
* `snet-privatelinkendpoints` for Private Link endpoints to Azure Container Registry, Azure Key Vault, and similar services.
* `snet-apiserver`, a minimum `/28` subnet delegated to `Microsoft.ContainerService/managedClusters` for [AKS API Server VNet Integration](/en-us/azure/aks/api-server-vnet-integration).

#### Subnet to host Azure Application Gateway

Azure [Application Gateway](/en-us/azure/application-gateway/overview) is a web traffic load balancer operating at Layer 7\. The reference implementation uses the `WAF_v2` SKU with a [Web Application Firewall (WAF) policy](/en-us/azure/web-application-firewall/ag/policy-overview) associated at the gateway, listener, or path level. The WAF policy helps protect incoming traffic from common web attacks and can also mitigate bot traffic when bot\-related managed rule sets are enabled. The instance has a public frontend IP configuration that receives user requests. By design, Application Gateway requires a dedicated subnet.

Note

The legacy inline WAF *configuration* on the Application Gateway `WAF_v2` SKU is deprecated. New WAF *configuration* deployments were discontinued on March 15, 2025, and existing inline WAF configurations are fully retired on March 15, 2027\. The `WAF_v2` SKU itself is **not** deprecated. New and existing deployments should use `WAF_v2` together with a separate **WAF Policy** resource (associated at the gateway, listener, or path level) instead of the inline WAF configuration. The `Standard_v2` SKU has no WAF support at all (neither inline WAF configuration nor WAF Policy resources). For migration guidance, see [Upgrade Web Application Firewall policies](/en-us/azure/web-application-firewall/ag/upgrade-ag-waf-policy).

#### Subnet to host the ingress resources

To route and distribute traffic, an ingress controller fulfills the Kubernetes ingress resources. The Azure internal load balancers exist in `snet-clusteringressservices`.

#### Subnet to host the cluster nodes

In this baseline architecture, deploy a dedicated **system node pool** for critical system pods and one or more **user node pools** for workloads and ingress components. System pools should be dedicated. For production, run at least 2 (preferably 3\) nodes and apply the taint `CriticalAddonsOnly=true:NoSchedule` to prevent application pods from scheduling there. For more information, see [Use system node pools in AKS](/en-us/azure/aks/use-system-pools).

#### Subnet to host Private Link endpoints

Azure Private Link connections are created for the Azure Container Registry and Azure Key Vault, so these services can be accessed using private endpoints within the spoke virtual network. Private endpoints don't require a dedicated subnet and can also be placed in the hub virtual network. In the baseline implementation, they're deployed to a dedicated subnet within the spoke virtual network. This approach reduces traffic passing the peered network connection and keeps the resources that belong to the cluster in the same virtual network.

#### Subnet for AKS API Server VNet Integration

AKS uses `snet-apiserver` for API Server VNet Integration. The subnet must be at least `/28` and delegated to `Microsoft.ContainerService/managedClusters`. A `/28` is a tight minimum (16 IPs, of which AKS reserves at least 9\), so consider `/27` or larger for production clusters to allow for API server scaling.

---

## Plan the IP addresses

The address space of the spoke virtual network should be large enough to hold all subnets and the IP allocations those subnets support. Plan the address space around the Azure Container Networking Interface (CNI) mode that you choose for the Azure Kubernetes Service (AKS) cluster.

### Choose a network model

AKS supports several network plugins and data plane options. Choose the model before you size the spoke virtual network because the choice determines whether pod IP addresses come from virtual network subnets or from a separate overlay address space. For more information, see [Network concepts for applications in AKS](/en-us/azure/aks/concepts-network-cni-overview) and [Azure CNI Overlay networking in AKS](/en-us/azure/aks/concepts-network-azure-cni-overlay).

* **Azure CNI Overlay** is the recommended baseline for most AKS clusters. Pods receive IP addresses from a separate private pod CIDR; AKS uses `10.244.0.0/16` by default if you don't specify `--pod-cidr`, but you can choose any private RFC 1918 or RFC 6598 range that doesn't overlap your spoke virtual network, peered virtual networks, on\-premises networks, or the Kubernetes service CIDR. This overlay address space doesn't consume IP addresses from the spoke virtual network subnets, so pod scale doesn't drive subnet sizing.
* **Azure CNI Pod Subnet** is appropriate when pods must be directly routable from the virtual network (for example, when services outside the cluster need direct pod connectivity). Pod Subnet supports two allocation modes: [Dynamic IP Allocation](/en-us/azure/aks/configure-azure-cni-dynamic-ip-allocation) for efficient per\-pod IP use, and [Static Block Allocation](/en-us/azure/aks/configure-azure-cni-static-block-allocation) for large\-scale clusters that need predictable per\-node CIDR blocks.
* **Azure CNI Node Subnet** is the legacy flat Azure CNI model. In general, use it only if you need AKS to manage the virtual network for your cluster.
* **Kubenet** is a legacy plugin that [retires on March 31, 2028](https://azure.microsoft.com/updates?id=485172). Don't use kubenet for new clusters.
* **Azure CNI Powered by Cilium** is the preferred data plane and network policy option where it's supported. Cilium is currently supported on Linux node pools only. For Windows node pools, use Calico for network policy. Azure Network Policy Manager (NPM) is a legacy option: NPM support ends on Windows nodes on September 30, 2026, and on Linux nodes on September 30, 2028\. Until Linux NPM retires, scaling beyond 250 nodes and 20,000 pods isn't supported and can result in out\-of\-memory errors. Don't use NPM for new clusters on either OS.

### Node subnet sizing for Azure CNI Overlay

With Azure CNI Overlay, plan the node subnets for node IP addresses, not pod IP addresses. Each node in a system or user node pool consumes an IP address from its node subnet. When you size the subnets, account for:

* The current node count for each node pool.
* Anticipated scale\-out for system and user node pools.
* Upgrade headroom. AKS adds temporary surge nodes during upgrades. The default `maxSurge` value is 1 (one extra node). For production node pools, 33% is recommended. With Azure CNI Overlay, each surge node consumes one extra **node\-subnet** IP address per node pool during an upgrade (pod IPs come from the overlay CIDR). With Azure CNI Node Subnet (flat networking), each surge node also consumes `maxPods` extra subnet IP addresses for its pods, which is why the flat\-networking sizing formula later in this unit multiplies `(nodes + maxSurge)` by `maxPods`.
* Internal load balancers, Application Gateway instances, and API Server VNet Integration (which projects API server pods and an internal load balancer into the delegated `snet-apiserver` subnet) that consume IP addresses from their respective subnets.

### Pod CIDR sizing for Azure CNI Overlay

With Azure CNI Overlay, pods get IP addresses from a private overlay pod CIDR. This CIDR must not overlap the spoke virtual network, peered virtual networks, on\-premises networks (including ExpressRoute and VPN ranges), or the Kubernetes service CIDR.

By default, the overlay assigns a `/24` pod block to each node. Size the overlay pod CIDR by the maximum simultaneous number of nodes in the cluster, including surge nodes during upgrades, not by the maximum number of pods. A `/16` pod CIDR contains 256 `/24` blocks, so it supports up to 256 simultaneously running nodes; for example, 255 steady\-state nodes with `maxSurge=1` fits in a `/16`, but 256 steady\-state nodes with `maxSurge=1` requires a larger pod CIDR. Use a larger pod CIDR for high\-scale clusters.

### Legacy flat Azure CNI sizing formula

If you use a directly routable Azure CNI mode instead of Azure CNI Overlay, include pod IP addresses in the virtual network address plan because each pod consumes a virtual network IP address. For Azure CNI Node Subnet, size the node subnet with this formula:

`(nodes + maxSurge) + ((nodes + maxSurge) * maxPods)`

For Azure CNI Pod Subnet, sizing depends on the allocation mode. With **Dynamic IP Allocation**, IP addresses are allocated to nodes in batches of 16, with another batch requested when fewer than 8 IPs remain unallocated on a node. As a starting baseline, size the pod subnet using `(maxNodes + maxSurge) × 16`, plus headroom for system pods, and size up further if you anticipate sustained high pod density — see [Configure Azure CNI networking with Dynamic IP Allocation](/en-us/azure/aks/configure-azure-cni-dynamic-ip-allocation). With **Static Block Allocation**, each node is assigned one or more `/28` blocks (16 IPs each); one IP per node is reserved for internal use, so the documented optimal `maxPods` setting is `maxPods = (16 × N) − 1` (for example, 31 for `N=2`, 47 for `N=3`), where `N` is the number of `/28` blocks per node. From the published examples, `N` is effectively `⌈(maxPods + 1) / 16⌉` and the pod subnet must hold `(maxNodes + maxSurge) × N × 16` addresses; treat these as derived guidance and confirm your sizing against the official examples in [Configure Azure CNI networking with Static Block Allocation](/en-us/azure/aks/configure-azure-cni-static-block-allocation) (max pod subnet size is `/12`). In both modes, still reserve node\-subnet IP addresses for `(nodes + maxSurge)`.

### Scalability

AKS supports up to 5,000 nodes per cluster (with VMSS\-backed node pools and the Standard SKU Load Balancer), 1,000 nodes per virtual machine scale set node pool, and 100 node pools per cluster. For current limits, see [AKS quotas, virtual machine size restrictions, and region availability](/en-us/azure/aks/quotas-skus-regions).

For Azure CNI Overlay, the practical scale limit for pod addressing is the overlay pod CIDR size. Each node consumes one `/24` pod block by default, so make sure the pod CIDR has enough `/24` blocks for the maximum simultaneous node count, including upgrade surge headroom, that you plan to support.

### Upgrade

AKS surges new nodes during cluster and node\-pool upgrades. The number of surge nodes is controlled by `--max-surge`. The default `maxSurge` value is 1 (one extra node). For production node pools, 33% is recommended.

For Azure CNI Overlay, surge nodes consume IP addresses from the node subnet. They don't consume pod\-subnet IP addresses because Overlay doesn't use a pod subnet for pods.

For pods, you might need extra addresses depending on your workload's deployment strategy:

* Rolling updates use temporary pods while the workload is updated.
* Recreate strategy removes the old pods before new pods are created, so the new pods can reuse released addresses.

### Network policy

For network policy, prefer Cilium when you use Azure CNI Powered by Cilium. For Windows node pools, use Calico. Azure Network Policy Manager (NPM) support ends on Windows nodes on September 30, 2026, and on Linux nodes on September 30, 2028\. Until Linux NPM retires, it has scale limitations beyond 250 nodes and 20,000 pods. Don't use NPM for new clusters on either OS. For more information, see [Network policies in AKS](/en-us/azure/aks/use-network-policies).

### Azure Private Link addresses

Factor in the addresses that are required for communication with other Azure services over Private Link. In this architecture, budget at least three Private Link IP addresses: two for the initial Azure Container Registry private endpoint (one for the registry endpoint and one for the home\-region regional data endpoint) and one for Azure Key Vault. Add more if you enable Azure Container Registry geo\-replication or additional regional endpoints.

This architecture is designed for a single workload. For multiple workloads, you might want to isolate the user node pools from each other and from the system node pool. That choice results in more subnets that are smaller in size. Also, the ingress resource might be more complex, and as a result you might need multiple ingress controllers that require extra IP addresses.

---

## Configure compute for nodes and node pools

### Plan node pools and VM sizes

In Azure Kubernetes Service (AKS), each node pool maps to an Azure Virtual Machine Scale Set or to the Virtual Machines node pool type. Use separate system and user node pools so cluster services and workloads can scale and upgrade independently.

#### System node pool

System node pools host critical AKS components such as CoreDNS. They must use Linux nodes, either Ubuntu or Azure Linux. The [Use system node pools in AKS](/en-us/azure/aks/use-system-pools) guidance lists system\-pool requirements, including a Linux `osType` and a VM SKU with at least 4 vCPUs and 4 GB of memory. The AKS\-wide [VM size restrictions](/en-us/azure/aks/quotas-skus-regions) page also lists a lower restricted\-size floor — VM sizes with fewer than 2 vCPUs and 4 GB of RAM might not be used — but size system pools according to the stricter system\-pools requirement. B\-series VMs aren't supported for system node pools, and Av1\-series VMs aren't recommended.

For dev and lab clusters, use a current\-generation D\-series SKU such as `Standard_D4ds_v5`. For production, choose a larger current\-generation D\-series SKU based on enabled system add\-ons, CoreDNS replica count, and your zone strategy. Confirm the SKU is AKS\-supported in the region and that quota is available.

Dedicate the system pool to critical system pods with the taint `CriticalAddonsOnly=true:NoSchedule`. The `kubernetes.azure.com/mode: system` label only prefers system pods on system pools; it doesn't isolate application workloads.

#### User node pools

User node pools run application workloads. Choose current\-generation v5 or later VM families that match CPU, memory, storage, and GPU requirements. Also consider regional quota and AKS\-supported SKUs. If you leave the VM SKU parameter blank, AKS dynamically selects an appropriate SKU based on available regional capacity and subscription quota. This capability, called Smart VM Defaults, became generally available in May 2025; before that, the default SKU was Standard\_DS2\_v2\. For general\-purpose workloads, start with current\-generation D\-series sizes and use specialized families only when required. Deploy at least two nodes for high availability and use autoscaling for demand changes.

### Choose the OS disk type

AKS prefers Ephemeral OS disks when the selected VM SKU supports them and the configured OS disk size fits within supported local storage, such as NVMe, temporary/resource disk, or cache, depending on the VM SKU. When `--node-osdisk-type` isn't specified and the requested or default OS disk size doesn't fit within supported local storage for that SKU, AKS uses a managed OS disk instead. If you explicitly request `--node-osdisk-type Ephemeral` and the disk doesn't fit, node\-pool creation fails validation; lower `--node-osdisk-size` or pick a SKU with enough supported local storage. For more information, see [Ephemeral OS disks for AKS nodes](/en-us/azure/aks/concepts-storage#ephemeral-os-disk). With an ephemeral OS disk, the OS disk lives on the VM cache or temporary storage, has no extra managed disk IOPS cost, and can make node creation, reimage, and upgrade operations faster. Use `--node-osdisk-type Ephemeral` in Azure CLI, or accept the portal default when it selects an ephemeral OS disk.

Since March 2025, when `--node-osdisk-size` isn't specified, AKS sizes the ephemeral OS disk to the VM's full supported local storage by default — provided that local storage is at least 128 GiB. VMs with less supported local storage fall back to a managed OS disk. For example, `Standard_D8ds_v5` (300 GiB temp storage) gets a 300 GiB ephemeral OS disk by default. Set `--node-osdisk-size` at node\-pool creation if you want to leave local storage available for workloads.

When ephemeral OS disks aren't supported for the selected VM size, AKS uses a managed OS disk. The default managed OS disk size is tiered by host vCPU count: 128 GB (P10\) for 1\-7 vCPUs, 256 GB (P15\) for 8\-15 vCPUs, 512 GB (P20\) for 16\-63 vCPUs, and 1024 GB (P30\) for 64\+ vCPUs.

### Plan node capacity

#### AKS reservations and allocatable resources

Don't use a fixed workload\-to\-platform percentage for capacity planning. AKS reserves CPU and memory on each node for system pods, the kubelet, and node reliability. CPU reservation varies by host vCPU count. On AKS 1\.29 and later, memory reservation uses a formula based on the node's `maxPods` value and total memory, plus a 100 Mi eviction threshold. Windows nodes also reserve an extra 2 GB of memory outside the calculated memory reservation. AKS versions earlier than 1\.29 use a regressive percentage\-based memory reservation formula with a 750 Mi eviction threshold and don't include `maxPods` as an input. For details, see [Resource reservations in AKS](/en-us/azure/aks/node-resource-reservations).

Use the allocatable CPU and memory shown by `kubectl describe node` as the capacity available to pods. Set workload resource requests and limits from allocatable capacity, and leave headroom for daemon sets, monitoring, logging, and workload bursts.

#### Maximum pods per node

Set `maxPods` based on network model, node size, IP address plan, and workload density. Current defaults vary by network model:

| Network model | Default max\-pods | Maximum |
| --- | --- | --- |
| Azure CNI Overlay | 250 | 250 |
| Azure CNI Pod Subnet (Dynamic IP Allocation) | 250 | 250 |
| Azure CNI Pod Subnet (Static Block Allocation) | Set explicitly; ideal values follow `(16 × N) − 1` | 250 |
| Azure CNI Node Subnet (legacy) | 30 | 250 |
| Kubenet (legacy, retires on March 31, 2028\) | 110 (CLI) / 30 (portal) | 250 |

Note

Defaults vary by tool and network model (for example, Kubenet defaults to 110 in the Azure CLI but 30 in the Azure portal). Always set `--max-pods` explicitly at cluster or node\-pool creation to avoid surprises, and verify with `az aks show --query agentPoolProfiles[].maxPods`.

Set `maxPods` at cluster or node\-pool creation. To change it later, create a new node pool with the desired value and migrate workloads.

### Use Availability Zones for production

For production node pools, use Availability Zones in supported regions. Choose the zone strategy when you create the node pool because zone selection is immutable after node\-pool creation.

Use `--zones 1 2 3` to create a zone\-spanning node pool. Alternatively, create one node pool per zone for a zone\-aligned strategy. If you use the cluster autoscaler with zone\-aligned pools, enable the `balance-similar-node-groups` cluster autoscaler profile setting (`--cluster-autoscaler-profile balance-similar-node-groups=true`) so similar pools scale evenly across zones.

### Choose the node OS

System pools must use Linux nodes: Ubuntu or Azure Linux. User pools can use Ubuntu, Azure Linux, or Windows. Keep node images current by applying AKS node image upgrades as part of normal patching.

---

## Integrate Microsoft Entra ID for the cluster

Securing access to and from an Azure Kubernetes Service (AKS) cluster is critical. AKS identity decisions fall into two areas:

* **Inside\-out access**. AKS and workloads access Azure resources such as networking infrastructure, Azure Container Registry, and Azure Key Vault. Authorize only the resources they need.
* **Outside\-in access**. Users, groups, and automation need access to the Kubernetes API server and Azure Resource Manager. Authorize only the identities that need cluster credentials or Kubernetes API permissions.

### Cluster\-to\-Azure managed identities (control plane and kubelet)

The control\-plane identity is how AKS manages Azure resources for the cluster. AKS uses a system\-assigned managed identity by default when you create a cluster, and managed identity is recommended for the control\-plane identity. You don't need to create or rotate a service principal secret.

Managed identities are the default and recommended identity model for AKS clusters. Service principals are still supported, but new clusters should use a managed identity. If you have an existing service\-principal\-based cluster, you can migrate it to a system\-assigned managed identity later by running:

```
az aks update --resource-group <rg> --name <cluster> --enable-managed-identity

```

After running this command, the cluster's control\-plane identity is migrated to a system\-assigned managed identity. Two follow\-up steps may be required to complete the migration to a fully managed\-identity\-based cluster: if your cluster previously used the AKS\-to\-ACR integration to pull from Azure Container Registry, you must re\-grant ACR pull permissions to the new kubelet managed identity (see the IMPORTANT note below); and you must upgrade node\-pool images so the kubelet on each node stops using the service principal and starts using the managed identity.

Important

If your cluster previously used the AKS\-to\-ACR integration to pull from Azure Container Registry, the new kubelet managed identity doesn't inherit registry pull permissions. After migration, re\-grant access:

* For non\-ABAC ACR registries, re\-run `az aks update --resource-group <rg> --name <cluster> --attach-acr <acr-resource-id>` so the new kubelet identity is granted `AcrPull` on the registry. Run this command as an identity that has permission to create role assignments on the registry; otherwise, assign the `AcrPull` role to the kubelet managed identity manually.
* For ABAC\-enabled ACR registries (RBAC Registry \+ ABAC Repository Permissions), the AKS\-to\-ACR integration command isn't supported. Manually assign the `Container Registry Repository Reader` role to the kubelet managed identity at the appropriate registry or repository scope. For more information about ABAC permissions modes on Azure Container Registry, see [Azure Container Registry role\-based access control](/en-us/azure/container-registry/container-registry-rbac-abac-repository-permissions).

Otherwise, image pulls fail with `ImagePullBackOff` or `ErrImagePull`; inspect `kubectl describe pod` Events and use `az aks check-acr` to diagnose. For more information, see [Authenticate with Azure Container Registry from AKS](/en-us/azure/aks/cluster-container-registry-integration).

After running the migration command, kubelet on existing nodes continues using the service principal until you upgrade the node pool images. The node\-pool upgrade cordons, drains, and reimages nodes, so plan the upgrade during a maintenance window and protect workloads with multiple replicas and PodDisruptionBudgets:

```
az aks nodepool upgrade --resource-group <rg> --cluster-name <cluster> --name <nodepool> --node-image-only

```

The node\-image upgrade only takes effect when a newer node\-image VHD is available in the cluster's region. If the node pool is already on the latest image, the command has no effect and kubelet continues to use the service principal until the next image release reaches the region. Per [AKS node images](/en-us/azure/aks/node-images#node-image-releases), Linux node images typically release weekly, Windows node images monthly, and regional rollout can take up to two weeks. (Note: another AKS doc page lists "up to a week" for regional rollout — the slower two\-week figure is the safer planning assumption.) For more information, see [AKS managed\-identity update considerations](/en-us/azure/aks/system-assigned-managed-identity#update-cluster-considerations) and [AKS node images](/en-us/azure/aks/node-images#node-image-releases).

AKS uses two primary managed identities:

* **Control\-plane identity**. The AKS control plane uses this identity to manage resources such as ingress load balancers, managed public IP addresses, cluster autoscaler resources, and storage integrations.
* **Kubelet identity**. The kubelet uses this identity to authenticate to Azure Container Registry and other Azure resources needed by nodes. Some AKS add\-ons also use managed identities.

When a cluster pulls images from Azure Container Registry, avoid storing registry credentials in Kubernetes `Secret` objects and referencing them with `imagePullSecrets`. Instead, assign the registry pull role to the kubelet managed identity at the smallest practical scope: `AcrPull` for non\-ABAC registries, or `Container Registry Repository Reader` for ABAC\-enabled registries.

Assign Azure role\-based access control (Azure RBAC) permissions to managed identities at the smallest practical scope. Common assignments include [`Network Contributor`](/en-us/azure/role-based-access-control/built-in-roles/networking#network-contributor), [`Monitoring Metrics Publisher`](/en-us/azure/role-based-access-control/built-in-roles/monitor#monitoring-metrics-publisher), and [`AcrPull`](/en-us/azure/role-based-access-control/built-in-roles/containers#acrpull) for network resources, Azure Monitor metrics, and Azure Container Registry image pulls.

### Workload identity (pods to Azure services)

For applications in pods that need Azure service access, use Microsoft Entra Workload ID. It is generally available and uses federated OpenID Connect (OIDC) so Kubernetes service accounts can exchange projected service account tokens for Microsoft Entra ID tokens.

Use Microsoft Entra Workload ID with Azure Identity client libraries or Microsoft Authentication Library (MSAL) to avoid storing service principal secrets in Kubernetes and to align workload access with Microsoft Entra ID governance.

The older pod\-managed identity model, implemented by the open\-source `aad-pod-identity` project, was deprecated on October 24, 2022, and the project was archived in September 2023\. The AKS\-managed pod identity add\-on was supported through September 2025 and has since retired. Don't use pod\-managed identity for new workloads, and migrate existing workloads to Microsoft Entra Workload ID.

### Microsoft Entra ID integration with the AKS API server

Microsoft Entra ID integration covers outside\-in access to the Kubernetes API server.

#### Authentication (who you are)

Use AKS\-managed Microsoft Entra ID integration for cluster authentication. Legacy Microsoft Entra integration has retired; migrate any remaining legacy clusters by running `az aks update --resource-group <rg> --name <cluster> --enable-aad --aad-admin-group-object-ids <entra-group-object-id>`, and then refresh kubeconfig.

A user runs `az aks get-credentials` to download or merge kubeconfig. On clusters running Kubernetes 1\.24 or later, the `kubelogin` exec\-plugin format is configured in the kubeconfig automatically, so no manual conversion is required for interactive Azure CLI sign\-in. (The `kubelogin` binary itself must still be installed on the client; recent Azure CLI versions typically install or update it for you.) Explicit `kubelogin convert-kubeconfig` is needed for non\-interactive scenarios such as CI pipelines, or for sign\-in methods other than interactive Azure CLI, including service principal, managed identity, workload identity, and device code authentication. Device\-code authentication doesn't work when Microsoft Entra Conditional Access policies apply; use web\-browser interactive authentication in that scenario.

#### Authorization (what you can do)

Authorization has two distinct layers.

**Azure RBAC layer (ARM)**. The `az aks get-credentials` command is an Azure Resource Manager operation against the AKS resource. Azure RBAC controls kubeconfig download. For example, `Azure Kubernetes Service Cluster User Role` allows user kubeconfig, and `Azure Kubernetes Service Cluster Admin Role` allows admin kubeconfig. For Microsoft Entra user credentials on Microsoft Entra\-integrated clusters, a Cluster User kubeconfig download alone doesn't grant Kubernetes API permissions; Kubernetes API permissions are governed by Kubernetes RBAC or Azure RBAC for Kubernetes Authorization. By contrast, `--admin` cluster\-admin credentials grant Kubernetes admin access, and on clusters that don't use Microsoft Entra ID, clusterUser credentials have admin\-equivalent access.

**Kubernetes API authorization**. After kubeconfig is obtained and the user is authenticated, the Kubernetes API server evaluates the requested Kubernetes action. AKS supports two models:

* **Kubernetes RBAC**. Kubernetes RBAC is the native model. Define permissions with `Role` and `ClusterRole`, and grant them with `RoleBinding` and `ClusterRoleBinding`. Use Kubernetes RBAC for in\-cluster service\-account permissions, GitOps, or fine\-grained permissions in Kubernetes manifests.
* **Azure RBAC for Kubernetes Authorization**. Assign Azure roles such as `Azure Kubernetes Service RBAC Reader`, `Azure Kubernetes Service RBAC Writer`, `Azure Kubernetes Service RBAC Admin`, or `Azure Kubernetes Service RBAC Cluster Admin` to Microsoft Entra ID users or groups. Use Azure RBAC for Kubernetes Authorization for centralized governance, Azure Activity Log audit, and Privileged Identity Management integration. Conditional Access is enforced separately at Microsoft Entra sign\-in to the cluster control plane and applies to either Kubernetes RBAC or Azure RBAC for Kubernetes Authorization.

#### Conditional Access

AKS clusters with Microsoft Entra ID integration can enforce Conditional Access during cluster sign\-in, including multifactor authentication, device compliance, approved locations, or other conditions before a user accesses the control plane. Conditional Access requires a Microsoft Entra ID license that supports it.

### User and group assignment

Assign cluster\-admin and user roles to Microsoft Entra ID groups instead of individual users, so membership changes don't require cluster changes.

Apply least privilege at the smallest effective scope. Grant cluster\-wide administrator roles only when needed. For namespace\-limited access, prefer namespace\-scoped Azure RBAC for Kubernetes Authorization assignments or Kubernetes `RoleBinding` resources. A `RoleBinding` can reference either a namespaced `Role` or a reusable `ClusterRole`; use `ClusterRoleBinding` only when permissions must apply across the cluster.

---

## Secure the network flow

Securing network flow into and out of an Azure Kubernetes Service (AKS) cluster involves multiple layers. Network flow can be categorized as:

* **Ingress traffic**: From the client, to the workload running in the cluster.
* **Egress traffic**: From a pod or node, in the cluster to an external service.
* **Pod\-to\-pod traffic**: Communication between pods. This traffic includes communication between the ingress controller and the workload. Also, if your workload is composed of multiple applications deployed to the cluster, communication between those applications would fall into this category.
* **Management traffic**: Traffic that goes between the client and the Kubernetes API server.

This architecture has several layers of security to secure all types of traffic.

### Ingress traffic flow

The architecture accepts only TLS\-encrypted requests from the client. The Application Gateway is configured with the `AppGwSslPolicy20220101` predefined policy (or `AppGwSslPolicy20220101S` for a stricter cipher set, or an equivalent CustomV2 policy) to enforce TLS 1\.2 as the minimum protocol version, with TLS 1\.3 also enabled. Use host\-specific multi\-site HTTPS listeners for production sites so each TLS site is matched by SNI hostname. For no\-SNI or IP\-only clients on Application Gateway v2, configure a high\-priority dummy multi\-site HTTPS listener with a self\-signed certificate and route it to a sinkhole backend. Use lower\-priority wildcard or basic listeners only as catch\-all routing after TLS listener selection. For background on multisite listeners, see [Application Gateway multiple site hosting](/en-us/azure/application-gateway/multiple-site-overview). The diagram shows the recommended production posture: end\-to\-end TLS from the client to the workload pod, with certificate material stored in Azure Key Vault.

1. The client sends an HTTPS request to `delta.contoso.com`. The name resolves through a DNS `A` record to the public IP address of Azure Application Gateway. Application Gateway presents the `delta.contoso.com` certificate from Azure Key Vault by using a user\-assigned managed identity.
2. Application Gateway terminates client TLS so its web application firewall (WAF) can inspect the request and routing rules can select the backend. It then re\-encrypts the request and sends it over TLS to the AKS internal load balancer by using the backend certificate for `*.aks-ingress.contoso.com`.
3. The internal load balancer forwards encrypted traffic to the in\-cluster ingress controller. On the Application Gateway\-to\-ingress hop, the ingress controller presents the backend TLS certificate to Application Gateway. If the ingress controller then opens a TLS connection to the workload, the workload pod presents the certificate expected by the ingress controller. Mount each certificate in the component that presents it, for example by using the Azure Key Vault provider for Secrets Store CSI Driver.
4. Certificate management path: Application Gateway retrieves listener certificates from Azure Key Vault (background certificate rotation, not per\-request traffic). Grant its user\-assigned managed identity the least privilege needed to read certificates, and manage certificate rotation in Key Vault.

Note

TLS to the workload pod is recommended for sensitive workloads. If the workload doesn't support TLS termination, you can terminate TLS at the ingress controller and forward to the workload over HTTP within the cluster's private network, but the diagram in this unit shows the recommended end\-to\-end TLS configuration.

Application Gateway Ingress Controller (AGIC) runs in the cluster, monitors Kubernetes `Ingress` and `Service` resources, endpoint/pod state, and `Secret` state, and continuously configures Application Gateway through Azure Resource Manager. Application Gateway remains the ingress data plane. An in\-cluster ingress controller, such as NGINX or Istio, is a proxy behind Application Gateway for cluster\-local routing, TLS, or mesh policy. Application Gateway for Containers is the newer, next\-generation Kubernetes load\-balancing option from the Application Gateway family, and is positioned by Microsoft as the evolution of AGIC. It implements both the Kubernetes Gateway API and the Ingress API and provides near real\-time pod and route updates. AGIC remains fully supported for existing deployments; choose Application Gateway for Containers for new workloads that benefit from Gateway API features or fine\-grained traffic management.

### Egress traffic flow

Pods and nodes initiate outbound connections to Azure services and the internet. AKS also requires outbound dependencies for cluster operation, including image pulls from Microsoft Artifact Registry (`mcr.microsoft.com`), time servers, package repositories, and monitoring endpoints. Review required FQDNs and ports before you restrict egress.

Route egress through Azure Firewall in the hub virtual network. Apply a User\-Defined Route (UDR) to the AKS cluster subnet so outbound traffic uses the firewall as the next hop. Configure Azure Firewall application rules for HTTP/HTTPS FQDN dependencies (such as `mcr.microsoft.com`, `management.azure.com`, and package repositories — the `AzureKubernetesService` FQDN tag covers most of these). Use network rules for the non\-HTTP/S protocols required by your specific cluster configuration. For older public clusters without `konnectivity-agent`, allow UDP 1194 and TCP 9000 for tunneled node\-to\-control\-plane communication. For clusters with `konnectivity-agent`, allow the API\-server FQDN `*.hcp.<location>.azmk8s.io` over HTTPS 443 instead. Private clusters and clusters that use API Server VNet Integration don't require the public tunnel port rules. UDP 123 for NTP is only required for older Linux node images that don't use the Azure host time source. With the Azure Firewall DNS proxy enabled, FQDN\-based matching also works in network rules. For the authoritative list of required egress endpoints for your cluster configuration, see [Outbound network and FQDN rules for AKS clusters](/en-us/azure/aks/outbound-rules-control-egress).

API Server VNet Integration, shown by the `snet-apiserver` subnet in the hub\-spoke network diagram in the Plan the IP addresses unit, keeps node\-to\-API\-server traffic on the customer's private network. [Network\-isolated clusters](/en-us/azure/aks/concepts-network-isolated) can run without public outbound dependencies when required artifacts and control\-plane dependencies are available privately. AKS supports two outbound types for this scenario: `none` (generally available) and `block` (in preview at the time of writing). The `block` outbound type is supported only for managed virtual network network\-isolated clusters; for bring\-your\-own VNets, including hub\-spoke topologies, use `none` with explicit egress controls such as NSGs, UDRs, and firewall rules.

### Management traffic and API server access

Management traffic includes administrator, automation, and node communication with the Kubernetes API server. Restrict the API server to trusted networks and identities.

* **API server authorized IP ranges**: For a public API server, allow only trusted source IP ranges.
* **Private cluster**: Use a private API server endpoint that is reachable only from peered or private networks, such as a hub virtual network, VPN, or Azure ExpressRoute.
* **API Server VNet Integration**: Project the API server into a delegated subnet in the customer virtual network so node\-to\-API\-server traffic stays private.

### Pod\-to\-pod traffic and network policy

Use Kubernetes `NetworkPolicy` resources to restrict pod\-to\-pod traffic by namespace and label selectors. Start with least\-privilege policies that allow only the protocols and ports each application needs.

Azure CNI Powered by Cilium is the recommended AKS option for a managed eBPF\-based data plane and policy engine. Azure Network Policy Manager (NPM) and Calico are alternatives for supported network configurations, but NPM support ends on Windows nodes on September 30, 2026, and on Linux nodes on September 30, 2028\. Validate the policy engine and data\-plane choice at cluster creation. Migrating an existing supported cluster to Azure CNI Powered by Cilium is supported in place via `az aks update --name <cluster-name> --resource-group <resource-group> --network-dataplane cilium`. The operation simultaneously reimages all node pools and isn't supported on clusters with Windows node pools or Node Auto\-Provisioning enabled. If you also need Azure CNI Overlay IPAM, after uninstalling or disabling NPM or Calico network policy if enabled, update the IPAM mode first as a separate, irreversible operation, then update the dataplane to Azure CNI Powered by Cilium. Choosing Cilium from day one avoids the migration disruption.

For service\-to\-service encryption, traffic management, and identity\-aware policy, use a service mesh with mutual TLS (mTLS). AKS recommends the Istio\-based service mesh add\-on. The [Open Service Mesh (OSM) add\-on for AKS retires on September 30, 2027](/en-us/azure/aks/open-service-mesh-about), and should not be used for new workloads.

### Private endpoints to Azure dependencies

Use Azure Private Link with private endpoints in `snet-privatelinkendpoints` to keep traffic to Azure Container Registry, Azure Key Vault, and other Azure dependencies on the private network. This pattern reduces exposure to public endpoints.

### NSG and firewall caveat

Use Network Security Groups (NSGs) for subnet boundary controls, but understand their limits. NSGs cannot enforce FQDN\-based rules; use Azure Firewall application rules for FQDN\-based egress control. Blocking traffic between AKS\-internal subnets with NSGs or firewall rules is not supported and can break the cluster.

---

## Node and pod scalability

### Scale pods and nodes in Azure Kubernetes Service (AKS)

Azure Kubernetes Service (AKS) supports scaling at two levels: **pod\-level scaling** changes the number of workload replicas, and **node\-level scaling** changes the cluster infrastructure that runs those workloads. Choose scaling mechanisms that match the workload pattern, availability requirements, and budget. For example, a steady web API might use a fixed node pool with the Horizontal Pod Autoscaler (HPA), while a bursty queue processor might use Kubernetes Event\-driven Autoscaling (KEDA) and node autoscaling.

Use pod\-level mechanisms to scale applications first. Use node\-level mechanisms when the cluster needs more or fewer nodes to host scheduled pods. For more information, see [Scaling options for applications in AKS](/en-us/azure/aks/concepts-scale).

### Manual scaling

Manual scaling is useful for testing, controlled operations, or workloads with predictable demand. For pods, set the deployment replica count. For infrastructure, set the node count on a node pool or on the cluster.

```
kubectl scale deployment <name> --replicas <n>
az aks nodepool scale --cluster-name <cluster> --resource-group <rg> --name <pool> --node-count <n>
az aks scale --resource-group <rg> --name <cluster> --nodepool-name <pool> --node-count <n>

```

Fixed node\-count scaling with `az aks scale` or `az aks nodepool scale` is disabled on node pools where cluster autoscaler is enabled. To set a specific node count, disable cluster autoscaler on that node pool first. If you want autoscaler to keep managing the node pool, adjust its `--min-count` and `--max-count` values instead.

`User` node pools can scale to `0` nodes. To force a user node pool to `0` manually, disable the cluster autoscaler on the node pool first. Autoscaler\-enabled user node pools can allow scale\-to\-zero by setting `--min-count 0`. `System` node pools can't scale to `0` because AKS needs system nodes to run critical cluster services.

Important

Don't remove AKS nodes by running `kubectl delete node`. Always use `az aks` commands to scale nodes so AKS keeps the Kubernetes node objects and the underlying virtual machine scale set in sync.

For more information, see [Manually scale the node count in an AKS cluster](/en-us/azure/aks/scale-cluster).

### Horizontal Pod Autoscaler

The HPA scales the number of pod replicas based on observed metrics. You define minimum and maximum replicas and the metric targets that indicate when the workload should scale out or scale in.

Out of the box, HPA supports **CPU and memory** resource metrics from the Kubernetes Metrics Server. Custom and external metrics require an adapter, such as Prometheus Adapter or KEDA, to expose those metrics through the Kubernetes metrics APIs.

The HPA controller sync period is `15` seconds by default. In AKS, Metrics Server scrapes the kubelet every `60` seconds, so although the controller loop runs every `15` seconds it acts on data that refreshes only every `60` seconds — meaning effective scaling decisions change at most once every `60` seconds. HPA makes replica decisions from the metrics it observes, and the Kubernetes scheduler places new pods on nodes with available capacity.

Use HPA for workloads that need more or fewer replicas as resource use changes. If no node has enough available resources for the new replicas, the pods remain pending until node capacity is available.

### Vertical Pod Autoscaler

The Vertical Pod Autoscaler (VPA) right\-sizes pod CPU and memory **requests** based on observed usage. VPA is generally available on AKS and helps improve scheduling and cluster utilization by aligning requests with real workload behavior.

VPA supports these update modes:

* `Off`: VPA provides recommendations only and doesn't apply changes.
* `Initial`: VPA applies recommendations only when pods are created.
* `Recreate`: VPA assigns updated resource requests when pods are created and evicts existing pods when their current requests differ significantly from recommendations, so they're recreated with updated values.
* `InPlaceOrRecreate` (Requires AKS 1\.34\+.): VPA tries to apply supported request changes in place, and recreates pods when in\-place updates aren't possible. Microsoft recommends `InPlaceOrRecreate` over `Recreate` when the workload tolerates it, because it takes advantage of restart\-free updates whenever possible.
* `Auto` (deprecated): An alias for `Recreate` (deprecated as of VPA 1\.4\.0 / AKS 1\.34\+). Use `Recreate` for new manifests.

Don't combine VPA and HPA on the **same** CPU or memory metrics. HPA changes replica count based on those metrics, while VPA changes the requested resources that those same metrics compare against. This conflict can cause unstable scaling behavior. VPA doesn't support AKS Windows containers.

For more information, see [Vertical pod autoscaling in AKS](/en-us/azure/aks/vertical-pod-autoscaler).

### Kubernetes Event\-driven Autoscaling

AKS provides a managed KEDA add\-on for event\-driven autoscaling. KEDA scales workloads based on event sources such as queue depth, message backlog, schedules, or external metrics. KEDA can also scale workloads to `0` replicas when no events need processing.

Use KEDA when application demand is driven by events rather than only CPU or memory usage. Examples include queue processors, stream consumers, scheduled jobs, and workloads that use external metrics.

Use Microsoft Entra Workload ID for KEDA scalers that need to authenticate to Azure resources. Workload ID is preferred over pod\-managed identity for new deployments. Don't combine a KEDA `ScaledObject` with an HPA that targets the same workload because KEDA uses HPA behavior in the background and the two controllers compete. By default, the conflict failure mode is asymmetric: if an HPA already exists for the workload, creating a KEDA `ScaledObject` for it fails; if the `ScaledObject` is created first, a subsequently created HPA isn't blocked but still produces unstable scaling behavior. KEDA exposes advanced ownership\-transfer annotations such as `scaledobject.keda.sh/transfer-hpa-ownership`, but these are not a substitute for running a single autoscaler per workload.

For more information, see [KEDA add\-on for AKS](/en-us/azure/aks/keda-about).

### Cluster autoscaler

The [cluster autoscaler](/en-us/azure/aks/cluster-autoscaler) adjusts the number of nodes in autoscaler\-enabled node pools. It watches for pods that can't be scheduled because of resource constraints and adds nodes when another node could run those pods. It also evaluates whether underutilized nodes can be removed safely.

You don't have to enable cluster autoscaler during cluster provisioning. You can enable it later on an existing cluster or node pool.

```
az aks update --resource-group <rg> --name <cluster> --enable-cluster-autoscaler --min-count <n> --max-count <m>
az aks nodepool update --resource-group <rg> --cluster-name <cluster> --name <pool> --enable-cluster-autoscaler --min-count <n> --max-count <m>

```

AKS uses one cluster\-wide autoscaler profile. You can enable cluster autoscaler on multiple node pools, but per\-node\-pool configuration is limited to values such as `min-count` and `max-count`. Autoscaler profile settings, such as `scan-interval`, apply to all autoscaler\-enabled node pools in the cluster.

#### Scale\-up behavior

The Kubernetes scheduler first tries to place a pod on existing nodes. If no node has enough resources or matching scheduling constraints, the pod is marked unschedulable. The cluster autoscaler watches for that condition and asks Azure to add capacity to a suitable node pool. After the new node is ready, the scheduler can place pending pods on it.

#### Scale\-down behavior

The cluster autoscaler removes a node only when the node has been underutilized for `scale-down-unneeded-time` and the pods on the node can be safely evicted and rescheduled elsewhere. The default `scale-down-unneeded-time` is `10` minutes.

Scale\-down can be blocked by workload or scheduling constraints. Common blockers include restrictive PodDisruptionBudgets, pods that can't run on other nodes because of affinity or topology constraints, and the `cluster-autoscaler.kubernetes.io/safe-to-evict: false` annotation. The `skip-nodes-with-local-storage` autoscaler\-profile setting (which AKS defaults to `false`) controls whether nodes that run pods with local storage are skipped. The `skip-nodes-with-system-pods` setting (which AKS defaults to `true`) prevents scale\-down of nodes running `kube-system` pods, except for DaemonSet and mirror pods.

#### Default autoscaler profile settings

| Setting | Default |
| --- | --- |
| `scan-interval` | 10 s |
| `scale-down-unneeded-time` | 10 min |
| `scale-down-utilization-threshold` | 0\.5 |
| `max-graceful-termination-sec` | 600 |
| `max-node-provision-time` | 15 min |

For more information, including the full list of profile settings, see [Use the cluster autoscaler in AKS](/en-us/azure/aks/cluster-autoscaler#cluster-autoscaler-profile-settings). For an architectural overview, see [Cluster autoscaling in AKS overview](/en-us/azure/aks/cluster-autoscaler-overview).

### PodDisruptionBudgets

Configure PodDisruptionBudgets (PDBs) for production workloads to maintain availability during voluntary disruptions such as node drains, cluster upgrades, and cluster autoscaler scale\-down. A PDB tells Kubernetes how many pods in a workload must remain available while voluntary disruption operations proceed.

Caution

Overly restrictive PDBs can block cluster autoscaler scale\-down and AKS cluster upgrades. Set PDBs to protect availability without preventing safe evictions.

### Virtual nodes

Virtual nodes let AKS schedule pods to Azure Container Instances without provisioning extra virtual machines. They're useful for burst workloads that need fast capacity while you avoid keeping extra nodes running during idle periods.

Virtual nodes have important constraints. They support Linux pods only and require Azure CNI in flat\-networking mode with a delegated virtual\-node subnet (Microsoft's documented examples use Azure CNI Node Subnet). Azure CNI Overlay isn't compatible because virtual\-node pods need direct VNet routability to Azure Container Instances. Virtual nodes don't support DaemonSets, don't support init containers, and don't support managed identity on virtual nodes, IPv6, or persistent volumes.

For more information, see [Create and configure an AKS cluster to use virtual nodes](/en-us/azure/aks/virtual-nodes).

### Node auto\-provisioning

Node auto\-provisioning (NAP) is a newer Karpenter\-based node provisioning mode for AKS. NAP watches pending pods and automatically selects optimal VM SKUs and node configurations to satisfy workload requirements.

NAP is preconfigured in AKS Automatic. You can enable it on Standard\-tier clusters (non\-Automatic) when the cluster meets the prerequisites and constraints. NAP can't coexist with cluster autoscaler on the same cluster. Other limitations include no Windows node pools, no IPv6 clusters, no service principals (managed identity is required), and no cluster stop/start once NAP is enabled. NAP is supported through stable AKS APIs and is preconfigured for AKS Automatic clusters; Microsoft's general AKS scaling concepts page may still describe it as preview, so confirm the current preview/GA status against the [Node auto\-provisioning in AKS](/en-us/azure/aks/node-auto-provisioning) documentation before adopting it for production.

For more information, see [Node auto\-provisioning in AKS](/en-us/azure/aks/node-auto-provisioning).

### Scale limits

Plan scaling with AKS limits, Azure subscription quotas, regional VM capacity, IP address capacity, and the AKS pricing tier. Current AKS scale limits include the following values.

| Resource | Limit |
| --- | --- |
| Nodes per cluster with Virtual Machine Scale Sets and Standard Load Balancer SKU | Up to 5,000 for Standard and Premium tier clusters, subject to AKS quotas, regional capacity, and subscription quota. Free tier supports up to 1,000 nodes and is recommended for clusters with fewer than 10 nodes. |
| Nodes per virtual machine scale set node pool | 1,000 |
| Node pools per cluster | 100 |
| Pods per node | 250 |
| Azure CNI Overlay pod CIDR allocation | One `/24` pod CIDR per node |

For AKS service limits, see [AKS quotas, virtual machine size restrictions, and region availability](/en-us/azure/aks/quotas-skus-regions). For Azure CNI Overlay pod CIDR planning, including the per\-node `/24` allocation, see [Azure CNI Overlay IP address planning](/en-us/azure/aks/concepts-network-azure-cni-overlay#ip-address-planning).

---

## Try\-This exercise \- Create an Azure Kubernetes Service cluster

Azure Kubernetes Service (AKS) simplifies deploying a managed Kubernetes cluster in Azure by offloading operational work to Azure. Azure manages the Kubernetes control plane and critical tasks such as health monitoring and maintenance. AKS clusters use one of three cluster management pricing tiers: **Free**, **Standard**, or **Premium**. The Free tier has no cluster management charge but provides only best\-effort uptime (no financial SLA). The Standard tier includes a 99\.9% Uptime SLA (99\.95% when the cluster uses Availability Zones). The Premium tier provides the same Uptime SLA as Standard (99\.9%, or 99\.95% with Availability Zones) and is the required pricing tier for enabling Long Term Support (LTS). When you use Premium, you also explicitly select the LTS support plan (`--k8s-support-plan AKSLongTermSupport`), which extends Kubernetes version support to two years from GA (one year of community support plus one additional year of long\-term support).

AKS nodes run on Azure virtual machines (VMs). With AKS nodes, you can connect storage to nodes and pods, upgrade cluster components, and use GPUs. AKS supports Kubernetes clusters that run multiple node pools to support mixed operating systems and Windows Server containers.

When you deploy an AKS cluster, you choose settings such as node count, VM size, region, networking, monitoring, and integrations. AKS deploys and configures the Kubernetes control plane and nodes.

Note

To complete this procedure, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

Note

This exercise creates a standard, custom\-configured AKS cluster. It doesn't use AKS Automatic.

1. Sign in to the Azure portal at [https://portal.azure.com](https://portal.azure.com/).
2. Select **Create a resource**.
3. Search the marketplace for **Azure Kubernetes Service (AKS)**, or browse **Categories** \> **Infrastructure Services** (or **Containers**, depending on the portal version) \> **Azure Kubernetes Service (AKS)**, and then select **Create**.
4. Configure **Basics**:

	* Under **Project details**, select an Azure **Subscription**, and create or select the resource group **myResourceGroup**. For testing or evaluation, use a separate resource group so you can remove the lab resources without affecting production or development workloads.
	* Under **Cluster details**, set **Cluster preset configuration** to **Dev/Test**, enter **myAKSCluster** for **Kubernetes cluster name**, choose a **Region**, set **Fleet manager** to **None**, set **Availability zones** to **None** (this evaluation lab uses **None** to keep deployment simple and avoid regional SKU constraints; production node pools should use Availability Zones in supported regions), explicitly set **AKS pricing tier** to **Free** (the Dev/Test preset doesn't change the pricing tier, so you must select Free yourself), and leave **Kubernetes version** at the default N\-1 latest patch version.
	* Under **Authentication and Authorization**, set the option to **Local accounts with Kubernetes RBAC** for this evaluation lab to keep the steps minimal and avoid an extra Azure RBAC role assignment. For production clusters, choose **Microsoft Entra ID authentication with Azure RBAC** instead, and grant your account both the **Azure Kubernetes Service Cluster User Role** (which allows `az aks get-credentials` to download the kubeconfig) and an additional Kubernetes\-API role (for example, **Azure Kubernetes Service RBAC Reader**) so `kubectl` calls succeed. On Microsoft Entra ID\-integrated clusters, the Cluster User Role alone only enables kubeconfig download and triggers a sign\-in prompt — Kubernetes API permissions are then governed by the user's Microsoft Entra group membership and the assigned Azure RBAC for Kubernetes role. On clusters that don't use Microsoft Entra ID (such as the local\-accounts cluster created in this lab), the Cluster User Role grants admin\-equivalent access. For Microsoft Entra ID\-integrated clusters running Kubernetes 1\.24 or later, the `kubelogin` exec\-plugin format is configured in the kubeconfig automatically for interactive Azure CLI sign\-in, so no extra conversion is required. The lab cluster created here uses local accounts, so `kubelogin` isn't involved in the lab connection step. After the lab, you can enforce Microsoft Entra ID authentication by first enabling Microsoft Entra integration on the cluster and then disabling local accounts. **Do not disable local accounts on this lab cluster as configured** — it uses local accounts only, and disabling them without first enabling Microsoft Entra integration locks every user out of the cluster. The correct sequence is to first enable Microsoft Entra ID authentication: `az aks update --resource-group myResourceGroup --name myAKSCluster --enable-aad --aad-admin-group-object-ids <entra-group-object-id>`. If you also want to use Azure RBAC for Kubernetes Authorization, then enable it: `az aks update --resource-group myResourceGroup --name myAKSCluster --enable-azure-rbac` and assign AKS RBAC roles to the appropriate Microsoft Entra users or groups. Only after Microsoft Entra integration is in place should you run `az aks update --resource-group myResourceGroup --name myAKSCluster --disable-local-accounts`.
	* Select **Next: Node pools**.
5. Configure **Node pools**:

	* Accept the Dev/Test preset defaults for the system node pool. If you change **Node size**, choose a supported D\-series SKU such as **Standard\_D4ds\_v5**; B\-series VMs aren't supported for system node pools.
	* Leave virtual nodes disabled for this exercise.
Note

Virtual nodes require Azure CNI in flat\-networking mode (the documented examples use Azure CNI Node Subnet) with a delegated virtual\-node subnet, because Azure Container Instances need direct VNet\-routable pod IPs. As a result, virtual nodes aren't compatible with **Azure CNI Overlay** and are out of scope for this lab — see the virtual nodes documentation.

	* Select **Next: Networking**.
6. Configure **Networking**:

	* Set the network configuration option (labeled **Container networking** or **Network configuration** depending on the portal version) to **Azure CNI Overlay**. Use kubenet only for legacy clusters; kubenet retires on March 31, 2028\.
	* Set **Network dataplane** to **Cilium (Azure CNI Powered by Cilium)**.
	* Set **Network policy** to **Cilium** (recommended).
	
	
	
	Note
	
	
	This **Network policy** selection overrides the Dev/Test preset default of **None**.
	* Accept the default **DNS name prefix**, virtual network, and subnet values for this lab.
	* Select **Next: Integrations**.
7. Configure **Integrations**:

	* Optionally attach an existing **Azure Container Registry** under **Azure Container Registry** (skip if you don't have one — you can attach an ACR later with `az aks update --name myAKSCluster --resource-group myResourceGroup --attach-acr <acr-name>`). The command creates an `AcrPull` role assignment for the kubelet managed identity, so the caller needs permission to create role assignments on the registry. The command isn't supported for ABAC\-enabled ACR registries (RBAC Registry \+ ABAC Repository Permissions); for those, manually assign the `Container Registry Repository Reader` role to the kubelet managed identity instead.
	* Enable **Container insights** (Azure Monitor) for cluster observability.
	* For this lab, leave **Managed Prometheus**, **Azure Managed Grafana**, **Azure Policy**, and **Defender for Containers** disabled to minimize cost. Enable each in production for managed metrics, governance, and runtime threat protection.
	* Select **Next: Monitoring**.
8. Review **Monitoring**:

	* Review **Container insights** and alert rules, and confirm the lab settings are selected.
	* Select **Next: Advanced**.
9. Review **Advanced**:

	* Accept the defaults for this lab.
	* Select **Next: Tags**.
10. Review **Tags**:

* Accept the defaults and select **Next: Review \+ create**.

11. Validate and create the cluster:

* Review the settings. If validation fails, update the settings identified by the validation message.
* Select **Create**.

12. Open the deployed cluster:

* When the deployment completes, select **Go to resource**, or open **myResourceGroup** and select **myAKSCluster**.

13. Connect to the cluster from Azure Cloud Shell:

* Select **Connect**.
* Start **Cloud Shell**.
* Run the following command to download the cluster credentials:

```
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

```

14. Verify the connection:

* Run the following command to verify that `kubectl` can connect to the cluster:

```
kubectl get nodes

```
* Optionally, list deployments across all namespaces (you can use the `-A` shorthand for `--all-namespaces`):

```
kubectl get deployments --all-namespaces

```

15. Clean up:

* When you're finished with the lab, delete **myResourceGroup**. Deleting this resource group deletes the AKS resource and its managed node resource group, including cluster infrastructure such as nodes, the Standard Load Balancer, and public IP addresses. The Free tier removes only the cluster management charge, not the cost of consumed resources.

```
az group delete --name myResourceGroup --yes --no-wait

```
* Container insights uses a Log Analytics workspace for logs. It might create a Log Analytics workspace outside **myResourceGroup** (for example, a `DefaultWorkspace-<GUID>-<Region>` workspace), or it might use an existing workspace. Check for any Log Analytics workspace created or selected only for this lab outside **myResourceGroup** and delete that lab\-created workspace too. If you enabled Managed Prometheus or Azure Managed Grafana, also remove any Azure Monitor workspace or Grafana resource created only for this lab. Don't delete workspaces or Grafana resources that predate the lab or are used by other resources.

---

## Module assessment

Choose the best response for each question.

### Check your knowledge

---

## Summary

In this module, you learned how to:

* Create an Azure Kubernetes Service cluster.
* Configure Azure Kubernetes Service components.
* Connect to an Azure Kubernetes Service cluster.
* Configure Microsoft Entra ID integration.
* Plan virtual network topology and IP addressing for an Azure Kubernetes Service (AKS) cluster.
* Review node and pod scaling options for an AKS cluster.

### Learn more

* [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) \| [Azure free account FAQ](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn#FAQ)
* [Free account for Students](https://azure.microsoft.com/free/students/?cid=msft_learn) \| [Azure for students FAQ](/en-us/azure/education-hub/azure-dev-tools-teaching/program-faq?azure-portal=true#azure-for-students)
* [Create an Azure account](/en-us/training/modules/create-an-azure-account/)
* [AKS pricing tiers (Free, Standard, Premium)](/en-us/azure/aks/free-standard-pricing-tiers)
* [Azure CNI Overlay networking in AKS](/en-us/azure/aks/concepts-network-azure-cni-overlay)
* [AKS Long Term Support (LTS)](/en-us/azure/aks/long-term-support)
* [AKS\-managed Microsoft Entra ID integration](/en-us/azure/aks/entra-id-control-plane-authentication)
* [Cluster autoscaler in AKS](/en-us/azure/aks/cluster-autoscaler)
* [AKS baseline reference architecture](/en-us/azure/architecture/reference-architectures/containers/aks/baseline-aks)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/deploy-azure-kubernetes-service-cluster/_

## Fuentes
- [Deploy an Azure Kubernetes Service cluster](https://learn.microsoft.com/en-us/training/modules/deploy-azure-kubernetes-service-cluster/?WT.mc_id=api_CatalogApi)
