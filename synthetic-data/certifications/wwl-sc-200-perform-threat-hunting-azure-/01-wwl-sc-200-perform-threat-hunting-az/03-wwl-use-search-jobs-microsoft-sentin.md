# Use Search jobs in Microsoft Sentinel

> Curso: Perform threat hunting in Microsoft Sentinel (wwl-sc-200-perform-threat-hunting-azure-sentinel) · Seccion: Perform threat hunting in Microsoft Sentinel
> Duracion estimada: 15 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

In Microsoft Sentinel, you can search across long time periods in large datasets by using a search job. You also have the option to restore archived logs to include in the search job.

You're a Security Operations Analyst working at a company that implemented Microsoft Sentinel. You discover a new indicator of Compromise (IoC) and need to investigate if it has been previously seen in the logs. You need to restore archive logs and run a search job to discover previous instances of the IoC.

After completing this module, you'll be able to:

* Use Search Jobs in Microsoft Sentinel
* Restore archive logs in Microsoft Sentinel

### Prerequisites

Basic knowledge of operational concepts such as Kusto Query Language (KQL), logging, and archiving

Important

[Microsoft Sentinel is generally available in the Microsoft Defender portal](https://security.microsoft.com), including for customers without Microsoft Defender XDR or an E5 license.

Starting in **July 2026**, all customers using Microsoft Sentinel in the Azure portal will be redirected to the Defender portal and will use Microsoft Sentinel in the Defender portal only. Starting in **July 2025**, many new customers are automatically onboarded and redirected to the Defender portal.

If you're still using Microsoft Sentinel in the Azure portal, we recommend that you start planning your transition to the Defender portal to ensure a smooth transition and take full advantage of the unified security operations experience offered by Microsoft Defender. For more information, see [It’s Time to Move: Retiring Microsoft Sentinel’s Azure portal for greater security](https://techcommunity.microsoft.com/blog/microsoft-security-blog/planning-your-move-to-microsoft-defender-portal-for-all-microsoft-sentinel-custo/4428613).

---

## Hunt with a Search Job

One of the primary activities of a security team is to search logs for specific events. For example, you might search logs for the activities of a specific user within a given time\-frame.

In Microsoft Sentinel, you can search across long time periods in large datasets by using a search job. While you can run a search job on any type of log, search jobs are ideally suited to search archived logs. If you need to do a full investigation on archived data, you can restore that data into the hot cache to run high performing queries and analytics.

### Search large datasets

Use a search job when you start an investigation to find specific events in logs within a given time frame. You can search all your logs to find events that match your criteria and filter through the results.

Search in Microsoft Sentinel is built on top of search jobs. Search jobs are asynchronous queries that fetch records. The results are returned to a search table that's created in your Log Analytics workspace after you start the search job. The search job uses parallel processing to run the search across long time spans, in large datasets. So search jobs don't impact the workspace's performance or availability.

Search results remain in a search results table that has a \***\_SRCH** suffix.

### Supported log types

Use search to find events in any of the following log types:

* Analytics logs (no charges apply)
* Basic logs
* Auxiliary logs

### Limitations of a search job

Before you start a search job, be aware of the following limitations:

* Optimized to query one table at a time.
* Search date range is up to one year.
* Supports long running searches up to a 24\-hour timeout.
* Results are limited to one million records in the record set.
* Concurrent execution is limited to five search jobs per workspace.
* Limited to 100 search results tables per workspace.
* Limited to 100 search job executions per day per workspace.

### Start a search job

Go to Microsoft Sentinel in the Azure portal, or in the Microsoft Defender portal, to enter your search criteria. Depending on the size of the target dataset, search times vary. While most search jobs take a few minutes to complete, searches across massive data sets that run up to 24 hours are also supported.

1. For Microsoft Sentinel in the [Defender portal](https://security.microsoft.com/), select **Microsoft Sentinel** \> **Data lake exploration** \> **Search \& restore**. For Microsoft Sentinel in the [Azure portal](https://portal.azure.com), under **General**, select **Search**.
2. Select the **Table** menu and choose a table for your search.
3. In the **Search** box, enter a search term.

	* [Defender portal](#tabpanel_1_defender-portal)
	* [Azure portal](#tabpanel_1_azure-portal)
4. Enter a **keyword** for your search.

Note

A keyword is a word or phrase that you want to search for in the selected table. You can use operators such as AND, OR, and NOT to refine your search. For example, if you want to search for events related to a specific user, you can enter the user's name as the keyword.
5. Select the **Start** to open the advanced Kusto Query Language (KQL) editor and preview of the results for a set time range.

Note

This opens the advanced KQL editor in the Azure portal.
6. Change the KQL query as needed and select **Run** to get an updated preview of the search results.
7. When you're satisfied with the query and the search results preview, select the ellipses **...** and toggle **Search job mode** on.
8. Specify the search job date range using the **Time range** selector. If your query also specifies a time range, Microsoft Sentinel runs the search job on the union of the time ranges.
9. When you're ready to start the search job, select **Search job**.
10. Enter a new table name to store the search job results.
11. Select **Run a search job**.
12. Wait for the notification **Search job is done** to view the results.

### View search job results

View the status and results of your search job by going to the **Saved Searches** tab.

* [Defender portal](#tabpanel_2_defender-portal)
* [Azure portal](#tabpanel_2_azure-portal)

1. In Microsoft Sentinel in the Defender portal, select **Data lake exploration** \> **Search \& restore**\> **Saved Searches**.
2. On the search card, select **View search results**.
3. This takes you to the Advanced Hunting page with the KQL query prepopulated.
4. Select **Run query** to see all the results that match your original search criteria.
5. To refine the list of results returned from the search table, select **Add filter**.

1. In Microsoft Sentinel, select **Search** \> **Saved Searches**.
2. On the search card, select **View search results**.

By default, you see all the results that match your original search criteria.
3. To refine the list of results returned from the search table, select **Add filter**.
4. As you're reviewing your search job results, select **Add bookmark**, or select the bookmark icon to preserve a row. Adding a bookmark allows you to tag events, add notes, and attach these events to an incident for later reference.
5. Select the **Columns** button and select the checkbox next to columns you'd like to add to the results view.
6. Add the **Bookmarked** filter to only show preserved entries.
7. Select **View all bookmarks** to go the **Hunting** page where you can add a bookmark to an existing incident.

---

## Restore historical data

When you need to do a full investigation on data stored in archived logs, restore a table from the Search page in Microsoft Sentinel. Specify a target table and time range for the data you want to restore. Within a few minutes, the log data is restored and available within the Log Analytics workspace. Then you can use the data in high\-performance queries that support full KQL.

A restored log table is available in a new table that has a \***\_RST** suffix. The restored data is available as long as the underlying source data is available. But you can delete restored tables at any time without deleting the underlying source data. To save costs, we recommend you delete the restored table when you no longer need it.

### Limitations of log restore

Before you start to restore an archived log table, be aware of the following limitations:

* Restore data for a minimum of two days.
* Restore up to 60 TB.
* Restore is limited to one active restore per table.
* Restore up to four archived tables per workspace per week.
* Limited to two concurrent restore jobs per workspace.

Note

Tables with the Auxiliary table plan don't support data restore. Use a search job to retrieve data that's in long\-term retention from an Auxiliary table.

### Restore archived log data

To restore archived log data in Microsoft Sentinel, specify the table and time range for the data you want to restore. Within a few minutes, the log data is available within the Log Analytics workspace. Then you can use the data in high\-performance queries that support full Kusto Query Language (KQL).

Restore archived data directly from search or from a saved search.

1. In the [Defender portal](https://security.microsoft.com/), select **Microsoft Sentinel** \> **Data lake exploration** \> **Search \& restore**. In the [Azure portal](https://portal.azure.com), the **Search** page is listed under **General**.

* [Defender portal](#tabpanel_1_defender-portal)
* [Azure portal](#tabpanel_1_azure-portal)

1. Restore log data using one of the following methods:

	* Select 
	**Restore** at the top of the page. In the **Restoration** pane on the side, select the table and time range you want to restore, and then select **Restore at the bottom of the pane**.
	* Select **Saved searches**, locate the search results you want to restore, and then select **Restore**. If you have multiple tables, select the one you want to restore and then select **Actions \> Restore** in the side pane. For example:
2. Wait for the log data to be restored. View the status of your restoration job by selecting on the **Restoration** tab.

1. Restore log data using one of the following methods:

	* Select 
	**Restore** at the top of the page. In the **Restoration** pane on the side, select the table and time range you want to restore, and then select **Restore at the bottom of the pane**.
	* Select **Saved searches**, locate the search results you want to restore, and then select **Restore**. If you have multiple tables, select the one you want to restore and then select **Actions \> Restore** in the side pane. For example:
2. Wait for the log data to be restored. View the status of your restoration job by selecting on the **Restoration** tab.

### View restored log data

View the status and results of the log data restore by going to the **Restoration** tab. You can view the restored data when the status of the restore job shows **Data Available**.

1. In Microsoft Sentinel, select **Search** \> **Restoration**.
2. When your restore job is complete and the status is updated, select the table name and review the results.

In the [Azure portal](https://portal.azure.com), results are shown in the **Logs** query page. In the [Defender portal](https://security.microsoft.com/), after you select the table name on the **Microsoft Sentinel** \> **Data lake exploration** \> **Search \& restore** \> **Restoration** tab, results are shown in the **Advanced hunting** page.

For example:

The **Time range** is set to a custom time range that uses the start and end times of the restored data.

### Delete restored data tables

To save costs, we recommend you delete the restored table when you no longer need it. When you delete a restored table, the underlying source data isn't deleted.

1. In the [Defender portal](https://security.microsoft.com/), go to **Microsoft Sentinel** \> **Data lake exploration** \> **Search \& restore** \> **Restoration** and identify the table you want to delete.
2. Select **Delete** for that table row to delete the restored table.

For example:

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary and resources

You should have learned how to perform search on large datasets in Microsoft Sentinel.

You should now be able to:

* Create and view a Search Job in Microsoft Sentinel
* Restore archived logs in Microsoft Sentinel

### Learn more

You can learn more by reviewing the following.

[Start an investigation by searching for events in large datasets](/en-us/azure/sentinel/investigate-large-datasets)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/use-search-jobs-microsoft-sentinel/_

## Fuentes
- [Use Search jobs in Microsoft Sentinel](https://learn.microsoft.com/en-us/training/modules/use-search-jobs-microsoft-sentinel/?WT.mc_id=api_CatalogApi)
