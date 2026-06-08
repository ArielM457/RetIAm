# Create and manage Microsoft Sentinel workspaces

> Curso: Implement activity and event collection in Microsoft Sentinel (wwl-implement-activity-event-collection-sentinel) · Seccion: Implement activity and event collection in Microsoft Sentinel
> Duracion estimada: 41 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Deploying the Microsoft Sentinel environment involves designing a workspace configuration to meet your security and compliance requirements. The provisioning process includes creating a Log Analytics workspace and configuring the Microsoft Sentinel options.

You're a Security Operations Analyst working at a company that is implementing Microsoft Sentinel. You're responsible for setting up the Microsoft Sentinel environment to meet the company requirement to minimize cost, meet compliance regulations, and provide the most manageable environment for your security team to perform their daily job responsibilities.

You start by understanding the Microsoft Sentinel workspace's architecture. After you've decided on your workspace implementation options, you create your first Microsoft Sentinel workspace.

After completing this module, you'll be able to:

* Describe Microsoft Sentinel workspace architecture
* Onboard a Microsoft Sentinel workspace to Microsoft Defender
* Manage a Microsoft Sentinel workspace in Microsoft Defender

### Prerequisites

Basic experience with Microsoft Defender and Azure services

---

## Manage workspaces across tenants using Azure Lighthouse

If you're required to manage multiple Microsoft Sentinel workspaces, or workspaces not in your tenant, you have two options:

* Microsoft Sentinel Workspace manager
* Azure Lighthouse

### Microsoft Sentinel Workspace manager

Microsoft Sentinel's Workspace manager enables users to centrally manage multiple Microsoft Sentinel workspaces within one or more Azure tenants. The Central workspace (with Workspace manager enabled) can consolidate content items to be published at scale to Member workspaces. Workspace manager is enabled in the `Configuration settings`.

### Azure Lighthouse

Implementing Azure Lighthouse provides the option to enable your access to the tenant. Once Azure Lighthouse is onboarded, use the directory \+ subscription selector on the Azure portal to select all the subscriptions containing workspaces you manage.

Azure Lighthouse allows greater flexibility to manage resources for multiple customers without having to sign in to different accounts in different tenants. For example, a service provider may have two customers with different responsibilities and access levels. By using Azure Lighthouse, authorized users can sign in to the service provider's tenant to access these resources.

---

## Configure logs

### Configure logs in Microsoft Sentinel workspaces

When configuring your Microsoft Sentinel workspaces, you have to plan for the two data states, the three table plans, and the two primary log tiers.

The two data states are:

* Analytics retention: For monitoring, troubleshooting, and near\-real\-time analytics
* Long\-term retention: A low\-cost state, not available in all table plans, but can be accessed through search jobs and restores

Table plans in a Log Analytics workspace determine the features available for each table and the cost of storing data in that table. You can configure different tables in a workspace to use different plans.

There are three plans in a Log Analytics workspace:

* The **Analytics** plan is suited for continuous monitoring, real\-time detection, and performance analytics. This plan makes log data available for interactive multi\-table queries and use by features and services for 30 days to two years.
* The **Basic** plan is suited for troubleshooting and incident response. This plan offers discounted ingestion and optimized single\-table queries for 30 days.
* The **Auxiliary** plan is suited for low\-touch data, such as verbose logs, and data required for auditing and compliance. This plan offers low\-cost ingestion and unoptimized single\-table queries for 30 days.

#### Log retention plans in Microsoft Sentinel

For Microsoft Sentinel workspaces connected to Defender, tiering and retention management must be done from the new table management experience in the Defender portal. If you have Basic logs in your workspace, convert them to analytics tier first from Log Analytics Tables experience before you can change tiering or retention from the Defender’s new table management experience.

Important

We recommend that users consider Microsoft Sentinel data lake as the preferred solution for storing secondary and long\-term data. Microsoft Sentinel data lake is designed to offer enhanced scalability, flexibility, and integration capabilities for advanced security and compliance scenarios.
Microsoft Sentinel data lake is currently in public preview and not yet generally available. We advise users to monitor updates and announcements regarding its availability status.

#### Manage data tiers in Microsoft Sentinel

There are two primary tiers in Microsoft Sentinel and a default XDR tier:

* Analytics Tier
* Data lake Tier
* XDR default tier

#### Analytics tier

This tier makes data available for alerting, hunting, workbooks, and all Microsoft Sentinel features. It retains data in two states:

* **Analytics retention**: In this "hot" state, data is fully available for real\-time analytics \- including high\-performance queries and analytics rules \- and threat hunting. By default, Microsoft Sentinel and Microsoft Defender XDR retain data in this tier for 30 days. You can extend the retention period of all tables to up to two years at a prorated monthly long\-term retention charge. You can extend the retention period of Microsoft Sentinel solution tables to 90 days for free.
* **Total retention**: By default, all data in the analytics tier is mirrored to the data lake for the same retention period. You can extend the retention of your data in the lake beyond the analytics retention, for up to 12 years of total retention at a low cost.

#### Data lake tier

In this low\-cost "cold" tier, Microsoft Sentinel retains your data in the lake only. Data in the data lake tier isn't available for real\-time analytics features and threat hunting. However, you can access data in the lake whenever you need it through KQL jobs, analyze trends over time by running scheduled KQL or Spark jobs, and aggregate insights from incoming data at a regular cadence by using summary rules

#### XDR default tier

By default, Microsoft Defender XDR retains threat hunting data in the XDR default tier, which includes 30 days of analytics retention, included in the XDR license. This data isn't ingested into the analytics or data lake tiers. You can extend the retention period of supported Defender XDR tables beyond 30 days and ingest the data into the analytics tier.

