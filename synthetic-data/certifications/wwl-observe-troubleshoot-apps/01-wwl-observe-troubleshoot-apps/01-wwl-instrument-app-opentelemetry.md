# Instrument an app with OpenTelemetry

> Curso: Observe and troubleshoot apps on Azure (wwl-observe-troubleshoot-apps) · Seccion: Observe and troubleshoot apps on Azure
> Duracion estimada: 79 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

AI applications built on distributed architectures require end\-to\-end visibility into request flows to maintain performance and reliability. This module guides you through instrumenting applications with OpenTelemetry on Azure to capture distributed traces, diagnose latency issues, and gain deep observability into AI solution components.

Imagine you're a developer building a retrieval\-augmented generation (RAG) pipeline for a customer support AI application. The system consists of four microservices: an API gateway that receives user queries, an embedding service that converts text into vector representations, a vector search service that retrieves relevant documents, and an LLM orchestration service that generates responses. Users report intermittent slow responses, but your team can't pinpoint which service causes the delays. Some requests complete in under two seconds, while others take over ten seconds. Without visibility into how a single request flows through all four services, debugging requires manually correlating logs across separate outputs. Each service writes its own log format to its own destination, making it difficult to reconstruct the full path of any given request. Your client expects 95th\-percentile response times under three seconds and needs a dashboard showing real\-time service health. OpenTelemetry provides the standardized instrumentation framework to capture traces across all services and export them to Azure Monitor for unified analysis and visualization.

After completing this module, you'll be able to:

* Explain how OpenTelemetry provides vendor\-neutral observability for distributed AI applications on Azure.
* Add and configure the Azure Monitor OpenTelemetry Distro in an application to collect telemetry data.
* Create and manage custom spans and traces to capture request flows across distributed services.
* Export telemetry data to Azure Monitor Application Insights for analysis and visualization.
* Use trace data in Application Insights to identify and debug performance issues in distributed workflows.

Note

All code examples in this module are based on the most recent version of the `azure-monitor-opentelemetry` package at the time of writing. The package is updated often and the recommendation is to visit the [Azure Monitor OpenTelemetry documentation](/en-us/azure/azure-monitor/app/opentelemetry-enable) for the most up\-to\-date information.

---

## Explore OpenTelemetry and its role in observability

Distributed AI applications present unique observability challenges because a single user request often spans multiple services, each with its own runtime, dependencies, and failure modes. Understanding how OpenTelemetry addresses these challenges gives you the foundation to instrument your applications effectively and gain the visibility needed to maintain performance and reliability.

### Understand observability for distributed AI applications

Observability is the ability to understand the internal state of a system by examining its external outputs. For distributed AI workloads that span multiple services, observability is essential because issues like latency spikes, failed requests, or degraded model performance can originate in any service along the request path. Without observability, diagnosing these issues requires guesswork and manual log correlation across separate systems.

Consider what happens when a single user query enters a RAG pipeline. The request touches an API gateway, an embedding generation service, a vector search service, and an LLM orchestration service. If the overall response takes ten seconds instead of two, you need to determine which service contributed the most latency. Was it the embedding generation? The vector search? The LLM API call? Without correlated telemetry, answering this question means opening four separate log outputs, searching for timestamps that roughly align, and hoping the logs capture enough detail to reconstruct the request flow.

Observability rests on three pillars that each provide a different perspective on system behavior:

* **Distributed tracing:** Captures the full path of a request as it moves through services. Traces show you the sequence and timing of operations, making it possible to identify exactly where delays or errors occur. Tracing is the primary focus of this module.
* **Metrics:** Provide aggregate numerical measurements over time, such as request counts, error rates, and response\-time percentiles. Metrics help you detect trends and set alerting thresholds for service\-level objectives.
* **Logs:** Capture detailed, timestamped records of discrete events within a service. Logs provide the granular detail needed to understand why a specific operation behaved the way it did.

Each pillar complements the others. Metrics tell you that something changed, traces tell you where the problem occurs, and logs tell you why it happened. Together, they provide the comprehensive visibility that AI applications require to meet performance targets and reliability expectations.

### Explore OpenTelemetry as a standard

OpenTelemetry is a vendor\-neutral, open\-source observability framework maintained by the Cloud Native Computing Foundation (CNCF). It provides a unified set of APIs, SDKs, and tools for generating, collecting, and exporting telemetry data. Microsoft is a Platinum Member of the CNCF and an active contributor to the OpenTelemetry project.

The framework consists of several key components that work together to enable observability:

* **APIs:** Define the interfaces for creating and managing telemetry data. These APIs are stable and designed to be embedded directly in application code and libraries.
* **SDKs:** Implement the APIs and provide configuration options for processing and exporting telemetry. The SDK handles batching, sampling, and resource detection.
* **Instrumentation libraries:** Automatically capture telemetry from common frameworks and libraries without requiring you to write instrumentation code. For example, an HTTP instrumentation library captures incoming and outgoing HTTP request details automatically.
* **Exporters:** Serialize and transmit collected telemetry to backend analysis tools. Different exporters send data to different backends.

Vendor neutrality is a core design principle of OpenTelemetry. You instrument your code once using the OpenTelemetry APIs, and you can export that telemetry to any compatible backend. This means you aren't locked into a specific monitoring vendor. You can send the same telemetry data to Azure Monitor, Jaeger, Prometheus, Grafana, or any other OpenTelemetry\-compatible system without changing your instrumentation code.

