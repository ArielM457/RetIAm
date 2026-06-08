# Manage data storage and query audit logs in Microsoft Sentinel

> Curso: Implement activity and event collection in Microsoft Sentinel (wwl-implement-activity-event-collection-sentinel) · Seccion: Implement activity and event collection in Microsoft Sentinel
> Duracion estimada: 31 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

With event collection, enrichment, and automated response now in place, Contoso Financial Services' Microsoft Sentinel environment is ingesting security data from across their hybrid infrastructure. But the security engineering team is facing three new challenges that expose gaps in the deployment.

First, the trading platform engineering team deployed a proprietary risk management system that generates security\-relevant events in a custom JSON format. None of Contoso's existing Microsoft Sentinel tables accept this format cleanly—forcing the team to either discard the events or shoehorn them into an ill\-fitting table schema that breaks every query written against it.

Second, the compliance team escalated. PCI\-DSS requires one year of log retention for in\-scope systems, and SOX requires seven years of audit records for financial controls. Contoso's current workspace default of 30 days satisfies neither, and the team has no cost model for extending retention across all tables—some of which generate hundreds of gigabytes per day.

Third, the internal audit team needs to investigate a suspicious SharePoint file download event from three months ago. The trail lives in Microsoft Purview Audit, not in the Microsoft Sentinel workspace. The audit team wants to search and correlate that activity alongside Microsoft Sentinel incidents from the same timeframe, but currently has to use a separate Microsoft Purview portal, export results to a spreadsheet, and correlate manually.

This module resolves all three challenges. You create a custom log table for the trading system's nonstandard events, configure per\-table Analytics \& Archive retention tiers that meet compliance requirements without over\-spending on hot storage, connect Microsoft Purview Audit as a Microsoft Sentinel data source, and query Purview Audit events directly from the Microsoft Defender portal—giving Contoso a unified investigation surface for both security and compliance scenarios.

### Learning objectives

After completing this module, you'll be able to:

* Create custom log tables in a Microsoft Sentinel workspace to store nonstandard ingested data.
* Configure data retention tiers and archive policies for Microsoft Sentinel tables.
* Connect Microsoft Purview Audit as a data source in Microsoft Sentinel.
* Query Purview Audit logs in the Microsoft Defender XDR portal.

---

## Create custom log tables in Microsoft Sentinel

Every data source that connects to Microsoft Sentinel lands its events in a Log Analytics table. Built\-in connectors write to well\-known tables like `SecurityEvent`, `CommonSecurityLog`, and `AzureActivity` \- tables with fixed schemas that the Microsoft Sentinel analytics rules and workbooks already know how to query. But Contoso's proprietary trading risk management system generates security\-relevant events in a custom JSON format that doesn't match any built\-in table. Without a custom table, those events have nowhere to land.

### Identify when a custom table is needed

A custom log table is the right choice when your data source meets any of these conditions:

* The data format doesn't match any existing built\-in table schema.
* You want to store data from an application that sends logs via the Logs Ingestion API rather than a standard connector.
* The data is high\-volume and noncritical, making it a candidate for the Auxiliary table plan at a lower ingestion cost.
* You need to define a custom schema to make the data queryable in a structured way.

Before creating a custom table, verify there isn't an existing connector that handles your data source—many purpose\-built connectors in the Content Hub write to `_CL` tables with parsers and workbooks already included.

When you do need a custom table, you have two table plan options. The **Analytics plan** supports full interactive KQL queries with standard retention—use this for security\-relevant data that analysts will actively query. The **Auxiliary plan** offers lower ingestion cost with limited query capability and short retention—use this for high\-volume compliance or usage data that you ingest for archival but rarely query directly.

### Create and define a custom table schema

To create a custom table in the Microsoft Defender portal:

1. Navigate to **Microsoft Sentinel** \> **Configuration** \> **Tables**.
2. Select **\+ New custom table**.
3. Enter a table name. Microsoft Sentinel automatically appends the `_CL` suffix to custom log tables. For Contoso's trading system, enter `TradingSystemEvents` \- the table appears as `TradingSystemEvents_CL` in all queries and schema views.
4. Select the table plan: **Analytics** for a table that analysts query in investigations, or **Auxiliary** for high\-volume, low\-query data.
5. Define the schema by adding columns. For each column, specify a name and data type. Common data types include `string` for identifiers and messages, `datetime` for timestamps, `int` for numeric codes, and `dynamic` for nested JSON objects. Add at minimum a `TimeGenerated` column of type `datetime` \- this column is required by all Log Analytics tables and drives time\-range filtering in queries.

For the Contoso trading risk system, the schema includes:

| Column name | Type | Description |
| --- | --- | --- |
| `TimeGenerated` | datetime | Event timestamp (UTC) |
| `TradeId` | string | Unique trade identifier |
| `RiskScore` | int | Calculated risk score (0–100\) |
| `AlertType` | string | Risk alert category |
| `UserId` | string | Trader who initiated the action |
| `SourceSystem` | string | Originating platform identifier |
6. Select **Create**.

### Configure a data collection rule for ingestion

Creating the table establishes the schema and target. Sending data to it requires a **Data Collection Rule (DCR)** and a **Data Collection Endpoint (DCE)**. The DCE provides the network endpoint that applications call, and the DCR defines the transformation and routing from the source data stream to the target table.

To configure ingestion:

1. In the Azure portal, navigate to **Monitor** \> **Data Collection Endpoints** and create a new endpoint in the same region as your workspace. Note the **Logs Ingestion URI** shown on the endpoint's Overview page—your source application uses this URI to POST events.
2. Navigate to **Monitor** \> **Data Collection Rules** and select **Create**. On the **Basics** tab, enter a rule name and select the same subscription and resource group as your workspace.
3. On the **Data sources** tab, select **\+ Add data source**. Set the **Data source type** to **Custom logs (JSON format)**. Under **Destination**, select your Log Analytics workspace and the `TradingSystemEvents_CL` table.
4. If your source data format differs from the target table schema, add a **Transformation** using KQL. For example, to rename an incoming field `risk_score` to the table column `RiskScore`:

```
source | extend RiskScore = toint(risk_score) | project-away risk_score

```
5. Select **Review \+ create**, then **Create**.

To validate ingestion, have your source application send a test event to the DCE's Logs Ingestion URI with the correct authorization header. After one to two minutes, run the following KQL query in the Defender portal to confirm the event arrived:

```
TradingSystemEvents_CL
| take 10

```

If the query returns results, the table and ingestion pipeline are working. If no results appear after five minutes, verify that the DCR is correctly associated with the DCE and that the application is sending to the correct URI.

---

## Implement data retention in Microsoft Sentinel

Contoso's Microsoft Sentinel workspace is currently running on the Log Analytics default retention of 30 days for all tables. That means events older than a month are gone—no recovery, no query, no audit trail. PCI\-DSS requires one year of in\-scope system log retention. SOX requires seven years of financial control audit records. The gap between 30 days and seven years isn't a configuration oversight; it's a compliance liability. Closing it requires understanding how Microsoft Sentinel's data tiers work and applying them deliberately to the right tables.

### Compare Microsoft Sentinel data retention tiers

Microsoft Sentinel offers three storage tiers for Log Analytics tables. Each balances queryability, cost, and retention duration differently.

**Analytics tier** is the standard tier for all tables. Data in this tier is fully interactive—you can run any KQL query against it at any time. Interactive retention in the Analytics tier can be set from 30 days up to two years. The cost is higher per gigabyte than the other tiers, which makes it the right choice for tables you actively query during investigations and threat hunting.

**Basic tier** is designed for high\-volume, low\-value logs—think verbose diagnostic data or network flow records that you ingest for completeness but rarely query. Basic tier tables have eight days of interactive retention at a lower ingestion cost. The tradeoff is limited query capability: you can run queries, but only against a limited time window. Use the Basic tier for tables that serve compliance ingestion requirements but don't feed your daily detection and investigation workflows.

**Archive tier** extends the total retention period for any Analytics or Basic table beyond the interactive window, up to 12 years. Data in the Archive tier is stored at low cost, but it isn't directly queryable with KQL. To investigate archived data, you run a **restore job** that brings a copy of the archived data back into an interactive temporary table (with `_RST` suffix) for a defined time window. For smaller data sets, a **search job** provides full\-text lookup against archived data without a full restore.

The distinction between *interactive retention* and *total retention* is important. Interactive retention is how long the data stays in the queryable Analytics or Basic tier. Total retention is how long the data exists at all—the sum of the interactive period plus the Archive period.

### Design a retention strategy for compliance requirements

Before touching any settings, map your compliance requirements to specific tables. Contoso's requirements break down as follows:

| Compliance requirement | Retention period | Applicable tables |
| --- | --- | --- |
| PCI\-DSS \- in\-scope system logs | One year interactive | `SecurityEvent`, `CommonSecurityLog`, `AzureActivity`, `TradingSystemEvents_CL` |
| SOX \- financial control audit records | Seven years total | `OfficeActivity`, `CopilotActivity`, `AzureActivity`, `SigninLogs` |
| General security operations | 90 days interactive | All other Microsoft Sentinel tables |

