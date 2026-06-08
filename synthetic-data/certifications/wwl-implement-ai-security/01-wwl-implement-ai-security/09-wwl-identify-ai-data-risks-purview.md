# Identify AI data risks using Microsoft Purview Data Security Posture Management

> Curso: Implement security for AI (wwl-implement-ai-security) · Seccion: Implement security for AI
> Duracion estimada: 21 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Contoso Financial Services deployed Microsoft 365 Copilot across its finance and advisory teams. Analysts use Copilot daily to draft reports, summarize client files, and query internal data sources. The AI tools are working—productivity is up, and teams are moving faster. But the security team has a problem. The security team has no visibility into which sensitive data Copilot is surfacing. There's no visibility into which SharePoint sites are being used as AI grounding sources, or whether any interactions involve restricted client financial records.

The question isn't whether AI is being used. It's whether it's being used safely.

Microsoft Purview Data Security Posture Management (DSPM) for AI addresses this gap directly. It discovers how AI tools interact with your organizational data, identifies SharePoint content that is overexposed to AI grounding, and surfaces interaction risks from Copilot and other AI applications—all without requiring log exports or custom queries.

### Learning objectives

In this module, you learn how to:

* Configure Microsoft Purview Data Security Posture Management (DSPM) for AI
* Assess SharePoint data overexposure risks that affect AI grounding data
* Identify sensitive data risks in Copilot and AI application interactions
* Interpret DSPM for AI dashboards and prioritize remediation actions

### Prerequisites

Before you begin, you should have:

* Familiarity with Microsoft Purview portal navigation
* Basic understanding of data security and posture management concepts
* Awareness of Microsoft 365 Copilot and AI application data access patterns

---

## Configure Data Security Posture Management (DSPM) for AI

Microsoft Purview Data Security Posture Management (DSPM) for AI helps security teams understand how AI tools like Microsoft 365 Copilot interact with sensitive data across the organization. At Contoso Financial Services, the security team needs visibility into which SharePoint sites and files Copilot references when responding to user prompts from the finance and advisory teams. Here, you learn how to enable and configure DSPM for AI, explore the dashboard, and understand what data discovery reveals.

Note

Microsoft Purview offers two versions of Data Security Posture Management. **DSPM for AI (classic)** \- covered in this module—is accessible via **Solutions \> DSPM for AI (classic)** in the Microsoft Purview portal. Microsoft also released a newer **Data Security Posture Management** experience with expanded data source coverage, guided workflows organized around data security objectives, and a unified interface across Purview solutions. The classic version remains available and fully functional; the new version builds on the same underlying capabilities with a streamlined experience. New features are added to the newer version only.

| Configuration Step | Action |
| --- | --- |
| Access the portal | Navigate to the Microsoft Purview portal \> Solutions \> DSPM for AI (classic) |
| Review prerequisites | Verify Microsoft Purview Audit is enabled and users have Microsoft 365 Copilot licenses assigned |
| Review the Get started section | Confirm prerequisite status and activate any needed one\-click policies |
| Review dashboard | Examine Reports, Data risk assessments, and Activity explorer for AI interaction data |

Note

The **Get started** section surfaces three one\-click policies you can activate immediately: **Detect risky AI usage** flags risky prompts and responses across Copilot and AI apps; **Unethical behavior in AI apps** detects inappropriate content in AI interactions; and **Detect sensitive info shared with AI via network** captures sensitive data sent to external AI sites. Each policy creates the underlying DLP or communication compliance rule automatically—no manual policy authoring required.

### What DSPM for AI monitors

DSPM for AI surfaces data security risks that arise when users interact with AI applications. Unlike traditional data loss prevention tools that focus on preventing data exfiltration, DSPM for AI focuses on understanding, which sensitive content AI tools can access and reference.

The capability monitors three primary risk areas. First, it tracks when Microsoft 365 Copilot references sensitive content classified by sensitivity labels during user interactions. Second, it identifies SharePoint sites that serve as grounding sources for Copilot and contain broadly accessible sensitive data. Third, it detects when users paste or type sensitive content into external AI sites accessed through a browser.

