# Design a data partitioning strategy

> Curso: Implement a data modeling and partitioning strategy for Azure Cosmos DB for NoSQL (wwl-implement-modeling-partitioning-azure-cosmos-d) · Seccion: Implement a data modeling and partitioning strategy for Azure Cosmos DB for NoSQL
> Duracion estimada: 51 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Cosmos DB is a fully managed Microsoft NoSQL database on Azure. As a NoSQL database, Azure Cosmos DB is both horizontally scalable and non\-relational. Horizontal scalability enables Azure Cosmos DB to grow well beyond the size of typical relational databases. Also, Azure Cosmos DB does not impose relational constraints on data, which means that Azure Cosmos DB can deliver predictable performance.

To achieve this level of scalability, it's important to understand the concepts, techniques, and technologies for modeling and partitioning data that are unique to NoSQL databases. It's also important to understand how relational concepts, such as maintaining referential integrity, are applied in a NoSQL world.

:

### Scenario

Imagine that you're working for a retail startup that's designing a database to manage online orders. You're working on a proposal for an efficient database design. You've been given a relational model to start from. To improve scalability, efficiency, and performance, you want to migrate the model to NoSQL. You've modeled most of the entities so far, but there are more entities to model and further optimizations to make.

### What will we be doing?

In this module, you'll complete the redesign of the NoSQL database for your e\-commerce application by modeling the product and sales\-order entities. During this process, you'll learn about and apply the following concepts:

* **Denormalization**: You'll apply this concept when you model your product data. You'll then measure the performance and cost difference between storing the data in a relational manner and modeling it for a NoSQL database.
* **Referential integrity**: You'll learn how to use a feature called *change feed* to maintain the referential integrity between data that's stored in two different containers. In our e\-commerce scenario, you'll see how to use change feed to automatically update all the products in a category when the name of the category is changed.
* **Combining entities**: You'll explore the concept of storing different entities in the same container and learn how to explain when this technique can be applied in a NoSQL model.
* **Denormalizing aggregates**: You'll apply a technique that can help improve performance on queries where you're frequently querying for aggregate values on data. The technique also helps in queries that require a subquery to first do a *group by and aggregate* and then do an *outer query*, with an *order by* on the results. This technique uses Azure Cosmos DB transaction capability and, as part of the process, you'll learn about an SDK feature called *transactional batch*.

### What is the main goal?

After you've finished this module and its companion module "Model and partition your data in Azure Cosmos DB," you'll have the knowledge and skills necessary to properly model and partition data for a NoSQL database, such as Azure Cosmos DB.

After completing this module, you’ll be able to:

* Manage relationships between data entities by using advanced modeling and partitioning strategies.
* Maintain the referential integrity of your data by using change feed.
* Implement pre\-aggregating and denormalizing data strategies to improve data\-model performance and scaling.
* Optimizing storage and compute by mixing entity types in a single container

---

## Denormalize data in your model

In this unit, you'll look at the product table from your relational database and model it for a NoSQL database. You'll also look at the *many\-to\-many* relationship your product table has with product tags.

### Model the product entities

Your initial model for the product table includes only the fields from your relational table. However, your e\-commerce application must display the product category name when you display a product page. You'll also want to query for products by product tags within a product category as well. This can be done in either of two ways: you can store products in a product tags container, or you can embed your tags in the product container.

Because there are far fewer tags per product than products per tag, it makes more sense to embed the product tags in the product table. There is a *one\-to\-few* relationship between each product and the tags, which makes a good case for embedding. You'll also store your product data with embedded tags in your new product container. So your new product model will appear as shown in the following diagram:

### Select a partition key

Next, you'll select a partition key for the product container. Again, you need to look at the operations to be performed to decide on a partition key. Your options are either to create a product or edit a product. As customers navigate your e\-commerce site, they'll often do so by product category. You need a query that filters products by `categoryId` to display them to users. To make your query a single\-partition query with all products by category, you use `categoryId` as the partition key for your product container.

