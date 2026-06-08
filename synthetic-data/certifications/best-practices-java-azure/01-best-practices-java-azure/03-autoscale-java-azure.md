# Drive higher utilization of your Java apps - autoscaling

> Curso: Best practices for Java apps on Azure (best-practices-java-azure) · Seccion: Best practices for Java apps on Azure
> Duracion estimada: 56 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

### The sample microservice application

In this module, you configure a sample Microservice architecture to be ready for autoscaling. Later, you view the application autoscaling details and learn how to trigger it to scale.

To start, you clone a Git repository and run a script that sets up Azure Spring Apps microservice applications that connect to an Azure Database for MySQL.

Your Azure Spring Apps is set up with autoscaling. This feature allows Azure Spring Apps to respond to changes in the environment by adding or removing instances and balancing the load between them. Autoscaling doesn't have any effect on the CPU power, memory, or storage capacity of the application instances powering the app. It only changes the number of application instances.

The script deploys a well\-known PetClinic microservice application and is built around small independent services, communicating over HTTP via a REST API. The sample is decomposed into four core microservices. All of them are independently deployable, organized by business domains.

* **Customers service**: Contains general user input logic and validation including pets and owners information (Name, Address, City, Telephone).
* **Visits service**: Stores and shows visits information for each pet.
* **Vets service**: Stores and shows Veterinarians' information, including names and specialties.
* **API Gateway**: A single entry point into the system, used to handle requests and route them to an appropriate service, and aggregate the results.

---

## Autoscaling rules

In this unit, we look at autoscaling rule concepts. Then, in the next exercise, we trigger the rules.

### Rules

Autoscaling is based on a set of scale conditions, rules, and limits. A scale condition combines time and a set of scale rules. If the current time falls within the period defined in the scale condition, the condition's scale rules are evaluated. The results of this evaluation determine whether to add or remove instances. The scale condition also defines the limits of scaling for the maximum and minimum number of instances.

Azure Spring Apps autoscaling allows you to scale the number of running instances out or in, based on metrics. The autoscaling rules process these metrics. You can create complex overlapping rules as needed for your situation.

### Autoscale conditions

There are two rule types:

* Metric\-based rules
* Schedule\-based rules

In metric\-based types, the number of apps and resources are horizontally scaled out to the amount necessary to handle the load, without exceeding the maximum limits that you establish. Similarly, the number of apps and resources are horizontally scaled in to the amount necessary to support your load, without falling below the minimums that you set.

In schedule\-based rules, your apps are scaled in and out based on your predefined schedule and limits. This rule type is useful for cases that often follow a predictable pattern, and to establish a baseline for more metric\-based scaling.

You can create multiple autoscale conditions to handle different schedules and metrics. Azure autoscales your service when any of these conditions apply. You can also define a default condition to be used if none of the other conditions are applicable. This condition is always active and doesn't have a schedule.

### Autoscale actions

When an autoscale rule detects that a metric crossed a threshold, it does an autoscale action. An autoscale action can be **scale\-out** or **scale\-in**. A **scale\-out** action increases the number of instances, and a **scale\-in** action reduces the instance count. An autoscale action uses an operator (such as **less than**, **greater than**, **equal to**, and so on) to determine how to react to the threshold. **Scale\-out** actions typically use the **greater than** operator to compare the metric value to the threshold. **Scale\-in** actions tend to compare the metric value to the threshold with the **less than** operator. An autoscale action can also set the instance count to a specific level, rather than incrementing or decrementing the number available.

An autoscale action has a cool\-down period, specified in minutes. During this interval, the scale rule can't be triggered again. This cool\-down period is to allow the system to stabilize between autoscale events. Remember that it takes time to start up or shut down instances, and so any metrics gathered might not show any significant changes for several minutes.

Estimation during a scale\-in is intended to avoid *Flapping* situations, where scale\-in and scale\-out actions continually go back and forth. Keep this behavior in mind when you choose the same thresholds for scale\-out and scale\-in.

---

## Exercise \- Autoscaling rules

In this exercise, we look at exercises for setting up and triggering autoscaling of your sample application.

### Rule exercise

In your sample Azure Spring Apps application, your application triggered a scale\-out action on the customer service microservice when it was created.

The customers\-service app scales **out** when the tomcat request count exceeds 10 sessions, per minute, on average. After the autoscale is triggered, it then scales **in** if the request count is less than or equal to 10 sessions per minute, on average.

### View Autoscale setup in the Azure portal

