# Connect Microsoft services to Microsoft Sentinel

> Curso: Implement activity and event collection in Microsoft Sentinel (wwl-implement-activity-event-collection-sentinel) · Seccion: Implement activity and event collection in Microsoft Sentinel
> Duracion estimada: 26 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You connect Microsoft 365 and Azure services to the Microsoft Sentinel workspace using the provided data connectors. The data connectors are included in out\-of\-the\-box (OOTB), or built\-in Content Hub solutions.

You're a Security Operations Analyst working at a company that implemented Microsoft Sentinel. You'll connect Microsoft 365 and Azure services to Microsoft Sentinel.

Based on your previously documented connector plan, you use the Content Hub to install the solutions that include the specific connectors. As you activate the connectors, you notice the option to have incidents created from the Microsoft Entra ID Protection service. You don’t follow the recommended option to create incidents as you plan to activate the incident creation rule with custom options later in your implementation process.

After completing this module, you'll be able to:

* Connect Microsoft service connectors
* Explain how connectors autocreate incidents in Microsoft Sentinel

### Prerequisites

Basic experience with Microsoft Azure operations.

---

## Connect the Microsoft 365 connector

The Microsoft 365 connector provides insight into ongoing user activities. You collect data like file downloads, access requests sent, changes to group events, set\-mailbox, and details of the user who performed the actions.​

### Install the solution

Start by installing the Microsoft 365 solution that contains the data connector.

1. For Microsoft Sentinel in the Azure portal, under **Content management**, select **Content hub**.   
For Microsoft Sentinel in the Defender portal, select **Microsoft Sentinel** \> **Content management** \> **Content hub**.
2. Search for and select **Microsoft 365**.
3. On the right\-hand side pane, select **Install**.

### Configure the data connector

After the solution is installed, connect the data connector.

1. In the Microsoft Sentinel left navigation menu expand **Configuration**, and select **Data connectors**.
2. Select **Microsoft 365**.
3. Then select the **Open connector page** on the preview pane.
4. Review the *Description* and *Data types* tabs to understand the data that is ingested.
5. In the **Instructions** tab, verify that you meet the *Prerequisites*.
6. In the **Instructions** tab, under the section labeled **Configuration**, select the record types to collect and **Apply Changes**.
7. Wait until validation is complete and the button changes to **Disconnect**.

---

## Connect the Microsoft Entra connector

Gain insights into Microsoft Entra ID by connecting Audit and Sign\-in logs to Microsoft Sentinel to gather insights around Microsoft Entra scenarios. You can learn about app usage, conditional access policies, and legacy auth related details using our Sign\-in logs. You can get information on your Self\-Service Password Reset (SSPR) usage, Microsoft Entra Management activities like user, group, role, and app management in the Audit logs table.

### Install the solution

Start by installing the solution that contains the data connector.

1. For Microsoft Sentinel in the Azure portal, under **Content management**, select **Content hub**.   
For Microsoft Sentinel in the Defender portal, select **Microsoft Sentinel** \> **Content management** \> **Content hub**.
2. Search for and select **Microsoft Entra ID**.
3. On the right\-hand side pane, select **Install**.

### Configure the data connector

After the solution is installed, connect the data connector.

1. In the Microsoft Sentinel left navigation menu expand **Configuration**, and select **Data connectors**.
2. Select **Microsoft Entra ID**.
3. Then select the **Open connector** page on the preview pane.
4. Mark the checkboxes next to the logs you want to stream into Microsoft Sentinel, and select **Connect**.

#### Available log types

When you configure the connector, you can independently select which log types to stream into Microsoft Sentinel. Each log type writes to a separate Log Analytics table:

| Log type | Table |
| --- | --- |
| Interactive user sign\-in logs | SigninLogs |
| Non\-interactive user sign\-in logs | AADNonInteractiveUserSignInLogs |
| Service principal sign\-in logs | AADServicePrincipalSignInLogs |
| Managed identity sign\-in logs | AADManagedIdentitySignInLogs |
| Provisioning logs | AADProvisioningLogs |
| AD FS sign\-in logs | ADFSSignInLogs |
| Audit logs | AuditLogs |

Enabling only the log types relevant to your use cases helps manage Log Analytics ingestion costs.

---

## Connect the Microsoft Entra ID Protection connector

