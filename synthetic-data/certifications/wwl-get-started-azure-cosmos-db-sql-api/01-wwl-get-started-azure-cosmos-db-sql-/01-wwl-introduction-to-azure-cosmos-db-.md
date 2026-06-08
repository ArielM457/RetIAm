# Introduction to Azure Cosmos DB for NoSQL

> Curso: Get started with Azure Cosmos DB for NoSQL (wwl-get-started-azure-cosmos-db-sql-api) · Seccion: Get started with Azure Cosmos DB for NoSQL
> Duracion estimada: 24 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Today's apps deliver innovation in all facets of life. For a business to remain competitive, companies must build apps and products that work with real\-time data, are resilient, flexible and can support the next generation of AI capabilities.

Modern apps thrive on real\-time data from different sources, shaped in different forms. An apps' usefulness is often in its ability to move and use data.

Developers require flexibility in their platforms so they can be responsive to business changes. Developers also require their entire application ecosystem to flexibly handle changes in the velocity, volume, or shape of their data. This flexibility enables developers to develop new features more rapidly than they ever have before.

### Scenario

Suppose you work as the lead developer at a retail company. Your team is building your online storefront with AI Agents to assist customers in all aspects of their experience. You're designing the new storefront to be accessible across various devices including mobile. The team expects a spike in demand when the storefront is published and various "grand opening" sales begin.

As the lead developer, you have been tasked with identifying a database platform. The database platforms you consider should be able to service the data your team will generate and collect over time. The selected database should also be able to handle a large variety of data, at high volumes and velocity. Your database solution needs to scale quickly and with little friction in order to handle this demand that is both growing and variable. Your database should be able to support the vectorized data for search using AI Agents that handle customer requests.

### Azure Cosmos DB

Azure Cosmos DB is a fast NoSQL database service for modern and AI app development at any scale.

Here, we look at how Azure Cosmos DB and its NoSQL API can be used for this type of business problem. We also learn a bit about how the database works. At the end, this module helps you decide if Azure Cosmos DB for NoSQL is a good choice for your solutions.

After completing this module, you’ll be able to:

* Evaluate whether Azure Cosmos DB for NoSQL is the right database for your application.
* Describe how the features of the Azure Cosmos DB for NoSQL are appropriate for modern applications.

---

## How does Azure Cosmos DB for NoSQL work

Now that we know the basics of Azure Cosmos DB, let's see what resources and information are required to start working with an account. This information should help you decide whether Azure Cosmos DB for NoSQL works for your data set. Also, it should help you decide how much, if any, extra configuration is necessary.

### What are the components of Azure Cosmos DB for NoSQL?

To begin using Azure Cosmos DB, you first create various resources in Azure such as accounts, databases, containers, and items.

#### Accounts

**Accounts** are the fundamental units of high availability and tenant isolation for SaaS applications. At the account level, you can configure the region\[s] for your data in Azure Cosmos DB for NoSQL. Accounts also contain the globally unique DNS name used for API requests. You can also set the default consistency level for requests at the account level. You can manage or create accounts using the Azure portal, Azure Resource Manager templates, the Azure CLI, or Azure PowerShell.

#### Databases

Each account can contain one or more **Databases**. A database is a logical unit of management for containers in Azure Cosmos DB for NoSQL.

#### Containers

**Containers** are the fundamental unit of scalability in Azure Cosmos DB for NoSQL. With Azure Cosmos DB, you provision throughput at the container level. You can also optionally configure an indexing policy or a default time\-to\-live value at the container level. Azure Cosmos DB for NoSQL will automatically and transparently partition the data in a container.

#### Items

The NoSQL API for Azure Cosmos DB stores individual documents in JSON format as *items* within the container. Azure Cosmos DB for NoSQL natively supports JSON files and can provide fast and predictable performance because write operations on JSON documents are atomic.

### Partitioning \& Partition Keys

Every Azure Cosmos DB for NoSQL container is required to specify a **partition key path** that is used to distribute data for scale out. Behind the scenes, Azure Cosmos DB for NoSQL uses this path to logically partition data using **partition key values**. For example, consider the following JSON document:

