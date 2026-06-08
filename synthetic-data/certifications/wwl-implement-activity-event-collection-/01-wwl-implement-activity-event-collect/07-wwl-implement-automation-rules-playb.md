# Implement automation rules and playbooks in Microsoft Sentinel

> Curso: Implement activity and event collection in Microsoft Sentinel (wwl-implement-activity-event-collection-sentinel) · Seccion: Implement activity and event collection in Microsoft Sentinel
> Duracion estimada: 31 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Financial Services spent three months building a Microsoft Sentinel workspace and connecting data sources across their hybrid infrastructure. Events are flowing in from Azure Activity logs, Linux trading platforms, and Windows servers—the SOC finally has visibility. What they're discovering now is a problem familiar to every growing operations team: the data is there, but the volume of incidents is outpacing the team's capacity to triage them manually.

Analysts are spending 40% of their shift on repetitive, low\-judgment tasks—assigning incidents to the right team, suppressing known\-benign alerts during maintenance windows, and copying incident details into their ticketing system. High\-severity alerts from the trading platform sit unacknowledged while the team clears a backlog of informational events. The analyst shortage isn't a people problem; it's a workflow problem.

Microsoft Sentinel addresses this with two automation layers designed to work together. Automation rules handle the lightweight, no\-code tier: tagging incidents by category, assigning them to the right owner, suppressing noise during known maintenance windows, and closing incidents that match established benign patterns—all without running a workflow engine. Playbooks, built on Azure Logic Apps, handle everything that requires more: querying external threat intelligence APIs, calling the Defender for Endpoint isolation API, posting adaptive notification cards to Teams, and synchronizing incident status with external ticketing systems.

By the end of this module, you'll create automation rules that take over Contoso's incident triage layer, activate a prebuilt notification playbook from Content Hub, and author a custom Logic Apps playbook that gives the SOC a reusable, version\-controlled response workflow they can extend as their environment grows.

### Learning objectives

After completing this module, you'll be able to:

* Explain the difference between automation rules and playbooks in Microsoft Sentinel.
* Create automation rules to automate incident management tasks.
* Configure and activate a prebuilt playbook from the Microsoft Sentinel Content Hub.
* Author a custom Logic Apps playbook and connect it to an automation rule.

---

## Understand Microsoft Sentinel automation options

Contoso Financial Services' SOC handles roughly 200 incidents per week. Most require the same initial steps: assign the incident to the right team, add a category tag, and check whether the source analytics rule tends toward false positives. These steps don't require judgment—they require consistency. The two problems aren't complexity or ambiguity; they problems are repetition and latency. Microsoft Sentinel addresses both through two automation layers that you choose between based on what the response actually requires.

### Distinguish automation rules from playbooks

**Automation rules** are Microsoft Sentinel's native, no\-code incident management layer. They run entirely inside Microsoft Sentinel without invoking an external workflow engine, which makes them fast and easy to audit. An automation rule evaluates a set of conditions against an incident when it's created or updated, then executes a sequence of actions from a fixed set: assign an owner, change severity, add a tag, add a comment, assign analyst tasks, suppress the incident, close it, or run a playbook. You configure automation rules once in the **Automation** page of the Microsoft Defender portal, and they apply automatically to every matching incident.

**Playbooks** are Azure Logic Apps workflows that use the Microsoft Sentinel connector to interact with your workspace. Unlike automation rules—which only take actions built into Microsoft Sentinel—playbooks reach outside the Microsoft Sentinel environment. A playbook can query a threat intelligence API, call the Microsoft Defender for Endpoint isolation endpoint, post an adaptive card to Teams, or write a record to an external ticketing system. Playbooks run when triggered by a Microsoft Sentinel incident or alert, either automatically through an automation rule or manually from an incident's action menu.

The key distinction is scope. Automation rules manage incidents *within* Microsoft Sentinel. Playbooks extend the response *beyond* Microsoft Sentinel into connected services and external systems.

Note

When your Microsoft Sentinel workspace is onboarded to the Defender portal, incident creation is managed by Defender Extended Detection and Response (XDR). In this configuration, disable incident creation in your Microsoft Sentinel analytics rules to avoid duplicate incidents. Incident\-triggered playbooks still work correctly—you trigger them through automation rules rather than through the analytics rule directly.

### Identify when to use automation rules

