# Build serverless AI backends with Azure Functions

> Curso: Integrate backend services for AI solutions (wwl-integrate-backend-services-ai-solutions) · Seccion: Integrate backend services for AI solutions
> Duracion estimada: 98 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

AI solutions require lightweight, event\-driven compute to handle tasks such as serving inference requests, processing data pipelines, and integrating with external services. This module guides you through building serverless AI backends with Azure Functions to create responsive, cost\-efficient, and secure endpoints that scale automatically with demand.

Imagine you're a developer at a company building an intelligent document processing pipeline. The system receives documents through an API, extracts text using an Azure AI service, classifies the content, and stores the results in a database. The current architecture runs on dedicated virtual machines that sit idle most of the day but struggle to keep up during peak upload windows. Operational costs are climbing because the VMs run around the clock, and the team spends significant effort maintaining the infrastructure. Your manager asks you to move the processing logic to a serverless architecture that scales with actual demand and charges only for execution time. You need an HTTP endpoint that accepts document uploads, a queue\-based processor that handles classification asynchronously, and output bindings that write results to storage. Each component must securely access Azure AI services and databases without embedding credentials in code. The client expects the new system to handle bursts of several hundred concurrent requests while keeping average response latency under 500 milliseconds. You choose Azure Functions because it provides event\-driven triggers, built\-in bindings to Azure services, and flexible hosting plans that let you balance cold start latency against cost. Building this solution requires understanding how Functions scales, how to develop and debug locally, and how to properly manage secrets and identity.

After completing this module, you'll be able to:

* Evaluate cold start, scaling, and instance memory trade\-offs when choosing between Flex Consumption and Premium hosting for AI workloads.
* Set up a local development environment for Azure Functions using Core Tools, emulators, and an IDE.
* Create triggers and bindings that implement common AI integration patterns such as HTTP inference endpoints and queue\-based batch processors.
* Configure secrets management and application settings using Key Vault references and Azure App Configuration.
* Apply managed identity and function\-level authorization to secure access between Functions and other Azure resources.

Note

All code examples in this module are based on the most recent version of the Azure Functions libraries at the time of writing. The libraries are updated often and the recommendation is to visit the [Azure Functions Python developer guide](/en-us/azure/azure-functions/functions-reference-python) for the most up\-to\-date information.

---

## Understand Azure Functions hosting and scaling for AI workloads

The hosting plan you choose for your Azure Functions app determines how instances start, how the app scales under load, and how much memory each instance provides. These decisions directly affect the latency, throughput, and cost of an AI backend. This unit focuses on the two hosting plans most relevant to serverless AI workloads, the Flex Consumption plan and the Premium plan, and explains how to configure scaling and handle long\-running tasks.

### Understand cold start and why it matters for AI

Cold start is the delay that occurs when the Azure Functions platform allocates a new instance, loads the runtime, and initializes your application's dependencies before the instance can handle its first request. Every serverless hosting plan that scales to zero experiences cold start because no preallocated compute exists to serve the initial invocation. Understanding cold start behavior helps you make informed hosting decisions for latency\-sensitive AI endpoints.

AI workloads tend to amplify cold start latency beyond what simpler applications experience. Large dependency graphs from machine learning libraries and SDK packages increase the time the platform spends loading modules into memory. Model configuration loading, connection warm up to downstream services like Azure AI Services or databases, and initialization of HTTP clients all add seconds of latency on top of the base platform delay. For example, a Python function that imports `azure-ai-documentintelligence` and `azure-cosmos` adds measurably more startup time than a function with minimal dependencies.

Cold start is a per\-instance event. It affects only the first request routed to a new instance, not every request. Once an instance is warm, subsequent requests execute without the startup overhead. This distinction matters for AI workloads because consistent traffic to warm instances delivers predictable low latency, while bursty traffic that triggers new instance creation introduces intermittent delays.

### Choose between Flex Consumption and Premium

Azure Functions offers several hosting plans, but two stand out for serverless AI backends: the Flex Consumption plan and the Premium plan. Each takes a different approach to managing cold starts and scaling, and the right choice depends on your workload's traffic patterns and latency requirements.

The **Flex Consumption plan** is the recommended default for new serverless function apps. It's a Linux\-only plan that provides per\-function scaling, configurable instance memory sizes (512 MB, 2,048 MB, or 4,096 MB), virtual network integration, and always\-ready instances. Flex Consumption scales up to 1,000 instances and charges based on active execution time plus any always\-ready baseline. The always\-ready feature lets you keep a minimum number of warm instances for latency\-sensitive functions while other functions in the same app remain fully serverless and scale to zero. This approach gives you fine\-grained control over the trade\-off between cold start mitigation and cost, because you pay only for the always\-ready instances you configure.

The **Premium plan** eliminates cold starts entirely by keeping at least one pre\-warmed worker always running. Premium provides event\-driven scaling with pre\-warmed instances, custom Linux image support, and virtual network connectivity. Choose Premium when your functions run continuously or nearly continuously and the always\-on cost is justified, when you need larger compute sizes than Flex Consumption offers, or when you need to deploy functions using custom container images.

The following list summarizes when to consider other hosting options beyond these two plans:

* **Dedicated (App Service) plan:** Makes sense when underutilized App Service capacity already exists and you want to run functions on those instances without additional cost.
* **Container Apps hosting:** Appropriate when functions need GPU access for model inference, custom OS\-level packages, or need to run alongside other containerized microservices in the same environment.
* **Consumption plan (Linux):** The legacy serverless plan. The ability to run function apps on Linux in a Consumption plan retires after September 2028\. New projects should use the Flex Consumption plan instead.

### Configure scaling and concurrency

The Flex Consumption plan introduces per\-function scaling, which provides more deterministic resource allocation than plans that scale the entire function app as a single unit. Understanding how scaling works helps you tune throughput and cost for AI backends that handle multiple trigger types.

