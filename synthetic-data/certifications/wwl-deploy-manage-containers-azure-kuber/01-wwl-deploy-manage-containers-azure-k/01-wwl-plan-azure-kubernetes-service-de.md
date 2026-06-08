# Plan an Azure Kubernetes Service deployment

> Curso: Deploy containers by using Azure Kubernetes Service (AKS) (wwl-deploy-manage-containers-azure-kubernetes-serv) · Seccion: Deploy containers by using Azure Kubernetes Service (AKS)
> Duracion estimada: 43 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

This module covers the core infrastructure components of Kubernetes and how they're used in Azure Kubernetes Service (AKS).

### Scenario

As application development continues to move towards a container\-based approach, there's an increasing need to orchestrate and manage resources. Kubernetes provides reliable scheduling of fault\-tolerant application workloads, making it the leading platform for container orchestration. Azure Kubernetes Service (AKS) is a managed Kubernetes offering that further simplifies container\-based application deployment and management.

In this module, you learn about the core Kubernetes infrastructure components, including the control plane, node pools, pods, deployments, namespaces, services, ingress, and load balancing in AKS. You learn how to build and run modern, portable, microservices\-based applications using Kubernetes to orchestrate and manage the availability of the application components. Finally, you learn how AKS provides a managed Kubernetes service that reduces the complexity of deployment and core management tasks, like upgrade coordination.  

### Learning Objectives

After completing this module, you'll be able to:

* Describe control plane components, node pools, pods, deployments, namespaces, and network access in AKS.
* Schedule fault\-tolerant application workloads using Azure Kubernetes Service.
* Manage core AKS tasks such as deployment and upgrade coordination.
* Explain how Kubernetes clusters group nodes that share compute, network, and storage resources.

### Goals

The goal of this module is to provide an understanding of the core infrastructure components of Kubernetes and how they're used in Azure Kubernetes Service (AKS).

---

## Azure Kubernetes Service

Kubernetes is a rapidly evolving platform that manages container\-based applications and their associated networking and storage components. Kubernetes focuses on the application workloads, not the underlying infrastructure components. Kubernetes provides a declarative approach to deployments, backed by a robust set of APIs for management operations.

You can build and run modern, portable, microservices\-based applications, using Kubernetes to orchestrate and manage the availability of the application components. Kubernetes supports both stateless and stateful applications as teams progress through the adoption of microservices\-based applications.

As an open platform, Kubernetes allows you to build your applications with your preferred programming language, OS, libraries, or messaging bus. Existing continuous integration and continuous delivery (CI/CD) tools can integrate with Kubernetes to schedule and deploy releases.

AKS provides a managed Kubernetes service that reduces the complexity of deployment and core management tasks, like upgrade coordination. Azure manages the AKS control plane and offers three pricing tiers: Free (no uptime SLA, intended for development and testing), Standard (per\-cluster hourly fee with a financially backed uptime SLA, recommended for production workloads), and Premium (Standard plus 24\-month Long\-Term Support for eligible Kubernetes versions, beginning with version 1\.27\). For every tier, you also pay for the worker node VMs that run your applications.

The basic components for Azure Kubernetes Service are:

