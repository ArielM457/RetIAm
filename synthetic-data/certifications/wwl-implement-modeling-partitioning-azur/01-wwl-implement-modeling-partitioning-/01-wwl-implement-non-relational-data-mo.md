# Implement a non-relational data model

> Curso: Implement a data modeling and partitioning strategy for Azure Cosmos DB for NoSQL (wwl-implement-modeling-partitioning-azure-cosmos-d) · Seccion: Implement a data modeling and partitioning strategy for Azure Cosmos DB for NoSQL
> Duracion estimada: 57 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Cosmos DB is Microsoft's fully managed NoSQL database on Azure. As a NoSQL database, Azure Cosmos DB is both nonrelational and horizontally scalable or scales out. This ability to scale out is achieved by adding more nodes, or partitions, to a container.

This ability to scale out allows containers to grow to a theoretically infinite size. So as a container grows in size, the container can also handle increasing numbers of requests, providing the same performance regardless of how large the container gets.

However, to achieve this level of scalability, users need to understand the concepts and techniques unique to Azure Cosmos DB for modeling and partitioning data. The users also need to understand as the concepts for NoSQL databases in general.

### Scenario

Imagine that you work for a retail startup that's designing a database to manage online orders. You're working on a proposal for an efficient database design using Azure Cosmos DB for NoSQL. You are provided with an entity\-relationship model to start from. You want to provide the maximum scalability, performance, and efficiency possible and to achieve this task so the data needs to be modeled correctly.

The following entity\-relationship diagram (ER model) provides you with the details of the nine entities you expect to work with. The relational model has nine entities in their own tables.

### How do we accomplish this?

In this module, we take our existing relational data model and redesign it as a NoSQL database for our e\-commerce application. During this process, you learn the following concepts:

* **Differences between relational versus NoSQL databases**: You explore some of the differences between NoSQL databases and relational databases and why they're that way.
* **Using application data access patterns to model data**: You learn how understanding the way an application reads and writes data influences how to model it for a NoSQL database.
* **Embedding versus referencing**: You learn when you should embed data within the same document versus when you should store data as a separate document.
* **Choosing a partition key**: You learn key concepts needed for choosing the best partition key to achieve the ability to scale out, and optimize workloads that are either read or write heavy, or both.
* **Modeling lookup or reference data**: Finally, you learn how to model data that's used as a lookup or reference for other data.

### What is the main goal?

When you finish this module (and the companion module, *Optimize your database by using advanced modeling patterns for Azure Cosmos DB*), you'll have the knowledge and skills to properly model and partition data for a NoSQL database deployed on Azure Cosmos DB.

After completing this module, you’ll be able to:

* Determine access patterns for data.
* Apply data model and partitioning strategies to support an efficient and scalable NoSQL database.

---

## What's the difference between NoSQL and relational databases?

Azure Cosmos DB is characterized as being both nonrelational and horizontally scalable.

### Horizontal scale versus vertical scale

Relational databases typically grow by increasing the size of the VM or compute that they're hosted on. NoSQL databases like Azure Cosmos DB scale by adding more servers or nodes. This is known as scale\-out. These nodes are also known as physical partitions in Cosmos DB. Data stored on these physical partitions needs to be organized so that it can be efficiently accessed later.

Data is routed to different physical partitions by using the value of a required property on each document. This property is called a container's *partition key*, this partition key needs to be specified when creating the container. Passing the partition key when data is written or read from a container ensures that operations are efficient by only directing the request to the partition it is stored on.

Although the need for a partition key might appear to be constraint, it has some enormous benefits. Typically, relational database possibly will grow to less than 100 TB at most. A NoSQL database can grow to unlimited size, and can do so without any impact on response times when it's accessing data from any single partition.

Additionally, as partitions are added, so too is more compute added and the amount of processing that is supported by the database simultaneously grows. This means that it can support more concurrent users as well. Also with no impact on performance.

### Nonrelational versus relational databases

The second defining characteristic of a NoSQL database is that there are no foreign keys, constraints, or enforced relationships of any kind between pieces of data. Because data in a NoSQL database is stored on different physical servers, enforcing constraints or relationships, or placing locks on data would result in negative or unpredictable performance.

However, not having enforced relationships doesn't mean that you can't manage entities that have relationships in a NoSQL database, it just means that you need to do it differently.