DSPM for AI automatically discovers active AI tools in your environment. The discovery process identifies which Microsoft 365 Copilot features users access, which SharePoint sites Copilot queries for grounding data, and which external AI applications connect to your tenant. This discovery runs continuously, updating the dashboard as user behavior and AI tool usage evolve.

### Prerequisites for enabling DSPM for AI

Before admins configure DSPM for AI, your organization must have specific infrastructure and licenses in place. You need access to the **Microsoft Purview portal** (`purview.microsoft.com`) with Compliance Administrator permissions or an equivalent role that includes information protection management rights.

The primary prerequisites for monitoring Copilot interactions are:

* **Microsoft Purview Audit** must be enabled for your organization. Auditing is on by default for new tenants, but verify auditing is active before expecting data to appear in the dashboard.
* **Microsoft 365 Copilot licenses** must be assigned to users whose interactions you want to monitor. Without these licenses, DSPM for AI has no Copilot interaction data to surface.
* **Microsoft 365 E5 or Microsoft Purview Suite** (formerly Microsoft 365 E5 Compliance) is required for DSPM access. Microsoft 365 E3 isn't a qualifying license tier for this capability.

For Purview to monitor external AI sites such as ChatGPT or Gemini, two other prerequisites apply: devices must be **onboarded to Microsoft Purview**, and users must have the **Microsoft Purview browser extension** installed. Without these, DSPM can't detect sensitive content pasted into external AI sites accessed through a browser.

Sensitivity labels are recommended but aren't a hard prerequisite for enabling DSPM. The dashboard can surface some risks based on sensitive information type detection (credit card numbers, SSNs, and similar patterns) even without labels applied. However, labeled content enables full risk prioritization and remediation guidance. Organizations without sensitivity labels in place see limited insights—deploying labels is the highest\-value step for maximizing DSPM for AI value.

### Navigate the DSPM for AI dashboard

The DSPM for AI (classic) dashboard is organized into several sections accessible from the left navigation pane. Understanding where each risk type surfaces helps you build an efficient review workflow.

The **Reports** section displays AI interaction data organized into three categories: **Copilot experiences and agents** (Microsoft 365 Copilot, Copilot Studio), **Enterprise AI apps** (ChatGPT Enterprise), and **Other AI apps** (external sites such as ChatGPT consumer and Gemini). The Reports section is where you review which AI tools are active in your organization and the volume of interactions involving sensitive content.

The **Data risk assessments** section is the equivalent of what some documentation calls the SharePoint overexposure view. DSPM for AI automatically runs a weekly data risk assessment against the top 100 SharePoint sites based on usage. For each assessed site, a flyout pane shows **Overview**, **Identify**, **Protect**, and **Monitor** tabs—giving you a structured path from risk discovery to remediation action. Custom assessments can be created to extend coverage beyond the default top\-100 list.

The **Activity explorer** provides granular, event\-level data on AI interactions. Each event record shows the activity type (AI interaction, AI website visit, sensitive info types detected), the user, the AI app category, any sensitive information types found, and files referenced during the interaction.

The **Apps and agents** section lists all AI tools discovered in your environment across the same three categories. This view shows per\-app usage statistics and interaction counts involving sensitive content. In this context, *agents* are AI workflows—such as workflows built\-in Microsoft Copilot Studio—that query organizational data and take actions independently of a direct user session rather than in response to a single prompt. DSPM for AI tracks per\-agent details, showing which sensitive data each agent accessed, and whether Purview policies protect those interactions. Microsoft Security Copilot appears here only when a separate collection policy is configured to capture its prompts and responses—it doesn't appear automatically.

At Contoso, the security team opens the Data risk assessments section and finds the "Earnings Analysis" SharePoint site flagged in the default weekly assessment. The site contains 47 files including items labeled "Confidential" and its permissions grant access to all finance team members—far broader than the senior analyst audience the data requires.

Tip

