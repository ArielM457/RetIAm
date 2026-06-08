# Analyze app telemetry with logs and metrics

> Curso: Observe and troubleshoot apps on Azure (wwl-observe-troubleshoot-apps) · Seccion: Observe and troubleshoot apps on Azure
> Duracion estimada: 82 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

AI applications in production generate large volumes of telemetry data across distributed services, but raw data alone doesn't provide actionable insight. This module guides you through analyzing application telemetry with Azure Monitor logs and metrics to detect failures, identify performance trends, and maintain operational visibility for AI solutions on Azure.

Imagine you're a developer building a document processing pipeline for an enterprise content moderation AI service. The system consists of four services: an ingestion API that receives document uploads, a classification service that categorizes content using a trained model, an extraction service that identifies key entities, and a moderation service that flags policy violations. After deploying to production, the team notices that some documents take over 30 seconds to process, but there's no way to determine which service causes the delay. Occasionally, the moderation service returns errors for specific document types, and the team only discovers these failures when users report them. Your client expects a dashboard that shows real\-time pipeline health, with alerts that notify the on\-call team within five minutes of a failure spike. The client also needs the ability to investigate incidents interactively, drilling into specific time windows and filtering by document type or service. Azure Monitor provides the query language, visualization tools, and alerting capabilities to meet all of these requirements.

After completing this module, you'll be able to:

* Write KQL queries to retrieve and analyze application telemetry from Application Insights.
* Explore log data to identify error patterns, performance bottlenecks, and trends in application behavior.
* Build Azure dashboards that display key telemetry metrics and log query results for operational monitoring.
* Create Azure Monitor Workbooks for interactive, parameter\-driven telemetry analysis.
* Configure alert rules that detect application failures, performance degradation, and anomalies.

Note

All code examples in this module use KQL queries against Application Insights log tables. The Azure Monitor query experience is updated regularly, and the recommendation is to visit the [Azure Monitor logs documentation](/en-us/azure/azure-monitor/logs/log-query-overview) for the most up\-to\-date information.

---

## Write basic KQL queries

Kusto Query Language (KQL) is the primary tool developers use to retrieve and analyze telemetry data stored in Azure Monitor logs. Whether you're investigating a spike in errors across your document processing pipeline or measuring how long the classification service takes to respond, KQL provides the operators and functions to extract the answers from your telemetry. This unit introduces the KQL fundamentals you need to start querying Application Insights log data effectively.

Note

All code examples in this module use KQL queries against Application Insights log tables. The Azure Monitor query experience is updated regularly, and the recommendation is to visit the [Azure Monitor logs documentation](/en-us/azure/azure-monitor/logs/log-query-overview) for the most up\-to\-date information.

### Understand KQL and Azure Monitor logs

KQL is the query language used across Azure Monitor, Log Analytics, and Azure Data Explorer to retrieve and analyze log data. KQL follows a pipe model where queries start with a table name and flow through a sequence of operators separated by the pipe (`|`) character. Each operator takes the output of the previous step, transforms it, and passes the result to the next operator. This approach makes queries readable from top to bottom, with each line representing a distinct step in the data processing pipeline.

Developers write KQL queries in the Log Analytics query editor. You can access the editor from the Azure Monitor menu in the Azure portal, from a specific Application Insights resource, or from any Log Analytics workspace. The editor provides IntelliSense autocompletion, syntax highlighting, and a results pane that displays query output as tables or charts.

Query scoping determines which tables and column names your queries use. When you open logs from an Application Insights resource, the query scope targets that resource's data using the Application Insights table names like `requests`, `exceptions`, and `dependencies`. When you query from a Log Analytics workspace directly, you use the workspace table names like `AppRequests`, `AppExceptions`, and `AppDependencies`. The examples in this module use the Application Insights table names because that's the most common starting point for application developers investigating their own telemetry.

### Explore the Application Insights table structure

Application Insights organizes telemetry into specialized tables, each storing a different category of data collected from your instrumented application. Understanding these tables is essential for knowing where to look when you need specific information. Whether you're searching for failed HTTP requests, slow database calls, or unhandled exceptions, the answer lives in one of these core tables.

The following tables store the telemetry data most relevant to application developers:

* **`requests`:** Stores incoming HTTP requests with details like duration, response code, and success status. Each row represents one request handled by your application.
* **`dependencies`:** Captures outbound calls from your application to databases, HTTP endpoints, Azure services, and other microservices. For AI applications, these calls often include requests to model inference endpoints and vector databases.
* **`exceptions`:** Records errors and exceptions with stack traces and severity levels. Both handled and unhandled exceptions appear in this table.
* **`traces`:** Contains application log messages from frameworks like ILogger, log4j, or Serilog. Each log statement your application writes appears as a row in this table.
* **`customEvents`:** Stores custom business events that developers explicitly track in their code, such as "document classified" or "moderation flagged."
* **`customMetrics`:** Holds custom numeric measurements that developers track, such as queue depth or model inference confidence scores.
* **`performanceCounters`:** Contains system\-level metrics like CPU usage, memory consumption, and I/O rates.

