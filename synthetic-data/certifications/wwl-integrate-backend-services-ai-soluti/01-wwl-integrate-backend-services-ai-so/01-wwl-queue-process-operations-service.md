# Queue and process AI operations with Azure Service Bus

> Curso: Integrate backend services for AI solutions (wwl-integrate-backend-services-ai-solutions) · Seccion: Integrate backend services for AI solutions
> Duracion estimada: 81 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

AI applications require asynchronous messaging to decouple request submission from inference processing and ensure reliable delivery under variable load. This module guides you through using Azure Service Bus to queue, distribute, and reliably process AI workloads on Azure.

Imagine you're a developer building a document analysis platform that uses large language models to extract structured data from uploaded contracts. Clients submit documents through a web API, and each document requires between five and 30 seconds of processing time depending on length and complexity. During peak hours, hundreds of documents arrive within minutes, but the inference service can only process a limited number concurrently. Without a buffer between the API and the processing layer, the API becomes unresponsive under load, clients receive timeout errors, and documents are lost when processing pods restart. Your team needs a messaging layer that absorbs traffic spikes, distributes work across multiple processors, and guarantees that every document is processed exactly once. Some downstream services also need to react to completed analyses, such as a notification service that alerts the submitter and an audit service that logs the result for compliance. The platform must handle processing failures gracefully, routing unprocessable documents to a separate queue for investigation rather than silently dropping them. Azure Service Bus provides the queuing, publish\-subscribe, and dead\-letter capabilities that this architecture requires.

After completing this module, you'll be able to:

* Explain how Azure Service Bus decouples AI application components and identify when to apply messaging patterns such as load leveling, competing consumers, and publish\-subscribe.
* Choose between Service Bus queues and topics with subscriptions based on whether an AI workflow requires single\-consumer processing or fan\-out to multiple consumers.
* Structure Service Bus messages for AI workloads, including serializing prompts and model parameters, handling large payloads with the claim\-check pattern, and including correlation IDs for end\-to\-end request tracking.
* Process messages reliably using peek\-lock receive mode, handle poison messages through dead\-letter queues, and monitor the dead\-letter queue for failed inferences.

Note

All code examples in this module are based on the most recent version of the `azure-servicebus` library at the time of writing. The library is updated often and the recommendation is to visit the [Azure Service Bus Python SDK documentation](/en-us/python/api/overview/azure/servicebus-readme) for the most up\-to\-date information.

---

## Explore Azure Service Bus concepts and messaging in AI architectures

Azure Service Bus is a fully managed enterprise message broker that provides queuing and publish\-subscribe capabilities for distributed applications. For AI backends, Service Bus acts as the connective layer between components that produce work (such as API endpoints accepting inference requests) and components that consume work (such as model processors running predictions). Understanding the core concepts and messaging patterns helps you design AI architectures that handle variable latency, traffic spikes, and processing failures without losing requests.

### What Azure Service Bus provides

Azure Service Bus delivers enterprise\-grade messaging through two primary entity types: queues for point\-to\-point delivery and topics with subscriptions for publish\-subscribe communication. Every Service Bus resource lives inside a namespace, which serves as the container for all messaging entities and provides a dedicated capacity allocation. The service uses the Advanced Message Queuing Protocol (AMQP) 1\.0 as its primary wire protocol, which provides reliable, binary\-level message transfer between clients and the broker. Service Bus also supports features such as message ordering, duplicate detection, and transactions that go beyond what basic queue services offer.

A Service Bus namespace acts as the application boundary for your messaging infrastructure. You can create multiple queues and topics within a single namespace, and each namespace provides its own connection endpoint in the form `<namespace-name>.servicebus.windows.net`. Authentication uses either shared access signatures (SAS) or Microsoft Entra ID with role\-based access control. For AI applications, Microsoft Entra ID with managed identity is the recommended approach because it eliminates the need to manage connection strings or rotate keys.

### Why AI architectures need messaging

AI inference operations have unpredictable latency that makes synchronous request\-response patterns fragile under load. A text summarization request might complete in two seconds, while a complex document extraction takes thirty. When a web API calls an inference service synchronously, clients must wait for the slowest operation to finish, and the API's thread pool fills with blocked requests during traffic spikes. This coupling between request rate and processing capacity means that a burst of incoming requests can exhaust compute resources, cause cascading timeouts, and ultimately drop client requests.

Messaging decouples the producer (the component that creates work) from the consumer (the component that processes work). The producer sends a message to a Service Bus queue and immediately returns an acknowledgment to the client. The consumer retrieves messages from the queue at its own pace, processes them, and writes results to a results store that the client can poll or receive through a callback. This separation lets each side scale independently. The API layer can accept thousands of requests per second, and the processing layer can work through them at whatever rate the model infrastructure supports.