* **Azure Kubernetes Service** (AKS). AKS is a managed Kubernetes cluster hosted in the Azure cloud. Azure manages the AKS control plane. Agent nodes are a shared responsibility: you configure and pay for node pools and keep supported node images and Kubernetes versions current, while AKS manages supported node lifecycle operations and remediation.
* **Virtual network**. By default, AKS creates a virtual network into which agent nodes are connected. You can create the virtual network first for more advanced scenarios, which lets you control things like subnet configuration, on\-premises connectivity, and IP addressing.
* **Ingress**. An ingress controller exposes HTTP(S) routes to services inside the cluster.
* **Azure Load Balancer**. Once the AKS cluster is created, the cluster is ready to use the Standard SKU Azure Load Balancer. For public ingress, AKS configures load balancer frontend IPs and rules with cluster nodes, node IPs, or node\-pool instances in the backend pool. Kubernetes Service routing then forwards traffic to ingress\-controller pod endpoints. Internal load balancers and private ingress configurations are also supported.
* **External data stores**. Microservices are typically stateless and write state to external data stores, such as Azure SQL Database or Azure Cosmos DB.
* **Microsoft Entra ID**. AKS uses a Microsoft Entra ID identity to create and manage other Azure resources such as Azure load balancers. Microsoft Entra ID is also recommended for user authentication in client applications.
* **Azure Container Registry**. Use Container Registry to store private container images, which are deployed to the cluster. The recommended way to authenticate AKS with Azure Container Registry is to attach the registry to the cluster, which assigns the AcrPull role to the kubelet managed identity. AKS doesn't require Azure Container Registry — you can use any OCI\-compliant registry — but anonymous pulls from public registries such as Docker Hub are subject to rate limits, so a private or authenticated registry is recommended for production workloads.
* **Azure Monitor**. Azure Monitor collects and stores metrics and logs, application telemetry, and platform metrics for the Azure services. Use this data to monitor the application, set up alerts, dashboards, and perform root cause analysis of failures. Azure Monitor integrates with AKS to collect metrics from controllers, nodes, and containers.

---

## Azure Kubernetes cluster architecture

At the highest level, Kubernetes is a cluster of machines—called nodes—that share compute, network, and storage resources. Each cluster has a control plane connected to one or more worker nodes. The worker nodes are responsible for running groups of containerized applications and workloads, known as pods, and the control plane manages which pods run on which worker nodes. In production, the control plane runs as a highly available, multi\-replica service. In Azure Kubernetes Service (AKS), the control plane is fully managed by Azure. AKS node\-pool nodes are Azure virtual machines, and AKS can also use virtual nodes backed by Azure Container Instances for specific scale\-out scenarios.

Furthermore, a Kubernetes cluster is divided into two components:  

* **Control plane**: provides the core Kubernetes services and orchestration of application workloads.
* **Nodes**: run your application workloads.

A cluster is a set of computers that you configure to work together and view as a single system. A Kubernetes cluster contains at least one control plane and one or more nodes. In self\-managed Kubernetes, the control plane and node instances can be physical devices, virtual machines, or instances in the cloud; in AKS, the control plane is a managed Azure service and node\-pool nodes are Azure virtual machines. Linux is the default host OS, and the AKS system node pool must run Linux. AKS also supports Windows Server LTSC node pools for Windows container workloads. Supported Windows Server versions depend on the Kubernetes version: Windows Server 2022 isn't supported for node pools running Kubernetes 1\.36 or later, and Windows Server 2025 LTSC is currently in preview where available.

A cluster uses centralized software that's responsible for scheduling and controlling these tasks. The computers in a cluster that run application workloads are called *nodes*, and the set of components that run the scheduling and orchestration software is called the *control plane*. In AKS, the control plane is a managed Azure service, and you don't manage the machines that host its components.

A node in a Kubernetes cluster is where your compute workloads run. Each node communicates with the control plane via the API server to inform it about state changes on the node.

For the control plane to communicate with the worker nodes—and for a person to communicate with the control plane—Kubernetes includes many components that make up the control plane.

Developers and operators interact with the cluster primarily by using kubectl, a command\-line tool that installs on their local OS. Commands issued through kubectl are sent to the kube\-apiserver, the component of the control plane that exposes the Kubernetes API. The kube\-apiserver validates the request, creates or updates Kubernetes API objects, and stores API object data, including desired state in object specs, in etcd. The kube\-controller\-manager runs control loops that continuously watch the kube\-apiserver for state changes and reconciles the cluster by issuing further API calls. The kubelet on each worker node also watches the kube\-apiserver for pods assigned to its node and ensures that those containers are running.

