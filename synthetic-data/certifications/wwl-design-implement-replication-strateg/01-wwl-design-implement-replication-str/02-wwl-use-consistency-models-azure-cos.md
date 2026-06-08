# Use consistency models in Azure Cosmos DB for NoSQL

> Curso: Design and implement a replication strategy for Azure Cosmos DB for NoSQL (wwl-design-implement-replication-strategy-cosmos-d) · Seccion: Design and implement a replication strategy for Azure Cosmos DB for NoSQL
> Duracion estimada: 36 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

As a distributed database, Azure Cosmos DB offers a sliding scale of consistency options that can map to your application’s needs much closer than the binary (strong/weak consistency) option provided by many data platforms. In this module, you will explore the consistency options in Azure Cosmos DB and how they can be configured.

After completing this module, you'll be able to:

* Configure default consistency level for an Azure Cosmos DB account
* Change the consistency level on a per\-request basis

---

## Understand consistency models

In a distributed database system when data is replicated over a wide area network to other regions to provide higher availability or lower read latency for users, tradeoffs must be made either on the data being completely consistent across the database or in higher write latency as data is synchronously committed to the other regions.

Azure Cosmos DB offers a sliding scale of consistency with many options between the traditional strong and weak options provided by other data storage solutions.

Each of the five consistency levels is well\-defined with clear tradeoffs when compared with each other:

| **Consistency Level** | **Description** |
| --- | --- |
| **Strong** | Linear consistency. Data is replicated and committed in all configured regions before acknowledged as committed and visible to all clients. |
| **Bounded Staleness** | Reads lag behind writes by a configured threshold in time or items. |
| **Session** | Within a specific session (SDK instance), users can read their own writes. |
| **Consistent Prefix** | Reads may lag behind writes, but reads will never appear out of order. |
| **Eventual** | Reads will eventually be consistent with writes. |

### Strong consistency

Strong consistency guarantees that all read operations will return the most recent version of the item. Client applications will never read an outdated item due to latency or inconsistency. Write operations are not fully committed until they are ready in all other regions.

This characteristic causes strong consistency to have the highest latency as it must wait for commits to replicate across large geographical distances.

### Bounded Staleness consistency

Bounded staleness is similar to Strong consistency except that reads are allowed to lag behind writes up to a defined threshold. That threshold could be defined as:

* **K** versions of an item lag behind the writes
* **T** time interval lag behind the writes

Bounded staleness is a good compromise for applications that want low write latency but need to enforce consistency up to a reasonable threshold.

Tip

Bounded staleness provides strong consistency guarantees within the region in which data is written.

### Session consistency

Session consistency provides read your own write guarantees within a single client session or where the session token is passed between the SDK and client. Outside of that, the consistency guarantee is relaxed to either Consistent Prefix or Eventual consistency.

Session consistency is a great option for applications where the end users may be confused if they cannot immediately see any transaction they just made.

### Consistent Prefix consistency

Consistent Prefix consistency allows for looser consistency and higher performance while guaranteeing that reads, which lag behind the writes, will appear in order in which they were written.

Consistent Prefix consistency is ideal for applications where the order of read operations matters more than the latency.

### Eventual consistency

Eventual consistency is the weakest form of consistency where reads lag behind writes and reads may appear out of order. However, eventual consistency will have the lowest write latency, highest availability, and potential for most read scalability compared to other options.

Eventual consistency is a good option for applications that don't require any linear or consistency guarantees.

---

## Configure default consistency model in the portal

Each new Azure Cosmos DB account has a default consistency level of Session. In the Azure portal, the Default consistency pane is used to configure a new default consistency level for the entire account.

All reads and queries issued against containers in the account will use the default consistency level.

---

## Change consistency model with the SDK

The **ItemRequestOptions** class contains configuration properties to modify a specific request. Using this class, you can relax the current default consistency level to a weaker one.

For example, a new variable illustrated here, named **options,** contains a **ConsistencyLevel** property configured to the weakest consistency level.

```
ItemRequestOptions options = new()
{ 
    ConsistencyLevel = ConsistencyLevel.Eventual 
};

```

Now, the options variable can be added to any operation request. In this example, a request is made to read an item from the container. The **ReadItemAsync** method has an extra parameter to accept the options variable.

```
string id = "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009";

string categoryId = "9603ca6c-9e28-4a02-9194-51cdb7fea816";
PartitionKey partitionKey = new (categoryId);

Product item = await container.ReadItemAsync<Product>(id, partitionKey, requestOptions: options);

```

Note

The consistency level can only be relaxed on a per\-request basis, not strengthened.

As an alternative, you can relax the consistency for the entire **CosmosClient** instance using the **CosmosClientOptions** class.

```
CosmosClientOptions options = new()
{
    ConsistencyLevel = ConsistencyLevel.Eventual 
};

CosmosClient client = new (endpoint, key, options);

```

---

## Use session tokens

When session consistency is selected, consistency is managed using a session token. This token is then passed back\-and\-forth between Azure Cosmos DB and the client to ensure that clients get read your own write guarantees.

Using the .NET SDK classes, the session token can be manually extracted and passed back to the Azure Cosmos DB resource.

Tip

Typically, the .NET SDK automatically manages session tokens for you. You will not need to implement this code in most applications.

In this example, a new item is created. The response class contains a **Headers** property with a specific **Session** header, which contains the session token in string format.

```
ItemResponse<Product> response = await container.CreateItemAsync<Product>(item);
string token = response.Headers.Session;

```

Future requests can use the **ItemRequestOptions** class to configure the session token. This example illustrates a request to read a new item while still honoring the session token.

```
ItemRequestOptions options = new()
{
    SessionToken = token
};
ItemResponse<Product> readResponse = container.ReadItemAsync<Product>(id, partitionKey, requestOptions: options);)

```

Tip

Session tokens can be manually pulled out of a client and used on another client to preserve a session between multiple clients.

---

## Exercise: Configure consistency models in the portal and the Azure Cosmos DB for NoSQL SDK

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

In this module, you learned how to evaluate, implement, and override consistency levels in an Azure Cosmos DB account. Selecting the right consistency level is the key to ensuring that Azure Cosmos DB behaves in a manner that is ideal for your workload or application.

Now that you have completed this module, you can:

* Configure the default consistency level and override it on a per\-request basis
* Evaluate the consistency levels and select the correct one for your application

### Learn more

For more information about the topics discussed in this module, see:

* [Consistency levels in Azure Cosmos DB](/en-us/azure/cosmos-db/consistency-levels)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/_

## Fuentes
- [Use consistency models in Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/use-consistency-models-azure-cosmos-db-sql-api/?WT.mc_id=api_CatalogApi)
