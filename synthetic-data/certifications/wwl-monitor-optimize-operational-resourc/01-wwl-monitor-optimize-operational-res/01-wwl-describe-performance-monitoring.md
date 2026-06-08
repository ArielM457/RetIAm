# Describe performance monitoring

> Curso: Monitor and optimize operational resources in Azure SQL (wwl-monitor-optimize-operational-resources-sql-ser) · Seccion: Monitor and optimize operational resources in Azure SQL
> Duracion estimada: 83 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

A major part of the job of a database administrator is proper performance monitoring. This task doesn't change when moving to a cloud platform. While Azure offers tools for monitoring, you may lack some specific controls around hardware that you would have in an on\-premises environment which makes understanding how to identify and resolve performance bottlenecks while in Azure SQL that is much more critical.

### Learning objectives

* Understanding methods to review potential performance issues
* Identify critical Azure metrics
* Learn how to collect metrics for an established baseline
* Use extended events for performance analysis
* Understand database watcher

---

## Describe critical performance metrics

Let's learn how to create metrics in Azure Monitor, which allow you to trigger alerts or execute automated error responses.

### Review of Azure metrics

The Azure Monitor service includes the ability to track various metrics about the overall health of a given resource. Metrics are gathered at regular intervals and are the gateway for alerting processes that help to resolve issues quickly and efficiently. Azure Monitor Metrics is a powerful subsystem that allows you to not only analyze and visualize your performance data, but to also trigger alerts that notify administrators or automated actions that can trigger an Azure Automation runbook or a webhook. You can also archive your Azure Metrics data to Azure Storage, since active data is only stored for 93 days.

### Create metric alerts

Utilizing the Azure portal, you can create alert rules, based on defined metrics, in the overview section of the Azure Monitor blade. Azure Monitor Alerts can be scoped in three ways. For example, using Azure Virtual Machines as an example you can specify the scope as:

* A list of virtual machines in one Azure region within a subscription
* All virtual machines (in one Azure region) in one or more resource groups in a subscription
* All virtual machines (in one Azure region) in one subscription

In this manner, you can create an alert rule based on resources contained within resource groups as shown.

The following example demonstrates creating an alert for a virtual machine named *SQL2019*, focusing on the scope of the individual virtual machine.

Regardless the scope of the alert, the creation process is the same.

From the alerts screen, select **New Alert Rule**. If an alert is created from within the scope of a resource, the resource values should be populated for you. You can see that the resource is the *SQL2019* virtual machine, the subscription is *Dev\-Test\-Lab* and the resource group in which it resides is *SQLPlayground*.

Under the Condition section, select **Add**:

Select the metric that you wish to alert on. The following image shows Percentage CPU, which you'll then see selected.

The alerts can be configured in a static manner (for example, raise an alert when CPU goes over 95%) or in a dynamic fashion using Dynamic Thresholds. Dynamic Thresholds learn the historical behavior of the metric and raise an alert when the resources are operating in an abnormal manner. These Dynamic Thresholds can detect seasonality in your workloads and adjust the alerting accordingly.

If Static alerts are used, you must provide a threshold for the selected metric. In this example, 80 percent was specified. This threshold means that if the CPU utilization exceeds 80 percentage over a given period, an alert is fired and reacts as specified.

Both types of alerts offer Booleans operators such as the 'greater than' or 'less than' operators. Along with Boolean operators, there are aggregate measurements to select from such as average, minimum, maximum, count, average, and total. With these options available, it’s easy to construct a flexible alert that will suit just about any enterprise level alerting.

After you create the alert, in order to notify administrators or launch an automation process, an action group needs to be configured.

Defining an action group is optional, and if one isn't configured the alert will just log the notification to storage with no further action. You can create a new action group from the metrics screen, by selecting **Add** next to Action Groups.

Once you select **Create Action Group**, you see the following screen. You name the action group and define an alert and the response. In this example, the administrator receives an email notification if the alert condition is triggered.

You can configure the email or SMS details by selecting **Edit Details** under **Configure**, or by adding a new action, which will also bring up the configuration screen.

With an action group, there are several ways in which you can respond to the alert. The following options are available for defining the action to take:

* Automation Runbook
* Azure Function
* Email Azure Resource Manager Role
* Email/SMS/Push/Voice
* ITSM
* Azure Logic App
* Secure Webhook
* Webhook

There are two categories to these actions—notification, which means to notify an administrator or group of administrators of an event, and automation, which is taking a defined action to respond to a performance condition.

### Review past performance data

One of the benefits of utilizing the Azure Monitor is the ability to easily and quickly review past metrics that were gathered. If you examine a resource, you note a datetime picker in the upper right\-hand corner. Azure Monitor Metrics will be retained for 93 days, after which they're purged, however you do have the option to archive them to Azure Storage.

You're also able to select a smaller window of time such as the last 30 minutes, last hour, last 4 hours, or last 12 hours as an example. The flexibility of Azure monitor allows administrators to quickly identify issues and to potentially diagnose past issues.