Automation rules are the right choice when the response is one of Microsoft Sentinel's built\-in operations and doesn't require external API calls or conditional branching. Common scenarios for Contoso include:

* **Routing by source**: Automatically assign all incidents from the trading platform analytics rules to the trading security team owner.
* **Suppressing known noise**: Close incidents from a specific analytics rule that consistently produces false positives during a scheduled maintenance window. The rule's expiration setting re\-enables it automatically when the window ends.
* **Standardizing tags**: Add a "PCI\-in\-scope" tag to every incident involving a cardholder data environment system, so the compliance team's incident filter always returns complete results.
* **Triggering a playbook**: Run a Logic Apps playbook as one action within the automation rule, combining Sentinel\-native steps with external integration steps in a single coordinated flow.

Automation rules evaluate in priority order. If multiple rules match the same incident, they execute in sequence from lowest to highest priority number, giving you control over exactly which actions run first.

### Identify when to use playbooks

Playbooks are the right choice when the response workflow requires any of the following:

* calling an external API
* making a decision based on data retrieved at runtime
* performing actions across multiple connected services
* building a response pattern that needs version control and reusability

Contoso's security team identified three playbook use cases during their automation planning session:

* **Incident enrichment**: When a high\-severity incident is created, a playbook queries a threat intelligence service for each IP entity in the incident, then adds the reputation score as a comment before the analyst opens the case.
* **Machine isolation**: If a confirmed malware incident includes a named host entity, the playbook calls the Defender for Endpoint API to isolate the machine, then posts a Teams message to the on\-call analyst with the incident URL.
* **Compliance notification**: When a SharePoint audit alert triggers a Microsoft Sentinel incident, the playbook posts a formatted incident summary to the compliance team's Teams channel and creates a record in Contoso's external compliance tracking system.

None of these workflows are possible with automation rules alone—they all require external API calls or runtime data retrieval.

For Logic Apps plan selection, use the **Consumption plan** for most Microsoft Sentinel playbooks. Consumption plan Logic App is event\-driven, cost nothing when idle, and integrate directly with the Microsoft Sentinel connector.

### Combine both tiers into a unified response workflow

You don't have to choose one tier exclusively. The most effective Microsoft Sentinel automation architecture combines both: an automation rule handles the immediate, no\-code steps the moment an incident is created, then triggers a playbook for the steps that require external integration.

For Contoso's high\-severity trading platform incidents, the workflow looks like this. An automation rule fires immediately when the incident is created, assigns it to the trading security team, adds the "trading\-platform" and "PCI\-in\-scope" tags, and triggers the enrichment playbook. The playbook runs asynchronously—querying threat intelligence, posting the enriched summary to Teams, and adding a comment to the incident. By the time an analyst opens the case, it's already tagged, assigned, enriched, and notified.

---

## Create automation rules in Microsoft Sentinel

Before you build your first automation rule, take a few minutes to map the incident patterns that your SOC handles repeatedly. For Contoso, the most obvious candidates are incidents from the trading platform analytics rules (always routed to the same team), informational incidents during the nightly batch maintenance window (always suppressed), and any incident involving a host in the cardholder data environment (always tagged for compliance). Identifying these patterns first means you build rules with clear intent rather than discovering gaps after the first deployment.

### Plan your automation rule strategy

Before opening the rule wizard, answer these questions:

* **What is the trigger?** Most incident management rules use the **Incident created** trigger. Use **Incident updated** when you need to react to status changes, such as reassigning an incident when escalated from low to high severity.
* **How specific should the conditions be?** A rule scoped to a single analytics rule by name is precise but requires updates when you rename that rule. A rule scoped to a severity level is broad but durable. Combine both for the right balance.
* **What actions run, and in what order?** Actions within a single rule execute in the order you define them. Put the assign action before the tag action if you want the assignee to already be set when the notification fires.
* **What priority number should this rule have?** Lower numbers run first. If two rules match the same incident, the lower\-priority rule's actions complete before the higher one runs. Reserve the lowest numbers (1–10\) for critical suppression or escalation rules.

### Create an automation rule in Microsoft Sentinel

To create an automation rule:

1. In the Microsoft Defender portal, select **Microsoft Sentinel**, then select **Automation** from the left navigation.
2. Select **Create**, then select **Automation rule**.
3. Enter a descriptive rule name. A consistent naming convention helps—for example, `ROUTE-TradingPlatform-HighSeverity` or `SUPPRESS-MaintenanceWindow-Informational`.
4. Under **Trigger**, select **Incident created**.
5. Under **Conditions**, select **Add condition**. Select **Analytics rule name**, set the operator to **Contains**, and enter the name of the trading platform analytics rule. Select **Add condition** again, set **Incident severity** to **Equals**, and select **High** and **Medium**.
6. Under **Actions**, select **Add action**. Select **Assign owner** and choose the trading security team account. Select **Add action** again, select **Add tags**, and enter `trading-platform` and `PCI-in-scope`.
7. Set **Order** to `10` to give this rule a defined priority among your automation rules.
8. Leave **Expiration** empty for a permanent rule, or set a date for time\-limited suppression scenarios.
9. Verify the rule is set to **Enabled**, then select **Apply**.

### Configure conditions to target specific incidents

Conditions support **AND** logic by default—all conditions must be true for the rule to fire. This is the right model for most routing and tagging rules, where you want both the right analytics rule *and* the right severity before taking action.

The condition field options give you several ways to target incidents precisely:

* **Analytics rule name**: Match by exact name or partial string using the **Contains** operator. Use this to scope a rule to a specific detection without editing every time you add a new rule to the same analytics rule.
* **Incident title**: The **Contains** operator works here for title patterns like "impossible travel" or "malware detected."
* **Severity**: Useful for escalation rules—for example, automatically assigning any critical\-severity incident to a senior analyst regardless of source.
* **Tactics**: Scope a rule to all incidents tagged with a specific MITRE ATT\&CK tactic, such as Initial Access or Exfiltration, to apply consistent handling to an entire category of threats.

### Monitor and manage your automation rules

The **Automation** page lists all your rules with their current status, trigger type, and a run count showing how many times each rule executed. Select any rule to view its configuration, edit conditions or actions, change the priority order, or disable the rule without deleting it.

When a rule isn't triggering as expected, check the conditions first. A common issue is an analytics rule name condition that uses an exact match rather than **Contains**, which fails silently when the rule name changes slightly. If two rules conflict—one closing an incident that another rule should be tagging—check the priority numbers and verify that the lower\-priority rule isn't consuming the incident before the tag rule runs.

For audit purposes, every automation rule execution is logged in the Microsoft Sentinel audit log, available in the **Logs** page under the `SentinelAudit` table. This gives you a complete, queryable record of every automated action taken on every incident—essential for demonstrating process controls during a PCI or SOX audit review.

---

## Configure and activate a Content Hub playbook

Before you build a custom playbook from scratch, check the Content Hub. Microsoft and partners publish hundreds of prebuilt Logic Apps playbook templates as part of Microsoft Sentinel solutions—covering common scenarios like incident notifications, account disabling, IP blocking, and ticket synchronization. For many response workflows, a Content Hub playbook gets you to a working, tested solution in under 30 minutes, with no Logic Apps authoring required.

### Find playbook solutions in the Content Hub

In the Microsoft Defender portal, select **Microsoft Sentinel**, then select **Content hub** under **Content management**. To filter for playbooks, select **Content type** in the filter panel and choose **Playbook**.

Each solution card shows the solution name, publisher, and the types of content it includes. Select a solution card to open the details pane, which lists every content item the solution contains—including how many playbooks, analytics rules, workbooks, and data connectors come with it. For the Contoso SOC notification use case is search for "Microsoft Sentinel Incidents" or "Teams notification" to find solutions that include incident notification playbooks.

When you identify a solution that fits your scenario, review the permissions documentation in the details pane before installing. Most playbook solutions require you to create API connections during or after deployment—for example, a Teams connection authenticated with a service account or a managed identity.

### Deploy a Content Hub playbook to your subscription

To install a playbook solution:

1. In the solution details pane, select **Install** (or **Update** if a newer version is available).
2. On the **Basics** tab, select your **Subscription**, **Resource group**, and **Workspace**. The Logic App resource deploys to the resource group you select.
3. On the subsequent tabs, review the playbook components. Some solutions prompt you to configure settings—such as the Teams channel ID or email recipient—during deployment. Enter the values specific to Contoso's environment.
4. On the **Review \+ create** tab, wait for **Validation passed**, then select **Create**.

Deployment takes one to three minutes. When it completes, navigate to the resource group in the Azure portal to confirm the Logic App resource is present.

### Grant the playbook access to Microsoft Sentinel

