# Hunt for threats using notebooks in Microsoft Sentinel

> Curso: Perform threat hunting in Microsoft Sentinel (wwl-sc-200-perform-threat-hunting-azure-sentinel) · Seccion: Perform threat hunting in Microsoft Sentinel
> Duracion estimada: 31 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

You can use notebooks in Microsoft Sentinel for advanced hunting.

You're a Security Operations Analyst working at a company that implemented Microsoft Sentinel. You want to mature your Security Operations team to proactively hunt for malicious activity in your environment with advanced machine learning capabilities.

After developing your hunting hypothesis, you utilize a Jupyter notebook to integrate machine learning libraries, advanced visualizations, and external data to detect malicious activity patterns.

After completing this module, you'll be able to:

* Explore API libraries for advanced threat hunting in Microsoft Sentinel
* Describe notebooks in Microsoft Sentinel
* Create and use notebooks in Microsoft Sentinel

### Prerequisites

* Basic knowledge of operational concepts such as monitoring, logging, and alerting
* Familiarity deploying Azure services
* Familiarity with scripting and Python coding

---

## Access Azure Sentinel data with external tools

Before hunting with notebooks, it's essential to understand the foundation of Microsoft Sentinel is the Log Analytics data store, which combines high\-performance querying, dynamic schema, and scales to massive data volumes. The Azure portal and all Microsoft Sentinel tools use a standard API to access this data store. The same API is also available for external tools such as Python and PowerShell. There are two libraries that you can use to simplify API access:

* Kqlmagic
* msticpy

#### Kqlmagic

The Kqlmagic library provides an easy to implement API wrapper to run KQL queries.

#### msticpy

Microsoft Threat Intelligence Python Security Tools is a set of Python tools intended to be used for security investigations and hunting. Many of the tools originated as code Jupyter notebooks written to solve a problem as part of a security investigation. Some of the tools are only useful in notebooks (for example, much of the nbtools subpackage), but many others can be used from the Python command line or imported into your code.

The package addresses three central needs for security investigators and hunters:

* Acquiring and enriching data
* Analyzing data
* Visualizing data

