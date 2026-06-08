# Migrate on-premises MySQL databases to Azure Database for MySQL

> Curso: Migrate open-source databases to Azure (wwl-migrating-open-source-workloads-to-azure) · Seccion: Migrate open-source databases to Azure
> Duracion estimada: 69 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Database for MySQL is an adapted version of MySQL to take full advantage of the Azure platform. It's closely integrated with Azure services and is fully managed by Microsoft. Microsoft handles the updates and patches to the software, and provide an SLA guarantee of 99\.99% availability.

You work as a database developer for an online retailer. Their systems store information in a database that currently runs using MySQL on an Azure VM. As part of a hardware rationalization exercise, AdventureWorks want to move the database to an Azure\-managed database. Your company wants to reduce the management overhead of keeping MySQL updated and performant.

In this module, you'll learn about the benefits of migrating MySQL workloads to Azure, and the features that Azure provides to help manage and optimize MySQL systems. You'll see how to create an instance of the Azure Database for MySQL service, and learn how to migrate on\-premises MySQL databases to Azure. You'll also see how to reconfigure an application that uses the database to connect to Azure instead.

### Learning objectives

By the end of this module, you'll be able to:

* Describe the features and limitations of Azure Database for MySQL.
* Migrate an on\-premises MySQL database to Azure Database for MySQL.
* Reconfigure existing applications that use your on\-premises MySQL databases to connect to Azure Database for MySQL.

---

## Introduction to Azure Database for MySQL

Azure Database for MySQL can be deployed as a Flexible Server (Preview) to host your organizations MySQL database in Azure. It's a fully managed database as a service that can handle mission\-critical workloads with predictable performance and dynamic scalability.

As a database developer with many years experience of running and managing on\-premises MySQL installations, you want to explore how Azure Database for MySQL supports and scales its features.

In this unit, you'll explore the pricing, version support, replication, and scaling options of Azure Database for PostgreSQL.

### Understand the benefits of Azure Database for MySQL

Azure Database for MySQL is provisioned as an Azure Database for MySQL server. The Azure Database for MySQL server is equivalent to an on\-premises MySQL server and provides a central point to administer multiple MySQL databases.

To create an Azure Database for MySQL database, you must first provision an Azure Database for MySQL Server. An Azure Database for MySQL server is the parent of one or many databases and provides the namespace for the databases. If you delete the server, you'll delete all databases that it contains.

#### What does Azure Database for MySQL server provide?

The Azure Database for MySQL service includes high availability at no additional cost and scalability as required. You only pay for what you use. Automatic backups are provided, with point\-in\-time restore.

The server provides connection security to enforce firewall rules and, optionally, require SSL connections. Numerous server parameters enable you to configure server settings such as lock modes, maximum number of connections, and timeouts. Changes to parameters that are marked as *Dynamic* take effect immediately. Static parameters require a server restart. You restart the server using the **Restart** button on the **Overview** page in the portal.

Azure Database for MySQL servers include monitoring functionality to add alerts, and to view metrics and logs.

#### Pricing tiers

Pricing tiers enable a wide range of performance and capacity from one to 64 vCores and from 5 GB to 4 TB of storage. The basic pricing tier is designed for light compute workloads and supports up to two vCores with 2 GB of memory per core. The general purpose pricing tier will suit most business workloads and supports from two to 64 vCores with 5 GB of memory per core. The memory\-optimized pricing tier supports two to 32 vCores, has 10 GB of memory per vCore, and is intended for high performance workloads, including real\-time data analysis. Although you can switch between general purpose and memory\-optimized pricing tiers, and change the number of vCores or storage within seconds, you can't move to or from the basic pricing tier.

There are connection limits based on pricing tiers and the number of vCores. See [Limitations in Azure Database for MySQL](/en-us/azure/mysql/concepts-limits) for more information.

#### Versioning and upgrades

Azure Database for MySQL supports version 5\.6 (with bug fix release 5\.6\.42\), 5\.7 (with bug fix release 5\.7\.24\), and 8\.0 (with bug fix release 8\.0\.15\).

Note

A gateway redirects connections to server instances. MySQL clients will display the version of the gateway rather than the version of the server instance.
To view the version of the server instance, use the SELECT VERSION(); command.

Bug fix versions are applied automatically, but version upgrades are not supported. To upgrade from one version to another, you should perform a dump and restore.

#### Scalability

As mentioned, you can't change to or from the basic pricing tier. However, you can alter the number of vCores, the hardware generation, the storage volume, and the backup retention period. You can also switch between the general purpose and memory\-optimized pricing tiers.