Microsoft provides the Azure Monitor OpenTelemetry Distro, which bundles the OpenTelemetry SDK with Azure Monitor\-specific exporters and commonly used instrumentation libraries. The Distro simplifies setup by packaging everything you need to send telemetry to Application Insights into a single package. It includes automatic instrumentation for popular frameworks, Azure\-specific resource detectors, and the Azure Monitor exporter. The exporter handles serialization and transport to the Application Insights ingestion endpoint.

### Understand traces, spans, and context propagation

A trace represents the complete record of a request's journey through a distributed system. Each trace consists of one or more spans that represent individual operations along the request path. Together, the spans in a trace form a tree structure that shows the full sequence and timing of work performed to handle a request.

A span is a named, timed operation within a trace. Each span captures information about a specific unit of work, such as an HTTP request, a database query, or a call to an external API. Every span contains the following key elements:

* **Trace ID:** A globally unique identifier shared by all spans in the same trace. This ID links every operation in the request flow together.
* **Span ID:** A unique identifier for this specific span within the trace.
* **Parent span ID:** The span ID of the parent operation that initiated this span. Root spans don't have a parent.
* **Name:** A descriptive label for the operation the span represents.
* **Start and end timestamps:** The precise timing of the operation, which determines its duration.
* **Attributes:** Key\-value pairs that provide additional context about the operation, such as the HTTP method, URL, status code, or custom data like a model name.
* **Status:** Indicates whether the operation succeeded or failed.

The span hierarchy defines the structure of a trace. The root span represents the entry point into the system, such as an incoming HTTP request to the API gateway. Child spans represent downstream operations triggered by the root request. When the API gateway calls the embedding service, that call creates a child span. When the embedding service calls the vector search service, another child span is created under the embedding span. This parent\-child relationship forms a tree that visually represents the work done to fulfill the original request.

Context propagation is the mechanism that carries trace and span IDs across service boundaries. Without context propagation, each service would create independent traces with no way to correlate them. OpenTelemetry uses the W3C TraceContext standard to propagate context through HTTP headers. When one service calls another, it includes a `traceparent` header that contains the trace ID and the calling span's ID:

```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01

```

The `traceparent` header contains four fields separated by hyphens:

* **Version (`00`):** The trace context format version.
* **Trace ID:** A 32\-character hexadecimal string that uniquely identifies the trace.
* **Parent span ID:** A 16\-character hexadecimal string identifying the calling span.
* **Trace flags (`01`):** Indicates the trace is sampled.

The receiving service reads this header, creates a new span with the same trace ID and the caller's span ID as its parent, and continues the trace. This process ensures that all spans across all services connect into a single, correlated trace.

### Compare OpenTelemetry terminology with Application Insights

When you work with both OpenTelemetry and Azure Monitor Application Insights, understanding how terminology maps between the two systems helps you navigate documentation, write queries, and interpret telemetry data correctly. OpenTelemetry uses its own vocabulary rooted in the open standard, while Application Insights uses terms established before OpenTelemetry became the industry standard.

The following table shows the key term mappings:

| OpenTelemetry concept | Python equivalent | Application Insights term |
| --- | --- | --- |
| Tracer | `trace.get_tracer("name")` | N/A (instrumentation source) |
| Span | `opentelemetry.trace.Span` | Request or Dependency |
| Server Span | `SpanKind.SERVER` | Request |
| Client Span | `SpanKind.CLIENT` | Dependency |
| Internal Span | `SpanKind.INTERNAL` | Dependency |
| Consumer Span | `SpanKind.CONSUMER` | Request |
| Producer Span | `SpanKind.PRODUCER` | Dependency |
| Trace ID | `span.get_span_context().trace_id` | Operation ID |
| Span ID | `span.get_span_context().span_id` | ID or Operation Parent ID |
| Span Attributes | `span.set_attribute()` | `customDimensions` |

Understanding this mapping matters in practice. When you write a KQL query in Application Insights, you search the `requests` table for server spans and the `dependencies` table for client and internal spans. The `operation_Id` field in Application Insights corresponds to the OpenTelemetry trace ID. When you set attributes on a span using `span.set_attribute()` in Python, those values appear in the `customDimensions` column in Application Insights query results. Knowing these mappings prevents confusion and helps you build effective queries and dashboards.

### Additional resources

