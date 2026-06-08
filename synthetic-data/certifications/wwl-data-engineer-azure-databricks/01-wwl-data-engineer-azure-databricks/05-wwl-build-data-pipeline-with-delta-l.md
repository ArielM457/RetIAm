# Build Lakeflow Declarative Pipelines

> Curso: Implement a Data Analytics Solution with Azure Databricks (wwl-data-engineer-azure-databricks) · Seccion: Implement a Data Analytics Solution with Azure Databricks
> Duracion estimada: 85 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You and your team of data engineers want to focus on what really matters: shaping data so it’s ready for the business. That means transforming and aggregating it, preparing it for BI, data science, and machine learning. But before you can even get there, you’re stuck figuring out where the data actually lives—scattered across your data lake and data warehouse. Then comes the demand to support streaming pipelines for new use cases, enable generative AI projects, and manage orchestration, all while juggling version control, CI/CD, and deployment infrastructure. Add in data quality checks, governance, and discovery, and the challenges only grow. And beyond that, there’s the operational grind—hand\-coding backfills, managing dependencies, partitions, checkpointing, and retries—when all you really want is to deliver reliable data.

That’s why building and running data pipelines is so difficult. Development is slow and labor\-intensive, pipelines are fragile and error\-prone, and delays ripple into the business. Operational complexity drives downtime, wasted resources, and engineering toil. And with batch and streaming often siloed, adapting to new requirements around latency, cost, and SLAs feels rigid and expensive.

With Lakeflow Declarative Pipelines, you and your team can leave those headaches behind. Instead of wrestling with orchestration and infrastructure, you can focus on writing and managing transformation logic. It's a framework within the Databricks Lakehouse Platform for building and running data pipelines in a **declarative** manner. The result: clean, reliable data pipelines, delivered with less effort and far more confidence.

Lakeflow Declarative Pipelines has several features for streamlining data engineering tasks and for enhancing data infrastructure reliability. You can define **data quality** rules and *expectations* directly within your pipeline code. The system monitors data quality in real\-time, providing visibility and control over your data's integrity. With **Change Data Capture** (CDC), it handles inserts, updates, and deletes automatically in addition to handling out\-of\-order events.

---

## Explore Lakeflow Declarative Pipelines

Lakeflow Declarative Pipelines is a framework in Azure Databricks for building and running both batch and streaming data pipelines. Instead of requiring engineers to write step\-by\-step instructions for data movement and transformations, Lakeflow Declarative Pipelines lets them declare the desired data flows and outcomes. The system then takes responsibility for orchestrating execution, ensuring reliability, and managing incremental updates. Pipelines in this framework can include flows that ingest and process data, streaming tables that continuously update with new events, materialized views that maintain precomputed results, and sinks that deliver outputs to external systems.

### What problem does it aim to solve?

Traditional data engineering pipelines are often imperative and low\-level. Developers must define exactly how to ingest data, manage state, handle late\-arriving events, recover from failures, and process incremental updates efficiently. This is both time\-consuming and error\-prone, especially when combining batch workloads with real\-time streaming needs or when working with change data capture scenarios. Lakeflow Declarative Pipelines address these challenges by abstracting away much of the operational complexity. Instead of worrying about checkpoints, retry strategies, or dependencies between steps, engineers simply describe what data transformations and outputs are required, and the framework ensures the pipeline executes correctly and consistently.

### What are the benefits?

The declarative approach brings several advantages:

* It **simplifies development** by letting engineers focus on business logic rather than operational details.
* It improves efficiency through **incremental processing**: materialized views and flows only reprocess new or changed data, which reduces compute cost and latency.
* It unifies **streaming and batch** semantics, so the same framework can power both real\-time and scheduled workloads.
* **Reliability** is built in through automatic retries at multiple levels, dependency management, and orchestration of flows within a pipeline.
* It also provides native support for common enterprise needs such as **change data capture** and **slowly changing dimensions**, reducing the amount of custom code needed for these scenarios.
* Lakeflow Declarative Pipelines can **dynamically scale** resources based on a workload, which means that it can handle increases in data volume without manual intervention.

