# Migrate on-premises PostgreSQL databases to Azure Database for PostgreSQL

> Curso: Migrate open-source databases to Azure (wwl-migrating-open-source-workloads-to-azure) · Seccion: Migrate open-source databases to Azure
> Duracion estimada: 70 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure Database for PostgeSQL is an adapted version of PostgreSQL to take full advantage of the Azure platform. It's closely integrated with Azure services and is fully managed by Microsoft. Microsoft handles the updates and patches to the software, and provide an SLA guarantee of 99\.99% availability.

You work as a database developer for an online retailer. Their systems store information in a database that currently runs using PostgreSQL on an Azure VM. As part of a hardware rationalization exercise, AdventureWorks want to move the database to an Azure\-managed database. Your company wants to reduce the management overhead of keeping PostgreSQL updated and performant.

In this module, you'll learn about the benefits of migrating PostgreSQL workloads to Azure, and the features that Azure provides to help manage and optimize PostgreSQL systems. You'll see how to create an instance of the Azure Database for PostgreSQL service, and then you'll learn how to migrate on\-premises PostgreSQL databases to Azure. You'll also see how to reconfigure an application that uses the database to connect to Azure instead.

### Learning objectives

By the end of this module, you'll be able to:

* Describe the features and limitations of Azure Database for PostgreSQL.
* Migrate an on\-premises PostgreSQL database to Azure Database for PostgreSQL.
* Reconfigure existing applications that use your on\-premises PostgreSQL databases to connect to Azure Database for PostgreSQL.

---

## Introduction to Azure Database for PostgreSQL

Azure Database for PostgreSQL is available in multiserver versions.

As a database developer with many years experience of running and managing on\-premises PostgreSQL installations, you want to explore how Azure Database for PostgreSQL supports and scales its features.

In this unit, you'll explore the pricing, version support, replication, and scaling options of Azure Database for PostgreSQL.

### Azure Database for PostgreSQL

The Azure Database for PostgreSQL service is an implementation of the community version of PostgreSQL. The service provides the common features used by typical PostgreSQL systems, including geo\-spatial support and full\-text search.

Microsoft has adapted PostgreSQL for the Azure platform, and it's closely integrated with many Azure services. The Azure Database for PostgreSQL service is fully managed by Microsoft. Microsoft handle updates and patches to the software, and provide an SLA of 99\.99% availability. This means you can just focus on the databases and applications running, using the service.

You can deploy multiple databases in each instance of this service.

#### Pricing tiers

When you create an instance of the Azure Database for PostgreSQL service, you specify the compute and storage resources that you want to allocate by selecting a *Pricing tier*. A pricing tier combines the number of virtual processor cores, the amount of storage available, and various backup options. The more resources you allocate, the higher the cost.

The Azure Database for PostgreSQL service uses storage to hold your database files, temporary files, transaction logs, and the server logs. You can optionally specify that you want the storage available to be increased when you get close to the current capacity. If you don't select this option, servers that run out of storage will continue running, but operate as read\-only.

The Azure portal groups pricing tiers into three broad ranges:

* **Basic**, which is suitable for small systems and development environments, but has variable I/O performance.
* **General Purpose**, which provides predictable performance, up to 6000 IOPS, depending on the number of processor cores and the storage space available.
* **Memory Optimized**, which uses up to 32 memory\-optimized virtual processor cores, and also provides predictable performance of up to 6000 IOPS.

Microsoft also has a *Large storage* option in preview, which can provision up to 16 TB of storage and support up to 20,000 IOPS.

You can fine\-tune the number of processor cores and storage that you require. You can scale up and down the processing resources—you can't scale storage down, only up—and switch between the General Purpose and Memory Optimized pricing tiers as necessary after you've created your databases. You only pay for what you need.

Note

If you change the number of processor cores, Azure creates a new server with this compute allocation. When the server is running, client connections are switched to the new server. This switch can take up to a minute. During this interval, no new connections can be made, and any in\-flight transactions will be rolled back.

If you only change the storage size of backup options, there's no interruption in service.

The pricing tier and the processing resources allocated determine the maximum number of concurrent connections the service will support. For example, if you select the General Purpose pricing tier and allocate 64 virtual cores, the service supports 1900 concurrent connections. The Basic Tier, with two virtual cores, handles up to 100 concurrent connections. Azure itself requires five of these connections to monitor the server. If you exceed the number of available connections, clients will receive the error **FATAL: sorry, too many clients already**.

