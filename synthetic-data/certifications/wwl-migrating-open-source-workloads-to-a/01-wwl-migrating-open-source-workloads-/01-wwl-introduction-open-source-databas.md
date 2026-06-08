# Introduction to open-source database migration on Azure

> Curso: Migrate open-source databases to Azure (wwl-migrating-open-source-workloads-to-azure) · Seccion: Migrate open-source databases to Azure
> Duracion estimada: 50 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

If you have an on\-premises database that runs on MySQL, MariaDB, or PostgreSQL, and you want to migrate to the cloud, Azure provides several services that can host those databases and help you to realize all the scaling, availability, and cost advantages of cloud computing.

Suppose you work at a start\-up technology company that has recently been created to market a new product developed in a university. You have several databases that were implemented on both MySQL and PostgreSQL that support your Computer Aided Design (CAD) and supplier communications systems. You have ambitious targets for rapid growth and you want to ensure that the databases can scale up quickly when needed. You also want to set up offices around the globe in the first year or two of trading. You've decided to migrate the databases to the cloud to support these requirements. You want to know what technologies are available in Azure to host these databases and you want to plan your migration.

In this module, you'll learn about the issues and considerations for migrating on\-premises open\-source databases to Azure. You'll be introduced to the services that Azure provides to help you migrate and host your databases. You'll look at what you need to consider when planning a migration project, and you'll learn about different approaches to migrating databases.

By the end of this module, you'll be able to migrate an on\-premises database on an open\-source platform to Azure.

### Learning objectives

By the end of this module, you'll be able to:

* Describe the features and services available in Azure for hosting an open\-source database.
* Explain the key considerations for implementing a migration project.
* Describe different approaches that you can take for migrating databases.

---

## Introduction to open\-source database migration on Azure

* Module
* 6 Units

 Intermediate
 

 Data Engineer
 

 Azure
 

In this module, you'll learn about the issues and considerations for migrating on\-premises open\-source databases to Azure, the services that Azure provides to help you migrate your databases, and how to plan a migration.

### Learning objectives

By the end of this module, you'll be able to:

* Describe the features and services available in Azure for hosting an open\-source database.
* Explain the key considerations for implementing a migration project.
* Describe different approaches that you can take for migrating databases.

### Prerequisites

* Knowledge of MySQL or PostgreSQL database management systems, including application development for these systems, administration, backup, and recovery techniques, such as import/export and backup/restore.
* Knowledge of Azure fundamental concepts, and experience using the Azure portal.

### Get started with Azure

Choose the Azure account that's right for you. Pay as you go or try Azure free for up to 30 days. [Sign up.](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)

* [Introduction](1-introduction)
min
* [MySQL and PostgreSQL database services in Azure](2-mysql-postgresql-database-services)
min
* [Considerations for migration](3-considerations-migration)
min
* [Approaches to migration](4-approaches-migration)
min
* [Module assessment](5-knowledge-check)
min
* [Summary](6-summary)
min

---

Take the module assessment

 Module Assessment Results

Assess your understanding of this module. Sign in and answer all questions correctly to earn a pass designation on your profile.