The control plane stores cluster state and configuration in etcd, a distributed key\-value store. To run pods with your containerized apps and workloads, you describe the desired state to the cluster in a YAML manifest. The manifest is submitted to the kube\-apiserver, which creates or updates Kubernetes API objects from it and stores API object data and cluster state in etcd. Workload controllers in the kube\-controller\-manager (such as the Deployment controller) watch for new objects and create the underlying resources, such as ReplicaSets and Pods, by calling the kube\-apiserver. The kube\-scheduler independently watches for newly created pods that have no node assignment, selects an appropriate node based on resource requirements and policies, and writes the binding back through the kube\-apiserver. The kubelet on the chosen node then pulls the container images and starts the pod's containers.

In a Kubernetes deployment, the desired state you describe is stored in object specs, while current state is reported in object status and actual cluster state. Controllers continuously reconcile the actual state toward the desired state. Kubernetes supports rollbacks, rolling updates, and pausing rollouts: Deployments retain a configurable revision history of their underlying ReplicaSets so you can roll back to a previous version. Deployments use ReplicaSets to ensure that the specified number of identically configured pods are running. If one or more pods fail, the ReplicaSet replaces them. In this way, Kubernetes is said to be self\-healing.

---

## Azure Kubernetes Service pods

Kubernetes uses *pods* to run an instance of your application. A pod represents a single instance of your application.

Pods typically have a 1:1 mapping with a container. In advanced scenarios, a pod may contain multiple containers. Multi\-container pods are scheduled together on the same node, and allow containers to share related resources.

When you create a pod, you can define *resource requests* to request a certain amount of CPU or memory. The Kubernetes Scheduler uses requests to place a pod on a node that has enough available resources to satisfy them. You can also specify *resource limits* to cap how much CPU or memory a container can consume; the kubelet on each node enforces these limits at runtime. Best practice is to set both requests and limits for all pods—requests inform scheduling decisions, and limits prevent a single pod from starving other workloads on the node.

A pod is a logical resource, but application workloads run on the containers. Pods are typically ephemeral, disposable resources. Individually scheduled pods miss some of the high availability and redundancy Kubernetes features. Pods are deployed and managed using Kubernetes *Controllers*, such as the Deployment Controller.  

### Pod Disruption Budgets

A *Pod Disruption Budget* (PDB) defines the minimum number of pod replicas that must remain available—or the maximum that can be simultaneously unavailable—during voluntary disruptions, such as node drains during cluster upgrades or scale\-down operations. PDBs help maintain application availability while still allowing controlled maintenance to proceed. When you plan an AKS deployment, defining PDBs for production workloads protects against availability loss during planned cluster maintenance.

---

## Nodes and node pools for Azure Kubernetes Service

