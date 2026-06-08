# Configure AI Gateway security in Microsoft Foundry

> Curso: Implement security for AI (wwl-implement-ai-security) · Seccion: Implement security for AI
> Duracion estimada: 22 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Financial Services is expanding its AI capabilities with Microsoft Foundry, deploying language models for document analysis and regulatory research. Multiple applications share the same model deployments, and the security team identified a gap: there's no access control layer between the applications and the models. Any application that knows the endpoint can call the model. There's no visibility into token consumption, no audit trail for model calls, and no mechanism to detect or prevent misuse.

Adding a control layer between callers and AI models is the role of AI Gateway. In Microsoft Foundry, AI Gateway is powered by **Azure API Management (APIM)** and sits between your applications and model deployments, enforcing authentication, rate limits, routing policies, and logging—before any request reaches the model.

Note

AI Gateway in Microsoft Foundry is currently in **Preview**. Before following the configuration steps in this module, verify that preview features are available in your Azure subscription and Foundry environment.

This module covers how AI Gateway works, how to create and configure a gateway instance. Then you explore how to apply security controls and monitoring to protect your AI model traffic.

### Learning objectives

In this module, you learn how to:

* Examine the AI Gateway architecture and explain how it secures AI model traffic
* Create and configure an AI Gateway instance in Microsoft Foundry
* Apply access controls and monitoring to secure and audit AI Gateway usage

### Prerequisites

Before you begin, you should have:

* Experience working with Microsoft Azure AI Foundry
* Familiarity with API management and gateway concepts
* Understanding of AI workload security requirements
* **Contributor** or **Owner** role on an Azure resource group (to create a new API Management instance), or **API Management Service Contributor** role on an existing AI Policy Manager (APIM) instance
* **Azure AI Account Owner** or **Azure AI Owner** role on the Foundry resource

---

## Examine AI Gateway architecture

AI Gateway acts as a managed security layer between your applications and AI model deployments, enforcing authentication and access policies at a single control point. In Microsoft Foundry, AI Gateway is powered by **Azure API Management (APIM)**—a fully managed service that becomes the actual enforcement engine for authentication, rate limiting, policy application, and diagnostic logging. At Contoso Financial Services, multiple applications currently share the same model endpoint and API key—creating a risk where compromising one application exposes all model access. Here, you examine how AI Gateway architecture addresses this security gap by centralizing authentication, rate limiting, and audit logging.

| Component | Role |
| --- | --- |
| **Callers** | Client applications, agents, or services that request model inference |
| **AI Gateway (APIM instance)** | Azure API Management instance that enforces authentication, applies policies, logs traffic, and routes requests to model deployments |
| **Model deployments** | Backend AI models that receive and respond to requests only after passing gateway validation |
| **Azure Monitor / Log Analytics** | Destination for AI Policy Manager (APIM) diagnostic logs, enabling KQL queries, dashboards, and alert rules |

Agents are a common caller type in AI workloads. A Microsoft Foundry agent is an autonomous AI workflow that can call the model dozens of times per user interaction as it reasons through tasks, uses tools, or orchestrates subagents. Unlike a human\-operated application that makes one model call per user action, an agent can generate bursts of model traffic that are difficult to predict. Unknown model traffic for agents makes gateway rate limits and per\-caller authentication especially important: without them, a single runaway agent can exhaust model capacity for every other caller, and without per\-caller logging, agent activity is invisible in your audit trail.

### The security problem AI Gateway solves

Without a gateway, any application with the model endpoint URL and API key can call the model directly. This approach creates several security risks that grow as your AI deployment expands.

First, there's no authentication enforcement per caller. If you share a single API key across five applications, you can't distinguish which application made which request. When one application is compromised, the attacker gains access to all model deployments using that key.

Second, there's no rate limiting or quota control. A runaway application or malicious actor can consume all available model capacity, blocking legitimate users. Without a control layer, you must implement rate limiting in each calling application—a maintenance burden that invites inconsistent enforcement.

Third, there's no centralized audit trail. Requests go directly from applications to models, bypassing any logging infrastructure you maintain. Investigating suspicious activity or tracking usage patterns requires aggregating logs from every application individually.

### How AI Gateway centralizes security controls