### Key Concepts

The following diagram illustrates the most important concepts of Lakeflow Declarative Pipelines.

#### Pipeline

The pipeline is the top\-level structure that contains all logic and execution in Lakeflow Declarative Pipelines. It defines the set of flows, streaming tables, materialized views, and sinks that together make up a data system. The pipeline automatically understands dependencies between components, determines the correct order of execution, and handles fault tolerance and retries. For the data engineer, the pipeline serves as the single definition that captures the full lifecycle of ingestion, transformation, and delivery.

#### Flow

A flow represents a transformation step within a pipeline. It reads data from a source, applies logic, and writes the result to a target. Flows can be either batch or streaming, depending on the needs of the workload. They can operate in append mode, where new data is simply added to the target, or in automatic change data capture (AUTO CDC) mode, where changes are tracked and applied to maintain an up\-to\-date representation of the source. Flows are the primary mechanism by which data moves and evolves inside a pipeline.

#### Streaming Table

A streaming table is a managed table that continuously ingests and updates with new data. It's the natural target for streaming flows, ensuring that data remains fresh as events arrive. Streaming tables integrate seamlessly with Unity Catalog, so they're governed and managed like other tables in Databricks. They can capture raw event data or maintain processed representations, and because they're managed resources, they automatically benefit from the reliability, orchestration, and incremental logic of the pipeline framework.

#### Materialized View

A materialized view is a managed table designed for batch\-oriented but incremental processing. Rather than recomputing the entire dataset each time, a materialized view only processes data that has changed since the last run. This allows complex transformations and aggregations to be kept up\-to\-date without high costs or long runtimes. Materialized views are useful for building curated datasets, summary tables, or analytical layers on top of raw ingested data.

#### Sink

A sink is a destination for pipeline output that exists outside the managed table environment. Sinks are used primarily with streaming flows to deliver data to external systems, such as Kafka topics, Azure Event Hubs, or other Delta tables. They allow a pipeline to not only manage internal transformations but also publish results to downstream services, applications, or consumers. Sinks extend the reach of a pipeline beyond the Databricks environment, enabling it to power real\-time data products and integrations.

---

## Data ingestion and integration

Data ingestion and integration form the foundational layer for effective data processing in Lakeflow Declarative Pipelines within Azure Databricks. This ensures that data from various sources is accurately and efficiently loaded into the system for further analysis and processing.

Lakeflow Declarative Pipelines facilitates data ingestion and integration through:

* **Multi\-source ingestion**: allows you to collect data from various sources.
* **Stream and batch data processing**: enables you to process data either continuously or in grouped intervals.
* **Schema management**: ensures that your data is well\-structured and easy to manage.
* **Data quality and governance**: helps you maintain the integrity and compliance of your data
* **Pipeline automation and orchestration**: streamlines and controls the sequence of your data processing tasks
* **Integration with Azure ecosystem**: allows you to interact smoothly with various Azure tools and services
* **Performance optimization**: enhances your ability to process data quickly and effectively
* **Monitoring and lineage tracking**: helps you track the data's journey and monitor its movement through the system.

### Create a pipeline

First, you create an ETL pipeline in Lakeflow Declarative Pipelines. Lakeflow Declarative Pipelines creates pipelines by resolving dependencies defined in notebooks or files (called source code) using Lakeflow Declarative Pipelines syntax. Each source code file can contain only one language, but you can add multiple language\-specific notebooks or files in the pipeline.

In your workspace, you can create a new ETL Pipeline from the **Jobs \& Pipelines** section in the sidebar. You should assign a **name** to the pipeline, configure a **notebook** or **files** that contain the source code, and set the **destination** storage location and schema.

### Load from an existing table

In your notebook, you can load data from any existing table in Databricks. You can transform the data using a query, or load the table for further processing in your pipeline.