For tables in multiple categories, apply the stricter requirement. `AzureActivity` appears in both lists—set it to one year interactive and seven years total to satisfy both.

For cost optimization, apply this rule: if your team doesn't query a table during active investigations, it's a candidate for the Basic tier or a short interactive period with Archive extension. For Contoso, the trading system's `TradingSystemEvents_CL` table is queried regularly in investigations, so it stays on the Analytics tier.

### Configure per\-table retention in the Defender portal

Retention settings are managed per\-table from the **Tables** page in the Microsoft Defender portal. To configure a table:

1. Navigate to **Microsoft Sentinel** \> **Configuration** \> **Tables**.
2. Find the table you want to configure—for example, `SecurityEvent`. Select the table row to open the details panel.
3. Select **Manage table**.
4. Under **Analytics tier**, set the **Interactive retention** value. For PCI\-DSS compliance on `SecurityEvent`, enter `365` days.
5. Under **Total retention**, enter the total period. For the SOX\-applicable tables, enter `2555` days (seven years).
6. Select **Save**.

Repeat this process for each table in your compliance scope. Changes take effect immediately and apply to new data going forward. Existing data that's already past the previous retention period can't be recovered—which is why establishing these settings at deployment time, rather than after the fact, is critical.

Note

The workspace\-level default retention setting (configurable in the Log Analytics workspace settings) applies to any table that doesn't have a per\-table override. Set the workspace default to your most common retention requirement—for example, 90 days—and then apply per\-table overrides only for tables that need longer or shorter periods. This approach minimizes per\-table configuration without sacrificing compliance coverage for the tables that need it most.

---

## Connect Microsoft Purview Audit to Microsoft Sentinel

Contoso's SOC received a request from the compliance team: investigate whether a SharePoint document containing trading strategy data was accessed by an unauthorized account three months ago. The event isn't in any firewall log or endpoint alert. It happened entirely within Microsoft 365—a platform Microsoft Sentinel doesn't monitor by default unless you configure it to. Microsoft Purview Audit captures exactly this type of user activity across the Microsoft 365 service boundary, and connecting it to Microsoft Sentinel brings those records into the same workspace where analysts are already working incidents.

### Understand what Microsoft Purview Audit captures

Microsoft Purview Audit records user and administrator activity across Microsoft 365 services. The scope is broad: Exchange Online email actions, SharePoint document operations, Teams messages and channel activity, Microsoft Entra sign\-in and directory changes, Power BI report access, and Dynamics 365 entity operations. Each event records the operation type, the user who performed it, the target object, the client IP address, and the timestamp.

E5 licensing unlocks **Audit Premium**, which provides longer retention within Purview, faster log availability, and other event types compared to the **Audit Standard** tier available with E3\.

Two Microsoft 365 Audit tables are especially relevant to Microsoft Sentinel investigations:

* **`OfficeActivity`**: The primary audit table. Captures Exchange, SharePoint, Teams, Microsoft Entra, and most other Microsoft 365 service activities.
* **`CopilotActivity`**: Captures activity from Microsoft 365 Copilot—including prompts submitted, responses returned, and files accessed in Teams, Word, SharePoint, and other Microsoft 365 applications where Copilot is active. \[REVIEW: Confirm `CopilotActivity` is a distinct table in Microsoft Sentinel as of mid\-2026 and not a subset of `OfficeActivity`.]

The `CopilotActivity` table represents an important and growing compliance surface. For Contoso, SOX requires audit evidence that access to financial systems and data is controlled and monitored. Microsoft 365 Copilot's ability to reason across SharePoint content and summarize documents means it can access sensitive financial data—and those accesses need to be in your audit trail. Connecting the Purview Audit data connector to Microsoft Sentinel brings both `OfficeActivity` and `CopilotActivity` into scope for KQL\-based investigation and incident correlation.

Note

Purview Audit events are typically available in Microsoft Sentinel within 30 minutes of the activity occurring. For time\-critical investigations, be aware of this lag when querying recent events.

### Prepare the prerequisites for integration

Before configuring the connector, verify these prerequisites are met:

* **Unified audit logging is enabled** in your Microsoft 365 tenant. In the Microsoft Purview portal, navigate to **Audit** and check that the banner says "Recording user and admin activity." If it shows "Start recording," select it to enable. You can also verify via PowerShell in Exchange Online:

```
Get-AdminAuditLogConfig | Select-Object UnifiedAuditLogIngestionEnabled

```