All tables share common columns that provide context for every telemetry item. The `timestamp` column records when the event occurred. The `operation_Id` column links all telemetry items from a single distributed trace, making it possible to follow a request as it moves through multiple services. The `cloud_RoleName` column identifies which service generated the telemetry, which is critical for multi\-service architectures. The `customDimensions` column contains a dynamic property bag of key\-value pairs that developers add to enrich telemetry with application\-specific context. The `itemCount` column indicates how many actual events a single sampled record represents, which matters when Application Insights sampling is active.

### Filter and select data with core operators

The most common KQL task is filtering a table down to the rows you care about and selecting the columns you want to see. KQL provides several core operators for this purpose, and most queries you write start with one or more filtering steps followed by a column selection step.

The `where` operator filters rows based on conditions. You can use comparison operators like `==`, `!=`, `>`, and `<` for exact matches and numeric comparisons. For string matching, KQL offers several options with different performance characteristics. The `has` operator checks whether a term appears in a string and uses the column's term index for fast lookups. The `contains` operator checks for substring matches but doesn't use term indexing, making it slower on large datasets. The `startswith` operator matches the beginning of a string. You can combine multiple conditions with the `and` and `or` logical operators.

The `project` operator selects specific columns to include in the output. Using `project` reduces the width of your results and focuses attention on the data that matters for your analysis. You can also rename columns and create calculated columns within a `project` step.

The `take` operator returns an arbitrary set of N rows from the table, which is useful for quickly inspecting the shape of your data. The `top` operator returns the first N rows sorted by a specified column, which is more useful when you need the highest or lowest values. The following query filters for failed requests from the last hour, selects key columns, and returns the 20 slowest failures:

```
requests
| where timestamp > ago(1h)
| where success == false
| project timestamp, name, resultCode, duration, cloud_RoleName
| top 20 by duration desc

```

This query starts with the `requests` table, filters to the last hour using the `ago()` function, narrows to only failed requests, selects five columns, and returns the top 20 results sorted by duration in descending order. Each line performs one clear transformation, making the query easy to read and modify.

### Aggregate and summarize data

Filtering shows you individual records, but understanding trends and patterns requires aggregation. The `summarize` operator groups rows and applies aggregation functions to produce summary statistics. Each unique combination of values in the `by` clause produces one output row in the results.

KQL provides several aggregation functions that work within `summarize`. The `count()` function returns the number of rows in each group. The `avg()`, `sum()`, `min()`, and `max()` functions calculate statistics on numeric columns. The `dcount()` function estimates the count of distinct values using a probabilistic algorithm, which is useful for questions like "how many unique users experienced this error." For exact distinct counts on small datasets, use `count_distinct()`, though it's more resource\-intensive at scale. The `percentile()` function calculates a specific percentile value, which is essential for latency analysis where average values can mask outlier behavior. For example, `percentile(duration, 95)` returns the response time below which 95 percent of requests fall.

The `bin()` function groups continuous values like timestamps into fixed\-size intervals. Using `bin(timestamp, 1h)` rounds each timestamp down to the nearest hour, creating consistent time buckets for trend analysis. Without `bin()`, each unique millisecond timestamp would create its own group, making aggregation meaningless for time series data.

The following query counts requests and calculates average duration per hour, grouped by service name:

```
requests
| where timestamp > ago(24h)
| summarize requestCount = count(), avgDuration = avg(duration)
    by bin(timestamp, 1h), cloud_RoleName

```

Each row in the output represents one hour of data for one service. This pattern is the foundation for most trend analysis queries, and you can adjust the time window and bin size to match the granularity you need.

### Visualize query results with the render operator

KQL includes the `render` operator for specifying chart types directly in your queries. Adding a `render` step as the final operator in a query tells Log Analytics to display the results as a chart instead of a table. This approach is useful for quickly visualizing trends, distributions, and comparisons without leaving the query editor.

The most common chart types for telemetry data include `timechart`, `barchart`, `piechart`, `columnchart`, and `areachart`. The `timechart` type requires a datetime column and one or more numeric columns, and it's the most frequently used visualization for telemetry because it shows how values change over time. The `barchart` and `columnchart` types work well for comparing values across categories, such as error counts by service. The `piechart` type shows proportional distributions, such as the share of requests handled by each service.

The following query renders a time chart showing request counts by service over the last 24 hours:

```
requests
| where timestamp > ago(24h)
| summarize requestCount = count() by bin(timestamp, 1h), cloud_RoleName
| render timechart

```

Log Analytics displays this query as a line chart with one line per `cloud_RoleName` value and time on the horizontal axis. You can switch between chart types in the results pane without modifying the query, but including `render` in the query itself ensures the visualization is preserved when you pin the results to a dashboard or share the query with team members.

### Additional resources

* [KQL overview](/en-us/azure/azure-monitor/logs/log-query-overview)
* [Get started with log queries](/en-us/azure/azure-monitor/logs/get-started-queries)
* [Application Insights data model](/en-us/azure/azure-monitor/app/data-model-complete)

