# Create resource template for Azure Cosmos DB for NoSQL

> Curso: Manage an Azure Cosmos DB for NoSQL solution using DevOps practices (wwl-manage-cosmos-db-sql-api-solution-using-devops) · Seccion: Manage an Azure Cosmos DB for NoSQL solution using DevOps practices
> Duracion estimada: 43 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Once an Azure Cosmos DB for NoSQL account is ready to go through a release lifecycle, it's not uncommon for an operations team to attempt to automate the creation of Azure Cosmos DB resources in the cloud. Automation makes it easier to deploy new environments, restore past environments, or scale a service out.

In Azure, Azure Resource Manager and Bicep templates are two of the ways you can automate the creation of Azure Cosmos DB resources. Azure Resource Manager templates are JavaScript Object Notation (JSON) files that define the infrastructure and configuration for your project. Bicep is an alternative template language that can be used to develop templates.

Note

For this module, we will use both the **Bicep** and **JSON** syntaxes for **Azure Resource Manager templates**. The hands\-on exercise for this module will use both the **Bicep** and **JSON** syntaxes to illustrate the differences.

After completing this module, you'll be able to:

* Identify the three most common resource types for Azure Cosmos DB for NoSQL accounts
* Create and deploy a JSON Azure Resource Manager template for an Azure Cosmos DB for NoSQL account, database, or container
* Create and deploy a Bicep template for an Azure Cosmos DB for NoSQL account, database, or container
* Manage throughput and index policies using JSON or Bicep templates

---

## Understand Azure Resource Manager resources

When creating Bicep files or Azure Resource Manager templates (ARM templates), you need to understand what resource types are available, and what values to use in your template.

Each of the resources available for Azure Cosmos DB is listed under the **Microsoft.DocumentDB** resource provider:

| **Resource type** | **Description** |
| --- | --- |
| **Microsoft.DocumentDB/databaseAccounts** | Represents an account |
| **Microsoft.DocumentDB/databaseAccounts/sqlDatabases** | Represents a NoSQL API database |
| **Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers** | Represents a NoSQL API container |

Visually, you can think of these resources as a hierarchy.

This list is not exhaustive, other resources can be created in a template such as:

* Stored procedures
* User\-defined functions
* Pre\-triggers
* Post\-triggers

Tip

These example container\-level resources can be created with their code automatically deployed using a template.

---

## Author Azure Resource Manager templates

Authoring a template for an Azure Cosmos DB for NoSQL account is much like building one from scratch using the portal or from the CLI. There are three primary resources to define in a specific relationship order.

### Empty template

An Azure Resource Manager template is, at its core, a JSON file with a specific syntax you must follow. The default minimal empty template is a JSON document with a **schema** property set to `https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#`, a **contentVersion** property set to `1.0.0.0`, and an empty **resources** array. This example illustrates a minimal empty template.

```
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
  ]
}

```

Note

All resources we place in this template will be JSON objects within the **resources** array.

### Account resource

The first resource type to define is **Microsoft.DocumentDB/databaseAccounts**. This represents an account that is not specific to any API. If the API is not specified, it is inferred to be a NoSQL API account.

An object for this resource must contain, at a minimum, the following properties:

* name
* location
* properties.databaseAccountOfferType
* properties.locations\[].locationName

Here is an example of an account that has a unique name with a prefix of **csmsarm** and is deployed to **West US**.

```
{
  "type": "Microsoft.DocumentDB/databaseAccounts",
  "apiVersion": "2024-04-15",
  "name": "[concat('csmsarm', uniqueString(resourceGroup().id))]",
  "location": "[resourceGroup().location]",
  "properties": {
    "databaseAccountOfferType": "Standard",
    "locations": [
      {
        "locationName": "westus"
      }
    ]
  }
}

```

Note

You can define more than one location using the locations array.

### Database resource

The next resource is of type **Microsoft.DocumentDB/databaseAccounts/sqlDatabases** and is a child resource of the account. This relationship is defined using the **dependsOn** property.

