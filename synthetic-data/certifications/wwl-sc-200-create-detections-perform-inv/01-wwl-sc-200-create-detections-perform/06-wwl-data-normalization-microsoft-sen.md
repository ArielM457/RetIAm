# Data normalization in Microsoft Sentinel

> Curso: Create detections and perform investigations using Microsoft Sentinel (wwl-sc-200-create-detections-perform-investigation) · Seccion: Create detections and perform investigations using Microsoft Sentinel
> Duracion estimada: 56 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Data normalization in Microsoft Sentinel allows for the standardization of data across multiple data sources.

You're a Security Operations Analyst working at a company that implemented Microsoft Sentinel. You have multiple connectors that write unstructured firewall data to the CommonSecurityLog table. You need to empower security analysts to easily write analytical rule queries against the firewall data. You need to create an ASIM parser to provide one table for the analysts to query.

By the end of this module, you'll be able to use ASIM parsers to identify threats inside your organization.

After completing this module, you'll be able to:

* Use ASIM Parsers
* Create ASIM Parser
* Create parameterized KQL functions

---

## Understand data normalization

Microsoft Sentinel ingests data from many sources. Working with various data types and tables together requires you to understand each of them, and write and use unique sets of data for analytics rules, workbooks, and hunting queries for each type or schema.

Sometimes, you'll need separate rules, workbooks, and queries, even when data types share common elements, such as firewall devices. Correlating between different types of data during an investigation and hunting can also be challenging.

The Advanced Security Information Model (ASIM) is a layer that is located between these diverse sources and the user. ASIM follows the robustness principle: "Be strict in what you send, be flexible in what you accept". When the robustness principle is used as a design pattern, ASIM transforms Microsoft Sentinel's inconsistent, and hard to use source telemetry to user friendly data.

### Common ASIM usage

ASIM provides a seamless experience for handling various sources in uniform, normalized views, by providing the following functionality:

* **Cross source detection**. Normalized analytics rules work across sources, on\-premises and cloud, and detect attacks such as brute force or impossible travel across systems, including Okta, AWS, and Azure.
* **Source agnostic content**. The coverage of both built\-in and custom content using ASIM automatically expands to any source that supports ASIM, even if the source was added after the content was created. For example, process event analytics support any source that a customer may use to bring in the data, such as Microsoft Defender for Endpoint, Windows Events, and Sysmon.
* **Support for your custom sources**, in built\-in analytics
* **Ease of use**. After an analyst learns ASIM, writing queries is simpler as the field names are always the same.

### ASIM and the Open Source Security Events Metadata

ASIM aligns with the Open Source Security Events Metadata (OSSEM) common information model, allowing for predictable entities correlation across normalized tables.

OSSEM is a community\-led project that focuses primarily on the documentation and standardization of security event logs from diverse data sources and operating systems. The project also provides a Common Information Model (CIM) that can be used for data engineers during data normalization procedures to allow security analysts to query and analyze data across diverse data sources.

### ASIM components

The following image shows how non\-normalized data can be translated into normalized content and used in Microsoft Sentinel. For example, you can start with a custom, product\-specific, non\-normalized table, and use a parser and a normalization schema to convert that table to normalized data. Use your normalized data in both Microsoft and custom analytics, rules, workbooks, queries, and more.

ASIM includes the following components:

| Component | Description |
| --- | --- |
| Normalized schemas | Cover standard sets of predictable event types that you can use when building unified capabilities. Each schema defines the fields that represent an event, a normalized column naming convention, and a standard format for the field values. |
| Parsers | Map existing data to the normalized schemas using KQL functions. Many ASIM parsers are available out of the box with Microsoft Sentinel. More parsers, and versions of the built\-in parsers that can be modified can be deployed from the Microsoft Sentinel GitHub repository. |
| Content for each normalized schema | Includes analytics rules, workbooks, hunting queries, and more. Content for each normalized schema works on any normalized data without the need to create source\-specific content. |
|  |  |

### ASIM terminology

ASIM uses the following terms:

| Term | Description |
| --- | --- |
| Reporting device | The system that sends the records to Microsoft Sentinel. This system may not be the subject system for the record that's being sent. |
| Record | A unit of data sent from the reporting device. A record is often referred to as log, event, or alert, but can also be other types of data. |
| Content, or Content Item | The different, customizable, or user\-created artifacts than can be used with Microsoft Sentinel. Those artifacts include, for example, Analytics rules, Hunting queries and workbooks. A content item is one such artifact. |