### SQL Server metrics that matter

Microsoft SQL Server is a well instrumented piece of software that collects a great deal of performance metadata. The database engine has metrics that can be monitored to help identify and improve performance\-related issues. Some operating system metrics are only viewable from within performance monitor while others can be accessed through T\-SQL queries, in particular, by selecting from the dynamic management views (DMVs). There are some metrics that are exposed in both locations so knowing where to identify specific metrics is important. One example of data that can only be captured from DMVs is data and transaction log file read/write latency as exposed in `sys.dm_os_volume_stats`. On the other hand, an example of an OS metric that isn't available directly through SQL Server is the seconds per disk read and write for the disk volume. Combining these two metrics can help you gain better understand if a performance issue is related to database structure or a physical storage bottleneck.

---

## Establish baseline metrics

A baseline is a collection of data measurements that helps you understand the normal state of your application or server’s performance. Having the data collected over time allows you to identify changes from the normal state. Baselines can be as simple as a chart of CPU utilization over time, or complex aggregations of metrics to offer granular level performance data from specific application calls. The granularity of your baseline depends on the criticality of performance of your database and application.

With any type of application workload, it's imperative to establish a working baseline. A baseline helps you identify if an ongoing issue should be considered within normal parameters or has exceeded given thresholds. Without a baseline, every issue encountered could be considered normal and therefore not require any extra intervention.

### Correlating SQL Server and operating system performance

When deploying SQL Server on an Azure virtual machine, it’s critical to correlate the performance of SQL Server with the performance of the underlying operating system. If you're using Linux as the operating system, you need to install *InfluxDB*, *Collectd*, and *Grafana* to capture data similar to Windows Performance Monitor. These services collect data from SQL Server and provide a graphical interface to review the data. Utilizing these tools on Linux or Performance Monitor on Windows can be used in conjunction looking at SQL Server\-specific data such as SQL Server wait statistics. Using these tools together allow you to identify bottlenecks in hardware or code. The following Performance Monitor counters are a sampling of useful Windows metrics, and can allow you to capture a good baseline for a SQL Server workload:

**Processor(\_Total)% Processor Time** \- This counter measures the CPU utilization of all of the processors on the server. It's a good indication of the overall workload, and when used with other counters, this counter can identify problems with query performance.

**Paging File(\_Total)% Usage** \- In a properly configured SQL Server, memory shouldn't page to the paging file on disk. However, in some configurations you may have other services running that consume system memory and lead to the operating system paging memory to disk resulting in performance degradation.

**PhysicalDisk(\_Total)\\Avg. Disk sec/Read and Avg. Disk sec/Write** \- This counter provides a good metric for how the storage subsystem is working. Your latency values in most cases shouldn't be above 20 ms, and with Premium Storage you should see values less than 10 ms.

**System\\Processor Queue Length** \- This number indicates the number of threads that are waiting for the time on the processor. If it's greater than zero, it indicates CPU pressure, indicating your workload could benefit from more CPUs.

**SQLServer:Buffer Manager\\Page life expectancy** \- Page life expectancy indicates how long SQL Server expects a page to live in memory. There's no proper value for this setting. Older documentation refers to 300 seconds as proper, but that was written in a 32\-bit era when servers had far less RAM. You should monitor this value over time, and evaluate sudden drops. Such drops in the counter's value could indicate poor query patterns, external memory pressure (for example, the server running a large SSIS package) or could just be normal system processing like running a consistency check on a large database.

**SQLServer:SQL Statistics\\Batch Requests/sec** \- This counter is good for evaluating how consistently busy a SQL Server is over time. Once again there's no good or bad value, but you can use this counter with % Processor time to better understand your workload and baselines.

**SQLServer:SQL Statistics\\SQL Compilations/sec and SQL Re\-Compilations/sec** \- These counters are updated when SQL Server has to compile or recompile an execution plan for a query because there's no existing plan in the plan cache, or because a plan was invalidated because of a change. Recompiles can indicate T\-SQL with recompile query hints, or be indicative of memory pressure on the plan cache caused by either many ad\-hoc queries or simple memory pressure.

These counters are just a sample of the available performance monitor counters that are available to you. While these counters provide a good baseline of performance, you may need to examine more counters to identify specific performance problems.

### Wait statistics

When a thread is being executed and is forced to wait on an unavailable resource, SQL Server keeps track of these metrics. This information is easily identifiable via the dynamic management view (DMV) `sys.dm_os_wait_stats`. This information is important to understanding the baseline performance of your database, and can help you identify specific performance issues both with query execution and hardware limitations. Identifying the appropriate wait type and corresponding resolution is critical for resolving performance issues. Wait statistics are available across the Azure SQL platform.

---

## Describe database watcher (preview)

One of the benefits of using any of the products part of the Azure SQL family is the monitoring capability that is built into Azure platform.