* [OpenTelemetry overview for Application Insights](/en-us/azure/azure-monitor/app/opentelemetry-overview)
* [W3C Trace Context specification](https://www.w3.org/TR/trace-context/)

---

## Add the OpenTelemetry SDK to an application

Adding the OpenTelemetry SDK to your application is the first step toward capturing telemetry data. This unit covers installing the Azure Monitor OpenTelemetry Distro, understanding what it collects automatically, and configuring the essential settings that route telemetry to Application Insights.

Note

All code examples in this module use the Azure Monitor OpenTelemetry Distro packages and follow patterns from official Azure SDK documentation. The packages are updated regularly, and the recommendation is to visit the [Azure Monitor OpenTelemetry documentation](/en-us/azure/azure-monitor/app/opentelemetry-enable) for the most up\-to\-date information.

### Choose an instrumentation approach

Azure Monitor supports two primary instrumentation approaches, and choosing the right one depends on your hosting environment and the level of control you need over telemetry collection. Understanding the trade\-offs between these approaches helps you make the right decision for your AI application.

**Autoinstrumentation** enables telemetry collection through configuration without modifying application code. This approach works well for supported hosting environments like Azure App Service, Azure Functions, and Azure Virtual Machines, and it provides a quick path to basic observability. However, autoinstrumentation offers limited control over what other telemetry is collected and how you enrich it with custom data.

**Manual instrumentation** uses the OpenTelemetry SDK embedded in your application code. This approach gives you full control over telemetry collection, including the ability to create custom spans, add custom attributes, and configure sampling. For AI applications where you need to capture business\-specific operations like embedding generation timing or LLM token usage, SDK\-based instrumentation is the preferred choice.

The Azure Monitor OpenTelemetry Distro is the recommended SDK\-based approach. It's an [OpenTelemetry distribution](https://opentelemetry.io/docs/concepts/distributions/#what-is-a-distribution) that bundles the OpenTelemetry SDK with Azure Monitor exporters and commonly used instrumentation libraries into a single package. The Distro simplifies setup by providing everything you need to start collecting and exporting telemetry to Application Insights with minimal configuration.

### Install the Azure Monitor OpenTelemetry Distro

The Azure Monitor OpenTelemetry Distro for Python is distributed as a single pip package that includes the OpenTelemetry SDK, the Azure Monitor exporter, and automatic instrumentation libraries for common frameworks. You can install it with the following command:

```
pip install azure-monitor-opentelemetry

```

The minimal setup calls `configure_azure_monitor()` once at application startup. This single call initializes the tracer provider, the meter provider, and the logger provider, and configures all of them to export to Application Insights:

```
## Code fragment - focus on minimal OpenTelemetry setup with Azure Monitor
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

```

### Understand automatic data collection

The Azure Monitor OpenTelemetry Distro automatically collects telemetry from common frameworks and libraries without requiring you to write any instrumentation code. This automatic collection provides immediate visibility into your application's behavior as soon as you install and configure the Distro.

For Python applications, automatic collection includes the following instrumentation libraries:

* **`requests` library:** Captures outgoing HTTP calls as client spans. Each call to an external service or API, such as an embedding endpoint or an LLM API, is recorded as a dependency in Application Insights.
* **`urllib` / `urllib3`:** Captures outgoing HTTP calls made through Python's built\-in `urllib` module and the `urllib3` library as client spans.
* **Flask / Django / FastAPI:** Captures incoming HTTP requests as server spans, including route, status code, and duration. These appear as requests in Application Insights.
* **`psycopg2`:** Captures PostgreSQL database queries as dependency spans, including the database name and query execution time.
* **Azure SDK:** Captures calls to Azure services made through Azure SDK client libraries. This provides visibility into operations like storage access, message queue interactions, and secret retrieval from Key Vault.

Python's standard `logging` module is also integrated automatically. The Distro connects the OpenTelemetry logging pipeline to Python's built\-in logging infrastructure, which means logs produced through `logging.getLogger()` flow into Application Insights without extra configuration.

This automatic collection reduces boilerplate significantly. For many common scenarios in AI applications, such as capturing HTTP calls to embedding APIs, database queries for document retrieval, or Azure SDK calls to storage services, developers don't need to write any instrumentation code. The Distro handles these automatically.

### Configure the connection string

The connection string is the configuration value that tells the Azure Monitor exporter where to send telemetry data. It's unique to each Application Insights resource and contains the ingestion endpoint URL and an instrumentation key. Without a valid connection string, the exporter can't deliver telemetry to Application Insights.

You can configure the connection string using three approaches, listed here in order of preference for production environments:

**Environment variable (recommended for production):** You can set the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable, and the Distro picks it up automatically without any code changes. This approach keeps sensitive configuration out of your source code and makes it easy to change per environment.

```
export APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=00000000-0000-0000-0000-000000000000;IngestionEndpoint=https://eastus-0.in.applicationinsights.azure.com/"

```

**Code\-based configuration:** You can pass the connection string directly to `configure_azure_monitor()`. This approach is the least recommended for production because it embeds credentials in source code.

```
## Code fragment - focus on code-based connection string configuration
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string="InstrumentationKey=00000000-0000-0000-0000-000000000000;IngestionEndpoint=https://eastus-0.in.applicationinsights.azure.com/"
)

```

When you set the connection string in multiple places, the Distro follows this precedence order: code takes the highest priority, followed by environment variable.

### Set the cloud role name

When multiple services in a distributed application send telemetry to the same Application Insights resource, each service needs a distinct cloud role name to appear as a separate node on the Application Map. Without unique role names, all services appear as a single node, making it impossible to distinguish between them when debugging distributed request flows.

The cloud role name derives from the `service.name` and `service.namespace` OpenTelemetry resource attributes. Application Insights uses `service.namespace` combined with `service.name` to form the cloud role name. If `service.namespace` isn't set, Application Insights falls back to using `service.name` alone. You can also set the `service.instance.id` attribute to distinguish between multiple instances of the same service.

The following code fragment shows how to configure resource attributes in a Python application using `configure_azure_monitor()`:

```
## Code fragment - focus on setting cloud role name via resource attributes
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.sdk.resources import Resource

configure_azure_monitor(
    resource=Resource.create({
        "service.name": "embedding-service",
        "service.namespace": "rag-pipeline",
        "service.instance.id": "embedding-instance-1",
    })
)

```

In this example, the embedding service appears on the Application Map with the cloud role name "rag\-pipeline.embedding\-service". Each service in your RAG pipeline should use its own `service.name` value, such as "api\-gateway", "embedding\-service", "vector\-search\-service", and "llm\-orchestrator". Using a consistent `service.namespace` across all services groups them together logically on the Application Map.

You can also set resource attributes through environment variables without modifying code:

```
export OTEL_SERVICE_NAME="embedding-service"
export OTEL_RESOURCE_ATTRIBUTES="service.namespace=rag-pipeline,service.instance.id=embedding-instance-1"

```

### Additional resources

* [Enable Azure Monitor OpenTelemetry](/en-us/azure/azure-monitor/app/opentelemetry-enable)
* [Add and modify Azure Monitor OpenTelemetry](/en-us/azure/azure-monitor/app/opentelemetry-add-modify)

---

## Configure spans and traces

Automatic instrumentation captures telemetry from common frameworks like HTTP clients and database libraries, but it can't observe the custom business logic that makes your AI application unique. Operations like embedding generation, vector similarity scoring, prompt assembly, and LLM response parsing are specific to your application and require custom spans to appear in your traces. This unit covers creating custom spans and traces to capture these application\-specific operations.

Note

All code examples in this module use the Azure Monitor OpenTelemetry Distro packages and follow patterns from official Azure SDK documentation. The packages are updated regularly, and the recommendation is to visit the [Azure Monitor OpenTelemetry documentation](/en-us/azure/azure-monitor/app/opentelemetry-add-modify) for the most up\-to\-date information.

### Create custom spans with a tracer

Custom spans let you represent business\-specific operations in your trace data. In a RAG pipeline, you might create custom spans for operations like "generate embedding," "search vector index," "assemble prompt," or "call LLM API." These spans appear in the Application Insights end\-to\-end transaction view alongside automatically collected spans, giving you a complete picture of what your application does to fulfill each request.

In Python, the `opentelemetry.trace` module is the entry point for creating spans. You call `trace.get_tracer("name")` to obtain a tracer for your service or component. The name you provide identifies the instrumentation source in telemetry data. Unlike some other languages, Python requires no more registration steps. Calling `get_tracer()` after `configure_azure_monitor()` is all that's needed because the Distro configures the global tracer provider during setup.

The following code fragment shows how to create a tracer and start a custom span:

```
## Code fragment - focus on creating a custom tracer and span
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

configure_azure_monitor()

## Equivalent to creating an instrumentation source — use once per service/component
tracer = trace.get_tracer("embedding-service")

## start_as_current_span is a context manager — the span ends automatically when the block exits
with tracer.start_as_current_span("GenerateEmbedding") as span:
    span.set_attribute("embedding.model", "text-embedding-ada-002")
    span.set_attribute("embedding.token_count", token_count)
    # Embedding generation logic
    embedding = generate_embedding(input_text)

```

The `start_as_current_span` context manager starts the span when the `with` block is entered and ends it automatically when the block exits, whether normally or due to an exception. The span reference inside the `with` block is always valid, so there's no need for null checks.

### Add attributes to spans

Span attributes enrich your trace data with contextual information that helps you filter, search, and analyze traces. For AI applications, attributes like model names, token counts, document IDs, result counts, and user intent categories provide meaningful context that makes traces actionable rather than structural only.

The difference between resource attributes and span attributes is important to understand. Resource attributes describe the service itself and apply to all telemetry from that service. You set resource attributes once during startup, as shown in the previous unit with `service.name` and `service.namespace`. Span attributes describe a specific operation and apply only to the individual span. You set span attributes within the scope of an active span to capture details about that particular operation.

You can set attributes on a span using the `set_attribute()` method. Each attribute is a key\-value pair where the key is a string and the value can be a string, number, or boolean:

```
## Code fragment - focus on adding meaningful attributes to a span
with tracer.start_as_current_span("SearchVectorIndex") as span:
    span.set_attribute("search.index_name", "product-docs")
    span.set_attribute("search.query_vector_dimension", 1536)
    span.set_attribute("search.top_k", 10)
    results = search_index(embedding)
    span.set_attribute("search.result_count", len(results))
    span.set_attribute("search.similarity_threshold", 0.78)

```

When these attributes are exported to Application Insights, they appear in the `customDimensions` column. You can query them using KQL to filter and analyze traces based on specific attribute values, such as finding all traces where the result count was zero or where a particular model was used.

You can follow these best practices when naming attributes. You can use namespaced, descriptive keys like `embedding.model`, `search.result_count`, or `llm.token_count` to avoid collisions with other attribute names. This naming pattern also improves searchability in Application Insights queries. You should avoid using generic keys like `value` or `data` that don't convey meaning when viewed in a trace explorer.

### Control span kinds and status

The span kind indicates what type of operation a span represents, and Application Insights uses this value to classify spans as either requests or dependencies. Choosing the correct span kind ensures your telemetry appears in the right tables and visualizations within Application Insights.

OpenTelemetry defines five span kinds through the `SpanKind` enum in the `opentelemetry.trace` module:

* **`SpanKind.SERVER`:** Represents an incoming request handled by the service. Application Insights maps these spans to the `requests` table.
* **`SpanKind.CLIENT`:** Represents an outgoing call to an external service or resource. Application Insights maps these spans to the `dependencies` table.
* **`SpanKind.INTERNAL`:** Represents an internal operation within the service that doesn't cross process boundaries. Application Insights maps these spans to the `dependencies` table. This is the default when no kind is specified.
* **`SpanKind.PRODUCER`:** Represents a span that initiates an asynchronous operation, such as sending a message to a queue. Application Insights maps these spans to the `dependencies` table.
* **`SpanKind.CONSUMER`:** Represents a span that processes an asynchronous operation, such as receiving a message from a queue. Application Insights maps these spans to the `requests` table.

You can specify the span kind using the `kind` parameter when starting a span:

```
## Code fragment - focus on setting span kind for an outgoing LLM API call
from opentelemetry.trace import SpanKind

with tracer.start_as_current_span("CallLlmApi", kind=SpanKind.CLIENT) as span:
    span.set_attribute("llm.provider", "azure-openai")
    span.set_attribute("llm.model", "gpt-4o")
    # LLM API call logic
    response = call_llm(prompt)
    span.set_attribute("llm.response_tokens", response.usage.completion_tokens)

```

The Python SDK automatically records exceptions that propagate out of a `start_as_current_span` block and sets the span status to error. If you catch the exception yourself and want to provide a custom error description, you can call `span.record_exception()` and `span.set_status()` explicitly:

```
## Code fragment - focus on recording errors and exceptions on a span
from opentelemetry.trace import Status, StatusCode

with tracer.start_as_current_span("GenerateEmbedding") as span:
    try:
        embedding = generate_embedding(input_text)
        span.set_status(Status(StatusCode.OK))
    except Exception as ex:
        span.record_exception(ex)
        span.set_status(Status(StatusCode.ERROR, "Embedding generation failed"))
        raise

```

### Model nested operations in a trace

Nested spans create a parent\-child hierarchy that represents the logical flow of a request through your application. In Python, you achieve nesting by placing `start_as_current_span` context managers inside one another. When a new span starts while another span is active, the OpenTelemetry SDK automatically sets the active span as the parent of the new one. You don't need to pass parent references explicitly. The SDK tracks the current span for you using Python's context variable mechanism.

This hierarchy is valuable for AI applications because a single request typically involves multiple sequential operations. The parent\-child structure shows you exactly which operations happen within the scope of another operation, how long each one takes relative to the total, and where time is spent.

The following code fragment shows how nested spans model a simplified RAG pipeline request flow:

```
## Code fragment - focus on nested spans modeling a RAG pipeline request flow
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.trace import SpanKind

configure_azure_monitor()
tracer = trace.get_tracer("llm-orchestrator")

def process_query(query: str) -> str:
    with tracer.start_as_current_span("ProcessQuery", kind=SpanKind.SERVER) as root_span:
        root_span.set_attribute("query.length", len(query))

        # Child span: Generate embedding
        with tracer.start_as_current_span("GenerateEmbedding") as embed_span:
            embed_span.set_attribute("embedding.model", "text-embedding-ada-002")
            embedding = embedding_service.generate(query)
            embed_span.set_attribute("embedding.dimensions", len(embedding))

        # Child span: Search vector index
        with tracer.start_as_current_span("SearchVectorIndex") as search_span:
            search_span.set_attribute("search.top_k", 5)
            results = vector_search.search(embedding, top_k=5)
            search_span.set_attribute("search.result_count", len(results))

        # Child span: Call LLM
        with tracer.start_as_current_span("CallLlm", kind=SpanKind.CLIENT) as llm_span:
            prompt = build_prompt(query, results)
            llm_span.set_attribute("llm.prompt_tokens", count_tokens(prompt))
            response = llm_client.get_completion(prompt)
            llm_span.set_attribute("llm.response_tokens", response.usage.completion_tokens)
            return response.content

```

When you view this trace in the Application Insights end\-to\-end transaction view, you see a waterfall chart. `ProcessQuery` appears as the root span with `GenerateEmbedding`, `SearchVectorIndex`, and `CallLlm` as child spans nested underneath. The timeline shows each operation's duration and its relationship to the overall request time. If `CallLlm` takes eight seconds out of a ten\-second total, the visualization makes this bottleneck immediately obvious.

### Additional resources

* [Add custom spans](/en-us/azure/azure-monitor/app/opentelemetry-add-modify#add-custom-spans)
* [Add and modify Azure Monitor OpenTelemetry](/en-us/azure/azure-monitor/app/opentelemetry-add-modify)

---

## Export telemetry to Azure Monitor

After you instrument your application with the OpenTelemetry SDK and create custom spans, the next step is ensuring that telemetry data flows reliably to Azure Monitor Application Insights. This unit covers how the export pipeline works, how to configure sampling to manage costs, and how to verify that your telemetry data arrives correctly.

Note

All code examples in this module use the Azure Monitor OpenTelemetry Distro packages and follow patterns from official Azure SDK documentation. The packages are updated regularly, and the recommendation is to visit the [Azure Monitor OpenTelemetry documentation](/en-us/azure/azure-monitor/app/opentelemetry-configuration) for the most up\-to\-date information.

### Understand telemetry export to Application Insights

The telemetry export pipeline moves data from your application to Application Insights through a series of steps. The OpenTelemetry SDK collects telemetry from instrumentation libraries and custom spans. The Azure Monitor exporter serializes that data and sends it to the Application Insights ingestion endpoint identified by your connection string. This entire process happens in\-process within your application.

The Azure Monitor OpenTelemetry Distro uses direct export by default. Direct export means the application sends telemetry directly to the Application Insights ingestion endpoint without an intermediary. This approach simplifies deployment because there's no additional infrastructure to manage. The alternative approach uses the OpenTelemetry Collector, a separate process that receives telemetry from applications, processes it, and forwards it to one or more backends. The Collector approach adds operational complexity but provides additional capabilities like centralized sampling, data transformation, and multi\-backend routing.

When telemetry arrives in Application Insights, different signal types land in different tables. Understanding this mapping helps you write effective queries:

* **Server spans** (`SpanKind.SERVER` and `SpanKind.CONSUMER`) appear in the `requests` table.
* **Client, internal, and producer spans** (`SpanKind.CLIENT`, `SpanKind.INTERNAL`, and `SpanKind.PRODUCER`) appear in the `dependencies` table.
* **Log records** emitted through Python's `logging` module or the OpenTelemetry logging API appear in the `traces` table.
* **Exceptions** recorded on spans or captured through the `logging` module appear in the `exceptions` table.
* **Custom metrics** recorded through the OpenTelemetry Metrics API appear in the `customMetrics` table.

### Configure sampling to control telemetry volume

Sampling reduces the volume of telemetry data sent to Application Insights by collecting only a percentage of traces. For AI applications that handle high request volumes, sampling is essential for controlling ingestion costs. Without sampling, a service processing thousands of requests per minute generates significant telemetry data that can lead to unexpected costs.

The Azure Monitor OpenTelemetry Distro supports two sampling strategies for traces:

* **Fixed\-percentage sampling:** Collects a fixed fraction of all traces. You specify a ratio between 0\.0 and 1\.0 where 0\.1 means approximately 10% of traces are sampled.
* **Rate\-limited sampling:** Caps the number of traces collected per second. You specify the maximum traces per second, such as 1\.5 for approximately one and a half traces per second.

You can configure fixed\-percentage sampling in code using the `sampling_ratio` parameter, or rate\-limited sampling using `traces_per_second`:

```
## Code fragment - focus on configuring sampling via configure_azure_monitor()
from azure.monitor.opentelemetry import configure_azure_monitor

## Fixed-percentage sampling: sample approximately 10% of traces
configure_azure_monitor(
    sampling_ratio=0.1,
)

## Rate-limited sampling: sample approximately 1.5 traces per second
## configure_azure_monitor(
## traces_per_second=1.5,
## )

```

You can also configure sampling using environment variables, which is useful for adjusting sampling rates without redeploying your application:

```
## Fixed-percentage sampling at approximately 10%
export OTEL_TRACES_SAMPLER="microsoft.fixed_percentage"
export OTEL_TRACES_SAMPLER_ARG=0.1

```

```
## Rate-limited sampling at approximately 1.5 traces per second
export OTEL_TRACES_SAMPLER="microsoft.rate_limited"
export OTEL_TRACES_SAMPLER_ARG=1.5

```

When both code\-level options and environment variables are configured, environment variables take precedence. If you don't configure a sampler at all, the Python Distro uses `RateLimitedSampler` by default.

The trade\-off with sampling is important to understand. Lower sampling ratios reduce ingestion costs but decrease the accuracy of aggregated statistics shown in experiences like the Performance and Failures panes. The sampler attaches the sampling ratio to exported spans so Application Insights can adjust experience counts, but the fewer data points collected, the less precise these adjusted counts become. A good starting point is 5% (0\.05\), and you can adjust based on the accuracy shown in the failures and performance panes.

Note

Sampling decisions apply to traces (spans) only. Metrics are never sampled. Logs that belong to unsampled traces are dropped by default, but you can opt out of trace\-based sampling for logs if needed.

### Enable offline storage and automatic retries

The Azure Monitor exporter caches telemetry locally when the application loses connectivity to the Application Insights ingestion endpoint and retries sending for up to 48 hours. This built\-in resilience ensures that temporary network issues or service outages don't result in permanent telemetry data loss.

For Python applications, the exporter uses a subdirectory under the system's temp directory by default. The path is derived from the instrumentation key, process name, username, and application directory. This gives each application on the same host its own isolated storage location: `<tempfile.gettempdir()>/Microsoft-AzureMonitor-<hash>/opentelemetry-python-<instrumentation-key>`.

You can override the default storage directory in production if you need telemetry cached to a specific location:

```
## Code fragment - focus on configuring offline storage directory
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    storage_directory="/var/telemetry/rag-pipeline",
)

```

When application load is high, the exporter might occasionally drop telemetry if the volume exceeds the allowable time window or the maximum file size. In these cases, the exporter prioritizes recent events over older ones. You can also disable offline storage entirely by setting `disable_offline_storage=True`, though this isn't recommended for production environments where connectivity interruptions are possible.

### Verify telemetry data flow

After initial setup, it's important to verify that telemetry data actually arrives in Application Insights. Data might not appear immediately because the SDK batches telemetry before sending and there can be an ingestion delay of a few minutes.

The first step is to check the Application Insights overview pane in the Azure portal. After running your application and generating some traffic, you should see server requests and response times on the overview charts. If these charts show data, your instrumentation is working correctly.

For real\-time verification during development, Live Metrics provides a dashboard that displays telemetry data with minimal delay. Live Metrics bypasses the normal ingestion pipeline to show incoming requests, outgoing dependencies, and exceptions as they happen. This feature is useful for verifying that new custom spans and attributes appear correctly before deploying to production. Live Metrics is enabled by default in the Azure Monitor OpenTelemetry Distro.

You can also run a KQL query in the Application Insights Logs section to verify that trace data is available:

```
requests
| where timestamp > ago(1h)
| project timestamp, name, duration, success, cloud_RoleName
| order by timestamp desc
| take 20

```

This query returns the 20 most recent requests from the last hour, showing the operation name, duration, success status, and the cloud role name of the service that handled the request. If you see results, your telemetry pipeline is working end to end. If you see requests from multiple services, context propagation is also functioning correctly, and you can proceed to analyze distributed traces.

### Additional resources

* [Configure Azure Monitor OpenTelemetry](/en-us/azure/azure-monitor/app/opentelemetry-configuration)
* [Sampling in Application Insights](/en-us/azure/azure-monitor/app/sampling)

---

## Debug distributed flows with trace data

Collecting and exporting telemetry is only valuable when you can use that data to find and fix problems. This unit covers how to use Application Insights tools and KQL queries to navigate distributed traces, identify performance bottlenecks, and diagnose issues specific to AI workloads.

### Navigate the Application Map

The Application Map provides a visual topology of all services in your distributed application, showing how they connect and where failures or latency problems occur. Each node on the map represents a cloud role, identified by the `service.name` resource attribute you configured during setup. Edges between nodes represent calls from one service to another, such as the API gateway calling the embedding service.

The Application Map displays key metrics on each node and edge, including average response time, request count, and failure rate over the selected time range. These metrics give you a rapid overview of system health without querying data manually. A node with high average duration or elevated failure rate stands out visually, making it easy to spot which service in your RAG pipeline needs attention.

You can use the map to quickly narrow your investigation. If the vector search service node shows an average response time of five seconds while all other nodes average under 500 milliseconds, you've immediately identified the service contributing the most latency. Selecting a node opens detailed metrics and lets you drill into specific requests and dependencies for that service. Selecting an edge shows the call characteristics between two services, including response time distribution and failure rates.

### Use end\-to\-end transaction details

The end\-to\-end transaction view displays a waterfall chart of all spans in a single trace, showing the timing, duration, and dependencies for each operation. This view is the primary tool for understanding what happens during a specific request and identifying exactly where time is spent.

You can navigate to the transaction view from several places in Application Insights. You can select a specific request in the Performance pane, choose a failed request in the Failures pane, or select a node on the Application Map and drill into individual transactions. Each path leads to the same detailed view of a single distributed trace.

The waterfall chart shows the root span at the top, representing the entry point of the request. Child spans nest underneath their parent spans, indented to show the hierarchical relationship. The horizontal timeline shows when each span starts and how long it takes. Sequential operations appear one after another, while parallel operations overlap in the timeline.

Reading the waterfall chart reveals the bottleneck. If the total request duration is 10 seconds and the LLM API call span takes eight seconds, the LLM call is the primary contributor to overall latency. If the embedding generation span shows consistent 200\-millisecond timing but the vector search span varies between 100 milliseconds and five seconds, the vector search service has an intermittent performance issue. The visual layout makes these patterns immediately apparent.

Each span in the waterfall shows additional detail when you select it, including the operation name, duration, status code, and any custom attributes you set using `set_attribute()`. If you recorded exceptions on a span, the exception details appear in this view as well, showing the exception type, message, and stack trace alongside the span that captured the error.

### Write KQL queries to analyze trace data

Application Insights stores telemetry in Log Analytics tables that you can query using Kusto Query Language (KQL). Writing KQL queries gives you precise control over trace analysis, letting you answer specific questions about your application's behavior across time ranges, services, and operational patterns that the visual tools can't address directly.

Trace data lands in four primary tables. The `requests` table contains server spans and consumer spans. The `dependencies` table contains client, internal, and producer spans. The `traces` table contains log records. The `exceptions` table contains recorded exceptions. All tables share the `operation_Id` column, which corresponds to the OpenTelemetry trace ID and lets you correlate all telemetry items belonging to the same distributed trace.

The following query finds slow requests and summarizes them by service:

```
requests
| where duration > 3000
| summarize count(), avg(duration) by cloud_RoleName
| order by avg_duration desc

```

This query returns the count and average duration of requests that took longer than three seconds, grouped by cloud role name. The results show you which services contribute the most slow requests and help you prioritize your investigation.

You can join requests with their dependencies to find slow downstream calls that contribute to overall latency:

```
requests
| where duration > 5000
| join kind=inner (dependencies) on operation_Id
| project timestamp, requestName = name, requestDuration = duration,
    dependencyName = name1, dependencyDuration = duration1,
    dependencyTarget = target
| order by requestDuration desc

```

This query connects each slow request with its downstream dependency calls, showing you which outgoing calls contributed to the overall request duration. The `operation_Id` join links all spans in the same distributed trace. If you see that most slow requests have a dependency named "CallLlmApi" with durations over four seconds, you identified the downstream call causing the latency.

You can also query custom attributes stored in `customDimensions` to analyze AI\-specific metrics:

```
dependencies
| where name == "GenerateEmbedding"
| extend tokenCount = toint(customDimensions["embedding.token_count"]),
    model = tostring(customDimensions["embedding.model"])
| summarize avg(duration), percentile(duration, 95),
    avg(tokenCount) by model
| order by avg_duration desc

```

This query analyzes embedding generation performance by model, showing average and 95th\-percentile durations alongside average token counts. Custom attributes that you set on spans using `set_attribute()` become queryable dimensions that let you segment and filter trace data in ways that are specific to your AI workload.

### Apply diagnostic patterns for AI workloads

AI applications have distinctive failure and performance patterns that differ from traditional web applications. Understanding these patterns helps you interpret trace data effectively and build monitoring that catches problems early.

**Embedding generation timeouts** occur when the embedding model API takes too long to respond or becomes unavailable. You can identify these by querying for dependency spans named after your embedding operation. You can look for spans with durations exceeding your timeout threshold or spans with error status codes. Setting an attribute like `embedding.model` on these spans helps you determine whether the issue is model\-specific or affects all embedding calls.

**Vector search cold starts** manifest as high variability in vector search span durations. The first few queries after a period of inactivity might take significantly longer than subsequent queries because the search index needs to load data into memory. You can identify this pattern by looking for clusters of slow search spans that follow periods with no search activity. Querying span attributes like `search.result_count` helps you distinguish between cold starts and genuinely slow queries that return many results.

**LLM token rate limiting** shows up as dependency spans to the LLM API with HTTP 429 status codes or unusually long durations caused by retry delays. Setting attributes like `llm.prompt_tokens` and `llm.response_tokens` on your LLM call spans lets you correlate rate limiting with token usage patterns. You can also identify whether specific queries consume more tokens than expected.

**Context window overflow** occurs when the assembled prompt exceeds the LLM's maximum context window, causing the API to return an error. Adding a `llm.prompt_tokens` attribute to your prompt assembly span helps you detect when prompts approach the context limit and take corrective action.

Building proactive monitoring around these patterns improves reliability. You can:

* Set alerts in Application Insights for latency thresholds on specific operations.
* Use workbooks to create dashboards that display AI pipeline health metrics.
* Correlate trace data with custom metrics to identify trends before they affect users.

### Additional resources

* [Application Map in Application Insights](/en-us/azure/azure-monitor/app/app-map)
* [Transaction diagnostics](/en-us/azure/azure-monitor/app/transaction-search-and-diagnostics)

---

## Exercise \- Instrument an app with the OpenTelemetry SDK

OpenTelemetry is an open\-source observability framework that provides a standardized way to collect traces, metrics, and logs from applications. The Azure Monitor OpenTelemetry Distro packages the OpenTelemetry SDK with the Azure Monitor exporter so Python applications can send telemetry to Application Insights with minimal configuration. Custom spans let you trace application\-specific operations and add attributes that enrich trace data with business context.

In this exercise, you deploy an Application Insights resource and build a Python Flask web application that demonstrates OpenTelemetry instrumentation for a document processing pipeline. You configure the Azure Monitor OpenTelemetry Distro, create custom parent and child spans for each pipeline stage, add span attributes to capture document metadata, and use Transaction search and log queries in the Azure portal to verify your telemetry and diagnose a simulated latency bottleneck.

Tasks performed in this exercise:

* Download the project starter files
* Create an Application Insights resource
* Add code to the starter files to complete the app
* Run the app and diagnose a performance issue in Application Insights

This exercise takes approximately **25** minutes to complete.

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

In this module, you learned how OpenTelemetry provides a vendor\-neutral, open\-source framework for instrumenting distributed applications on Azure. You explored the three pillars of observability and how traces, spans, and context propagation work together to capture end\-to\-end request flows across service boundaries. You learned how the W3C TraceContext standard carries trace IDs through `traceparent` headers, enabling services to participate in the same distributed trace without vendor\-specific integration. You added the Azure Monitor OpenTelemetry Distro to a Python application and configured it using `configure_azure_monitor()` to collect telemetry automatically from frameworks like Flask, the `requests` library, and the Azure SDK. You also created custom spans using `trace.get_tracer()` and `start_as_current_span()` to capture business\-specific operations like embedding generation and LLM API calls. You enriched those spans with attributes using `set_attribute()` to provide meaningful context. You configured sampling using the `sampling_ratio` parameter to balance observability with ingestion costs. You then verified that telemetry data flows correctly to Application Insights. Finally, you used the Application Map to visualize service topology, the end\-to\-end transaction view to examine individual request flows, and KQL queries to analyze trace data and identify performance bottlenecks in a distributed AI pipeline.

### Additional resources

* [OpenTelemetry overview for Application Insights](/en-us/azure/azure-monitor/app/opentelemetry-overview)
* [Enable Azure Monitor OpenTelemetry](/en-us/azure/azure-monitor/app/opentelemetry-enable)
* [Add and modify Azure Monitor OpenTelemetry](/en-us/azure/azure-monitor/app/opentelemetry-add-modify)
* [Configure Azure Monitor OpenTelemetry](/en-us/azure/azure-monitor/app/opentelemetry-configuration)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/_

## Fuentes
- [Instrument an app with OpenTelemetry](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/?WT.mc_id=api_CatalogApi)