Start with Data risk assessments to identify quick wins on SharePoint overexposure. Restricting site permissions or applying more stringent access controls provides immediate risk reduction.

---

## Assess SharePoint overexposure

SharePoint sites that serve as grounding sources for Microsoft 365 Copilot can create data exposure risks when they contain sensitive content accessible to more users than intended. When Copilot queries these sites to answer user prompts, it can surface confidential information to users who shouldn't have access to it. At Contoso Financial Services, the security team discovered that quarterly earnings analysis files stored in a broadly accessible SharePoint site were appearing in Copilot responses to junior analysts. Those analysts shouldn't have access to prerelease financial data. Here, you learn how to identify SharePoint overexposure risks, interpret the DSPM dashboard, and prioritize remediation actions.

| Site Risk Level | Sensitivity Labels Present | Remediation Priority |
| --- | --- | --- |
| High | Highly Confidential, Confidential | Immediate \- Restrict site access within 24 hours |
| Medium | Confidential, Internal | Review within one week \- Apply tighter access controls |
| Low | Internal, Public | Monitor \- Ensure labeling is accurate |

### How SharePoint overexposure affects Copilot grounding

Microsoft 365 Copilot grounds its responses in content the user has permission to access. When a user asks Copilot a question, it searches across SharePoint sites, OneDrive files, and other Microsoft 365 content the user's account can reach. If a SharePoint site contains sensitive files but has overly broad permissions, Copilot can include that content in responses to users who shouldn't see it.

Overexposure occurs when site permissions don't match the sensitivity of the content stored there. A site might be set to allow all employees to view content, even though it contains files labeled "Confidential \- Finance Only." In this scenario, Copilot can reference those files when responding to any employee's prompt, creating an inadvertent data disclosure risk.

DSPM for AI detects this pattern by correlating three data points: which SharePoint sites Copilot queries, which sensitivity labels are applied to files in those sites, and which users have access to those sites. When it identifies a mismatch between sensitivity and access breadth, it flags the site as an overexposure risk.

### Read the SharePoint data risk assessment

The **Data risk assessments** section in the DSPM for AI (classic) dashboard is where SharePoint oversharing risks surface. DSPM for AI automatically runs a weekly assessment against the top 100 SharePoint sites based on usage in your organization. You can also create custom assessments to scan specific sites or a broader set of users.

Select a site from the assessment list to open a flyout pane with four tabs:

* **Overview** \- shows the total number of items scanned, sensitive data detected, and sharing links that expose data broadly
* **Identify** \- shows how much content is scanned for sensitive information types, with an option to trigger an on\-demand classification scan
* **Protect** \- provides remediation actions including restricting access by label, restricting all items using SharePoint Restricted Content Discovery, creating autolabeling policies for unlabeled sensitive files, and creating retention policies for stale content
* **Monitor** \- shows how items in the site are shared: with specific people, with the organization, with external users, or via anyone\-with\-the\-link

Sites with high\-sensitivity labels and broad access appear at the top of the assessment. A site containing "Highly Confidential" labeled files accessible to hundreds of users represents a higher priority than a site with "Internal" files accessible to a large department. At Contoso, the security team finds the "Earnings Analysis" site at the top of the default weekly assessment with sharing links accessible to the entire finance group.

### Prioritize remediation actions

Not all overexposure risks require immediate action. Security teams must prioritize based on sensitivity level, access breadth, and Copilot activity patterns.

High\-priority risks involve sites with "Highly Confidential" labeled files accessible to large groups. These sites require immediate remediation because a single Copilot interaction could expose critical business data, personal data, or regulated financial information. Contoso's security team addresses these sites within 24 hours by restricting site permissions to only users who require access for their job functions.

Medium\-priority risks include sites with "Confidential" labeled files or sites with moderately sensitive content accessible to departments beyond the content owner's team. These sites warrant review within one week. Remediation might involve applying more granular access controls, relabeling files with more appropriate sensitivity classifications, or configuring conditional access policies that restrict Copilot's ability to reference that site.