```
CREATE OR REFRESH MATERIALIZED VIEW top_baby_names_2021
COMMENT "A table summarizing counts of the top baby names for New York for 2021."
AS SELECT
  First_Name,
  SUM(Count) AS Total_Count
FROM baby_names_prepared
WHERE Year_Of_Birth = 2021
GROUP BY First_Name
ORDER BY Total_Count DESC

```

### Load files from cloud object storage

Databricks recommends using **Auto Loader** with Lakeflow Declarative Pipelines for most data ingestion tasks from cloud object storage or from files in a Unity Catalog volume. Auto Loader and Lakeflow Declarative Pipelines are designed to incrementally and idempotently load ever\-growing data as it arrives in cloud storage.

Auto Loader can ingest `JSON`, `CSV`, `XML`, `PARQUET`, `AVRO`, `ORC`, `TEXT`, and `BINARYFILE` file formats.

The following SQL example reads data from cloud storage using Auto Loader:

```
CREATE OR REFRESH STREAMING TABLE sales
  AS SELECT *
  FROM STREAM read_files(
    'abfss://myContainer@myStorageAccount.dfs.core.windows.net/analysis/*/*/*.json',
    format => "json"
  );

```

The following SQL example use Auto Loader to create datasets from CSV files in a Unity Catalog volume:

```
CREATE OR REFRESH STREAMING TABLE customers
AS SELECT * FROM STREAM read_files(
  "/Volumes/my_catalog/retail_org/customers/",
  format => "csv"
)

```

### Parsing JSON

In Lakeflow Declarative Pipelines, when you parse JSON data using the function `from_json`, you can let the system automatically figure out the JSON schema (inference) and adjust it over time (evolution) rather than hardcoding a schema upfront. This is useful when schemas aren't known ahead of time or when they change often.

Each `from_json` expression, when set up for inference \+ evolution, needs a unique identifier called the `schemaLocationKey`. It lets the system keep track of which JSON schema belongs to which parsing expression. If you have multiple JSON parsing expressions in your pipeline, each must use a distinct schemaLocationKey. Also, the key must be unique in the context of a given pipeline.

Here's an example using SQL syntax demonstrating setting the schema argument to NULL, signaling that schema should be inferred rather than fixed:

```
SELECT
  value,
  from_json(value, NULL, map('schemaLocationKey', 'keyX')) parsedX,
  from_json(value, NULL, map('schemaLocationKey', 'keyY')) parsedY,
FROM STREAM READ_FILES('/databricks-datasets/nyctaxi/sample/json/', format => 'text')

```

You have the option instead to use a fixed schema with `from_json(jsonStr, schema, ...)`. If you choose fixed schema, then inference \& evolution aren't used. Also, schema hints are useful when you want fixed schema but also want to anticipate or handle schema drift.

Here's an example in SQL where the query takes a JSON string containing two fields, a and b, and parses it into a structured object using the schema specified in the second argument. Here, the schema declares a as an integer and b as a double, so the result is a `STRUCT<a: INT, b: DOUBLE>`

```
SELECT from_json('{"a":1, "b":0.8}', 'a INT, b DOUBLE');

```

### Manage data quality with pipeline expectations

Optionally, you can use expectations to apply quality constraints that validate data as it flows through ETL pipelines. Expectations provide greater insight into data quality metrics and allow you to fail updates or drop records when detecting invalid records.

Important

The **Advanced** product edition of Lakeflow Declarative Pipelines is required to use expectations. If your pipeline includes expectations with the Core or Pro editions, you receive an error.

Here's an example of a materialized view that defines a constraint clause. In this case, the constraint contains the actual logic for what is being validated: the Country\_Region shouldn't be empty. When a record fails this condition, the expectation is triggered.

```
CREATE OR REFRESH MATERIALIZED VIEW processed_covid_data (
 CONSTRAINT valid_country_region EXPECT (Country_Region IS NOT NULL) ON VIOLATION FAIL UPDATE
)
COMMENT "Formatted and filtered data for analysis."
AS
SELECT
   TO_DATE(Last_Update, 'MM/dd/yyyy') as Report_Date,
   Country_Region,
   Confirmed,
   Deaths,
   Recovered
FROM raw_covid_data;

```