---

## Explore logs for errors and performance

Once you understand the basic KQL operators, the next step is applying them to real investigation scenarios. When an AI pipeline experiences errors or performance degradation, developers need to identify what's failing, correlate issues across services, and measure the impact on dependent systems. This unit covers the KQL patterns and Application Insights tools that developers use to investigate application errors and analyze performance bottlenecks.

### Investigate application errors with KQL

Identifying what's failing in a distributed AI pipeline requires more than checking a single error log. A failure in the moderation service might stem from a timeout in the extraction service, which itself depends on a slow database query. The first step in any investigation is understanding the scope of the problem: how many errors are occurring, when did they start, and which exception types are involved.

The following query shows exception rates over time, grouping by exception type to reveal error spikes and patterns:

```
exceptions
| where timestamp > ago(24h)
| summarize exceptionCount = sum(itemCount) by bin(timestamp, 1h), type
| render timechart

```

This query uses `sum(itemCount)` instead of `count()` to produce accurate results when Application Insights sampling is active. When sampling is enabled, Application Insights keeps a representative subset of telemetry and assigns an `itemCount` value to each sampled record that reflects how many actual events that record represents. Using `count()` with active sampling returns only the count of sampled records, which underrepresents the true error volume. The `sum(itemCount)` approach accounts for sampling and produces totals that reflect actual application behavior.

Once you identify an error spike in the timechart, you can drill down to find the most common exception types and the operations they affect:

```
exceptions
| where timestamp > ago(24h)
| summarize exceptionCount = sum(itemCount) by type, operation_Name
| top 10 by exceptionCount desc

```

This query groups exceptions by both the exception type and the operation name, producing a ranked list that highlights which operations generate the most errors. For a content moderation pipeline, this query might reveal that `System.TimeoutException` concentrates in the `POST /classify` operation, immediately narrowing the investigation scope.

### Correlate failures across services

In a multi\-service architecture, a single user request flows through several services, and a failure at any point in the chain affects the overall outcome. The `operation_Id` column links all telemetry items from a single distributed request. By joining tables on `operation_Id`, developers can see the full sequence of events that led to a failure, from the initial request through every dependency call and exception.

The following query joins exceptions with the originating requests to identify which operations produce the most errors and which services those errors originate from:

```
exceptions
| where timestamp > ago(24h)
| join kind=inner (
    requests
    | project requestName = name, requestDuration = duration, operation_Id, requestRoleName = cloud_RoleName
) on operation_Id
| project timestamp, exceptionType = type, exceptionMessage = outerMessage,
    requestName, requestDuration, cloud_RoleName = requestRoleName
| top 20 by timestamp desc

```

Each row in the results shows an exception alongside the request that triggered it. The `cloud_RoleName` column identifies which service generated the exception, and the `requestDuration` column reveals whether the overall request was slow. This combination helps developers distinguish between errors that cause user\-visible failures and errors that occur in background processes.

When joining `exceptions` with `requests`, some columns like `timestamp`, `operation_Id`, and `cloud_RoleName` exist in both tables. KQL appends a numeric suffix (`1`) to disambiguate these duplicate column names in the output. The cleanest approach is to rename columns inside the subquery before the join, as the example shows, so the final `project` step uses unambiguous names. This pattern applies to all KQL `join` operations and avoids confusion when columns share names across tables.

### Analyze dependency latency and failures

The `dependencies` table captures every outgoing call from an instrumented service, including calls to databases, HTTP APIs, Azure services, and other microservices. For AI applications, dependency calls often represent the most performance\-sensitive operations in the pipeline: requests to model inference endpoints, vector database lookups, embedding generation services, and storage operations. When the pipeline runs slower than expected, the `dependencies` table is the first place to look for the bottleneck.

The following query calculates latency percentiles for each dependency target, helping you identify which dependencies contribute the most latency:

```
dependencies
| where timestamp > ago(24h)
| summarize avg(duration), percentiles(duration, 50, 95, 99) by target, type
| order by percentile_duration_95 desc

```

Percentile calculations provide a more accurate picture of dependency performance than averages alone. An average response time of 200 milliseconds might hide a scenario where 95 percent of calls complete in 100 milliseconds while 5 percent take over two seconds. The 95th and 99th percentiles reveal these outliers, which often correspond to the user experiences that generate support tickets and complaints.

Failed dependencies represent a different category of problem. While slow dependencies degrade performance, failed dependencies can break entire request flows. The following query identifies failed dependencies grouped by target, result code, and originating service:

```
dependencies
| where timestamp > ago(24h)
| where success == false
| summarize failureCount = count() by target, resultCode, cloud_RoleName
| order by failureCount desc

```

The `resultCode` column provides diagnostic context that helps narrow the investigation. An HTTP 429 result code from a model inference endpoint indicates rate limiting, which you address by adjusting throughput or implementing retry policies. An HTTP 500 result code suggests a server\-side failure in the dependency itself. A timeout with no result code points to network issues or an overloaded service.

