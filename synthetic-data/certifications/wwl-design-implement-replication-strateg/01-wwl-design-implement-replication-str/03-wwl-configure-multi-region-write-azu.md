# Configure multi-region write in Azure Cosmos DB for NoSQL

> Curso: Design and implement a replication strategy for Azure Cosmos DB for NoSQL (wwl-design-implement-replication-strategy-cosmos-d) · Seccion: Design and implement a replication strategy for Azure Cosmos DB for NoSQL
> Duracion estimada: 41 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

With Azure Cosmos DB, you can enable global scale for both read and write throughput. The multi\-write feature in Azure Cosmos DB makes it possible for every region to be writable so that you can elastically scale your write\-heavy workloads across the globe. In this module, you will explore the multi\-write functionality in Azure Cosmos DB and how to use it with the .NET SDK for Azure Cosmos DB for NoSQL.

After completing this module, you'll be able to:

* Configure Azure Cosmos DB for multi\-region write
* Use the Azure Cosmos DB for NoSQL .NET SDK to select a write region for operations.

---

## Understand multi\-region write

With Azure Cosmos DB, every region supports both writes and reads. Enabling the ability to write to any region is a turnkey operation that doesn’t interrupt the application’s availability. With the combination of Azure Cosmos DB’s global geo\-replication functionality, and the ability to write to any region, Azure Cosmos DB can be used in application scenarios with significant write performance and scalability demands.

In practice, an account with multi\-region writes enabled has stronger write guarantees than a single\-region account or a single writable region account.

With multi\-region write enabled, many of the features associated with a single\-region Azure Cosmos DB account are still available:

* Sliding scale of well\-defined consistency models
* Low latency write operations across the globe
* High availability with financially backed SLA

Note

Strong consistency is not supported in a multi\-region write scenario.

In the event of a data center outage, accounts with multiple write\-regions will continue to be available for read and write operations as the SDK will automatically attempt requests at another region from the preferred regions list.

Multi\-region write can be configured using the Azure CLI, PowerShell, code, Azure Resource Manager templates (JSON/Bicep), or the Azure portal.

Once the multiple write\-region functionality is enabled, all replica regions associated with the account will automatically become writable regions.

---

## Configure multi\-region support in the SDK

In the .NET SDK for Azure Cosmos DB for NoSQL, configuring the preferred region to write to be a matter of selecting between two different properties in the **CosmosClientOptions** object.

Tip

If you do not specify a preferred region, the SDK will automatically default to the primary region for your account. The primary region is the first region in the region list, and is typically the region you selected first when you created the Azure Cosmos DB account.

### Selecting a single write region

The **ApplicationRegion** property specifies which region you want the SDK to use for its operations. Effectively, this region is the writable region you use. In this example, the selected region is **West US**.

```
CosmosClientOptions options = new()
{
    ApplicationRegion = Regions.WestUS
};

TokenCredential managedIdentityCredential = new ManagedIdentityCredentialBuilder()
    .clientId("<your-managed-identity-client-id>")
    .build();

using CosmosClient client = new CosmosClient("<your-cosmos-endpoint>", managedIdentityCredential, options);

```

You can also use the **CosmosClientBuilder** to configure the preferred region.

```
using CosmosClient client = builder
    .WithApplicationRegion(Regions.WestUS)
    .Build();

```

Once the client connects to Azure Cosmos DB, the client pulls a list of available regions and prioritizes them based on proximity from the region you chose. If the region you selected isn't available, the client tries the alternative regions in the established order.

### Building a preferred write regions list

If you want to create your own prioritized list of regions to attempt read and write operations, you can use the **ApplicationPreferredRegions** property. In the first example, this property is set to a list of three regions in a custom prioritization.

```
CosmosClientOptions options = new()
{
    ApplicationPreferredRegions = new List<string>
    {
        Regions.WestUS,
        Regions.AustraliaSoutheast,
        Regions.NorthEurope
    }
};

TokenCredential managedIdentityCredential = new ManagedIdentityCredentialBuilder()
    .clientId("<your-managed-identity-client-id>")
    .build();

using CosmosClient client = new CosmosClient("<your-cosmos-endpoint>", managedIdentityCredential, options);

```

Again, this same example could be implemented using the **CosmosClientBuilder** class.

```
using CosmosClient client = builder
    .WithApplicationPreferredRegions(
        new List<string>
        {
            Regions.WestUS,
            Regions.AustraliaSoutheast,
            Regions.NorthEurope
        }
    )
    .Build();

```

---

## Understand conflict resolution policies

Out of the box, Azure Cosmos DB’s multi\-region write feature has automatic conflict management built in. Conflicts can occur when clients concurrently update the same item in multiple regions. There are three types of conflicts:

| **Type** | **Description** |
| --- | --- |
| **Insert** | This conflict occurs when more than one item is inserted simultaneously with the same unique identifier in multiple regions |
| **Replace** | Replace conflicts occur when multiple client applications update the same item concurrently in separate regions |
| **Delete** | Delete conflicts occurs when a client is attempting to update an item that has been deleted in another region at the same time |

The default conflict resolution policy in Azure Cosmos DB is **Last Write Wins**. This policy uses the timestamp (\_ts) to determine which item wrote last. In simple terms, if multiple items are in conflict, the item with the largest value for the **\_ts** property will win. In the case of a delete conflict, the operation to delete an item will always win out over other operations.