For a playbook to interact with Microsoft Sentinel—reading incident data, posting comments, or updating status—its identity needs permission to do so. A Logic App uses a **managed identity** for this purpose.

To assign the required role:

1. In the Azure portal, navigate to the resource group that contains your Microsoft Sentinel workspace.
2. Select **Access control (IAM)**, then select **Add role assignment**.
3. In the **Role** tab, search for and select **Microsoft Sentinel Responder**. This role grants the minimum permissions a playbook needs: read incidents, post comments, and update incident status.
4. In the **Members** tab, set **Assign access to** to **Managed identity**, then select **\+ Select members**. Find the Logic App by name, select it, and confirm.
5. Select **Review \+ assign**.

Important

If you skip this step, the playbook fails with a 401 Unauthorized error every time it tries to call the Microsoft Sentinel connector. You can diagnose this by selecting the Logic App in the Azure portal, opening **Run history**, and selecting a failed run to view the error detail on the Microsoft Sentinel connector action.

This same managed identity and role assignment pattern applies beyond playbooks. When an autonomous AI agent—such as an agent built on Azure AI Foundry—needs programmatic access to Microsoft Sentinel to read incidents, add comments, or update status, you assign the same Microsoft Sentinel Responder role to the agent's managed identity on the same workspace. The identity model is identical whether the caller is a Logic Apps playbook or an AI\-powered automation agent.

### Activate the playbook and test the response flow

With the Logic App deployed and authorized, connect it to an automation rule:

1. In the Microsoft Defender portal, select **Automation**, then select **Create** \> **Automation rule**.
2. Configure the trigger and conditions for when the playbook should run—for example, **Incident created**, severity **High**.
3. Under **Actions**, select **Add action**, then select **Run playbook**. Select the playbook you deployed from the list.
4. Select **Apply** to save the rule.

To test, create a test incident manually or wait for a real incident that matches the rule conditions. Once triggered, navigate to **Microsoft Sentinel** \> **Automation** \> the playbook name, and select **Run history** to confirm the playbook executed. Select the run record to view each action's input, output, and duration. A successful run shows green checkmarks on every action. If any action failed, the run record shows the exact error and the input that caused it—making diagnosis straightforward even for complex multi\-step playbooks.

---

## Author a custom playbook with Azure Logic Apps

Content Hub playbooks cover many common scenarios, but Contoso's SOC has a specific requirement that no prebuilt template addresses: when a high\-severity incident is created, post a formatted Teams notification to the security operations channel that includes the incident title, severity, entity list, and a direct link to the incident in the Defender portal—all within 60 seconds of incident creation. Building this from scratch takes about 20 minutes in the Logic Apps Designer, produces a reusable template your team can extend, and gives you hands\-on familiarity with the Microsoft Sentinel connector.

### Design your playbook before building

Two trigger types are available for Microsoft Sentinel playbooks: the **Incident trigger** and the **Alert trigger**. Use the incident trigger for nearly all response playbooks. Incidents are Microsoft Sentinel's primary investigation unit—they contain grouped alerts, entity lists, comments, and status. The incident trigger provides all of that as structured input to your workflow.

The alert trigger is useful in one specific scenario: when you disable incident creation in your analytics rules (which is required when Microsoft Sentinel is onboarded to the Defender portal, to avoid duplicate incidents from Defender XDR). In that case, an alert\-triggered playbook can still run response logic against individual alerts before they're grouped into an incident.

For the Contoso Teams notification playbook, the incident trigger is the right choice. The notification needs the incident title, severity, and entity list—all of which the incident trigger surfaces as dynamic content in Logic Apps.

### Build a Logic App with the Microsoft Sentinel incident trigger

To create the Logic App:

1. In the Azure portal, search for **Logic Apps** and select **Create**.
2. Select **Consumption** as the plan type. Enter a name—for example, `sentinel-teams-incident-notify` \- and select the same subscription and resource group as your Microsoft Sentinel workspace.
3. Select **Review \+ create**, then **Create**. When deployment completes, select **Go to resource**.
4. In the Logic App resource, select **Logic app designer** under **Development tools**.
5. Select **Blank Logic App** to start from scratch.
6. In the search box, search for **Microsoft Sentinel**. Select **Microsoft Sentinel** under **Triggers**, then select **When a Microsoft Sentinel incident is created**.
7. Select **Sign in** and authenticate using your account. If your organization uses managed identity, switch the connection to **Managed Identity** in the connection settings.