### View ASIM Parsers

To view ASIM functions in your Microsoft Sentinel environment.

* Navigate to your Microsoft Sentinel workspace in the Azure portal
* Select Logs from the left navigation
* Expand the schema and filter pane on the left side (if needed use the ellipsis to reveal all the tools)
* Select Functions
* Expand Microsoft Sentinel

You'll see functions starting with ***ASim*** and ***Im***.

---

## Use ASIM Parsers

In Microsoft Sentinel, parsing and normalizing happen at query time. Parsers are built as KQL user\-defined functions that transform data in existing tables, such as CommonSecurityLog, custom logs tables, or Syslog, into the normalized schema.

Users use Advanced Security Information Model (ASIM) parsers instead of table names in their queries to view data in a normalized format, and to include all data relevant to the schema in your query.

### Built\-in ASIM parsers and workspace\-deployed parsers

Many ASIM parsers are built in and available out\-of\-the\-box in every Microsoft Sentinel workspace. ASIM also supports deploying parsers to specific workspaces from GitHub, using an ARM template or manually. Both out\-of\-the\-box and workspace\-deployed parsers are functionally equivalent, but have slightly different naming conventions, allowing both parser sets to coexist in the same Microsoft Sentinel workspace.

Each method has advantages over the other:

| Compare | Built\-in | Workspace\-deployed |
| --- | --- | --- |
| Advantages | Exist in every Microsoft Sentinel instance. Usable with other built\-in content. | New parsers are often delivered first as workspace\-deployed parsers. |
| Disadvantages | Can't be directly modified by users. Fewer parsers available. | Not used by built\-in content. |
| When to use | Use in most cases that you need ASIM parsers. | Use when deploying new parsers, or for parsers not yet available out\-of\-the\-box. |

It's recommended to use built\-in parsers for schemas for which built\-in parsers are available.

### Parser hierarchy

ASIM includes two levels of parsers: unifying parser and source\-specific parsers. The user usually uses the unifying parser for the relevant schema, ensuring all data relevant to the schema is queried. The unifying parser in turn calls source\-specific parsers to perform the actual parsing and normalization, which is specific for each source.

The unifying parser name is **\_Im\_Schema** for built\-in parsers, and **imSchema** for workspace deployed parsers. Where **Schema** stands for the specific schema it serves. Source\-specific parsers can also be used independently. For example, in an Infoblox\-specific workbook, use the **vimDnsInfobloxNIOS** source\-specific parser.

### Unifying parsers

When using ASIM in your queries, use unifying parsers to combine all sources, normalized to the same schema, and query them using normalized fields.

For example, the following query uses the built\-in unifying DNS parser to query DNS events using the ResponseCodeName, SrcIpAddr, and TimeGenerated normalized fields:

```
_Im_Dns(starttime=ago(1d), responsecodename='NXDOMAIN')
| summarize count() by SrcIpAddr, bin(TimeGenerated,15m)

```

The example uses filtering parameters, which improve ASIM performance. The same example without filtering parameters would look like this:

```
_Im_Dns
| where TimeGenerated > ago(1d)
| where ResponseCodeName =~ "NXDOMAIN"
| summarize count() by SrcIpAddr, bin(TimeGenerated,15m)

```

The following table lists key unifying parsers. For the complete current list, see [ASIM parsers overview](/en-us/azure/sentinel/normalization-parsers-overview).

| Schema | Built\-in unifying parser |
| --- | --- |
| Authentication | `_Im_Authentication` |
| Audit Event | `_Im_AuditEvent` |
| DHCP Event | `_Im_Dhcp` |
| DNS | `_Im_Dns` |
| File Event | `_Im_FileEvent` |
| Network Session | `_Im_NetworkSession` |
| Process Event | `_Im_ProcessEvent` |
| Registry Event | `_Im_RegistryEvent` |
| User Management | `_Im_UserManagement` |
| Web Session | `_Im_WebSession` |

### Optimizing parsing using parameters

Using parsers may impact your query performance, primarily from filtering the results after parsing. For this reason, many parsers have optional filtering parameters, which enable you to filter before parsing and enhance query performance. With query optimization and pre\-filtering efforts, ASIM parsers often provide better performance when compared to not using normalization at all.

When invoking the parser, always use available filtering parameters by adding one or more named parameters to ensure optimal performance of the ASIM parsers.

Each schema has a standard set of filtering parameters documented in the relevant schema documentation. Filtering parameters are entirely optional. The following schemas support filtering parameters:

* Authentication
* DNS
* Network Session
* Web Session

Every schema that supports filtering parameters supports at least the starttime and enttime parameters and using them is often critical for optimizing performance.

---

## Understand parameterized KQL functions

When calling KQL functions, you can provide a set of parameters. This is an important concept for building ASIM parsers as it allows you to filter the function results with dynamic values before returning results.

First, navigate to Logs in the Microsoft Sentinel workspace.

The following sample function returns all events in the Azure Activity log since a particular date and that match a particular category.

Start with the following query using hardcoded values. This verifies that the query works as expected.

```
AzureActivity
| where CategoryValue == "Administrative"
| where TimeGenerated > todatetime("2021/04/05 5:40:01.032 PM")

```

Next, replace the hardcoded values with parameter names and then save the function by selecting Save and then Save as function.

```
AzureActivity
| where CategoryValue == CategoryParam
| where TimeGenerated > DateParam

```

Enter Function name as AzureActivityByCategory
Then create two parameters:

| Type | Name | Default value |
| --- | --- | --- |
| string | CategoryParam | "Administrative" |
| datetime | DateParam |  |

Your screen should look like the image below:

Create a new query. Then enter:

```
AzureActivityByCategory("Administrative", todatetime("2021/04/05 5:40:01.032 PM")) 

```

---

## Create an ASIM Parser

Advanced Security Information Model (ASIM) users use unifying parsers instead of table names in their queries, to view data in a normalized format and to include all data relevant to the schema in the query. Unifying parsers, in turn, use source\-specific parsers to handle the specific details of each source.

Microsoft Sentinel provides built\-in, source\-specific parsers for many data sources. You may want to modify, or develop, these source\-specific parsers in the following situations:

When your device provides events that fit an ASIM schema, but a source\-specific parser for your device and the relevant schema isn't available in Microsoft Sentinel.

When ASIM source\-specific parsers are available for your device, but your device sends events in a method or a format different than expected by the ASIM parsers. For example:

Your source device may be configured to send events in a non\-standard way.

Your device may have a different version than the one supported by the ASIM parser.

The events might be collected, modified, and forwarded by an intermediary system.

### Custom parser development process

The following workflow describes the high level steps in developing a custom ASIM, source\-specific parser:

1. Collect sample logs.
2. Identify the schemas or schemas that the events sent from the source represent.
3. Map the source event fields to the identified schema or schemas.
4. Develop one or more ASIM parsers for your source. You'll need to develop a filtering parser and a parameter\-less parser for each schema relevant to the source.
5. Test your parser.
6. Deploy the parsers into your Microsoft Sentinel workspaces.
7. Update the relevant ASIM unifying parser to reference the new custom parser.
8. You might also want to contribute your parsers to the primary ASIM distribution. Contributed parsers may also be made available in all workspaces as built\-in parsers.

#### Collect sample logs

To build effective ASIM parsers, you need a representative set of logs, which in most case will require setting up the source system and connecting it to Microsoft Sentinel. If you don't have the source device available, cloud pay\-as\-you\-go services let you deploy many devices for development and testing.

In addition, finding the vendor documentation and samples for the logs can help accelerate development and reduce mistakes by ensuring broad log format coverage.

A representative set of logs should include:

* Events with different event results.
* Events with different response actions.
* Different formats for username, hostname and IDs, and other fields that require value normalization.

#### Mapping

Before you develop a parser, map the information available in the source event, or events to the schema you identified:

* Map all mandatory fields and preferably also recommended fields.
* Try to map any information available from the source to normalized fields. If not available as part of the selected schema, consider mapping to fields available in other schemas.
* Map values for fields at the source to the normalized values allowed by ASIM. The original value is stored in a separate field, such as EventOriginalResultDetails.

#### Developing parsers

Develop both a filtering and a parameter\-less parser for each relevant schema.

A custom parser is a KQL query developed in the Microsoft Sentinel Logs page. The parser query has three parts:

Filter \> Parse \> Prepare fields

#### Filtering the relevant records

In many cases, a table in Microsoft Sentinel includes multiple types of events. For example:

* The Syslog table has data from multiple sources.
* Custom tables may include information from a single source that provides more than one event type and can fit various schemas.

Therefore, a parser should first filter only the records relevant to the target schema.

Filtering in KQL is done using the **where** operator. For example, **Sysmon event 1** reports process creation, and is therefore normalized to the **ProcessEvent** schema. The **Sysmon event 1** event is part of the **Event** table, so you would use the following filter:

```
Event | where Source == "Microsoft-Windows-Sysmon" and EventID == 1

```

Important

A parser should not filter by time. The query which uses the parser will apply a time range.

#### Filtering by source type using a Watchlist

In some cases, the event itself doesn't contain information that would allow filtering for specific source types.

For example, Infoblox DNS events are sent as Syslog messages, and are hard to distinguish from Syslog messages sent from other sources. In such cases, the parser relies on a list of sources that defines the relevant events. This list is maintained in the ASimSourceType watchlist.

To use the ASimSourceType watchlist in your parsers:

* Include the following line at the beginning of your parser:

```
let Sources_by_SourceType=(sourcetype:string){_GetWatchlist('ASimSourceType') | where SearchKey == tostring(sourcetype) | extend Source=column_ifexists('Source','') | where isnotempty(Source)| distinct Source };

```

* Add a filter that uses the watchlist in the parser filtering section. For example, the Infoblox DNS parser includes the following in the filtering section:

```
| where Computer in (Sources_by_SourceType('InfobloxNIOS'))

```

To use this sample in your parser:

* Replace Computer with the name of the field that includes the source information for your source. You can keep this as Computer for any parsers based on Syslog.
* Replace the InfobloxNIOS token with a value of your choice for your parser. Inform parser users that they must update the ASimSourceType watchlist using your selected value, and the list of sources that send events of this type.

#### Filtering based on parser parameters

When developing filtering parsers, make sure that your parser accepts the filtering parameters for the relevant schema, as documented in the reference article for that schema. Using an existing parser as a starting point ensures that your parser includes the correct function signature. In most cases, the actual filtering code is also similar for filtering parsers for the same schema.

When filtering, make sure that you:

* **Filter before parsing using physical fields**. If the filtered results aren't accurate enough, repeat the test after parsing to fine\-tune your results. For more information, see filtering optimization.
* **Do not filter if the parameter is not defined and still has the default value.**

The following examples show how to implement filtering for a string parameter, where the default value is usually '\*', and for a list parameter, where the default value is usually an empty list.

```
srcipaddr=='*' or ClientIP==srcipaddr
array_length(domain_has_any) == 0 or Name has_any (domain_has_any)

```

#### Filtering optimization

To ensure the performance of the parser, note the following filtering recommendations:

* **Always filter on built\-in rather than parsed fields**. While it's sometimes easier to filter using parsed fields, it dramatically impacts performance.
* **Use operators that provide optimized performance**. In particular, \=\=, has, and startswith. Using operators such as contains or matches regex also dramatically impacts performance.

Filtering recommendations for performance may not always be easy to follow. For example, using has, is less accurate than contains. In other cases, matching the built\-in field, such as SyslogMessage, is less accurate than comparing an extracted field, such as DvcAction. In such cases, we recommend that you still pre\-filter using a performance\-optimizing operator over a built\-in field and repeat the filter using more accurate conditions after parsing.

For an example, see the following Infoblox DNS parser snippet. The parser first checks that the SyslogMessage field has the word client. However, the term might be used in a different place in the message, so after parsing the Log\_Type field, the parser checks again that the word client was indeed the field's value.

```
Syslog | where ProcessName == "named" and SyslogMessage has "client"
…
      | extend Log_Type = tostring(Parser[1]),
      | where Log_Type == "client"

```

#### Parsing

Once the query selects the relevant records, it may need to parse them. Typically, parsing is needed if multiple event fields are conveyed in a single text field.

The KQL operators that perform parsing are listed below, ordered by their performance optimization. The first provides the most optimized performance, while the last provides the least optimized performance.

| Operator | Description |
| --- | --- |
| split | Parse a string of delimited values. |
| parse\_csv | Parse a string of values formatted as a CSV (comma\-separated values) line. |
| parse | Parse multiple values from an arbitrary string using a pattern, which can be a simplified pattern with better performance, or a regular expression. |
| extract\_all | Parse single values from an arbitrary string using a regular expression. extract\_all has a similar performance to parse if the latter uses a regular expression. |
| extract | Extract a single value from an arbitrary string using a regular expression. Using extract provides better performance than parse or extract\_all if a single value is needed. However, using multiple activations of extract over the same source string is less efficient than a single parse or extract\_all and should be avoided. |
| parse\_json | Parse the values in a string formatted as JSON. If only a few values are needed from the JSON, using parse, extract, or extract\_all provides better performance. |
| parse\_xml | Parse the values in a string formatted as XML. If only a few values are needed from the XML, using parse, extract, or extract\_all provides better performance. |

