# Develop event-driven AI workflows with Azure Event Grid

> Curso: Integrate backend services for AI solutions (wwl-integrate-backend-services-ai-solutions) · Seccion: Integrate backend services for AI solutions
> Duracion estimada: 84 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

AI applications require immediate, coordinated responses to system events such as new data arrivals, completed model training, or pipeline stage transitions. This module guides you through using Azure Event Grid to build event\-driven AI workflows on Azure that react to state changes in real time.

Imagine you're a developer building an AI\-powered content moderation platform that processes images and text uploaded to Azure Blob Storage. Each upload triggers a series of downstream operations: an embeddings service generates vector representations, a classification model assigns content categories, and a notification service alerts reviewers when content is flagged. Currently, each service polls for new data on a fixed interval, creating delays between upload and processing, wasting compute resources on empty polls, and making it difficult to add new processing steps without modifying existing services. During traffic spikes, the polling intervals can't keep up, and newly uploaded content waits minutes before processing begins. Your team needs an architecture where each component reacts to events as they occur rather than checking for changes on a schedule. When a new image arrives in storage, the system should immediately trigger the embeddings pipeline without any service needing to know about the others. Failed processing attempts should retry automatically, and permanently failed events should route to a dead\-letter destination for investigation. The platform also needs to emit its own custom events when processing completes, so additional downstream services can subscribe without modifying the existing pipeline. Azure Event Grid provides the event\-driven routing, filtering, and delivery guarantees that this architecture requires.

After completing this module, you'll be able to:

* Explain how Azure Event Grid enables event\-driven patterns in AI solutions and identify the core components (topics, event subscriptions, and event handlers) that form an event\-routing architecture.
* Design events using the CloudEvents schema for AI operations, define custom event types, and configure event subscriptions with filters that route events based on type, subject, or data attributes.
* Configure delivery and retry policies to handle transient failures in AI pipelines, set dead\-letter destinations for undeliverable events, and monitor delivery outcomes.
* Publish custom events from AI applications to signal completed inferences, model updates, or pipeline stage transitions using the Event Grid SDK and REST API.

Note

All code examples in this module are based on the most recent version of the `azure-eventgrid` library at the time of writing. The library is updated often and the recommendation is to visit the [Azure Event Grid SDK for Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/eventgrid/azure-eventgrid) site for the most up\-to\-date information.

---

## Understand Azure Event Grid concepts and event\-driven patterns for AI solutions

Azure Event Grid is a fully managed event\-routing service that connects event sources to event handlers with low latency and per\-event pricing. For AI solutions, Event Grid eliminates the need to poll for state changes by delivering events directly to your application endpoints as those changes occur. This unit introduces the core Event Grid components and explains how event\-driven architecture addresses common challenges in AI backends.

### Understand what Azure Event Grid provides

Azure Event Grid operates as a publish\-subscribe service that routes events from sources to handlers without requiring you to manage messaging infrastructure. The service ingests events from Azure services, custom applications, and partner systems, then delivers those events to subscriber endpoints based on subscription filters. Event Grid handles millions of events per second with subsecond latency and charges on a per\-event basis, so you pay only for the events your system processes.

Event Grid supports two delivery models. Push delivery sends events to an endpoint that you specify, such as a webhook, Azure Function, or Service Bus queue. Pull delivery lets your consumer application connect to Event Grid and read events at its own pace. Both models serve different architectural needs, and you choose the right one based on whether your handler can accept incoming HTTP requests or prefers to consume events on demand.

Event Grid natively integrates with Azure services through [system topics](/en-us/azure/event-grid/system-topics) and supports custom application events through [custom topics](/en-us/azure/event-grid/custom-topics). This combination means that your AI solution can react to both infrastructure\-level events (a blob appears in storage, a container image is pushed to a registry) and application\-level events (an inference completes, a model finishes training) using the same routing infrastructure.

### Identify the core components of Event Grid architecture

Event Grid architecture consists of five core components that work together to route events from producers to consumers. Understanding each component helps you design event\-driven pipelines that scale and adapt as you add new AI capabilities.

#### Events

An event is a lightweight notification that describes a state change. Events indicate that something happened, such as "blob created" or "model training completed," without carrying the full changed resource. The subscriber retrieves the resource separately if it needs the complete data. This design keeps events small and fast to deliver, which is important for AI workflows that generate thousands of events during batch processing runs.

Each event contains metadata that identifies what happened, where it happened, and when it happened. The event body includes a data payload with operation\-specific details, but the payload should remain compact. For example, a blob creation event includes the blob URL and content type but doesn't embed the blob content itself.

#### Event sources

Event sources are Azure services or custom applications that emit events. Azure services such as Blob Storage, Azure Key Vault, Azure Container Registry, and Azure Event Hubs automatically publish events as system topics. Custom applications publish events to custom topics that you create. An AI application might act as both a consumer and a source. It subscribes to storage events to detect new training data and publishes its own events when model training completes.

#### Topics

Topics are endpoints that receive events from sources. Event Grid uses three types of topics:

* **System topics:** Event Grid creates these automatically for Azure service events. When you create an event subscription for a supported Azure resource, the system topic appears without any manual setup. You can't publish directly to system topics because only the Azure service itself emits events to them.
* **Custom topics:** These are user\-defined endpoints where your applications post events. You create a custom topic, configure its input schema, and then publish events to its endpoint using the Event Grid SDK or REST API.
* **Namespace topics:** These are part of the Event Grid namespace resource and support both push and pull delivery. Namespace topics offer additional capabilities such as MQTT support and are suited for scenarios where you need more control over event consumption.

#### Event subscriptions

An event subscription is a configuration resource that defines which events to receive from a topic and where to send them. Each subscription specifies a topic to listen on, optional filters to select specific events, and a destination endpoint (the event handler). You can create multiple subscriptions on the same topic to fan out events to different handlers. Filters let you narrow the events each subscription receives by event type, subject path, or data attributes.

#### Event handlers

Event handlers are destinations that receive and process events. Event Grid supports several handler types for push delivery:

* **Azure Functions:** Processes events using serverless compute with automatic scaling
* **Azure Event Hubs:** Ingests events into a high\-throughput streaming pipeline
* **Azure Service Bus queues and topics:** Delivers events to enterprise messaging infrastructure
* **Webhooks:** Sends events to any HTTP endpoint, including custom services
* **Azure Storage queues:** Queues events for asynchronous processing by worker applications

The handler you choose depends on your processing requirements. Azure Functions works well for lightweight, stateless event processing. Service Bus queues suit scenarios where you need guaranteed ordering or transactional processing. Webhooks provide flexibility to route events to any HTTP\-capable service, including AI inference endpoints.

### Explore how AI architectures benefit from event\-driven patterns

AI workflows involve multiple loosely coupled components that need to coordinate without tight dependencies. Traditional polling\-based architectures introduce latency, waste compute on empty checks, and create coupling between producer and consumer services. Event\-driven architecture addresses each of these problems by pushing notifications to interested parties as state changes occur.

When a new dataset arrives in Blob Storage, Event Grid immediately notifies the embeddings pipeline rather than waiting for a polling interval to elapse. This approach reduces end\-to\-end latency from minutes to seconds. When a model finishes retraining, a custom event can trigger downstream validation and deployment services without any service needing to know about the others. Components subscribe to only the events they care about, and new consumers can be added without modifying producers.

Event\-driven patterns also improve fault isolation. If one consumer experiences an outage, other consumers continue to receive and process events independently. Event Grid's retry mechanism automatically redelivers failed events, so transient issues in a single AI service don't create data loss across the pipeline.

### Apply event\-driven patterns to AI workloads

Several event\-driven patterns apply directly to AI systems. Each pattern addresses a specific coordination challenge that arises when building multi\-stage AI processing pipelines.

#### Reactive data processing

You can subscribe to Blob Storage events (`Microsoft.Storage.BlobCreated`) to trigger an AI pipeline whenever new training data, documents, or images arrive. The pipeline receives the event, retrieves the blob using the URL in the event data, and processes it without maintaining a polling loop. This pattern works for scenarios such as document ingestion in a RAG pipeline, image classification from an upload queue, or dataset preparation for model retraining.

#### Pipeline stage coordination

Multi\-step AI pipelines benefit from custom events that signal stage transitions. When an embeddings generation step completes, it publishes an event that triggers the indexing step. Each stage operates independently and scales based on its own workload. This decoupling allows you to replace or upgrade individual stages without disrupting the entire pipeline. It also provides natural observability boundaries because each stage transition creates a trackable event.

#### Model lifecycle management

You can publish custom events for model training completion, validation results, and deployment promotions. Downstream services subscribe to these events to update serving endpoints, refresh model caches, or notify stakeholders. For example, when a model's validation accuracy exceeds a threshold, a custom event triggers a deployment workflow that promotes the model to production.

### Compare system topics and custom topics

For most AI workflows, you use both system topics and custom topics. System topics handle infrastructure events that originate from Azure services. Custom topics handle application\-level events that your code produces. The following table summarizes when to use each type.

| Aspect | System topics | Custom topics |
| --- | --- | --- |
| **Event source** | Azure services (Blob Storage, Key Vault, Container Registry) | Your application code |
| **Creation** | Created automatically when you subscribe to an Azure resource's events | Created explicitly by you before publishing |
| **Publishing** | Only the Azure service publishes events | Your application publishes events via SDK or REST API |
| **Use cases** | React to data arrivals, secret rotations, image pushes | Signal inference completion, pipeline transitions, anomaly detection |
| **Schema** | Predefined by the Azure service | You define the event type and data schema |

In a content moderation platform, you would use a system topic to receive `Microsoft.Storage.BlobCreated` events when users upload content. Your classification service would then consume these events, process the content, and publish a custom event like `com.contoso.ai.ContentClassified` to a custom topic. Downstream services such as the notification service and the analytics dashboard would subscribe to that custom topic independently.

### Additional resources

* [What is Azure Event Grid?](/en-us/azure/event-grid/overview)
* [Concepts in Azure Event Grid](/en-us/azure/event-grid/concepts)
* [System topics in Azure Event Grid](/en-us/azure/event-grid/system-topics)

---

## Work with event schemas and properties