Low\-priority risks appear when sites contain "Internal" labeled files accessible to all employees, or when sensitivity labels can be incorrectly applied. These sites don't pose immediate disclosure risks but can benefit from better labeling practices or periodic access reviews.

After Purview identifies an overexposure risk, DSPM for AI surfaces remediation actions directly from the **Protect** tab of each site's flyout pane:

* **Restrict access by label** \- creates a DLP policy that prevents Microsoft 365 Copilot and agents from summarizing content carrying specific sensitivity labels, without changing SharePoint permissions
* **Restrict all items** \- uses SharePoint Restricted Content Discovery to exclude the site from Copilot grounding entirely, eliminating AI access while preserving human access
* **Create an auto\-labeling policy** \- for sites with unlabeled sensitive files, creates a policy that automatically applies a sensitivity label when sensitive information types are detected
* **Create retention policies** \- for content without access in at least three years, automatically deletes stale data that unnecessarily expands the oversharing surface

The most direct approach restricts site permissions to limit access to only users who need the content. In SharePoint, navigate to the site's settings and modify the members list or change the site from company\-wide sharing to specific security groups. This reduces both human and AI exposure simultaneously.

Applying or updating sensitivity labels addresses scenarios where files lack labels or carry labels that don't match their actual sensitivity. Review unlabeled files in the site and apply appropriate classifications. If files are labeled "Internal" but actually contain confidential financial data, relabel them "Confidential \- Finance Only."

Some organizations choose to exclude specific SharePoint sites from serving as Copilot grounding sources. This approach prevents Copilot from querying the site entirely, eliminating the risk of inadvertent exposure through AI interactions. However, this also reduces Copilot's ability to provide helpful responses to authorized users who legitimately need that content.

At Contoso, the security team restricts the "Earnings Analysis" site to senior financial analysts only and applies a "Highly Confidential \- Earnings Data" label to all quarterly reports. This remediation ensures Copilot can still reference the site for authorized analysts while preventing junior staff from receiving responses that include prerelease financial data.

Tip

Combine sensitivity labels with SharePoint permissions for defense in depth. Even if permissions are misconfigured, labeled files trigger other protections through Microsoft Purview Data Loss Prevention policies.

---

## Identify risks in Copilot and AI app interactions

Every time a user interacts with Microsoft 365 Copilot or another AI application, there's potential for sensitive data to be referenced, generated, or shared in ways that create security risks. Microsoft Purview DSPM for AI captures these interaction events and flags those involving content classified by sensitivity labels. At Contoso Financial Services, a compliance analyst used Copilot to summarize a client financial assessment report labeled "Confidential \- Client Data" and pasted the generated summary into an email to an external consultant. DSPM for AI flagged this interaction as a risk because the summary derived from highly sensitive content and was shared outside the organization. Here, you learn how to identify interaction risks, investigate specific events, and prioritize remediation based on severity.

| Risk Type | Description |
| --- | --- |
| Sensitive data in prompt | User includes content classified with a sensitivity label in a Copilot prompt |
| Sensitive data in response | Copilot returns content that references files classified with sensitivity labels |
| Sensitive data pasted to external AI | User pastes or types labeled content into an external AI site via browser |
| Cross\-boundary interaction | Sensitive data moves between different security zones through AI interactions |

### What interaction risks reveal

Interaction risks surface instances where AI tools accessed, generated, or returned content that carries a Microsoft Purview sensitivity label. Unlike traditional data loss prevention events that trigger when a user attempts to send an email or share a file, interaction risks occur during the AI generation process itself.

When a user asks Copilot to summarize a document, draft an email, or answer a question, Copilot queries content across Microsoft 365 to ground its response. If any content is labeled "Confidential," "Highly Confidential," or another sensitivity classification, DSPM for AI records the interaction as a potential risk. The risk doesn't necessarily mean a policy violation occurred—it means sensitive data was involved in an AI\-generated output that warrants review.

