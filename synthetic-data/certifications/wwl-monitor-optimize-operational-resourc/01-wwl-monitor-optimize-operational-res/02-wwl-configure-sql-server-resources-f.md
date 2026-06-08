# Configure SQL Server resources for optimal performance

> Curso: Monitor and optimize operational resources in Azure SQL (wwl-monitor-optimize-operational-resources-sql-ser) · Seccion: Monitor and optimize operational resources in Azure SQL
> Duracion estimada: 35 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

One of the challenges administrators face in the cloud is balancing costs and performance. Both Azure and SQL Server provide many options for configuration to meet the needs of small and large workloads. Choosing the right storage and sizing your virtual machine are critical steps in meeting the performance needs of your applications and balancing cloud costs. Proper configuration of SQL Server resources like TempDB which can easily become a performance bottleneck, and Resource Governor, which can be used to manage multitenant workloads, are also important for properly maintaining your server performance.

### Learning objectives

In this module, you will:

* Understand your options for configuration of Azure storage
* Learn how to configure TempDB data files in SQL Server
* Learn how to choose the right type of VM for SQL Server workloads
* Understand the use cases and configuration of Resource Governor in SQL Server

---

## Describe virtual machine resizing

There are many size options for Azure Virtual Machines. For SQL Server workloads the main characteristics to look for are the amount of memory available, and the number of input and output operations (IOPs) the virtual machine can perform.

### Using constrained cores

Typically, SQL Server licenses are based on the number of cores, and Azure allocates a fixed ratio of CPU cores to memory. However, some workloads may require large amounts of memory without needing the default number of allocated CPUs. In such cases, using Azure's constrained cores can be beneficial.

With constrained cores, you can reduce the cost of software licensing while still getting the full amount of memory, storage, and I/O bandwidth. This is good for database workloads that aren't CPU\-intensive and can benefit from high memory, storage, and I/O bandwidth, while using a constrained vCPU count.

### Using general purpose virtual machines

Most SQL Server production workloads run on the general purpose or memory\-optimized families of Azure Virtual Machines. Larger workloads requiring more memory and/or CPU resources land in memory\-optimized virtual machines, but many production applications can run comfortably on general purpose virtual machines.

### Resizing virtual machines

Azure supports resizing your virtual machine. This operation does require a restart; however, restarting a virtual machine is typically a fast process. In some cases, depending on what virtual machine type you're switching to and from, you may need to deallocate your virtual machine and then resize. This operation does extend the duration of the outage but shouldn't take more than a few minutes.

---

## Optimize database storage

To optimize database storage, you should consider proportional fill and tempdb configuration.

### Understand I/O performance

I/O performance can be critical to a database application. Azure SQL abstracts you from physical file placement, but there are methods to ensure you get the I/O performance you need.

Input/output per second (IOPS) might be important to your application. Be sure you've chosen the right service tier and vCores for your IOPS needs. Understand how to measure IOPS for your queries on\-premises if you're migrating to Azure. If you have restrictions on IOPS, you might see long I/O waits. In the vCore purchasing model, you can scale up vCores or move to Business Critical or Hyperscale if you don't have enough IOPS. For production workloads, when using DTU, we recommend moving to the Premium tier.

I/O latency is another key component for I/O performance. For faster I/O latency for Azure SQL Database, consider Business Critical or Hyperscale. For faster I/O latency for SQL Managed Instance, move to Business Critical or increase the file size or the number of files for the database. Improving transaction log latency might require you to use multistatement transactions.

#### Files and filegroups

SQL Server professionals often use files and filegroups to improve I/O performance through physical file placement. Azure SQL doesn't allow users to place files on specific disk systems. However, Azure SQL has resource commitments for I/O performance regarding rates, IOPS, and latencies. In this way, abstracting the user from physical file placement can be a benefit.

Azure SQL Database only has one database file (Hyperscale typically has several), and the maximum size is configured through Azure interfaces. There's no functionality to create more files.

Azure SQL Managed Instance supports adding database files and configuring sizes, but not physical placement of files. You can use the number of files and file sizes for SQL Managed Instance to improve I/O performance. In addition, user\-defined filegroups are supported for SQL Managed Instance for manageability purposes.

### Describe proportional fill