### Core messaging patterns for AI workloads

Several messaging patterns address common challenges in AI architectures. Each pattern solves a specific problem that arises when you decouple request submission from processing.

#### Load leveling

The load leveling pattern uses a queue to absorb bursts of incoming requests, allowing processors to consume at a steady, sustainable rate. During a traffic spike, messages accumulate in the queue rather than overwhelming the processing layer. As the spike subsides, processors work through the backlog without any requests being dropped. This pattern eliminates the need to provision compute resources for peak traffic. Instead, you size your processing layer for average throughput and let the queue absorb the difference between peak arrival rate and processing capacity.

For AI workloads, load leveling is valuable because inference operations are compute\-intensive. Provisioning GPU or high\-memory instances for peak demand adds significant cost. A queue lets you maintain a smaller, steady\-state pool of processors that handles the workload over time rather than all at once.

#### Competing consumers

The competing consumers pattern places multiple worker instances as receivers on the same queue. Service Bus delivers each message to exactly one consumer, so all workers read from the same queue without processing the same message twice. This pattern provides horizontal scaling for processing\-intensive AI tasks. Each worker processes at its own maximum rate, and adding workers increases throughput without code changes. If one worker crashes, the remaining workers continue processing, and the failed worker's unacknowledged messages become available for redelivery.

This pattern is the foundation for scaling AI inference services. You can start with one worker and add more as queue depth increases. The workers can run on different compute services, such as Azure Container Apps, Azure Kubernetes Service (AKS), or Azure Functions, as long as each worker connects to the same queue.

#### Temporal decoupling

Temporal decoupling means that producers and consumers don't need to be online simultaneously. An API can enqueue inference requests even when all processors are offline for maintenance, a deployment update, or a scaling event. Messages persist durably in the queue (with triple\-redundant storage across availability zones in zone\-enabled namespaces) until processors come back online and consume them. This pattern is critical for AI platforms where model services might be restarted for deployments, where GPU instances cycle through scaling operations, or where a processing outage shouldn't result in lost customer requests.

### Manage backpressure with queue depth monitoring

When AI processing falls behind the rate of incoming requests, messages accumulate in the queue. Rather than treating this accumulation as a problem, you can use queue depth as a scaling signal. Azure Monitor provides metrics for active message count on each queue, and you can set alerts that trigger when the count exceeds thresholds. Azure Container Apps and Azure Functions support KEDA\-based scalers that automatically add processing instances based on Service Bus queue length. This creates a feedback loop where queue depth drives scaling decisions, ensuring that throughput increases proportionally with demand.

Monitoring queue depth also provides operational visibility into your AI pipeline's health. A consistently growing queue indicates that processing capacity isn't sufficient for the current request rate. A consistently empty queue might indicate over\-provisioning. The queue depth metric gives your operations team a single number that summarizes the relationship between input rate and processing capacity.

### Select the right Service Bus tier

Azure Service Bus offers Standard and Premium tiers, each with different capabilities and performance characteristics. Choosing the right tier for your AI workload depends on message size requirements, latency sensitivity, and security needs.

The Standard tier supports queues, topics, and subscriptions with shared broker capacity. It handles messages up to 256 KB in size and provides variable throughput based on load. For many AI workloads where payloads are small (such as JSON\-serialized prompts and parameters) and some latency variation is acceptable, the Standard tier provides a cost\-effective option.

The Premium tier provides dedicated resources, which means your messaging workload doesn't share compute with other tenants. It supports messages up to 100 MB when using the AMQP protocol (1 MB for HTTP), offers predictable latency, and includes features such as virtual network integration and private endpoints. AI workloads that send large payloads (such as base64\-encoded images or serialized embedding vectors) or require predictable submillisecond broker latency benefit from the Premium tier. The Premium tier also supports availability zones for higher reliability.

The Premium tier's larger message size limit (100 MB via AMQP versus 256 KB in Standard) can simplify architectures for AI scenarios that handle medium\-sized payloads like document text or small images, allowing you to send payloads directly rather than implementing the claim\-check pattern described in a later unit.

### Additional resources

* [What is Azure Service Bus?](/en-us/azure/service-bus-messaging/service-bus-messaging-overview)
* [Service Bus queues, topics, and subscriptions](/en-us/azure/service-bus-messaging/service-bus-queues-topics-subscriptions)
* [Service Bus Premium messaging tier](/en-us/azure/service-bus-messaging/service-bus-premium-messaging)

---

## Choose between queues and topics with subscriptions

When you design a messaging layer for an AI workflow, the first architectural decision is whether to use a Service Bus queue or a topic with subscriptions. This choice determines how messages flow through your system, how many consumers can act on each message, and how easily you can add new consumers in the future. The right entity type depends on whether each message needs single\-consumer processing or fan\-out to multiple independent consumers.