While the **\_ts** property is the default for the Last Write Wins policy, you can configure any numeric property for this policy by configuring a *conflict resolution path*. You can use the .NET SDK for Azure Cosmos DB for NoSQL to configure the custom conflict resolution path.

In this example, a new container named **products** is created with a custom conflict resolution path of **/sortableTimestamp**.

```
Database database = client.GetDatabase("cosmicworks");

ContainerProperties properties = new("products", "/categoryId")
{
    ConflictResolutionPolicy = new ConflictResolutionPolicy()
    {
        Mode = ConflictResolutionMode.LastWriterWins,
        ResolutionPath = "/sortableTimestamp",
    }
};

Container container = database.CreateContainerIfNotExistsAsync(properties);

```

Note

You can only set a conflict resolution policy on newly created containers.

---

## Create custom conflict resolution policy

There may be times when you wish to write your own logic to resolve conflicts between items. This can be accomplished by using a Custom conflict resolution policy.

A custom resolution policy will use a stored procedure to resolve conflicts between items in different regions. All custom stored procedures must be implemented with the following JavaScript function signature.

```
function <function-name>(incomingItem, existingItem, isTombstone, conflictingItems)

```

Each of these four parameters is required in the function:

| **Parameter** | **Description** |
| --- | --- |
| **existingItem** | The item that is already committed |
| **incomingItem** | The item that's being inserted or updated that generated the conflict |
| **isTombstone** | Boolean indicating if the incoming item was previously deleted |
| **conflictingItems** | Array of all committed items in the container that conflict with incomingItem |

An example implementation of a stored procedure to resolve conflict by using the **/metadata/sortableTimestamp** would include the following code.

```
function resolveConflicts(incomingItem, existingItem, isTombstone, conflictingItems) {
  if (!incomingItem) {
    if (existingItem) {
      __.deleteDocument(existingItem._self, {});
    }
  } else if (isTombstone) {
  } else {
    if (existingItem) {
      if (incomingItem.metadata.sortableTimestamp > existingItem.metadata.sortableTimestamp) {
        return;
      }
    }
    var i;
    for (i = 0; i < conflictingItems.length; i++) {
      if (incomingItem.metadata.sortableTimestamp > conflictingItems[i].metadata.sortableTimestamp) {
        return;
      }
    }
    delete (conflictingItems, incomingItem, existingItem);
  }

  function delete (documents, incoming, existing) {
    if (documents.length > 0) {
      __.deleteDocument(documents[0]._self, {}, function (err, responseOptions) {
        documents.shift();
        delete (documents, incoming, existing);
      });
    } else if (existing) {
      __.replaceDocument(existing._self, incoming);
    } else {
      __.createDocument(collection.getSelfLink(), incoming);
    }
  }
}

```

You can use the .NET SDK for Azure Cosmos DB for NoSQL to configure the custom conflict resolution policy. To start this example, a container named **products** will be created with a custom conflict resolution policy.

```
string databaseName = "cosmicworks";
string containerName = "products";
string partitionKey = "/categoryId";
string sprocName = "resolveConflicts";

Database database = client.GetDatabase(databaseName);

ContainerProperties properties = new(containerName, partitionKey)
{
    ConflictResolutionPolicy = new ConflictResolutionPolicy()
    {
        Mode = ConflictResolutionMode.Custom,
        ResolutionProcedure = $"dbs/{databaseName}/colls/{containerName}/sprocs/{sprocName}",
    }
};

Container container = database.CreateContainerIfNotExistsAsync(properties);

```

Finally, a stored procedure named **resolveConflicts** is created to support the conflict resolution policy.

```
StoredProcedureProperties properties = new (sprocName, File.ReadAllText(@"code.js"))

await container.Scripts.CreateStoredProcedureAsync(properties);

```

Alternatively, a custom conflict resolution policy can be configured without a stored procedure. In this scenario, conflicts are written to a conflicts feed. Your application code can then manually resolve conflicts in the feed.

Using .NET you can configure a container for manual conflict resolution using this code sample.

```
Database database = client.GetDatabase("cosmicworks");

ContainerProperties properties = new("products", "/categoryId")
{
    ConflictResolutionPolicy = new ConflictResolutionPolicy()
    {
        Mode = ConflictResolutionMode.Custom
    }
};

Container container = database.CreateContainerIfNotExistsAsync(properties);

```

---

## Summary

In this module, you explored how to configure the .NET SDK to support multi\-region writes to a specific preferred region

Now that you have completed this module, you can:

* Enable multi\-region write on an Azure Cosmos DB account
* Select a preferred write region in the .NET SDK for Azure Cosmos DB for NoSQL

### Learn more

For more information about the topics discussed in this module, see:

* [Configure multi\-region writes in your applications that use Azure Cosmos DB](/en-us/azure/cosmos-db/how-to-multi-master)
* [Conflict types and resolution policies when using multiple write regions](/en-us/azure/cosmos-db/conflict-resolution-policies)
* [Manage conflict resolution policies in Azure Cosmos DB](/en-us/azure/cosmos-db/how-to-manage-conflicts)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/_

## Fuentes
- [Configure multi-region write in Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/configure-multi-region-write-azure-cosmos-db-sql-api/?WT.mc_id=api_CatalogApi)