External AI applications create extra risk scenarios. DSPM for AI detects sensitive content when users paste or type it into external generative AI sites—such as ChatGPT consumer or Gemini—through a browser. This detection requires devices to be onboarded to Microsoft Purview and the Microsoft Purview browser extension installed. When these prerequisites are in place, DSPM records an **AI website visit** event and a **Sensitive info types** event when sensitive content is detected during the browser interaction.

### Navigate the Reports and Activity explorer

The **Reports** section in the DSPM for AI (classic) dashboard displays AI interaction data summarized by AI app category: **Copilot experiences and agents**, **Enterprise AI apps**, and **Other AI apps**. Use this view for a high\-level picture of which AI tools are generating sensitive interaction events and at what volume.

For event\-level detail, use **Activity explorer**. Activity explorer displays a chronological list of AI interaction events. Each entry shows the activity type, the sensitivity label or sensitive information type involved, the user who triggered the event, the AI application, and a timestamp. Activity types include:

* **AI interaction** \- a Copilot or agent interaction where prompts and responses were captured
* **AI website visit** \- a user browsed to an external AI site
* **Sensitive info types** \- sensitive information was detected during an AI interaction
* **DLP rule match** \- a DLP policy matched during an AI interaction

Risk types for Copilot interactions fall into several categories. **Prompt\-based risks** occur when a user includes sensitive content directly in a Copilot prompt—for example, copying text from a confidential document into the Copilot chat window. **Response\-based risks** occur when Copilot generates a response that references or incorporates content from labeled files the user has access to. **Browser\-based risks** occur when a user pastes sensitive content into an external AI site.

The AI application column in Activity explorer distinguishes between Microsoft 365 Copilot interactions, Copilot Studio agents, ChatGPT Enterprise, and external consumer AI sites.

At Contoso, the security team filters Activity explorer to show only events involving "Confidential" or "Highly Confidential" sensitive info types and interactions with external AI sites. This filter surfaces the highest\-priority risks: sensitive data leaving the Microsoft 365 security boundary through external AI tools.

### Investigate a specific interaction risk

Selecting an interaction risk from the dashboard opens a detail pane that provides context about what happened during the AI interaction. The detail view shows which specific files or content items were involved and the user account that initiated the interaction. It also displays the full sensitivity label classification, including any sublabels or metadata.

For Copilot interactions, the detail pane indicates whether the sensitive content appeared in the user's prompt, in Copilot's response, or both. If a user asked Copilot "Summarize the Q3 earnings forecast" and Copilot referenced three files labeled "Confidential \- Finance" to generate the summary, the detail view lists all three files.

The detail pane also shows the timestamp and duration of the interaction. Longer Copilot sessions that involve multiple back\-and\-forth prompts and responses appear as separate interaction events if each involves labeled content. This granularity helps you understand whether a user had a single brief interaction with sensitive data or an extended session that repeatedly referenced confidential files.

For external AI site risks, the Activity explorer record identifies which external service was accessed. The event shows the sensitive information types detected, the site visited, and the user—helping you determine whether the interaction represents a one\-time event or part of a pattern of regular data sharing with external AI services. DSPM for AI surfaces these events at the sensitive information type level; it doesn't provide file\-level metadata such as file name or size for browser\-based interactions.

Important

DSPM for AI provides visibility into AI interactions but doesn't automatically block them. To enforce controls that prevent users from uploading sensitive content to external AI apps, configure Microsoft Purview Data Loss Prevention policies targeting those scenarios.

### Prioritize high\-severity interactions

Not every interaction risk requires immediate action. Security teams must prioritize based on the combination of sensitivity label severity, AI application type, and user context.

**Highest priority**: Interactions involving "Highly Confidential" labeled content and external AI sites detected via browser. These events represent sensitive data reaching outside your organization's security perimeter and warrant immediate investigation. Determine whether the user had a legitimate business need to use the external AI site and whether sensitive content was pasted intentionally or inadvertently.

**High priority**: Copilot interactions involving "Highly Confidential" content where the user shared the generated output externally. Even though Copilot itself operates within Microsoft 365's security boundary, if a user copies a Copilot\-generated summary of confidential content and emails it to external recipients, a data disclosure risk exists.