The structure of your events determines how Event Grid routes, filters, and delivers them to subscribers. This unit covers how to design events using the CloudEvents schema for AI operations, define custom event types that represent meaningful state changes, and configure event subscription filters to route events based on type, subject, or data attributes.

Note

All code examples in this module are based on the most recent version of the `azure-eventgrid` library at the time of writing. The library is updated often and the recommendation is to visit the [Azure Event Grid SDK for Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/eventgrid/azure-eventgrid) site for the most up\-to\-date information.

### Choose between Event Grid schema and CloudEvents schema

Event Grid supports two event schemas: the proprietary Event Grid schema and the open [CloudEvents v1\.0 schema](/en-us/azure/event-grid/cloud-event-schema). CloudEvents is the recommended format for new implementations because it provides a standardized, protocol\-agnostic event structure backed by the Cloud Native Computing Foundation (CNCF). The standardization means that events produced by your AI services can interoperate with any system that supports CloudEvents, not just Azure Event Grid.

CloudEvents simplifies multi\-platform integration with a minimal set of required attributes and a well\-defined extension mechanism. If your AI pipeline involves components outside of Azure, CloudEvents ensures consistency across boundaries. Event Grid natively supports CloudEvents JSON format and HTTP protocol binding, so you don't need to transform events before publishing or consuming them.

The proprietary Event Grid schema remains available for backward compatibility. Existing Azure [system events](/en-us/azure/event-grid/system-topics) can be delivered in CloudEvents format by configuring the output schema on the event subscription. However, CloudEvents\-to\-Event Grid schema conversion isn't supported because CloudEvents supports extension attributes that the Event Grid schema doesn't accommodate.

### Understand the CloudEvents schema structure

A CloudEvents event contains required attributes that identify the event and optional attributes that provide additional context. For AI operations, each attribute plays a specific role in routing and filtering decisions.

The following example shows a CloudEvents JSON event for a completed inference operation in a content moderation pipeline:

```
{
    "specversion": "1.0",
    "type": "com.contoso.ai.InferenceCompleted",
    "source": "/services/content-moderation",
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "time": "2025-09-15T14:30:00Z",
    "subject": "/pipelines/moderation/batch-42",
    "datacontenttype": "application/json",
    "data": {
        "modelName": "content-classifier-v3",
        "requestId": "req-78901",
        "resultLocation": "https://storage.blob.core.windows.net/results/batch-42.json",
        "processingDurationMs": 1250,
        "status": "success",
        "itemsProcessed": 150
    }
}

```

The required attributes serve the following purposes:

* **`specversion`:** Identifies the CloudEvents specification version. Always set this to `"1.0"`.
* **`type`:** Categorizes the event. This field drives event type filtering. Use a reverse\-DNS naming convention to avoid collisions across organizations and services.
* **`source`:** Identifies the originating system or component. Combine with `type` to uniquely identify the context in which the event happened.
* **`id`:** Provides a unique identifier for this specific event. Subscribers use this field to detect and deduplicate repeated deliveries.

The optional attributes add context that enables more granular routing:

* **`subject`:** Provides a path for filtering. Set this to a hierarchical value that reflects the event context, enabling prefix and suffix filtering on subscriptions.
* **`time`:** Records when the event occurred in UTC. Useful for monitoring and debugging.
* **`datacontenttype`:** Describes the format of the data payload, typically `"application/json"`.
* **`data`:** Carries the event payload with operation\-specific details.

### Design custom event types for AI workflows

Well\-designed event types make your event\-driven AI pipeline easier to filter, monitor, and extend. Each event type should represent a meaningful state change that at least one subscriber needs to know about. Define types using a reverse\-DNS naming convention to avoid collisions with events from other teams or services.

Common event types for AI applications include:

* **`com.contoso.ai.InferenceCompleted`:** Published when an inference request finishes processing
* **`com.contoso.ai.EmbeddingsRefreshed`:** Published when a vector embedding index is updated
* **`com.contoso.ai.BatchProcessingStarted`:** Published when a batch processing job begins
* **`com.contoso.ai.AnomalyDetected`:** Published when the system identifies an anomaly in incoming data
* **`com.contoso.ai.ModelRetrained`:** Published when a model completes a retraining cycle
* **`com.contoso.ai.ContentClassified`:** Published when a content moderation classification finishes

Keep the event payload small and focused. Include enough context for the subscriber to begin processing, such as a resource URI, model name, processing duration, and a result summary. Don't embed full inference results in the event data. Instead, include a reference (like a storage URL) that the subscriber uses to retrieve detailed results from a data store.

### Configure event type filtering

Event subscriptions can filter events by type to ensure that each handler receives only the events it needs. This approach keeps handlers focused and avoids unnecessary invocations. For AI workflows where different services process different event types, type filtering routes each event to the right handler without custom routing logic in your code.

You can configure event type filtering when you create an event subscription. The `--included-event-types` parameter accepts a list of event types that the subscription delivers. Events with types not in the list are filtered out before delivery. The following example creates an event subscription that only receives inference completion events:

```
az eventgrid event-subscription create \
    --name inference-handler-sub \
    --source-resource-id /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.EventGrid/topics/ai-events \
    --endpoint https://inference-handler.azurewebsites.net/api/events \
    --included-event-types com.contoso.ai.InferenceCompleted

```