Note that storage is only increased, not decreased, and can be set to auto\-grow. If auto\-grow is enabled, storage grows by 5 GB when available storage is less than 1 GB or 10% of storage volume (whichever is greater) for servers with less than 100 GB of storage. For servers with more than 100 GB, storage increases by 5% when available storage is less than 5%.

#### High availability

Azure Database for MySQL includes a financially\-backed service level agreement (SLA) for availability of 99\.99%. If there's a hardware failure or service deployment, a new node is automatically created, and storage is attached to this node. Failover will be complete within tens of seconds.

If an Azure Database for MySQL server instance is scaled up or scaled down, a similar process occurs with the data storage being attached to the new instance. If a failover takes place, a scale up or scale down occurs, or there's any interruption in internet traffic between the client and Azure, a transient connectivity error might happen at the client. It's important to have retry logic in applications. In the case of a failover, a gateway will direct traffic to the new node with no configuration required at the client.

For information on handling transient errors, see [Handling of transient connectivity errors for Azure Database for MySQL](/en-us/azure/mysql/concepts-connectivity).

### Replicate data in Azure Database for MySQL

#### Data\-in Replication

Data\-in Replication uses the native replication functionality of MySQL to replicate data from an external MySQL Server into Azure Database for MySQL. This is useful if you want to provision a hybrid environment with an existing on\-premises MySQL instance and an Azure\-based replica. This scenario provides local data to users in a globally distributed system. You could also use Data\-in Replication to replicate data from a virtual machine or MySQL database service hosted by another cloud provider.

##### Considerations for Data\-in Replication

Here are some factors to consider for Data\-in Replication:

* The source and replica servers must be the same version—and at least version 5\.6\.
* The source and replica should use the InnoDB engine.
* Every table must have a primary key.
* The Azure Database for MySQL server must have a **General Purpose** or **Memory Optimized** pricing tier.
* You should have the rights to create users and configure binary logging on the source server.
* The **mysql system database** is not replicated. Accounts and permissions are not replicated from the source server to the replica, and should be created manually.

##### Steps to configure Data\-in Replication

There's a number of steps to configure Data\-in Replication:

* Create an Azure Database for MySQL Server to be used as a host for the replica, and create any necessary user accounts and privileges.
* Configure replication on the source server.
* Dump and restore the source server.
* Use Data\-in Replication stored procedures to configure the target server.

See [How to configure Azure Database for MySQL Data\-in Replication](/en-us/azure/mysql/howto-data-in-replication) for more information.

#### Read replicas

Read replicas use native MySQL replication technology to create asynchronous replica instances of Azure Database for MySQL servers. The replica servers are read\-only and there can be up to five replicas for each source server. For each read replica, the monthly cost is billed based on the vCores and storage it uses.

##### Uses for read replicas

**Reporting servers**

By creating a read\-only replica of the source server, you direct all reporting, BI, and analytical workloads to the replica. This removes the workload from the source server and reduces conflicts while the source server runs its write\-intensive workloads.

**Bringing data close to users**

You create cross\-region replicas to bring data close to users and improve their read speeds. Cross\-region replicas can be in a universal replica region or the paired region of the source server. The available regions are listed when you create a replica server.

##### Configure read replicas

You configure a read replica in the Azure portal:

You then specify the name and region of the replica:

Note

Read replicas aren't available in the basic pricing tier.

For more information on read replicas, see [Read replicas in Azure Database for MySQL](/en-us/azure/mysql/concepts-read-replicas).

### Management and monitoring

Azure Database for MySQL has a wide array of monitoring tools to help you optimize your server, be notified of events, and proactively respond to metrics. You can also use familiar MySQL administration tools, such as recent versions of MySQL Workbench, PHPMyAdmin, and Navicat, to manage and monitor Azure Database for MySQL servers:

#### Azure tools for monitoring Azure Database for MySQL

The tools available in the Azure portal for managing and monitoring Azure Database for MySQL include the following:

* **Azure metrics**. Metrics provide numeric data every minute and are stored for 30 days. There's a wide array of metrics that you use to monitor your server—you can also configure alerts to respond to metrics.

See [Azure Monitor data platform](/en-us/azure/azure-monitor/platform/data-platform) for more information.
* **Server and audit logs**. You enable server logs to monitor slow queries and provide audit logging for your server. Server logs are available outside SQL Database for MySQL through Azure Diagnostic Logs.

See [Slow query logs in Azure Database for MySQL](/en-us/azure/mysql/concepts-server-logs) for more information.
Audit logs are a preview feature to provide audit logging to track database activity. To turn on audit logging, set the **audit\_log\_enabled** parameter to **ON**.
For more information on audit logs, see [Audit Logs in Azure Database for MySQL](/en-us/azure/mysql/concepts-audit-logs).
* **Query Store**. This is used to track the performance of your server over time and give troubleshooting information. Query Store retains query history and run\-time statistics so you can identify resource intensive or long running queries.
To enable Query Store, set the **query\_store\_capture\_mode** server parameter to **ALL**:

To view query store data about queries, run the following query:

```
SELECT * FROM mysql.query_store;

```

To view data about wait statistics, run the following query:

```
SELECT * FROM mysql.query_store_wait_stats;

```

Note

Query Store is a preview feature and is not available in the basic pricing tier.

For more information on Query Store, see [Monitor Azure Database for MySQL performance with Query Store](/en-us/azure/mysql/concepts-query-store).
* **Query Performance Insight**. Query Performance Insight displays data from Query Store as visualizations to enable you to identify queries that affect performance. Query Performance Insight is in the **Intelligent Performance** section of your Azure Database for MySQL, in the Azure portal.

Note

Query Performance Insight is a preview feature and is not available in the basic pricing tier.

For more information on Query Performance Insight, see [Query Performance Insight in Azure Database for MySQL](/en-us/azure/mysql/concepts-query-performance-insight).
* **Performance Recommendations**. Performance Recommendations uses data from the Query Store to analyze workloads, and combines this with database characteristics to suggest new indexes to improve performance. Performance Recommendations is in the **Intelligent Performance** section of your Azure Database for MySQL in the Azure portal.

Note

Performance Recommendations is a preview feature and is not available in the basic pricing tier.

For more information on Performance Recommendations, see [Performance Recommendations in Azure Database for MySQL](/en-us/azure/mysql/concepts-performance-recommendations).

### Client connectivity

#### MySQL drivers

Azure Database for MySQL uses the MySQL community edition and is compatible with a wide range of drivers—it supports a variety of programming languages. Connection strings are provided in the Azure portal:

For more information on MySQL drivers, see [MySQL drivers and management tools compatible with Azure Database for MySQL](/en-us/azure/mysql/flexible-server/how-to-data-in-replication)

#### Configure the firewall

The simplest way to configure the firewall is to use the Connection Security settings for your service in the Azure portal. Add a rule for each client IP address range. You can also use this page to enforce SSL connections to your service.

You click **Add Client IP** in the toolbar to add the IP address of your desktop computer.

If you've configured read\-only replicas, you must add a firewall rule to each one to make them accessible to clients.

#### Transient connection errors

When you connect to a database over the internet, transient connection errors are inevitable and should be handled by client applications.

For information on transient connectivity errors, see [Handling of transient connectivity errors for Azure Database for MySQL](/en-us/azure/mysql/concepts-connectivity).

### MySQL features that aren't supported in Azure Database for MySQL

While most features in MySQL are available in Azure Database for MySQL, some aren't supported. You should review these features to ensure you mitigate any potential issues when migrating.

#### Storage engines

Azure Database for MySQL supports the InnoDB and MEMORY storage engines. InnoDB is the default storage engine for MySQL, providing a balance between high performance and high reliability. All new tables in MySQL will use the InnoDB storage engine unless specified otherwise.