```
{
  "id": "35b5bf7d-5f0e-4209-b7cb-8c5c70c3bb59",
  "deviceDisplayName": "shared-printer",
  "acquiredYear": 2019,
  "department": {
    "name": "information-technology",
    "metadata": {
      "location": "floor-5-unit-27"
    }
  },
  "queuedDocuments": [
    {
      "sender": "user-293749329",
      "sentTime": "2019-07-26T05:12:37",
      "pages": 5,
      "spoolRef": "3f4b759c-3230-4269-a88e-de7620ad91c0"
    },
    {
      "device": {
        "type": "mobile"
      },
      "sentTime": "2019-11-12T13:08:42",
      "spoolRefs": [
        "6a86682c-be5a-4a4a-bacd-96c4d1c7ece6",
        "79e78fe2-93aa-4688-89db-a7278b034aa6"
      ]
    }
  ]
}

```

If your container specifies a partition key **path** of `/department/name`, then the partition key **value** of this document would be `information-technology`. Behind the scenes, Azure Cosmos DB for NoSQL automatically manages the physical resources necessary to support your data workload.

Selecting a partition key path for a container is critical to allow applications to scale and is one of the most important design decisions for a new workload. Review the [choosing a partition key](/en-us/azure/cosmos-db/partitioning-overview#choose-partitionkey) documentation for a deeper technical explanation and best practices.

---

## When should you use Azure Cosmos DB for NoSQL

Azure Cosmos DB for NoSQL is a fully managed NoSQL database service for modern and AI app development. It provides guaranteed single\-digit millisecond response times, 99\.999\-percent availability and [vector database capabilities](/en-us/azure/cosmos-db/vector-database), backed by SLAs with automatic and instant scalability.

For enterprise scenarios, Azure Cosmos DB for NoSQL has a comprehensive suite of financially backed [service level agreements (SLAs)](https://azure.microsoft.com/support/legal/sla/cosmos-db/) that cover throughput, consistency, availability, and latency.

### Common use cases for the Azure Cosmos DB for NoSQL

As a fast NoSQL database with a flexible API and vector indexing and search capabilities, Azure Cosmos DB for NoSQL is well suited for many types and sizes of applications. From the very small scale, to high\-performance applications with global ambition. Speed and flexibility make Azure Cosmos DB for NoSQL great for Generative AI, web, retail, IoT, gaming, and mobile applications. Azure Cosmos DB for NoSQL is a good fit for applications that require flexibility, low cost, fast response times, and the ability to scale to massive volume or velocity.

#### Generative AI

Generative AI applications can be diverse and unpredictable. These workloads require a database platform that is cost\-efficient, responsive and scalable. Users can store vectors directly in their documents with traditional schema\-free data and high\-dimensional vectors as other properties. This colocation of data and vectors allows for efficient indexing and searching, as the vectors are stored in the same logical unit as the data they represent. Keeping vectors and data together simplifies data management, AI application architectures, and the efficiency of vector\-based operations.

In this example, customers are taking transactional and operational data and vectorizing it to be used for vector search by multiple AI Agents serving customers. Azure Cosmos DB's Change Feed is used to handle ingestion and vectorization of new or updated data, making it available in near real\-time for users. Customers interacting with these agents generate prompts and completions which are also stored as their chat history in Azure Comsos DB and used to provide a semantic cache for improved cost and performance.

#### Retail/marketing

Azure Cosmos DB for NoSQL is a great fit for retail and marketing workloads that can experience dramatic and unexpected swings in usage at any point throughout the year. The elastic scale of Azure Cosmos DB for NoSQL ensures that the database platform can handle requests during peak usage, and save money during nonpeak times.

In this example, a JavaScript web application, built on content stored in Azure Blob Storage, uses Azure Cosmos DB for NoSQL as it's backing database. Multiple accounts are used to manage different facets of the solution such as the shopping cart, inventory, or catalog. The solution then uses Azure Search to index the Azure Cosmos DB for NoSQL data, providing a rich search experience to end users.

#### Web/mobile

Many modern social applications generate a plethora of user\-generated content that is diverse in quantity, shape, and volume. Azure Cosmos DB for NoSQL is a great candidate for this workload as this API can store data of varying schemas. Consider the NoSQL API for data that may have schemas that change or evolve over time as the company's initiatives expand into new areas.

In this example, a user is using a URL to access a web site in their browser. The URL points to Azure Traffic Manager, which then uses a built\-in algorithm to determine which Azure App Service endpoint to redirect the user to. Since Azure Cosmos DB for NoSQL is capable of global distribution, you only need one account that is replicated across multiple regions.

### Module Scenario

Consider the scenario from the beginning of this module:

> Suppose you work as the lead developer at a retail company. Your team is building your online storefront with support for AI Agents to provide a rich experience for users. You're designing the new storefront to be accessible across various devices including mobile. The team expects a spike in demand when the storefront is published and various "grand opening" sales begin.

One key part of your store's success is the ability for the company to notify users of shipping updates regardless of what device they place the order on or are currently using. Your team has worked hard on a sophisticated system to manage detailed order status tracking. The tight integration of Azure Cosmos DB with other Azure services, let's you consider building solutions that use order data in Azure Cosmos DB for NoSQL to send notification to your user's mobile devices. The notifications alert them when their package ships, or is out for delivery.

This example is similar to the example from the introduction of this module. To build on the first example, your team has decided to introduce Azure Cosmos DB for NoSQL as the database of choice. Now, your team can use Azure Synapse Link to prepare and aggregate data for deeper analysis using Azure Synapse Analytics. Your team can also use services such as Azure Functions to react to data events with Azure Cosmos DB, and then trigger an Azure Logic Apps workflow that sends notifications to mobile devices.

---

## Summary

In this module, you learned how Azure Cosmos DB for NoSQL allows you to launch a database relatively easily. That database can grow with your company as your needs evolve as well as allows you to build the new generation of AI\-enabled applications.

Azure Cosmos DB for NoSQL eases many common pain points by offering an elastic, globally distributed database platform with support for vector indexing and search. Azure Cosmos DB for NoSQL scales up\-and\-down to meet your real\-world usage. The NoSQL API for Azure Cosmos DB for NoSQL provides the widest variety of SDK options for developers in your organization. The NoSQL API also natively uses JSON documents, enabling your team to store a wide variety of data formats in your database.

Now that you completed this module, you can:

* Evaluate whether Azure Cosmos DB for NoSQL is the right database for your application.
* Describe how the features of the Azure Cosmos DB forNoSQL are appropriate for modern applications.

### Learn more

For more information about the subjects discussed in this module, see:

* [Azure Cosmos DB resource model](/en-us/azure/cosmos-db/account-databases-containers-items)
* \[Azure Cosmos DB vector database]\[/azure/cosmos\-db/vector\-database]
* [Choose an API in Azure Cosmos DB](/en-us/azure/cosmos-db/choose-api)
* [Partitioning and horizontal scaling in Azure Cosmos DB \| Choosing a partition key](/en-us/azure/cosmos-db/partitioning-overview#choose-partitionkey)
* \[Azure Cosmos DB .NET SDK for NoSQL]\[/azure/cosmos\-db/nosql/sdk\-dotnet\-v3]
* \[Azure Cosmos DB Java SDK for NoSQL]\[/azure/cosmos\-db/nosql/sdk\-java\-v4]
* [Azure Cosmos DB Node.js SDK for NoSQL](/en-us/azure/cosmos-db/nosql/sdk-nodejs)
* [Azure Cosmos DB Python SDK for NoSQL](/en-us/azure/cosmos-db/nosql/sdk-python)
* [Azure Cosmos DB GO SDK for NoSQL](/en-us/azure/cosmos-db/nosql/sdk-go)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-cosmos-db-sql-api/_

## Fuentes
- [Introduction to Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/introduction-to-azure-cosmos-db-sql-api/?WT.mc_id=api_CatalogApi)