Examples of constraints:

```
-- Simple constraint
CONSTRAINT non_negative_price EXPECT (price >= 0) ON VIOLATION DROP ROW

-- SQL functions
CONSTRAINT valid_date EXPECT (year(transaction_date) >= 2020) ON VIOLATION FAIL UPDATE

-- CASE statements
CONSTRAINT valid_order_status EXPECT (
  CASE
    WHEN type = 'ORDER' THEN status IN ('PENDING', 'COMPLETED', 'CANCELLED')
    WHEN type = 'REFUND' THEN status IN ('PENDING', 'APPROVED', 'REJECTED')
    ELSE false
  END
)

-- Multiple constraints
CONSTRAINT non_negative_price EXPECT (price >= 0),
CONSTRAINT valid_purchase_date EXPECT (date <= current_date())

-- Complex business logic
CONSTRAINT valid_subscription_dates EXPECT (
  start_date <= end_date
  AND end_date <= current_date()
  AND start_date >= '2020-01-01'
)

-- Complex boolean logic
CONSTRAINT valid_order_state EXPECT (
  (status = 'ACTIVE' AND balance > 0)
  OR (status = 'PENDING' AND created_date > current_date() - INTERVAL 7 DAYS)
)

```

Retaining invalid records is the default behavior for expectations. Records that violate the expectation are added to the target dataset along with valid records. If you specify `ON VIOLATION DROP ROW`, then records that violate the expectation are dropped from the target dataset. Finally, if you specify `ON VIOLATION FAIL UPDATE`, then the system atomically rolls back the transaction.

### Apply transformations

You can transform the data using a query, just like with standard SQL commands. In the following example, we define another materialized view that aggregates data.

```
CREATE OR REFRESH MATERIALIZED VIEW aggregated_covid_data
COMMENT "Aggregated daily data for the US with total counts."
AS
SELECT
   Report_Date,
   sum(Confirmed) as Total_Confirmed,
   sum(Deaths) as Total_Deaths,
   sum(Recovered) as Total_Recovered
FROM processed_covid_data
GROUP BY Report_Date;

```

### Execute and monitor the ETL pipeline

After you defined the code in notebooks or source code files, you can start the ETL pipeline. There's a visual interface you can use to monitor the execution:

The pipeline graph appears as soon as an update to a pipeline has successfully started. Arrows represent dependencies between data sets in your pipeline. By default, the pipeline details page shows the most recent update for the table, but you can select older updates from a drop\-down menu.

Lakeflow Declarative Pipelines support tasks such as:

* Observing the progress and status of pipeline updates.
* Alerting on pipeline events such as the success or failure of pipeline updates.
* Viewing metrics for streaming sources like Apache Kafka and Auto Loader.
* Receiving email notifications when a pipeline update fails or completes successfully.

### Develop with the Lakeflow Pipelines Editor

The **Lakeflow Pipelines Editor** is the integrated development environment for creating and iterating on pipeline source code. When you create a new pipeline, the editor provides a default folder structure with a `transformations/` directory for source code and an `explorations/` directory for ad hoc analysis notebooks. Store your pipeline source code in a Git folder to enable version control.

The editor supports iterative development through several features:

* **Dry run**: Validates your pipeline code without processing data, allowing you to catch syntax errors and missing dependencies before execution.
* **Selective execution**: Run individual files or single table definitions rather than the entire pipeline, enabling faster iteration during development.
* **Interactive DAG**: Visualize the dependency graph between your tables, select specific tables for targeted refreshes, and inspect execution metrics.
* **Data preview**: Sample data from streaming tables and materialized views directly in the editor to verify transformation logic.

---

## Real\-time processing

A streaming table is a Delta table that includes support for streaming and incremental data processing. Unlike traditional tables, a streaming table is designed to continuously accept data as it arrives. It's updated by flows within a pipeline and is useful for scenarios where new data must be ingested or transformed on an ongoing basis.