msticpy can query using KQL; the library also provides predefined queries for Microsoft Sentinel, Microsoft Defender XDR for Endpoint, and the Microsoft Security Graph. An example of a function is the list\_logons\_by\_account, which retrieves the logon events for an account. For details about msticpy visit: [https://msticpy.readthedocs.io/](https://msticpy.readthedocs.io/?azure-portal=true)

---

## Create a notebook

To get started with Notebooks, use the *Getting Started Guide For Microsoft Sentinel ML Notebooks* notebook.

1. In the Microsoft Sentinel navigation menu, expand the *Threat Management* section, and select **Notebooks**
2. You need to create an Azure Machine Learning (ML) Workspace. From the menu, select **Configure Azure Machine Learning**, then **Create new Azure ML workspace**.
3. In the Subscription box, select your subscription.
4. Select **Create a new Resource group** and choose a name for your new resource group.
5. In the Workspace details section:

	* Give your workspace a unique name.
	* Choose your Region
	* Keep the default Storage account, Key vault, and Application insights information.
	* The Container registry option can remain as None.
6. At the bottom of the page, select **Review \+ create**. Then on the next page, select **create**. It takes a moment to deploy the workspace.

Note

It takes a few minutes to deploy the Machine Learning workspace.
7. After *Your deployment is complete* message appears, return to Microsoft Sentinel.
8. Navigate to the Threat Management section, and select **Notebooks**.
9. Select the **Templates** tab.
10. Select the **A Getting Started Guide For Microsoft Sentinel ML Notebooks** from the list.
11. Select **Create from template** button on the bottom of the detail pane.
12. Review the default options and then select **Save**.
13. Select the **Launch notebook** button.
14. Select **Close** if an informational window appears in the Microsoft Azure Machine Learning studio.
15. 1. In the command bar, to the right of the **Compute:** selector, select the **\+** symbol to *Create Azure ML compute* instance. **Hint:** It might be hidden inside the ellipsis icon **(...)**.
Note

You can have more screen space by hiding the Azure ML Studio left menu selections. Select the *Hamburger menu* (3 horizontal lines on the top left), and by collapsing the Notebooks Files by selecting the **\<\<** icon.
16. Type a unique name in the *Compute name* field. This identifies your compute instance.
17. Scroll down and select the first option available.

Tip

Workload type: Development on Notebooks (or other IDE) and lightweight testing.
18. Select the **Review \+ Create** button at the bottom of the screen, then scroll down and select **Create**. Close any feedback window that appears. This takes a few minutes. You see a notification (bell icon) when it completes and the *Compute instance* left icon turns from blue to green.
19. Once the Compute is created and running, verify that the kernel to use is *Python 3\.10 \- Pytorch and Tensorflow*.

Tip

This is shown in the right of the menu bar. If that kernel isn't selected, select the *Python 3\.10 \- Pytorch and Tensorflow* option from the drop\-down list. You can select the **Refresh** icon on the far right to see the kernel options.
20. Select the **Authenticate** button and wait for the authentication to complete.
21. Clear all the results from the notebook by selecting the **Clear all outputs** (Eraser icon) from the menu bar and follow the *Getting Started* tutorial.

Tip

This can be found by selecting the ellipsis (...) from the menu bar.
22. Review section *1 Introduction* in the notebook and proceed to section *2 Initializing the notebook and MSTICPy*.

Tip

Section 1\.2 *Running code in notebooks* lets you practice running small lines of Python code.
23. In section *2 Initializing the notebook and MSTICPy*, review the content on Initializing the notebook and installing the MSTICPy package.
24. Run the *Python code* to initialize the cell by selecting the **Run cell** button (Play icon) to the left of the code.
25. It should take \>30 seconds to run. Once it completes, review the output messages and *disregard any warnings about the Python kernel version* or other error messages.
26. The code ran successfully if *msticpyconfig.yaml* was created in the *utils* folder in the *file explorer* pane on the left. It can take another 30 seconds for the file to appear. If it doesn't appear, select the **Refresh** icon in the *file explorer* pane.

Tip

You can clear the output messages by selecting the ellipsis (...) on the left of the code window for the *Output menu* and selecting the *Clear output* (square with an x\*) icon.
27. Select the **msticpyconfig.yaml** file in the *file explorer* pane on the left to review the contents of the file and then close it.
28. Proceed to section *3 Querying data with MSTICPy* and review the contents. Don't run the *Multiple Microsoft Sentinel workspaces* code cell as it fails, but the other code cells can be run successfully.

Note

If you can't complete the steps above to access the Notebook, you can follow it on its GitHub viewer page instead. [Getting Started with Azure ML Notebooks and Microsoft Sentinel](https://nbviewer.org/github/Azure/Azure-Sentinel-Notebooks/blob/master/A%20Getting%20Started%20Guide%20For%20Azure%20Sentinel%20ML%20Notebooks.ipynb)

---

## Explore notebook code

The following code blocks provide a representative example of using notebooks to work with Microsoft Sentinel data.

**Code Block**

In this snippet of code:

* Create a new variable \[test\_query] that contains the KQL query.
* Next, you run the query \[qry\_prov.exec\_query()]. This utilizes the msticpy library to execute the KQL query in the Microsoft Sentinel Log Analytics related workspace. The results are stored in the \[test\_df] variable.
* Next, display the first five rows with the xxx\_xxxx.head() function.

**Code Block**

In this snippet of code:

* You create a new function called lookup\_res that takes a variable row.
* Next, you save the IP address stored in row to the variable \[ip].
* The next line of code uses the msticpy function \[ti.lookup\_ioc()] to query the ThreatIntelligenceIndicator table for a row that is sourced from VirusTotal with a matching ip\-address.
* Next, the msticpy function \[ti.result\_to\_df()] will return a DataFrame representation of response.
* The new function returns the Severity of the IP address.

**Code Block**

In this snippet of code:

* Create a new variable \[vis\_q] that contains the KQL query.
* Next, you run the query \[qry\_prov.exec\_query()]. This utilizes the msticpy library to execute the KQL query in the Microsoft Sentinel Log Analytics related workspace. The results are stored in the \[vis\_data] variable.
* Then, \[qry\_prov.exec\_query()] returns a pandas DataFrame that provides visualization features. You then plot a bar graph with the unique IP addresses and how many times they were used in the first five entries of the Dataframe.

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary and resources

You should have learned how to perform advanced hunting in Microsoft Sentinel.

You should now be able to:

* Explore API libraries for advanced threat hunting in Microsoft Sentinel
* Describe notebooks in Microsoft Sentinel
* Create and use notebooks in Microsoft Sentinel

### Learn more

You can learn more by reviewing the following.

[Become a Microsoft Sentinel Ninja](https://techcommunity.microsoft.com/t5/azure-sentinel/become-an-azure-sentinel-ninja-the-complete-level-400-training/ba-p/1246310?azure-portal=true)

[Microsoft Tech Community Security Webinars](https://techcommunity.microsoft.com/t5/microsoft-security-and/security-community-webinars/ba-p/927888?azure-portal=true)

[KQL quick reference](/en-us/azure/data-explorer/kql-quick-reference?azure-portal=true)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/perform-threat-hunting-sentinel-with-notebooks/_

## Fuentes
- [Hunt for threats using notebooks in Microsoft Sentinel](https://learn.microsoft.com/en-us/training/modules/perform-threat-hunting-sentinel-with-notebooks/?WT.mc_id=api_CatalogApi)