Creating an Azure Kubernetes Service (AKS) cluster automatically creates and configures the control plane, which provides [core Kubernetes services](https://kubernetes.io/docs/concepts/overview/components) and application workload orchestration. AKS offers three cluster management tiers: Free (no uptime SLA, intended for development and testing), Standard (paid per\-cluster fee with a financially backed uptime SLA, recommended for production workloads), and Premium (Standard plus Long\-Term Support for eligible Kubernetes versions, beginning with version 1\.27\). The control plane and its resources exist only in the region where you created the cluster.

The nodes, also called *agent nodes* or *worker nodes*, host the workloads and applications. In AKS, customers configure and pay for node pools and keep cluster versions and node images supported and current, while AKS manages supported node lifecycle operations and remediation. Directly modifying the underlying node VMs through IaaS APIs is unsupported.

To run applications and supporting services, an AKS cluster needs at least one node: an Azure virtual machine (VM) to run the Kubernetes node components and container runtime. Every AKS cluster must contain at least one system node pool. A single\-node system pool is supported only for development or test clusters; for production workloads, the system node pool must contain at least two nodes (three or more is recommended for fault tolerance and Availability Zone coverage).

AKS groups nodes of the same configuration into *node pools* of VMs. *System* node pools host critical Kubernetes system pods such as CoreDNS and metrics\-server, and shouldn't normally be used to run your own application workloads. *User* node pools serve the primary purpose of hosting workload pods. If you want to have only one node pool in your AKS cluster, for example in a development environment, you can schedule application pods on the system node pool.

You can also create multiple user node pools to segregate different workloads on different nodes.

---

## Namespaces for Azure Kubernetes Service

Most workload resources, such as Pods, Deployments, and Services, are namespaced. Some resources, such as Nodes, PersistentVolumes, StorageClasses, and namespaces, are cluster\-scoped. Use namespaces to logically divide an AKS cluster and create, view, or manage resources. For example, you can create namespaces to separate business groups. Kubernetes RBAC or other authorization mechanisms can be used to scope user access to namespaces; ClusterRoleBindings can grant cluster\-wide or cross\-namespace access.

When you create an AKS cluster, the following namespaces are available:  

| **Namespace** | **Description** |
| --- | --- |
| *default* | Used when no namespace is specified. The default namespace is suitable for simple or test scenarios, but production workloads should usually use dedicated namespaces. |
| *kube\-system* | Where core system resources exist, such as CoreDNS, metrics\-server, and other AKS components. kube\-proxy exists depending on networking configuration; AKS clusters that use the Cilium data plane don't use kube\-proxy. You typically don't deploy your own applications into this namespace. |
| *kube\-public* | Typically not used. Reserved for resources that need to be visible across the whole cluster and readable by any user. |
| *kube\-node\-lease* | Holds Lease objects associated with each node. The kubelet sends heartbeats to its Lease so the control plane can detect node failures quickly. |

---

## Access to Azure Kubernetes Service

To allow access to your applications or between application components, Kubernetes provides an abstraction layer to virtual networking. Kubernetes nodes connect to a virtual network, providing inbound and outbound connectivity for pods. The *kube\-proxy* component commonly provides Service networking in many configurations, but AKS clusters with Azure CNI powered by Cilium don't use kube\-proxy.

In Kubernetes:

* *Services* typically group pods using label selectors and provide a stable IP address or DNS name to reach them. The ExternalName service type is an exception—it maps a service name to an external DNS hostname.
* *ServiceTypes* allow you to specify what kind of Service you want.
* You can distribute traffic using a *load balancer*.
* More complex routing of application traffic can also be achieved with *ingress controllers*.

The Azure platform also simplifies virtual networking for AKS clusters. When you create a Kubernetes LoadBalancer service, AKS provisions a Standard SKU Azure Load Balancer (the Basic SKU was retired on September 30, 2025\). As you open network ports to pods, the corresponding Azure network security group rules are configured. The Application Routing add\-on is a Microsoft\-managed NGINX ingress option supported through November 2026; AKS is moving toward Gateway API as the long\-term direction.

### Services

To simplify the network configuration for application workloads, Kubernetes uses *Services* to logically group a set of pods together and provide network connectivity. You can specify a Kubernetes *ServiceType* to specify what kind of Service you want.

The following ServiceTypes are available:

* **ClusterIP**

ClusterIP creates an internal IP address for use within the AKS cluster. This Service is good for *internal\-only applications* that support other workloads within the cluster.
* **NodePort**

NodePort creates a port mapping on the underlying node that allows the application to be accessed directly with the node IP address and port. NodePort allocates a port from the cluster's configured node\-port range (default 30000–32767\) on every node.
* **LoadBalancer**

LoadBalancer creates a Standard SKU Azure load balancer resource. In AKS, the Azure Load Balancer backend pool contains cluster nodes, node IPs, or node pool instances, not pods. By default, AKS provisions a public Standard Load Balancer frontend IP; using the internal load balancer annotation provisions a private IP instead. Load balancing rules are created on the desired ports so the load balancer distributes traffic to cluster nodes, and Kubernetes Service networking forwards it to the selected pod endpoints.

For extra control and routing of the inbound traffic, you may instead use an [Ingress controller](/en-us/azure/aks/concepts-network-ingress#ingress-controllers).
* **ExternalName**

Maps the service to an external DNS hostname by configuring the cluster DNS to return a CNAME record. No traffic proxying is performed; pods resolve the in\-cluster service name and DNS redirects them to the external endpoint.

Either the load balancers and services IP address can be dynamically assigned, or you can specify an existing static IP address. You can assign both internal and external static IP addresses. Existing static IP addresses are often tied to a DNS entry.

You can create both *internal* and *external* load balancers. Internal load balancers are only assigned a private IP address, so they can't be accessed from the Internet.

### Azure virtual networks

AKS supports several network plug\-ins (Container Network Interface, or CNI), grouped into two networking models:

* **Overlay model** — Pods receive IP addresses from a private CIDR that is logically separate from the virtual network subnet that hosts the nodes. This model conserves virtual network IP space and scales to large clusters.
* **Flat (VNet\-integrated) model** — Pods receive IP addresses from the same virtual network as the nodes, so pods are directly addressable from other resources in the virtual network.

#### Recommended plug\-ins

* **Azure CNI Overlay** — The default plug\-in for new AKS clusters. Pod IPs come from a private overlay CIDR, and traffic leaving the cluster is source NATed (SNATed) to the node IP. Recommended for most scenarios.
* **Azure CNI Pod Subnet** — Pods receive IPs from a separate, dedicated subnet in the virtual network and are directly addressable from other VNet resources without NAT. Recommended when pods need direct VNet IP connectivity.
* **Azure CNI Powered by Cilium** — Combines supported Azure CNI IPAM modes, including overlay, virtual\-network pod subnet with dynamic pod IP allocation, and node subnet mode where supported, with the Cilium eBPF data plane for advanced network policy and observability.

#### Legacy plug\-ins

* **Azure CNI Node Subnet** — The original Azure CNI mode. Every pod receives an IP address from the node's virtual network subnet, and the maximum number of pod IPs per node is reserved up front. This approach can lead to IP exhaustion in large or growing clusters, so plan IP space carefully.
* **Kubenet** — A legacy overlay plug\-in. Pods receive IPs from a logically separate address space and use network address translation (NAT) to reach resources on the virtual network; the source IP is translated to the node's primary IP. Kubenet is scheduled to be **retired on March 31, 2028** and isn't recommended for new clusters. Migrate to Azure CNI Overlay before that date.

#### Advanced options

* **Bring your own (BYO) CNI** — Use `--network-plugin none` to install and manage your own CNI plug\-in. Microsoft support can't assist with CNI\-related issues in BYO CNI clusters; use AKS\-supported CNI plug\-ins when Microsoft CNI support is required.

### Ingress controllers

When you create a LoadBalancer\-type Service, you also create an underlying Azure load balancer resource. The load balancer is configured to distribute traffic on the Service port to cluster nodes. Kubernetes Service routing then forwards that traffic to matching pod endpoints for the Service.

The *LoadBalancer* only works at layer 4\. At layer 4, the Service is unaware of the actual applications, and can't make any more routing considerations.

*Ingress controllers* work at layer 7 and can use more intelligent rules to distribute application traffic. Ingress controllers typically route HTTP traffic to different applications based on the inbound URL.

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary

In this module, you learned about:

* Control plane components, node pools, pods, deployments, namespaces, and network access in AKS.
* Scheduling fault\-tolerant application workloads using Azure Kubernetes Service.
* Managing core AKS tasks, including deployment and upgrade coordination.
* How Kubernetes clusters group nodes that share compute, network, and storage resources.

### Learn more

* [Azure free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) \| [Azure free account FAQ](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn#FAQ)
* [Free account for Students](https://azure.microsoft.com/free/students/?cid=msft_learn) \| [Azure for students FAQ](/en-us/azure/education-hub/azure-dev-tools-teaching/program-faq?azure-portal=true#azure-for-students)
* [Create an Azure account](/en-us/training/modules/create-an-azure-account/?azure-portal=true) module on Learn.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/plan-azure-kubernetes-service-deployment/_

## Fuentes
- [Plan an Azure Kubernetes Service deployment](https://learn.microsoft.com/en-us/training/modules/plan-azure-kubernetes-service-deployment/?WT.mc_id=api_CatalogApi)