### Use queues for single\-consumer AI processing

A Service Bus queue delivers each message to exactly one competing consumer. When you have multiple worker instances reading from the same queue, Service Bus ensures that each message is processed by only one worker. This pattern suits AI workloads where a single processing step handles each request, such as an inference service that receives prompts, runs a model, and writes results to a database. You can scale processing horizontally by adding more workers without changing any code. Each worker independently connects to the queue, pulls messages, and processes them.

Queues support two receive modes that control how delivery acknowledgment works. In receive\-and\-delete mode, Service Bus removes the message from the queue immediately upon delivery. In peek\-lock mode (the default), Service Bus locks the message for a configurable duration and waits for the consumer to explicitly complete, abandon, or dead\-letter the message. Peek\-lock is the recommended mode for AI workloads because it provides at\-least\-once delivery. If a worker crashes during processing, the lock expires and Service Bus makes the message available for another worker to pick up.

Queues also support sessions, which enable first\-in\-first\-out (FIFO) processing guarantees and single\-receiver semantics per session group. For AI workloads that need to process related messages in order, such as a multi\-step document pipeline where extraction must precede classification, sessions allow you to group related messages using a session ID and ensure they're processed sequentially by a single consumer.

### Use topics and subscriptions for fan\-out AI workflows

A Service Bus topic accepts messages from senders and distributes copies to each attached subscription. Each subscription acts like an independent virtual queue with its own consumer. This pattern fits scenarios where multiple downstream services need to react to the same event independently. For example, when a document analysis completes, a notification subscription sends an alert to the user, an audit subscription logs the result for compliance, and a metrics subscription updates a processing dashboard. Each subscription processes its copy of the message independently, so a failure in one subscription doesn't affect the others.

Topics decouple the sender from the receivers. The sender publishes to a single topic without knowing how many subscriptions exist or what each subscriber does with the message. You can add new subscriptions at any time without modifying the producer's code. This extensibility is valuable in AI architectures that evolve over time. You might start with a single inference pipeline that writes results to a database, then later add a subscription for a quality\-assurance service that spot\-checks model outputs, and another subscription for a retraining pipeline that collects input\-output pairs for model improvement.

### Filter messages with subscription rules

Subscriptions support filter rules that select messages based on properties, allowing you to route messages selectively without writing filtering logic in each consumer. Service Bus evaluates filter rules at the broker level, so messages that don't match a subscription's filter are never delivered to that subscription's consumer. This reduces unnecessary message delivery and processing.

Three filter types are available. Boolean filters accept all messages (`TrueFilter`, the default) or reject all messages (`FalseFilter`). SQL filters use a SQL\-like expression syntax that evaluates against application properties and system properties of the message. Correlation filters match against specific property values and are more efficient than SQL filters for exact\-match scenarios.

For AI workloads, you can tag messages with application properties such as `model_name`, `priority`, or `document_type`, and each subscription receives only messages that match its filter. A high\-priority subscription can filter on `priority = 'high'` to route urgent inference requests to a dedicated processor with reserved GPU capacity. A subscription for a specific model version can filter on `model_name = 'gpt-4o'` to process only requests targeting that model.

```
## Code fragment - focus on creating a subscription rule with the management client
from azure.servicebus.management import ServiceBusAdministrationClient, SqlRuleFilter

admin_client = ServiceBusAdministrationClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    credential=credential
)

admin_client.create_rule(
    topic_name="inference-results",
    subscription_name="high-priority",
    rule_name="filter-high-priority",
    filter=SqlRuleFilter("priority = 'high'")
)

```

Note

Code examples in this module are patterns to adapt to your specific requirements. They illustrate the SDK's API surface and aren't intended for direct copy\-paste into production applications.

### Decide between queues and topics

The following decision framework helps you match the right entity type to common AI messaging scenarios.

You can use a **queue** when:

* **A single processing pipeline handles each request.** A document extraction service receives a prompt, runs a model, and writes results. Only one consumer needs to act on each message.
* **You need competing consumers for horizontal scaling.** Multiple workers pull from the same queue. Service Bus ensures each message reaches only one worker.
* **No other service needs the same message.** The message represents a task that's complete once a single consumer processes it.

You can use a **topic with subscriptions** when:

* **Multiple independent services need to react to the same message.** A completed inference result needs to trigger notifications, auditing, and dashboard updates simultaneously.
* **You need content\-based routing.** Different consumers should receive different subsets of messages based on properties like priority level, model name, or document type.
* **You want to add new consumers without modifying the producer.** New subscriptions can be created at any time, and the publisher's code doesn't change.

### Send messages with queue senders and topic senders