**Medium priority**: Copilot interactions involving "Confidential" labeled content where the output remained within the organization. These interactions can be legitimate uses of Copilot to work with appropriately accessible data, but they warrant review to ensure users understand when they work with sensitive information.

**Lower priority**: Interactions involving "Internal" labeled content or Copilot sessions where the user has explicit permissions to access all referenced files. These events can reflect normal AI\-assisted work and require no remediation.

At Contoso, the security team investigates the compliance analyst's interaction where a Copilot\-generated summary of client financial data was shared externally. The investigation reveals the analyst didn't realize the summary derived from confidential source files. The security team provides training on how sensitivity labels apply to AI\-generated content and configures a Data Loss Prevention policy to warn users before sending emails containing Copilot\-generated summaries of confidential data.

### Connect interaction risks to remediation controls

DSPM for AI helps you move from risk identification to risk mitigation by connecting each interaction to relevant Microsoft Purview controls. From an interaction risk detail pane, you can navigate directly to the sensitivity label policy that classifies the content. You can also access the SharePoint site permissions where the source files are stored, or the Data Loss Prevention rules that should prevent similar future interactions.

If an interaction risk stems from a user accessing overly broad SharePoint permissions, navigate to the Data risk assessments section to address the root cause. If the risk involves an external AI site, you create or update a DLP policy to block or warn users before pasting labeled content into that service.

This connected approach ensures DSPM for AI doesn't just generate alerts—it helps you systematically reduce the attack surface for AI\-related data risks across your organization.

Tip

Review interaction risks weekly to identify patterns. If the same users repeatedly trigger risks with the same external AI application, consider providing targeted training or implementing application controls.

---

## Summary

Microsoft Purview Data Security Posture Management for AI gives Contoso Financial Services' security team what they were missing: visibility into how AI tools interact with organizational data, which SharePoint sites expose sensitive content to Copilot grounding, and which interactions involve classified data that requires follow\-up.

### Review what you accomplished

You configured DSPM for AI in the Microsoft Purview portal, enabling the posture management dashboard that continuously monitors AI tool interactions across your Microsoft 365 environment. The configuration required Microsoft Purview Audit to be enabled and Microsoft 365 Copilot licenses assigned to users—the two primary prerequisites that unlock interaction monitoring. Sensitivity labels aren't a hard requirement to enable DSPM for AI, but they're the highest\-value next step: without them, the dashboard surfaces only pattern\-based detection such as credit card numbers and SSNs. With labels applied, you gain full risk prioritization, label\-scoped remediation actions, and the ability to restrict Copilot access by classification.

With the dashboard active, you assessed SharePoint overexposure by reviewing which sites are being used as AI grounding sources and how many sensitive files they contain. The overexposure view prioritizes sites by label severity, giving you a clear starting point for restricting access or applying more protection. In the Contoso scenario, the quarterly earnings SharePoint site—broadly shared and unlabeled—moved immediately to the top of the remediation queue.

You also reviewed interaction risks, which surface instances where Copilot or AI applications referenced content classified by Microsoft Purview sensitivity labels. Each risk entry links to the label policy, the SharePoint location, and the relevant DLP configuration—so DSPM for AI doesn't just show you problems, it connects you to the controls that address them.

In this module, you learned how to:

* Configure Microsoft Purview Data Security Posture Management (DSPM) for AI
* Assess SharePoint data overexposure risks that affect AI grounding data
* Identify sensitive data risks in Copilot and AI application interactions
* Interpret DSPM for AI dashboards and prioritize remediation actions

### What's next

Data risk visibility is your foundation. The next step is securing the identities that AI agents use to act on that data. In the next module, you'll configure Conditional Access policies for agent identities in Microsoft Entra Agent ID—controlling when and how agents can authenticate to Microsoft services.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/identify-ai-data-risks-purview/_

## Fuentes
- [Identify AI data risks using Microsoft Purview Data Security Posture Management](https://learn.microsoft.com/en-us/training/modules/identify-ai-data-risks-purview/?WT.mc_id=api_CatalogApi)