An object for this resource must contain, at a minimum, the following properties:

* name
* properties.resources.id

Here is an example of a database that is named **cosmicworks**.

```
{
  "type": "Microsoft.DocumentDB/databaseAccounts/sqlDatabases",
  "apiVersion": "2024-04-15",
  "name": "[concat('csmsarm', uniqueString(resourceGroup().id), '/cosmicworks')]",
  "dependsOn": [
    "[resourceId('Microsoft.DocumentDB/databaseAccounts', concat('csmsarm', uniqueString(resourceGroup().id)))]"
  ],
  "properties": {
    "resource": {
      "id": "cosmicworks"
    }
  }
}

```

### Container resource

Within a database, you can define multiple child **Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers** resources. Here, you can allocate throughput, configure indexing policy, and set a partition key path.

A container object must contain, at a minimum, the following properties:

* name
* properties.resource.id
* properties.resource.partitionkey.paths\[]

A container can also optionally contain the following properties:

* properties.options.throughput
* properties.options.autoscaleSettings.maxThroughput
* properties.resource.indexingPolicy

Here is an example of a container that is named **products**, has **1000 RU/s** autoscale, and a partition key path of **/categoryId**.

```
{
  "type": "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers",
  "apiVersion": "2024-04-15",
  "name": "[concat('csmsarm', uniqueString(resourceGroup().id), '/cosmicworks/products')]",
  "dependsOn": [
    "[resourceId('Microsoft.DocumentDB/databaseAccounts', concat('csmsarm', uniqueString(resourceGroup().id)))]",
    "[resourceId('Microsoft.DocumentDB/databaseAccounts/sqlDatabases', concat('csmsarm', uniqueString(resourceGroup().id)), 'cosmicworks')]"
  ],
  "properties": {
    "resource": {
      "id": "products",
      "partitionKey": {
        "paths": [
          "/categoryId"
        ]
      }
    },
    "options": {
      "autoscaleSettings": {
        "maxThroughput": 1000
      }
    }
  }
}

```

Note

Throughput is itself a child resource of a container and can be provisioned by creating a **Microsoft.DocumentDB/databaseAccounts/sqlDatabases/throughputSettings** child resource of the container. However, it is less verbose to set throughput values using the `options` of the container properties. This is the recommended means for both creating and updating throughput for a container.

### Final template

Now that all resources are in place, the template file should now contain the following code.

```
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.DocumentDB/databaseAccounts",
      "apiVersion": "2024-04-15",
      "name": "[concat('csmsarm', uniqueString(resourceGroup().id))]",
      "location": "[resourceGroup().location]",
      "properties": {
        "databaseAccountOfferType": "Standard",
        "locations": [
          {
            "locationName": "westus"
          }
        ]
      }
    },
    {
      "type": "Microsoft.DocumentDB/databaseAccounts/sqlDatabases",
      "apiVersion": "2024-04-15",
      "name": "[concat('csmsarm', uniqueString(resourceGroup().id), '/cosmicworks')]",
      "dependsOn": [
        "[resourceId('Microsoft.DocumentDB/databaseAccounts', concat('csmsarm', uniqueString(resourceGroup().id)))]"
      ],
      "properties": {
        "resource": {
          "id": "cosmicworks"
        }
      }
    },
    {
      "type": "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers",
      "apiVersion": "2021-05-15",
      "name": "[concat('csmsarm', uniqueString(resourceGroup().id), '/cosmicworks/products')]",
      "dependsOn": [
        "[resourceId('Microsoft.DocumentDB/databaseAccounts', concat('csmsarm', uniqueString(resourceGroup().id)))]",
        "[resourceId('Microsoft.DocumentDB/databaseAccounts/sqlDatabases', concat('csmsarm', uniqueString(resourceGroup().id)), 'cosmicworks')]"
      ],
      "properties": {
        "resource": {
          "id": "products",
          "partitionKey": {
            "paths": [
              "/categoryId"
            ]
          }
        },
        "options": {
          "autoscaleSettings": {
            "maxThroughput": 1000
          }
        }
      }
    }
  ]
}

```

