# Expand query and transaction functionality in Azure Cosmos DB for NoSQL

> Curso: Create server-side programming constructs in Azure Cosmos DB for NoSQL (wwl-create-server-side-programming-azure-cosmos-db) · Seccion: Create server-side programming constructs in Azure Cosmos DB for NoSQL
> Duracion estimada: 53 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Cosmos DB provides language\-integrated, transactional execution of JavaScript. When using the NoSQL API in Azure Cosmos DB, you can write triggers and user\-defined functions (UDFs) in the JavaScript language. In this module, you will author JavaScript logic that enhances the functionalities of the SQL query language and point operations.

After completing this module, you'll be able to:

* Create user\-defined functions
* Create triggers

---

## Create user\-defined functions

User\-defined functions (UDFs) are used to extend the Azure Cosmos DB for NoSQL’s query language grammar and implement custom business logic. UDFs can only be called from inside queries as they enhance and extend the SQL query language.

Note

UDFs do not have access to the context object and are meant to be used as compute\-only code

Here is an example JSON document for a product with a **name** and a **price** property.

```
{
  "name": "Black Bib Shorts (Small)",
  "price": 80.00
}

```

A simple SQL query to get the data from a container with many items like this one, would be constructed to include both fields.

```
SELECT 
    p.name,
    p.price
FROM
    products p

```

UDFs extend the SQL query language by giving you small areas where you can inject simple business logic into a query. Let's take this example, and create a user\-defined function to apply business tax. In our example scenario, we want to apply a 15% tax and end up with an ideal result set that includes a third **priceWithTax** property.

```
[
  {
    "name": "Black Bib Shorts (Small)",
    "price": 80.00,
    "priceWithTax": 92.00
  }
]

```

A user\-defined function is defined as a JavaScript function that takes in one or more scalar input\[s] and then returns a scalar value as the output.

```
function name(input) {
    return output;
}

```

In this example function, the scalar input is assumed to be a number that is then multipled by **1\.15** to add 15% tax.

```
function addTax(preTax) {
    return preTax * 1.15;
}

```

The updated query includes a third projected field that references the udf function by using the `udf.addTax()` syntax passing in the **p.price** field as an input parameter and aliasing the output of that field to the name **priceWithTax**.

```
SELECT 
    p.name,
    p.price,
    udf.addTax(p.price) AS priceWithTax
FROM
    products p

```

---

## Create user\-defined functions with the SDK

The **Scripts** property in the **Microsoft.Azure.Cosmos.Container** class contains a **CreateUserDefinedFunctionAsync** method that is used to create a new user\-defined function from code.

Note

The next set of examples assume that you already have a container variable defined.

To start, define the JavaScript function for the UDF in a string variable.

```
string udf = @"function addTax(preTax) {
    return preTax * 1.15;
}";

```

Tip

Alternatively, you can use file APIs such as **System.IO.File** to read a function from a \*.js file.

Next, create an object of type **Microsoft.Azure.Cosmos.Scripts.UserDefinedFunctionProperties** with the **Id** and **Body** properties set to the unique identifier and content of the UDF, respectively.

```
UserDefinedFunctionProperties properties = new()
{
    Id = "addTax",
    Body = udf
};

```

Finally, invoke the **CreateUserDefinedFunctionAsync** method of the container variable to create a new UDF passing in the properties composed earlier.

```
await container.Scripts.CreateUserDefinedFunctionAsync(properties);

```

---

## Summary

In this module, you authored a user\-defined function that enhanced the functionality of a SQL query.

Now that you have completed this module, you can:

* Create a user\-defined function and use it in a SQL query
* Create a pre or post trigger that is executed with a point operation

### Learn more

For more information about the topics discussed in this module, see:

* [How to write stored procedures, triggers, and user\-defined functions in Azure Cosmos DB](/en-us/azure/cosmos-db/how-to-write-stored-procedures-triggers-udfs)
* [User\-defined functions (UDFs) in Azure Cosmos DB](/en-us/azure/cosmos-db/sql/sql-query-udfs)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/_

## Fuentes
- [Expand query and transaction functionality in Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/expand-query-transaction-functionality-azure-cosmos-db-sql-api/?WT.mc_id=api_CatalogApi)