AI Gateway sits between callers and model deployments as a reverse proxy. All requests flow through the APIM instance, which validates authentication, applies rate limits, and logs traffic before routing to the target model. Because APIM is the underlying engine, monitoring and advanced configuration—such as custom policies, load balancing, and detailed diagnostic logs—are managed through the APIM experience in the Azure portal, not exclusively through the Foundry portal.

The gateway enforces caller\-specific authentication using either API keys or Microsoft Entra tokens. With Microsoft Entra token authentication, each application uses its own managed identity to request a token. The gateway validates the token and identifies the caller before allowing the request to proceed. This approach eliminates shared credentials and gives you per\-application visibility into model usage.

Rate limiting operates at the gateway layer, not within each application. You configure token limits per caller or per subscription, and the gateway rejects requests that exceed the threshold. Limits protect model capacity from any single application monopolizing resources.

All request metadata—timestamp, caller identity, token count, response code, latency—flows to Azure Monitor through diagnostic logging. You gain a complete audit trail of model access without modifying calling applications.

### Gateway architecture for Contoso's scenario

Contoso operates three applications that call the same AI model: a document analysis tool, a regulatory research agent, and a customer\-facing chatbot. Today, all three use a shared API key stored in environment variables.

With AI Gateway in place, the shared key is replaced with individual managed identities for each application. The document analysis tool receives a token limit of 50,000 tokens per hour to handle peak processing loads. The regulatory research agent gets 30,000 tokens per hour for background analysis. The customer chatbot receives 20,000 tokens per hour with burst capacity for high\-traffic periods.

The gateway routes all three applications through a single inbound endpoint, validates each request's Microsoft Entra token, checks the caller's token quota, and logs the request before forwarding to the model deployment. If the regulatory research agent is compromised, the attacker can't access the other applications' quotas or impersonate their identities.

---

## Create and configure AI Gateway

Creating an AI Gateway in Microsoft Foundry establishes the security layer between your applications and model deployments, replacing direct endpoint access with centralized authentication and policy enforcement. Contoso Financial Services needs to replace its shared API key approach with individual caller authentication and token rate limits to prevent any single application from monopolizing model capacity. Here, you learn how to create a gateway instance, configure route policies, set token limits, and enable authentication.

| Configuration Step | Purpose |
| --- | --- |
| **Create gateway instance** | Deploy the managed reverse proxy within your Foundry project |
| **Configure route policies** | Direct incoming requests to specific model deployments based on caller or criteria |
| **Set token rate limits** | Control token consumption per caller to protect model capacity |
| **Configure authentication** | Enforce caller identity validation using API keys or Microsoft Entra tokens |
| **Review and test** | Verify configuration and validate with sample requests |

### Create the AI Gateway instance