### Use the failures and performance views

Application Insights provides built\-in investigation views that complement KQL queries for common diagnostic scenarios. These views offer curated starting points for investigation, while KQL queries provide the flexibility to ask specific questions that the built\-in views don't cover.

The Failures view groups failed operations by type and displays the top three response codes, exception types, and failed dependencies for each operation. You can access this view from the Application Insights resource menu under **Investigate \> Failures**. Selecting a specific operation opens a panel that shows sample operations, and selecting a sample opens the end\-to\-end transaction details view. The transaction details view displays the full timeline of a single request, showing every dependency call, exception, and trace message in chronological order. This timeline is invaluable for understanding exactly what happened during a specific failed request.

The Performance view shows all operations with their response time distributions and request counts. You can access this view from **Investigate \> Performance**. The view displays a summary of operations ranked by duration or count, and selecting an operation reveals the duration distribution chart. This chart shows the range of response times for that operation, making it easy to spot bimodal distributions where most requests are fast but a subset is consistently slow.

KQL queries are the right tool when you need to join across tables, build custom aggregations, filter by dimensions that the built\-in views don't expose, or create visualizations for dashboards. The built\-in views are the right tool when you need a quick investigation starting point or want to drill into a specific transaction's end\-to\-end timeline. In practice, developers often start with the built\-in views to identify the general problem area, then switch to KQL to dig deeper into specific patterns and root causes.

### Additional resources

* [Failures and performance views](/en-us/azure/azure-monitor/app/failures-performance-transactions)
* [Application Insights data model](/en-us/azure/azure-monitor/app/data-model-complete)

---

## Build dashboards for app telemetry

Writing KQL queries is essential for investigating specific problems, but teams also need a persistent visual summary that shows the health of their application at a glance. Azure dashboards provide a shared surface where developers and operations teams pin metrics charts, log query results, and other tiles into a single view that answers the question "is the system healthy right now?" This unit covers how to build dashboards that combine Application Insights data into an operational monitoring view for your AI solution.

### Understand Azure dashboards for monitoring

Azure dashboards are customizable visual surfaces in the Azure portal that combine tiles from multiple Azure resources into a single view. Each tile displays a specific piece of information: a metrics chart, a log query result, a Markdown text block, or a resource from the Tile Gallery. Teams use dashboards for operational awareness during day\-to\-day monitoring, keeping them open on wall\-mounted screens or checking them during stand\-up meetings to confirm pipeline health.

Dashboards differ from workbooks in their design intent and interaction model. Dashboards are optimized for at\-a\-glance visibility with tiles that refresh on a schedule and display the latest data automatically. The layouts are relatively static. You arrange tiles once, and the dashboard continues to display updated data without manual intervention. Workbooks, which the next unit covers, are designed for interactive exploration where users adjust parameters and drill into data dynamically. Choose dashboards for ongoing operational monitoring and workbooks for incident investigation and ad\-hoc analysis.

A single dashboard can combine resources from multiple subscriptions and resource groups. This capability means you can build a dashboard that shows metrics from your Application Insights resource alongside storage account throughput, Azure Kubernetes Service node health, and any other Azure resource data that's relevant to your application's overall health.

### Pin metrics to a dashboard

Application Insights collects standard metrics that provide immediate insight into application behavior without requiring any KQL queries. You can create metrics charts and pin them directly to a dashboard, building a monitoring view from precollected data.

To create a metrics chart, you open your Application Insights resource and navigate to the **Metrics** pane under **Monitoring**. You select a metric from the dropdown, such as server response time, failed requests, or dependency duration. You can apply filters to narrow the data, for example filtering to a specific `cloud_RoleName` to see metrics for just one service. You can also use splitting to break the chart into separate lines by a dimension like operation name or result code. Once the chart looks right, you select the pin icon to add it to an existing dashboard or create a new one.

Common metrics for AI application dashboards include:

* **Server response time:** Shows average and percentile response times for incoming requests, indicating overall application responsiveness.
* **Failed requests:** Tracks the rate and count of requests that return error status codes, highlighting reliability problems.
* **Dependency failures:** Monitors failed outgoing calls to databases, APIs, and model endpoints.
* **Server request rate:** Displays throughput in requests per second, showing traffic patterns and capacity utilization.
* **Availability:** Shows the success rate of configured availability tests, confirming that the application is reachable.

When configuring metrics charts, the aggregation type determines what value the chart displays. Average aggregation shows typical behavior and is appropriate for response times and latency. Sum aggregation works well for counting total events over a time period. Max aggregation reveals worst\-case values, which is useful for identifying latency spikes that affect user experience even if they occur infrequently.

### Pin log query results to a dashboard

Metrics charts are limited to the precollected standard metrics and custom metrics your application emits. Log queries provide the flexibility to calculate values, join across tables, and create visualizations that metrics alone can't produce. You can pin KQL query results to a dashboard for richer analysis tiles.