The output should show `True`. If it shows `False`, contact your Microsoft Purview admin to enable it.
* **Licensing**: The tenant must have at least Microsoft 365 E3 for Audit Standard coverage. For `CopilotActivity` events, verify that Microsoft 365 Copilot licenses are assigned to users whose activity you want to audit.
* **Permissions**: Three roles are needed across the integration:

	+ **Microsoft Sentinel Contributor** (or higher) in Azure—required to configure the data connector in the Defender portal.
	+ **Global Administrator** or **Security Administrator** in Microsoft 365—required to authorize the connector to access the tenant's audit logs.
	+ **View\-Only Audit Logs** in Microsoft 365 (assigned via the Microsoft Purview portal or Exchange admin center)—required for analysts who will query the `OfficeActivity` or `CopilotActivity` tables after ingestion.

### Configure the connector and validate ingestion

To connect Purview Audit to Microsoft Sentinel:

1. In the Microsoft Defender portal, navigate to **Microsoft Sentinel** \> **Configuration** \> **Data connectors**.
2. Search for the audit connector. \[REVIEW: Confirm the exact connector name as of mid\-2026—it can be listed as **Microsoft 365**, **Office 365**, or a dedicated **Microsoft Purview Audit** connector depending on the Defender portal version at your organization's tenant.]
3. Select the connector and choose **Open connector page**.
4. On the connector page, review the prerequisites section to confirm all conditions are met. Then select the log categories you want to ingest. At minimum, enable:
	* **Exchange**
	* **SharePoint**
	* **Microsoft Teams**
5. Select **Apply changes** (or **Save**, depending on the portal version). The connector authenticates to your Microsoft 365 tenant using delegated permissions established during the initial Microsoft Sentinel onboarding.

To validate ingestion, wait 30 to 60 minutes after enabling the connector, then run the following query in the Defender portal's **Advanced Hunting** or in **Logs**:

```
OfficeActivity
| where TimeGenerated > ago(1h)
| summarize count() by RecordType, Operation
| order by count_ desc

```

If results appear, the connector is ingesting data. To verify `CopilotActivity` ingestion, run:

```
CopilotActivity
| where TimeGenerated > ago(24h)
| take 10

```

If no results appear in `CopilotActivity` but `OfficeActivity` is populated, confirm that Microsoft 365 Copilot is licensed and active in the tenant, and that the connector configuration includes the Copilot or AI activity log category if listed as a separate option.

---

## Query Purview Audit logs in Microsoft Defender XDR

With the Purview Audit connector running and data flowing into the `OfficeActivity` table, Contoso's analysts now have two distinct tools for interrogating that data. The Purview Audit search interface in the Defender portal offers a guided, filter\-driven experience—ideal for compliance investigations where a nontechnical reviewer might examine the results. Advanced Hunting KQL gives analysts the ability to write precise queries, join across tables, and correlate audit records with active Microsoft Sentinel incidents. Knowing when to use each tool, and how to move between them, is what separates a complete investigation from an incomplete one.

### Search audit records using the Purview Audit search tool

The Purview Audit search interface is available in the Microsoft Defender portal. Navigate to the **Microsoft Purview** section and select **Audit**, or search for "Audit" using the portal search bar. If you don't see the navigation option, your account can need the **View\-Only Audit Logs** role assigned in the Microsoft Purview portal.

The Audit search page presents a structured filter form:

* **Start date / End date**: Set to the investigation window. For the Contoso SharePoint scenario, set the start date to 90 days ago and today as the end date.
* **Users**: Enter the account or accounts under investigation. Leave blank to search all users.
* **Activities**: Select specific operation types. For the SharePoint download scenario, search for "FileDownloaded" under SharePoint file and folder activities. Selecting specific activities narrows the result set significantly and reduces export size.
* **File, folder, or site** / **Workload**: Enter the SharePoint site URL or document name, and filter by service area (SharePoint, Exchange, Teams) if known.

Select **Search** to run the query. Results appear in a paginated list. Select any record to view the full detail panel, which includes the operation, user principal name, client IP address, site URL, target object, and result. For the Contoso investigation, the detail panel shows exactly which document was downloaded, from which site, and from which client IP—the information the compliance team needs.

To export results for compliance reporting, select **Export** in the toolbar. The export produces a CSV file with all record fields included, which you can share with the compliance team or retain as audit evidence.

### Query audit data with Advanced Hunting KQL

For more precise analysis—especially when you want to filter on multiple conditions, compute aggregations, or correlate audit data with other Microsoft Sentinel tables—use Advanced Hunting. The `OfficeActivity` table is available directly in Advanced Hunting queries.

For Contoso's SharePoint investigation, the following KQL query returns all SharePoint file download operations by the account under investigation within the 90\-day window:

```
OfficeActivity
| where TimeGenerated > ago(90d)
| where RecordType == "SharePointFileOperation"
| where Operation == "FileDownloaded"
| where UserId == "analyst@contoso.com"
| project TimeGenerated, UserId, ClientIP, Site_Url, SourceFileName, Operation
| order by TimeGenerated desc

```

Adjust the `UserId` value to the account under investigation. The `project` clause surfaces the fields most relevant to the compliance question: when the download occurred, who performed it, from where, and which file.

For `CopilotActivity` queries—for example, to identify Microsoft 365 Copilot interactions with SharePoint content—modify the table name and filter on relevant fields:

```
CopilotActivity
| where TimeGenerated > ago(30d)
| where AppContext contains "SharePoint"
| project TimeGenerated, UserId, AppContext, PromptType, ResponseSummary
| order by TimeGenerated desc

```

This type of query is valuable for SOX compliance reviews where you need to demonstrate that AI\-assisted access to financial data is auditable and reviewable.

### Correlate audit records with Microsoft Sentinel incidents

When an active Microsoft Sentinel incident involves a user account, you can pivot from the incident's entity into the `OfficeActivity` table to surface related audit events from the same time window.

For example, suppose a Microsoft Sentinel incident flagged impossible travel for the account `jsmith@contoso.com` \- sign\-ins from two geographically distant locations within 30 minutes. The account is already in your Microsoft Sentinel workspace as a user entity. To correlate that incident with SharePoint activity during the same window:

```
let incidentTime = datetime(2026-03-15T14:00:00Z);
let investigatedUser = "jsmith@contoso.com";
OfficeActivity
| where TimeGenerated between ((incidentTime - 2h) .. (incidentTime + 2h))
| where UserId =~ investigatedUser
| project TimeGenerated, RecordType, Operation, ClientIP, Site_Url, SourceFileName
| order by TimeGenerated asc

```

If the results show SharePoint document access from a different IP than the Microsoft Sentinel incident's flagged location, you have corroborating evidence for the compromise scenario. Select the query results and use **Add to incident** (if available in your portal version) to attach the findings directly to the Microsoft Sentinel incident record.

As with the Audit search tool, use **Export** in the Advanced Hunting toolbar to save results to CSV for documentary evidence linking the Microsoft Sentinel investigation to the Microsoft 365 audit trail.

---

## Knowledge check

Check your knowledge of custom log tables, data retention tiers, and Microsoft Purview Audit integration in Microsoft Sentinel.

### Check your knowledge

---

## Summary

Contoso Financial Services' Microsoft Sentinel environment now has a complete data lifecycle architecture. The proprietary trading system has a dedicated custom log table—events land in a properly typed schema that KQL queries can use without workarounds. Per\-table retention is configured at 90 days interactive for all compliance\-relevant tables, with Archive tier extending total retention to seven years across the in\-scope dataset, satisfying both PCI\-DSS and SOX requirements at a sustainable storage cost. And Purview Audit is connected as a Microsoft Sentinel data source, with audit events queryable from the Microsoft Defender portal using either the guided Audit search experience or Advanced Hunting KQL—giving the compliance and security teams a unified investigation surface they no longer have to leave to conduct a compliance inquiry.

In this module, you:

* Created a custom log table in the Microsoft Sentinel workspace and configured DCR\-based ingestion via the Logs Ingestion API for a nonstandard data source
* Configured Analytics and Archive retention tiers and set per\-table retention periods via the Defender portal table management experience
* Connected Microsoft Purview Audit as a data source in Microsoft Sentinel and verified log ingestion
* Queried Purview Audit logs in the Microsoft Defender XDR portal using both the Audit search tool and Advanced Hunting KQL to investigate a compliance scenario

### What's next

With the full collection\-to\-retention architecture in place and compliance audit access unified in the Defender portal, Contoso's Microsoft Sentinel implementation is ready for the next phase of the SC\-500 learning path: building detection capabilities through analytics rules, behavioral analytics, and threat hunting. For a deeper exploration of the data management patterns covered in this module, see the Microsoft Sentinel data transformation and retention documentation.

Tip

To explore the full range of data tier and retention options, see [Manage data tiers and retention in Microsoft Sentinel](/en-us/azure/sentinel/manage-data-overview).

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/manage-data-storage-audit-logs-sentinel/_

## Fuentes
- [Manage data storage and query audit logs in Microsoft Sentinel](https://learn.microsoft.com/en-us/training/modules/manage-data-storage-audit-logs-sentinel/?WT.mc_id=api_CatalogApi)