In per\-function scaling, each trigger type scales independently based on its own event\-driven demand. All HTTP triggers in a function app scale together as a group on the same instances because HTTP traffic typically shares similar resource requirements. All other trigger types, such as queue triggers, Service Bus triggers, and timer triggers, each scale on their own independent set of instances. This separation means a surge in queue processing doesn't compete with HTTP request handling for compute resources.

Concurrency settings control the maximum number of parallel executions that each instance handles simultaneously. Lower concurrency values spread load across more instances, which isolates resource consumption per invocation. Higher concurrency values use fewer instances but require more memory per instance to handle multiple executions in parallel. For AI workloads that perform CPU\-intensive or memory\-intensive inference, lower concurrency often produces more predictable performance because each invocation has more dedicated resources.

Instance memory selection determines the compute resources available to each instance. The 2,048\-MB instance size is the default and suits most scenarios. Use the 4,096\-MB size when functions load large models, process memory\-intensive data, or require higher CPU allocation, because CPU cores scale proportionally with memory (2,048 MB provides one vCPU, 4,096 MB provides two vCPU). The 512\-MB tier suits lightweight, high\-volume event processors that don't require significant memory or CPU per invocation.

### Handle long\-running AI tasks

HTTP\-triggered functions face a 230\-second timeout imposed by the Azure Load Balancer, regardless of the hosting plan or the `functionTimeout` setting in `host.json`. AI inference, document processing, and model training tasks that exceed this limit cause a timeout error for the caller even though the function might still be executing on the backend. Planning for this constraint is essential when building AI backends that process complex or batch workloads.

The recommended approach uses the async request\-reply pattern. The HTTP\-triggered function accepts the incoming request, validates the input, writes a message to a Service Bus queue, and immediately returns a `202 Accepted` response with a status endpoint URL. A separate Service Bus\-triggered function picks up the message and performs the long\-running processing without any HTTP timeout constraint, because Service Bus\-triggered functions can run for an unbounded duration on the Flex Consumption and Premium plans.

```
## Code fragment - focus on async request-reply pattern
import azure.functions as func
import json
import uuid

app = func.FunctionApp()

@app.route(route="process-document", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
@app.service_bus_queue_output(arg_name="queue_msg", queue_name="document-jobs", connection="ServiceBusConnection")
def accept_document(req: func.HttpRequest, queue_msg: func.Out[str]) -> func.HttpResponse:
    job_id = str(uuid.uuid4())
    document_url = req.get_json().get("document_url")

    queue_msg.set(json.dumps({"job_id": job_id, "document_url": document_url}))

    return func.HttpResponse(
        json.dumps({"job_id": job_id, "status_url": f"/api/job-status/{job_id}"}),
        status_code=202,
        mimetype="application/json"
    )

```

This pattern also decouples ingestion throughput from processing throughput. The HTTP endpoint can accept hundreds of requests per second, while the Service Bus\-triggered processor scales independently based on queue depth. Each component scales to its own optimal instance count without affecting the other.

### Additional resources

* [Azure Functions Flex Consumption plan](/en-us/azure/azure-functions/flex-consumption-plan)
* [Azure Functions hosting options](/en-us/azure/azure-functions/functions-scale)
* [Improve Azure Functions performance and reliability](/en-us/azure/azure-functions/performance-reliability)

---

## Set up the local development environment for Functions

A productive local development workflow lets you build and test Azure Functions on your own machine before deploying to Azure. Local development eliminates the need to provision cloud resources during the early stages of development, reduces the feedback loop between writing code and seeing results, and helps you catch configuration issues before they reach production. This unit walks through setting up Visual Studio Code with the Azure Functions extension, understanding the project structure, configuring emulators for dependent services, and debugging functions locally.

### Install Azure Functions Core Tools

The [Azure Functions extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) provides an integrated development experience for creating, testing, and deploying functions. The extension depends on Azure Functions Core Tools, which provides the local version of the Azure Functions runtime. Core Tools includes the same trigger and binding processing logic that runs in Azure, so functions behave consistently between local and cloud environments.

You can install Core Tools through several package managers depending on your operating system. On macOS, use Homebrew with `brew tap azure/functions && brew install azure-functions-core-tools@4`. On Linux, use the appropriate package manager for your distribution. On Windows, use winget with `winget install Microsoft.Azure.FunctionsCoreTools`. After installation, verify the setup by running `func --version` in your terminal.

You can create a new Functions project in Visual Studio Code by running the **Azure Functions: Create Function...** command from the Command Palette. This command walks you through selecting a project folder, language runtime, and trigger template. It scaffolds the project structure, creates a starter function, and generates the `.vscode/launch.json`, `.vscode/tasks.json`, and `.vscode/extensions.json` files that enable integrated debugging and task running. Starting the local runtime with `func start` or by pressing F5 launches the Functions host and exposes HTTP endpoints at `http://localhost:7071` by default.

Note

You can also create projects from the command line with `func init` and `func new`. The command `func init my-ai-backend --python` scaffolds the project structure, and `func new --name classify --template "HTTP trigger"` adds a function. However, these commands don't generate the `.vscode` configuration files, so you need to create them manually or run **Azure Functions: Create Function...** afterward.

### Understand local project structure

Azure Functions projects follow a specific directory layout that the runtime uses to discover functions, load configuration, and manage dependencies. Understanding this structure helps you organize your code, troubleshoot startup issues, and configure deployments correctly.

The Python v2 programming model uses a single entry point file, typically `function_app.py`, where you define functions and their triggers using decorators. This approach consolidates function definitions in one place rather than spreading them across multiple directories with individual `function.json` files.