To pin a log query result, you navigate to **Logs** under **Monitoring** in your Application Insights resource, write and run your query, switch to chart view if you want a visual tile, and select the pin icon. The chart type you select at the time of pinning is preserved on the dashboard tile. The following query provides a useful dashboard tile that shows failed requests grouped by service:

```
requests
| where timestamp > ago(24h)
| where success == false
| summarize failedCount = count() by cloud_RoleName
| render barchart

```

The bar chart immediately reveals which services contribute the most failures, making it easy to spot a service that needs attention. For latency monitoring, the following query creates a tile that displays request latency percentiles over time:

```
requests
| where timestamp > ago(24h)
| summarize p50 = percentile(duration, 50),
    p95 = percentile(duration, 95),
    p99 = percentile(duration, 99)
    by bin(timestamp, 1h)
| render timechart

```

This time chart displays three lines representing the 50th, 95th, and 99th percentile response times. A growing gap between the p50 and p95 lines indicates that while most requests remain fast, a significant portion of requests experiences degradation. This pattern is common in AI pipelines when a specific document type triggers more expensive processing.

Dashboard tiles refresh on a schedule and display the query results as of the last refresh. Tiles aren't real\-time. The refresh frequency depends on the dashboard configuration, with the default being periodic automatic refresh. For real\-time visibility during active incidents, consider using Live Metrics in Application Insights or workbooks with shorter time ranges.

### Organize and share dashboards

A dashboard with tiles in random positions is harder to read than one organized with clear groupings. Effective dashboard design requires deliberate arrangement that helps team members find the information they need quickly.

You can arrange tiles by selecting **Edit** mode at the top of the dashboard. In edit mode, you can drag tiles to new positions, resize them to show more or less detail, and rename them with descriptive titles. Grouping related tiles together helps teams scan the dashboard efficiently. For example, placing all latency\-related tiles in one row and all error\-related tiles in another row creates a logical reading flow.

To share a dashboard with team members, you select **Share** and then **Publish**. Publishing makes the dashboard available to other users in your organization. Access control uses Azure role\-based access control (RBAC), so team members need read permissions on both the dashboard resource and the underlying data sources. If a team member has access to the dashboard but not to the Application Insights resource, the tiles that query that resource display an access error.

When designing dashboards for AI application monitoring, consider these best practices:

* **Separate concerns into different dashboards:** Create one dashboard for pipeline health (latency, throughput, error rates) and another for business metrics (documents processed, classifications made, violations detected). Combining too many concerns into a single dashboard makes it harder to scan.
* **Limit tile count:** Keep dashboards focused on 5 to 10 tiles that answer the most important operational questions. Too many tiles create visual clutter and dilute attention.
* **Use descriptive tile titles:** Rename each tile to describe what it shows ("Classification Service P95 Latency" rather than "Query 3"). Team members who didn't create the dashboard need clear titles to understand each tile's purpose.
* **Include a Markdown tile for context:** Add a Markdown tile at the top of the dashboard that describes the application being monitored, links to runbooks, and lists on\-call contacts.

### Additional resources

* [Create a Log Analytics dashboard](/en-us/azure/azure-monitor/visualize/tutorial-logs-dashboards)
* [Application Insights overview dashboard](/en-us/azure/azure-monitor/app/overview-dashboard)

---

## Create workbooks for interactive analysis

Dashboards provide at\-a\-glance operational awareness, but investigating an incident or exploring a trend requires interactivity. Azure Monitor Workbooks provide a flexible canvas that combines text, KQL queries, metrics, and parameters into interactive reports where users can adjust filters, select time ranges, and drill into specific data points. This unit covers how to create workbooks that enable developers and operations teams to explore telemetry data dynamically.

### Understand Azure Monitor Workbooks

Azure Monitor Workbooks are interactive analysis tools that let developers combine rich text, KQL queries, metrics, and parameters into reusable reports. Workbooks go beyond dashboards by supporting user interactions: selecting a parameter value, choosing a time range, or clicking a grid row dynamically updates all dependent visualizations. This interactivity makes workbooks the right choice for troubleshooting, root cause analysis, and any scenario where the investigator needs to adjust the analysis scope based on what they find.

Dashboards and workbooks serve different purposes in the monitoring workflow. Dashboards show static tiles for ongoing operational awareness, answering the question "is the system healthy?" Workbooks enable exploratory analysis, answering the question "why is the system behaving this way?" During an incident, a team member might glance at a dashboard to confirm that error rates are elevated, then open a workbook to filter by service, time window, and error type to identify the root cause.

You can access workbooks from Azure Monitor, from a Log Analytics workspace, or directly from an Application Insights resource. The Azure portal includes a gallery of prebuilt workbook templates organized by category, such as performance analysis, failure analysis, and usage analysis. You can use these templates as starting points and customize them for your application, or you can create workbooks from scratch.

### Add query steps and visualizations