Streaming tables are especially useful for data ingestion because they process each input row only once, which matches most ingestion workloads. They're capable of handling large volumes of append\-only data efficiently. They're also valuable in low\-latency transformations because they can process data over rows and windows of time, manage high volumes of input, and deliver results with minimal delay.

### How Streaming tables work

When a streaming table is updated, the flows associated with it read new information from the streaming source and append it to the table. The table is defined in the pipeline’s source code, and only that pipeline has the authority to update it. If a streaming table is created outside of a pipeline in Databricks SQL, the system automatically generates a hidden pipeline to manage its updates.

In practice, multiple flows can append data to the same streaming table. Conceptually, you can imagine a streaming table as the central destination in an ETL process where flows continuously supply new data.

### Create streaming tables

In SQL, you can define a streaming table with Lakeflow Declarative Pipelines as follows:

```
CREATE OR REFRESH STREAMING TABLE customers_bronze
AS SELECT * FROM STREAM read_files(
  "/volumes/path/to/files",
  format => "json"
);

```

### Append\-only behavior

Streaming tables are designed to work with append\-only data sources. Once a row has been appended to the table, it isn't reprocessed even if the query defining the table changes. For example, if the original query transforms names to lowercase and is later modified to transform them to uppercase, the rows that were already appended remain in lowercase. Only new rows arriving after the change are processed with the updated logic. If you need to update all rows with the new transformation, you must trigger a full refresh of the pipeline.

### Low\-latency streaming

Streaming tables are optimized for low\-latency workloads through checkpoint management. They operate best when working with bounded streams. A naturally bounded stream occurs when the data source has a clear start and end, such as a directory of files that isn't updated after an initial batch. Another way to bound a stream is by applying a watermark. A watermark in Spark Structured Streaming specifies how long the system should wait for late\-arriving data before it closes a window of time. Without a watermark, an unbounded stream could accumulate state indefinitely, leading to pipeline failures caused by memory pressure.

### Stream\-snapshot joins

Streaming tables also support joins between a live stream and a static snapshot of a dimension table. In this scenario, the dimension table is treated as a snapshot at the moment the stream starts. Any changes to the dimension after the stream begins aren't reflected in the join unless the dimension table is explicitly refreshed. This approach is often acceptable in use cases where the fact table is extremely large compared to the dimension table, and a small discrepancy is tolerable.

### Limitations of Streaming Tables

Streaming tables have the following limitations:

* **Limited evolution**: Changing queries only affects new rows; old rows remain unchanged unless full refresh is triggered.
* **State management**: Requires bounded or watermarked streams to avoid failures.
* **Joins don't recompute**: Joins don’t update when dimension tables change. For always\-correct joins, use materialized views.

---

## Exercise \- Create a Lakeflow Declarative Pipeline

Now it's your chance to create a Lakeflow Declarative Pipeline.

Note

To complete this lab, you need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) in which you have administrative access.

Launch the exercise and follow the instructions.

---

## Summary

Lakeflow Declarative Pipelines are a powerful framework provided by Databricks that simplifies the construction and management of reliable data pipelines for big data and machine learning applications. Utilizing Lakeflow Declarative Pipelines, developers can define data transformations declaratively in Python or SQL, which the system automatically orchestrates and manages.

In this module, you learned how to:

* Describe Lakeflow Declarative Pipelines
* Ingest data into materialized views and streaming tables
* Use Lakeflow Declarative Pipelines for Real time Data Processing

### Learn more

* [Lakeflow Declarative Pipelines](/en-us/azure/databricks/ldp/concepts)
* [Load data with Lakeflow Declarative Pipelines](/en-us/azure/databricks/dlt/load)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/build-data-pipeline-with-delta-live-tables/_

## Fuentes
- [Build Lakeflow Declarative Pipelines](https://learn.microsoft.com/en-us/training/modules/build-data-pipeline-with-delta-live-tables/?WT.mc_id=api_CatalogApi)