### Why are these database types so different?

Understanding how the economics of computing has changed since relational databases were first introduced can help explain why these two types of databases are so different.

When relational databases were invented in 1970, the costs of storage and memory were high relative to compute. The goal of normalizing a database model was to reduce duplicate data and thus cost within a database. The database engine would apply locks and latches to enforce strict ACID (atomicity, consistency, isolation, durability) semantics as it performed operations on all the needed pieces of data together. The locks on data ensured consistent data, but with trade\-offs in concurrency, latency, and availability.

Today, the cost of storage and memory is relatively cheap compared to compute, thus, to be cost effective we no longer need optimize for storage efficiency. With workloads requiring increasing levels of concurrency and availability and lower latencies, there was a need for a new type of database that's optimized for these requirements, and so NoSQL databases were born.

It is also for these reasons, that one of the goals in modeling data for a NoSQL database is to do so in a manner that ensures reading or writing data is compute\-efficient. In\-part because relational operators like cross\-document joins don't exist in NoSQL databases, data must be stored as the application uses it for it to be the most efficient. Often data needs to be denormalized, duplicated, or otherwise stored in a way that breaks many of the relational normalization rules that are used for relational data modeling.

### Can you use NoSQL for relational workloads?

At this point, you might be wondering whether NoSQL databases are appropriate to use for relational workloads. And the answer is yes! NoSQL databases can absolutely be used for workloads where relationships between different entities exist.

NoSQL databases are often used when a relational database can't meet the desired performance, scale, or availability needs of the application.

The techniques for designing a NoSQL database are different from the techniques for modeling data for a relational database. These techniques are also not intuitive for someone with a background in relational database design. Some of the best practices that you learn for building relational databases are often antipatterns when you're designing for a NoSQL database.

For the rest of this module and in the advanced modeling module, we'll step you through the techniques that are used to model data in a manner that will result in a high\-performance NoSQL database.

---

## Identify access patterns for your app

When you're designing a data model for a NoSQL database, the objective is to ensure that operations on data are done in the fewest requests. To do this, you need to understand the relationships between the data and how data will be accessed by the application. These access patterns are important because they, along with the relationships, will determine how the properties of the various entities are grouped together and stored in documents within containers in Azure Cosmos DB for NoSQL.

In Azure Cosmos DB for NoSQL, documents are called items and containers are often synonymously referred to as collections.

### Identify access patterns for customer entities

Let's start with the customer entities in our e\-commerce database. The following diagram shows three entities and the relationships between them. The three entities are **Customer**, **CustomerAddress**, and **CustomerPassword**. The **Customer** entity has a 1:Many relationship to **CustomerAddress**. **Customer** has a 1:1 relationship to **CustomerPassword**.

In our application, we'll perform three operations on the customer entities:

* **Create a customer**: When a new user first visits the e\-commerce site, a new customer will be created.
* **Update a customer**: When an existing user updates their profile information, their customer record will be updated.
* **Retrieve a customer**: When an existing user visits the site, they'll sign in with their password. During that same session, they'll need to access other customer data (such as address) to purchase new items.

For each of these operations, we need all this data at the same time. If they were modeled as separate documents, it would require multiple round trips to the server to create, update, and retrieve the customer data. This is inefficient.

### Model customer entities

Azure Cosmos DB stores data as JSON, so we can model the 1:Many relationship between **Customer** and **CustomerAddress** and embed the customer address data as an array. For the 1:1 relationship between **Customer** and **CustomerPassword**, we can embed that as an object in our new single customer document. Then the e\-commerce application can create, edit, or retrieve customer data in a single request.

The following diagram shows what our customer entity looks like.

---

## When to embed or reference data

In the previous unit, we embedded the customer address and password data into a new customer document. That action reduces the number of requests, which improves performance and reduces cost. However, you can't always embed data. There are rules for when you should embed data in a document instead of referencing it in a different row.

### When should you embed data?

Embed data in a document when the following criteria apply to your data:

* **Read or updated together**: Data that's read or updated together is nearly always modeled as a single document. This reduces the number of requests which is our objective in being efficient. In our scenario, all of the customer entities are read or written together.
* **1:1 relationship**: For example, **Customer** and **CustomerPassword** have a 1:1 relationship.
* **1:Few relationship**: In a NoSQL database, it's necessary to distinguish 1:Many relationships as bounded or unbounded. **Customer** and **CustomerAddress** have a bounded 1:Many relationship because customers in an e\-commerce application normally have only a handful of addresses to ship to. When the relationship is bounded, this is a 1:Few relationship.

