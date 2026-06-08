# Protect, monitor, and tune a migrated database

> Curso: Migrate open-source databases to Azure (wwl-migrating-open-source-workloads-to-azure) · Seccion: Migrate open-source databases to Azure
> Duracion estimada: 66 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Azure provides you with tools to enable organizations to protect, monitor, and tune their Azure databases.

Imagine you work as a database developer for an on\-line retail organization. Your company has been selling bicycles and bicycle parts directly to end\-consumers and distributors for over a decade. Their systems store information in a database that you have previously migrated to Azure Database for PostgreSQL.

In this module, you'll learn how to use the Azure features available for protecting a database and server against malicious users and disasters. This module also describes how to monitor and tune a database running in Azure Database for MySQL or PostgreSQL.

### Learning objectives

By the end of this module, you'll be able to:

* Protect a database running in Azure Database for MySQL and Azure Database for PostgreSQL.
* Monitor a database running in Azure Database for MySQL and Azure Database for PostgreSQL.
* Trace and track activity for a database running in Azure Database for MySQL and Azure Database for PostgreSQL.
* Configure read replicas for a database running in Azure Database for MySQL and Azure Database for PostgreSQL.

---

## Monitor and configure a database server

After a company has migrated their on\-premises databases to Azure Database for MySQL/PostgreSQL, they still need a way to monitor their performance.

As the database developer you've been used to using databases\-specific tools and on\-premises VM monitoring. Now that your databases are running on Azure, you can take advantage of the portal to use a single tool to monitor all the different databases.

In this unit you'll look at how Azure Monitor can support you in monitoring the health of the databases you're responsible for. Once you've uncovered issues, you'll see how to change the configuration of your databases to resolve the problems.

### How to use Azure Monitor to view the health of your databases

Use Azure Monitor to track resource use in Azure Database for MySQL/PostgreSQL. The **Metrics** page for your server in the Azure portal enables you to create charts that help to detect trends in performance, and spot anomalies.

#### Metrics for Azure Database for MySQL/PostgreSQL

The metrics available for monitoring a server fall into four broad categories:

* Storage metrics
* Connection metrics
* Data processing resource utilization metrics
* Replication metrics

##### Storage metrics

Storage metrics track the total size of your databases across the server (*Storage used*), and the current amount of storage space on the server (*Storage limit*). In an active system, you'll likely find the *Storage used* metric grows over time. If you have the auto\-growth option selected for the server, the *Storage limit* metric occasionally increases as the amount of free space diminishes. Extra storage is added whenever the amount of free space drops below 5 percent of the current usage. Use the *storage percent* metric to view the proportion of used space to free space on your server.

If your server is regularly spending time increasing storage, consider assigning more space manually. Do this in the Azure portal by selecting the **Pricing tier** page for your server, and use the **Storage** slider. Remember you're charged for storage, so don't set the storage available to high to being with.

The *Backup Storage used* metric shows how much space your backups are taking. This metric is important from a cost perspective. You aren't charged for backup storage providing it remains below the size of the storage space allocated to your server (as specified by the pricing tier). When you go above this limit, you incur charges for backup storage.

##### Connection metrics