When inserting 1 gigabyte of data into a SQL Server database with two data files, you might expect each file to increase by approximately 512 megabytes. However, this isn't always the case. SQL Server distributes data based on the size of each file. For instance, if both data files are 2 gigabytes, the data would be evenly distributed. But if one file is 10 gigabytes and the other is 1 gigabyte, around 900 MB would go into the larger file and 100 MB into the smaller one. This behavior is common in any database, but in the write\-intensive tempdb, an uneven write pattern can create a bottleneck in the largest file, as it handles more writes.

### Configure Tempdb in SQL Server

SQL Server detects the number of available CPUs during setup and configures the appropriate number of files, up to eight, with even sizing. Additionally, the behaviors of trace flags 1117 and 1118 are integrated into the database engine, but only for `tempdb`. For tempdb\-heavy workloads, it may be beneficial to increase the number of tempdb files beyond eight, matching the number of CPUs on your machine.

You use `tempdb` in the same way for both SQL Server and Azure SQL. Note, however, that your ability to configure `tempdb` is different, including the placement of files, the number and size of files, and `tempdb` configuration options.

SQL Server uses tempdb for various tasks beyond just storing user\-defined temporary tables. It's used for work tables that store intermediate query results, sorting operations, and the version store for row versioning, among other purposes. Due to this extensive utilization, it's crucial to place tempdb on the lowest latency storage available and to properly configure its data files.

The database files of `tempdb` are always automatically stored on local SSD drives, so I/O performance shouldn't be an issue.

SQL Server professionals often use more than one database file to partition allocations for `tempdb` tables. For Azure SQL Database, the number of files is scaled with the number of vCores (for example, two vCores equals four files) with a maximum of 16\. The number of files isn't configurable through T\-SQL against `tempdb`, but you can configure it by changing the deployment option. The maximum size of `tempdb` is scaled per number of vCores. You get 12 files with SQL Managed Instance, independent of vCores.

The database option `MIXED_PAGE_ALLOCATION` is set to *OFF*, and `AUTOGROW_ALL_FILES` is set to *ON*. You can't configure this, but, as with SQL Server, these are the recommended defaults.

The `tempdb` metadata optimization feature introduced in SQL Server 2019, which can alleviate heavy latch contention, isn't currently available in Azure SQL Database or Azure SQL Managed Instance.

### Database configuration

Commonly, you configure a database with the T\-SQL `ALTER DATABASE` and `ALTER DATABASE SCOPED CONFIGURATION` statements. Many of the configuration options for performance are available for Azure SQL. Consult the [ALTER DATABASE](/en-us/sql/t-sql/statements/alter-database-transact-sql) and [ALTER DATABASE SCOPED CONFIGURATION](/en-us/sql/t-sql/statements/alter-database-scoped-configuration-transact-sql) T\-SQL reference for the differences between SQL Server, Azure SQL Database, and Azure SQL Managed Instance.

In Azure SQL Database, the default recovery model is full recovery, which ensures that your database can meet Azure service\-level agreements (SLAs). This means that minimal logging for bulk operations isn't supported, except for `tempdb`, where minimal logging is allowed.

#### MAXDOP configuration

Max degree of parallelism (MAXDOP) can affect the performance of individual queries. SQL Server and Azure SQL handle `MAXDOP` in the same way. When `MAXDOP` is set to a higher value, more parallel threads are used per query, potentially speeding up query execution. However, this increased parallelism requires extra memory resources, which can lead to memory pressure and affect storage performance. For example, when compressing rowgroups into a columnstore, parallelism requires more memory, which can result in memory pressure and rowgroup trimming.

Conversely, setting MAXDOP to a lower value can reduce memory pressure, allowing the storage system to perform more efficiently. This is important in environments with limited memory resources or high storage demands. By carefully configuring MAXDOP, you can balance query performance and storage efficiency, ensuring optimal use of both CPU and storage resources.

You can configure MAXDOP in Azure SQL, similar to SQL Server, by using the following techniques:

* `ALTER DATABASE SCOPED CONFIGURATION` to configure `MAXDOP` is supported for Azure SQL.
* The stored procedure `sp_configure` for "max degree of parallelism" is supported for SQL Managed Instance.
* `MAXDOP` query hints are fully supported.
* Configuring `MAXDOP` with Resource Governor is supported for SQL Managed Instance.

---

## Control SQL Server resources