Workbooks are built by adding steps vertically, with each step rendering a component in the final report. The available step types include text blocks for explanations and instructions, query steps that execute KQL queries and display results, metrics steps that show Azure resource metrics, and parameter steps that create interactive filters. Steps render in the order they appear, creating a top\-to\-bottom narrative flow.

To add a KQL query step, you select **Add query**, choose **Logs** as the data source, specify the Application Insights resource as the scope, write your KQL query, and select a visualization type. The available visualization types include grid (tabular results), chart (line, bar, area), tiles (summary cards), and map (geographic distribution). Each visualization type suits different data shapes and analysis goals.

The following query works as a workbook step that displays request success rates by service. It references a workbook parameter called `{TimeRange}` to control the query window:

```
requests
| where timestamp > ago({TimeRange})
| summarize totalRequests = count(),
    failedRequests = countif(success == false)
    by cloud_RoleName
| extend successRate = round(100.0 * (totalRequests - failedRequests) / totalRequests, 2)
| project cloud_RoleName, totalRequests, failedRequests, successRate

```

The `{TimeRange}` syntax references a workbook parameter. When the user changes the time range parameter at the top of the workbook, this query and all other queries that reference `{TimeRange}` automatically re\-execute with the new value. This behavior creates a coordinated analysis experience where adjusting one filter updates the entire workbook.

### Use parameters for interactive filtering

Parameters are the feature that makes workbooks interactive. Each parameter appears as a control at the top of the workbook, typically a dropdown menu, text input, or time picker. Users select values from these controls, and the selected values are injected into query steps throughout the workbook.

The most common parameter types are:

* **Time range:** Controls the time window for all queries in the workbook. This parameter type provides a standard dropdown with options like "last hour," "last 24 hours," and "last seven days."
* **Dropdown:** Populated by a KQL query or a static list of values. Dropdown parameters let users filter results by dimensions like service name, environment, or error type.
* **Resource picker:** Lets users select which Application Insights resource or Log Analytics workspace to analyze. This parameter type is useful for workbooks that need to work across multiple environments.

To create a dropdown parameter that lists all services in your application, you add a parameter step and configure a KQL query that returns distinct `cloud_RoleName` values from the `requests` table. Subsequent query steps reference the parameter using the `{ServiceName}` syntax to filter their results to the selected service.

When a dropdown parameter allows multi\-select, users can choose several services at once. The parameter value becomes a comma\-separated list, and queries use the `in` operator to filter by multiple values. For example, `| where cloud_RoleName in ({ServiceName})` filters results to all selected services. Multi\-select parameters are useful when team members need to compare behavior across two or three specific services without viewing the entire pipeline.

### Configure conditional visibility and linked content

Conditional visibility and grid link actions add depth to workbooks by creating drill\-down experiences. Instead of showing every detail upfront, you can design workbooks that start with a high\-level summary and reveal detailed analysis only when the user selects a specific item.

Conditional visibility controls whether a workbook step is shown or hidden based on a parameter value. You configure this by editing a step's advanced settings and specifying a condition. For example, you can create a workbook where a detailed exception analysis step is hidden by default and only appears when the user selects a specific service from the dropdown. This approach keeps the initial view clean and focused, while making detailed data available on demand.

Grid link actions create interactive tables where selecting a row triggers a downstream action. When you configure a grid column as a link, clicking a cell in that column can open the end\-to\-end transaction details for a specific request, navigate to another workbook for deeper analysis, or export a parameter value that other steps reference. The exported parameter pattern is powerful: you can display a summary grid of services with error counts, and when a user select a service name, the selected value populates a parameter that filters the remaining workbook steps to show only data for that service.

Effective workbook design follows a consistent pattern. You can start with a summary query at the top that shows overall pipeline health across all services, add parameter filters for time range and service selection, and use linked grids to enable drill\-down from the summary into specific services or operations. You can place detailed analysis steps, such as exception stack traces or dependency timelines, in conditionally visible sections that appear only when the user selects a specific item. You can also keep the number of query steps manageable to maintain fast load times, because each query step executes against the Log Analytics backend every time a parameter changes.

### Additional resources

* [Azure Monitor Workbooks overview](/en-us/azure/azure-monitor/visualize/workbooks-overview)
* [Workbooks parameters](/en-us/azure/azure-monitor/visualize/workbooks-parameters)
* [Workbooks visualizations](/en-us/azure/azure-monitor/visualize/workbooks-visualizations)

---

## Set alerts for app failures and anomalies

Dashboards and workbooks provide visibility into application health, but they require someone to be watching. Alert rules proactively notify your team when telemetry indicates a problem, ensuring that failures and performance degradation are detected even when no one is actively monitoring. This unit covers how developers configure Azure Monitor alert rules to detect application issues, set up action groups for notifications, and use smart detection for automatic anomaly identification.

### Understand the alert rule structure

Every Azure Monitor alert rule consists of four components that work together to detect problems and trigger responses. Understanding these components helps you design alert rules that balance sensitivity with noise reduction.

The four components are:

* **Scope:** The Azure resource or resources that the alert rule monitors. For application telemetry, the scope is typically an Application Insights resource or a Log Analytics workspace.
* **Condition:** The signal and threshold logic that determines when the alert fires. The condition specifies what data to evaluate and what constitutes a problem.
* **Action group:** The collection of notifications and automated actions that execute when the alert fires. Action groups are reusable across multiple alert rules.
* **Severity:** A classification from 0 (Critical) to 4 (Verbose) that indicates the urgency of the alert.

Azure Monitor supports two primary alert types for application telemetry. Metric alerts evaluate resource metrics at regular intervals and work well for straightforward threshold monitoring, such as detecting when CPU usage exceeds 80 percent or when request rates drop below a minimum. Log search alerts run KQL queries at a configured frequency and evaluate the results against a threshold. Log search alerts provide more flexibility because you can use any KQL query to define the detection logic, including queries that join across tables, calculate percentiles, or aggregate data by custom dimensions. For AI application monitoring, log search alerts are the more common choice because they let you express complex conditions that metric alerts can't capture.

Alert severity levels communicate the urgency of each alert to responders. Severity 0 (Critical) signals production\-impacting failures that require immediate response, such as a complete service outage. Severity 1 (Error) signals significant problems that affect functionality. Severity 2 (Warning) signals potential issues that need attention before they escalate. Severity 3 (Informational) tracks notable events that don't require immediate action. Severity 4 (Verbose) provides detailed diagnostic information. Assigning appropriate severity levels helps on\-call teams prioritize their response when multiple alerts fire simultaneously.

### Create log search alert rules

Log search alerts run a KQL query at a defined frequency and evaluate the results against a condition. The evaluation determines whether the query returns rows that indicate a problem, and if the condition is met, the alert fires and triggers the associated action group.

The key configuration options for log search alerts are evaluation frequency, aggregation granularity, and the threshold condition. The evaluation frequency controls how often the query runs, with options ranging from one minute to 24 hours. The aggregation granularity (window size) defines the time window that each evaluation covers. The threshold condition specifies whether the alert fires based on the number of returned rows or a calculated numeric value. You can also configure the number of violations required before the alert fires, which prevents single transient spikes from generating noise.

The following KQL query detects a high failure rate by counting failed requests per service and returning rows only for services that exceed 10 failures:

```
requests
| where success == false
| summarize failedCount = count() by cloud_RoleName
| where failedCount > 10

```

To configure this query as a log search alert, you set the aggregation granularity to five minutes, the evaluation frequency to five minutes, and the measure to table rows. The threshold is set to greater than zero, meaning the alert fires if the query returns any rows. Each returned row represents a service that exceeded 10 failures in the five\-minute window, providing immediate context about which services are affected.

For latency monitoring, a different threshold approach detects when response times exceed acceptable levels. The following query calculates the 95th\-percentile response time per service and returns rows for services where that percentile exceeds three seconds:

```
requests
| summarize p95Duration = percentile(duration, 95) by cloud_RoleName
| where p95Duration > 3000

```

Using percentile\-based thresholds instead of average\-based thresholds produces more actionable alerts. An average response time might remain within acceptable limits even when a significant percentage of users experiences slow responses. The 95th percentile captures the experience of the slowest five percent of requests, which often represents the users most likely to encounter problems.

### Configure action groups for notifications

Action groups define what happens when an alert fires. Each action group is a reusable collection of notification preferences and automated actions that you can attach to multiple alert rules. A single alert rule can reference up to five action groups, allowing you to send different types of notifications to different teams from the same alert.

Action groups support several notification types. Email notifications send an alert summary with a link to the fired alert in the Azure portal. SMS notifications deliver a short message to a phone number, which is useful for critical alerts that need immediate attention outside of working hours. Azure mobile app push notifications appear on devices with the Azure mobile app installed. Voice call notifications deliver an automated call to a phone number for the highest\-severity alerts.

Beyond notifications, action groups support automated actions that trigger workflows in response to alerts. You can configure an Azure Function to execute remediation logic, a Logic App to create a ticket in an external system, a webhook to call a third\-party incident management service, an Automation Runbook to execute a scripted recovery procedure, or an Event Hub to stream alert data into an event processing pipeline. These automated actions enable teams to respond to common problems without manual intervention.

When designing action groups, consider creating separate groups for different severity levels. A critical action group might include SMS and voice call notifications for the on\-call engineer plus a webhook to an incident management system. A warning action group might include only email notifications to the team distribution list. This separation ensures that critical alerts get immediate attention while less urgent alerts don't create notification fatigue. Test action groups using the portal's test feature before relying on them in production to verify that notifications reach the intended recipients.

### Use smart detection for anomaly identification

Azure Monitor smart detection uses machine learning to identify unusual patterns in application telemetry without requiring manual threshold configuration. Smart detection learns the normal behavior of your application over a baseline period and alerts when it detects significant deviations. This approach complements manual alert rules by catching unexpected problems that developers wouldn't anticipate when setting static thresholds.