The Python `azure-servicebus` SDK uses the same `ServiceBusClient` class for both queues and topics. The difference is in how you create senders and receivers. You can call `get_queue_sender()` to send to a queue or `get_topic_sender()` to publish to a topic. On the receiving side, you can call `get_queue_receiver()` for queue consumers or `get_subscription_receiver()` for subscription consumers. This consistent API makes it straightforward to switch between patterns or use both patterns in the same application.

```
## Code fragment - focus on sending to a queue versus a topic
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

with ServiceBusClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    credential=credential
) as client:
    # Send to a queue (point-to-point)
    with client.get_queue_sender("inference-requests") as queue_sender:
        queue_sender.send_messages(
            ServiceBusMessage("queue message body")
        )

    # Send to a topic (publish-subscribe)
    with client.get_topic_sender("inference-results") as topic_sender:
        topic_sender.send_messages(
            ServiceBusMessage("topic message body")
        )

```

On the receiving side, a subscription receiver connects to a specific subscription on a topic. Each subscription maintains its own copy of the messages, so consuming from one subscription doesn't affect the message availability in other subscriptions.

```
## Code fragment - focus on receiving from a subscription
with client.get_subscription_receiver(
    topic_name="inference-results",
    subscription_name="notifications"
) as receiver:
    for msg in receiver:
        print(str(msg))
        receiver.complete_message(msg)

```

The `ServiceBusClient` uses context managers (`with` statements) to ensure connections are properly closed. You can also manage the client lifecycle manually by calling `client.close()`, but context managers are the recommended approach because they guarantee cleanup even when exceptions occur.

### Additional resources

* [Service Bus queues, topics, and subscriptions](/en-us/azure/service-bus-messaging/service-bus-queues-topics-subscriptions)
* [Topic filters and actions](/en-us/azure/service-bus-messaging/topic-filters)

---

## Structure messages for AI workloads

How you structure a Service Bus message determines how efficiently your AI pipeline processes requests, how effectively you can trace failures, and how well your system handles payloads of varying sizes. A well\-structured message carries all the information the processor needs, includes metadata for routing and tracking, and stays within the size limits of your Service Bus tier. This unit covers message anatomy, payload serialization, correlation tracking, large payload handling, TTL configuration, and batch sending.

### Understand message anatomy

A Service Bus message consists of three parts: the body, application properties, and system properties. The body carries the message payload, which is the primary data you want to transmit. Application properties are custom key\-value metadata that you define, useful for routing, filtering, and tracking. System properties are set by Service Bus or the SDK and include values such as `message_id`, `correlation_id`, `content_type`, `time_to_live`, `session_id`, and `sequence_number`.

For AI workloads, the body typically carries serialized inference request data, such as a JSON object containing a prompt, model parameters, and context documents. Application properties carry metadata that processors and subscriptions use for routing decisions and operational tracking, such as the model name, priority level, and document type. System properties provide delivery infrastructure like unique message identification and TTL enforcement.

### Serialize prompts and model parameters

The most common serialization format for AI workload messages is JSON, because it's human\-readable, widely supported across languages, and integrates naturally with REST APIs and model serving frameworks. You can structure the message body as a JSON payload containing the fields the processor needs: the prompt text, model name, temperature, maximum tokens, and any context documents or reference data.

Setting the `content_type` property to `application/json` signals clients and processors about the encoding format. The processor deserializes the body on receipt using standard JSON parsing and passes the extracted parameters to the model inference call.

```
## Code fragment - focus on creating a message with a JSON payload
import json
import uuid
from azure.servicebus import ServiceBusMessage

request_payload = {
    "prompt": "Extract the contract parties and effective date from this document.",
    "model": "gpt-4o",
    "temperature": 0.1,
    "max_tokens": 2000,
    "document_id": "doc-2025-0142"
}

message = ServiceBusMessage(
    body=json.dumps(request_payload),
    content_type="application/json",
    message_id=str(uuid.uuid4()),
    correlation_id="req-abc-12345",
    application_properties={
        "model_name": "gpt-4o",
        "priority": "standard",
        "document_type": "contract"
    }
)

```

Note

Code examples in this module are patterns to adapt to your specific requirements. They illustrate the SDK's API surface and aren't intended for direct copy\-paste into production applications.

The `message_id` uniquely identifies the message within Service Bus. If you enable duplicate detection on the queue, Service Bus uses this ID to discard duplicate submissions within the detection window. Always generate a unique `message_id` per message to avoid accidental deduplication of distinct requests.

### Track requests with correlation IDs

The `correlation_id` property provides end\-to\-end request tracking across your entire AI pipeline. You can set this property to a unique identifier that the client generates when it submits the original request, such as a UUID or a request ID from the API layer. This same ID follows the request from the API that enqueues it, through the processor that runs inference, into any downstream services that handle results, and back to the results store that the client polls.