A single `function_app.py` file works well for projects with a handful of functions, such as an HTTP trigger for inference and a queue trigger for batch processing. As the number of functions grows, you can split definitions into separate files using [blueprints](/en-us/azure/azure-functions/functions-reference-python#blueprints). Blueprints let you define functions in individual modules and register them with the main `function_app.py` entry point, which keeps each file focused and easier to maintain.

The `host.json` file contains global runtime configuration that applies to all functions in the app. Settings in this file control behavior such as function timeout duration, logging levels, extension bundle versions, and concurrency limits for specific trigger types. Changes to `host.json` affect every function in the app, so treat it as shared infrastructure configuration.

The `local.settings.json` file stores application settings and connection strings for local development. The runtime reads values from the `Values` object in this file and exposes them as environment variables to your function code. This file is excluded from source control by the default `.gitignore` because it typically contains connection strings and other sensitive values. Never commit `local.settings.json` to a repository.

The `.vscode` folder contains Visual Studio Code configuration files generated by the Azure Functions extension. The `launch.json` file configures the debugger to attach to the Core Tools process, `tasks.json` defines the build and host start tasks, and `extensions.json` recommends the Azure Functions extension to other developers who open the project. These files enable F5 debugging and should be committed to source control so the team shares a consistent development experience.

Dependency management files, such as `requirements.txt` for Python or `package.json` for Node.js, list the packages your functions need. The runtime installs these dependencies during deployment or when you run `pip install -r requirements.txt` locally. The `.funcignore` file specifies files and folders to exclude from deployment packages, keeping your deployed artifact lean by omitting test files, documentation, and other development\-only resources.

### Use Azurite for the Functions runtime storage dependency

The Azure Functions runtime requires a storage account connection (configured through the `AzureWebJobsStorage` setting) to manage internal operations such as coordinating trigger processing across instances, tracking timer trigger state, and storing function access keys. This dependency exists regardless of whether your application code uses Azure Storage directly. Without a valid storage connection, non\-HTTP triggers such as queue triggers and timer triggers don't work.

For local development, you can route the runtime's storage dependency to the [Azurite emulator](/en-us/azure/storage/common/storage-use-azurite) by setting `AzureWebJobsStorage` to `UseDevelopmentStorage=true` in `local.settings.json`. Azurite provides local implementations of Azure Blob Storage, Queue Storage, and Table Storage that behave like the cloud service. This approach eliminates the need to create an Azure Storage account for development purposes.

The simplest way to run Azurite is through the [Azurite Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=Azurite.azurite), which starts the emulator automatically when you launch a debugging session. You can also install Azurite globally through npm with `npm install -g azurite` and start it from the command line with `azurite --silent`. The following configuration in `local.settings.json` connects the runtime to Azurite:

```
{
    "IsEncrypted": false,
    "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python"
    }
}

```

When you deploy a function app to Azure, the platform creates or requires a linked storage account automatically. The `UseDevelopmentStorage=true` setting applies only to local development and has no effect in the cloud.

### Use emulators and local services for connected resources

Beyond the runtime storage dependency, AI backends typically connect to databases, caches, and other services for application\-level data operations. Several emulators and local alternatives help you test these connections without provisioning cloud resources, keeping your development workflow fast and cost\-free during the build phase.

The [Azure Cosmos DB emulator](/en-us/azure/cosmos-db/emulator) runs locally on Windows, Linux, and macOS (through Docker). It supports the NoSQL API and provides a local endpoint that behaves like the cloud service. You can use the emulator's connection string in `local.settings.json` and switch to the production endpoint when deploying. This approach works well for AI applications that store inference results, session state, or vector embeddings in Cosmos DB.

Azure Database for PostgreSQL doesn't have an Azure\-specific emulator, but PostgreSQL is open source. You can run a local instance through Docker with `docker run -e POSTGRES_PASSWORD=mysecret -p 5432:5432 postgres` or install PostgreSQL natively. Your function code connects identically to a local instance and the Azure\-managed service, because both use the same PostgreSQL wire protocol.

Azure Managed Redis doesn't have an Azure\-specific emulator either, but Redis is open source. You can run a local instance through Docker with `docker run -p 6379:6379 redis` or install Redis natively. For AI backends that use Redis for caching inference results or managing rate limiting, local Redis provides a functional development target.

You can configure connection strings for all local services in the `Values` section of `local.settings.json`. When deploying to Azure, swap these values to production connection strings or identity\-based connections. This separation between local and production configuration keeps your development environment isolated from cloud resources.

### Debug locally with Visual Studio Code

The Azure Functions extension for Visual Studio Code provides integrated debugging that lets you set breakpoints, inspect variables, and step through trigger execution in your functions. Debugging locally gives you the same visibility into function behavior that you'd have with any other application, which is essential for troubleshooting AI pipeline logic and data transformation issues.

You can configure launch settings in the `.vscode/launch.json` file to attach the debugger to the Core Tools process. When you press F5, Visual Studio Code starts Core Tools, attaches the debugger, and opens the terminal showing the function endpoints. You can set breakpoints in your function code and step through execution when a trigger fires.

For testing HTTP triggers, you can use `.http` files directly in Visual Studio Code with the REST Client extension, or tools like `curl` from the command line. The following example shows how to test an HTTP trigger locally:

```
curl -X POST http://localhost:7071/api/classify \
    -H "Content-Type: application/json" \
    -d '{"document_url": "https://storage.example.com/docs/sample.pdf"}'

```

You can also test Service Bus triggers locally by configuring a Service Bus connection string in `local.settings.json` and sending messages through the Azure portal's Service Bus Explorer or the Azure CLI with `az servicebus queue message send`. Timer triggers fire automatically based on their CRON schedule when Core Tools runs.

### Synchronize settings between local and Azure

Keeping local development settings aligned with your Azure function app's configuration prevents environment\-specific bugs and simplifies the transition from development to production. The Azure Functions extension and Core Tools both provide ways to synchronize settings between your local environment and Azure.

In Visual Studio Code, you can right\-click your function app in the Azure Resources panel and select **Download Remote Settings** to pull production app settings into your local `local.settings.json` file. You can also select **Upload Local Settings** to push local values to Azure. These commands provide a quick way to keep environments aligned without leaving the editor.

The equivalent CLI commands are `func azure functionapp fetch-app-settings <app-name>` to download settings and `func azure functionapp publish <app-name>` to deploy code along with local settings. You can encrypt the local settings file with `func settings encrypt` to protect any secrets stored on your development machine. The encrypted file can only be decrypted by Core Tools on the same machine.

Be mindful of which settings you push to Azure, because overwriting production settings with local development values can break your deployed application. A common practice is to manage production settings through Azure CLI (`az functionapp config appsettings set`) or infrastructure\-as\-code templates, and reserve `local.settings.json` for development\-only values.

### Additional resources

* [Azure Functions Core Tools reference](/en-us/azure/azure-functions/functions-run-local)
* [Code and test Azure Functions locally](/en-us/azure/azure-functions/functions-develop-local)
* [Use the Azurite emulator for local Azure Storage development](/en-us/azure/storage/common/storage-use-azurite)

---

## Create triggers and bindings for AI integration patterns

Azure Functions triggers and bindings provide a declarative way to connect functions to external services without writing boilerplate connection and serialization code. Triggers determine how a function is invoked, while bindings move data into and out of functions through configuration rather than explicit SDK calls. For AI backends, triggers and bindings simplify the integration between inference endpoints, message queues, storage services, and databases. This unit covers how to create HTTP triggers for inference endpoints, queue triggers for batch processing, and output bindings for storing results.

### Understand triggers and bindings

A trigger defines how a function starts executing. Every function has exactly one trigger, and the trigger type determines the event source that invokes the function. Common triggers include HTTP requests, queue messages, timer schedules, and database change feeds. The trigger also serves as an input binding, providing the event data to your function code as a parameter.

Bindings connect a function to other services through input bindings (data flowing into the function) and output bindings (data flowing out). Bindings are optional, and a function can have zero or multiple bindings of either type. The runtime handles authentication to the target service and data serialization, so your code focuses on business logic rather than connection management.

The combination of triggers and bindings eliminates the need to hardcode connection logic for Azure services that the runtime supports. For services without binding support, you create SDK clients directly in your function code. The [supported bindings reference](/en-us/azure/azure-functions/functions-triggers-bindings#supported-bindings) lists all available binding extensions, including Blob Storage, Cosmos DB, Event Hubs, Service Bus, Queue Storage, and more.

### Create HTTP triggers for inference endpoints

HTTP triggers turn a function into a REST API endpoint that responds to HTTP requests. They support GET, POST, and other HTTP methods, making them the primary pattern for building inference endpoints that clients call synchronously. HTTP triggers are the most common entry point for AI backends that serve predictions, classifications, or transformations in real time.

In the Python v2 programming model, you define HTTP triggers using the `@app.route()` decorator. The decorator specifies the route path, accepted HTTP methods, and authorization level. The function receives an `HttpRequest` object containing headers, query parameters, and the request body, and returns an `HttpResponse` with the result.

```
## Code fragment - focus on HTTP trigger for an inference endpoint
import azure.functions as func
import json

app = func.FunctionApp()

@app.route(route="classify", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def classify_document(req: func.HttpRequest) -> func.HttpResponse:
    payload = req.get_json()
    document_text = payload.get("text")

    # Call inference logic or Azure AI service
    classification = perform_classification(document_text)

    return func.HttpResponse(
        json.dumps({"category": classification}),
        status_code=200,
        mimetype="application/json"
    )

```

Authorization levels control who can invoke an HTTP\-triggered function. The `anonymous` level requires no key, which suits development and internal health check endpoints. The `function` level requires a function\-specific key sent in the `x-functions-key` header or `code` query parameter, and is the recommended baseline for production inference endpoints. The `admin` level requires the master key and should be reserved for administrative operations. Authorization keys provide a basic access barrier but don't replace caller identity verification using Microsoft Entra ID or API Management.

HTTP\-triggered functions face a 230\-second timeout imposed by the Azure Load Balancer. For AI tasks that take longer than this limit, such as large document processing or complex model inference, return a `202 Accepted` response with a status endpoint URL and process the work asynchronously using a Service Bus trigger. This async request\-reply pattern was covered in the previous unit on hosting and scaling.

### Create Service Bus triggers for batch processing

Service Bus queue triggers start a function when a message arrives in an Azure Service Bus queue. This trigger type is the foundation for asynchronous AI processing patterns where work items are submitted through one interface and processed independently at a rate determined by available compute resources. Service Bus triggers handle retry logic, dead\-letter management, and concurrency scaling automatically. Service Bus also provides features beyond basic queuing, such as message sessions, duplicate detection, and scheduled delivery, which are valuable for coordinating complex AI processing pipelines.

A common AI pattern pairs an HTTP endpoint with a Service Bus trigger. The HTTP function accepts a batch request, validates the input, writes individual work items to a Service Bus queue, and returns immediately. A separate Service Bus\-triggered function processes each item independently, performing inference, calling Azure AI services, and writing results to storage. This separation decouples ingestion throughput from processing throughput, letting each scale to its own optimal instance count.

In the Python v2 model, you define Service Bus queue triggers using the `@app.service_bus_queue_trigger()` decorator. The decorator specifies the queue name and the connection setting that resolves to the Service Bus namespace connection string or identity\-based connection.

```
## Code fragment - focus on Service Bus queue trigger for processing work items
@app.service_bus_queue_trigger(arg_name="msg", queue_name="document-jobs", connection="ServiceBusConnection")
def process_document(msg: func.ServiceBusMessage) -> None:
    job = json.loads(msg.get_body().decode("utf-8"))
    document_url = job["document_url"]
    job_id = job["job_id"]

    # Perform document processing and classification
    result = extract_and_classify(document_url)

    # Store result (using output binding or SDK client)
    save_result(job_id, result)

```

You can configure concurrency behavior for Service Bus triggers in `host.json`. The `maxConcurrentCalls` property controls how many messages each instance processes simultaneously, and `maxAutoLockRenewalDuration` sets how long the runtime renews the message lock while processing continues. For AI workloads that perform resource\-intensive processing per message, setting `maxConcurrentCalls` to `1` ensures each message gets the full instance resources. The `maxAutoLockRenewalDuration` should be set high enough to cover your longest expected processing time, so the lock doesn't expire while an AI service call is still in progress.

```
{
    "version": "2.0",
    "extensions": {
        "serviceBus": {
            "maxConcurrentCalls": 1,
            "maxAutoLockRenewalDuration": "00:05:00"
        }
    }
}

```

When a message exceeds the queue's `maxDeliveryCount` (configured on the Service Bus queue resource itself, with a default of 10\), the Service Bus broker automatically moves it to the queue's built\-in dead\-letter sub\-queue. You can monitor this dead\-letter queue for messages that repeatedly fail processing, which helps identify issues with specific input data, downstream service outages, or bugs in your processing logic. The dead\-letter queue includes metadata such as the dead\-letter reason and description, providing richer diagnostic context than a simple failed message.

### Use output bindings to store results

Output bindings write data to external services without requiring explicit SDK client code in your function. The runtime handles connection management, authentication, and serialization based on the binding configuration. For AI backends, output bindings provide a concise way to persist inference results, processed documents, and derived data to storage services.

Common output binding targets for AI workloads include Azure Blob Storage for storing processed documents and binary artifacts, Azure Cosmos DB for writing structured inference results, and Azure Service Bus for fanning out work to downstream processors. The following example shows a Service Bus\-triggered function that uses a Blob Storage output binding to save processed text:

```
## Code fragment - focus on output binding for storing results
@app.service_bus_queue_trigger(arg_name="msg", queue_name="document-jobs", connection="ServiceBusConnection")
@app.blob_output(arg_name="output_blob", path="results/{rand-guid}.json", connection="AzureWebJobsStorage")
def process_and_store(msg: func.ServiceBusMessage, output_blob: func.Out[str]) -> None:
    job = json.loads(msg.get_body().decode("utf-8"))

    result = extract_and_classify(job["document_url"])

    output_blob.set(json.dumps({
        "job_id": job["job_id"],
        "classification": result["category"],
        "confidence": result["score"]
    }))

```

When a function needs to return an HTTP response and write to an output binding simultaneously, the Python v2 model supports multiple outputs through a custom return type. You can define the HTTP response and the output binding as separate properties, allowing the function to respond to the caller and persist data in a single invocation.

Cosmos DB output bindings write JSON documents directly to a container. You can specify the database name, container name, and connection setting in the decorator. The runtime serializes your output object and inserts or upserts it into the target container.

```
## Code fragment - focus on Cosmos DB output binding
@app.service_bus_queue_trigger(arg_name="msg", queue_name="classification-results", connection="ServiceBusConnection")
@app.cosmos_db_output(
    arg_name="output_doc",
    database_name="ai-results",
    container_name="classifications",
    connection="CosmosDBConnection"
)
def store_classification(msg: func.ServiceBusMessage, output_doc: func.Out[func.Document]) -> None:
    result = json.loads(msg.get_body().decode("utf-8"))

    output_doc.set(func.Document.from_dict({
        "id": result["job_id"],
        "category": result["category"],
        "confidence": result["score"],
        "processed_at": datetime.utcnow().isoformat()
    }))

```

### Connect to Azure AI services from a function

The triggers and bindings model doesn't cover every Azure service. For services without dedicated bindings, such as Azure AI Document Intelligence, Azure OpenAI Service, or Azure AI Search, you create SDK clients directly in your function code. This approach gives you full access to the service's API surface while still benefiting from the Functions hosting and scaling infrastructure.

When creating SDK clients, initialize the client object outside the function handler so it persists across invocations on the same instance. Client initialization typically involves establishing connections, loading configuration, and caching authentication tokens. By placing this initialization at the module level, you avoid repeating this overhead on every function invocation.

```
## Code fragment - focus on SDK client initialization and reuse
from azure.identity import DefaultAzureCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os

credential = DefaultAzureCredential()

doc_intelligence_client = DocumentIntelligenceClient(
    endpoint=os.environ["DOCUMENT_INTELLIGENCE_ENDPOINT"],
    credential=credential
)

@app.service_bus_queue_trigger(arg_name="msg", queue_name="document-jobs", connection="ServiceBusConnection")
def analyze_document(msg: func.ServiceBusMessage) -> None:
    job = json.loads(msg.get_body().decode("utf-8"))

    poller = doc_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        analyze_request={"url_source": job["document_url"]},
        content_type="application/json"
    )
    result = poller.result()
    # Process extraction results...

```

Using `DefaultAzureCredential` for authentication allows the same code to work both locally (using developer credentials from Azure CLI or Visual Studio Code) and in production (using the function app's managed identity). This credential chain is covered in detail in a later unit on identity and access configuration.

### Additional resources

* [Azure Functions triggers and bindings](/en-us/azure/azure-functions/functions-triggers-bindings)
* [Azure Service Bus trigger for Azure Functions](/en-us/azure/azure-functions/functions-bindings-service-bus-trigger)
* [Azure Blob Storage output binding for Azure Functions](/en-us/azure/azure-functions/functions-bindings-storage-blob-output)

---

## Manage secrets and configuration in Functions

Azure Functions stores configuration as application settings, which the runtime injects into the process as environment variables. For AI backends, these settings typically include service endpoints, model identifiers, connection strings, and feature flags. Managing these values securely across development, staging, and production environments require a layered approach that separates nonsecret configuration from sensitive credentials and provides auditability for secret access.

### Use application settings for configuration

Application settings are key\-value pairs that you configure in the Azure portal, Azure CLI, or through infrastructure\-as\-code templates. The Azure Functions runtime exposes these settings to your function code as environment variables, making them accessible through standard language mechanisms. Azure encrypts application settings at rest and decrypts them only when injecting them into the app's process memory, so they aren't stored in plaintext on disk.

In Python, you access application settings using `os.environ` for required settings or `os.getenv` for settings with fallback defaults. This pattern keeps your function code environment\-agnostic, since the same code reads configuration from `local.settings.json` during development and from Azure\-managed application settings in production.

```
## Code fragment - focus on reading application settings
import os

ai_endpoint = os.environ["AI_SERVICE_ENDPOINT"]
model_id = os.environ["MODEL_ID"]
confidence_threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.85"))
max_batch_size = int(os.getenv("MAX_BATCH_SIZE", "10"))

```

Common application settings for AI workloads include Azure AI service endpoints, model deployment names, inference confidence thresholds, concurrency limits, and feature flags that toggle processing behavior. Keep each setting focused on a single value to make updates granular. Avoid encoding complex structures in a single setting when separate key\-value pairs provide clearer configuration management.

Locally, application settings live in `local.settings.json` under the `Values` object. This file is excluded from source control by the default `.gitignore` because it often contains connection strings and other sensitive values. When deploying, the runtime reads settings from the Azure\-managed configuration store rather than from this file.

### Reference secrets from Azure Key Vault

Key Vault references let you store sensitive values in Azure Key Vault and reference them from application settings. Instead of placing an API key or connection string directly in an application setting, you set the value to a Key Vault reference expression. The runtime resolves the reference at app startup, retrieves the secret from Key Vault, and injects the actual value as an environment variable. Your function code reads the setting with `os.environ` as usual, unaware that the value originates from Key Vault.

Two reference syntaxes are available. The URI syntax points to a specific secret version or the latest version:

```
@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/AiServiceKey/)

```

The named syntax uses vault name and secret name as separate components:

```
@Microsoft.KeyVault(VaultName=myvault;SecretName=AiServiceKey)

```

Both syntaxes require the function app to have a managed identity (system\-assigned or user\-assigned) with the `Key Vault Secrets User` role on the target vault. Without this role assignment, the runtime can't retrieve the secret and the application setting resolves to an error indicator rather than the secret value.

Key Vault references resolve at app startup and are periodically re\-resolved. When you use a versionless secret URI (omitting the version GUID), the runtime automatically detects new secret versions and begins using the latest version within 24 hours. Any configuration change to the app triggers an immediate refetch of all referenced secrets. If you specify a version in the URI, the reference remains pinned to that version until you update the application setting with a new version identifier. For AI backends that use API keys with scheduled rotation, use versionless URIs so the runtime picks up rotated secrets automatically.

The benefits of Key Vault references extend beyond security. They centralize secret management across multiple function apps and services, provide audit logging through Key Vault's access policies and diagnostic settings, and separate secret ownership from application deployment. A security team can manage and rotate secrets without modifying application configuration.

### Integrate with Azure App Configuration

Azure App Configuration provides a centralized store for non\-secret configuration values and feature flags. While application settings work well for individual function apps, App Configuration becomes valuable when multiple function apps or microservices share configuration values such as model endpoint URLs, inference thresholds, or feature toggles. Changing a setting once in App Configuration propagates the update across all connected applications.

You connect to App Configuration using the App Configuration provider library for your language. In Python, the `azure-appconfiguration-provider` library loads configuration values during function startup and makes them available throughout the function's lifetime. The provider supports label\-based filtering, which lets you load different configuration sets for different environments (development, staging, production) from the same App Configuration store.

```
## Code fragment - focus on loading configuration from App Configuration
from azure.appconfiguration.provider import load
from azure.identity import DefaultAzureCredential
import os

config = load(
    endpoint=os.environ["APP_CONFIG_ENDPOINT"],
    credential=DefaultAzureCredential(),
    selects=[{"key_filter": "AIBackend/*"}]
)

model_endpoint = config["AIBackend/ModelEndpoint"]
inference_timeout = int(config["AIBackend/InferenceTimeout"])

```

A common architecture combines App Configuration for nonsecret values with Key Vault for secrets. App Configuration even supports Key Vault references as configuration values, creating a unified configuration surface where developers retrieve both regular settings and secrets through the same provider. This layered approach provides centralized management for shared configuration while maintaining strict access control over sensitive values.

### Handle configuration in the local development workflow

Local development requires reproducing the same configuration structure that runs in Azure, but pointing to local services and emulators instead of cloud resources. The `local.settings.json` file mirrors the application settings that the Azure portal manages, giving developers a local equivalent of the production configuration surface.

You can pull current application settings from a deployed function app into your local configuration using the Azure Functions Core Tools command. This command downloads all settings and writes them to `local.settings.json`, which is useful when you need to quickly replicate a production or staging environment's configuration locally.

```
func azure functionapp fetch-app-settings <function-app-name>

```

Because `local.settings.json` might contain connection strings or API keys after fetching settings, you can encrypt the file with Core Tools to protect secrets at rest on your development machine. The encrypted file is still readable by the local Functions runtime, but the values aren't visible in plaintext in your editor or file system.

```
func settings encrypt

```

For day\-to\-day development, maintain separate configuration values that point to local resources. Set `AzureWebJobsStorage` to `UseDevelopmentStorage=true` for Azurite, configure Cosmos DB connection strings to target the local emulator endpoint, and use local Redis or PostgreSQL instances. When the app is deployed, these values are replaced by production application settings, Key Vault references, or identity\-based connections. This separation ensures that local development never accidentally touches production data or services.

### Additional resources

* [App settings reference for Azure Functions](/en-us/azure/azure-functions/functions-app-settings)
* [Use Key Vault references for App Service and Azure Functions](/en-us/azure/app-service/app-service-key-vault-references)
* [Azure App Configuration documentation](/en-us/azure/azure-app-configuration/overview)

---

## Configure identity and access for Functions

Azure Functions provides two identity and access mechanisms that differ from general Azure security patterns: identity\-based connections that replace connection strings in trigger and binding configurations, and authorization keys that control access to HTTP\-triggered endpoints. These mechanisms change how you configure bindings, authenticate to downstream services, and protect function endpoints from unauthorized callers. Understanding both features helps you eliminate stored credentials from your function app's configuration while maintaining appropriate access control.

### Replace connection strings with identity\-based connections

Azure Functions binding extensions support identity\-based connections, which use the function app's managed identity to authenticate instead of requiring a connection string stored in application settings. This approach eliminates secrets from your trigger and binding configuration entirely. Rather than storing a full connection string that contains account keys or shared access signatures, you configure the binding with a named connection that includes only the service endpoint or account name. The runtime handles authentication transparently using the assigned managed identity.

To set up an identity\-based connection, enable a system\-assigned managed identity on the function app, then assign the required Azure roles on the target resource. The function app authenticates using the identity, and no secret values appear in application settings. This is particularly valuable for AI backends that connect to multiple Azure services, because each additional connection string in configuration expands the surface area for credential leaks.

The most common identity\-based connection is for the runtime's own storage dependency. You can replace the traditional `AzureWebJobsStorage` connection string with identity\-based settings by configuring the storage account name and assigning the appropriate roles:

```
AzureWebJobsStorage__accountName = mystorageaccount

```

The runtime authenticates with the function app's managed identity. The minimum required role is `Storage Blob Data Owner`, which covers host\-level coordination such as function state, key storage, and timer locks. If your app uses blob triggers, you also need `Storage Queue Data Contributor` and `Storage Account Contributor` because blob triggers internally use storage queues for blob receipts. For the Service Bus and Cosmos DB patterns covered in this module, `Storage Blob Data Owner` alone is sufficient.

### Use identity\-based connections for trigger and output bindings

Identity\-based connection configuration differs from connection string configuration in how you set up the named connection prefix. Each binding's `connection` property in `function_app.py` references a named prefix (for example, `connection="ServiceBusConnection"`). With connection strings, you create a single application setting with the prefix name containing the full connection string. With identity\-based connections, you create settings using the prefix with property suffixes that specify the service endpoint.

The following examples show how identity\-based configuration works for common binding types used in AI backends:

**Service Bus trigger with identity\-based connection:** Replace the Service Bus connection string with the fully qualified namespace. Assign the `Azure Service Bus Data Receiver` role to the function app's managed identity on the Service Bus namespace. For output bindings, assign the `Azure Service Bus Data Sender` role instead.

```
ServiceBusConnection__fullyQualifiedNamespace = mynamespace.servicebus.windows.net

```

```
## Code fragment - focus on Service Bus trigger with identity-based connection
@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="document-jobs",
    connection="ServiceBusConnection"
)
def process_document(msg: func.ServiceBusMessage) -> None:
    job = json.loads(msg.get_body().decode("utf-8"))
    # Process the document...

```

**Cosmos DB output binding with identity\-based connection:** Replace the Cosmos DB connection string with the account endpoint. Assign the `Cosmos DB Built-in Data Contributor` role to the function app's managed identity.

```
CosmosDBConnection__accountEndpoint = https://mycosmosaccount.documents.azure.com:443/

```

Each binding extension documents its supported identity properties and required roles. The suffix pattern differs by service: storage bindings use `__accountName` or service\-specific URIs, Cosmos DB uses `__accountEndpoint`, and messaging services use `__fullyQualifiedNamespace`. Consult the [identity\-based connections reference](/en-us/azure/azure-functions/functions-reference#configure-an-identity-based-connection) for the complete list of supported bindings and their configuration properties.

### Authenticate SDK clients with managed identity

For Azure services without dedicated binding support, such as Azure AI Document Intelligence, Azure OpenAI Service, or Azure AI Search, you create SDK clients directly in your function code. These clients can authenticate using the same managed identity that serves your trigger and binding connections, providing a consistent identity\-based approach across all service integrations.

`DefaultAzureCredential` from the Azure Identity library provides a credential chain that works in both local development and production environments. Locally, it authenticates using your developer credentials from Azure CLI or Visual Studio Code. In production, it uses the function app's managed identity. This dual behavior means the same code runs without modifications across environments.

Initialize both the credential object and the service client outside the function handler at the module level. This placement ensures the objects persist across invocations on the same instance, avoiding the overhead of repeated credential resolution and connection establishment. Module\-level initialization is safe because Azure Functions reuses the same process for multiple invocations until the instance is recycled.

```
## Code fragment - focus on module-level client initialization
import os
from azure.identity import DefaultAzureCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.search.documents import SearchClient

credential = DefaultAzureCredential()

doc_client = DocumentIntelligenceClient(
    endpoint=os.environ["DOCUMENT_INTELLIGENCE_ENDPOINT"],
    credential=credential
)

search_client = SearchClient(
    endpoint=os.environ["SEARCH_ENDPOINT"],
    index_name=os.environ["SEARCH_INDEX"],
    credential=credential
)

```

For production deployments, assign the minimum required roles for each service. Azure AI Document Intelligence requires the `Cognitive Services User` role, Azure AI Search requires `Search Index Data Reader` or `Search Index Data Contributor` depending on the operations your function performs, and Azure OpenAI Service requires `Cognitive Services OpenAI User`. Applying the principle of least privilege limits the impact of any identity compromise.

### Secure HTTP endpoints with authorization keys

Azure Functions uses access keys to restrict access to HTTP\-triggered function endpoints. This mechanism is specific to Azure Functions and operates independently from Microsoft Entra authentication. Access keys provide a basic barrier that prevents unauthorized callers from invoking your functions, but they don't verify caller identity or provide fine\-grained access control.

Azure Functions defines four types of keys, each with a different scope:

* **Function keys:** Scoped to a single function. Each function can have multiple named keys. Include the key in the `x-functions-key` header or the `code` query parameter when calling the function.
* **Host keys:** Scoped to all functions in the function app. A single host key grants access to every HTTP\-triggered function in the app. Use host keys for administrative tools or monitoring agents that need to call multiple functions.
* **System keys:** Used by specific extensions to authenticate internal operations. For example, the MCP extension uses the `mcp_extension` system key to authenticate MCP client connections to the function app. System keys are managed by the runtime and shouldn't be shared broadly.
* **Master key:** Provides administrative access and overrides all other key types. The master key also grants access to the runtime REST APIs. Treat the master key as a highly sensitive credential and never embed it in client applications.

You set the authorization level per HTTP trigger using the `auth_level` parameter in the `@app.route()` decorator. The `anonymous` level requires no key, which is appropriate for health check endpoints or functions behind an API gateway that handles authentication separately. The `function` level requires a function\-specific key or a host key, and is the recommended baseline for production endpoints. The `admin` level requires the master key and should be reserved for administrative operations.

```
## Code fragment - focus on authorization levels
@app.route(route="classify", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def classify_document(req: func.HttpRequest) -> func.HttpResponse:
    # This function requires a function key or host key to invoke
    pass

@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("OK", status_code=200)

```

Access keys provide a basic access barrier but don't replace authentication for production AI endpoints. For applications that require caller identity verification, layer Azure API Management or App Service Authentication (Easy Auth) on top of access keys. API Management adds rate limiting, request validation, and OAuth 2\.0 token verification, while Easy Auth integrates Microsoft Entra ID directly with the function app.

### Additional resources

* [Identity\-based connections for Azure Functions](/en-us/azure/azure-functions/functions-reference#configure-an-identity-based-connection)
* [Azure Functions access keys](/en-us/azure/azure-functions/security-concepts#function-access-keys)
* [DefaultAzureCredential overview](/en-us/azure/developer/python/sdk/authentication/credential-chains#defaultazurecredential-overview)

---

## Exercise \- Create an MCP server with Azure Functions

The Model Context Protocol (MCP) is an open standard that defines how AI agents and language models discover and invoke external tools. Azure Functions includes an MCP extension that lets you expose function apps as MCP servers, where each function becomes a tool that MCP clients can call.

In this exercise, you create an Azure Functions project with the MCP extension, define tool trigger functions for document processing, configure the MCP server settings, and test the server locally by connecting to it from GitHub Copilot in agent mode.

Note

This exercise uses the Azure Functions MCP extension, which is actively evolving. Visit the [Azure Functions MCP extension documentation](/en-us/azure/azure-functions/functions-bindings-mcp-tool-trigger) for the most up\-to\-date setup instructions, API surface, and configuration options.

Tasks performed in this exercise:

* Create a new Azure Functions project with the MCP extension
* Configure the MCP server settings in *host.json*
* Define MCP tool trigger functions in *function\_app.py*
* Verify the Python environment
* Test the MCP server locally using GitHub Copilot in agent mode

This exercise takes approximately **25** minutes to complete.

### Before you start

To complete the exercise, you need:

* [Visual Studio Code](https://code.visualstudio.com/) on one of the [supported platforms](https://code.visualstudio.com/docs/supporting/requirements#_platforms).
* The [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) for Visual Studio Code.
* [Azure Functions Core Tools](/en-us/azure/azure-functions/functions-run-local) v4 or later.
* [Python 3\.9](https://www.python.org/downloads/) or later.
* The [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) extension for Visual Studio Code.

### Get started

Select the **Launch Exercise** button to open the exercise instructions in a new browser window. When you're finished with the exercise, return here to:

* Complete the module
* Earn a badge for completing this module

---

## Module assessment

Choose the best response for each of the following questions.

---

## Summary

In this module, you learned how Azure Functions provides a serverless compute platform for building AI backends that scale automatically with demand and charge only for actual execution time. You explored the differences between the Flex Consumption, Premium, and Consumption hosting plans, and evaluated cold start behavior and scaling mechanics for latency\-sensitive AI inference endpoints. You also set up a local development environment using Azure Functions Core Tools and the Azurite storage emulator to build and debug functions before deploying to Azure. You created HTTP triggers for inference endpoints and queue triggers for asynchronous batch processing, and used output bindings to write results to Azure Storage and Cosmos DB without writing boilerplate connection code. Additionally, you configured application settings, Key Vault references, and Azure App Configuration to manage secrets and configuration securely across environments. Finally, you applied managed identity to authenticate your function app to downstream Azure services without storing credentials, and secured HTTP endpoints using function\-level authorization keys.

### Additional resources

* [Azure Functions hosting options](/en-us/azure/azure-functions/functions-scale)
* [Azure Functions triggers and bindings](/en-us/azure/azure-functions/functions-triggers-bindings)
* [Securing Azure Functions](/en-us/azure/azure-functions/security-concepts)
* [Azure Functions Flex Consumption plan](/en-us/azure/azure-functions/flex-consumption-plan)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/_

## Fuentes
- [Build serverless AI backends with Azure Functions](https://learn.microsoft.com/en-us/training/modules/build-backends-azure-functions/?WT.mc_id=api_CatalogApi)