### When should you reference data?

Reference data as separate documents when the following criteria apply to your data:

* **Read or updated independently**: This is especially true where combining entities that would result in large documents. Updates in Azure Cosmos DB require the entire item to be replaced. If a document has a few properties that are frequently updated alongside a large number of mostly static properties, it's much more efficient to split the document into two. One document then contains the smaller set of properties that are updated frequently. The other document contains the static, unchanging values.
* **1:Many relationship**: This is especially true if the relationship is unbounded. If you have a document which increases in size an unknown or unlimited amount of times, the cost and latency for those updates will keep increasing. This is due to the increasing size of the update costing more RU/s and the payloads going over the network which itself, is also inefficient.
* **Many:Many relationship**: We'll explore an example of this relationship in a later unit with product tags.

Separating these properties reduces throughput consumption for more efficiency. It also reduces latency for better performance.

---

## Exercise: Measure performance for customer entities

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

## Choose a partition key

Remember that data in JSON documents is stored in Azure Cosmos DB databases within containers that are in turn distributed across physical partitions and where the data is routed to the appropriate physical partition based on the value of a partition key.

The partition key is a required document property that ensures documents with the same partition key value are routed to and stored within a specific physical partition. A physical partition supports a fixed maximum amount of storage and throughput (RU/s). Azure Cosmos DB automatically distributes the logical partitions across the available physical partitions, again using the partition key value to do so in a predictable way.

In this unit, you'll learn more about logical partitions and how to avoid hot partitions. This information will help us choose the appropriate partition key for the customer data in our scenario.

In Azure Cosmos DB, you increase storage and throughput by adding more physical partitions to access and store data. The maximum storage size of a physical partition is 50 GB, and the maximum throughput is 10,000 RU/s.

### Logical partitions in Azure Cosmos DB

A logical partition is an abstraction above the underlying physical partitions. Multiple logical partitions can be stored within a single physical partition. A container can have an unlimited number of logical partitions. Individual logical partitions are moved to new physical partitions as they grow in size to ensure optimum storage utilization and growth. Moving logical partitions as a unit ensures that all documents within it reside on the same physical partition. The maximum size for a logical partition is 20 GB. Using a partition key with high cardinality allows you to avoid this 20\-GB limit by spreading your data across a larger number of logical partitions. You can also use hierarchical partition keys which organize partition key values in a hierarchy to avoid this limit. These are covered in another learning path.

A partition key provides a way to route data for a logical partition. It's a property that exists within every document in your container that routes your data. A container is another abstraction for all data stored with the same partition key. The partition key is defined when you create a container.

In the following example, the container has a partition key of `/username`.

### Avoid hot partitions

When you're modeling data for Azure Cosmos DB, it's critically important that the partition key that you choose results in an even distribution of data and requests across both logical and by extension, the physical partitions in your container. This is especially true when containers grow larger and have an increasing number of physical partitions.

If you don't test the design of your database under load during development, a poor choice for partition key might not be revealed until the application is in production and significant data has already been written.

When data is not partitioned correctly, it can result in *hot partitions*. Hot partitions prevent your application workload from scaling, and they can occur on both storage and throughput.

#### Storage hot partitions

A hot partition on storage occurs when you have a partition key that results in highly asymmetric storage patterns. As an example, consider a multitenant application that uses TenantId as its partition key with six tenants: A to F. Tenants B,C,E and F are very small, Tenant D has a little more data. However Tenant A is massive and quickly hits the 20\-GB limit for its partition. In this scenario, we need to select a different partition key that will spread the storage across more logical partitions.

#### Throughput hot partitions

Throughput can suffer from hot partitions when most or all of the requests go to the same logical partition.

It's important to understand the access patterns for your application to ensure that requests are spread as evenly as possible across partition key values. When throughput is provisioned for a container in Azure Cosmos DB, it's allocated evenly across all the physical partitions within a container.

As an example, if you have a container with 30,000 RU/s, this workload is spread across the three physical partitions for the same six tenants mentioned earlier. So each physical partition gets 10,000 RU/s. If tenant D consumes all of its 10,000 RU/s, it will be rate limited because it can't consume the throughput allocated to the other partitions. This results in poor performance for tenant C and D, and leaving unused compute capacity in the other physical partitions and remaining tenants. Ultimately, this partition key results in a database design where the application workload can't scale.

