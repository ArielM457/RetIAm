# Migrate SQL Server workloads to Azure SQL Database

> Curso: Migrate application workloads and data to Azure (wwl-migrate-application-workloads-data-azure) · Seccion: Migrate application workloads and data to Azure
> Duracion estimada: 78 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure SQL Database is a Platform as a Service (PaaS) database engine that provides a complete development and deployment environment in the cloud, which can be used for simple cloud\-based applications and for advanced enterprise applications.

Migrating to SQL Database allows you to modernize your application by taking advantage of its PaaS capabilities. This enables you to eliminate dependencies on technical components that are scoped at the instance level, such as SQL Agent jobs. Azure SQL Database offers a low\-maintenance solution that can be an excellent choice for certain workloads.

You may have specific requirements that are better suited for Azure SQL Database rather than Azure SQL Managed Instance in the following scenarios:

* You need to simplify deployment for databases with intermittent, unpredictable usage.
* New databases without usage history where compute sizing is difficult or not possible to estimate prior to deployment.
* The complexity of deployment and development is a concern.
* Your storage requirements are higher than what Azure SQL Managed Instance offers, and database consolidation isn't an option.

The process of migrating a SQL Server database running on an Azure virtual machine to Azure SQL Database is similar to the steps we'll learn in this module.

Note

Before proceeding, it is important to ensure that you have reviewed the [Assess SQL Server databases for migration to Azure SQL](/en-us/training/modules/assess-sql-server-databases-for-migration-to-azure-sql/). This module will introduce you to the assessment tools and help you discover new features in the target SQL Server platform that your database can benefit from after an upgrade.

#### Use case scenario

Throughout this module, we're using an example scenario to explain key data migration concepts.

Suppose you work for a company that builds bikes and bicycle parts. You have several legacy database servers that you want to upgrade, including a product database, a parts stock database, and a human resources database. You also want to move from a capital expenditure model to an operational expenditure model, and benefit from the scalability and availability of Azure services. You plan to migrate your SQL Server databases to Azure SQL Database. Your board of directors has asked you to plan the migration project and has made you responsible for the execution of the migration tasks.

You'll learn how to migrate SQL Server databases to Azure SQL Database. You'll begin by exploring the pre\-migration considerations you need to take into account before a migration, and how to create an Azure SQL database. You'll then explore the different methods for offline and online migrations, and look at ways to move data to Azure SQL Database.

---

## Choose the right Azure SQL Database feature

In our bicycle manufacturing scenario, you've already identified and profiled the databases that you want to migrate to Azure SQL Database. Now, you want to plan the migration, considering data recoverability, disaster recovery, security, and other implementation details.

You'd like to know the tools and features available to support with the migration process to Azure SQL Database.

### Benefits of Azure SQL Database

The following summarize the benefits of deploying single and elastic pool databases:

| Category | Feature |
| --- | --- |
| **Backup and recovery** | Automatic backup |
|  | Point\-in\-time restore |
|  | Backup retention 7 days\+ |
|  | Long\-term backup retention stores backups for up to 10 years |
| **High availability** | 99\.99% availability guarantee |
|  | Built\-in availability with three secondary replicas |
|  | Zone redundancy via Azure availability zones |
| **Disaster recovery** | Geo\-restore of database backups |
|  | Active\-geo replication between Azure regions |
| **Service scalability** | Dynamic scale\-up and scale\-down |
|  | Scale out with multiple shards |
|  | Share compute resources between databases using elastic pools |
| **Security** | Support for Microsoft Entra authentication |
|  | Cloud\-only security features such as Advanced Threat Protection |
|  | Transparent data encryption (TDE) enabled by default |
|  | Support for dynamic and static data masking, row\-level security, and Always Encrypted |
|  | Firewall allowlist |
| **Licensing** | DTU purchasing model for predictive costing |
|  | vCore purchasing model, enabling storage to be scaled independently of compute |
|  | Combine the vCore purchasing model with Azure Hybrid Benefit for SQL Server to realize cost savings of up to 30 percent |

Tip

To review the benefits of migrating to Azure SQL Database and the features available, please refer to [Deploy PaaS solutions with Azure SQL](/en-us/training/modules/deploy-paas-solutions-with-azure-sql/) module.