When troubleshooting a failed inference, you can search logs, dead\-letter queues, and result stores by correlation ID to trace the full lifecycle of a request. This is especially valuable in AI systems where requests flow through multiple asynchronous stages and a failure at any stage can be difficult to correlate with the original request without a consistent tracking ID.

If your system uses distributed tracing with OpenTelemetry, you can propagate the trace context as application properties. This approach connects the message processing span to the originating request span in your tracing backend, providing a unified view of the request's journey across synchronous and asynchronous boundaries.

```
## Code fragment - focus on propagating trace context in application properties
from opentelemetry import trace

current_span = trace.get_current_span()
span_context = current_span.get_span_context()

message = ServiceBusMessage(
    body=json.dumps(request_payload),
    correlation_id=correlation_id,
    application_properties={
        "traceparent": f"00-{format(span_context.trace_id, '032x')}-{format(span_context.span_id, '016x')}-01",
        "model_name": "gpt-4o"
    }
)

```

### Handle large payloads with the claim\-check pattern

Service Bus Standard tier supports messages up to 256 KB, and Premium tier supports up to 100 MB. AI workloads sometimes need to send payloads that exceed these limits, such as full document text for summarization, images for classification, or large batches of embedding vectors. The claim\-check pattern addresses this constraint by separating the payload from the message.

With the claim\-check pattern, the producer uploads the large payload to Azure Blob Storage (or another durable store) and sends a Service Bus message that contains only the blob URI as a reference. The message body stays small, typically just a JSON object with the storage location and metadata. The processor retrieves the full payload from storage using the URI, processes it, and optionally deletes the blob after successful processing.

```
## Code fragment - focus on the claim-check pattern for large payloads
import json
from azure.storage.blob import BlobServiceClient
from azure.servicebus import ServiceBusMessage

## Producer: upload the large payload to Blob Storage
blob_service = BlobServiceClient(
    account_url="https://<storage-account>.blob.core.windows.net",
    credential=credential
)
container_client = blob_service.get_container_client("documents")
blob_client = container_client.get_blob_client("doc-2025-0142.pdf")
blob_client.upload_blob(large_document_bytes)

## Send a claim-check message with the blob URI
claim_check = {
    "blob_uri": f"https://<storage-account>.blob.core.windows.net/documents/doc-2025-0142.pdf",
    "document_id": "doc-2025-0142",
    "model": "gpt-4o",
    "operation": "extract"
}

message = ServiceBusMessage(
    body=json.dumps(claim_check),
    content_type="application/json",
    correlation_id="req-abc-12345",
    application_properties={"pattern": "claim-check"}
)

```

The claim\-check pattern offers several benefits beyond working within message size limits. It reduces broker throughput costs because the broker transfers only small reference messages rather than large payloads. It works within any tier's size limits, so you don't need to upgrade to Premium solely for large message sizes. It also lets you apply separate access controls to the message metadata and the actual payload, since Blob Storage access can be scoped independently from Service Bus access.

### Set message time\-to\-live

The `time_to_live` property defines how long a message remains in the queue before expiring. For time\-sensitive AI requests, such as real\-time classification where a stale result doesn't have value, you can set a shorter TTL so that the message disappears if the processor doesn't reach it in time. Expired messages can be routed to the dead\-letter queue when dead\-lettering on message expiration is enabled on the queue, providing visibility into messages that weren't processed in time.

```
## Code fragment - focus on setting time-to-live
from datetime import timedelta
from azure.servicebus import ServiceBusMessage

## Real-time classification: expire after five minutes
urgent_message = ServiceBusMessage(
    body=json.dumps(request_payload),
    time_to_live=timedelta(minutes=5)
)

## Batch processing: expire after 24 hours
batch_message = ServiceBusMessage(
    body=json.dumps(batch_payload),
    time_to_live=timedelta(hours=24)
)

```

For batch processing with relaxed latency requirements, set a longer TTL or omit the property to use the queue's default TTL. The appropriate TTL depends on how time\-sensitive the request is and how long the client is willing to wait for a result. Setting TTL values thoughtfully prevents stale requests from consuming processing resources while ensuring legitimate requests have enough time to be processed during load spikes.

### Batch messages for throughput

When you need to send multiple inference requests at once, use `ServiceBusMessageBatch` to group messages into a single send operation. Batching reduces the number of network round trips between your application and the Service Bus broker, which improves throughput when you're sending a large volume of messages. The SDK manages the batch size automatically, ensuring that the total batch doesn't exceed the maximum message size for your tier.

