# Try Azure Cosmos DB for NoSQL

> Curso: Get started with Azure Cosmos DB for NoSQL (wwl-get-started-azure-cosmos-db-sql-api) · Seccion: Get started with Azure Cosmos DB for NoSQL
> Duracion estimada: 32 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

The first step to getting started with Azure Cosmos DB is to create a new account. You will learn, here, the basic hierarchy of resources in an Azure Cosmos DB for NoSQL account and how to create an account along with those resources.

After completing this module, you'll be able to:

* Create a new Azure Cosmos DB for NoSQL account
* Create database, container, and item resources for an Azure Cosmos DB for NoSQL account

---

## Explore resources

An Azure Cosmos DB for NoSQL account is composed of a basic hierarchy of resources that include:

* An account
* One or more databases
* One or more containers
* Many items

Let's explore each item in this hierarchy.

### Account

Each tenant of the Azure Cosmos DB service is created by provisioning a database account. Accounts are the fundamental units of data distribution, high availability and security. At the account level, you can configure the region\[s] for your data in Azure Cosmos DB for NoSQL. Accounts also contain the globally unique DNS name used for API requests

### Database

A database is a logical unit of management for containers in Azure Cosmos DB for NoSQL. Within the database, you can find one or more containers.

### Container

Containers are the fundamental unit of scalability in Azure Cosmos DB for NoSQL. Typically, you provision throughput at the container level but can use Serverless as well. Azure Cosmos DB for NoSQL will automatically and transparently partition the data in a container using the document property you select as a partition key for the container. You can also optionally configure indexing policies or a default time\-to\-live value at the container level.

### Item\[s]

An Azure Cosmos DB for NoSQL resource container is a schema\-agnostic container of arbitrary user\-generated JSON items. The NoSQL API for Azure Cosmos DB stores individual documents in JSON format as items within the container. Azure Cosmos DB for NoSQL natively supports JSON files and can provide fast and predictable performance because write operations on JSON documents are atomic.

Tip

Containers can also store JavaScript based stored procedures, triggers and user\-defined\-functions (UDFs)

---

## Review basic operations

There are a few basic operations that you will need to perform anytime you create any Azure Cosmos DB for NoSQL account resource in Azure.

### Creating a new account

The first step to getting started with Azure Cosmos DB is to create a new account.

When creating a new account in the portal, you must first select an API for your workload. The API selection cannot be changed after the account is created. For the remainder of this section, we will assume that the NoSQL API has been selected.

Next, the Azure portal will use a step\-by\-step wizard with tabs for various configuration options. Here you can configure options such as:

* The globally unique name of your account
* The location (Azure region) for the account
* Capacity mode (provisioned throughput or serverless)

Note

Only the options in the **Basics** tab are required to create an Azure Cosmos DB account.

### Creating a new database

Databases are logical units of management in Azure Cosmos DB for NoSQL, and don't require much to create. You only need a unique database name within the account to create a new database.

Note

However, if you choose to provision throughput at the database level, configuring the database may require additional steps. This is explored deeper in other Azure Cosmos DB for NoSQL topics.

### Creating a new container

Containers are the primary unit of scalability in Azure Cosmos DB for NoSQL. When creating a container, you should specify:

* The parent database
* A unique name for the container with the database
* The path for the partition key value
* *Optional*: provisioned throughput if not using a Serverless account.

The Azure Cosmos DB service will automatically and transparently partition your data based on the value of the partition key for each individual item.

### Creating simple items

Once the database and container resources exist, you are ready to create your first item. In Azure Cosmos DB for NoSQL, an item is a JSON document.

Note

JavaScript Object Notation (JSON) is an open standard file format, and data interchange format, that uses human\-readable text to store and transmit data objects consisting of attribute–value pairs and array data types (or any other serializable value)

JSON is a language\-independent data format with well\-defined data types and near universal support across a diverse range of services and programing languages. Here is an example of a JSON document that could be an item in an Azure Cosmos DB account:

```
{
  "id": "0012D555-C7DE",
  "type": "customer",
  "fullName": "Franklin Ye",
  "title": null,
  "emailAddress": "fye@cosmic.works",
  "creationDate": "2014-02-05",
  "addresses": [
    {
      "addressLine": "1796 Westbury Drive",
      "cityStateZip": "Melton, VIC 3337 AU"
    },
    {
      "addressLine": "9505 Hargate Court",
      "cityStateZip": "Bellflower, CA 90706 US"
    }
  ],
  "password": {
    "hash": "GQF7qjEgMk=",
    "salt": "12C0F5A5"
  },
  "salesOrderCount": 2
}

```

---

## Exercise: Create an Azure Cosmos DB for NoSQL account

#### Set up environment

Note

To complete this exercise, you will need a [Microsoft Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) in which you have administrative access.

To set up the lab environment for this exercise, sign into your Azure subscription and follow these instructions to provision your Azure resources:

* **[Create an Azure resource group for the lab.](https://go.microsoft.com/fwlink/?linkid=2295043&azure-portal=true)**
* **[Set up your local lab environment.](https://go.microsoft.com/fwlink/?linkid=2294752)**
* **[Enable Azure resource providers.](https://go.microsoft.com/fwlink/?linkid=2294853&azure-portal=true)**

#### Complete the exercise

Launch the exercise and follow the instructions.

---

## Summary

In this module, you learned and performed the core operations that are necessary anytime you create an Azure Cosmos DB for NoSQL account. These core operations will be repeated often as you explore deeper concepts for the Azure Cosmos DB for NoSQL.

Now that you have completed this module, you can:

* Create a new Azure Cosmos DB account resource that uses the NoSQL API
* Create database and container resources using the Data Explorer
* Create item resources using the Data Explorer

### Learn more

For more information about the topics discussed in this module, see:

* [Quickstart: Create an Azure Cosmos account, database, container, and items from the Azure portal](/en-us/azure/cosmos-db/sql/create-cosmosdb-resources-portal)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/_

## Fuentes
- [Try Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/try-azure-cosmos-db-sql-api/?WT.mc_id=api_CatalogApi)