The *Active connections* metric shows how many concurrent connections the server is currently supporting. This might not be the same as the number of concurrent users, depending on whether you've configured any type of connection pooling. Azure Database for MySQL/PostgreSQL doesn't currently provide any connection pooling capability, but you could use a proxy service such as *PgBouncer*\* (for PostgreSQL) to implement this feature. For more information, see [Performance best practices for using Azure Database for PostgreSQL – Connection Pooling](https://azure.microsoft.com/blog/performance-best-practices-for-using-azure-database-for-postgresql-connection-pooling/)

The *Failed connections* metric shows how often users have presented invalid credentials. A large number of these events over a short period of time might indicate a brute\-force attack.

##### Data processing resource utilization metrics

These metrics help you to monitor how your server handles the workload.

The *CPU percent* metric shows how busy the CPU is. High CPU usage isn't a problem, unless it has been increasing over time. CPU utilization that's over 90% and still rising indicates that your system is approaching processing capacity. You should consider scaling up to a pricing tier with more resources.

The *Memory percent* metric indicates memory occupancy. Azure Database for MySQL/PostgreSQL uses memory for caching data, and for running the processes initiated by each client request. High memory usage isn't a problem until it becomes excessive this is typically over 95%, depending on the actual amount of memory available. Very low memory availability can cause connection failures, and slow performance because of memory fragmentation. You should monitor this metric to determine whether memory occupancy is growing over time, and scale your server accordingly.

The *IO percent* metric tracks the amount of disk activity being performed by the server. Ideally, this value should be as low as possible. Disk IO is a slow operation. A high value for this metric, in conjunction with a high value for *Memory percent*, might indicate that the server has insufficient resources to cache data effectively, and is instead having to read and write data to disk storage. A degree of IO activity is inevitable, because your data must be persisted to disk at some point, and transaction logs must be maintained. In most database servers, this writing is performed by a separate process or thread that runs asynchronously.

The *Network In* and *Network Out* metrics show the volume of traffic entering and exiting the server across active connections. The limits to these figures are determined by the bandwidth of the path between the client applications and the server.

##### Replication metrics

Azure Database for PostgreSQL provides the *Max Lag Across Replicas*, and *Replica Lag* metrics to help you determine how up to date any replicas are. These metrics are only meaningful if you've configured read\-only replicas.

The *Max Lag Across Replicas* metric shows how many bytes the slowest replica is behind the master. You can only monitor this metric from the master.

The *Replica Lag* metric shows the time, in seconds, since the latest transaction was received from the master and applied to a replica. This metric only makes sense when viewed on a replica.

Azure Database for MySQL has the *Replication lag in seconds* metric. This metric, which you can only monitor from a replica, shows the number of seconds by which the replica is lagging behind the master.

#### Create charts and alerts to monitor performance

The **Metrics** page for a server in the Azure portal enables you to create charts that track metric values. Metrics are gathered at one\-minute intervals. For each metric, you specify an aggregation that determines how to report that metric.

* *Average* generates an average value for the metric in each minute
* *Max* shows the maximum value achieved during each minute
* *Min* shows the smallest value
* *Sum* totals the metric
* *Count* shows how many times the event generating the metric occurred

Not all aggregations are necessarily meaningful for every metric.

The example chart below captured the average minute\-by\-minute values for the CPU percent, Memory percent, IO percent, and Active connections metrics. You'll see that there are 101 active connections all running concurrently. The CPU and memory utilization are both stable, and the IO percent is at 0\. In this example, the client applications are performing read\-intensive workloads and the necessary data is cached in memory.

Note that there's a lag of up to five minutes between the metrics being captured and the results displayed on a chart.

If a metric indicates that a resource is reaching a critical point, you can set an alert to notify an administrator. The example below sends an email to an administrator if the memory utilization exceeds 90 percent.

### Configure server parameters

Native MySQL and PostgreSQL servers are highly configurable as both use configuration settings stored in parameter files. For PostgreSQL, this information is held in the *postgresql.conf* file. For MySQL, configuration data is stored in various *my.cnf* files. In Azure Database for MySQL/PostgreSQL, you don't have direct access to these files. Instead, you view and modify server parameters by using the Azure portal or the Azure CLI.

#### View and set parameters using the Azure portal

The server configuration parameters are available on the **Server parameters** page for your server in the Azure portal. You can modify the parameter values as appropriate for your server. The image below shows the server parameters page for Azure Database for PostgreSQL. The corresponding page for Azure Database for MySQL is similar.

Not all server configuration parameters are available because a large part of the server configuration is controlled by Azure. For example, parameters associated with memory allocation are missing. Additionally, Azure Database for MySQL doesn't support ISAM storage, so the *myisam* parameters aren't there.

Changes to parameters that are marked as *Dynamic* come into effect immediately. Parameters marked as *Static* require you to restart the server. You do this on the **Overview** page for your server.

#### View and set parameters using the Azure CLI

You can view and modify parameters programmatically with the `az mysql/postgres server configuration` commands. View the settings of every configuration parameter with `az mysql/postgres server configuration list`, and home in on a single parameter using `az mysql/postgres server configuration show [parameter-name]`. The code snippet below shows an example for Azure Database for PostgreSQL:

```
az postgres server configuration show \
    --resource-group northwindrg \
    --server-name northwind101 \
    --name vacuum_defer_cleanup_age

```

The result should look similar to this:

```
{
  "allowedValues": "0-1000000",
  "dataType": "Integer",
  "defaultValue": "0",
  "description": "Number of transactions by which VACUUM and HOT cleanup should be deferred, if any.",
  "id": "**********************",
  "name": "vacuum_defer_cleanup_age",
  "resourceGroup": "northwindrg",
  "source": "system-default",
  "type": "Microsoft.DBforPostgreSQL/servers/configurations",
  "value": "0"
}

```

The important item in the output is the **value** field, which shows the current setting for the parameter.

Use the `az mysql/postgres server configuration set` command to change the value of a configuration parameter, as follows:

```
az postgres server configuration set \
    --resource-group northwindrg \
    --server-name northwind101 \
    --name vacuum_defer_cleanup_age \
    --value 5

```

If you need to restart a server after changing a static parameter, run the `az mysql/postgres server restart` command:

```
az postgres server restart \
    --resource-group northwindrg \
    --name northwind101

```

---

## Trace and track activity

A large part of maintaining databases is performance tuning. The same log files you're used to reviewing on your on\-premises databases are still available with Azure Database for MySQL/PostgreSQL.

With your databases migrated to Azure, you need to continue reviewing the log files to ensure the performance of the databases are maintained.

In this unit you'll see where the log files for PostgreSQL and MySQL are stored in Azure, and the level of detail they contain.

### Use server logs to track database activity

Azure Database for MySQL/PostgreSQL also records diagnostic information in the server logs. Server logs are the native message log files for MySQL and PostgreSQL (not the transaction log files, which are inaccessible in Azure Database for MySQL/PostgreSQL). These files contain messages, server status, and other error information that you use to debug problems with your databases. The server logs are retained for up to seven days (less, if the total size of the server log files exceeds 7 GB).

Azure Database for MySQL and Azure Database for PostgreSQL record different details in the server logs. The following sections describe the server logs for each service separately.

#### Server logs in Azure Database for MySQL

In Azure Database for MySQL, the server log provides the information normally available in the *slow query log* and the *audit log* on a MySQL server.

You use the information in the slow query log to help identify slow\-running queries. By default, the slow query log is disabled. You enable it by setting the **slow\_query\_log** server parameter to **ON**. You configure the slow query log to determine what is meant by a *slow query* using the following server parameters:

* **log\_queries\_not\_using\_indexes**. This parameter is either **ON** or **OFF**. Set it to **ON** to record all queries that are likely to perform a full table scan rather than an index lookup.
* **log\_throttle\_queries\_not\_using\_indexes**. Specifies the maximum number of slow queries not using indexes that can be logged per minute.
* **log\_slow\_admin\_queries**. Set this parameter to **ON** to include slow running administrative queries in the log.
* **long\_query\_time**. The threshold (in seconds) for a query to be considered *slow running*.

After you've enabled the slow query log and the audit log, the log files will start to appear in the **Server logs** page for the server. A new slow query log is created each day. Click a log file to download it:

To enable audit logging, set the **audit\_log\_enabled** server parameter to **ON**. You configure audit logging with the following parameters:

* **audit\_log\_events**. Specify the events to be audited. In the Azure portal, this parameter provides a drop\-down list of events, such as **CONNECTION**, **DDL**, **DML**, **ADMIN**, and others.
* **audit\_log\_exclude\_users**. This parameter is a comma\-separated list of users whose activities won't be included in the audit log.

If you need to preserve the slow query log and audit log for more than seven days, you arrange for them to be transferred to Azure storage. Use the **Diagnostics settings** page for your server, and then select **\+ Add diagnostic setting**. On the **Diagnostics settings** page, select **Archive to a storage account**, select a storage account in which to save the log files (this storage account must already exist), select **MySqlSlowLogs** and **MySqlAuditLogs**, and specify a retention period of up to 365 days. You can download the log files from Azure storage at any point during this time. Select **Save**:

Slow query log data will be written in JSON format to blobs in a container named **insights\-logs\-mysqlslowlogs**. It can take up to 10 minutes for the log files to appear in Azure storage. Audit records are stored in the **insights\-logs\-mysqlslowlogs** blob container, again in JSON format.

#### Server logs in Azure Database for PostgreSQL

In Azure Database for PostgreSQL, the server log contains error log and query log files. Use the information in these files to help locate the sources of any errors and inefficient queries.

You enable logging by setting the various **log\_** server configuration parameters to **ON**. These parameters include:

* **log\_checkpoints**. A checkpoint occurs whenever every data file has been updated with the latest information from the transaction log. If there's a server failure, this point marks the time at which recovery needs to commence by rolling forward from the transaction log.
* **log\_connection** and **log\_disconnections**. These settings record each successful connection, and the end of each session.
* **log\_duration**. This setting causes the duration of each completed SQL statement to be recorded.
* **log\_lock\_waits**. This setting causes lock wait events to be recorded. Lock waits can be caused by poorly implemented transactions in application code.
* **log\_statement\_stats**. This setting writes cumulative information about the performance of the server to the log.

Azure Database for PostgreSQL also provides further parameters to fine\-tune the information that's recorded:

* **log\_error\_verbosity**. This setting specifies the level of detail recorded for each logged message.
* **log\_retention\_days**. This is the number of days that the server retains each log file before removing it. The default is three days, and you can set it to a maximum of seven days.
* **log\_min\_messages** and **log\_min\_error\_statement**. Use these parameters to specify the warning and error levels for recording statements.

As with Azure Database for MySQL, the log files generated by Azure Database for PostgreSQL are available on the **Server logs** page. You can also use the **Diagnostic settings** page to copy the logs to Azure storage.

### Track query performance

Query Store is an additional feature provided by Azure to help you identify and track poorly running queries. You use it with Azure Database for MySQL and Azure Database for PostgreSQL.

#### Enabling query performance tracking

Query Store records information in the **mysql** schema in Azure Database for MySQL, and in a database named **azure\_sys** in Azure Database for PostgreSQL. Query Store can capture two types of information—data about query execution, and information on wait statistics. Query Store is disabled by default. To enable it:

* If you're using Azure Database for MySQL, set the server parameters **query\_store\_capture\_mode** and **query\_store\_wait\_sampling\_capture\_mode** to **ALL**.
* If you're using Azure Database for PostgreSQL, set the server parameter **pg\_qs.query\_capture\_mode** to **ALL** or **TOP**, and set the **pgms\_wait\_sampling.query\_capture\_mode** parameter to **ALL**.

#### Analyzing query performance data

You can query the tables used by Query Store directly. If you're running Azure Database for MySQL, connect to your server, and run the following queries:

```
SELECT * FROM mysql.query_store;

SELECT * FROM mysql.query_store_wait_stats;

```

If you're using Azure Database for PostgreSQL, run the following queries instead:

```
SELECT * FROM query_store.qs_view;

SELECT * FROM query_store.pgms_wait_sampling_view;

```

In both cases, the first query will display the text for each recently run query, and a host of statistics about how long the query took to compile and execute. The second query displays information about wait events. A wait event occurs when one query is prevented from running because it requires the resources held by another.

If you examine the Query Store directly, you can generate your own custom reports and gain a detailed insight into how the system is functioning. However, the amount of data available can make it difficult to understand what's happening. Azure Database for MySQL/PostgreSQL provides two additional tools to help you navigate this data—**Query Performance Insight**, and **Query Recommendations**.

**Query Performance Insight** is a graphical utility, available from the **Query Performance Insight** page for your server. The **Long running queries** tab displays the statistics for the most long running queries. You specify the time period, and zoom in to within a few minutes. The legend shows the text of each query, together with the duration and number of times the query was run. The graph gives a comparative view of the duration of each query. You view the data by the average time for each query, but it's also instructive to display the total time (*duration* \* *execution count*) for each query. The image below shows an example:

The **Wait Statistics** tab shows the wait event information for each query. You'll see the amount of time spent by a query waiting for various resources.

Wait events typically fall into three categories:

* **Lock waits**. These events occur if a query is attempting to read or modify data that's locked by another query. If you experience a large number of lock waits, check for long running transactions, or operations that use a highly restrictive isolation level.
* **IO waits**. This type of wait occurs if a query is performing a significant amount of IO. This could be due to a poorly designed query (check the *WHERE* clause), an inefficient join operation, or a full table scan incurred because of a missing index.
* **Memory waits**. A memory wait occurs if there's insufficient memory available to process a query. Your query could be attempting to read a large amount of data, or it might be blocked by other queries hogging memory. Again, this might indicate that indexes are missing, causing queries to read entire tables into memory.

It's also highly likely that one form of wait triggers another, so you can't necessarily examine these issues in isolation. For example, a transaction that reads and updates data in different tables might be subject to a memory wait. In turn, this transaction could have locked data that causes another transaction to incur a lock wait.

The **Performance Recommendations** page for the server takes the information held in Query Store and uses it to make recommendations for tuning your database for the workloads it's experiencing.

---

## Configure read replicas

Companies can use read\-only replicas of their databases to scale performance globally. Replicas are useful when an organization has customers distributed globally, and have users in their millions trying to access their data. Once in place, they can also handle regional disaster recover.

Your company has grown to an internationally renowned seller of bicycles. The CIO has asked your department to improve the responsiveness of your online shop for its users across the globe. You know that a quick and simple way to improve the performance is place read\-only replicas of your databases in each geographical location.

In this unit, you'll see how easy it is to create and manage read\-only replicas of data stored in an Azure Database for MySQL/PostgreSQL.

### How to use read replication

You use read replication to copy data from one instance of Azure Database for MySQL/PostgreSQL (referred to as the *source*) to up to five replicas. Use replication to spread the load across servers for read\-heavy workloads. Replication is one\-way only, and each replica is read\-only. Replication operates asynchronously, so there's a lag between the time the data changes on the source and the point at which it appears in each replica.

Replicas can be in different regions from the source. You use replicas to place data close to the clients needing it, to reduce query latency. Cross\-region replication also gives you a mechanism for handling regional disaster recovery.

Note

Cross\-region replication is not available in the Basic performance tier.

Each replica is an instance of Azure Database for MySQL/PostgreSQL in its own right, but configured as read\-only. If the connection to the source server is lost, or the source server is deleted, each replica becomes an independent read\-write server. In this case, replicas are no longer synchronized with each other, so the data they hold might start to diverge.

Note

If you're using Azure Database for MySQL, read replicas are only available in the General Purpose and Memory Optimized pricing tiers. Additionally, read replicas aren't available in Azure Database for PostgreSQL flexible servers.

#### Create replicas

The simplest way to add replicas to a server is through the **Replication** page for the server in the Azure portal. On this page, select **\+ Add Replica**.

You'll be prompted for a name and location for the server. Apart from that, the other details for the replica, including the pricing tier, are set to the same as those used by the source. When the replica has been created, you can amend any settings for that server, including adjusting the pricing tier. However, make sure that each replica has sufficient resources available to handle the workload associated with receiving and storing the replicated data.

Note

If you're using the General Purpose or Memory Optimized pricing tiers, you must also enable replication support. You do this on the **Replication** page by selecting **Enable replication support**. The server will be restarted before you can continue.

When you've added a replica, it'll be shown on the **Replication** page. Depending on the size of the source and the amount of data in the databases, deployment and synchronization of each replica might take a significant amount of time.

You reconfigure and resize a replica by selecting it on the **Replication** page.

If you prefer to use the Azure CLI, create replicas with the `az mysql/postgres server replica create` command:

```
az postgres server replica create \
  --name northwindreplica3 \
  --resource-group northwindrg \
  --source-server northwind101

```

#### Remove a replica

To remove a replica, select the replica on the **Replication** page, and select **Stop Replication**. The replica server will detach from the source and be converted into a read\-write server instead. The replica won't be deleted, and you'll continue to be charged for the resources it consumes. If you need to delete the replica, use the **Delete Replica** command instead.

The Azure CLI provides the `az mysql/postgres server replica stop` command to halt replication and convert a replica into a read\-write server. You then use the `az mysql/postgres server delete` command to delete the replica and free its resources.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/protect-monitor-tuning-migrated-database/_

## Fuentes
- [Protect, monitor, and tune a migrated database](https://learn.microsoft.com/en-us/training/modules/protect-monitor-tuning-migrated-database/?WT.mc_id=api_CatalogApi)