1. In a new web browser tab, open the Azure portal.
2. From the top search box, search for **Azure Spring Apps**.
3. From the Azure Spring Apps Overview page, select your Azure Spring Apps instance from the results.
4. Select the **Apps** tab under **Settings** in the menu on the left navigation pane.
5. Select the customers\-service application. You should then see the application's **Overview** page.
6. Go to the **Scale\-out** tab under Settings in the menu on the left side of the page.

There are two options for Autoscale demand management:

1. Manual scale: Maintains a fixed instance count. In the Standard tier, you can scale out to a maximum of 500 instances. This value changes the number of separate running instances of the microservice application.
2. Custom autoscale: Scales on any schedule, based on any metrics.

In the Azure portal, view the presetup configuration for your application. The following figure shows a **Custom** autoscale configured to scale on the tomcat request count.

#### Viewing the finished autoscale events

In the Scale out setting screen, go to the **Run history** tab to see the most recent scale actions. The tab shows the change in Observed Capacity over time graphically, and a log of every autoscale action.

### Trigger the scale\-out action with a script

You can also trigger autoscaling manually via a web browser or a shell script.

To test the autoscale rules, we generate some load on the instances. This simulated load causes the autoscale rules to scale out and increase the number of instances. As the simulated load is then stopped, the autoscale rules scale\-in and reduce the number of instances.

To allow you to trigger the autoscale, we provided a shell script in the same GIT repo you used to create your Azure Spring Apps application.

1. Set the instance name of your Spring Apps service, by running the following command in your <https://shell.azure.com> bash window. Use the same Azure spring Apps service name you used in the previous exercise:

```
export SPRING_APPS_SERVICE=<spring-apps-instance-name>

```
2. Next, in the bash window, run the following commands to execute transactions against your Spring Apps *customers\-service* microservice:

```
cd mslearn-autoscale-java
sh loadTest.sh

```
3. You should see the output of the *customers\-service* load test that sends 100 requests to your instance.

### Trigger the scale\-out action manually via a web browser (Optional)

To manually trigger the scale\-out condition in the autoscale setting created, the *customers\-service* microservice must have more than 10 requests in less than one minute.

1. Open a new browser window and navigate to the *customers\-service* microservice:

```
https://<your-spring-apps-service>-api-gateway.azuremicroservices.io/api/customer/owners

```
2. In quick succession, reload the page more than 10 times.

### Viewing the scale\-out action

1. Back in the original browser window, on the autoscale setting, select the **Run history** tab.
2. You should see a chart reflecting the instance count.
3. In a few minutes, the instance count should rise from 1 to 2\.
4. Under the chart, you should have the activity log entries for each scale action taken by this autoscale setting.

### Scale\-in action

The scale\-in condition in the autoscale setting triggers if there are fewer than or equal to 10 requests to the *customers\-service* microservice over a period of one minute.

1. Ensure that no requests are being sent to your *customers\-service* microservice and the browser window to your app/service is closed.
2. Observe the instance count. In a few minutes, the instance count *could* fall from 2 to 1 (see the following important point).

Important

Your Azure Spring Apps might not scale, because autoscale will try to estimate what the final state will be after it's scaled. This means autoscale would have to immediately scale again, if the average tomcat request count remains the same or even falls only a small amount.

---

## Autoscaling monitoring

In this unit, we look at autoscale monitoring concepts.

### Monitoring

Similar to other Azure resources, Azure Spring Apps autoscale actions create logs. There are two categories of logs it can create:

* **Autoscale Evaluations**: The autoscale engine records log entries for every single condition evaluation every time it does a check. The entry includes details on the observed values of the metrics, the rules evaluated, and if the evaluation resulted in a scale action or not.
* **Autoscale Scale Actions**: The engine records scale action events started by the autoscale service and the results of those scales actions (success, failure, and how much scaling occurred as seen by the autoscale service).

### Understanding autoscale events

In the autoscale setting screen, you can go to the **Run history** tab to see the most recent scale actions. The tab also shows the change in Observed Capacity over time. It also shows more details about all autoscale actions, including operations such as updating and deleting autoscale settings. The **Setting** screen also shows you the activity log and allows you to filter by autoscale operations.

Autoscale posts to the Activity Log if any of the following conditions occur:

* Autoscale issues a scale operation.
* Autoscale service successfully completes a scale action.
* Autoscale service fails to take a scale action.
* Autoscale detects flapping and aborts the scale attempt. You see a log type of `Flapping` in this situation. If you see `Flapping`, consider whether your thresholds are too narrow.
* Autoscale detects flapping, but is still able to successfully scale. You see a log type of `FlappingOccurred` in this situation. If you see `FlappingOccurred`, the autoscale engine attempted to scale (for example, from four instances to two), but determined that this action would cause flapping. Instead, the autoscale engine scaled to a different number of instances (for example, using three instances instead of two), which no longer causes flapping, so it scaled to this number of instances.