Microsoft Entra ID Protection provides a consolidated view of at\-risk users, risk events, and vulnerabilities, with the ability to remediate risk immediately and set policies to autoremediate future events.

### Install the solution

Start by installing the solution that contains the data connector.

1. For Microsoft Sentinel in the Azure portal, under **Content management**, select **Content hub**.   
For Microsoft Sentinel in the Defender portal, select **Microsoft Sentinel** \> **Content management** \> **Content hub**.
2. Search for and select **Microsoft Entra ID Protection**.
3. On the right\-hand side pane, select **Install**.

### Configure the data connector

After the solution is installed, connect the data connector.

1. In the Microsoft Sentinel left navigation menu expand **Configuration**, and select **Data connectors**.
2. Select **Microsoft Entra ID Protection**.
3. Then select the **Open connector** page on the preview pane.
4. Select **Connect** to start streaming the Microsoft Entra ID Protection alerts.
5. Select whether alerts from Microsoft Entra ID Protection automatically generate incidents by selecting **Enable**.

If you enable creating incidents, the default analytics rule "Create incidents based on Microsoft Entra ID Protection alerts" is enabled with default values. You can edit this analytical rule on the Analytics page.

---

## Connect the Azure Activity connector

The Azure Activity Log is a subscription log that provides insight into subscription\-level events that occur in Azure. The events included are from Azure Resource Manager operational data, service health events, write operations taken on the resources in your subscription, and the status of activities performed in Azure. The Azure Activity Data connector uses Azure Policy to apply an Azure Subscription log\-streaming pipeline that sends the event data to Log Analytics.

Important

Prerequisites require your user to be assigned the owner role on the relevant subscription.

### Install the solution

Start by installing the solution that contains the data connector.

1. For Microsoft Sentinel in the Azure portal, under **Content management**, select **Content hub**.   
For Microsoft Sentinel in the Defender portal, select **Microsoft Sentinel** \> **Content management** \> **Content hub**.
2. Search for and select **Azure Activity**.
3. On the right\-hand side pane, select **Install**.

### Configure the data connector

After the solution is installed, connect the data connector.

1. In the Microsoft Sentinel left navigation menu expand **Configuration**, and select **Data connectors**.
2. Select the **Azure Activity** Data connector.
3. Select **Open connector page**.
4. In the *Instructions/Configuration* area, scroll down and under *2\. Connect your subscriptions...* select **Launch Azure Policy Assignment Wizard**.
5. In the **Basics** tab, select the ellipsis button (...) under **Scope** and select your "Azure subscription" from the drop\-down list and select **Select**.
6. Select the **Parameters** tab, choose your *yourName\-sentinel* workspace from the **Primary Log Analytics workspace** drop\-down list.
7. Select the **Remediation** tab and select the **Create a remediation task** checkbox. This action applies the subscription configuration to send the information to the Log Analytics workspace.

Note

To apply the policy to your existing resources, you need to create a remediation task.
8. Select the **Review \+ Create** button to review the configuration.
9. Select **Create** to finish.

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary and resources

You learned how to connect Microsoft 365 and Azure services to the Microsoft Sentinel workspace using the provided data connectors.

You should now be able to:

* Connect Microsoft services connectors
* Explain how connectors autocreate incidents in Microsoft Sentinel

### Learn more

You can learn more by reviewing the following.

* [Microsoft Sentinel data connectors](/en-us/azure/sentinel/connect-data-sources)
* [Microsoft 365 connector for Microsoft Sentinel](/en-us/azure/sentinel/data-connectors/microsoft-365)
* [Connect Microsoft Entra data to Microsoft Sentinel](/en-us/azure/sentinel/connect-azure-active-directory)
* [Become a Microsoft Sentinel Ninja](https://techcommunity.microsoft.com/blog/microsoftsentinelblog/become-a-microsoft-sentinel-ninja-the-complete-level-400-training/1246310)
* [Microsoft Tech Community Security Webinars](https://techcommunity.microsoft.com/t5/microsoft-security-and/security-community-webinars/ba-p/927888)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/connect-microsoft-services-to-azure-sentinel/_

## Fuentes
- [Connect Microsoft services to Microsoft Sentinel](https://learn.microsoft.com/en-us/training/modules/connect-microsoft-services-to-azure-sentinel/?WT.mc_id=api_CatalogApi)