The trigger is now configured. Every time an incident is created in your Microsoft Sentinel workspace, this Logic App receives the incident details as a structured JSON object.

### Add enrichment and notification actions

With the trigger in place, add the actions that retrieve incident data and post the notification:

1. Select **\+ New step**. Search for **Microsoft Sentinel** and select **Get incident**. In the **Incident ARM ID** field, select the dynamic content icon and choose **Incident ARM ID** from the trigger output. This action retrieves the full incident object, including the entity list.
2. Select **\+ New step**. Search for **Microsoft Teams** and select **Post message in a chat or channel**.
3. Select **Channel** as the message destination. Enter your Teams team and channel.
4. In the **Message** field, build the notification content using dynamic content from both the trigger and the **Get incident** action:

```
New Sentinel Incident
Title: [Incident Title]
Severity: [Incident Severity]
Status: [Incident Status]
Created: [Incident Created Time]

View incident: [Incident URL]

```

Replace each bracketed item by selecting the corresponding field from the dynamic content panel. Use **Incident Title**, **Incident Severity**, **Incident Status**, **Incident Created Time UTC**, and **Incident URL** from the trigger output.
5. Select **Save** in the toolbar.

Note

If the Teams connector's dynamic content fields don't appear, check that the Teams connection is authenticated. Select the Teams action's connection, select **Change connection**, and sign in with an account that has permission to post to the target channel.

### Connect the playbook to an automation rule and validate

Before the playbook can run automatically, assign its managed identity the Microsoft Sentinel Responder role (as covered in the previous unit). Then connect it to an automation rule:

1. In the Microsoft Defender portal, navigate to **Microsoft Sentinel** \> **Automation**.
2. Select **Create** \> **Automation rule**.
3. Name the rule, then set the trigger to **Incident created**, and add a condition for **Incident severity Equals High**.
4. Under **Actions**, select **Run playbook** and choose `sentinel-teams-incident-notify`.
5. Select **Apply**.

To validate the end\-to\-end flow, create a test incident manually or briefly enable a test analytics rule that you know activates.

Once the incident is created, open the Logic App in the Azure portal and select **Run history**. The most recent run appears at the top of the list. Select it to view each action in sequence—the Microsoft Sentinel trigger, the Get incident action, and the Teams post action. Each action shows its execution time, input payload, and output. A green checkmark on every action means the notification posted successfully. Check your Teams channel to confirm the message arrived with the expected content.

If the Teams action fails with a connection error, reauthorize the Teams connection in the Logic App's **Connections** settings.

---

## Knowledge check

Check your knowledge of Microsoft Sentinel automation rules and Logic Apps playbooks.

### Check your knowledge

---

## Summary

Contoso Financial Services' SOC now has a layered automation architecture in place. Automation rules handle the triage layer—incidents are automatically tagged by category, assigned to the appropriate team, and known\-benign alerts are suppressed during maintenance windows without analyst intervention. The prebuilt notification playbook from Content Hub delivers immediate Teams notifications with embedded incident details when high\-severity incidents are created. And the custom Logic Apps playbook gives the team a reusable, version\-controlled response workflow they can extend as Contoso's threat landscape grows.

In this module, you:

* Explained the difference between automation rules and playbooks and identified when to use each
* Created automation rules to assign, tag, and suppress incidents based on conditions and evaluation order
* Configured and activated a prebuilt Content Hub playbook with the correct managed identity permissions
* Authored a custom Logic Apps playbook using the Microsoft Sentinel incident trigger and connected it to an automation rule

### What's next

With automated response in place, Contoso's Microsoft Sentinel deployment is operationally ready. The final step is closing out the data lifecycle: making sure nonstandard event sources have a table to land in, compliance retention requirements are met at the right cost tier, and Purview Audit logs are queryable from the Defender portal for SOX compliance investigations.

Tip

For the full catalog of prebuilt automation solutions, see [Microsoft Sentinel SOAR content catalog](/en-us/azure/sentinel/sentinel-soar-content).

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/implement-automation-rules-playbooks-sentinel/_

## Fuentes
- [Implement automation rules and playbooks in Microsoft Sentinel](https://learn.microsoft.com/en-us/training/modules/implement-automation-rules-playbooks-sentinel/?WT.mc_id=api_CatalogApi)