Failure anomaly detection monitors the rate of failed requests and compares the current rate to the historical baseline. When smart detection identifies an abnormal rise in failures, it fires an alert that includes a cluster analysis showing the characteristic patterns of the anomalous failures. The analysis identifies affected users, correlated exceptions, and related dependencies, providing investigation context that goes beyond a simple "failure rate exceeded threshold" notification. This contextual information helps developers immediately focus on the root cause rather than spending time gathering diagnostic data.

Performance anomaly detection identifies response time degradation, dependency duration slowdowns, and abnormal exception volume increases. Smart detection recognizes gradual degradation patterns that might not trigger a fixed threshold alert because the values never exceed a specific number. Instead, it detects that performance is worse than its historical norm, which is often the earliest signal of an emerging problem.

Smart detection and manual alert rules serve different purposes and work best when used together. Smart detection is ideal for catching unexpected problems that developers wouldn't anticipate with static thresholds, such as a new type of exception that suddenly appears or a dependency that gradually degrades over weeks. Manual log search alerts are better for enforcing specific SLA thresholds or business rules, such as "the 95th\-percentile response time must stay below three seconds" or "fewer than one percent of requests should fail." Using both approaches together provides comprehensive coverage: manual alerts enforce known operational boundaries while smart detection watches for novel problems.

### Additional resources

* [Azure Monitor alerts overview](/en-us/azure/azure-monitor/alerts/alerts-overview)
* [Create a log search alert rule](/en-us/azure/azure-monitor/alerts/alerts-create-log-alert-rule)
* [Action groups](/en-us/azure/azure-monitor/alerts/action-groups)
* [Smart detection in Application Insights](/en-us/azure/azure-monitor/alerts/proactive-diagnostics)

---

## Exercise \- Query logs with KQL

Kusto Query Language (KQL) is the query language used to analyze log data in Application Insights. KQL queries let you filter, aggregate, and join telemetry tables such as requests, dependencies, and exceptions to diagnose application health and performance. The Logs blade in Application Insights provides an interactive query editor with autocomplete, visual results, and time range controls that make it the primary tool for investigating telemetry. Combined with scheduled query alert rules created through the Azure CLI, KQL enables proactive monitoring that notifies your team when failure rates or latency exceed acceptable thresholds.

In this exercise, you deploy an Application Insights resource, run a Python script that generates sample request, dependency, and exception telemetry using OpenTelemetry, then write KQL queries in the Azure portal Logs blade to investigate application health. You query the requests table to identify failures, join exceptions with requests to correlate errors, analyze dependency latency with percentile calculations, and create an action group and log search alert rule using the Azure CLI.

Tasks performed in this exercise:

* Download the project starter files
* Create an Application Insights resource
* Run the telemetry generator to create sample data
* Query telemetry with KQL in the Azure portal
* Create an action group and alert rule with the Azure CLI

This exercise takes approximately **20** minutes to complete.

### Before you start

To complete the exercise, you need:

* An Azure subscription. If you don't already have one, you can [sign up for one](https://azure.microsoft.com/).
* [Visual Studio Code](https://code.visualstudio.com/) on one of the [supported platforms](https://code.visualstudio.com/docs/supporting/requirements#_platforms).
* [Python 3\.12](https://www.python.org/downloads/) or greater.
* The latest version of the [Azure CLI](/en-us/cli/azure/install-azure-cli).

### Get started

Select the **Launch Exercise** button to open the exercise instructions in a new browser window. When you're finished with the exercise, return here to:

* Complete the module
* Earn a badge for completing this module

---

## Module assessment

Choose the best response for each of the following questions.

---

## Summary

In this module, you learned how to analyze application telemetry using Azure Monitor logs and metrics. You started by writing KQL queries that filter, aggregate, and visualize data from the Application Insights tables, using operators like `where`, `summarize`, `bin()`, and `render` to transform raw telemetry into actionable insights. You explored log data to identify error patterns, correlate failures across services using `operation_Id`, and measure dependency latency with percentile calculations. You built Azure dashboards by pinning metrics charts and log query results to create shared operational views that teams use for day\-to\-day monitoring. You also created Azure Monitor Workbooks with parameters and conditional visibility to enable interactive investigation and drill\-down analysis. Finally, you configured alert rules using KQL queries to detect failure spikes and performance degradation, set up action groups for notifications, and explored smart detection for automatic anomaly identification.

### Additional resources

* [KQL overview](/en-us/azure/azure-monitor/logs/log-query-overview)
* [Azure Monitor alerts overview](/en-us/azure/azure-monitor/alerts/alerts-overview)
* [Azure Monitor Workbooks overview](/en-us/azure/azure-monitor/visualize/workbooks-overview)
* [Application Insights data model](/en-us/azure/azure-monitor/app/data-model-complete)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/_

## Fuentes
- [Analyze app telemetry with logs and metrics](https://learn.microsoft.com/en-us/training/modules/analyze-telemetry-logs-metrics/?WT.mc_id=api_CatalogApi)