#### Exclusive features of Azure SQL Database

Some features are supported in Azure SQL Database that aren't available in other Azure SQL offerings:

| Feature | Definition |
| --- | --- |
| [**Hyperscale**](/en-us/azure/azure-sql/database/service-tier-hyperscale) | Cloud\-native architecture that allows for independently scalable compute and storage, providing greater flexibility and resources than other tiers. |
| [**Auto\-scale**](/en-us/azure/azure-sql/database/serverless-tier-overview?tabs=general-purpose#autoscaling) | With serverless compute tier |
| [**Automatic tuning (indexes)**](/en-us/azure/azure-sql/database/automatic-tuning-overview) | This built\-in feature automatically identifies and creates indexes that can improve the performance of your workload. It also verifies that query performance has improved and removes unused or duplicate indexes. |
| [**Elastic query**](/en-us/azure/azure-sql/database/elastic-query-overview) | Allows you to run T\-SQL queries that bridge multiple databases in SQL Database. This feature is useful for applications using three\- and four\-part names that can't be changed. |
| [**Elastic jobs**](/en-us/azure/azure-sql/database/job-automation-overview) | The elastic job feature is the SQL Server Agent replacement for Azure SQL Database. To some extent, elastic job is equivalent to the Multi Server Administration feature available on SQL Server instance. |
| [**Query Performance Insights (QPI)**](/en-us/azure/azure-sql/database/query-performance-insight-use) | This tool helps find the queries to optimize to improve overall workload performance and efficiently use the resource that you're paying for. |

Important

To understand additional feature differences between SQL Database, SQL Server, and Azure SQL Managed Instance, as well as the differences among different Azure SQL Database options, see [SQL Database features](/en-us/azure/azure-sql/database/features-comparison).

### Migration options supported

There are two modes of migration to Azure SQL Database: **Online** and **Offline**. The online mode has minimal or no downtime, while the offline mode experiences downtime during the migration process.

| Tool | Migration mode |
| --- | --- |
| [Azure Database Migration Service](/en-us/azure/dms/dms-overview) | **Offline** |
| [Transactional replication](/en-us/sql/relational-databases/replication/transactional/transactional-replication) | **Online** |
| [Azure Migrate](/en-us/azure/migrate/migrate-services-overview) | **Offline** |
| [Import Export Wizard/BACPAC](/en-us/azure/azure-sql/database/database-export) | **Offline** |
| [Bulk copy (bcp utility)](/en-us/sql/relational-databases/import-export/import-and-export-bulk-data-by-using-the-bcp-utility-sql-server) | **Offline** |
| [Azure Data Factory](/en-us/azure/data-factory/quickstart-get-started) | **Offline** |

\* Can have a higher performance impact, depending on the workload.

Note

We recommend that you use the [Azure Database Migration Service](/en-us/azure/dms/dms-overview) for large migrations and enhanced overall experience.

### Migration performance

Consider the following recommendations when migrating to Azure SQL Database:

* Monitor data file I/O and latency on the source, and mitigate any bottlenecks.
* Scale up the target Azure SQL database to Business Critical Gen5 8 vCore or use the Hyperscale service tier to minimize latency for log files.
* Ensure that your network bandwidth can accommodate the maximum log ingestion rate.
* Choose the highest service tier and compute size for maximum transfer performance, and scale down after migration.
* Minimize the distance between BACPAC files and the destination data center.
* Disable auto update and auto create statistics during migration.
* Partition tables and indexes, drop indexed views, and recreate them after migration.
* Consider migrating rarely queried historical data to a separate database in Azure SQL Database, and query it using elastic queries.

### Retry application connections

When migrating to Azure SQL Database, it's important to anticipate occasional transient failures when connecting to the database resource, and implement a proper retry logic method. Setting a maximum number of retries before the program terminates is also important.

We recommend waiting for 5 seconds at a minimum on your first retry. Each subsequential retry should increase the delay exponentially, up to a maximum of 60 seconds.

Note

If a SELECT statement fails with a transient error for SQL Database, don't directly retry it. Instead, retry the SELECT statement in a new connection.

To learn more about the connection retry principals, see [Troubleshoot transient connection errors in SQL Database and SQL Managed Instance](/en-us/azure/azure-sql/database/troubleshoot-common-connectivity-issues).

---

## Use Azure Database Migration Service to migrate to Azure SQL Database

If you can afford to take the database offline while you migrate to Azure, you have a few tools you can use.

In our bicycle manufacturing scenario, the HR database is considered business\-critical but is rarely used at weekends. You've planned to execute an offline migration between Friday evening and Monday morning, but you want to assess the best migration method.

It's assumed that all pre\-migration checks have been done with [Azure Migrate](/en-us/azure/migrate/migrate-services-overview). This process ensures that feature and compatibility issues are addressed.

### Migrate using Azure Database Migration Service with Azure CLI

[Azure Database Migration Service](/en-us/azure/dms/dms-overview) is a fully managed service designed to enable seamless migrations from multiple database sources to Azure data platforms with minimal downtime. You can use Azure CLI or PowerShell to automate database migrations, making it ideal for migrating databases at scale.

The Azure CLI `az datamigration` extension provides commands to create and manage database migrations to Azure SQL Database. This approach is particularly useful for:

* Automating migrations as part of CI/CD pipelines
* Migrating multiple databases at scale
* Scripting repeatable migration processes

#### Prerequisites

Before starting the migration, ensure you have:

1. **Azure CLI installed** with the `datamigration` extension
2. **Azure Database Migration Service** created in your subscription
3. **Target Azure SQL Database** provisioned with the schema already deployed
4. **Self\-hosted integration runtime** configured for connectivity to your source SQL Server

To install the Azure CLI datamigration extension, run:

```
az extension add --name datamigration

```

#### Create the Database Migration Service

First, create an Azure Database Migration Service to orchestrate your migration activities:

```
## Create the Azure Database Migration Service
az datamigration sql-service create \
    --resource-group "<YourResourceGroup>" \              # Name of your Azure resource group
    --sql-migration-service-name "<YourMigrationService>" \  # Name for the migration service
    --location "<YourLocation>"                            # Azure region (e.g., eastus2, westus)

```

#### Migrate the database schema

Before migrating data, you need to migrate the database schema from the source to the target. Use the `az datamigration sql-server-schema` command:

```
## Migrate schema from source to target database
az datamigration sql-server-schema \
    --action "MigrateSchema" \
    --src-sql-connection-str "Server=<YourSourceServer>;Initial Catalog=<YourSourceDB>;User ID=<YourSourceUser>;Password=<YourSourcePassword>" \
    --tgt-sql-connection-str "Server=<YourTargetServer>.database.windows.net;Initial Catalog=<YourTargetDB>;User ID=<YourTargetUser>;Password=<YourTargetPassword>"

```

#### Start the database migration

Create a new database migration to copy data from the source to target:

```
## Create a database migration to Azure SQL Database
az datamigration sql-db create \
    --resource-group "<YourResourceGroup>" \            # Name of your Azure resource group
    --sqldb-instance-name "<YourTargetServer>" \        # Name of the target Azure SQL Database server
    --target-db-name "<YourTargetDB>" \                 # Name of the target database
    --source-database-name "<YourSourceDB>" \           # Name of the source database
    --source-sql-connection authentication="SqlAuthentication" \
        data-source="<YourSourceServer>" \              # Source SQL Server hostname or IP
        user-name="<YourSourceUser>" \                  # Source SQL Server username
        password="<YourSourcePassword>" \               # Source SQL Server password
        encrypt-connection=true \
        trust-server-certificate=true \
    --target-sql-connection authentication="SqlAuthentication" \
        data-source="<YourTargetServer>.database.windows.net" \  # Target Azure SQL Database server
        user-name="<YourTargetUser>" \                  # Target database username
        password="<YourTargetPassword>" \               # Target database password
        encrypt-connection=true \
        trust-server-certificate=true \
    --scope "/subscriptions/<YourSubscription>/resourceGroups/<YourResourceGroup>/providers/Microsoft.Sql/servers/<YourTargetServer>" \
    --migration-service "/subscriptions/<YourSubscription>/resourceGroups/<YourResourceGroup>/providers/Microsoft.DataMigration/sqlMigrationServices/<YourMigrationService>"

```

#### Migrate specific tables

To migrate only specific tables, use the `--table-list` parameter:

```
## Create a database migration for specific tables
az datamigration sql-db create \
    --resource-group "<YourResourceGroup>" \
    --sqldb-instance-name "<YourTargetServer>" \
    --target-db-name "<YourTargetDB>" \
    --source-database-name "<YourSourceDB>" \
    --source-sql-connection authentication="SqlAuthentication" \
        data-source="<YourSourceServer>" \
        user-name="<YourSourceUser>" \
        password="<YourSourcePassword>" \
        encrypt-connection=true \
        trust-server-certificate=true \
    --target-sql-connection authentication="SqlAuthentication" \
        data-source="<YourTargetServer>.database.windows.net" \
        user-name="<YourTargetUser>" \
        password="<YourTargetPassword>" \
        encrypt-connection=true \
        trust-server-certificate=true \
    --table-list "[Person].[Person]" "[Person].[EmailAddress]" "[Sales].[Customer]" \  # Specify tables to migrate
    --scope "/subscriptions/<YourSubscription>/resourceGroups/<YourResourceGroup>/providers/Microsoft.Sql/servers/<YourTargetServer>" \
    --migration-service "/subscriptions/<YourSubscription>/resourceGroups/<YourResourceGroup>/providers/Microsoft.DataMigration/sqlMigrationServices/<YourMigrationService>"

```

The Database Migration Service optimizes the migration process by skipping empty tables, even if you select them.

#### Migration status

There are a few statuses that keep you updated on the progress of the migration.

* **Preparing for copy**: The service is in the process of disabling autostats, triggers, and indexes in the target table.
* **Copying**: The data copy from the source database to the target database is in progress.
* **Copy finished**: Data copy is finished, and the service is waiting on other tables to finish copying.
* **Rebuilding indexes**: The service is rebuilding indexes on target tables.
* **Succeeded**: All data is copied and the indexes are rebuilt.

### Monitor migration using Azure CLI

You can check the status of your migration using the `az datamigration sql-db show` command:

```
## Check the status of the database migration
az datamigration sql-db show \
    --resource-group "<YourResourceGroup>" \
    --sqldb-instance-name "<YourTargetServer>" \
    --target-db-name "<YourTargetDB>" \
    --expand "MigrationStatusDetails"                   # Include detailed migration status

```

This command returns detailed information about the migration, including the current status and any errors encountered.

#### Wait for migration completion

You can use the `wait` command to pause script execution until the migration completes:

```
## Wait for the migration to complete before continuing
az datamigration sql-db wait \
    --resource-group "<YourResourceGroup>" \
    --sqldb-instance-name "<YourTargetServer>" \
    --target-db-name "<YourTargetDB>" \
    --created                                           # Wait until migration is created/completed

```

#### Cancel a migration

If you need to stop an in\-progress migration:

```
## Cancel an in-progress migration
az datamigration sql-db cancel \
    --resource-group "<YourResourceGroup>" \
    --sqldb-instance-name "<YourTargetServer>" \
    --target-db-name "<YourTargetDB>" \
    --migration-operation-id "<YourMigrationOperationId>"  # ID from the migration operation

```

### Monitor migration from the Azure portal

You can also monitor the migration activity using Azure Database Migration Service in the Azure portal.

To monitor your database migration, go to the Azure portal and find your instance of the Database Migration Service. Once you've located the service, you can view its instance overview. Select **Monitor migrations** to access detailed information about your ongoing database migration.

After the migration status is **Succeeded**, navigate to the target server, and validate the target database. Check the database schema and data.

### Performance considerations

Migration speed heavily depends on the target Azure SQL Database SKU and the self\-hosted Integration Runtime host. We strongly recommend that you scale up your Azure SQL Database compute resources before initiating the migration process for an optimal migration experience.

When deciding on the server to install the self\-hosted integration runtime, make sure this machine can handle the CPU and memory load of the data copy operation.

Azure SQL Database migration can be slow with a large volume of tables due to the time Azure Data Factory (ADF) takes to start activities, even for small tables.

Tables with large blob columns may fail to migrate due to timeout.

We recommend up to 10 concurrent database migrations per self\-hosted integration runtime on a single computer. Scale out the self\-hosted runtime or create separate instances on different computers to increase the concurrent database migrations.

### Migrate at scale using PowerShell

You can also perform an offline migration of the database from SQL Server on\-premises to an Azure SQL Database by using PowerShell.

The following example migrates the *AdventureWorks* database to Azure SQL Database.

```
## Set up secure credentials for source and target connections
$sourcePass = ConvertTo-SecureString "<YourSourcePassword>" -AsPlainText -Force
$targetPass = ConvertTo-SecureString "<YourTargetPassword>" -AsPlainText -Force

## Start the database migration to Azure SQL Database
New-AzDataMigrationToSqlDb `
    -ResourceGroupName "<YourResourceGroup>" `              # Name of your Azure resource group
    -SqlDbInstanceName "<YourTargetServer>" `               # Name of the target Azure SQL Database server
    -Kind "SqlDb" `
    -TargetDbName "<YourTargetDB>" `                        # Name of the target database
    -SourceDatabaseName "<YourSourceDB>" `                  # Name of the source database
    -SourceSqlConnectionAuthentication SQLAuthentication `
    -SourceSqlConnectionDataSource "<YourSourceServer>" `   # Source SQL Server hostname or IP
    -SourceSqlConnectionUserName "<YourSourceUser>" `       # Source SQL Server username
    -SourceSqlConnectionPassword $sourcePass `
    -Scope "/subscriptions/<YourSubscription>/resourceGroups/<YourResourceGroup>/providers/Microsoft.Sql/servers/<YourTargetServer>" `
    -TargetSqlConnectionAuthentication SQLAuthentication `
    -TargetSqlConnectionDataSource "<YourTargetServer>.database.windows.net" `
    -TargetSqlConnectionUserName "<YourTargetUser>" `       # Target database username
    -TargetSqlConnectionPassword $targetPass `
    -MigrationService "/subscriptions/<YourSubscription>/resourceGroups/<YourResourceGroup>/providers/Microsoft.DataMigration/SqlMigrationServices/<YourMigrationService>"

```

The following example migrates a subset of tables from the *AdventureWorks* database.

```
## Migrate specific tables from source to target database
New-AzDataMigrationToSqlDb `
    -ResourceGroupName "<YourResourceGroup>" `
    -SqlDbInstanceName "<YourTargetServer>" `
    -Kind "SqlDb" `
    -TargetDbName "<YourTargetDB>" `
    -SourceDatabaseName "<YourSourceDB>" `
    -SourceSqlConnectionAuthentication SQLAuthentication `
    -SourceSqlConnectionDataSource "<YourSourceServer>" `
    -SourceSqlConnectionUserName "<YourSourceUser>" `
    -SourceSqlConnectionPassword $sourcePass `
    -Scope "/subscriptions/<YourSubscription>/resourceGroups/<YourResourceGroup>/providers/Microsoft.Sql/servers/<YourTargetServer>" `
    -TargetSqlConnectionAuthentication SQLAuthentication `
    -TargetSqlConnectionDataSource "<YourTargetServer>.database.windows.net" `
    -TargetSqlConnectionUserName "<YourTargetUser>" `
    -TargetSqlConnectionPassword $targetPass `
    -TableList "[Person].[Person]", "[Person].[EmailAddress]" `  # Specify tables to migrate
    -MigrationService "/subscriptions/<YourSubscription>/resourceGroups/<YourResourceGroup>/providers/Microsoft.DataMigration/SqlMigrationServices/<YourMigrationService>"

```

To learn more about database migration commands, refer to the following links: [PowerShell module for data migration](/en-us/powershell/module/az.datamigration) and [Azure CLI for data migration](/en-us/cli/azure/datamigration).

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/_

## Fuentes
- [Migrate SQL Server workloads to Azure SQL Database](https://learn.microsoft.com/en-us/training/modules/migrate-sql-workloads-azure-sql-databases/?WT.mc_id=api_CatalogApi)