```
## Code fragment - focus on batch message sending
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import MessageSizeExceededError
import json

with client.get_queue_sender("inference-requests") as sender:
    batch = sender.create_message_batch()

    for request in pending_requests:
        message = ServiceBusMessage(
            body=json.dumps(request),
            content_type="application/json"
        )
        try:
            batch.add_message(message)
        except MessageSizeExceededError:
            # Batch is full, send the current batch and start a new one
            sender.send_messages(batch)
            batch = sender.create_message_batch()
            batch.add_message(message)

    # Send any remaining messages in the last batch
    if len(batch) > 0:
        sender.send_messages(batch)

```

The `add_message()` method raises a `MessageSizeExceededError` when the message would exceed the batch's size limit. The previous pattern handles this by sending the full batch and starting a new one. This approach ensures that all messages are sent even when the full list doesn't fit in a single batch. For AI workloads that generate many small inference requests in a short period, such as a document processing pipeline that splits a large document into page\-level requests, batching significantly reduces send latency.

### Additional resources

* [Service Bus messages, payloads, and serialization](/en-us/azure/service-bus-messaging/service-bus-messages-payloads)
* [Claim\-check pattern](/en-us/azure/architecture/patterns/claim-check)
* [Service Bus quotas](/en-us/azure/service-bus-messaging/service-bus-quotas)

---

## Process messages reliably

Reliable message processing ensures that your AI pipeline handles every inference request exactly as intended, even when processors crash, models return errors, or payloads contain unexpected data. Azure Service Bus provides receive modes, message settlement operations, dead\-letter queues, and lock management features that give developers fine\-grained control over delivery guarantees. This unit covers how to receive and process messages with the appropriate reliability level for AI workloads.

### Choose a receive mode

Service Bus offers two receive modes that control how the broker handles message delivery acknowledgment. The choice between them determines whether your system prioritizes throughput or delivery guarantees.

#### Receive\-and\-delete mode

In receive\-and\-delete mode, Service Bus removes the message from the queue immediately when it delivers the message to the consumer. If the processor crashes after receiving the message but before completing inference, the system loses the message. This mode provides the highest throughput because it eliminates the lock management and settlement round trip. It suits scenarios where occasional message loss is acceptable and processing speed is the priority, such as real\-time telemetry ingestion or noncritical logging where missing a few data points doesn't affect overall system correctness.

#### Peek\-lock mode

Peek\-lock mode is the default and the recommended mode for AI workloads. Service Bus locks the message for a configurable duration and delivers it to the consumer without removing it from the queue. The consumer must explicitly settle the message (complete, abandon, dead\-letter, or defer) within the lock duration. If the lock expires before settlement, Service Bus releases the lock and makes the message available for another consumer to receive. This two\-phase approach provides at\-least\-once delivery, which is essential for AI workloads where losing an inference request is unacceptable.

The trade\-off with peek\-lock is slightly lower throughput compared to receive\-and\-delete, because each message requires a settlement call. For most AI workloads, this overhead is negligible compared to the time spent on inference processing, and the delivery guarantee far outweighs the minor throughput difference.

### Settle messages after processing

After receiving a message in peek\-lock mode, the processor calls one of four settlement operations to report the processing outcome to Service Bus. Each operation signals a different outcome and instructs the broker to handle the message accordingly.

#### Complete a message

The `complete_message()` method marks the message as successfully processed and removes it from the queue permanently. You can call this method after the processor finishes inference and writes the result to the results store. Completing a message is the normal success path in the processing loop.

#### Abandon a message

The `abandon_message()` method releases the lock without removing the message from the queue, making it immediately available for redelivery. You can use this method when the processor encounters a transient error that might succeed on a retry, such as a model service timeout or a temporary network failure. Service Bus increments the message's delivery count each time it's abandoned, so the message eventually moves to the dead\-letter queue if transient errors persist beyond the maximum delivery count.

#### Dead\-letter a message

The `dead_letter_message()` method moves the message to the dead\-letter subqueue with a reason string and an error description. You can use this method when the processor can never successfully handle the message, such as when it contains a malformed JSON payload, references an unsupported model, or fails validation checks that won't pass on retry. Dead\-lettering immediately removes the message from normal processing and preserves it for investigation without consuming further retry attempts.

#### Defer a message

The `defer_message()` method keeps the message in the queue but removes it from regular delivery. You can only retrieve the message later by its sequence number using `receive_deferred_messages()`. This suits scenarios where the processor can't handle the message right now but expects to handle it later, such as when a required dependency isn't available yet or when messages need processing in a specific order but arrive out of sequence.

The following example shows the peek\-lock receive pattern with complete and dead\-letter settlements in an AI processing loop.