This diagram shows the retention components of the analytics, data lake, and XDR default tiers, and which table types apply to each tier:

#### Which tables can you manage in the Defender portal?

This section describes the table types you can manage in the Defender portal.

| Table type | Description | Examples | Is in Microsoft Sentinel workspace? |
| --- | --- | --- | --- |
| **Microsoft Sentinel** | Built\-in tables, including:\- Azure tables, such as AzureDiagnostics and SigninLogs. Microsoft Sentinel tables. Supported Defender XDR advanced hunting tables, which are created in your Microsoft Sentinel workspace when you increase the retention period beyond 30 days. See the **XDR** table type for Defender XDR tables that are currently unsupported. | \- Azure tables: `AzureDiagnostics`, `SigninLogs`\- Microsoft Sentinel tables: `AWSCloudTrail`, `SecurityAlert`\- XDR tables: `DeviceEvents`,`AlertInfo` | Yes |
| **Custom** | Tables you create manually or through jobs in your Microsoft Sentinel workspace, including summary rule and search job results tables, and custom data source tables. | Tables with `_CL` or `_SRCH` suffixes. | Yes |
| **XDR** | Tables in the XDR default tier, which have 30 days of analytics retention by default. You can view these tables, but you can't manage them from the Defender portal. | `IdentityInfo` | No |

Note

You can view Basic logs tables in your Microsoft Sentinel workspace from the Defender portal, but you can only currently manage them from your Log Analytics workspace. To manage these tables from the Defender portal, change the table plan from basic to analytics in your Microsoft Sentinel workspace.

#### Manage table settings

To view and manage table settings in the Microsoft Defender portal:

1. Select **Microsoft Sentinel** \> **Configuration** \> **Tables** from the left navigation pane.

The **Table** screen lists all the tables you can manage in the Microsoft Defender portal and the settings of each table.

The workspace column shows the Microsoft Sentinel workspace in which a Microsoft Sentinel or custom table is stored.
2. To manage Microsoft Sentinel and custom tables in a different Microsoft Sentinel workspace, select the workspace name at the top left corner of the screen to switch between workspaces.
3. Select a table on the **Tables** screen.

This opens the table details side panel with more information about the table, including the table description, tier, and retention details.
4. Select **Manage table**.

The **Manage table** screen lets you modify the table's retention settings in the current tier, and change the storage tier, if necessary.

	* **Analytics tier retention settings**:
	
	
		+ **Analytics retention**: 30 days to two years.
		+ **Total retention**: Up to 12 years of long\-term storage in the data lake. By default, total retention is equal to analytics retention, which means long\-term retention isn't applied. To enable long\-term retention, set the total retention to a value greater than analytics retention.
		
		
		Example: To retain six months of data in long\-term retention total and 90 days of data in analytics retention, set **Analytics retention** to 90 days and **Total retention** to 180 days.
	* **Data lake tier retention settings**: Set **Retention** to a value between 30 days and 12 years.
	* **Tier changes**: If necessary, you can change tiers at any time based on your cost management and data usage needs.
	
	
	
	Note
	
	
	Tier changes aren't available for all tables. For example, XDR and Microsoft Sentinel solution tables must be available in the analytics tier because Microsoft security services require the data in these tables for near\-real\-time analytics.
5. Review warnings and messages. These messages help you understand important implications of changing table settings.

For example:

	* Increased retention is likely to lead to increased data cost.
	* Changing from the analytics to the data lake tier causes features that rely on analytics data to stop functioning such as:
		+ Alerting
		+ Advanced hunting
		+ Analytics rules
		+ Custom detection rules
6. Select **Save** to apply the new settings.

#### Table support for Basic Logs \& KQL language limits

All tables in your Log Analytics are Analytics tables, by default. You can configure particular tables to use Basic Logs. You can't configure a table for Basic Logs if Azure Monitor relies on that table for specific features.

You can currently configure the following tables for Basic Logs:

* All tables created with the Data Collection Rule (DCR)\-based custom logs API.
* ContainerLogV2, which Container Insights uses and which include verbose text\-based log records.
* AppTraces, which contain freeform log records for application traces in Application Insights.

Queries against Basic Logs are optimized for simple data retrieval using a subset of KQL language, including the following
operators:

* where
* extend
* project
* project\-away
* project\-keep
* project\-rename
* project\-reorder
* parse
* parse\-where

The following KQL isn't supported:

* join
* union
* aggregates (summarize)

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary and resources

You should have learned how the Microsoft Sentinel provisioning process includes creating a Log Analytics workspace and configuring the Microsoft Sentinel options.

You should now be able to:

* Describe Microsoft Sentinel workspace architecture
* Provision a Microsoft Sentinel workspace
* Manage a Microsoft Sentinel workspace

### Learn more

You can learn more by reviewing the following.

[Become a Microsoft Sentinel Ninja](https://techcommunity.microsoft.com/t5/azure-sentinel/become-an-azure-sentinel-ninja-the-complete-level-400-training/ba-p/1246310?azure-portal=true)

[Microsoft Tech Community Security Webinars](https://techcommunity.microsoft.com/t5/microsoft-security-and/security-community-webinars/ba-p/927888?azure-portal=true)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/create-manage-azure-sentinel-workspaces/_

## Fuentes
- [Create and manage Microsoft Sentinel workspaces](https://learn.microsoft.com/en-us/training/modules/create-manage-azure-sentinel-workspaces/?WT.mc_id=api_CatalogApi)
