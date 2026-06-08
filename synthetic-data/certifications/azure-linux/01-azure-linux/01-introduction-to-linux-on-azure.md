# Introduction to Linux on Azure

> Curso: Linux on Azure (azure-linux) · Seccion: Linux on Azure
> Duracion estimada: 44 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Suppose you're an experienced Linux admin who's tasked with deploying a new Linux environment on Azure. You know you need to understand the tradeoffs between the two major approaches (IaaS and PaaS) and the different ways you can deploy within each approach. You also want to understand how to select a Linux distribution, decide on a subscription model, and identify the most appropriate supporting Azure services for your needs.

In this module, you'll learn about the types of services and platforms that Azure provides for Linux environments. Whether you're exploring the migration of Linux\-based workloads to the cloud or you're looking at rearchitecting your Linux\-based applications to increase agility and reduce time to market, after completing this module, you should be able to choose which types of services you'll need to start planning your Linux environment on Azure.

---

## What is Linux on Azure?

The Microsoft Azure cloud is a worldwide network of state\-of\-the\-art datacenters and more than 200 products and cloud services designed to support a broad spectrum of business and technical scenarios. Moving to Azure enables you to minimize the burden of maintaining physical infrastructure and benefit from advanced compute services. Microsoft and third parties on Azure offer many programming languages, development frameworks, and operating\-system distributions. Microsoft and its partners also offer hundreds of prebuilt solutions that can quickly add value to both new and existing workloads.

Linux is the fastest growing platform on Azure, so Linux users will find familiar tools and systems. Microsoft and its partners also offer hundreds of prebuilt solutions that can quickly add value to both new and existing workloads.

* First, choose the Linux distribution you want based on familiarity, usage, cost, and support requirements. You can bring your own distribution or find distributions in [Azure Marketplace](https://azuremarketplace.microsoft.com).
* If you bring your own Linux distribution, follow [Azure guidelines to prepare your image](/en-us/azure/virtual-machines/linux/create-upload-generic).
* Linux\-based images in Azure Marketplace include base distributions and images with preinstalled software for specific scenarios. All images contain the software and configuration that's needed to ensure smooth operation on Azure VMs. This includes kernel\-level driver support for Azure infrastructure like storage and networking, and Azure\-supported features like remote direct memory access.
* Many of the images in Azure Marketplace are free: you pay only for the virtual infrastructure your VM consumes. Some images have other license and purchase terms for the software they include. You'll learn more about pricing and support options later in this module.
* You can also find hundreds of other Linux images for third\-party developer tools, security, databases, analytics, and more.

As you think about designing a computing environment on Azure, distinguish between four general\-usage models available: infrastructure as a service (IaaS), platform as a service (PaaS), database as a service (DBaaS), and software as a service (SaaS). Unit 4 describes in more depth why you might choose one of these models over the other and what the tradeoffs might be.

**IaaS**: Azure maintains the physical hardware and provisions more computing resources as needed. You, the customer, are responsible for managing the operating system, configuring other services for security, web applications, your development environment, application deployment, and monitoring.

**PaaS**: Azure maintains all aspects of the infrastructure, but allows you to control, configure, and deploy applications.

**DBaaS**: Azure automates database updates, provisioning, and backups, which let you focus on application development.

**SaaS**: Azure manages complete applications that customers subscribe to, such as Microsoft 365 and Dynamics 365\. ISVs (Independent software vendors) offer a wide range of SaaS solutions on the Microsoft [AppSource](https://appsource.microsoft.com/) site.

This module focuses on IaaS, PaaS, and DBaaS options for Linux.

---

## Summary

With Azure, you have the freedom to choose to use IaaS, PaaS, or both. Before you plan a move to Azure, you need to evaluate your short\-term and long\-term goals and decide the best approach for your various workloads. With Linux on Azure, you can take advantage of existing Linux skill sets and rely on familiar tools and methods for provisioning and maintaining systems while offloading hardware support responsibilities. When you're ready, you can use tools like Azure Resource Manager to integrate with more advanced services and solutions.

As with any technology shift, analyzing the current environment and planning carefully are key.

Now that you have a better understanding of the resources available for your Linux deployment, it's time to begin planning and sizing your environment to best meet your needs.

### Learn more

* [Choose an Azure compute service \- Azure Architecture Center](/en-us/azure/architecture/guide/technology-choices/compute-decision-tree)
* [Use platform as a service (PaaS) options \- Azure Architecture Center](/en-us/azure/architecture/guide/design-principles/managed-services?source=recommendations)
* [Integrated support for Red Hat solutions in Microsoft Azure](https://www.redhat.com/en/partners/microsoft/red-hat-on-azure)
* [Red Hat on Azure](https://azure.microsoft.com/solutions/linux-on-azure/red-hat/)
* [SUSE on Azure](https://azure.microsoft.com/solutions/linux-on-azure/suse/)
* [Ubuntu on Azure](https://ubuntu.com/azure)
* [Azure Hybrid Benefit for Red Hat Enterprise Linux (RHEL) and SUSE Linux Enterprise Server (SLES) virtual machines](/en-us/azure/virtual-machines/linux/azure-hybrid-benefit-linux)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/intro-to-linux-on-azure/_

## Fuentes
- [Introduction to Linux on Azure](https://learn.microsoft.com/en-us/training/modules/intro-to-linux-on-azure/?WT.mc_id=api_CatalogApi)