When data and requests are spread evenly, the database can grow in a way that fully utilizes both the storage and throughput. The result will be the best possible performance and highest efficiency. In short, the database design will scale.

### Consider reads versus writes

When you're choosing a partition key, you also need to consider whether the data is read heavy or write heavy. You should seek to distribute write\-heavy requests with a partition key that has high cardinality.

For read\-heavy workloads, you should ensure that queries are processed by one or a limited number of partitions by including an `WHERE` clause with an equality filter on the partition key, or an IN operator on a subset of partition key values in your queries.

In scenarios where the application workload is both write heavy and read heavy, there is a solution. We'll explore that in the next module.

The following illustration shows a container that's partitioned by username. This query will hit only a single logical partition, so its performance will always be good.

A query that filters on a different property, such as `favoriteColor`, would "fan out" to all partitions in the container. This is also known as a *cross\-partition query*. Such a query will perform as expected when the container is small and occupies only a single partition. However, as the container grows and there are increasing number of physical partitions, this query will become slower and more expensive because it will need to check every partition to get the results whether the physical partition contains data related to the query or not.

### Choose a partition key for customers

Now that you understand partitioning in Azure Cosmos DB, we can decide on a partition key for our customer data. As we covered earlier, we perform three operations on customers: create a customer, update a customer, and retrieve a customer. In this case, we'll retrieve the customer by their *id*. Because that operation will be called the most, it makes sense to make the customer's ID the partition key for the container.

You might worry here that making the ID the partition key means that we'll have as many logical partitions as there are customers, with each logical partition containing only a single document. Millions of customers would result in millions of logical partitions.

But this is perfectly fine! Logical partitions are a virtual concept, and there's no limit to how many logical partitions you can have. Azure Cosmos DB will collocate multiple logical partitions on the same physical partition. As logical partitions grow in number or in size, Cosmos DB will move them to new physical partitions when needed.

---

## Summary

In this module, you learned key concepts and techniques for modeling and partitioning data for NoSQL databases like Azure Cosmos DB. We applied these to our e\-commerce application that we needed to migrate from a relational database to a NoSQL database. The things that you learned in this module include:

* **Differences between relational versus NoSQL databases**: You learned how NoSQL databases like Azure Cosmos DB are horizontally scalable, whereas relational databases are typically vertically scalable.
* **Using access patterns to model data**: You learned how understanding an application's access patterns to data plays an important role in how to model and partition data.
* **Embedding versus referencing**: You learned when you should embed different entities within the same document versus when you should reference the data and store it as separate rows.
* **Choosing a partition key**: You learned key concepts for choosing a partition key. These concepts include how to avoid hot partitions and how to handle workloads that are both read and write heavy.
* **Modeling lookup or reference data**: Finally, you learned how to model data that's used as a lookup or reference for other data.

We applied all of these concepts and techniques to a relational database to model it for a NoSQL database. We modeled the three customer entities and embedded them in a single document. This resulted in an increase in performance by reducing the number of requests for the data.

We also modeled the product category and product tag entities. And we used a special technique to reduce the overall storage and throughput required for small lookup tables.

Now that you have completed this module, you can:

* Determine access patterns for data.
* Apply data model and partitioning strategies to support an efficient and scalable NoSQL database.

### Learn more

* [Understanding the differences between NoSQL and relational databases](/en-us/azure/cosmos-db/relational-nosql)
* [Data modeling in Azure Cosmos DB](/en-us/azure/cosmos-db/modeling-data)
* [How to model and partition data on Azure Cosmos DB using a real\-world example](/en-us/azure/cosmos-db/how-to-model-partition-example)
* [Partitioning and horizontal scaling in Azure Cosmos DB](/en-us/azure/cosmos-db/partitioning-overview)
* [Partitioning strategy and provisioned throughput costs](/en-us/azure/cosmos-db/optimize-cost-throughput#partitioning-strategy-and-provisioned-throughput-costs)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/_

## Fuentes
- [Implement a non-relational data model](https://learn.microsoft.com/en-us/training/modules/implement-non-relational-data-model/?WT.mc_id=api_CatalogApi)