In addition to parsing string, the parsing phase may require more processing of the original values, including:

* **Formatting and type conversion**. The source field, once extracted, may need to be formatted to fit the target schema field. For example, you may need to convert a string representing date and time to a datetime field. Functions such as todatetime and tohex are helpful in these cases.
* **Value lookup**. The value of the source field, once extracted, may need to be mapped to the set of values specified for the target schema field. For example, some sources report numeric DNS response codes, while the schema mandates the more common text response codes. The functions iff and case can be helpful to map a few values.

For example, the Microsoft DNS parser assigns the EventResult field based on the Event ID and Response Code using an iff statement, as follows:

```
extend EventResult = iff(EventId==257 and ResponseCode==0 ,'Success','Failure')

```

For several values, use datatable and lookup, as demonstrated in the same DNS parser:

```
let RCodeTable = datatable(ResponseCode:int,ResponseCodeName:string) [ 0, 'NOERROR', 1, 'FORMERR'....];
...
 | lookup RCodeTable on ResponseCode
 | extend EventResultDetails = case (
 isnotempty(ResponseCodeName), ResponseCodeName,
 ResponseCode between (3841 .. 4095), 'Reserved for Private Use',
 'Unassigned')

```

#### Mapping values

In many cases, the original value extracted needs to be normalized. For example, in ASIM a MAC address uses colons as separator, while the source may send a hyphen delimited MAC address. The primary operator for transforming values is extend, alongside a broad set of KQL string, numerical and date functions, as demonstrated in the Parsing section above.

Use case, iff, and lookup statements when there's a need to map a set of values to the values allowed by the target field.

When each source value maps to a target value, define the mapping using the datatable operator and lookup to map. For example

```
let NetworkProtocolLookup = datatable(Proto:real, NetworkProtocol:string)[
        6, 'TCP',
        17, 'UDP'
   ];
    let DnsResponseCodeLookup=datatable(DnsResponseCode:int,DnsResponseCodeName:string)[
      0,'NOERROR',
      1,'FORMERR',
      2,'SERVFAIL',
      3,'NXDOMAIN',
      ...
   ];
   ...
   | lookup DnsResponseCodeLookup on DnsResponseCode
   | lookup NetworkProtocolLookup on Proto

```

Notice that lookup is useful and efficient also when the mapping has only two possible values.

When the mapping conditions are more complex use the **iff** or **case** functions. The **iff** function enables mapping two values:

```
| extend EventResult = 
      iff(EventId==257 and ResponseCode==0,'Success','Failure’)

```

The **case** function supports more than two target values. The example below shows how to combine **lookup** and **case**. The **lookup** example above returns an empty value in the field DnsResponseCodeName if the lookup value isn't found. The **case** example below augments it by using the result of the **lookup** operation if available, and specifying additional conditions otherwise.

```
| extend DnsResponseCodeName = 
      case (
        DnsResponseCodeName != "", DnsResponseCodeName,
        DnsResponseCode between (3841 .. 4095), 'Reserved for Private Use',
        'Unassigned'
      )

```

#### Prepare fields in the result set

The parser must prepare the fields in the results set to ensure that the normalized fields are used.

The following KQL operators are used to prepare fields in your results set:

| Operator | Description | When to use in a parser |
| --- | --- | --- |
| project\-rename | Renames fields. | If a field exists in the actual event and only needs to be renamed, use project\-rename. The renamed field still behaves like a built\-in field, and operations on the field have much better performance. |
| project\-away | Removes fields. | Use project\-away for specific fields that you want to remove from the result set. We recommend not removing the original fields that aren't normalized from the result set, unless they create confusion or are very large and may have performance implications. |
| project | Selects fields that existed before, or were created as part of the statement, and removes all other fields. | Not recommended for use in a parser, as the parser shouldn't remove any other fields that aren't normalized. If you need to remove specific fields, such as temporary values used during parsing, use project\-away to remove them from the results. |
| extend | Add aliases. | Aside from its role in generating calculated fields, the extend operator is also used to create aliases. |

#### Handle parsing variants

In many cases, events in an event stream include variants that require different parsing logic. To parse different variants in a single parser either use conditional statements such as iff and case, or use a union structure.

To use union to handle multiple variants, create a separate function for each variant, and use the union statement to combine the results:

```
let AzureFirewallNetworkRuleLogs = AzureDiagnostics
    | where Category == "AzureFirewallNetworkRule"
    | where isnotempty(msg_s);
let parseLogs = AzureFirewallNetworkRuleLogs
    | where msg_s has_any("TCP", "UDP")
    | parse-where
        msg_s with           networkProtocol:string 
        " request from "     srcIpAddr:string
        ":"                  srcPortNumber:int
    …
    | project-away msg_s;
let parseLogsWithUrls = AzureFirewallNetworkRuleLogs
    | where msg_s has_all ("Url:","ThreatIntel:")
    | parse-where
        msg_s with           networkProtocol:string 
        " request from "     srcIpAddr:string
        " to "               dstIpAddr:string
    …
union parseLogs,  parseLogsWithUrls…

```

To avoid duplicate events and excessive processing, make sure each function starts by filtering, using native fields, only the events that it's intended to parse. Also, if needed, use project\-away at each branch, before the union.

#### Deploy parsers

Deploy parsers manually by copying them to the Azure Monitor Log page and saving the query as a function. This method is useful for testing. For more information, see Create a function.

To deploy a large number of parsers, we recommend using parser ARM templates, as follows:

1. Create a YAML file based on the relevant template for each schema and include your query in it. Start with the YAML template relevant for your schema and parser type, filtering or parameter\-less.
2. Use the ASIM Yaml to ARM template converter to convert your YAML file to an ARM template.
3. If deploying an update, delete older versions of the functions using the portal or the function delete PowerShell tool.
4. Deploy your template using the Azure portal or PowerShell.

You can also combine multiple templates to a single deploy process using linked templates.

---

## Configure Azure Monitor Data Collection Rules

Another way of normalizing log data is transforming the data at ingestion time. This provides the benefit of storing the data in a parsed format for use in Microsoft Sentinel.

### Data collection rules in Azure Monitor

Data Collection Rules (DCRs) provide an ETL\-like pipeline in Azure Monitor, allowing you to define the way that data coming into Azure Monitor should be handled. Depending on the type of workflow, DCRs may specify where data should be sent and may filter or transform data before storing it in Azure Monitor Logs. Some data collection rules are created by Azure Monitor, while you may create others to customize data collection for your particular requirements.

### Types of data collection rules

Azure Monitor supports several types of data collection rules. Common types include:

* **Standard DCR**. Used with different workflows that send data to Azure Monitor, including the Azure Monitor agent and custom logs ingestion.
* **Workspace transformation DCR**. Used with a Log Analytics workspace to apply ingestion\-time transformations to workflows that don't currently support DCRs directly.

Note

For the current complete list of DCR types and supported workflows, see [Data collection rules in Azure Monitor](/en-us/azure/azure-monitor/essentials/data-collection-rule-overview).

### Transformations

Transformations in a data collection rule (DCR) allow you to filter or modify incoming data before storing it in a Log Analytics workspace. Data transformations are defined using a Kusto Query Language (KQL) statement that is applied individually to each entry in the data source. It must understand the format of the incoming data and create output in the structure of the target table.

#### Transformation structure

The input stream is represented by a virtual table named **source** with columns matching the input data stream definition. Following is a typical example of a transformation. This example includes the following functionality:

* Filters the incoming data with a where statement
* Adds a new column using the extend operator
* Formats the output to match the columns of the target table using the project operator

```
source  
| where severity == "Critical" 
| extend Properties = parse_json(properties)
| project
    TimeGenerated = todatetime(["time"]),
    Category = category,
    StatusDescription = StatusDescription,
    EventName = name,
    EventId = tostring(Properties.EventId)

```

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary and resources

You learned how to normalize and use ASIM Parsers in Microsoft Sentinel.

You should now be able to:

* Use ASIM Parsers
* Create ASIM Parser
* Create parameterized KQL functions

### Learn more

You can learn more by reviewing the following.

[Become a Microsoft Sentinel Ninja](https://techcommunity.microsoft.com/t5/microsoft-sentinel-blog/become-a-microsoft-sentinel-ninja-the-complete-level-400/ba-p/1246310?azure-portal=true)

[Microsoft Tech Community Security Webinars](https://techcommunity.microsoft.com/t5/microsoft-security-and/security-community-webinars/ba-p/927888?azure-portal=true)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/data-normalization-microsoft-sentinel/_

## Fuentes
- [Data normalization in Microsoft Sentinel](https://learn.microsoft.com/en-us/training/modules/data-normalization-microsoft-sentinel/?WT.mc_id=api_CatalogApi)