```
## Code fragment - focus on peek-lock receive with settlement
import json
from azure.servicebus import ServiceBusClient, ServiceBusReceiveMode
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

with ServiceBusClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    credential=credential
) as client:
    with client.get_queue_receiver(
        queue_name="inference-requests",
        receive_mode=ServiceBusReceiveMode.PEEK_LOCK,
        max_wait_time=30
    ) as receiver:
        for msg in receiver:
            try:
                payload = json.loads(str(msg))
                result = run_inference(payload)
                save_result(result, payload.get("document_id"))
                receiver.complete_message(msg)
            except json.JSONDecodeError:
                receiver.dead_letter_message(
                    msg,
                    reason="MalformedPayload",
                    error_description="Message body is not valid JSON"
                )
            except ModelNotFoundError:
                receiver.dead_letter_message(
                    msg,
                    reason="UnsupportedModel",
                    error_description=f"Model {payload.get('model')} is not available"
                )
            except TransientServiceError:
                receiver.abandon_message(msg)

```

Note

Code examples in this module are patterns to adapt to your specific requirements. They illustrate the SDK's API surface and aren't intended for direct copy\-paste into production applications.

### Handle poison messages with max delivery count

Service Bus tracks how many times it delivers each message. When the delivery count exceeds the queue's `max_delivery_count` (the default is 10\), Service Bus automatically moves the message to the dead\-letter queue with the reason `MaxDeliveryCountExceeded`. This mechanism prevents a consistently failing message from blocking the queue indefinitely. Without max delivery count, a message that always causes an error would cycle through delivery and abandonment in an infinite loop, consuming processing resources without making progress.

For AI workloads, you can adjust `max_delivery_count` based on your retry strategy. A lower count (such as three to five) moves poison messages to the dead\-letter queue faster, freeing processing capacity for healthy messages. A higher count gives transient errors more opportunities to resolve, which is useful when model services experience intermittent availability issues. Consider the nature of the errors your pipeline encounters: if failures are typically transient (network timeouts, temporary resource constraints), a higher count provides better recovery. If failures are typically permanent (malformed data, unsupported parameters), a lower count reduces wasted processing.

### Monitor and process the dead\-letter queue

The dead\-letter queue (DLQ) is a subqueue attached to every queue and subscription. It holds messages that expire, exceed the max delivery count, or that application code explicitly dead\-letters. The DLQ exists automatically, and you don't need to create or manage it separately. Messages in the DLQ persist until you explicitly receive and complete them.

Each dead\-lettered message carries `dead_letter_reason` and `dead_letter_error_description` properties that explain why Service Bus moved it. For messages that exceed the max delivery count, the reason is `MaxDeliveryCountExceeded`. For messages that application code dead\-letters, the reason and description are whatever strings you pass to `dead_letter_message()`. These properties provide the diagnostic context needed to understand systemic issues in your AI pipeline.

Monitoring the DLQ is critical for AI applications because it reveals patterns of failure. A sudden increase in dead\-lettered messages might indicate that a model deployment isn't working, that the processor doesn't handle a new input format, or that an upstream service is sending malformed requests. You can set Azure Monitor alerts on the dead\-letter message count metric to detect these issues early.

```
## Code fragment - focus on receiving and inspecting dead-letter messages
from azure.servicebus import ServiceBusClient, ServiceBusSubQueue
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

with ServiceBusClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    credential=credential
) as client:
    with client.get_queue_receiver(
        queue_name="inference-requests",
        sub_queue=ServiceBusSubQueue.DEAD_LETTER,
        max_wait_time=10
    ) as dlq_receiver:
        for msg in dlq_receiver:
            print(f"Dead-letter reason: {msg.dead_letter_reason}")
            print(f"Error description: {msg.dead_letter_error_description}")
            print(f"Correlation ID: {msg.correlation_id}")
            print(f"Delivery count: {msg.delivery_count}")
            print(f"Body: {str(msg)}")
            # Inspect and decide whether to resubmit or discard
            dlq_receiver.complete_message(msg)

```

You access the DLQ using the `sub_queue=ServiceBusSubQueue.DEAD_LETTER` parameter on the receiver. Use this approach instead of constructing the path manually (such as `<queue_name>/$deadletterqueue`), because the SDK handles the path formatting internally from the `ServiceBusSubQueue` enum.

### Reprocess dead\-lettered messages

After fixing the root cause of failures, such as updating the model, correcting input validation, or expanding payload handling, you can resubmit dead\-lettered messages to the original queue. The reprocessing pattern involves reading each message from the DLQ, creating a new message with the same body and properties, sending the new message to the original queue, and completing the dead\-letter message to remove it from the DLQ.

```
## Code fragment - focus on resubmitting dead-lettered messages
with client.get_queue_receiver(
    queue_name="inference-requests",
    sub_queue=ServiceBusSubQueue.DEAD_LETTER,
    max_wait_time=10
) as dlq_receiver:
    with client.get_queue_sender("inference-requests") as sender:
        for msg in dlq_receiver:
            # Create a new message with the original body and properties
            new_message = ServiceBusMessage(
                body=msg.body,
                content_type=msg.content_type,
                correlation_id=msg.correlation_id,
                application_properties=msg.application_properties
            )
            sender.send_messages(new_message)
            dlq_receiver.complete_message(msg)

```