---

## Configure database or container resources

Each template resource uses the same resource type and version between both Azure Resource Manager and Bicep templates. If you learn how to build it in one language, you can easily learn it in the other.

Note

A Bicep template does not require any "empty" template syntax. You can begin writing your definitions in a blank file.

### Account resource

The **Microsoft.DocumentDB/databaseAccounts** resource in Bicep must contain the same minimal properties as in an Azure Resource Manager template.

Here is an example of an account that has a unique name with a prefix of **csmsarm** and is deployed to **West US**.

```
resource Account 'Microsoft.DocumentDB/databaseAccounts@2024-04-15' = {
  name: 'csmsbicep${uniqueString(resourceGroup().id)}'
  location: resourceGroup().location
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: 'westus'
      }
    ]
  }
}

```

Tip

If this resource already exists from a previous deployment, the Azure Resource Manager will just skip the resource and move on to the next. This is very handy when building a template incrementally.

### Database resource

This example of a **Microsoft.DocumentDB/databaseAccounts/sqlDatabases** resource configures a database resource, a slight difference from the JSON template reviewed in a previous unit.

Bicep also requires resources to define a **parent** property defining relationships as opposed to the verbose **dependsOn** property.

```
resource Database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-04-15' = {
  parent: Account
  name: 'cosmicworks'
  properties: {
    options: {
      
    }
    resource: {
      id: 'cosmicworks'
    }
  }
}

```

### Container resource

This **Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers** resource is similar to the JSON equivalent, except it defines a throughput property at this level.

```
resource Container 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-04-15' = {
  parent: Database
  name: 'customers'
  properties: {
    resource: {
      id: 'customers'
      partitionKey: {
        paths: [
          '/regionId'
        ]
      }
    },
    options: {
      autoscaleSettings: {
        maxThroughput: 1000
      }
    }
  }
}

```

### Final template

Now that all resources are in place, the template file should now contain the following code.

```
resource Account 'Microsoft.DocumentDB/databaseAccounts@2024-04-15' = {
  name: 'csmsbicep${uniqueString(resourceGroup().id)}'
  location: resourceGroup().location
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: 'westus'
      }
    ]
  }
}

resource Database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-04-15' = {
  parent: Account
  name: 'cosmicworks'
  properties: {
    resource: {
      id: 'cosmicworks'
    }
  }
}

resource Container 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-04-15' = {
  parent: Database
  name: 'customers'
  properties: {
    resource: {
      id: 'customers'
      partitionKey: {
        paths: [
          '/regionId'
        ]
      }
    },
    options: {
      autoscaleSettings: {
        maxThroughput: 1000
      }
    }
  }
}

```

---

## Manage index policies through Azure Resource Manager templates

It is common to define an indexing policy as part of deploying an Azure Cosmos DB account and its resources in an automated manner. Both the JSON and Bicep syntax for Azure Resource Manager templates supports defining indexing policies natively. However, the syntax can be tricky if you haven't tried it before.

For the examples in this unit, let's assume that we want to deploy the following indexing policy to our **products** container.

### Defining an indexing policy in JSON templates

Let's assume that we want to deploy the following indexing policy to our **products** container in our account.

```
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    {
      "path": "/price/*"
    }
  ],
  "excludedPaths": [
    {
      "path": "/*"
    }
  ]
}

```

The **indexingPolicy** object can be lifted with no changes and set to the **properties.resource.indexingPolicy** property of the **Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers**.