### Monitor the application's autoscale with Log Analytics

As with any Azure Monitor supported service, you can use Diagnostic Settings to route these logs:

* To your Azure Log Analytics workspace for detailed analytics.
* To Azure Event Hubs and then to non\-Azure tools.
* To your Azure storage account, for archiving.

You can validate the evaluations and scale actions better using Log Analytics. In your sample application, we routed your autoscale logs to Azure Monitor Logs (Log Analytics) through a workspace when you created the autoscale setting.

Data is retrieved from a Log Analytics workspace using a log query, which is a read\-only request to process data and return results. Log queries are written in **Kusto Query Language (KQL)**, which is the same query language used by Azure Data Explorer.

Note

For more information on **KQL** syntax, see the Summary unit at the end of this module.

In the next exercise, you'll use log analytics to find out more about the autoscale events.

---

## Exercise \- Autoscaling monitoring

In this exercise, you use log analytics to query autoscaling events for your sample application.

### Monitor the application's autoscale with Log Analytics

You can validate the evaluations and scale actions better using Log Analytics. In your sample application, we routed your autoscale logs to Azure Monitor Logs (Log Analytics) through a Log Analytics workspace you created with your sample application setup.

Important

The Log data ingestion time in Azure Monitor can take up to 15 minutes. If you don't find data in Log Analytics, it may take additional time to ingest Azure Spring Apps log data.

### Understanding autoscale events

In the autoscale setting screen, go to the **Run history** tab to see the most recent scale actions.

The tab also shows the change in Observed Capacity over time. To find more details about all autoscale actions including operations such as update/delete autoscale settings, view the activity log and filter by autoscale operations.

Next, we use log analytics to dig deeper into the autoscale events.

### Use Log Analytics to troubleshoot scale events

1. In the Azure portal, open the Log Analytics workspace in your resource group. This step sets the initial scope to a Log Analytics workspace, so that your query selects from all data in that workspace. If you select Logs from an Azure resource's menu, the scope is set to only records from that resource.
2. On the left menu, select **Logs**.

The left side of the screen includes the **Tables** tab, where you can inspect the tables that are available in the current scope.

Expand the Log Management solution and locate the **AutoscaleEvaluationsLog** table. You can expand the table to view its schema, or hover over its name to show more information about it.

### Write a Kusto query

Let's write a query by using the **AutoscaleEvaluationsLog** table. Double\-click its name to add it to the query window. You can also type directly in the window. You can even get IntelliSense that helps complete the names of tables in the current scope and Kusto Query Language (KQL) commands.

This query is the simplest query that we can write. It just returns all the records in a table. Run it by selecting the **Run** button or by pressing `Shift + Enter` on your keyboard with the cursor positioned anywhere in the query text.

```
AutoscaleEvaluationsLog

```

The number of records that the query returned appears in the lower\-right corner. For more exercises on KQL autoscale queries, see the Summary unit at the end of this module.

---

## Common autoscaling patterns

In this unit, we look at patterns for autoscaling.

Autoscaling isn't an instant solution. Simply adding resources to a system or running more instances of a process doesn't guarantee improved performance for the system. Consider the following points when designing an autoscaling strategy:

### Recommendations

**Identify bottlenecks**: Scaling out isn't a magic fix for every performance issue. For example, if your backend database is the bottleneck, it doesn't help to add more web servers. Identify and resolve the bottlenecks in the system before throwing more instances at the problem. Stateful parts of the system are the most likely cause of bottlenecks.

**Decompose workloads by scalability requirements**: Applications often consist of multiple workloads with different requirements for scaling. For example, an application might have a public\-facing site and a separate administration site. The public site might experience sudden surges in traffic, while the administration site has a smaller, more predictable load.

**Offload resource\-intensive tasks**: Tasks that require many CPU or I/O resources should be moved to background jobs when possible. Offloading tasks minimizes the load on the front end that's handling user requests.

**Use built\-in autoscaling features**: If the application has a predictable, regular workload, scale out on a schedule. For example, scale out during business hours. Otherwise, if the workload isn't predictable, use performance metrics such as CPU or request queue length to trigger autoscaling.

**Consider aggressive autoscaling for critical workloads**: For critical workloads, you want to keep ahead of demand. It's better to add new instances quickly under heavy load to handle the other traffic, and then gradually scale back.

**Design for scale in**: Remember that with elastic scale, the application has periods of scale in, when instances get removed. The application must gracefully handle instances being removed. Here are some ways to handle scale\-in:

* Listen for shutdown events when they're available and shut down cleanly.
* Support transient fault handling and retry.
* Consider breaking up the work for long\-running tasks.
* Put work items on a queue so that another instance can pick up the work if an instance is removed in the middle of processing.

