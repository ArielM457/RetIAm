# Identify threats with Behavioral Analytics

> Curso: Create detections and perform investigations using Microsoft Sentinel (wwl-sc-200-create-detections-perform-investigation) · Seccion: Create detections and perform investigations using Microsoft Sentinel
> Duracion estimada: 30 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

As Microsoft Sentinel collects logs and alerts from all of its connected data sources, it analyzes them. It builds baseline behavioral profiles of your organization’s entities (users, hosts, IP addresses, applications, etc.).

You're a Security Operations Analyst working at a company that implemented Microsoft Sentinel. The threat hunting team has raised concerns about a specific user account based on discovered threat indicators and needs to see a profile containing historical and related entity data quickly. You have the threat hunting team member navigate to the Entity behavior page to perform further analysis on the account.

By the end of this module, you'll be able to use entity behavior analytics in Microsoft Sentinel to identify threats inside your organization.

After completing this module, you'll be able to:

* Explain Entity Behavior Analytics in Microsoft Sentinel
* Explore entities in Microsoft Sentinel
* Use entity behavior in Analytical rules

### Prerequisites

Knowledge of security incident management in Microsoft Sentinel

---

## Understand behavioral analytics

Identifying threats inside your organization and their potential impact \- whether a compromised entity or a malicious insider \- is a time\-consuming and labor\-intensive process. When you're sifting through alerts, connecting the dots, and actively hunting, it adds up to massive amounts of time and effort expended with minimal returns. And, the possibility of sophisticated threats evading discovery. Elusive threats like zero\-day, targeted, and advanced persistent threats can be the most dangerous to your organization, making their detection all the more critical.

The Entity Behavior capability in Microsoft Sentinel eliminates the drudgery from your analysts’ workloads, and the uncertainty from their efforts. The Entity Behavior capability delivers high\-fidelity and actionable intelligence, so they can focus on investigation and remediation.

As Microsoft Sentinel collects logs and alerts from all the connected data sources, it analyzes and builds baseline behavioral profiles of your organization’s entities (users, hosts, IP addresses, applications, etc.). The analysis is across the time and peer group horizon. Microsoft Sentinel uses various techniques and machine learning capabilities, and can then identify anomalous activity and help you determine if an asset is compromised. Not only that, but it can also figure out the relative sensitivity of particular assets, identify peer groups of assets, and evaluate the potential impact of any given compromised asset (its "blast radius"). Armed with this information, you can effectively prioritize your investigation and incident handling.

#### Architecture overview

#### Security\-driven analytics

Microsoft adopted Gartner’s paradigm for UEBA solutions, Microsoft Sentinel provides an "outside\-in" approach, based on three frames of reference:

**Use cases:** Microsoft Sentinel prioritizes for relevant attack vectors and scenarios based on security research aligned with the MITRE ATT\&CK framework of tactics, techniques, and subtechniques. The prioritization identifies various entities as victims, perpetrators, or pivot points in the kill chain. Microsoft Sentinel focuses specifically on the most valuable logs each data source can provide.

**Data Sources:** While first and foremost supporting Azure data sources, Microsoft Sentinel thoughtfully selects third\-party data sources to provide data that matches our threat scenarios.

**Analytics:** Microsoft Sentinel uses machine learning (ML) algorithms, and identifies anomalous activities that presents evidence clearly and concisely in the form of contextual enrichments. See the examples below.

Microsoft Sentinel presents artifacts that help your security analysts get a clear understanding of anomalous activities in context, and in comparison with the user's baseline profile. Actions performed by a user (or a host, or an address) are evaluated contextually, where a "true" outcome indicates an identified anomaly:

* Across geographical locations, devices, and environments.
* Across time and frequency horizons (compared to user's own history).
* As compared to peers' behavior.
* As compared to organization's behavior.

#### Scoring

Each activity is scored with "Investigation Priority Score". The score determines the probability of a specific user performing a specific activity based on behavioral learning of the user and their peers. Activities identified as the most abnormal receive the highest scores (on a scale of 0\-10\).

---

## Explore entities

When alerts are sent to Microsoft Sentinel, they include data elements that Microsoft Sentinel identifies and classifies as entities, such as user accounts, hosts, IP addresses, and others. On occasion, this identification can be a challenge, if the alert doesn't contain sufficient information about the entity.

For example, user accounts can be identified in more than one way: using a Microsoft Entra account’s numeric identifier (GUID), or its User Principal Name (UPN) value, or alternatively, using a combination of its username and its NT domain name. Different data sources can identify the same user in different ways. Therefore, whenever possible, Microsoft Sentinel merges those identifiers into a single entity, so that it can be properly identified.

It can happen, though, that one of your resource providers creates an alert in which an entity isn't sufficiently identified \- for example, a user name without the domain name context. In such a case, the user entity can't be merged with other instances of the same user account, which would be identified as a separate entity, and those two entities would remain separate instead of unified.

In order to minimize the risk of this happening, you should verify that all of your alert providers properly identify the entities in the alerts they produce. Additionally, synchronizing user account entities with Microsoft Entra ID may create a unifying directory, which is able to merge user account entities.

The following types of entities are currently identified in Microsoft Sentinel:

* User account (Account)
* Host
* IP address (IP)
* Malware
* File
* Process
* Cloud application (CloudApplication)
* Domain name (DNS)
* Azure resource
* File (FileHash)
* Registry key
* Registry value
* Security group
* URL
* IoT device
* Mailbox
* Mail cluster
* Mail message
* Submission mail

#### Entity pages

When you encounter any entity (currently limited to users and hosts) in a search, an alert, or an investigation, you can select the entity and be taken to an **entity page**, a datasheet full of useful information about that entity. The types of information you find on this page include basic facts about the entity, a timeline of notable events related to this entity and insights about the entity's behavior.

Entity pages consist of three parts:

* The left\-side panel contains the entity's identifying information, collected from data sources like Microsoft Entra ID, Azure Monitor, Microsoft Defender for Cloud, and Microsoft Defender XDR.
* The center panel shows a graphical and textual timeline of notable events related to the entity, such as alerts, bookmarks, and activities. Activities are aggregations of notable events from Log Analytics. The queries that detect those activities are developed by Microsoft security research teams.
* The right\-side panel presents behavioral insights on the entity. These insights help to quickly identify anomalies and security threats. The insights are developed by Microsoft security research teams, and are based on anomaly detection models.

#### The timeline

The timeline is a major part of the entity page's contribution to behavior analytics in Microsoft Sentinel. It presents a story about entity\-related events, helping you understand the entity's activity within a specific time frame.

You can choose the **time range** from among several preset options (such as *last 24 hours*), or set it to any custom\-defined time frame. Additionally, you can set filters that limit the information in the timeline to specific types of events or alerts.

The following types of items are included in the timeline:

Alerts \- any alerts in which the entity is defined as a **mapped entity**. If your organization has created [custom alerts using analytics rules](/en-us/azure/sentinel/tutorial-detect-threats-custom?azure-portal=true), you should make sure that the rules' entity mapping is done properly.

Bookmarks \- any bookmarks that include the specific entity shown on the page.

Activities \- aggregation of notable events relating to the entity.

#### Entity Insights

Entity insights are queries defined by Microsoft security researchers to help your analysts investigate more efficiently and effectively. The insights are presented as part of the entity page, and provide valuable security information on hosts and users, in the form of tabular data and charts. Having the information here means you don't have to detour to Log Analytics. The insights include data regarding sign\-ins, Group Additions, Anomalous Events and more, and include advanced ML algorithms to detect anomalous behavior. The insights are based on the following data types:

* Syslog
* SecurityEvent
* Audit Logs
* Sign\-in Logs
* Office Activity
* BehaviorAnalytics (UEBA)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/use-entity-behavior-analytics-azure-sentinel/_

## Fuentes
- [Identify threats with Behavioral Analytics](https://learn.microsoft.com/en-us/training/modules/use-entity-behavior-analytics-azure-sentinel/?WT.mc_id=api_CatalogApi)