[Start](#)

---

## Considerations for migration

A business system running on\-premises can have an architecture that's coupled to other services operating within the same environment. It's important to understand the relationships between a system you wish to migrate, and the other applications and services your organization is currently using.

In your technology start\-up company, the supplier database is used to ensure components are always in stock and arrive just\-in\-time for their use in the manufacturing process. Stock controllers use mobile devices to update this database as consignments arrive and buyers use a website to monitor stock levels and identify the best time to order. Managers use a set of business\-critical reports to monitor the process and improve efficiency. You want to ensure that none of these users are negatively affected by the migration to Azure.

Here, you'll learn how to plan and execute a smooth database migration into the cloud.

#### Investigate dependencies

In a complex system, a component rarely functions entirely independently. Instead, it makes calls to other processes and components. Databases, for example, might depend on directory services that host user accounts. When you move a database into the cloud, can you access that directory service? If not, how will users sign in? When you overlook a dependency like this, there might be a total failure of the database.

To mitigate risks, check whether your database depends on services such as the following:

* Directory services, such as Active Directory.
* Other stores of security principals.
* Other databases.
* Web APIs or other network services.

Also remember that other components might depend on your database. If you move the database without reconfiguring the dependent components, what are the consequences? For example, if you move a product catalog database, and the public\-facing website depends on it to determine what products to present to users, will the move cause an interruption in service?

Check to see if any of these types of component depend on your database:

* Websites and web APIs.
* Client apps, such as mobile apps and desktop software.
* Other databases.
* Reports.
* Data warehouses.

To make these checks, talk to the stakeholders, administrators, and developers involved with each database and system component. Consult the documentation then, if you're not confident that you understand the behavior of the systems, consider running tests, such as network captures to observe behavior.

#### Prepare to fall back

In any migration project, you should always be prepared for a failure. In a database migration project to the cloud, the worst eventuality is that the new database becomes unavailable and users can't do their jobs. It's common to mitigate this risk, which might have a large impact on your company's profitability, by planning to roll back to the original, unmodified database on\-premises.

For the fall\-back plan, consider:

* How to ensure you can fall back to a database that's untouched by the failed migration? For example, it's highly recommended to take a full database backup, just before you begin the migration.
* How long is it acceptable for the database to be offline, if you need to fall back?
* How much budget do you have for the fall\-back plan? For example, can you afford to replicate the database to a dedicated fall\-back server? If so, you can switch this server off just before the migration. To fall back, you boot up this server. You would immediately have a database that's unaffected by the migration, without having to restore it from backup.

### Offline versus online migration

To migrate a database, you have at least two options:

Note

The **online** option is not currently available for **MySQL databases** in Data Migration Service.

* Halt the system, transfer the database, then reconfigure and restart the system to use the new database. This is an offline migration.
* Keep the system running while you move the database to its new location, roll forward transactions being performed against the original database to the new database while the migration is proceeding, and then switch your applications to connect to the new database. This is an online migration.

It's simpler to perform an offline migration, where users can't change the data while the migration takes place. However, if your database is busy or critical to the success of your organization, that might not be possible.

#### Offline migrations

Suppose that your database supports a team of analysts who all work in a single time zone during normal business hours. The team usually doesn't work at weekends. Between 6:00 PM on Friday and 9:00 AM on Sunday, the database isn't often used.

In this situation, you could do an offline migration over the weekend, by following these steps:

1. Take the database offline, after all transactions have completed on Friday evening.
2. Take a full backup or export of the database.
3. Shut down the on\-premises server and keep it in case you need to fall back.
4. Restore the database on the target cloud system.
5. Bring the target system online.
6. Reconfigure clients to connect to the cloud database.

In this case, an offline migration is possible because there's a long period when an interruption in service has little effect on users. During this time, you can do a complete backup and restore of the database, knowing that you won't miss any changes.

#### Online migrations

Now consider another database that supports a sales app. Sales staff are distributed around the world and also work at weekends. There isn't a period of low activity, the database is always busy and, if you take the database offline for a significant period, it will impact users. Sales activity is business\-critical, so an interruption in service will have a direct effect on the organization's bottom line.

In cases like this, consider performing an online migration. In an online migration, downtime is limited to the time it takes to switch to the new database. Use a tool such as the Azure Data Migration Service to execute an online migration. Online migrations have the following differences to offline migrations:

* You don't move the original database offline before taking a backup or export.
* While the migration is in progress, changes apply to the old database.
* The migration tool ensures that these changes are copied to the new database before the switch over. This is often achieved by reconfiguring the old database to replicate changes to the new one.

### Application migration

After you've migrated a database, how (and when) should you cut over to the new system and update applications to use the new database? You might:

* Move applications one\-by\-one to the new database.
* Move subsets of users.
* Adopt a combination of both approaches.

The intention is that you perform application migration in small stages that can be easily rolled back if something goes awry. Regardless of whether you've followed an offline or online approach to database migration, you should still have a working configuration located at the original source. In theory, you'll be able to switch back to the original source quickly. But if the data is constantly changing, you need to consider where these changes have been made.

* In an offline migration, the source and destinations are independent of each other. Users and applications might no longer see a consistent view of the data. In a transactional system, this situation is likely to be unacceptable. In this case, you would need to maintain some form of bidirectional replication between databases while both systems remain live. Alternatively, if the purpose of an application is to generate monthly or weekly reports, generate sales projections, or perform other statistical operations, this lack of consistency might not be so worrying. Such applications take a "long view" of the data, rather than being dependent on up\-to\-date data. In this latter case, transactional applications use the new database, whereas reporting applications are moved more slowly.
* In an online migration, the new database is kept synchronized with the old, usually by some form of replication. The replication process might be asynchronous, so there could be a lag. However, changes made to data in the new database won't be propagated back to the old, resulting in possible conflicts. An application running against the old database might make a conflicting change to data that's been modified in the new database. Replication will blindly overwrite the change in the new database, resulting in a "lost update".

#### Approaches to testing

If the database plays a critical role in your business, the consequences of a failure might be extensive. To increase your confidence that this won't happen, consider running performance tests against the migrated database to ensure that it copes with the load users might place upon it and respond quickly. Remember that there could be periods of peak activity, when demand is much higher than normal. You must be sure that your migrated system handles the expected workload.

Always perform some type of regression testing against the new database before allowing access to users. These tests will verify that the behavior and functionality of the system are correct.

Additionally, you should consider running a "soak test". A soak test is a load test designed to see how the system as a whole operates under pressure. A soak test stresses the new database and determines whether it's stable under high demand. A soak test runs over a significant time period to see what happens when high demand persists.

When you've established that the new system is stable, you can start to migrate users. However, you might need additional assurance that users will find the new system acceptable. At this point, you might consider "canary testing". A canary test transparently directs a small subset of users to the new system, but they aren't aware that they're accessing it. It's a form of blind test, intended to enable you to find any problems or issues with the new system. Monitor the responses from these users, and make any adjustments required.

### Maintaining parallel systems

There are several reasons why you might choose to run the old on\-premises database in parallel with the new cloud database:

* **Testing periods**. As you saw in the previous topic, it's a good idea to run canary tests against the migrated database to assess its functionality, stability, and capacity before using it to support people. Maintaining the on\-premises system in parallel gives you a quick way to revert users to the old system if there are issues with the new system.
* **Phased migrations**. One way to mitigate the impact of unexpected failures on production is to move a small number of users to the new system first, and monitor the results. If all runs smoothly, you could move other groups of users as you gain confidence in the new database. You can move users alphabetically, by department, by location, or by role, until they're all on the new database.
* **Piecemeal migrations**. Another approach is to segment the migration not by user, but by workload. For example, you could migrate the database tables that support human resources, before those that support sales.

In all these cases, there's a period when the old on\-premises database runs in parallel with the new cloud database. You must ensure that changes made to the old database are also applied to the new database and that they flow in the opposite direction. You could script this synchronization, or use a tool like Azure Data Migration Service.

If you decide to maintain parallel databases and synchronize changes, ask yourself these questions:

* **Conflict resolution**. Is it likely that a change to a row on\-premises happens at a similar time to a different change to the same row in the cloud? This would create a conflict, where it's unclear which change should be retained. How would you resolve such conflicts?
* **Network traffic**. How much network traffic will be generated while changes are synchronized between databases? Do you have enough network capacity for this traffic?
* **Latency**. When there's a change in one of the databases, what lag (if any) is acceptable before that change reaches the other database? For example, in a product catalog, you might be able to wait for up to a day before new products are visible to all users. However, if the database includes critical transactional information, such as currency exchange rates, that data should be synchronized much more frequently, if not instantaneously.

### Piecemeal migration

A piecemeal migration is where you divide a complete system into workloads and migrate one workload at a time.

#### Multiple databases

A complex system might include multiple databases that support several workloads. For example, human resources might use the *StaffDB* database, while the sales team could have mobile apps that query both the *ProductCatalogDB* database and the *OrdersDB* database.

Of course, you can choose to migrate the entire database system to the cloud in one go. This might be simpler, because you don't have to run databases both on\-premises and in the cloud. You don't need to consider how those databases communicate during the migration. However, the risks of failure are higher. A single problem might affect both the human resources team and the sales team.

Consider mitigating these risks for medium and large database systems by performing a piecemeal migration, where you move one workload at a time. In this example, you might consider migrating the *StaffDB* database first, because the problems associated with a failure would be limited to the human resources team and wouldn't prevent you from taking orders. By solving any problems that arise with the *StaffDB* migration, you'll learn lessons that apply to other workload migrations.

Next, you could think about migrating the *Product Catalog* workload to the cloud. If you do, consider questions such as:

* How do you ensure that products newly added to the catalog, are available to order?
* Do you need to synchronize any data with the *OrdersDB* database, which remains on\-premises?
* What latency is acceptable for new products to reach the *OrdersDB* database from the product catalog?

#### Single database piecemeal migrations

Even if you only have a single database that supports all the workloads, you can still consider a piecemeal migration. For example, you could divide the database into pieces like this:

* Tables that support HR operations.
* Tables that support sales.
* Tables that support analysis and reporting.

If you migrate the HR operations tables first, any problem that arises only affects HR personnel. Sales and data analysts continue to work on the old database without interruption.

Before you perform a piecemeal migration, you must fully understand the databases and how they're used by applications. For example, some tables in your database might support both sales and reporting. That means you can't cleanly divide workloads. You must synchronize these tables between on\-premises and cloud databases, until all the workloads have been migrated.

### Security concerns

Your databases might contain sensitive data, such as product details, personal staff information, and payment details—so security is always a high priority. You must decide how to protect this data during the migration and in the new database.

#### Firewall protection

In an internet\-connected application, database servers are usually protected by at least two firewalls. The first firewall separates the internet from the front\-end servers—if these servers host websites or web APIs, for example. Only TCP port 80 should be open on the outer firewall, but this port must be open for all source IP addresses, except blocked addresses.

The second firewall separates the front\-end servers from the database servers. It's recommended to publish the database service on a private port number that's not known to the outside world. On the second firewall, open this port number only for the IP addresses of the front\-end servers. This arrangement prevents any direct communication from a malicious internet user to the database servers.

If you plan to migrate database servers to Azure virtual machines, use a virtual network with Network Security Groups (NSGs) to replicate firewall rules. If you use **Azure Database for MySQL**, **Azure Database for MariaDB**, or **Azure Database for PostgreSQL**, you can create firewall rules to protect the database using the **Connection security** page for the server in the Azure portal.

#### Authentication and authorization

In most databases, you need to closely control who accesses and modifies which data. This control requires that users are positively identified when they connect to the database. This process is called **authentication** and is usually done with a username and password. Database systems such as MySQL, MariaDB, and PostgreSQL provide their own authentication mechanisms. You must ensure that you continue to authenticate users securely when you migrate your systems to the cloud.

Note

The **Azure Database for MySQL**, **Azure Database for MariaDB**, and **Azure Database for PostgreSQL** services emulate traditional MySQL, MariaDB, and PostgreSQL authentication.

When you know who the user is, you must assign them permissions to complete the tasks that are part of their job. This process is called **authorization**.

For a database migration project, you have to make sure that users are authorized correctly in the cloud database:

1. Find out where user accounts are stored in the on\-premises system. In MySQL, user accounts are usually stored in the `user` table of the `mysql` database but it's possible, for example, to integrate with user accounts stored in Active Directory.
2. Get a list of all the user accounts. In MySQL, for example, you could use this command:

```
SELECT host, user FROM mysql.user;

```
3. For each user account, find out what access they have to the database. In MySQL, for example, you could use this command for the `dbadmin@on-premises-host` user account:

```
SHOW GRANTS FOR 'dbadmin'@'on-premises-host';

```
4. Recreate each user account in the cloud database. In MySQL, for example, you could use this command to create a new account:

```
CREATE USER 'dbadmin'@'cloud-host'

```
5. Authorize each user account to the correct level of access in the cloud database. In MySQL, for example, you could use this command to permit a user to access the complete database:

```
GRANT USAGE ON *.* TO 'dbadmin'@'cloud-host'

```

#### Encryption

As data is sent across the network, it might be intercepted by a so\-called "man\-in\-the\-middle" attack. To prevent this, both **Azure Database for MySQL**, **Azure Database for MariaDB**, and **Azure Database for PostgreSQL** support Secure Sockets Layer (SSL) to encrypt communications. SSL is enforced by default, and it's highly recommended that you don't change this setting.

You might need to amend your client applications' connection settings to use SSL encryption. Discuss this topic with your developers to determine the changes, if any, that are necessary.

### Monitoring and management

Part of planning to migrate a database is to consider how database administrators will continue to perform their tasks after migration.

#### Monitoring

On\-premises database administrators are used to monitoring regularly to spot problems such as hardware bottlenecks, or contention for network access. They monitor to ensure they can fix any problems before productivity is affected. You can expect any database that's not regularly monitored to begin causing problems sooner or later.

You should take exactly the same approach to cloud databases. It might be easier to solve problems in a PaaS system like Azure, because you can add resources without buying, setting up, and configuring any hardware. However, you still need to spot developing problems, so monitoring is a high priority among your daily tasks.

Before you migrate databases into the cloud, find out what monitoring tools your administrators currently use. If those tools are compatible with your proposed cloud\-based solution, you might only need to reconnect them to the migrated databases. If not, you must investigate alternatives.

Bear in mind that Azure includes a set of performance monitoring tools, and collects a wide variety of performance counters and log data. You display this data using dashboards and charts in the Azure portal, by configuring Azure Monitor. You create custom graphs, tables, and reports, specifically designed for the needs of your administrators.

#### Management

Your database administrators use preferred tools to change the schema and content of the database on\-premises. If they use the same tools after migration, you can continue to benefit from their expertise. Start by assessing whether the existing set of tools is compatible with the proposed cloud\-hosted database. Many tools will be compatible because they're based on widely adopted standards such as SQL—but it's important to verify that compatibility. If the current management tools won't work after migration, try to identify alternatives with your administrators.

Azure includes several tools that you could use to administer MySQL, MariaDB, and PostgreSQL databases:

* **The Azure portal**. This website has powerful facilities that you use to configure, monitor, and manage databases—and all other resources that you might create in the Azure cloud.
* **Azure PowerShell**. This is a scripting execution environment and language that has a wide set of commands. Use PowerShell, which is available for Windows and Linux environments, to automate complex database administrative tasks.
* **Azure CLI**. This is a command\-line interface to Azure. Use it to manage services and resources in Azure. You can use the CLI from the Windows and Linux shell environments, and from within Bash scripts.

---

## Approaches to migration

You can take many different approaches to database migration, such and online or offline migration, backup and restore migration, or migration with custom SQL code or scripts. Each approach is most appropriate for certain business scenarios.

In your start\-up company, for example, the supplier communication database is critical and you want to try and migrate without any disruption to the service to users. This department of the company operates on a 24/7 basis and there are few predictable quiet times when you could take the database offline. The Computer Aided Design (CAD) system, by contrast, is only used during the week so you could take it offline over a weekend and migrate it to Azure.

Here, you'll learn about approaches, techniques, and tools that you can select to execute the migration.

#### When to use export and import

Export and import techniques give you control over the data and schema that's moved in the migration. Use export and import tools if you want to select which data is migrated to the new database, and perhaps clean or modify the data during migration.

Consider using export and import techniques:

* When you want to choose a subset of the tables in the on\-premises database to migrate to the cloud database.
* When you want to migrate database objects such as constraints, views, functions, procedures, and triggers, and control how these objects are set up in the cloud database.
* When you want to import data from external sources other than MySQL, MariaDB, or PostgreSQL.

For example, you might consider export and import in these scenarios:

* You want to perform a piecemeal migration where the marketing workload is migrated to the cloud and tested before the sales support workload. Both workloads use tables from the *SalesDB* database in your on\-premises system. You want to migrate the marketing tables only in the first phase of the project and the sales tables only in the second phase.
* Your on\-premises data is old and contains a mix of data that's relevant and irrelevant to the current business. You want to take the opportunity to remove old data and consider a more streamlined database schema.
* You have a large spreadsheet that contains data about products. You want to migrate this data into the cloud database.

#### Plan an export and import migration

The advantage of using export and import is the extra level of control you have over the data being migrated. However, a disadvantage is that you must plan more carefully to ensure that all the objects you need are included.

Make sure you understand how the following objects will be migrated:

* The database schema.
* Constraints including primary keys, foreign keys, and indexes.
* Views, functions, procedures, and triggers.
* User accounts and permissions.

#### Export and import for MySQL and MariaDB

You can use SQL scripts to perform selective export and import from one database to another. However, if your on\-premises database is in MySQL or MariaDB, there are several tools available to help, including:

* **MySQL Workbench**. This is a popular database design tool with a Graphical User Interface (GUI) developed by Oracle Corporation. It includes a **Data Export** tool with flexible data selection options.
* **Toad Edge**. This is a competing toolset developed by Quest. You use it to export and import data from both MySQL and PostgreSQL databases.
* **Navicat**. This database administration GUI tool is also compatible with MariaDB databases.
* **mysqlimport**. This command\-line tool can import data from text files.

Important

Azure Database for MySQL and Azure Database for MariaDB only support the InnoDB storage engine. If you have any tables that use other engines, such as the MyISAM engine, you must convert them to InnoDB before migrating to Azure.

#### PostgreSQL export and import

PostgreSQL provides the following tools that you use to export and import data:

* **pgAdmin**. This is a GUI utility for PostgreSQL administrators. It provides an interface for exporting and importing data.
* **pg\_dump**. This is a command\-line tool you use to export a database in various formats, including test. You can edit the resulting .sql files before you import them using the **psql** utility.
* **Toad Edge**. This is the same utility that you use with MySQL.

### Backup and restore

Backup and restore operations are usually done to protect a database against disasters. An exact copy of the database is taken and saved. If a disaster destroys the working copy, the backed\-up copy is restored and normal business can resume.

By restoring to a different location, you use a backup to migrate the complete database to another location, such as a database in the cloud.

#### When to use backup and restore

Backup tools make a simple and precise copy of the database. When you restore in the cloud database, you get exactly the same data and schema that you had in the on\-premises system. Use backup and restore to migrate a database:

* When you want to migrate an entire database or set of databases in one operation.
* When you don't need to make any modifications to the data, schema, or other database objects during migration.

You could consider using backup and restore to perform a migration in cases like these:

* You have a single database system that you want to lift\-and\-shift into the cloud with as little modification as possible.
* You want to perform a piecemeal migration on a system that has multiple databases. Each workload is supported by a complete database.

When you restore a database from a backup file to a cloud location, consider the quantity of data that must be sent across the network to the cloud database. To optimize this data transfer, copy the backed\-up database to a virtual machine in the same region as the destination database, and restore from there. This restore is quicker than using an on\-premises backup file and is less likely to cause contention for network bandwidth.

#### Plan a backup and restore on MySQL and MariaDB

To back up a database on an on\-premises server, you use the `mysqldump` tool at the command line. That creates a .sql file that you restore to the cloud database by passing it to the `mysql` command as a script. If you prefer a GUI tool, choose the **PHPMyAdmin** application, or **MySQL Workbench**. These GUI tools can both back up and restore the data.

Remember that Azure Database for MySQL and Azure Database for MariaDB only support the InnoDB engine. Make sure you convert all tables to InnoDB before you execute the backup.

To avoid any compatibility problems, check that the version number of MySQL or MariaDB used in the cloud matches the version number of the on\-premises database server. Azure Database for MySQL supports versions 5\.6, 5\.7, and 8\.0\. Azure Database for MariaDB supports versions 10\.2 and 10\.3\. If your on\-premises server uses an earlier version, consider upgrading to one of these versions first and troubleshooting any issues on\-premises, before you migrate to the cloud.

#### Plan a backup and restore on PostgreSQL

The equivalent command\-line backup and restore tools on PostgreSQL are `pg_dump` and `pg_restore`. For a GUI backup and restore tool, use **Toad Edge**.

### Custom application code

If you have extensive data transformation requirements or want to perform an unusual migration, consider writing your own custom code to move data from an on\-premises MySQL, PostgreSQL, or MariaDB database into the cloud.

Your custom code could take many forms. The language and framework you choose depends mostly on your development team's expertise:

* SQL Scripts generated from the database and modified or developed from scratch.
* Compiled code from a development framework such as .NET or Java.
* Scripts in PHP or Node.js.
* Shell scripts for Bash or PowerShell.

The custom code approach enables you to be extremely flexible. You customize how data is filtered, aggregated, and transformed, and you can migrate to multiple destinations or merge data from multiple sources. Use this approach if you have requirements that can't be satisfied with an out\-of\-the\-box backup or export tool.

The drawback to this approach is that it requires more investment in development time. For custom code to migrate all the data correctly, it must be extensively tested before it's run on real data. This task requires a team of skilled developers and testers, and often increases the project budget. If you're considering writing custom migration code, don't be tempted to underestimate the time and effort required to create reliable code.

### Azure Database Migration Service

Azure includes a flexible service called **Azure Database Migration Service (DMS)**, which you use to do seamless online migrations from multiple data sources into Azure data platforms. These platforms include **Azure Database for MySQL**, **Azure Database for MariaDB**, and **Azure Database for PostgreSQL**.

Consider using Azure DMS whenever you want to perform an online database migration into Azure.

#### Initial migration

To perform a migration with DMS, you complete these tasks:

1. Create a new target database within Azure on the platform of your choice.
2. Create a new Azure Database Migration Service (DMS) data migration project.
3. Generate the schema from the on\-premises source databases. If you're using MySQL, you can generate a schema with `sqldump`. If the source database is PostgreSQL, use `pg_dump`.
4. Create an empty database to act as the migration destination.
5. Apply the schema to the destination database.
6. Configure connection details for the source and destination databases in a DMS migration project.
7. Run the DMS migration project. The project transfers the data and generates a report.
8. Review the report and correct any issues that it identifies.

#### Online migrations

Azure DMS is a good tool to use for online migrations, in which the original database remains available while the migration executes. Users continue to make changes to data in the source database. Azure DMS uses replication to synchronize these changes with the migrated database. Once migration is complete, you reconfigure the user applications to connect to the migrated database.

### Migrate MySQL or MariaDB to Azure SQL Database

If you want to move a database that's hosted on\-premises on a MySQL database server into the Azure cloud—and you don't need the cloud database to run MySQL—consider migrating to Azure SQL Database. Azure SQL Database is a PaaS implementation of Microsoft's industry\-leading SQL Server database engine. It includes enterprise\-level availability, scalability, and security, and is easy to monitor and manage.

Similarly, if your on\-premises database server runs MariaDB, you can consider migrating to Azure SQL Database. The process is very similar because MariaDB is a fork of MySQL.

Azure SQL Database is more fully\-featured than Azure Database for MySQL and Azure Database for MariaDB.

Note

You might need to modify any applications that connect to your migrated database—because Azure SQL Database uses different data types, different database objects, and a different API from MySQL and MariaDB. Consult your developers to determine how much work is required to port a client application from an on\-premises MySQL or MariaDB database to a cloud Azure SQL database.

### SQL Server Migration Assistant for MySQL

If you decide to migrate from MySQL to Azure SQL Database, you can use a specialized tool: **SQL Server Migration Assistant for MySQL**. This GUI tool connects to a source MySQL database and a SQL Server database, which can be a database in the Azure SQL Database service.

When it's connected, the assistant copies the complete schema to Azure SQL Database, and converts any data types to their SQL Server equivalents. It also migrates views, procedures, triggers, and other objects. You can then start to migrate the data from MySQL to Azure SQL Database.

Note

SQL Server Migration Assistant for MySQL is not tested for migrating MariaDB databases to Azure SQL Database.

---

## Summary

In your start\-up technology company, you have several open\-source databases that were created when the organization was part of a university department. Now that you're building a global company and anticipate rapid growth around the world, you want to ensure that these databases can grow fast and be available to all parts of the world where your staff will work. By hosting MySQL, MariaDB, and PostgreSQL in Azure, you benefit from Azure's global infrastructure and instant scaling.

To build such an infrastructure on\-premises would require several expensive and robust data centers located around the world. This would take time to implement, and skilled technicians to configure and run. Azure technologies such as Azure Database for MySQL, Azure Database for MariaDB, and Azure Database for PostgreSQL, enable you to implement global database infrastructures quickly and with lower costs.

### Takeaways

In this module, you learned how to:

* Describe the features and services available in Azure for hosting an open\-source database.
* Explain the key considerations for implementing a migration project.
* Describe different approaches that you can take for migrating databases.

### Learn more

* [Azure Database for MySQL](https://azure.microsoft.com/services/mysql/)
* [Azure Database for MariaDB](https://azure.microsoft.com/services/mariadb/)
* [Azure Database for PostgreSQL](https://azure.microsoft.com/services/postgresql/)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/introduction-open-source-database-migration-azure/_

## Fuentes
- [Introduction to open-source database migration on Azure](https://learn.microsoft.com/en-us/training/modules/introduction-open-source-database-migration-azure/?WT.mc_id=api_CatalogApi)