```
{
  "type": "Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers",
  "apiVersion": "2024-04-15",
  "name": "[concat('csmsarm', uniqueString(resourceGroup().id), '/cosmicworks/products')]",
  "dependsOn": [
    "[resourceId('Microsoft.DocumentDB/databaseAccounts', concat('csmsarm', uniqueString(resourceGroup().id)))]",
    "[resourceId('Microsoft.DocumentDB/databaseAccounts/sqlDatabases', concat('csmsarm', uniqueString(resourceGroup().id)), 'cosmicworks')]"
  ],
  "properties": {
    "resource": {
      "id": "products",
      "partitionKey": {
        "paths": [
          "/categoryId"
        ]
      },
      "indexingPolicy": {
        "indexingMode": "consistent",
        "automatic": true,
        "includedPaths": [
          {
            "path": "/price/*"
          }
        ],
        "excludedPaths": [
          {
            "path": "/*"
          }
        ]
      }
    },
    "options": {
      "autoscaleSettings": {
        "maxThroughput" : 1000
      }
    }
  }
}

```

### Defining an indexing policy in Bicep templates

Let's assume that we want to deploy the following indexing policy to our **customers** container in our account.

```
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    {
      "path": "/address/*"
    }
  ],
  "excludedPaths": [
    {
      "path": "/*"
    }
  ]
}

```

A few small changes are required to use this indexing policy in Bicep. These changes include:

* Removing the double quotation from property names
* Changing property values from double quotes to single quotes
* Removing commas typically required in JSON

```
resource Container 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-04-15' = {
  parent: Database
  name: 'customers'
  properties: {
    resource: {
      id: 'customers'
      partitionKey: {
        paths: [
          '/regionId'
        ]
      }
      indexingPolicy: {
        indexingMode: 'consistent'
        automatic: true
        includedPaths: [
          {
            path: '/address/*'
          }
        ]
        excludedPaths: [
          {
            path: '/*'
          }
        ]
      }
    },
    "options": {
      "autoscaleSettings": {
        "maxThroughput" : 1000
      }
    }
  }
}

```

### Updating an indexing policy on an existing container

If a resource of type **Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers** already exists, and all other properties match, you can update the indexing policy by solely changing the values within the **properties.resource.indexingPolicy** property. Azure Resource Manager will only change the indexing policy while keeping the rest of the container intact.

The command for deployment is the same as the initial deployment.

```
az deployment group create \
    --resource-group '<resource-group>' \
    --template-file '.\template.json' \
    --name 'jsontemplatedeploy'

```

```
az deployment group create \
    --resource-group '<resource-group>' \
    --template-file '.\template.bicep' \
    --name 'biceptemplatedeploy'

```

---

## Exercise: Create an Azure Cosmos DB for NoSQL container using Azure Resource Manager templates

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

In this module, you used Azure Resource Manager and Bicep templates to automate the deployment and management of Azure Cosmos DB for NoSQL resources in the cloud.

Tip

Remember, the **Microsoft.DocumentDB** resource provider has many other resources that can be deployed using templates. This module only covered a subset of possible resources.

Now that you have completed this module, you can:

* Describe the differences between the various resource types within the **Microsoft.DocumentDB** resource provider.
* Create and deploy Azure Comsos DB for NoSQL accounts, databases, or containers using an Azure Resource Manager or Bicep template.
* Adjust the properties of containers and databases using an Azure Resource Manager or Bicep template.

### Learn more

For more information about the topics discussed in this module, see:

* [Quickstart: Create an Azure Cosmos DB and a container by using an ARM template](/en-us/azure/cosmos-db/sql/quick-create-template)
* [Bicep documentation](/en-us/azure/azure-resource-manager/bicep/)
* [ARM template documentation](/en-us/azure/azure-resource-manager/templates/)
* [Microsoft.DocumentDB \| databaseAccounts](/en-us/azure/templates/microsoft.documentdb/databaseaccounts)
* [Microsoft.DocumentDB \| databaseAccounts \| sqldatabases](/en-us/azure/templates/microsoft.documentdb/databaseaccounts/sqldatabases)
* [Microsoft.DocumentDB \| databaseAccounts \| sqldatabases \| containers](/en-us/azure/templates/microsoft.documentdb/databaseaccounts/sqldatabases/containers)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/_

## Fuentes
- [Create resource template for Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/create-resource-template-for-azure-cosmos-db-sql-api/?WT.mc_id=api_CatalogApi)
