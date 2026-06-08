# Manage content in Microsoft Sentinel

> Curso: Create detections and perform investigations using Microsoft Sentinel (wwl-sc-200-create-detections-perform-investigation) · Seccion: Create detections and perform investigations using Microsoft Sentinel
> Duracion estimada: 15 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Microsoft Sentinel **content** is Security Information and Event Management (SIEM) content that enables customers to ingest data, monitor, alert, hunt, investigate, respond, and connect with different products, platforms, and services in Microsoft Sentinel.

Content in Microsoft Sentinel includes any of the following types:

* **Data connectors** provide log ingestion from different sources into Microsoft Sentinel
* **Parsers** provide log formatting/transformation into ASIM formats, supporting usage across various Microsoft Sentinel content types and scenarios
* **Workbooks** provide monitoring, visualization, and interactivity with data in Microsoft Sentinel, highlighting meaningful insights for users
* **Analytics** rules provide alerts that point to relevant SOC actions via incidents
* **Hunting queries** are used by SOC teams to proactively hunt for threats in Microsoft Sentinel
* **Notebooks** help SOC teams use advanced hunting features in Jupyter and Azure Notebooks
* **Watchlists** support the ingestion of specific data for enhanced threat detection and reduced alert fatigue
* **Playbooks** and Azure Logic Apps custom connectors provide features for automated investigations, remediations, and response scenarios in Microsoft Sentinel

To maintain **content** in for Microsoft Sentinel use:

* **Content hub**: \- Microsoft Sentinel **solutions** are packages of Microsoft Sentinel content or Microsoft Sentinel API integrations, which fulfill an end\-to\-end product, domain, or industry vertical scenario in Microsoft Sentinel.
* **Repositories**: \- Repositories help you automate the deployment and management of your Microsoft Sentinel content through central repositories.
* **Community**: Onboard community content on\-demand to enable your scenarios. The GitHub repo at [https://github.com/Azure/Azure\-Sentinel](https://github.com/Azure/Azure-Sentinel) contains content by Microsoft and the community that is tested and available for you to implement in your Sentinel workspace.

You're a Security Operations Analyst working at a company that implemented Microsoft Sentinel. You need to install connectors and analytical rules from a vendor. You also created a library of hunting queries that need to be maintained across multiple environments.

By the end of this module, you are able to manage *content* in Microsoft Sentinel.

After completing this module, you'll be able to:

* Install a content hub solution in Microsoft Sentinel
* Connect a GitHub repository to Microsoft Sentinel

---

## Use solutions from the content hub

Use the Microsoft Sentinel Content hub to centrally discover and install out\-of\-the\-box (built\-in) content.

The Microsoft Sentinel Content Hub provides in\-product discoverability, single\-step deployment, and enablement of end\-to\-end product, domain, and/or vertical out\-of\-the\-box solutions and content in Microsoft Sentinel.

In the Content hub, filter by categories and other parameters, or use the powerful text search, to find the content that works best for your organization's needs. The Content hub also indicates the support model applied to each piece of content, as some content is maintained by Microsoft and others are maintained by partners or the community.

Manage updates for out\-of\-the\-box content via the Microsoft Sentinel Content hub, and for custom content via the Repositories page.

Customize out\-of\-the\-box content for your own needs, or create custom content, including analytics rules, hunting queries, notebooks, workbooks, and more. Manage your custom content directly in your Microsoft Sentinel workspace, via the Microsoft Sentinel API, or in your own source control repository, via the Microsoft Sentinel Repositories page.

### Solutions

Microsoft Sentinel solutions are packaged content or integrations that deliver end\-to\-end product value for one or more domain or vertical scenarios.

The solutions experience is powered by Azure Marketplace for solutions’ discoverability and deployment.

Microsoft Sentinel solutions provide in\-product discoverability, single\-step deployment, and enablement of end\-to\-end product, domain, and/or vertical scenarios in Microsoft Sentinel. This experience is powered by for solutions’ discoverability, deployment, and enablement, and by for solutions’ authoring and publishing.

* **Packaged content** are collections of one or more pieces of Microsoft Sentinel content, such as data connectors, workbooks, analytics rules, playbooks, hunting queries, watchlists, parsers, and more.
* **Integrations** include services or tools built using Microsoft Sentinel or Azure Log Analytics APIs that support integrations between Azure and existing customer applications, or migrate data, queries, and more, from those applications into Microsoft Sentinel.

You can also use solutions to install packages of out\-of\-the\-box content in a single step, where the content is often ready to use immediately. Providers and partners can use solutions to productize investments by delivering combined product, domain, or vertical value.

Use the Content hub to centrally discover and deploy solutions and out\-of\-the\-box content in a scenario\-driven manner.

#### Find a solution

* From the Microsoft Sentinel navigation menu, under Content management, select Content hub.
* The Content hub page displays a searchable and filterable grid of solutions.
* Filter the list displayed, either by selecting specific values from the filters, or entering any part of a solution name or description in the Search field.

Each solution in the grid shows the categories applied to the solution, and types of content included in the solution.

For example, in the Cisco Umbrella solution shows a category of Security \- Others, and that this solution includes 10 analytics rules, 11 hunting queries, a parser, three playbooks, and more.

### Install or update a solution

* In the content hub, select a solution to view more information on the right. Then select Install, or Update, if you need updates. For example:
* On the solution details page, select Create or Update to start the solution wizard. On the wizard's Basics tab, enter the subscription, resource group, and workspace to which you want to deploy the solution.
* Select Next to cycle through the remaining tabs (corresponding to the components included in the solution), where you can learn about, and in some cases configure, each of the content components.
* Finally, in the Review \+ create tab, wait for the Validation Passed message, then select Create or Update to deploy the solution. You can also select the Download a template for automation link to deploy the solution as code.

---

## Use repositories for deployment

When creating custom content, you can store and manage it in your own Microsoft Sentinel workspaces, or an external source control repository, including GitHub and Azure DevOps repositories. Managing your content in an external repository allows you to make updates to that content outside of Microsoft Sentinel, and have it automatically deployed to your workspaces.

### Prerequisites and scope

Before connecting your Microsoft Sentinel workspace to an external source control repository, make sure that you have:

* Access to a GitHub or Azure DevOps repository, with any custom content files you want to deploy to your workspaces, in relevant Azure Resource Manager (ARM) templates.

Microsoft Sentinel currently supports connections only with GitHub and Azure DevOps repositories.
* An Owner role in the resource group that contains your Microsoft Sentinel workspace. This role is required to create the connection between Microsoft Sentinel and your source control repository. If you're unable to use the Owner role in your environment, you can instead use the combination of User Access Administrator and Sentinel Contributor roles to create the connection.

### Maximum connections and deployments

Each Microsoft Sentinel workspace is currently limited to five connections.

Each Azure resource group is limited to 800 deployments in its deployment history. If you have a high volume of ARM template deployments in your resource group(s), you may see a Deployment QuotaExceeded error.

### Validate your content

Deploying content to Microsoft Sentinel via a repository connection doesn't validate that content other than verifying that the data is in the correct ARM template format.

We recommend that you validate your content templates using your regular validation process. You can use the Microsoft Sentinel GitHub validation process and tools to set up your own validation process.

### Connect a repository

This procedure describes how to connect a GitHub or Azure DevOps repository to your Microsoft Sentinel workspace, where you can save and manage your custom content, instead of in Microsoft Sentinel.

Each connection can support multiple types of custom content, including analytics rules, automation rules, hunting queries, parsers, playbooks, and workbooks. For more information, see About Microsoft Sentinel content and solutions.

To create your connection:

* Make sure that you're signed into your source control app with the credentials you want to use for your connection. If you're currently signed in using different credentials, sign out first.
* In Microsoft Sentinel, on the left under Content management, select Repositories.
* Select Add new, and then, on the Create a new connection page, enter a meaningful name and description for your connection.
* From the Source Control dropdown, select the type of repository you want to connect to, and then select Authorize.
* Select one of the following tabs, depending on your connection type:

#### GitHub

* Enter your GitHub credentials when prompted.

The first time you add a connection, you see a new browser window or tab, prompting you to authorize the connection to Microsoft Sentinel. If you're already logged into your GitHub account on the same browser, your GitHub credentials are auto\-populated.
* A Repository area now shows on the Create a new connection page, where you can select an existing repository to connect to. Select your repository from the list, and then select Add repository.

The first time you connect to a specific repository, you see a new browser window or tab, prompting you to install the Azure\-Sentinel app on your repository. If you have multiple repositories, select the ones where you want to install the Azure\-Sentinel app, and install it.

You are directed to GitHub to continue the app installation.
* After the Azure\-Sentinel app is installed in your repository, the Branch dropdown in the Create a new connection page is populated with your branches. Select the branch you want to connect to your Microsoft Sentinel workspace.
* From the Content Types dropdown, select the type of content you are deploying.

	+ Both parsers and hunting queries use the Saved Searches API to deploy content to Microsoft Sentinel. If you select one of these content types, and also have content of the other type in your branch, both content types are deployed.
	+ For all other content types, selecting a content type in the Create a new connection pane deploys only that content to Microsoft Sentinel. Content of other types isn't deployed.
* Select Create to create your connection.

After the connection is created, a new workflow or pipeline is generated in your repository, and the content stored in your repository is deployed to your Microsoft Sentinel workspace.

The deployment time may vary depending on the volume of content that you're deploying.

#### Azure DevOps

* You're automatically authorized to Azure DevOps using your current Azure credentials. To ensure valid connectivity, verify that you've authorized to the same Azure DevOps organization that you're connecting to from Microsoft Sentinel, or use an InPrivate browser window to create your connection.
* In Microsoft Sentinel, from the dropdown lists that appear, select your Organization, Project, Repository, Branch, and Content Types.

	+ Both parsers and hunting queries use the Saved Searches API to deploy content to Microsoft Sentinel. If you select one of these content types, and also have content of the other type in your branch, both content types are deployed.
	+ For all other content types, selecting a content type in the Create a new connection pane deploys only that content to Microsoft Sentinel. Content of other types isn't deployed.
* Select Create to create your connection. For example:

After the connection is created, a new workflow or pipeline is generated in your repository, and the content stored in your repository is deployed to your Microsoft Sentinel workspace.

The deployment time may vary depending on the volume of content that you're deploying.

---

## Module assessment

Choose the best response for each of the questions below.

### Check your knowledge

---

## Summary and resources

By the end of this module, you're able to manage *content* in Microsoft Sentinel.

You should now be able to:

* Install a content hub solution in Microsoft Sentinel
* Connect a GitHub repository to Microsoft Sentinel

### Learn more

You can learn more by reviewing the following.

[Become a Microsoft Sentinel Ninja](https://techcommunity.microsoft.com/t5/azure-sentinel/become-an-azure-sentinel-ninja-the-complete-level-400-training/ba-p/1246310?azure-portal=true)

[Microsoft Tech Community Security Webinars](https://techcommunity.microsoft.com/t5/microsoft-security-and/security-community-webinars/ba-p/927888?azure-portal=true)

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/manage-content-microsoft-sentinel/_

## Fuentes
- [Manage content in Microsoft Sentinel](https://learn.microsoft.com/en-us/training/modules/manage-content-microsoft-sentinel/?WT.mc_id=api_CatalogApi)