So `categoryId` is a good partition key that lets you retrieve all products in a category efficiently. By embedding tag IDs, you can get the IDs in your many\-to\-many relationship between products and tags as well. However, when you query for products, you need not only the product data but you also need to display the category name and the tag names. When you query for products, how can you return the category name for each product and the names for the product tags?

Currently, to display a product page for a category, you would need run the following queries:

1. Query the product container to return all the products in a category.
2. Query the productCategory container to return the product category's name.
3. Then, for every product returned by the first query, run a third query on the productTag container to get each product tag name.

### Denormalize product entities

Running all the preceding queries could work for you. However, this approach isn't very scalable. Remember that, in NoSQL databases, there are no *joins* between containers, so joins aren't an option for you. Also remember that, for NoSQL databases, the objective is to reduce the number of requests by modeling data so that you can fetch your application data in as few requests as possible.

The solution, then, is to *denormalize* your data. With denormalization, you can optimize your data models to ensure that all the required data for your application is ready to be served by your queries.

To denormalize your data in this instance, you add more properties, such as the name of the category and the name of each tag in your tags array. By adding these properties, you can now retrieve all the data you need to return to your clients in only a single request.

---

## Manage referential integrity by using change feed

In the last unit, you saw how denormalizing data can drastically improve performance and lower RU cost by providing the data needed by your e\-commerce application in a single request. However, when data is denormalized like this, you need a way to maintain referential integrity between the master data in the productCategory and productTag containers, and the product container.

Fortunately, Azure Cosmos DB has a feature called *change feed* that can manage referential integrity. Change feed is an API that lives within every Azure Cosmos DB container. Whenever you insert or update data to Azure Cosmos DB, change feed streams these changes to an API that you can listen to. When an event is triggered, you can use change feed to execute code that responds to the changed data.

In your e\-commerce application, you would use change feed to listen to the productCategory and propagate changes to the product container. Then, a second change feed listens to the productTag container and does the same thing.

---

## Combine multiple entities in the same container

You've nearly finished modeling your database for your e\-commerce application. To demonstrate the next concept, let's look at the sales order entities.

### Model sales order entities

As with the other entities, you want to look at your operations and then decide whether to embed or reference your related data. In this scenario, sales order detail makes a great candidate for embedding. This is because the items in the order are not unbounded and the data is always inserted and read together. So you'll embed sales order details as an array within your sales order entity. And you'll store your data in a new container, called salesOrder.

Next, you'll choose a partition key. Because you'll always search for sales order by customer, `customerId` makes a suitable partition key for your container. Your choice of `customerId` will give you a single partition query for an operation that will be run frequently.

At this point, you've modeled all your relational entities for your NoSQL database. So let's look at where you can make further optimizations.

### Identify optimization opportunities

One thing you might have noticed with the salesOrder container is that it shares the same partition key as the customer container. The customer container has a partition key of ID and salesOrder has a partition key of `customerId`. When data share a partition key and have similar access patterns, they're candidates for being stored in the same container. As a NoSQL database, Azure Cosmos DB is schema agnostic, so mixing entities with different schema is not only possible but, under these conditions, it's also another best practice. But to combine the data from these two containers, you'll need to make more changes to your schema.

First, you need to add a `customerId` property to each customer document. Customers will now have the same value for ID and `customerId`. Next, you need a way to distinguish a sales order from a customer in the container. So you'll add a discriminator property you'll call `type` that has a value of `customer` and `salesOrder` for each entity.

With these changes, you can now store both the customer data and sales order data in your new customer container. Each customer is in its own logical partition and will have one customer item with all its sales orders. For your second operation here, you now have a query you can run to list all sales orders for a customer.

---

## Denormalize aggregates in the same container

Before your new model is complete, one last operation to look at is to query your top 10 customers by the number of sales orders. In your current model, you first do a *group by* on each customer and sum for sales orders in your customer container. You then sort in descending order and take the top 10 results. Even though customers and sales orders sit in the same container, this type of query is not something you can currently do.

