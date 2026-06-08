# Configure replication and manage failovers in Azure Cosmos DB

> Curso: Design and implement a replication strategy for Azure Cosmos DB for NoSQL (wwl-design-implement-replication-strategy-cosmos-d) · Seccion: Design and implement a replication strategy for Azure Cosmos DB for NoSQL
> Duracion estimada: 39 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Modern applications require a data platform that is always online and near end users. Azure Cosmos DB is globally distributed by its design\-allowing scenarios where data can be at data centers closer to end\-users and scenarios where data is still available despite regional outages. In this module, you'll explore the various replication options for Azure Cosmos DB.

After completing this module, you'll be able to:

* Distribute data across global data centers
* Configure automatic failover and do a manual failover
* Configure the Azure Cosmos DB for NoSQL .NET SDK to use a specific region

---

## Understand replication

Azure Cosmos DB supports turnkey global scale\-out using any of the available management tools (SDK, CLI, PowerShell, Azure portal, etc.). To better understand why scale\-out is so frictionless, it's ideal to discuss how replication works in Azure Cosmos DB.

At the minimal configuration, every container has a partition key path defined. This path points to a key\-value pair in each JSON item. The value of the partition key is then used to distribute data within a region. Effectively, each container in Azure Cosmos DB will distribute data using the partition key's value to various physical partitions within the same region.

But, a physical partition isn’t really a single physical machine or device. The actual implementation of a physical partition is as a replica set. A replica set is a group of replicas that can dynamically grow and shrink to meet the needs of the database platform.

Each replica set will have other geographically distant replica sets that manage the same partition keys if data is distributed globally. These replica sets can then forward data to other replica sets in different regions to create replica copies of the data.

An Azure Cosmos DB account replicates data within a region (local distribution) among different replica sets servicing various partition key values. Replica sets that manage the same partition key value are referred to as a partition set as they will forward data between each other (global distribution).

Note

The direction that data flows between replica sets is contingent on whether the account is configured with a single\-write region or with multi\-region write enabled.

---

## Distribute data across regions

Configuring global distribution in Azure Cosmos DB is a turnkey operation that is performed when an account is created or afterward.

### Configuring geo\-redundancy for a new account

In the creation wizard, the Basics tab will require you to select a location for the new Azure Cosmos DB account. This location is referred to as the primary region. If multi\-region write is not enabled, this location is the only location where you can perform write operations.

The creation wizard includes a Global Distribution tab where the geo\-redundancy option should be enabled to add additional geo\-redundant read\-only regions. Enabling this setting will add the Azure region pair as your first replica for your data in Azure Cosmos DB.

### Configuring geo\-redundancy for an existing account

For existing Azure Cosmos DB accounts, the Replicate data globally pane is used to add or remove regions. Each region is added using a map, and then replication only occurs once the changes are saved. This pane can also be used to remove existing regions where data is currently replicated.

---

## Define automatic failover policies

An Azure Cosmos DB account with a single write region can be susceptible to downtime if a complete data center outage ever occurs. While this is rare, many organizations like to have a contingency plan in place. In the context of Azure Cosmos DB, an automatic failover plan can transfer the write region to one of the read regions in the case of such an outage.

By default, automatic failover is not enabled for an Azure Cosmos DB account. Automatic failover must be enabled before defining a plan. Once enabled, the read regions can then be sorted by order of failover priority. After sorting, the new priority list can then be persisted and applied to the account.

As an illustrative example, an Azure Cosmos DB account is configured with a write region, **West US 2**, and two read regions of **East US** and **UK South**. The automatic failover priorities are provided in this table:

| **Region** | **Priority** |
| --- | --- |
| **West US 2** | (N/A \- write region) |
| **East US** | 1 |
| **UK South** | 2 |

If the **West US 2** region experiences a data center outage, the **East US** region will first become the new write region. If **East US** experiences an outage, then **UK South** will become the new write region.

---

## Perform manual failovers

As part of your organization’s disaster recovery exercises, you may wish to test the failover capabilities in Azure Cosmos DB. A manual failover can be invoked using the Azure portal to validate the entire process.

The failover process requires connectivity between the two regions to ensure that it will succeed and maintain consistency in the data. For this reason, a manual failover should not be triggered during a service\-wide Azure Cosmos DB outage.

---

## Configure SDK region

The .NET SDK for Azure Cosmos DB for NoSQL includes configuration classes that can be used with the **CosmosClient** class to configure which region you want the SDK to target for requests.

There are two ways to configure the SDK client:

* Use the **ApplicationRegion** property to configure a single region for requests
* Use the **ApplicationPreferredRegions** property to configure a list of preferred regions

### Setting an application region