### Notifications

* All autoscale failures are logged to the Activity Log. You can then configure an activity\-log alert that notifies you via email, Short Message Service (SMS), or webhooks whenever there's an autoscale failure.
* Similarly, all successful scale actions are posted to the Activity Log. You can then configure an activity\-log alert so that you can be notified via email, SMS, or webhooks whenever there's a successful autoscale action. You can also configure email or webhook notifications to get notified for successful scale actions via the **Notifications** tab on the autoscale setting.

### Common patterns to scale your resource in Azure

#### Scale based on demand

You can automatically scale out the number of service instances at the start of the work day when customer demand increases. At the end of the work day, automatically scale in the number of application instances to minimize resource costs overnight when application use is low.

#### Scale differently on weekdays vs weekends

On an evening or weekend, you might have lower application demand. If this load is consistent over a period of time, you can configure autoscale rules to lower the number of service instances in the scale set. Taking this scale\-in action reduces the cost to run your scale set because you only run the number of instances required to meet the current demand.

#### Scale differently during holidays

If you have heavy usage for a service at certain parts of the month or fiscal cycle, you can automatically scale the number of service instances to accommodate their extra demands. When there's a marketing event, promotion, or holiday sale, you can automatically scale the number of service instances ahead of expected customer demand.

#### Scale based on custom metric

Finally, it's best to define your autoscaling rules carefully. For example, a Denial of Service (DoS) attack is likely to result in a large\-scale influx of incoming traffic. Trying to handle a surge in requests caused by a DoS attack would be fruitless and expensive. These requests aren't genuine, and should be discarded rather than processed. A better solution is to implement detection and filtering of requests that occur during such an attack before they reach your service.

After configuring the autoscaling rules, monitor the performance of your application over time. Use the results of this monitoring to adjust the pattern in which the system scales, if necessary.

---

## Summary

Congratulations! You learned about autoscaling for your Java applications on Azure.

### Summary of what you learned

In this module, you learned about:

* Creating a Sample Autoscale architecture with Azure Spring Apps.
* Investigating the sample scale rules.
* Triggering scale actions.
* Best practices for scaling Java applications on Azure.

### Clean up your Azure resources

In the preceding processes, you created Azure resources. If you don't expect to need these resources in the future, delete the resource group by running the following commands in Azure Cloud Shell:

```
az group delete --name <your Resource Group Name> --yes

```

#### Delete your log analytics workspace

When you delete your resource group, you soft delete your Azure Log Analytics workspace. When soft deleting an Azure Log Analytics workspace, it gets into a soft\-delete state to allow its recovery, including data and connected agents, within 14 days. If you wish to rerun the setup script and re\-create your resources, either create a new workspace with a new name or use the following command to permanently delete the old workspace:

```
az monitor log-analytics workspace delete --force true --resource-group <your Resource Group Name> --workspace-name <your log analytics workspace name>

```

### References

* [Autoscale in Azure](/en-us/azure/azure-monitor/platform/autoscale-get-started?WT.mc_id=java-00000-ropreddy)
* [Azure Spring Apps Availability by Region](https://azure.microsoft.com/global-infrastructure/services/)
* [Azure Spring Apps locations and pricing](https://azure.microsoft.com/pricing/details/spring-cloud?WT.mc_id=java-00000-ropreddy)
* [Azure Database for MySQL pricing](https://azure.microsoft.com/pricing/details/mysql/server?WT.mc_id=java-00000-ropreddy)
* [Kusto Query Language (KQL) syntax](/en-us/azure/data-explorer/kql-quick-reference?WT.mc_id=java-00000-ropreddy)
* [Azure for Java developers](/en-us/azure/developer/java?WT.mc_id=java-00000-ropreddy)
* [Azure Quickstart Templates \- Create an Activity Log Alert to monitor all autoscale engine operations on your subscription](https://github.com/Azure/azure-quickstart-templates/tree/master/demos/monitor-autoscale-alert)
* [Azure Quickstart Templates \- Create an Activity Log Alert to monitor all failed autoscale scale in/scale out operations on your subscription](https://github.com/Azure/azure-quickstart-templates/tree/master/demos/monitor-autoscale-failed-alert).
* [Azure Monitor autoscale troubleshooting](/en-us/azure/azure-monitor/autoscale/autoscale-troubleshoot?WT.mc_id=java-00000-ropreddy)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/autoscale-java-azure/_

## Fuentes
- [Drive higher utilization of your Java apps - autoscaling](https://learn.microsoft.com/en-us/training/modules/autoscale-java-azure/?WT.mc_id=api_CatalogApi)
