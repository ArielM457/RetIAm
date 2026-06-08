# Build multi-item transactions with the Azure Cosmos DB for NoSQL

> Curso: Create server-side programming constructs in Azure Cosmos DB for NoSQL (wwl-create-server-side-programming-azure-cosmos-db) · Seccion: Create server-side programming constructs in Azure Cosmos DB for NoSQL
> Duracion estimada: 39 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

When using the NoSQL API in Azure Cosmos DB, you can write stored procedures in the JavaScript language that perform multiple operations as a single logical unit. In this module, you will author JavaScript stored procedures that execute directly inside the database engine.

After completing this module, you'll be able to:

* Author stored procedures
* Rollback stored procedure transactions

---

## Understand transactions in the context of JavaScript SDK

In a database, a transaction is typically defined as a sequence of point operations grouped together into a single unit of work. It's expected that a transaction provides **ACID** guarantees:

* **Atomicity** guarantees that all the work done inside a transaction is treated as a single unit where either all of it is committed or none.
* **Consistency** makes sure that the data is always in a healthy internal state across transactions.
* **Isolation** guarantees that no two transactions interfere with each other – generally, most commercial systems provide multiple isolation levels that can be used based on the application's needs.
* **Durability** ensures that any change that's committed in the database will always be present.

In Azure Cosmos DB for NoSQL, a stored procedure executes one or more operations as a single unit of work within the same scope. Stored procedures are registered in containers, and run within the scope of that specific container.

Note

Stored procedures are scoped to a single logical partition. You cannot execute a stored procedure that performs operations across logical partition key values.

Transactions occur server\-side in Azure Cosmos DB for NoSQL, so they must adhere to the same limitations as many other HTTP requests. All operations within a stored procedure must be completed within a bounded amount of time. Specifically, the operations must be complete within the **server request timeout** duration.

For long\-running lists of operations, a helper boolean value is returned by any JavaScript function that performs an operation indicating whether that operation is expected to complete within the request timeout duration. If the Boolean is **true**, you can continue on with the stored procedure. Once that Boolean is **false**, then the stored procedure must finalize as soon as possible. At this point, it is common to return a pointer so that subsequent calls to the stored procedure can start from the pointer instead of rewinding progress all the way to the beginning of the long\-running list of operations.

---

## Author Stored procedures

Transactions are defined as JavaScript functions. The function is then executed when the stored procedure is invoked.

```
function name() {
}

```

Within the function, the `getContext()` method retrieves a context object, which can be used to perform multiple actions, including:

* Access the HTTP response object
* Access the corresponding Azure Cosmos DB for NoSQL container

Using the context object, you can invoke the `getResponse()` method to access the HTTP response object to perform actions such as returning a **HTTP OK** (200\) and setting the response's body to a static string.

```
function greet() {
    var context = getContext();
    var response = context.getResponse();
    response.setBody("Hello, Learn!");
}

```

Again, using the context object, you can invoke the `getCollection()` method to access the container using the JavaScript query API.

```
function createProduct(item) {
    var context = getContext();
    var container = context.getCollection(); 
}

```

At this point, you can perform typical operations such as creating a new document.

```
function createProduct(item) {
    var context = getContext();
    var container = context.getCollection(); 
    container.createDocument(
        container.getSelfLink(),
        item
    );
}

```

This stored procedure is almost complete. While this code will run fine, it does stand the risk of swallowing errors and potentially not returning if the stored procedure has exceeded the timeout. We should update the code by implementing two more changes:

* Store the boolean return value of container.createDocument, and then use that to determine if we should return from the function due to an impending server timeout.
* Add a third parameter to container.createDocument to handle potential errors and set the response of this stored procedure to the newly created item returned from the operation.

```
function createProduct(item) {
    var context = getContext();
    var container = context.getCollection(); 
    var accepted = container.createDocument(
        container.getSelfLink(),
        item,
        (error, newItem) => {
            if (error) throw error;
            context.getResponse().setBody(newItem)
        }
    );
    if (!accepted) return;
}

```

Tip

Alternatively, you can use the `__` (double underscore) shortcut as an equivalent to `getContext().getCollection()`.

---

## Rollback transactions

Transactions are deeply and natively integrated into Azure Cosmos DB for NoSQL’s JavaScript programming model. Inside a JavaScript function, all operations are automatically wrapped under a single transaction. If the function completes without any exception, all data changes are committed. Azure Cosmos DB for NoSQL will roll back the entire transaction if a single exception is thrown from the script.

Effectively, the start of the JavaScript function is similar to a **BEGIN TRANSACTION** statement in a database system, with the end of the function scope being the functional equivalent of **COMMIT TRANSACTION**. If any error is thrown, that’s the functional equivalent of **ROLLBACK TRANSACTION**.

In code, this is surfaced simply by throwing any error in JavaScript:

```
throw new Error('Something');

```

Using the create item example from earlier in this module, you can create a callback function to determine if the operation returned an error from the server. If so, you can rethrow the error immediately to short\-circuit your code and cause the entire stored procedure transaction to be rolled back.

```
(error, newItem) => {
    if (error) throw error;
    // Do something with item
}

```

---

## Create stored procedures with the JavaScript SDK

Creating a stored procedure using the .NET SDK requires the use of a special **Scripts** property in the **Microsoft.Azure.Cosmos.Container** class. Let’s start with an example that assumes a container instance in a variable named **container**.

1. First, define the JavaScript function for the stored procedure in a string variable.

```
string sproc = @"function greet() {
    var context = getContext();
    var response = context.getResponse();
    response.setBody('Hello, Learn!');
}";

```

Tip

Alternatively, you can use file APIs such as **System.IO.File** to read a function from a \*.js file.
2. Next, create an object of type **Microsoft.Azure.Cosmos.Scripts.StoredProcedureProperties** with the **Id** and **Body** properties set to the unique identifier and content of the stored procedure, respectively.

```
StoredProcedureProperties properties = new()
{
    Id = "greet",
    Body = sproc
};

```

Tip

Alternatively, you can provide the identifier and body of the stored procedure as constructor parameters.

```
    StoredProcedureProperties properties = new("greet", sproc);

```
3. Now, use the **CreateStoredProcedureAsync\<\>** method of the container variable to create a new stored procedure passing in the properties composed earlier.

```
await container.Scripts.CreateStoredProcedureAsync(properties);

```

If you'd like to parse the results, the **CreateStoredProcedureAsync\<\>** method returns an object of type **Microsoft.Azure.Cosmos.Scripts.StoredProcedureResponse** that contains metadata about the newly created stored procedure within the container.

---

## Exercise: Create a stored procedure with the Azure portal

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

In this module, you created stored procedures that executed JavaScript logic directly within the database engine.

Now that you have completed this module, you can:

* Create a stored procedure using the portal or the .NET SDK
* Roll back a transaction within a stored procedure by throwing an error

### Learn more

For more information about the topics discussed in this module, see:

* [How to write stored procedures, triggers, and user\-defined functions in Azure Cosmos DB](/en-us/azure/cosmos-db/how-to-write-stored-procedures-triggers-udfs)
* [How to write stored procedures and triggers in Azure Cosmos DB by using the JavaScript query API](/en-us/azure/cosmos-db/how-to-write-javascript-query-api)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/_

## Fuentes
- [Build multi-item transactions with the Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-multi-item-transactions-azure-cosmos-db-sql-api/?WT.mc_id=api_CatalogApi)