[Database watcher](/en-us/azure/azure-sql/database-watcher-overview) is a robust monitoring solution designed specifically for [Azure SQL Database](https://azure.microsoft.com/products/azure-sql/database/) and [Azure SQL Managed Instance](https://azure.microsoft.com/products/azure-sql/managed-instance/). This tool provides comprehensive insights into the performance, configuration, and overall health of your databases. It collects detailed monitoring data from various sources, including databases, elastic pools, and SQL managed instances, and ensures that you have a clear and detailed view of your SQL estate.

Note

Database watcher is currently in preview.

### How database watcher works

One of the key features of Database watcher is its ability to gather and store monitoring data in a central data store within your Azure subscription. This data can then be analyzed using tools like Azure Data Explorer or Real\-Time Analytics in Microsoft Fabric, allowing for quick ingestion and analysis of time\-series monitoring data.

Database watcher enables you to set targets, datasets, frequency, and retention according to your specific needs. It supports low latency, with data collection and ingestion happening within seconds. This ensures that you always have up\-to\-date information about your database's performance and health.

This tool also offers a range of dashboards in the Azure portal, providing a single\-pane\-of\-glass view of your entire SQL estate. These dashboards offer detailed insights into each monitored resource, allowing you to quickly identify and address any issues. Additionally, Database Watcher supports parameterized templates for common alert rules, and the ability to create custom alerts, ensuring that you're always notified of critical events.

Database watcher requires a data store for the monitoring data it collects. You can use a database on an [Azure Data Explorer](/en-us/azure/data-explorer/data-explorer-overview) cluster or on a free Azure Data Explorer cluster or you can use a [Real\-Time Analytics](/en-us/fabric/real-time-intelligence/overview) database in Microsoft Fabric.

### Configure database watcher

Here's a simple guide to configure database watcher for Azure SQL Database and Azure SQL Managed Instance:

1. Go to the Azure portal and sign in with your credentials.
2. In the Azure portal, search for "Database Watchers" and select it. Select **Create**.
3. Select your subscription and resource group. Provide a name, and select the region where you want to deploy the database watcher.
4. On the **Data store** tab, configure the data store for the monitoring data.
5. On the **SQL targets** tab, choose the Azure SQL Database or Azure SQL Managed Instance you want to monitor.
6. Review your configuration settings and select **Create** to deploy the database watcher resource.

To learn more about database watcher, see [Quickstart: Create a database watcher to monitor Azure SQL](/en-us/azure/azure-sql/database-watcher-quickstart).

---

## Explore Query Performance Insight

Identifying which queries are consuming the most resources is the first step in any database performance tuning endeavor. In older versions of SQL Server, this required extensive tracing and a series of complex SQL scripts, which could make the process of data gathering cumbersome.

### Identify problematic queries

Query Performance Insight allows the administrator to quickly identity expensive queries. You can navigate to Query Performance Insight in the main blade for your Azure SQL Database in the Intelligent Performance section.

When you launch Query Performance Insight, you discover three buttons to allow you to filter for long running queries, top resource consuming queries, or a custom filter. The default value is Resource Consuming Queries. This tab shows you the top five queries sorted by the particular resource that you select. In this case, it was sorted by CPU. You also have other options of sorting by Data IO and Log IO metrics.

You can drill into individual queries by selecting the row within the lower grid. Each row is identified with a unique color that correlates to the color within the bar graph above it.

Switching to Long Running Queries, you can see a similar layout as before. In this case, the metrics are limited to the top five queries sorted by duration from the previous 24 hours and is a sum aggregation. In the grid below the graph, you can examine specific queries by selecting the row.

Switching to the custom tab offers more flexibility compared to the other two options.

Within this tab, we can further define how we wish to examine performance data. It offers us several drop\-down menus that drive the visual representation of the data. The key metrics are CPU, Log IO, Data IO, and memory. These metrics are the aspects of database performance, the upper limits of which are determined by the service tier and compute resources of your Azure SQL Database.

If we drill into an individual query, we're able to see the query ID and the query itself, as well as the query aggregation type and associated time period. Furthermore, the query ID also correlates to the query ID located within the Query Store. Metrics gleaned from Query Performance Insights can then be easily located within the Query Store itself for deeper analysis or possibly problem resolution if needed.

While Query Performance Insight doesn't show the query’s execution plan, you can quickly identify that query, and use the information to extract the plan from the Query Store in your database.

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary

The Azure platform allows you to use the Azure Monitor to collect baseline performance data about both PaaS and IaaS resources. Within Windows, the Performance Monitor allows you to collect detailed performance information about your SQL Server. Azure SQL Database includes extra detailed query performance information through Query Performance Insight, and provides advanced monitoring capabilities through extended events.

Having a solid understand of the baseline workload of your server and database are critical to understanding performance anomalies.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/describe-performance-monitoring/_

## Fuentes
- [Describe performance monitoring](https://learn.microsoft.com/en-us/training/modules/describe-performance-monitoring/?WT.mc_id=api_CatalogApi)