You can include multiple event types in a single subscription by listing them separated by spaces. A monitoring service that tracks both inference completions and anomaly detections would include both types in its subscription filter.

### Apply subject filtering for granular routing

The `subject` field enables path\-based filtering using prefix and suffix matches. For AI applications, set the subject to a hierarchical path that reflects the event context, such as `/pipelines/embeddings/batch-42` or `/models/classification/v3`. Subscribers can then filter events based on where in the hierarchy the event originated.

Subject filtering uses two parameters on the event subscription:

* **`subjectBeginsWith`:** Matches events whose subject starts with the specified prefix. Use this to route events from a specific pipeline or service category.
* **`subjectEndsWith`:** Matches events whose subject ends with the specified suffix. Use this to filter by file type, version, or status.

The following example creates a subscription that receives only events from the embeddings pipeline:

```
az eventgrid event-subscription create \
    --name embeddings-sub \
    --source-resource-id /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.EventGrid/topics/ai-events \
    --endpoint https://embeddings-handler.azurewebsites.net/api/events \
    --subject-begins-with /pipelines/embeddings

```

You can combine subject filtering with event type filtering on the same subscription. An event subscription that filters on both type and subject prefix only receives events matching all specified criteria.

### Use advanced filtering on data attributes

Event Grid supports [advanced filters](/en-us/azure/event-grid/event-filtering#advanced-filtering) that match on values within the event body or extension attributes. Advanced filters let you make routing decisions based on the content of the event data, such as confidence scores, model names, or processing statuses. This capability is particularly useful for AI events where the routing decision depends on the event's payload.

Advanced filters use operators such as `StringContains`, `NumberGreaterThan`, `StringBeginsWith`, `BoolEquals`, and `IsNotNull`. You can define up to 25 filter conditions per subscription. Multiple conditions use AND logic between conditions and OR logic within each condition's values.

The following example creates a subscription that receives only events where the `data.status` field equals `"flagged"`. A moderation review service would use this filter to receive only content that needs human review:

```
az eventgrid event-subscription create \
    --name flagged-content-sub \
    --source-resource-id /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.EventGrid/topics/ai-events \
    --endpoint https://review-service.azurewebsites.net/api/events \
    --advanced-filter data.status StringIn flagged

```

For AI events, advanced filters enable targeted routing scenarios such as:

* **Confidence\-based routing:** Route events to different handlers based on a confidence score threshold, such as `data.confidence NumberGreaterThan 0.9` for high\-confidence results and a separate subscription for lower scores
* **Model\-specific subscriptions:** Filter on `data.modelName` to subscribe to events from a particular model version
* **Status\-based workflows:** Route only failed or flagged events to a review queue while completed events flow to a dashboard service

### Configure the input and output schema

When creating a custom topic, the `input-schema` parameter controls which schema the topic accepts. Set this to `cloudeventschemav1_0` to accept events in CloudEvents format:

```
az eventgrid topic create \
    --name ai-events \
    --resource-group ai-platform-rg \
    --location eastus \
    --input-schema cloudeventschemav1_0

```

When creating an event subscription, the `event-delivery-schema` parameter controls the format delivered to the handler. Event Grid can convert between Event Grid schema and CloudEvents schema during delivery. If your topic uses the Event Grid schema but your handler expects CloudEvents, you can set the output schema accordingly. However, CloudEvents\-to\-Event Grid conversion isn't supported because CloudEvents supports extension attributes that the Event Grid schema can't represent. For new implementations using CloudEvents throughout, you can omit this parameter and the events deliver in the same format they were published.

### Additional resources

* [CloudEvents v1\.0 schema with Azure Event Grid](/en-us/azure/event-grid/cloud-event-schema)
* [Azure Event Grid event schema](/en-us/azure/event-grid/event-schema)
* [Understand event filtering for Event Grid subscriptions](/en-us/azure/event-grid/event-filtering)

---

## Configure delivery and retry policies for reliable event processing

AI pipeline endpoints don't always respond successfully on the first attempt. Model services restart, serverless functions experience cold starts, and downstream dependencies go offline temporarily. This unit covers how Event Grid handles delivery failures through its retry mechanism, how to customize retry policies for different AI workload patterns, how to configure dead\-letter destinations for events that can't be delivered, and how to monitor delivery outcomes.

### Understand how Event Grid delivers events

Event Grid delivers events by sending an HTTP POST request to the subscriber's endpoint. The subscriber must respond with a success status code (200, 201, 202, 203, or 204\) to acknowledge receipt. Any other response code, or no response within the timeout period, triggers a retry. Event Grid waits 30 seconds for a response after delivering a message. If the endpoint hasn't responded within that window, Event Grid queues the message for retry.

Event Grid delivers one event at a time by default, with the payload as an array containing a single event. This default behavior ensures that each event is independently acknowledged and retried. For high\-throughput AI workloads, you can enable output batching to group multiple events per delivery request, which reduces HTTP overhead and improves throughput.

Event Grid provides at\-least\-once delivery, which means that subscribers might receive the same event more than once. This guarantee matters for AI pipelines because it means your handler endpoints must be idempotent. Use the event `id` field to detect and deduplicate repeated deliveries. For example, if your inference service receives the same event twice, it should check whether it already processed a result for that event ID before starting a new inference run.

### Examine the retry schedule and error handling

When Event Grid receives an error response, it evaluates the error type to decide whether to retry. Configuration\-related errors that can't be fixed with retries are handled differently from transient errors.

The following errors aren't retried because they indicate permanent issues:

* **400 Bad Request:** The event payload is malformed or the endpoint can't process it
* **413 Request Entity Too Large:** The event exceeds the endpoint's size limit
* **403 Forbidden:** The endpoint explicitly rejects the delivery

For webhook endpoints, a 401 Unauthorized response is also not retried. For Azure resource endpoints, 401 and 404 responses trigger a retry after five minutes or more because these errors might resolve as the resource finishes provisioning.

For all other errors, Event Grid applies an exponential backoff retry schedule:

1. 10 seconds
2. 30 seconds
3. One minute
4. Five minutes
5. 10 minutes
6. 30 minutes
7. One hour
8. Three hours
9. Six hours
10. Every 12 hours up to 24 hours

Event Grid adds randomization to retry intervals to spread load and might skip retries if an endpoint appears consistently unhealthy. If the endpoint responds within three minutes, Event Grid attempts to remove the event from the retry queue on a best\-effort basis, but duplicates might still be received.

### Customize retry policy settings

You can adjust two parameters when creating an event subscription to control retry behavior. Event Grid uses whichever limit is reached first to stop retrying and either drop or dead\-letter the event.

* **Maximum number of attempts:** An integer between one and 30 (default: 30\). Event Grid stops retrying after this many delivery attempts.
* **Event time\-to\-live (TTL):** An integer between one and 1,440 minutes (default: 1,440 minutes, or 24 hours). Event Grid stops retrying after this time elapses from the event's original publish time.

The right configuration depends on your AI workload's latency tolerance. For time\-sensitive operations such as real\-time content classification, set a shorter TTL so stale events don't consume handler resources when the window for useful processing has passed. For batch processing pipelines that can tolerate delays, use longer TTL values with more retry attempts to maximize the chance of successful delivery.

The following example creates an event subscription with a 30\-minute TTL and a maximum of five delivery attempts:

```
az eventgrid event-subscription create \
    --name moderation-sub \
    --source-resource-id /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.EventGrid/topics/ai-events \
    --endpoint https://moderation-service.azurewebsites.net/api/events \
    --max-delivery-attempts 5 \
    --event-ttl 30

```

Keep in mind that the exponential backoff schedule interacts with your TTL setting. With the default retry schedule, only about six delivery attempts complete within the first 30 minutes. Setting max delivery attempts to 10 with a 30\-minute TTL has no additional effect because the TTL expires first.

### Configure dead\-letter destinations for undeliverable events

When Event Grid exhausts all retry attempts or the event TTL expires, it can send the undelivered event to a [dead\-letter destination](/en-us/azure/event-grid/manage-event-delivery). Dead\-lettering is disabled by default. To enable it, you specify an Azure Blob Storage container as the dead\-letter endpoint when creating the event subscription. You must create the storage account and container before configuring dead\-lettering.

```
az eventgrid event-subscription create \
    --name moderation-sub \
    --source-resource-id /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.EventGrid/topics/ai-events \
    --endpoint https://moderation-service.azurewebsites.net/api/events \
    --max-delivery-attempts 5 \
    --event-ttl 30 \
    --deadletter-endpoint /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{storage-account}/blobServices/default/containers/dead-letters

```

Each dead\-lettered event includes diagnostic properties that help you understand why delivery failed. These properties appear alongside the original event data in the dead\-letter blob:

* **`deadLetterReason`:** The reason the event was dead\-lettered (for example, `MaxDeliveryAttemptsExceeded` or `MaxRetryDurationExceeded`)
* **`deliveryAttempts`:** The number of delivery attempts before the event was dead\-lettered
* **`lastDeliveryOutcome`:** The result of the last delivery attempt (for example, `NotFound`, `TimedOut`, `Busy`, or `Forbidden`)
* **`publishTime`:** The UTC time when Event Grid accepted the event
* **`lastDeliveryAttemptTime`:** The UTC time of the last delivery attempt

For AI pipelines, dead\-lettered events often indicate systemic issues that need investigation. A batch of dead\-lettered events with `lastDeliveryOutcome` of `NotFound` might mean your handler endpoint URL changed. A cluster of `TimedOut` outcomes might indicate that your inference service is overloaded and needs scaling adjustments.

You can also set up an event subscription on the dead\-letter Blob Storage container itself. This approach notifies a monitoring service whenever a new dead\-lettered event arrives, enabling automated alerting or reprocessing workflows.

### Handle transient failures in AI pipelines

AI handler endpoints experience several categories of transient failures that Event Grid's retry mechanism handles automatically. Model service restarts cause brief periods of unavailability. Serverless functions on consumption plans experience [cold\-start latency](/en-us/azure/azure-functions/event-driven-scaling#cold-start) that can exceed Event Grid's 30\-second response timeout. GPU memory pressure during peak inference loads can cause temporary request failures. Downstream dependency outages, such as a vector database being temporarily unavailable, cause the handler to return error codes.

Event Grid's exponential backoff and retry behavior addresses these transient failures without requiring you to build custom retry logic. However, you should design your handler endpoints to support this pattern:

* **Return appropriate status codes:** Return 200\-204 for successful processing. Return 503 if your service is temporarily overloaded. Don't return 400 for transient issues because Event Grid won't retry 400 responses.
* **Implement idempotent processing:** Keep track of event IDs you've already processed. Event Grid's at\-least\-once guarantee means your handler might receive the same event more than once.
* **Process quickly or acknowledge early:** If your inference operation takes longer than 30 seconds, return 202 (Accepted) immediately and process the event asynchronously. Event Grid interprets a 202 response as successful delivery.

### Enable output batching for high\-throughput AI workloads

For AI systems that generate or consume events at high volume, such as processing thousands of document uploads or image classifications, output batching reduces the number of HTTP requests to the handler. You configure batching on the event subscription with two parameters:

* **Maximum events per batch:** An integer between one and 5,000\. Event Grid won't exceed this number, but might deliver fewer events if less are available.
* **Preferred batch size in kilobytes:** An integer between one and 1,024\. Event Grid targets this batch size, but a single event larger than the preferred size still delivers in its own batch.

```
az eventgrid event-subscription create \
    --name batch-processor-sub \
    --source-resource-id /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.EventGrid/topics/ai-events \
    --endpoint https://batch-processor.azurewebsites.net/api/events \
    --max-events-per-batch 100 \
    --preferred-batch-size-in-kilobytes 512

```

Batching uses all\-or\-none delivery semantics. The handler must return a success code for the entire batch. If any event in the batch fails, the entire batch is retried. Design your handler to process all events in a batch or reject the entire batch by returning an appropriate error code. Don't set the batch size larger than what your handler can reliably process within the 30\-second response timeout.

### Monitor delivery outcomes

Event Grid publishes delivery metrics through [Azure Monitor](/en-us/azure/event-grid/monitor-event-delivery) that give you visibility into how events flow through your AI pipeline. Key metrics include:

* **Delivery success count:** Events successfully delivered to handler endpoints
* **Delivery failure count:** Events that failed delivery (individual attempt failures, not final failures)
* **Matched events:** Events that matched at least one subscription filter
* **Dropped events:** Events that matched a subscription but exceeded retry limits without dead\-lettering
* **Dead\-lettered events:** Events sent to the dead\-letter destination after exhausting retries

You can set alerts on these metrics to detect systemic issues in your pipeline. A sudden increase in dead\-lettered events might indicate that a model service is down, a handler endpoint URL changed, or a deployment introduced a bug. A drop in matched events might mean that your event source stopped publishing or that a filter configuration changed unexpectedly. Monitoring these metrics alongside your application logs provides a complete picture of event flow health across your AI solution.

### Additional resources

* [Event Grid message delivery and retry](/en-us/azure/event-grid/delivery-and-retry)
* [Dead letter and retry policies](/en-us/azure/event-grid/manage-event-delivery)
* [Monitor Event Grid message delivery](/en-us/azure/event-grid/monitor-event-delivery)

---

## Publish custom events from AI applications

The previous units covered how Event Grid routes events from sources to handlers and how to configure filtering and delivery policies. This unit focuses on the other side of the equation: publishing custom events from your AI applications. You learn how to create custom topics, construct well\-structured events for AI operations, and use the Event Grid SDK and REST API to emit events that signal completed inferences, model updates, and pipeline stage transitions.

Note

All code examples in this module are based on the most recent version of the `azure-eventgrid` library at the time of writing. The library is updated often and the recommendation is to visit the [Azure Event Grid SDK for Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/eventgrid/azure-eventgrid) site for the most up\-to\-date information.

### Create a custom topic for AI events

A custom topic provides a user\-defined endpoint where your application posts events. Before your AI application can publish events, you need to create the topic and configure it to accept the schema your events use. Set the input schema to `cloudeventschemav1_0` when creating the topic so events follow the standardized CloudEvents format.

```
az eventgrid topic create \
    --name ai-pipeline-events \
    --resource-group ai-platform-rg \
    --location eastus \
    --input-schema cloudeventschemav1_0

```

After creating the topic, you need credentials to publish events. You can retrieve the topic endpoint and access key using the Azure CLI:

```
az eventgrid topic show \
    --name ai-pipeline-events \
    --resource-group ai-platform-rg \
    --query "endpoint" \
    --output tsv

az eventgrid topic key list \
    --name ai-pipeline-events \
    --resource-group ai-platform-rg \
    --query "key1" \
    --output tsv

```

Event Grid supports three authentication methods: access key authentication (using the `aeg-sas-key` header), SAS token authentication, and Microsoft Entra ID. For production AI applications, [Microsoft Entra ID authentication](/en-us/azure/event-grid/authenticate-with-microsoft-entra-id) is the recommended approach. It eliminates the need to manage and rotate shared secrets, supports managed identities, and benefits from features such as Conditional Access policies. When your application runs on Azure services such as Azure Functions, Azure Container Apps, or Azure Kubernetes Service, you can assign a managed identity to the hosting service and grant it the **Event Grid Data Sender** role on the custom topic.

### Construct events for AI operations

Each custom event describes a meaningful state change in your AI system. A well\-constructed event includes enough context for the subscriber to start processing without embedding the full operation results. Subscribers retrieve detailed outputs from a data store using identifiers in the event data.

The following structure shows a CloudEvents event for an inference completion. The `type` field categorizes the operation, the `source` identifies the originating service, and the `subject` provides a filterable path. The `data` payload includes metadata about the operation and a reference to where the subscriber can find the detailed results:

```
{
    "specversion": "1.0",
    "type": "com.contoso.ai.InferenceCompleted",
    "source": "/services/content-moderation",
    "id": "evt-20250915-143000-001",
    "time": "2025-09-15T14:30:00Z",
    "subject": "/pipelines/moderation/image-classifier",
    "datacontenttype": "application/json",
    "data": {
        "requestId": "req-78901",
        "modelName": "content-classifier-v3",
        "modelVersion": "3.2.1",
        "processingDurationMs": 1250,
        "resultLocation": "https://results.blob.core.windows.net/output/req-78901.json",
        "status": "completed",
        "itemsProcessed": 1,
        "summary": {
            "classification": "safe",
            "confidence": 0.97
        }
    }
}

```

When designing the data payload, keep the following principles in mind:

* **Include identifiers for correlation:** The `requestId` or pipeline run ID lets subscribers trace the event back to the original request across distributed services.
* **Reference results instead of embedding them:** Store detailed outputs (inference results, embeddings, generated text) in Blob Storage or a database. Include the location in the event so subscribers can retrieve them when needed.
* **Add operational metadata:** Fields like `processingDurationMs` and `modelVersion` help monitoring services track performance trends and model usage without querying application logs.
* **Provide a summary for fast decisions:** Include a brief summary of the result so subscribers can make routing decisions (flag for review, proceed to next stage) without downloading the full output.

### Publish events using the Event Grid SDK

The `EventGridPublisherClient` from the `azure-eventgrid` library handles event serialization, authentication, and retries. You can authenticate with an access key using `AzureKeyCredential` or with Microsoft Entra ID using `DefaultAzureCredential`. The following example shows how to create a client and publish a CloudEvent to a custom topic:

```
## Code fragment - focus on creating and sending a CloudEvent
from azure.core.credentials import AzureKeyCredential
from azure.core.messaging import CloudEvent
from azure.eventgrid import EventGridPublisherClient

endpoint = os.environ["EVENTGRID_TOPIC_ENDPOINT"]
key = os.environ["EVENTGRID_TOPIC_KEY"]

credential = AzureKeyCredential(key)
client = EventGridPublisherClient(endpoint, credential)

event = CloudEvent(
    type="com.contoso.ai.InferenceCompleted",
    source="/services/content-moderation",
    data={
        "requestId": "req-78901",
        "modelName": "content-classifier-v3",
        "processingDurationMs": 1250,
        "resultLocation": "https://results.blob.core.windows.net/output/req-78901.json",
        "status": "completed"
    },
    subject="/pipelines/moderation/image-classifier"
)

client.send(event)

```

For production deployments, use `DefaultAzureCredential` to authenticate with a managed identity instead of access keys:

```
## Code fragment - focus on managed identity authentication
from azure.identity import DefaultAzureCredential
from azure.core.messaging import CloudEvent
from azure.eventgrid import EventGridPublisherClient

endpoint = os.environ["EVENTGRID_TOPIC_ENDPOINT"]

credential = DefaultAzureCredential()
client = EventGridPublisherClient(endpoint, credential)

```

You can publish events in batches for improved performance. When you publish a list of events, the SDK sends them in a single HTTP request. This approach reduces network overhead for AI applications that emit multiple events during a processing run, such as publishing stage\-transition events for each step in a pipeline:

```
## Code fragment - focus on batch publishing
events = [
    CloudEvent(
        type="com.contoso.ai.StageCompleted",
        source="/services/embeddings",
        data={"pipelineRunId": "run-42", "stage": "embeddings", "status": "completed"},
        subject="/pipelines/rag/run-42"
    ),
    CloudEvent(
        type="com.contoso.ai.StageCompleted",
        source="/services/indexing",
        data={"pipelineRunId": "run-42", "stage": "indexing", "status": "completed"},
        subject="/pipelines/rag/run-42"
    )
]

client.send(events)

```

Publish events at natural checkpoint boundaries in your AI workflow. Good publish points include after an inference completes, when a pipeline stage transitions, when an anomaly is detected, or when a model finishes validation. Don't publish events for internal state changes that no external subscriber needs to know about.

### Publish events using the REST API

You can also publish events by sending an HTTP POST request directly to the custom topic endpoint. This approach is useful when publishing from languages without an official Event Grid SDK, from lightweight services that don't need the full SDK dependency, or from non\-application systems such as CI/CD pipelines.

For a custom topic configured with the CloudEvents input schema, send a single CloudEvent as a JSON object with the `content-type` header set to `application/cloudevents+json; charset=utf-8`. Authenticate using the `aeg-sas-key` header:

```
curl -X POST \
    -H "Content-Type: application/cloudevents+json; charset=utf-8" \
    -H "aeg-sas-key: $EVENTGRID_TOPIC_KEY" \
    -d '{
        "specversion": "1.0",
        "type": "com.contoso.ai.ModelRetrained",
        "source": "/services/training",
        "id": "evt-20250915-160000-001",
        "time": "2025-09-15T16:00:00Z",
        "subject": "/models/sentiment-v2",
        "datacontenttype": "application/json",
        "data": {
            "modelName": "sentiment-v2",
            "modelVersion": "2.1.0",
            "accuracy": 0.94,
            "trainingDurationMinutes": 45,
            "artifactLocation": "https://models.blob.core.windows.net/trained/sentiment-v2.1.0.tar.gz"
        }
    }' \
    "$EVENTGRID_TOPIC_ENDPOINT"

```

The REST API returns 200 OK when the event is accepted for routing. A non\-200 response indicates an error in the request, such as a malformed event, an invalid key, or a schema mismatch.

### Apply event design patterns for AI applications

Different AI operations call for different event structures. The following patterns cover common scenarios in AI\-powered systems.

#### Inference completion events

Publish after each inference request completes. Include the request correlation ID, model name, processing duration, result location, and a summary status. Downstream subscribers can trigger notification workflows, update dashboards, or initiate follow\-up processing steps.

#### Model update events

Publish when a model is retrained, validated, or promoted to production. Include the model version, key training metrics, and the deployment target. Subscribers can refresh model caches in serving endpoints, update routing tables to direct traffic to the new model, or trigger integration tests against the updated version.

#### Pipeline stage transition events

Publish at each stage boundary in a multi\-step pipeline. Include the pipeline run ID, stage name, stage status, and input and output references. A monitoring service subscribes to these events to build a real\-time view of pipeline progress and detect bottlenecks. An orchestration service uses them to trigger the next stage when the previous one completes.

Each of these patterns follows the same core principle: the event describes what happened and provides enough context for subscribers to act. The event producer doesn't need to know who subscribes or what they do with the information. This decoupling is what makes event\-driven AI architectures extensible. Adding a new consumer is a matter of creating a new event subscription, not modifying the producer.

### Additional resources

* [Publish events to Azure Event Grid custom topics](/en-us/azure/event-grid/post-to-custom-topic)
* [Authenticate publishing clients using Microsoft Entra ID](/en-us/azure/event-grid/authenticate-with-microsoft-entra-id)
* [Azure Event Grid client library for Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/eventgrid/azure-eventgrid)

---

## Exercise \- Publish and receive events with Azure Event Grid

I content moderation systems generate a high volume of events as they classify and review submissions. Azure Event Grid provides the routing layer that directs these events to the right downstream consumers based on event type, so each handler receives only the events it needs without polling or manual filtering.

In this exercise, you deploy an Event Grid Namespace with a namespace topic and filtered event subscriptions, then build a Python Flask application that publishes content moderation events and receives them using pull delivery. Event Grid subscriptions route flagged content, approved content, and all events to separate subscriptions so you can observe how filtering works in practice. You also use the receive, acknowledge, and reject operations that pull delivery provides to control how your application processes events.

Tasks performed in this exercise:

* Download the project starter files
* Deploy an Event Grid Namespace with a namespace topic
* Create event subscriptions with type filters
* Add code to the starter files to complete the app
* Run the app to publish, receive, and process moderation events

This exercise takes approximately **30** minutes to complete.

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

In this module, you learned how Azure Event Grid enables event\-driven architectures for AI solutions by routing events from sources to handlers with low latency and high reliability. You explored the core Event Grid components, including topics, event subscriptions, and event handlers. You examined how these components work together to replace polling\-based coordination with reactive triggers. You also learned how to design events using the CloudEvents v1\.0 schema and define custom event types with reverse\-DNS naming conventions. You configured event subscriptions with type filters, subject filters, and advanced data attribute filters to route events to the right handlers. You examined how Event Grid handles delivery failures through exponential backoff retries and customizable retry policies with TTL and maximum attempt settings. You also configured dead\-letter destinations that capture undeliverable events for investigation. Finally, you learned how to publish custom events from AI applications using the Event Grid SDK and REST API. You constructed events that signal inference completions, model updates, and pipeline stage transitions so that downstream services can subscribe and react without modifying producers. These capabilities let you build AI systems that respond to state changes immediately, process events reliably, and scale by adding new event subscribers without modifying existing components.

### Additional resources

* [Azure Event Grid documentation](/en-us/azure/event-grid/)
* [CloudEvents v1\.0 schema with Azure Event Grid](/en-us/azure/event-grid/cloud-event-schema)
* [Event Grid message delivery and retry](/en-us/azure/event-grid/delivery-and-retry)
* [Publish events to Azure Event Grid custom topics](/en-us/azure/event-grid/post-to-custom-topic)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/_

## Fuentes
- [Develop event-driven AI workflows with Azure Event Grid](https://learn.microsoft.com/en-us/training/modules/event-driven-workflows-event-grid/?WT.mc_id=api_CatalogApi)