Prices can change. Visit the [Azure Database for PostgreSQL pricing](https://azure.microsoft.com/pricing/details/postgresql/server/) page for the latest information.

#### Server parameters

In an on\-premises installation of PostgreSQL, you set server configuration parameters in the *postgresql.conf* file. Use Azure Database for PostgreSQL to modify configuration parameters through the **Server parameters** page. Not all parameters for an on\-premises installation of PostgreSQL are relevant to Azure Database for PostgreSQL, so the Server parameters page only lists those parameters that are appropriate to Azure.

Changes to parameters marked as *Dynamic* take effect immediately. Static parameters require a server restart. You restart the server using the **Restart** button on the **Overview** page in the portal:

#### High availability

Azure Database for PostgreSQL is a highly available service. It contains built\-in failure detection and failover mechanisms. If a processing node stalls due to a hardware or software issue, a new node will be switched in to replace it. Any connections currently using that node will be dropped but automatically opened against the new node. Any transactions being performed by the failing node will be rolled back. For this reason, you should always ensure that clients are configured to detect and retry failing operations.

#### Supported PostgreSQL versions

The Azure Database for PostgreSQL service currently supports PostgreSQL version 11, back to version 9\.5\. You specify which version of PostgreSQL to use when you create an instance of the service. Microsoft aim to update the service as new versions of PostgreSQL become available, and will maintain compatibility with the previous two major versions.

Azure automatically manages upgrades to your databases between minor versions of PostgreSQL—but not major versions. For example, if you have a database that uses PostgreSQL version 10, Azure can automatically upgrade the database to version 10\.1\. If you want to switch to version 11, you must export your data from the databases in the current service instance, create a new instance of the Azure Database for PostgreSQL service, and import your data into this new instance.

#### Coordinator and worker nodes

Data is sharded and distributed between worker nodes. The query engine in the coordinator can parallelize complex queries, directing the processing towards the appropriate worker nodes. Worker nodes are selected according to which shards hold the data being processed. The coordinator then accumulates the results from the worker nodes before sending them back to the client. More straightforward queries might be performed using only a single worker node. Clients also connect to the coordinator, and never communicate directly with a worker node.

You can scale the number of worker nodes up and down in your service, as required.

#### Distributing data

You distribute data across worker nodes by creating *distributed* tables. A distributed table is split into shards, and each shard is allocated to storage on a worker node. You indicate how to split the data by defining a column as the *distribution* column. The data is sharded based on the values of the data in this column. When you design a distributed table, it's important to select the distribution column carefully; you should use a column with a large number of distinct values that would typically be used to group related rows. For example, in a table for an e\-commerce system that stores information about customers' orders, the customer ID might be a reasonable distribution column. All orders for a given customer will be held in the same shard, but orders for all customers will be spread across shards.

You can also create *reference* tables. These tables contain lookup data, such as the names of cities or status codes. A reference table is replicated in its entirety to every worker node. The data in a reference table should be relatively static; each change requires updating every copy of the table.

Finally, you can create *local* tables. A local table isn't sharded, but is stored on the coordinator node. Use local tables for holding small tables with data that's unlikely to be required by joins. Examples include the names of users and their login details.

### Replicate data in Azure Database for PostgreSQL

Read\-only replicas are useful for handling read\-intensive workloads. Client connections can be spread across replicas, easing the burden on a single instance of the service. If your clients are located in different regions of the world, you use cross\-region replication to position data close to each set of clients, and reduce latency.

You can also use replicas as part of a contingency plan for disaster recovery. If the primary server becomes unavailable, you might still be able to connect to a replica.

Note

If the primary is lost or deleted, all read\-only replicas become read\-write servers instead. However, these servers will be independent of each other, so any changes made to the data in one server will not be copied to the remaining servers.

#### Establishing a replica

A read\-only replica contains a copy of the databases held in the original server—referred to as the *primary*. You use the Azure portal or the CLI to create a replica of a primary.

When you create a read\-only replica, Azure creates a new instance of the Azure Database for PostgreSQL service, and then copies the databases from the primary server to the new server. The replica runs in read\-only mode. Any attempt to modify data will fail.

#### Replica lag

Replication is not synchronous, and any changes made to data in the primary server might take some time to appear in the replicas. Client applications that connect to replicas must be able to cope with this level of eventual consistency. Azure Monitor enables you to track the time lag in replication by using the **Max Lag Across Replicas** and **Replica Lag** metrics.

### Management and monitoring

You can use familiar tools such as **pgAdmin** to connect to Azure Database for PostgreSQL to manage and monitor your databases. However, some server\-focused functionality, such as performing server backup and restore, are not available because the server is managed and maintained by Microsoft.

#### Azure tools for monitoring Azure Database for PostgreSQL

Azure provides an extensive set of services that you use to monitor server and database performance, and troubleshoot issues. These services enable you to view how PostgreSQL is utilizing the Azure resources you've allocated. You use this information to assess whether you need to scale your system, modify the structure of tables and indexes in your databases, and visualize runtime statistics and other events. The services available include:

* **Azure Monitor**. The Azure Database for PostgreSQL provides metrics that enable you to track items such as CPU and storage utilization, I/O rates, memory occupancy, the number of active connections, and replication lag:
* **Server Logs**. Azure makes the logs available for each PostgreSQL server. You download them from the Azure portal:
* **Query Store and Query Performance Insights**. The Azure Database for PostgreSQL stores information about the queries run against databases on the server, and saves them in a database named *azure\_sys*, in the *query\_store* schema. You query the *query\_store.qs\_view* view to see this information. By default, Azure Database for PostgreSQL doesn't capture any query information as it imposes a small overhead, but you can enable tracking by setting the *pg\_qs.query\_capture\_mode* server property to *ALL* or *TOP*.

You also configure Query Store to capture information about queries that spend time waiting. A query might have to wait while another query releases a lock on a table, or because the query is performing a lot of I/O, or because memory is running short. You see this information in the *query\_store.runtime\_stats\_view* view.

If you prefer to visualize these statistics rather than running SQL statements, use Query Performance Insight in the Azure portal:
* **Performance Recommendations**. The Performance Recommendations utility, also available in the Azure portal, examines the queries your applications are running. It also looks at the structures in the database, and recommends how to organize your data— and whether you should consider adding or removing indexes.

### Client connectivity

Azure Database for PostgreSQL runs behind a firewall. To access your service and database you must add a firewall rule for the IP address ranges from which your clients connect. If you need to access the service from within Azure—such as an application running using Azure App Services—you must also enable access to Azure services.

#### Configure the firewall

The simplest way to configure the firewall is to use the Connection Security settings for your service in the Azure portal. Add a rule for each client IP address range. You also use this page to enforce SSL connections to your service.

You click **Add Client IP** in the toolbar to add the IP address of your desktop computer.

If you've configured read\-only replicas, you must add a firewall rule to each one to make them accessible to clients.

#### Client connection libraries

If you're writing your own client applications, you must use the appropriate database driver to connect to a PostgreSQL database. Many of these libraries are programming\-language dependent. They are maintained by independent third parties. Azure Database for PostgreSQL supports client libraries for Python, PHP, Node.js, Java, Ruby, Go, C\# (.NET), ODBC, C, and C\+\+.

#### Client retry logic

As mentioned earlier, some events—such as failover during high availability recovery, and scaling up the CPU resources—can cause a brief loss in connectivity. Any transactions in progress will be rolled back. Azure Database for PostgreSQL automatically redirects a connected client to a working node, but any operations being performed by the client at that time will return an error. You should treat this occurrence as a transient exception. Your application code should be prepared to catch these exceptions and retry them.

### PostgreSQL features supported in Azure Database for PostgreSQL

Azure Database for PostgreSQL supports most features commonly used by PostgreSQL databases, but there are some exceptions. If you require an unsupported feature, you'll either need to rework your database and application code to remove this dependency, or consider running PostgreSQL in a virtual machine. In the latter case, you'll have to take responsibility for managing and maintaining the server.

### Supported extensions in Azure Database for PostgreSQL

Much PostgreSQL functionality is encapsulated in extensions. Extensions are packages of SQL objects and code that are stored on the server—they can be loaded into a database using the `CREATE EXTENSION` command. Azure Database for PostgreSQL currently provides many commonly\-used extensions for:

* Data types
* Functions
* Full\-text search
* Indexes (bloom, btree\_gist, and btree\_gin)
* The plpgsql language
* PostGIS
* Many administrative functions

You use the *dblink* and *postgres\_fdw* packages to connect one PostgreSQL server to another—this enables code in one server to access data held in another. In Azure Database for PostgreSQL, you can only connect between servers created using Azure Database for PostgreSQL. You can't create outbound connections to PostgreSQL servers hosted elsewhere, such as on\-premises or in a virtual machine.

Note

The list of supported extensions is continuously under review, and can change. You'll generate a list of the extensions supported with the following query. Note that you can't create your own custom extensions and upload them to Azure Database for PostgreSQL:

```
SELECT * FROM pg_available_extensions;

```

Azure Database for PostgreSQL includes the *TimescaleDB* database as an optional extension. This database contains time\-oriented analytical functions and other features that support time\-series workloads. To use this database, select the *TIMESCALEDB* option in the *shared\_preload\_libraries* server parameter, and then restart the server.

### Language support for stored procedures and triggers

Support for languages other than plpgsql typically requires you to compile your stored procedure or trigger code separately, and upload the compiled library to the server. Mainly because of security reasons, you can't do this with Azure Database for PostgreSQL. If you have code written in other languages, you'll have to port it to plpgsql.

---

## Application migration

Once you've migrated your database from on\-premises to Azure, you need to update your existing applications so that they can access the PostgreSQL in its new location.

Your original on\-premises server and database will contain roles that define the privileges associated with users, the operations they can do, and the objects they perform these operations over. Azure Database for PostgreSQL uses the same authentication and authorization mechanisms as PostgreSQL running on\-premises.

In this unit, you'll explore the updates you need to make to your applications to connect to your newly migrated Azure Database for PostgreSQL.

### Create the user roles manually

When you transfer a PostgreSQL database to Azure Database for PostgreSQL using the Azure Database Migration Service, the roles and role assignments aren't copied. You must manually recreate the necessary roles and user accounts for the administrator and users of the tables in the target database. You use the psql or pgAdmin utilities to do these tasks. Run the `CREATE ROLE` command. You use the `GRANT` command to assign the necessary privileges to a role. For example:

```
CREATE ROLE myuseraccount WITH LOGIN NOSUPERUSER CREATEDB PASSWORD 'mY!P@ss0rd';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuseraccount;

```

Note

You also use the `createuser` command from the bash prompt to create PostgreSQL roles.

To view the existing roles in the on\-premises database, run the following SQL statement:

```
SELECT rolname
FROM pg_roles;

```

You can use the **\\du** command in the psql utility to display the privileges assigned to roles.

```
                              List of roles
   Role name   |               Attributes                                   | Member of
---------------+------------------------------------------------------------+-----------
 azureuser     | Superuser, Create DB                                       | {}
 myuseraccount | Create DB                                                  | {}
 postgres      | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

```

Note

Note that Azure Database for PostgreSQL adds some roles of its own. These roles include `azure_pg_admin`, `azure_superuser`, and the administrator user that you specified when you created the service. You sign in using your administrative accounts, but the other two roles are reserved for use by Azure—you shouldn't attempt to use them.

### Reconfigure applications

Reconfiguring an application to connect to Azure Database for PostgreSQL is a straightforward process. However, it's more important to determine a strategy for migration applications.

#### Considerations when reconfiguring PostgreSQL applications

In a corporate environment, you might have many applications running against the same PostgreSQL databases. There could be a large number of users running these applications. You want to be assured that, when you switch from the existing system to Azure Database for PostgreSQL, your systems will still work, users can continue doing their jobs, and your business\-critical operations remain operational. Module 1, Lesson 2, *Considerations for migration*, discussed many of the issues in general terms. When you migrate a PostgreSQL database to Azure, there are some specifics to note:

* If you're performing an offline migration, the data in the original PostgreSQL database and the new databases running on Azure can start to diverge quickly if the old database is still being used. An offline migration is suitable when you take a system out of operation entirely for a short while, and then switch all applications to the new system before starting up again. This approach might not be possible for a business\-critical system. If you're migrating to PostgreSQL running on an Azure virtual machine, you configure PostgreSQL replication between your on\-premises system and that running in Azure. Native PostgreSQL replication operates in one direction only, but third\-party solutions are available that support bidirectional replication between PostgreSQL servers (these solutions won't work with Azure Database for PostgreSQL).
* If you're performing an online migration, the Azure Database for PostgreSQL service sets up replication from the on\-premises database to the database running in Azure. After the initial data transfer, replication ensures that any changes made in the on\-premises database are copied to the database in Azure, but not the other way round.

In both cases, you should ensure that you don't lose live data through an accidental overwrite. For example, in the online scenario, an application connected to the database running in Azure Database for PostgreSQL could have its changes blindly overwritten by an application still using the on\-premises database. With this in mind, you should consider the following approaches:

* Migrate applications based on their workload type. An application that accesses the data for reading only can move safely to the database running in Azure Database for PostgreSQL, and will see all changes made by applications still using the on\-premises database. You can also adopt the converse strategy if read\-only applications don't require fully up\-to\-date data.
* Migrate users based on their workload type. This strategy is similar to the previous one, except that you might have users that only generate reports while others modify the data. You might have the same application configured to connect to the appropriate database according to user requirements.
* Migrate applications based on the datasets they use. If different applications utilize different subsets of the data, you might be able to migrate these applications independently of each other.

#### Reconfiguring an application

To reconfigure an application, you point it at the new database. Most well\-written applications will isolate the connection logic, and this should be the only part of the code that requires changing. In many cases, the connection information might be stored as configuration information—you only need to update that information.

You'll find the connection information for your Azure Database for PostgreSQL service in the Azure portal, on the **Connection strings** page for your service. Azure provides the information for many common programming languages and frameworks.

#### Open network ports

As mentioned in Lesson 1 of this module, Azure Database for PostgreSQL is a protected service that runs behind a firewall. Clients can't connect unless their IP address is recognized by the service. You must add the IP addresses, or address block ranges, for clients running applications that need to connect to your databases.

### Test and verify applications

Before you switch your applications and users to the new database, it's important to ensure that you've configured everything correctly.

Start by "dry\-running" applications and connect each role to ensure the correct functionality is available.

Next, perform "soak tests" to mimic the typical number of users running representative workloads concurrently for a period of time. Monitor the system, and verify that you've allocated sufficient resources to your Azure Database for PostgreSQL service.

At this point, you can start to roll out the system to users. It might be beneficial to implement some form of "canary testing", where a small subset of users is transferred to the system unawares. This gives you an unbiased opinion as to whether users are having the same, better, or worse experience with the new database.

---

## Exercise: Migrate an on\-premises PostgreSQL database to Azure Database for PostgreSQL

In this exercise, you'll migrate a PostgreSQL database to Azure. You'll migrate an existing PostgreSQL database running on a virtual machine to Azure Database for PostgreSQL.

You work as a database developer for the AdventureWorks organization. AdventureWorks has been selling bicycles and bicycle parts directly to end\-consumer and distributors for over a decade. Their systems store information in a database that currently runs using PostgreSQL on an Azure VM. As part of a hardware rationalization exercise, AdventureWorks want to move the database to an Azure managed database. You have been asked to perform this migration.

Important

Azure Data Migration Service isn't supported in the free Azure sandbox environment. You can perform these steps in your own personal subscription, or just follow along to understand how to migrate your database.

#### Setup the environment

Run these Azure CLI commands in the Cloud Shell to create a virtual machine, running PostgreSQL, with a copy of the adventureworks database. The last commands will print the IP address of the new virtual machine.

```
az account list-locations -o table

az group create \
    --name migrate-postgresql \
    --location <CHOOSE A LOCATION FROM ABOVE NEAR YOU>

az vm create \
    --resource-group migrate-postgresql \
    --name postgresqlvm \
    --admin-username azureuser \
    --admin-password Pa55w.rdDemo \
    --image Ubuntu2204 \
    --public-ip-address-allocation static \
    --public-ip-sku Standard \
    --vnet-name postgresqlvnet \
    --nsg ""

az vm run-command invoke \
    --resource-group migrate-postgresql \
    --name postgresqlvm \
    --command-id RunShellScript \
    --scripts "
## Install PostgreSQL
sudo echo deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main > /etc/apt/sources.list.d/pgdg.list
sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get -y update
sudo apt-get -y install postgresql-10
## Clone exercise code
sudo git clone https://github.com/MicrosoftLearning/DP-070-Migrate-Open-Source-Workloads-to-Azure.git /home/azureuser/workshop    
## Configure PostgreSQL
sudo service postgresql stop
sudo bash << EOF
    printf \"listen_addresses = '*'\nwal_level = logical\nmax_replication_slots = 5\nmax_wal_senders = 10\n\" >> /etc/postgresql/10/main/postgresql.conf
    printf \"host    all             all             0.0.0.0/0               md5\n\" >> /etc/postgresql/10/main/pg_hba.conf
EOF
sudo service postgresql start

## Add the azureuser role and adventure works
sudo bash << EOF
su postgres << EOC
printf \"create role azureuser with login;alter role azureuser createdb;alter role azureuser password 'Pa55w.rd';alter role azureuser superuser;create database adventureworks;grant all privileges on database adventureworks to azureuser; \" | psql
EOC
EOF

PGPASSWORD=Pa55w.rd psql -h localhost -U azureuser adventureworks -E -q -f /home/azureuser/workshop/migration_samples/setup/postgresql/adventureworks/adventureworks.sql
"

az vm open-port \
    --resource-group migrate-postgresql \
    --name postgresqlvm \
    --priority 200 \
    --port '22'

az vm open-port \
    --resource-group migrate-postgresql \
    --name postgresqlvm \
    --priority 300 \
    --port '5432'

echo Setup Complete

SQLIP="$(az vm list-ip-addresses \
    --resource-group migrate-postgresql \
    --name postgresqlvm \
    --query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" \
    --output tsv)"

echo $SQLIP

```

These commands will take approximately 5 minutes to complete. You don't need to wait, you can continue with the steps below.

### Create the Azure Database for PostgreSQL flexible server

1. Using a web browser, open a new tab and navigate to the [Azure portal](https://portal.azure.com/?azure-portal=true).
2. In the search bar, type **Azure Database for PostgreSQL flexible servers**.
3. On the **Azure Database for PostgreSQL flexible servers** page, select **\+ Create**.
4. On the **Flexible server** page, enter the following details, and then select **Review \+ create**:

| Property | Value |
| --- | --- |
| Resource group | **migrate\-postgresql** |
| Server name | **adventureworks*nnn***, where *nnn* is a suffix of your choice to make the server name unique |
| Location | Select your nearest location |
| PostgreSQL version | **13** |
| Compute \+ storage | Select **Configure server**, select the **Basic** pricing tier, and then select **OK** |
| Admin username | **awadmin** |
| Password | **Pa55w.rdDemo** |
| Confirm password | **Pa55w.rdDemo** |
5. On the **Review \+ create** page, select **Create**. Wait for the service to be created before continuing.
6. When the service has been created, select **Go to resource**.
7. Select **Connection security**.
8. On the **Connection security page**, set **Allow access to Azure services** to **Yes**.
9. In the list of firewall rules, add a rule named **VM**, and set the **START IP ADDRESS** and **END IP ADDRESS** to the IP address of the virtual machine running the PostgreSQL server you created earlier.
10. Select **Add current client IP address**, to enable your client machine to connect to the database.
11. **Save**, and wait for the firewall rules to be updated.
12. At the Cloud Shell prompt, run the following command to create a new database in your Azure Database for PostgreSQL service. Replace *\[nnn]* with the suffix you used when you created the Azure Database for PostgreSQL service. Replace *\[resource group]* with the name of the resource group you specified for the service:

```
az postgres flexible-server create \
  --name azureadventureworks \
  --resource-group migrate-postgresql

```

If the database is created successfully, you should see a message similar to the following:

```
{
  "charset": "UTF8",
  "collation": "English_United States.1252",
  "name": "azureadventureworks",
  "resourceGroup": "migrate-postgresql",
  "type": "Microsoft.DBforPostgreSQL/servers/databases"
}

```

#### Export the schema to use on the target database

You'll now connect to your existing PostgreSQL VM using the Cloud Shell to export your database schema.

1. Run this Azure CLI command to see the IP address for your existing VM.

```
SQLIP="$(az vm list-ip-addresses \
    --resource-group migrate-postgresql \
    --name postgresqlvm \
    --query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" \
    --output tsv)"

echo $SQLIP

```
2. Connect to your old database server using SSH. Enter **Pa55w.rdDemo** for the password.

```
ssh azureuser@$SQLIP

```
3. Run the following command to connect to the database on the virtual machine. The password for the **azureuser** user in the PostgreSQL server running on the virtual machine is **Pa55w.rd**:

```
psql adventureworks

```
4. Grant replication permission to azureuser:

```
ALTER ROLE azureuser REPLICATION;

```
5. Close the **psql** utility with the **\\q** command.
6. At the bash prompt, run the following command to export the schema for the **adventureworks** database to a file named **adventureworks\_schema.sql**

```
pg_dump -o  -d adventureworks -s > adventureworks_schema.sql

```

#### Import the schema into the target database

1. Run the following command to connect to the azureadventureworks\[nnn] server. Replace the two instances of *\[nnn]* with the suffix for your service. Note that the username has the *@adventureworks\[nnn]* suffix. At the password prompt, enter **Pa55w.rdDemo**.

```
psql -h adventureworks[nnn].postgres.database.azure.com -U awadmin@adventureworks[nnn] -d postgres

```
2. Run the following commands to create a user named **azureuser** and set the password for this user to **Pa55w.rd**. The third statement gives the **azureuser** user the necessary privileges to create and manage objects in the **azureadventureworks** database. The **azure\_pg\_admin** role enables the **azureuser** user to install and use extensions in the database.

```
CREATE ROLE azureuser WITH LOGIN;
ALTER ROLE azureuser PASSWORD 'Pa55w.rd';
GRANT ALL PRIVILEGES ON DATABASE azureadventureworks TO azureuser;
GRANT azure_pg_admin TO azureuser;

```
3. Close the **psql** utility with the **\\q** command.
4. Import the schema for the **adventureworks** database to the **azureadventureworks** database running on your Azure Database for PostgreSQL service. You are performing the import as **azureuser**, so enter the password **Pa55w.rd** when prompted.

```
psql -h adventureworks[nnn].postgres.database.azure.com -U azureuser@adventureworks[nnn] -d azureadventureworks -E -q -f adventureworks_schema.sql

```

You will see a series of messages as each item is created. The script should complete without any errors.
5. Run the following command. The **findkeys.sql** script generates another SQL script named **dropkeys.sql** that will remove all the foreign keys from the tables in the **azureadventureworks** database. You will run the **dropkeys.sql** script shortly:

```
psql -h adventureworks[nnn].postgres.database.azure.com -U azureuser@adventureworks[nnn] -d azureadventureworks -f workshop/migration_samples/setup/postgresql/adventureworks/findkeys.sql -o dropkeys.sql -t

```
6. Run the following command. The **createkeys.sql** script generates another SQL script named **addkeys.sql** that will recreate all the foreign keys. You will run the **addkeys.sql** script after you have migrated the database:

```
psql -h adventureworks[nnn].postgres.database.azure.com -U azureuser@adventureworks[nnn] -d azureadventureworks -f workshop/migration_samples/setup/postgresql/adventureworks/createkeys.sql -o addkeys.sql -t

```
7. Run the *dropkeys.sql* script:

```
psql -h adventureworks[nnn].postgres.database.azure.com -U azureuser@adventureworks[nnn] -d azureadventureworks -f dropkeys.sql

```

You will see a series **ALTER TABLE** messages displayed, as the foreign keys are dropped.
8. Stat the psql utility again and connect to the **azureadventureworks** database.

```
psql -h adventureworks[nnn].postgres.database.azure.com -U azureuser@adventureworks[nnn] -d azureadventureworks

```
9. Run the following query to find the details of any remaining foreign keys:

```
SELECT constraint_type, table_schema, table_name, constraint_name
FROM information_schema.table_constraints
WHERE constraint_type = 'FOREIGN KEY';

```

This query should return an empty result set. However, if any foreign keys still exist, for each foreign key, run the following command:

```
ALTER TABLE [table_schema].[table_name] DROP CONSTRAINT [constraint_name];

```
10. After you have removed any remaining foreign keys, execute the following SQL statement to display the triggers in the database:

```
SELECT trigger_name
FROM information_schema.triggers;

```

This query should also return an empty result set, indicating that the database contains no triggers. If the database did contain triggers, you would have to disable them before migrating the data, and re\-enable them afterwards.
11. Close the *psql* utility with the **\\q** command.

### Perform an online migration using the Database Migration Service

1. Switch back to the Azure portal.
2. Select **All services**, select **Subscriptions**, and then select your subscription.
3. On your subscription page, under **Settings**, select **Resource providers**.
4. In the **Filter by name** box, type **DataMigration**, and then select **Microsoft.DataMigration**.
5. If the **Microsoft.DataMigration** isn't registered, select **Register**, and wait for the **Status** to change to **Registered**. It might be necessary to select **Refresh** to see the status change.
6. Select **Create a resource**, in the **Search the Marketplace** box type **Azure Database Migration Service**, and then press Enter.
7. On the **Azure Database Migration Service** page, select **Create**.
8. On the **Create Migration Service** page, enter the following details, and then select **Next: Networking\>\>**.

| Property | Value |
| --- | --- |
| Select a resource group | **migrate\-postgresql** |
| Service name | **adventureworks\_migration\_service** |
| Location | Select your nearest location |
| Service mode | **Azure** |
| Pricing tier | **Premium, with 4 vCores** |
9. On the **Networking** page, select the **postgresqlvnet/posgresqlvmSubnet** virtual network. This network was created as part of the setup.
10. Select **Review \+ create** and then select **Create**. Wait while the Database Migration Service is created. This will take a few minutes.
11. When the service has been created, select **Go to resource**.
12. Select **New Migration Project**.
13. On the **New migration project** page, enter the following details, and then select **Create and run activity**.

| Property | Value |
| --- | --- |
| Project name | **adventureworks\_migration\_project** |
| Source server type | **PostgreSQL** |
| Target Database for PostgreSQL | **Azure Database for PostgreSQL** |
| Choose type of activity | **Online data migration** |
14. When the **Migration Wizard** starts, on the **Select source** page, enter the following details, and then select **Next: Select target\>\>**.

| Property | Value |
| --- | --- |
| Source server name | nn.nn.nn.nn *(The IP address of the Azure virtual machine running PostgreSQL)* |
| Server port | **5432** |
| Database | **adventureworks** |
| User Name | **azureuser** |
| Password | **Pa55w.rd** |
| Trust server certificate | **Selected** |
| Encrypt connection | **Selected** |
15. On the **Select target** page, enter the following details, and then select **Next: Select databases\>\>**.

| Property | Value |
| --- | --- |
| Azure PostgreSQL | **adventureworks\[nnn]** |
| Database | **azureadventureworks** |
| User Name | **azureuser@adventureworks\[nnn]** |
| Password | **Pa55w.rd** |
16. on the **Select databases** page, select the **adventureworks** database and map it to **azureadventureworks**. Deselect the **postgres** database. Select **Next: Select tables\>\>**.
17. On the **Select tables** page, select **Next: Configure migration settings\>\>**.
18. On the **Configure migration settings** page, expand the **adventureworks** dropdown, expand the **Advanced online migration settings dropdown**, verify that **Maximum number of instances to load in parallel** is set to 5, and then select **Next: Summary\>\>**.
19. On the **Summary** page, in the **Activity name** box type **AdventureWorks\_Migration\_Activity**, and then select **Start migration**.
20. On the **AdventureWorks\_Migration\_Activity** page, select **Refresh** at 15 second intervals. You'll see the status of the migration operation as it progresses. Wait until the **MIGRATION DETAILS** column changes to **Ready to cutover**.
21. Switch back to the Cloud Shell.
22. Run the following command to recreate the foreign keys in the **azureadventureworks** database. You generated the **addkeys.sql** script earlier:

```
psql -h adventureworks[nnn].postgres.database.azure.com -U azureuser@adventureworks[nnn] -d azureadventureworks -f addkeys.sql

```

You will see a series of **ALTER TABLE** statements as the foreign keys are added. You may see an error concerning the *SpecialOfferProduct* table, which you can ignore for now. This is due to a UNIQUE constraint that doesn't get transferred correctly. In the real world, you should retrieve the details of this constraint from the source database using the following query:

```
SELECT constraint_type, table_schema, table_name, constraint_name
FROM information_schema.table_constraints
WHERE constraint_type = 'UNIQUE';

```

You could then manually reinstate this constraint in the target database in Azure Database for PostgreSQL.

There should be no other errors.

### Modify data, and cut over to the new database

1. Return to the **AdventureWorks\_Migration\_Activity** page in the Azure portal.
2. Select the **adventureworks** database.
3. On the **adventureworks** page, verify that the **Full load completed** value is **66** and that all other values are **0**.
4. Switch back to the Cloud Shell.
5. Run the following command to connect to the **adventureworks** database running using PostgreSQL on the virtual machine:

```
psql adventureworks

```
6. Execute the following SQL statements to display, and then remove orders 43659, 43660, and 43661 from the database. Note that the database implements a cascading delete on the **salesorderheader** table, which automatically deletes the corresponding rows from the **salesorderdetail** table.

```
SELECT * FROM sales.salesorderheader WHERE salesorderid IN (43659, 43660, 43661);
SELECT * FROM sales.salesorderdetail WHERE salesorderid IN (43659, 43660, 43661);
DELETE FROM sales.salesorderheader WHERE salesorderid IN (43659, 43660, 43661);

```
7. Close the **psql** utility with the **\\q** command.
8. Return to the **adventureworks** page in the Azure portal, and select **Refresh**. Verify that 32 changes have been applied.
9. Select **Start Cutover**.
10. On the **Complete cutover** page, select **Confirm**, and then select **Apply**. Wait until the status changes to **Completed**.
11. Return to the Cloud Shell.
12. Run the following command to connect to the **azureadventureworks** database running using your Azure Database for PostgreSQL service:

```
psql -h adventureworks[nnn].postgres.database.azure.com -U azureuser@adventureworks[nnn] -d azureadventureworks

```

The password is **Pa55w.rd**.
13. Execute the following SQL statements to display the orders and order details in the database. Quit after the first page of each table. The purpose of these queries is to show that the data has been transferred:

```
SELECT * FROM sales.salesorderheader;
SELECT * FROM sales.salesorderdetail;

```
14. Run the following SQL statements to display the orders and details for orders 43659, 43660, and 43661\.

```
SELECT * FROM sales.salesorderheader WHERE salesorderid IN (43659, 43660, 43661);
SELECT * FROM sales.salesorderdetail WHERE salesorderid IN (43659, 43660, 43661);

```

Both queries should return 0 rows.
15. Close the *psql* utility with the **\\q** command.

#### Clean up the resources you've created

Important

If you've performed these steps in your own personal subscription, you can delete the resources individually or delete the resource group to delete the entire set of resources. Resources left running can cost you money.

1. Using the Cloud Shell run this command to delete the resource group:

```
az group delete --name migrate-postgresql

```

---

## Summary

In this module, you learned about the benefits of migrating PostgreSQL workloads to Azure, and the features that Azure provides to help manage and optimize PostgreSQL systems. You saw how to create an instance of the Azure Database for PostgreSQL service, and then you migrated an on\-premises PostgreSQL database to Azure. You also reconfigured an application that uses the database to connect to Azure.

### Takeaways

In this module, you:

* Learned about the features and limitations of Azure Database for PostgreSQL.
* Migrated an on\-premises PostgreSQL database to Azure Database for PostgreSQL.
* Reconfigured an application that used your on\-premises PostgreSQL database to connect to Azure Database for PostgreSQL instead.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/migrate-on-premises-postgresql-databases/_

## Fuentes
- [Migrate on-premises PostgreSQL databases to Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/migrate-on-premises-postgresql-databases/?WT.mc_id=api_CatalogApi)