For more information on the InnoDB storage engine, see [Introduction to InnoDB](https://dev.mysql.com/doc/refman/5.7/en/innodb-introduction.html).

To store data in memory, the MEMORY storage engine is available. This data is at risk from any form of crash or outage—the MEMORY storage engine should only be used as a temporary, high performance store.

For more information on the MEMORY storage engine, see[The MEMORY Storage Engine](https://dev.mysql.com/doc/refman/5.7/en/memory-storage-engine.html).

MyISAM, BLACKHOLE, ARCHIVE, and FEDERATED storage engines are not supported in Azure Database for MySQL. MyISAM data should be converted to the InnoDB storage engine. BLACKHOLE, ARCHIVE, and FEDERATED storage engines have specialist roles and are not used as typical data stores.

#### Privileges and roles

The **DBA** role is not exposed because many server settings and parameters can break transaction rules and degrade performance. For similar reasons, the **SUPER** privilege is restricted, as is the **DEFINER** clause that uses the **SUPER** privilege.

#### Restore

Two restore features function differently in Azure Database for MySQL:

* Point\-in\-time restore creates a new server with an identical configuration to the server that it's based on.
* You can't restore a deleted server.

---

## Application migration

Once you've migrated your database from on\-premises to Azure, you need to update your existing applications so that they can access the MySQL in its new location.

Your original on\-premises server and database will contain roles that define the privileges associated with users, the operations they can do, and the objects they perform these operations over. Azure Database for MySQL uses the same authentication and authorization mechanisms as PostgreSQL running on\-premises.

In this unit, you'll explore the updates you need to make to your applications to connect to your newly migrated Azure Database for MySQL.

### Create the users manually

Your original on\-premises server and database will contain users, the operations they perform, and the objects over which they do these operations. Azure Database for MySQL uses the same authentication and authorization mechanisms as MySQL running on\-premises.

When you transfer a MySQL database to Azure Database for MySQL using the Azure Database Migration Service, the users aren't copied. You must manually recreate the necessary user accounts for the administrator and users of the tables in the target database. To do these tasks, you use the SQL language or a utility such as MySQL Workbench. Run the `CREATE USER` command. You use the `GRANT` command to assign the necessary privileges to a user. For example:

```
CREATE USER 'myuseraccount'@'%' IDENTIFIED BY 'mY!P@ss0rd';
GRANT ALL PRIVILEGES ON DATABASE [Database Name].* TO myuseraccount;
FLUSH PRIVILEGES;

```

To view the existing grants in the on\-premises database, run the following SQL statement:

```
USE [Database Name];

SHOW GRANTS FOR 'myuseraccount'@'%';;

```

### Reconfigure applications

Reconfiguring an application to connect to Azure Database for MySQL is a straightforward process. However, it's crucial that you develop a strategy for migrating applications.

#### Considerations when reconfiguring MySQL applications

In a corporate environment, you might have many applications running against the same MySQL databases. There could be a large number of users running these applications. You want to be assured that, when you switch from the existing system to Azure Database for MySQL, your systems will still work, users can continue doing their jobs, and business\-critical operations remain operational. Module 1, Lesson 2, *Considerations for migration*, discussed many of the issues in general terms.

When migrating a MySQL database to Azure, there are some specifics to consider:

* If you're performing an offline migration, the data in the original MySQL database and the new databases running on Azure might start to diverge quickly if the old database is still being used. An offline migration is suitable when you take a system entirely out of operation for a short while, and then switch all applications to the new system before starting up again. This approach might not be possible for a business\-critical system. If you're migrating to MySQL running on an Azure virtual machine, you can configure MySQL replication between your on\-premises system and that running in Azure. Native MySQL replication operates in one direction only, but third\-party solutions are available that support bidirectional replication between MySQL servers. These solutions won't work with Azure Database for MySQL.
* If you're performing an online migration, the Azure Database for MySQL service sets up replication from the on\-premises database to the database running in Azure. After the initial data transfer, replication ensures that any changes made in the on\-premises database are copied to the database in Azure, but not the other way round.

In both cases, you should ensure that you don't lose live data through an accidental overwrite. For example, in the online scenario, an application connected to the database running in Azure Database for MySQL could have its changes blindly overwritten by an application still using the on\-premises database. Therefore, you should consider the following approaches:

* Migrate applications based on their workload type. An application that accesses the data for reading only can move safely to the database running in Azure Database for MySQL, and will see all changes made by applications still using the on\-premises database. You can also adopt the converse strategy if read\-only applications don't require fully up\-to\-data data.
* Migrate users based on their workload type. This strategy is similar to the previous one, except that you might have users who only generate reports while others modify the data. You can have the same application configured to connect to the appropriate database according to the user's requirements.
* Migrate applications based on the datasets they use. If different applications use different subsets of the data, you might be able to migrate these applications independently of each other.

#### Reconfiguring an application

To reconfigure an application, you point it at the new database. Most well\-written applications should isolate the connection logic—this should be the only part of the code that requires changing. In many cases, connection information might be stored as configuration information, so you just need to update that information.

You'll find the connection information for your Azure Database for MySQL service in the Azure portal, on the **Connection strings** page for your Azure Database for MySQL service. Azure provides the information for many common programming languages and frameworks.

#### Open network ports

As mentioned in Lesson 1 of this module, Azure Database for MySQL is a protected service that runs behind a firewall. Clients can't connect unless their IP address is recognized by the service. You must add the IP addresses, or address block ranges, for clients running applications that need to connect to your databases.

### Test and verify applications

Before you switch applications and users to the new database, it's important to ensure that you've configured everything correctly.

Start by "dry\-running" applications and connect as each role to ensure the correct functionality is available.

Next, perform "soak tests" to mimic the number of users running typical workloads concurrently for a period of time. Monitor the system, and verify that you've allocated sufficient resources to your Azure Database for MySQL service.

You can now start to roll out the system to users. It might be beneficial to implement some form of "canary testing", where a small subset of users is transferred to the system unawares. This gives you an unbiased opinion as to whether users are having the same, better, or worse experience with the new database.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/migrate-on-premises-mysql-databases/_

## Fuentes
- [Migrate on-premises MySQL databases to Azure Database for MySQL](https://learn.microsoft.com/en-us/training/modules/migrate-on-premises-mysql-databases/?WT.mc_id=api_CatalogApi)