To create an AI Gateway, sign in to **Microsoft Foundry** at [ai.azure.com](https://ai.azure.com)—not the Azure portal. Select **Operate** \> **Admin console**, then open the **AI Gateway** tab and select **Add AI Gateway**.

Select the Foundry resource you want to associate with the gateway. Then choose whether to create a new API Management instance or reuse an existing one.

Tip

**Create new** deploys a **Basic v2** Azure API Management instance—designed for development and testing. For production workloads, select **Use existing** and associate a Standard v2 or Premium v2 AI Policy Manager (APIM) instance. Premium v2 is required if your Foundry resource has public network access disabled and you need virtual network injection with private endpoint support.

Provide a name for the gateway and select **Add**. Provisioning typically completes within 5–10 minutes. Verify that the gateway appears in the list with a status of **Enabled**.

AI Gateway is enabled at the Foundry **resource** level—not the individual project level. After creation, new projects are gateway\-enabled by default. Existing projects must be manually enabled: select the gateway name, locate the project in the list, and select **Add project to gateway**.

### Configure route policies

Route policies determine how the gateway directs incoming requests to backend model deployments. Each route maps from the gateway's inbound endpoint to a specific model deployment, optionally filtering by caller identity, endpoint path, or request headers.

Open the gateway's route configuration panel and create a new route. Select the source as the gateway's inbound endpoint and the destination as your target model deployment. If you operate multiple models, create separate routes for each deployment.

With advanced routing, you direct different callers to different models based on their identity. For example, route internal applications to a premium model deployment with higher token limits, while external\-facing agents use a standard model with lower per\-request costs. Route policies also support A/B testing scenarios where you direct a subset of traffic to a new model version for validation.

For Contoso's scenario, configure three routes: one from the gateway to the production model deployment used by all three applications. Later, if Contoso deploys a specialized model for regulatory research, you add a second route that directs only the research agent to the specialized deployment.

### Set token rate limits

Token rate limits prevent a single project from monopolizing available model capacity. In Microsoft Foundry, rate limits apply at the **project level** per model deployment—each project can have independent tokens\-per\-minute (TPM) limits and total quota settings. This design lets you allocate capacity fairly across teams and workloads without depending on individual callers to self\-limit.

To configure token limits, go to **Operate** \> **Admin** in the Foundry portal, select the gateway, then select **Token management** \> **\+ Set limit**. Choose the project and the model deployment to restrict, then enter a value for **Limit (Token\-per\-minute)**.

Token enforcement has two complementary dimensions:

* \*\*TPM rate limit—limits token consumption to a configured maximum per minute. When requests exceed this limit, the caller receives a `429 Too Many Requests` response.
* \*\*Total token quota—limits token consumption to a configured maximum per quota period (hourly, daily, weekly, monthly, or yearly). When requests exhaust the quota, the caller receives a `403 Forbidden` response.

Understanding both response codes matters for application error handling: a `429` signals a temporary rate limit that resets at the next minute boundary, while a `403` means the project's total quota for the period is exhausted.

At Contoso, the security team configures separate project\-level limits for the shared model deployment: 50,000 TPM for the document analysis project to handle peak processing loads, 30,000 TPM for the regulatory research project, and 20,000 TPM for the customer chatbot project. Each project's limit is independent—if the document analysis project hits its rate limit, the other projects continue operating normally.

### Configure authentication

Authentication determines how the gateway validates caller identity. AI Gateway supports two primary modes: API key authentication and Microsoft Entra token authentication.

With API key authentication, each caller presents a unique API key in the request header. The gateway validates the key against registered callers and identifies the request source. While simpler to implement, API keys require secure storage and regular rotation to maintain security.

With Microsoft Entra token authentication, each calling application uses a managed identity or service principal to request an access token from Microsoft Entra ID. The application includes the token in the request header, and the gateway validates the token's signature, expiration, and claims before routing the request. This approach eliminates stored credentials and integrates with your organization's identity governance policies.

For production environments, configure Microsoft Entra token authentication. In the gateway's authentication settings, select **Microsoft Entra ID** as the authentication provider. Specify the required token audience and issuer to ensure the gateway only accepts tokens issued for your Foundry environment.

For each calling application, assign a managed identity (system\-assigned or user\-assigned) and grant the identity permission to access the gateway. Update application code to request a Microsoft Entra token and include it in the `Authorization: Bearer <token>` header with each model request.

For **Microsoft Foundry\-deployed agents**, authentication works through the managed identity assigned to the agent resource in Foundry. Each agent has a unique client ID that the gateway records in diagnostic logs as the caller identity—giving security teams per\-agent visibility into model usage rather than attributing all traffic to a single application identity. When the admin assigns gateway permissions, scope each agent's managed identity access to only the model deployments it legitimately needs. If an agent is compromised or begins generating unexpected traffic, you can revoke its role assignment without disrupting other agents or applications.

Contoso assigns a system\-assigned managed identity to each of its three applications. The gateway is configured to require Microsoft Entra tokens with the audience set to the gateway's resource ID. Applications request tokens using their managed identities and include them in all model inference requests.

### Review gateway configuration

Before directing production traffic to the gateway, verify your configuration settings. Confirm that route policies correctly map inbound requests to target model deployments. Check that token rate limits align with expected usage patterns and total model capacity.

Test authentication by making a sample request from one of your calling applications. Ensure the application successfully obtains a Microsoft Entra token, includes it in the request header, and receives a valid response from the gateway. Verify that the request appears in diagnostic logs with the correct caller identity.

Monitor the gateway's metrics during initial rollout to detect configuration issues early. Watch for elevated rates of authentication failures or rate limit rejections, which indicate misconfigured caller identities or token quotas.

---

## Secure and monitor AI Gateway access

After Contoso configures AI Gateway authentication and rate limits, applying network access controls and diagnostic logging completes your security posture. Contoso is restricting who can reach the gateway and capturing detailed audit trails of all model requests. Contoso Financial Services needs visibility into model usage patterns to detect anomalies like off\-hours requests or sudden token consumption spikes that could indicate credential theft or application errors. Here, you learn how to restrict gateway network exposure, enable diagnostic logging, monitor usage with Azure Monitor, and detect suspicious activity.

| Security Control | Purpose |
| --- | --- |
| **Network access restriction** | Limit gateway endpoint exposure to specific networks or IP ranges |
| **Managed identity for gateway** | Authenticate the gateway to backend resources without stored credentials |
| **Diagnostic logging** | Capture request metadata for audit trails and compliance |
| **Azure Monitor metrics** | Track request volume, token consumption, and error rates |
| **Anomaly detection** | Identify unusual usage patterns that indicate security or operational issues |

### Restrict network access to the gateway

By default, AI Gateway endpoint accessibility depends on the Azure API Management tier and networking configuration of your AI Policy Manager (APIM) instance. For production environments, restrict gateway access to specific Azure Virtual Networks or IP address ranges.

In the gateway's networking settings, configure network access rules that limit inbound connections. If the calling applications run within Azure, restrict access to the Virtual Network where those applications operate. Add the gateway to a private endpoint configuration so that traffic between applications and the gateway never traverses the public internet.

For applications running outside Azure or in hybrid environments, configure IP allowlisting to permit connections only from known source addresses. Combine IP restrictions with Microsoft Entra token authentication to enforce both network\-level and identity\-level access controls.

Contoso's three applications all run in Azure App Service within the same Virtual Network. The AI Gateway is configured with a private endpoint accessible only from that Virtual Network, eliminating public internet exposure entirely.

### Use managed identities for gateway authentication

The AI Gateway itself requires authentication to access backend resources like model deployments and diagnostic storage. Rather than storing credentials for the gateway, assign a system\-assigned or user\-assigned managed identity to the gateway resource.

In the gateway's identity settings, enable the system\-assigned managed identity. Grant this identity the necessary permissions to invoke model deployments—typically a role like **Cognitive Services User** or a custom role scoped to the specific deployments the gateway routes to.

Using managed identities eliminates the need to rotate credentials or secure connection strings for backend access. The gateway automatically obtains tokens as needed using its Azure\-managed identity, and access is governed through Azure role assignments you control centrally.

### Enable diagnostic logging

Diagnostic logging captures metadata for every request that passes through the gateway, creating a complete audit trail of model access. Logs include the timestamp, caller identity, token count, HTTP response code, and request latency. Prompt content and response content aren't logged by default—APIM diagnostic logging captures request metadata only.

In the gateway's diagnostic settings, create a new diagnostic configuration. Select the log categories you want to capture—typically **Request Logs** and **Authentication Logs**. Choose a destination for the logs: a Log Analytics workspace for querying and alerting, a Storage Account for long\-term retention, or an Event Hubs for streaming to external systems.

For compliance and incident response, route logs to a Log Analytics workspace. This destination supports rich querying with Kusto Query Language (KQL) and integrates with Azure Monitor alerts for real\-time detection of suspicious patterns.

Contoso configures the gateway to send diagnostic logs to its central Log Analytics workspace, where security operations teams already monitor other Azure resources. Retention is set to 90 days to meet regulatory compliance requirements.

### Monitor usage with Azure Monitor

After enabling diagnostic logging, use Azure Monitor to track gateway metrics and query log data for insights into model usage patterns. Key metrics to monitor include request volume, token consumption per caller, rate limit rejections, and error rates.

In Azure Monitor, create a dashboard that displays these metrics over time. Add charts showing total requests per hour, token consumption by caller identity, and the percentage of requests rejected due to rate limits or authentication failures. This visibility helps you detect capacity issues, misconfigured rate limits, or authentication problems.

Use KQL queries to analyze log data for specific insights. The following query summarizes successful request volume by API route over the past 24 hours, grouped by hour—helping you identify which model deployments are most heavily used and detect sudden changes in traffic patterns:

```
GatewayLogs
| where TimeGenerated > ago(24h)
| where ResponseCode == 200
| summarize TotalRequests = count() by ApiName, bin(TimeGenerated, 1h)
| order by TotalRequests desc

```

This query uses the **GatewayLogs** table in the Log Analytics workspace connected to your Azure API Management instance. It surfaces successful request volume by API name over the past 24 hours, helping you identify which model deployments are most heavily used and detect sudden changes in traffic patterns. If request volume for a specific API spikes unexpectedly, investigate for application errors or unauthorized access.

### Detect anomalies and respond to alerts

After the admin establishes a baseline of normal usage—typical request volume, token consumption rates, and access patterns—configure alerts to detect deviations that indicate problems. Create Azure Monitor alert rules for conditions like:

* A caller exceeds 80% of its token rate limit, suggesting the limit is too low or the application is making excessive requests
* Request error rates exceed 5%, indicating authentication issues or backend model problems
* Requests occur outside normal business hours from applications that should only operate during specific times
* A caller that typically consumes 10,000 tokens per day suddenly consumes 100,000 tokens
* A Foundry\-deployed agent generates far more model calls than its expected task frequency—for example, a document summarization agent that normally completes a task in 5–10 model calls suddenly makes hundreds of calls for a single document, suggesting a retry loop or prompt injection attack causing the agent to behave unexpectedly

When an alert fires, Azure Monitor sends notifications to your security or operations team via email, SMS, or integration with incident management systems. Investigate alerts promptly to determine whether the activity represents a genuine issue or an expected change in usage patterns.

One week after enabling alerts, Contoso's security team receives a notification: the document analysis application sent 300% more requests than usual at 2 AM on a Sunday. Investigation reveals a loop in the application code that retries failed requests indefinitely. The issue isn't a security breach, but without gateway monitoring, the problem would consume all available model capacity before anyone noticed during Monday morning business hours.

By combining network access restrictions, managed identities, diagnostic logging, and proactive monitoring, you create a comprehensive security and observability layer around your AI model deployments. You're ensuring that only authorized callers can access models, all activity is audited, and anomalies are detected quickly.

---

## Knowledge check

Check your knowledge with these questions.

### Check your knowledge

---

## Summary

Contoso Financial Services started this module with a shared API key, multiple applications calling the same model endpoint, and no mechanism to detect or prevent misuse. By the end, every model request passes through a controlled, authenticated, rate\-limited, and monitored gateway—and the 2 AM processing loop that could go undetected for weeks was caught within days.

### Review what you accomplished

You examined the AI Gateway architecture and identified the core principle: a managed reverse proxy layer that interposes between callers and model deployments, becoming the single enforcement point for all model access. Without a gateway, security depends on every application implementing its own controls—an approach that scales poorly and fails silently. With a gateway, access control, rate limiting, and logging happen in one place regardless of how many callers exist.

You created and configured a gateway instance in Microsoft Foundry, defining route policies that direct callers to the right model deployments. You then set token rate limits that allocate capacity fairly across applications, and Entra\-token authentication that replaces the shared API key with caller\-specific credentials. Each of Contoso's three applications now authenticates with its own managed identity—compromising one application's credential no longer grants access to the others.

You then applied access controls and monitoring to the running gateway, enabling diagnostic logging routed to Azure Monitor. You configured alert rules for token consumption anomalies, and wrote KQL queries to detect high\-volume requests outside business hours. The monitoring layer turns the gateway from a passive control point into an active detection capability.

In this module, you learned how to:

* Examine the AI Gateway architecture and explain how it secures AI model traffic
* Create and configure an AI Gateway instance in Microsoft Foundry
* Apply access controls and monitoring to secure and audit AI Gateway usage

### What's next

AI Gateway secures model\-layer traffic. You should next expand the protection upstream by configuring guardrails in Microsoft Foundry—content filters, block lists, and Prompt Shields that evaluate the content of prompts and responses before they reach your models.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-ai-gateway-security-foundry/_

## Fuentes
- [Configure AI Gateway security in Microsoft Foundry](https://learn.microsoft.com/en-us/training/modules/configure-ai-gateway-security-foundry/?WT.mc_id=api_CatalogApi)