The solution here is to denormalize the aggregate value in a new property, `salesOrderCount`, in the customer document. You can get the data you want by using this property in a query such as the one shown in the following diagram:

Now, every time a customer creates a new sales order and a new sales order is inserted into your customer container, you need a way to update the customer document and increment the `salesOrderCount` property by one. To do this, you need a transaction. Azure Cosmos DB supports transactions when the data sits within the same logical partition.

Because customers and sales orders reside in the same logical partition, you can insert the new sales order and update the customer document within a transaction. There are two ways to implement transactions in Azure Cosmos DB: by using stored procedures or by using a feature called *transactional batch*, which is available in both .NET and Java SDKs.

---

## Finalize the data model

You've nearly finished remodeling your database. You've transformed nine relational database tables into four containers for your NoSQL database. Your customer container contains your customer and sales order data. The product container contains your products and many\-to\-many product tags. And the other two are the productTag and productCategory containers.

### One final optimization

There's one final optimization you could make. Have you noticed that the productCategory and productTag containers share the same partition key? As you might have guessed, because they share this key, you can put both entities into the same container and give it a more generic name, such as productMeta.

Now you can use queries like the ones you've learned about earlier to get all your product tags and product categories. This pattern works for any kind of master or reference data you need to maintain. Because all of this data is in the same container, you can also use just a single host for Change Feed to maintain referential integrity across the entire database, rather than one for each individual container. Any change that comes in to change feed for any entity can then be routed to a corresponding function by inspecting the type property when the new data is read by change feed. This provides for more efficient usage of compute for change feed as well as efficient storage for the data.

### Your final design

Here then is your final design. With the merging of the product categories and tags, you've gone from nine relational tables to just three containers. Each one is optimized to serve your e\-commerce application efficiently and scale to any size you need.

---

## Exercise advanced modeling patterns

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

In this module, you learned key concepts, techniques, and technologies that are used to model and partition data for NoSQL databases, such as Azure Cosmos DB. You applied them to your e\-commerce application, which you needed to migrate from a relational database to a NoSQL database.

The concepts you learned about in this module include:

* **Denormalization**: You applied this concept to your product data and measured the performance versus querying individual containers.
* **Referential integrity**: You learned how to use change feed to help maintain referential integrity between data that's stored in two different containers.
* **Combining entities**: You learned when it makes sense to store different entities in the same container.
* **Denormalizing aggregates**: You learned a technique that improves performance on high concurrency queries that involve aggregate values on data. You applied it to scenarios that require a subquery to first do a *group by and aggregate*, then do an outer query with an *order by* on the results. You also learned about transactions in Azure Cosmos DB and an SDK feature called transactional batch.

Applying these concepts, techniques, and technologies help ensure that your final database design is efficient in terms of compute. This means that it can scale out as either the size of the database grows or the amount of throughput is increased to handle a higher volume of operations.

Now that you have completed this module, you can:

* Manage relationships between data entities by using advanced modeling and partitioning strategies.
* Maintain the referential integrity of your data by using change feed.
* Implement pre\-aggregating and denormalizing data strategies to improve data\-model performance and scaling.
* Optimizing storage and compute by mixing entity types in a single container

### Learn more

* [Understand the differences between NoSQL and relational databases](/en-us/azure/cosmos-db/relational-nosql)
* [Data modeling in Azure Cosmos DB](/en-us/azure/cosmos-db/modeling-data)
* [Model and partition data on Azure Cosmos DB by using a real\-world example](/en-us/azure/cosmos-db/how-to-model-partition-example)
* [Change feed in Azure Cosmos DB](/en-us/azure/cosmos-db/change-feed)
* [Transactional batch operations in Azure Cosmos DB that use the .NET SDK](/en-us/azure/cosmos-db/transactional-batch)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/_

## Fuentes
- [Design a data partitioning strategy](https://learn.microsoft.com/en-us/training/modules/design-data-partitioning-strategy/?WT.mc_id=api_CatalogApi)