Automated reprocessing scripts can handle bulk resubmission when a systemic fix resolves multiple failures at once. Before resubmitting, confirm that your fix genuinely resolves the root cause. Otherwise, the messages cycle back through processing and land in the DLQ again, wasting resources and obscuring the real failure count.

### Manage lock duration for long\-running AI operations

Some AI operations, such as processing a long document or running a complex model pipeline, take longer than the default lock duration. Service Bus queue lock duration is configurable up to a maximum of five minutes, with a default of one minute. If the lock expires before the processor settles the message, Service Bus makes the message available for another consumer, which leads to duplicate processing.

For operations that might exceed the lock duration, you have two options. You can extend the lock by calling `receiver.renew_message_lock()` periodically during processing. Alternatively, you can use the `AutoLockRenewer` class, which automatically renews the lock in the background until the specified maximum renewal duration elapses. The `AutoLockRenewer` is the simpler option for long\-running AI operations because it handles the renewal timing without requiring manual calls in your processing loop.

```
## Code fragment - focus on automatic lock renewal for long-running processing
from azure.servicebus import ServiceBusClient, AutoLockRenewer
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

with ServiceBusClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    credential=credential
) as client:
    renewer = AutoLockRenewer()
    with client.get_queue_receiver(
        queue_name="inference-requests",
        max_wait_time=30
    ) as receiver:
        for msg in receiver.receive_messages():
            # Renew the lock for up to 10 minutes
            renewer.register(receiver, msg, max_lock_renewal_duration=600)
            result = run_long_inference(msg)
            receiver.complete_message(msg)
    renewer.close()

```

For long operations that consistently exceed even the extended renewal period, consider a two\-phase processing approach. In the first phase, the processor receives the message, records the request in a tracking store, and completes the message quickly. In the second phase, a separate process picks up work from the tracking store and performs the long\-running inference. This approach avoids lock management entirely for the long\-running portion and uses the queue solely for reliable initial delivery.

### Additional resources

* [Settling receive operations](/en-us/azure/service-bus-messaging/message-transfers-locks-settlement#settling-receive-operations)
* [Overview of Service Bus dead\-letter queues](/en-us/azure/service-bus-messaging/service-bus-dead-letter-queues)
* [Service Bus message sessions](/en-us/azure/service-bus-messaging/message-sessions)

---

## Exercise \- Process messages with Azure Service Bus

AI workflows often rely on messaging to decouple request intake from model inference and to route results to multiple downstream consumers. Azure Service Bus provides the reliability and routing layer that connects these components so each piece can scale and fail independently.

In this exercise, you create an Azure Service Bus namespace and build a Python Flask web application that demonstrates core messaging patterns using an AI inference scenario. You work with queues to send and receive inference requests using peek\-lock delivery, inspect the dead\-letter queue for malformed payloads that failed processing, and use topics with filtered subscriptions to fan out inference results by priority level.

Tasks performed in this exercise:

* Download the project starter files
* Create an Azure Service Bus namespace
* Create messaging entities using the Azure CLI
* Add code to the starter files to complete the app
* Run the app to perform messaging operations

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

In this module, you learned how Azure Service Bus provides enterprise\-grade messaging capabilities that decouple AI application components and ensure reliable delivery of inference requests. You explored the core concepts of namespaces, queues, and topics with subscriptions. You also explored how messaging patterns like load leveling, competing consumers, and temporal decoupling address common AI architecture challenges such as variable inference latency and traffic spikes. You learned how to choose between queues for single\-consumer processing and topics with subscriptions for fan\-out workflows where multiple services react to the same event. You examined how to structure messages for AI workloads by serializing prompts and model parameters as JSON payloads. You also learned how to include correlation IDs for end\-to\-end request tracking and apply the claim\-check pattern when payloads exceed message size limits. Finally, you learned how to process messages reliably using peek\-lock receive mode and settle messages with complete, abandon, and dead\-letter operations. You also explored how to handle poison messages through max delivery count and monitor the dead\-letter queue to detect systemic processing failures.

### Additional resources

* [Azure Service Bus documentation](/en-us/azure/service-bus-messaging/)
* [Azure Service Bus Python SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/servicebus/azure-servicebus/samples)
* [Service Bus best practices for performance improvements](/en-us/azure/service-bus-messaging/service-bus-performance-improvements)
* [Claim\-check pattern](/en-us/azure/architecture/patterns/claim-check)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/_

## Fuentes
- [Queue and process AI operations with Azure Service Bus](https://learn.microsoft.com/en-us/training/modules/queue-process-operations-service-bus/?WT.mc_id=api_CatalogApi)