The **CosmosClientOptions** class contains a set of configuration options for new SDK client instances. Using this class, you can configure the preferred region for your queries and read operations. In this example, the **ApplicationRegion** property is configured to **UK South**.

```
using Azure.Identity;
using Microsoft.Azure.Cosmos;

// Configure the account endpoint
string accountEndpoint = "https://<cosmos-account-name>.documents.azure.com:443/";

// Define the preferred application region
CosmosClientOptions options = new()
{
    ApplicationRegion = "UK South"
};

// Use DefaultAzureCredential for Microsoft Entra Managed Identity authentication
DefaultAzureCredential credential = new DefaultAzureCredential();

// Initialize CosmosClient with endpoint, credential, and options
CosmosClient client = new(accountEndpoint, credential, options);

```

Alternatively; you can use the **Microsoft.Azure.Cosmos.Regions** static class which includes built\-in string properties for various Azure regions.

```
using Azure.Identity;
using Microsoft.Azure.Cosmos;

// Configure the account endpoint
string accountEndpoint = "https://<cosmos-account-name>.documents.azure.com:443/";

// Define the preferred application region using the Regions static class
CosmosClientOptions options = new()
{
    ApplicationRegion = Regions.UKSouth
};

// Use DefaultAzureCredential for Microsoft Entra Managed Identity authentication
DefaultAzureCredential credential = new DefaultAzureCredential();

// Initialize CosmosClient with endpoint, credential, and options
CosmosClient client = new(accountEndpoint, credential, options);

```

As another alternative, you can use the **CosmosClientBuilder** fluent classes to construct a new client with the application region set.

```
using Azure.Identity;
using Microsoft.Azure.Cosmos.Fluent;

// Configure the account endpoint
string accountEndpoint = "https://<cosmos-account-name>.documents.azure.com:443/";

// Use DefaultAzureCredential for Microsoft Entra Managed Identity authentication
DefaultAzureCredential credential = new DefaultAzureCredential();

// Build the CosmosClient with the specified application region
CosmosClient client = new CosmosClientBuilder(accountEndpoint, credential)
    .WithApplicationRegion(Regions.UKSouth)
    .Build();

```

### Setting a list of preferred application regions

The **ApplicationPreferredRegions** property is used to set a prioritized list of geo\-replicated regions to use with the SDK. In this first example, a string collection is created with the region values of **East Asia**, **South Africa North**, and **West US**. This collection is then used to assign the **ApplicationPreferredRegions** property.

```
using Azure.Identity;
using Microsoft.Azure.Cosmos;
using System.Collections.Generic;

// Configure the account endpoint
string accountEndpoint = "https://<cosmos-account-name>.documents.azure.com:443/";

// Create a list of preferred regions
List<string> regions = new()
{
    "East Asia",
    "South Africa North",
    "West US"
};

// Define the CosmosClientOptions with the preferred regions
CosmosClientOptions options = new()
{
    ApplicationPreferredRegions = regions
};

// Use DefaultAzureCredential for Microsoft Entra Managed Identity authentication
DefaultAzureCredential credential = new DefaultAzureCredential();

// Initialize CosmosClient with endpoint, credential, and options
CosmosClient client = new(accountEndpoint, credential, options);

```

This example could also be simplified with the use of the **Regions** static class and the **CosmosClientBuilder**.

```
using Azure.Identity;
using Microsoft.Azure.Cosmos.Fluent;
using System.Collections.Generic;

// Configure the account endpoint
string accountEndpoint = "https://<cosmos-account-name>.documents.azure.com:443/";

// Use DefaultAzureCredential for Microsoft Entra Managed Identity authentication
DefaultAzureCredential credential = new DefaultAzureCredential();

// Build the CosmosClient with a list of preferred regions
CosmosClient client = new CosmosClientBuilder(accountEndpoint, credential)
    .WithApplicationPreferredRegions(new List<string>
    {
        Regions.EastAsia,
        Regions.SouthAfricaNorth,
        Regions.WestUS
    })
    .Build();

```

---

## Summary

In this module, you evaluated your options for global distribution using Azure Cosmos DB. You also used the .NET SDK to connect to a specific region and read data from a replica.

Now that you have completed this module, you can:

* Add and remove regions from your Azure Cosmos DB account
* Configure and test failover scenarios
* Read data from a specific region using the .NET SDK for Azure Cosmos DB for NoSQL

### Learn more

For more information about the topics discussed in this module, see:

* [Distribute your data globally with Azure Cosmos DB](/en-us/azure/cosmos-db/distribute-data-globally)
* [Manage an Azure Cosmos account using the Azure portal](/en-us/azure/cosmos-db/how-to-manage-database-account)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/_

## Fuentes
- [Configure replication and manage failovers in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/configure-replication-manage-failovers-azure-cosmos-db/?WT.mc_id=api_CatalogApi)