While some SQL Servers or Azure SQL managed instances are dedicated to a single application's databases, a configuration often seen in mission\-critical applications, many servers support databases for multiple applications with varying performance requirements and peak workload cycles. Balancing these differing requirements can be challenging for administrators. One effective way to manage server resources is by using Resource Governor, introduced in SQL Server 2008\.

[Resource Governor](/en-us/sql/relational-databases/resource-governor/resource-governor) is a feature in SQL Server and Azure SQL managed instances that allow granular control over CPU, physical I/O, and memory resources for incoming application requests. When enabled at the instance level, Resource Governor uses a classifier function to define how connections are treated, subdividing sessions into workload groups. Each workload group is configured to use a specific pool of system resources.

### Resource pools

A resource pool represents the physical resources available on the server. SQL Server always has two pools: default and internal, even when Resource Governor isn't enabled. The internal pool is reserved for critical SQL Server functions and can't be restricted. The default pool, along with any resource pools you explicitly define, can be configured with limits on the resources they can use. For each noninternal pool, you can specify the following limits:

* Min/Max CPU percent
* Cap of CPU percent
* Min/Max memory percent
* NUMA node affinity
* Min/Max IOPs per volume

Note

Changes to a resource pool only impact new sessions, not those already in progress. Therefore, modifying a pool won't restrict the resources of a long\-running process. The exception to this rule is external pools used with SQL Server Machine Learning Services, which can be limited by a pool change even for ongoing sessions.

All resource pool settings, except for the minimum and maximum CPU percentage, represent hard limits that can't be exceeded. The min/max CPU percentage only applies when there's CPU contention. For instance, if you set a maximum of 70%, the workload may use up to 100% of available CPU cycles when there's no contention. However, if other workloads are running, the workload will be restricted to 70%.

### Workload group

A workload group serves as a container for session requests, classified by the classifier function. Similar to resource pools, there are two built\-in groups: default and internal. Each workload group is associated with a single resource pool, but a resource pool can host multiple workload groups. By default, all connections are directed to the default workload group unless the classifier function assigns them to a user\-defined group. The default workload group utilizes the resources allocated to the default resource pool.

### Classifier function

The classifier function is run at the time a connection is established to the SQL Server instance and classifies each connection into a given workload group. If the function returns a NULL, default, or the name of the nonexistent workload group the session is transferred into the default workload group. Since the classifier is run at every connection, it should be tested for efficiency. The following image shows a sample classifier function that classifies users based on their user name.

```
CREATE FUNCTION dbo.RGClassifier()
RETURNS SYSNAME
WITH SCHEMABINDING
AS
BEGIN
DECLARE @WorkloadGroup AS SYSNAME
IF(SUSER_NAME() = 'ReportUser')
    SET @WorkloadGroup = 'ReportServerGroup'

ELSE IF (SUSER_NAME() = 'PrimaryUser')
    SET @WorkloadGroup = 'PrimaryServerGroup'
ELSE
    SET @WorkloadGroup = 'default'

RETURN @WorkloadGroup
END

```

You can increase the complexity of the function definition shown in the example, but you should verify that the more complex function doesn't impact the user performance.

### Resource Governor use cases

Resource Governor is used primarily in multitenant scenarios where a group of databases share a single SQL Server instance, and performance needs to be kept consistent for all users of the server. You can also use Resource Governor to limit the resources used by maintenance operations like consistency checks and index rebuilds, to try to guarantee sufficient resources for user queries during your maintenance windows.

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary

Proper storage configuration is crucial for the performance of your Azure Virtual Machines. To ensure optimal performance, SQL Server should run on premium disk storage or ultra disk. The Resource Provider for SQL Server can automate the creation of storage for your SQL Servers on Azure Virtual Machines, simplifying the setup process. Additionally, Resource Governor can be used to manage to differ workloads within the same SQL Server, allowing you to allocate resources efficiently and maintain balanced performance across various applications. This combination of premium storage and resource management tools ensures that your SQL Server operates smoothly and efficiently in an Azure environment.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-sql-server-resources-optimal-performance/_

## Fuentes
- [Configure SQL Server resources for optimal performance](https://learn.microsoft.com/en-us/training/modules/configure-sql-server-resources-optimal-performance/?WT.mc_id=api_CatalogApi)
