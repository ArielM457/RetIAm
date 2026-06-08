# Introduction to GitHub administration

> Curso: GitHub fundamentals - Administration basics and product features Part 1 of 2 (github-github-administration-products-1) · Seccion: GitHub fundamentals - Administration basics and product features Part 1 of 2
> Duracion estimada: 36 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

GitHub administrators work to protect their organization's code and content assets while providing each team access to the repositories they rely on to collaborate and share their work.

Imagine that your CIO (Chief Information Officer) asks you for an adoption plan to help the entire company benefit from GitHub. You want to ensure every group has adequate access to the right repositories and that there's a sustainable way to provide adequate permissions to the appropriate software development and content teams. You'll need to think through the kinds of tasks that administrators need to perform and assign them the right level of access. But first, you really need to understand what options are available to you from GitHub.

In this module, you'll learn about:

* GitHub administrative tasks and their purpose at each hierarchical level.
* The various ways that administrators can configure authentication so that users can access GitHub via the web browser and the git client.
* Hierarchical permission levels and what these permissions allow you to do in GitHub.

### Learning objectives

By the end of this module, you'll be able to:

* Summarize the organizational structures and permission levels that GitHub administrators can use to organize members to control access and security.
* Identify the various technologies that enable a secure authentication strategy, allowing administrators to centrally manage repository access.
* Describe the technologies required to centrally manage teams and members using existing directory information services and how you can use GitHub itself as an identity provider for authentication and authorization.

---

## What is GitHub administration?

As a GitHub administrator, your goal is to keep everything working smoothly for your users. In this unit, you learn about the different levels in the GitHub organizational hierarchy and the administration tasks associated with each level.

### Administration at team level

In GitHub, each user is an organization member that you can add to a team. You can create teams in your organization with cascading access permissions and mentions reflecting your company or group's structure. A team is a useful substructure for refining repository permissions on a more granular level and enabling communication and notification between team members.

Additionally, GitHub allows you to sync your teams with identity provider (IdP) groups such as Microsoft Entra ID. When you synchronize a GitHub team with Microsoft Entra ID, you can replicate changes to GitHub automatically. This sync reduces the need for manual updates and custom scripts. This feature requires GitHub Enterprise Cloud and a verified domain. You can use Microsoft Entra ID with team synchronization to manage administrative tasks such as onboarding new members, granting new permissions, and removing member access to the organization.

Members of a team with *team maintainer* or repository *admin* permissions can:

* Create a new team and select or change the parent team.
* Delete or rename a team.
* Add or remove organization members from a team, or synchronize a GitHub team's membership with an IdP group.
* Add or remove outside collaborators (people who aren't explicitly members of your organization, such as consultants or temporary employees) from team repositories.
* Enable or disable team discussions on the team's page.
* Change the visibility of the team within the organization.
* Manage automatic code review assignment for pull requests, utilizing GitHub's review assignment routing algorithm.
* Schedule reminders.
* Set the team profile picture.

#### Best practices for team\-level administration

Creating teams in your organization enables greater flexibility for collaboration and can make it easier to separate repositories and permissions. The following are some best practices for setting up teams on GitHub:

* Create nested teams to reflect your group or company's hierarchy within your GitHub organization.
* Help streamline PR review processes by creating teams based on interests or specific technology (JavaScript, data science, etc.). Individuals can choose to join these teams according to their interests or skills.
* Enable team synchronization between your IdP and GitHub to allow organization owners and team maintainers to connect teams in your organization with IdP groups. When you synchronize a GitHub team with an IdP group, you can replicate changes to GitHub automatically, reducing the need for manual updates and custom scripts. You can use an IdP with team synchronization to manage administrative tasks such as onboarding new members, granting new permissions, and removing member access to the organization.

### Administration at organization level

In GitHub, organizations are shared spaces enabling users to collaborate across many projects at once. Owners and administrators can manage member access to the organization's data and repositories with sophisticated security and administrative features.

Members of an organization with the *owner* permission can perform a wide range of activities at the organization level including:

* Invite users to join the organization, and remove members from the organization.
* Organize users into a team, and grant *team maintainer* permissions to organization members.
* Add or remove outside collaborators (people who aren't explicitly members of your organization, such as consultants or temporary employees) to organizational repositories.
* Grant repository permission levels to members, and set the base (default) permission level for a given repository.
* Set up organization security.
* Set up billing or assign a billing manager for the organization.
* Extract various types of information about repositories via the use of custom scripts.
* Apply organization\-wide changes such as migrations via the use of custom scripts.

We recommend setting up only one organization for your users and repositories. If specific constraints in your company require you to create multiple organizations, you should be aware of the following points:

* Duplicating an organization or sharing configurations between two organizations isn't possible. This means that you must set up everything from scratch every time you create an organization, which increases the risk of errors in your settings.
* Depending on your software providers' policies, you might incur extra costs if you need to install some applications in multiple organizations.
* Managing multiple organizations introduces additional complexity and setup time.

### Administration at enterprise level

Enterprise accounts include GitHub Enterprise Cloud and Enterprise Server instances and enable owners to centrally manage policy and billing for multiple organizations.

At the enterprise level, members of an enterprise with the *owner* permissions can:

* Enable security assertion markup language (SAML) single sign\-on for their enterprise account, allowing each enterprise member to link their external identity on your IdP to their existing GitHub account.
* Add or remove organizations from the enterprise.
* Set up billing or assign a billing manager for all organizations in the enterprise.
* Set up repository management policies, project board policies, team policies, and other security settings that apply to all the organizations, repositories, and members in the enterprise.
* Extract various types of information about organizations via the use of custom scripts.
* Apply enterprise\-wide changes such as migrations via the use of custom scripts.
* Use GitHub Connect to integrate GitHub Enterprise Server with GitHub.com, if applicable.

### Learn more

Read more about [nested teams](https://docs.github.com/organizations/organizing-members-into-teams/about-teams#nested-teams) in GitHub Docs.

---

## How does GitHub authentication work?

In the previous unit, you learned about typical administration tasks at the team, organization, and enterprise level. In this unit, you’ll explore one of the most common administrative tasks performed by organization owners, which is setting up and controlling users' authentication to GitHub.

### GitHub's authentication options

There are several options for authenticating with GitHub:

#### Username and password

Administrators can allow users to continue using the default username and password authentication method, sometimes known as the "basic" HTTP authentication scheme.

Note

GitHub no longer supports password authentication for Git operations or API usage. We strongly recommend using one (or several) of the other options listed in this unit.

#### Personal access tokens

Personal access tokens (PATs) are an alternative to using passwords for authentication to GitHub when using the GitHub API or the command line. Users generate a token via the GitHub's settings option, and tie the token permissions to a repository or organization. When users interact with GitHub by using the git command\-line tool, they can enter the token information when they're asked for their username and password.

#### SSH keys

As an alternative to using personal access tokens, users can connect and authenticate to remote servers and services via SSH with the help of SSH keys. SSH keys eliminate the need for users to supply their username and personal access token for every interaction.

When setting up SSH, users generate an SSH key, add it to the ssh\-agent, and then add the key to their GitHub account. Adding the SSH key to the ssh\-agent ensures that the SSH key has a passphrase as an extra layer of security. Users can configure their local copy of git to automatically supply the passphrase, or they can supply it manually each time they use the git command\-line tool to interact with GitHub.

You can even use SSH keys with a repository owned by an organization that uses SAML single sign\-on (SSO). If the organization provides SSH certificates, users can also use it to access the organization's repositories without adding the certificate to their GitHub account.

#### Deploy keys

Deploy keys are another type of SSH key in GitHub that grants a user access to a single repository. GitHub attaches the public part of the key directly to the repository instead of a personal user account, and the private part of the key remains on the user's server. Deploy keys are read\-only by default, but you can give them write access when adding them to a repository.

To configure fork settings:

1. Go to the repository’s **Settings**.
2. In the left sidebar, under Security, click **Deploy keys**.
3. Locate the **Add deploy key** option to create a new key.

### GitHub's added security options

GitHub provides a range of security options to help protect accounts and organizational resources.

#### Two\-factor authentication

Two\-factor authentication (2FA), sometimes known as multifactor authentication (MFA), adds an extra layer of protection to your GitHub account. With 2FA, users sign in with their username and password, and then provide a second form of authentication.

GitHub supports several second\-factor options:

* Authenticator apps (like Microsoft Authenticator, Google Authenticator, or Authy) that generate time\-based one\-time codes.
* Hardware security keys (such as YubiKey or Titan Security Key) that support FIDO2/WebAuthn.
* Passkeys for passwordless, phishing\-resistant authentication.
* SMS\-based codes, which are supported but considered less secure than other options and are not recommended as a primary method.

**2FA enforcement:**

* For organizations on GitHub Team and GitHub Enterprise Cloud, organization owners can require members, outside collaborators, and billing managers to enable 2FA for their personal accounts.
* Enterprise Managed Users (EMUs) and GitHub Enterprise Server (GHE.com): Admins can require 2FA for enterprise\-managed accounts only, but cannot enforce 2FA on users’ personal GitHub.com accounts.

Enforcing 2FA helps protect organizations from unauthorized access and strengthens the security of repositories and sensitive data.

#### SAML SSO

If you centrally manage your users' identities with an identity provider (IdP), you can configure SAML single sign\-on (SSO) to protect your organization’s resources on GitHub. SAML SSO allows organization and enterprise owners to control and secure access to repositories, issues, pull requests, and more. When accessing resources, GitHub redirects users to authenticate with the organization’s IdP.

GitHub supports all identity providers that implement the SAML 2\.0 standard, with official support for several popular providers, including:

* Active Directory Federation Services (AD FS).
* Microsoft Entra ID.
* Okta.
* OneLogin.
* PingOne.

#### LDAP (GitHub Enterprise Server)

LDAP (Lightweight Directory Access Protocol) is a widely used protocol for accessing and managing user directory information. On GitHub Enterprise Server, LDAP integration allows you to authenticate users against your existing company directory and manage repository access centrally.

GitHub Enterprise Server integrates with major LDAP services such as:

GitHub Enterprise Server integrates with popular LDAP services like:

* Active Directory.
* Oracle Directory Server Enterprise Edition.
* OpenLDAP.
* Open Directory.

---

## How does GitHub organization and permissions work?

In the previous unit, you explored the different ways that users can authenticate themselves with GitHub. In this unit, you'll learn about permissions for each hierarchical level:

* Repository permissions
* Team permissions
* Organization permissions
* Enterprise permissions

### Repository permission levels

You can customize access to each repository by assigning specific permission levels. There are five standard repository\-level permissions:

* **Read**: Recommended for non\-code contributors who want to view or discuss your project. This level is good for anyone that needs to view the content within the repository but doesn't need to actually make contributions or changes.
* **Triage**: Recommended for contributors who need to proactively manage issues and pull requests without write access. This level is useful for project managers who track issues and discussions without modifying code.
* **Write**: Recommended for contributors who actively push to your project. Write is the standard permission for most developers.
* **Maintain**: Recommended for project managers who need to manage the repository without access to sensitive or destructive actions.
* **Admin**: Recommended for people who need full access to the project, including sensitive and destructive actions like managing security or deleting a repository. These people are repository owners and administrators.

You can give organization members, outside collaborators, and teams different levels of access to repositories owned by an organization. Each permission level grants progressively more access to repository content and settings. Choose the level that best fits each person or team's role in your project without giving more access to the project than necessary.

Administrators can also create custom roles in GitHub Enterprise, extending one of these base roles with additional permissions as needed.

#### What is repository forking?

Forking is a way to create a personal copy of someone else's repository under your own GitHub account. When you fork a repository, you get your own version that you can freely modify without affecting the original project. This process is a common workflow for contributing to open source or experimenting with changes safely.

You can also keep your fork up to date by pulling in changes from the original repository, often called the “upstream” repo.

Here’s how to fork a repository:

1. On GitHub.com, navigate to the main page of the repository you want to fork.
2. In the upper\-right corner, select **Fork**.
3. Choose an owner for the fork (your personal account or an organization).
4. Optionally, rename the forked repository or include all branches.
5. Select **Create fork**.

#### Managing fork permissions (for admins)

For organization\-owned repositories, administrators can control whether repositories can be forked:

* **Public repositories**: Forking is always allowed.
* **Private repositories**: Forking can be disabled or restricted to organization members only.
* **Internal repositories**: These can only be forked within the same enterprise account.

To configure fork settings:

1. Go to the Organization repository’s **Settings**.
2. In the left sidebar, under Access, click **Member privileges**.
3. Locate the **Repository forking** options and update them as needed.

Tip

If you disable forking for a private repository, no one (including organization members) will be able to fork it.

To learn more, see the GitHub Docs article on [Fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

### Viewing Repository Insights

Repository insights on GitHub offer a powerful way to monitor and analyze your project's activity, contributions, and dependencies. By leveraging these insights, you can track project health, identify bottlenecks, and ensure security. This section will guide you through the steps to access repository insights and provide best practices for using them effectively.

#### Steps to View Repository Insights

1. Navigate to the repository on GitHub.
2. Under the repository name, click on the **Insights** tab.
3. Explore the following sections within the Insights tab:
	* **Contributors**: View a graph of contributions over time, including commits, additions, and deletions by each contributor.
	* **Traffic**: Monitor repository traffic, including unique visitors and page views.
	* **Commits**: Analyze commit activity over time.
	* **Code Frequency**: Track the number of lines added and deleted over time.
	* **Dependency Graph**: View the dependencies of your repository and identify potential security vulnerabilities.

#### Best Practices for Using Repository Insights

* **Monitor Contributions**: Use the Contributors section to identify active contributors and areas of the repository that are receiving the most attention.
* **Track Traffic**: Use the Traffic section to understand how users are interacting with your repository and identify trends in engagement.
* **Address Vulnerabilities**: Regularly review the Dependency Graph to ensure your repository remains secure.

By leveraging repository insights, you can make data\-driven decisions to improve collaboration, security, and project management.

### Ways Users Receive Repository Access

#### Actions of a User Given a List of Their Repository Permissions

A user’s effective permissions in a repository are influenced by various factors, including:

* **Repository Role:** (e.g., Admin, Write, Read)
* **Team Membership:** (e.g., inherited permissions from a team)
* **Organization Membership:** (e.g., default organization permissions, SSO requirements)

When you combine these different permission sources, GitHub applies the highest level of access granted to the user. For example, if a user has Read access through a team but also has Write access directly assigned as a collaborator, they will effectively have Write permissions.

#### Repository Membership Options

When granting access to a repository, there are several ways a user can become a collaborator:

| Membership Type | Description |
| --- | --- |
| **Direct Collaborator** | Added explicitly to the repository with a specific role (Read, Triage, Write, Maintain, or Admin).  Recommended for external contributors or small teams. |
| **Team Membership** | A user inherits repository access via their team membership.  Team permissions are often set at the organization level for consistent, scalable management. |
| **Organization Default Permissions** | If the repository is part of an organization, there may be a default permission level for all organization members (e.g., None, Read).  Owners can override these defaults for specific teams or users. |
| **Outside Collaborator** | A user who is not a member of the organization but has explicit access to a repository.  Useful for contractors, freelancers, or open\-source contributors needing limited access. |

### Monitoring and Auditing Repository Access

Regularly auditing who has access to a repository ensures proper security and compliance. Here are some recommended steps and tools:

* **View Access in Repository Settings:**

	+ Navigate to Settings \> Manage access (for the repository).
	+ Review the list of users and teams, along with their permission levels.
* **Organization Audit Log (GitHub Enterprise or Organization\-level):**

	+ Organization owners can view changes to membership, repository access, and permissions in the Audit log.
	+ Filter events by repository name or access changes for a more focused view.
* **Enterprise Audit Log (GitHub Enterprise):**

	+ If you manage multiple organizations, use the Enterprise account’s audit log to track changes across all organizations and repositories.
	+ This is especially valuable for compliance reporting or large\-scale security reviews.
* **Automated Scripting:**

	+ Use the GitHub REST API or GraphQL API to programmatically list collaborators, teams, and permissions.
	+ Integrate scripts with your CI/CD pipeline or security dashboards to continuously monitor and flag anomalies.

**Tip:** Set up branch protection rules and required reviews to add another layer of security and accountability for all code changes.

### Team permission levels

A team in a GitHub organization is a group of users who collaborate on shared repositories. Teams help streamline access management and communication by applying consistent permissions across multiple repositories at once. Key benefits include:

* **Centralized Access Control:** Assign repository permissions (e.g., Read, Write) to the entire team instead of managing each user individually.
* **Structured Collaboration:** Organize members by department, project, or role for more efficient collaboration.
* **Visibility \& Communication:** Each team can have its own discussion board, making it easier to share updates and coordinate efforts.

Teams provide an easy way to assign repository permissions to several related users at once. Members of a child team also inherit the permission settings of the parent team, providing an easy way to cascade permissions based on the natural structure of a company.

There are two levels of permissions at the team level:

| **Permission level** | **Description** |
| --- | --- |
| Member | Team members have the same set of abilities as organization members |
| Maintainer | Team maintainers can do everything team members can, plus:  \- Change the team's name, description, and visibility.  \- Request that the team change parent and child teams.  \- Set the team profile picture.  \- Edit and delete team discussions.  \- Add and remove organization members from the team.  \- Promote team members to also have the team maintainer permission.  \- Remove the team's access to repositories.  \- Manage code review assignment for the team.  \- Manage scheduled reminders for pull requests. |

An organization owner can also promote any member of the organization to be a maintainer for a team.

To audit access to a repository that you administer, you can view a combined list of teams and users with access to your repository in your settings:

GitHub offers several permission levels that can be assigned to teams. When you grant a team access to a repository, you can choose from the following permission models:

#### Permission Models

| Permission Level | Description | Best For |
| --- | --- | --- |
| **Read** | Users can view and clone the repository. Can open and comment on issues and pull requests. | Individuals who need read\-only or review access. |
| **Triage** | Users can manage issues and pull requests (e.g., label, assign, comment). Cannot push changes to the repository. | Project managers or contributors who need to triage and organize issues without contributing code. |
| **Write** | Users can push to branches (except protected branches). Can manage issues and pull requests. | Active contributors who need to commit code or update documentation. |
| **Maintain** | Users can manage repository settings, issues, and pull requests. Cannot delete or transfer the repository. | Project maintainers who handle routine repository management but don’t require full admin rights. |
| **Admin** | Users have full control over the repository, including setting permissions, deleting the repository, and managing all settings. | Those who need top\-level administrative access. |

**Tip:** Always follow the Principle of Least Privilege—assign the lowest permission level necessary for each team to perform its tasks effectively. This approach reduces the risk of accidental or unauthorized changes.

---

## Managing enterprise access, permissions, and governance

In the previous unit, you explored how repository and team permissions work in GitHub and how users are granted access at those levels. In this unit, you'll learn how to manage permissions and access at a broader scale across organizations and enterprises:

* Organization permissions
* Enterprise permissions
* Internal vs. external collaborators
* Least privilege strategies
* Security and governance best practices

### Organization permission levels

GitHub organizations provide a centralized way for teams to collaborate on projects while maintaining controlled access to repositories and sensitive data. Organization permissions determine what members and teams can do within the organization, ensuring that each user has the appropriate level of access.

There are multiple levels of permissions at the organizational level:

| **Permission level** | **Description** |
| --- | --- |
| Owner | Organization owners can do everything that organization members can do, and they can add or remove other users to and from the organization. This role should be limited to no less than two people in your organization. |
| Member | Organization members can create and manage organization repositories and teams. |
| Moderator | Organization moderators can block and unblock nonmember contributors, set interaction limits, and hide comments in public repositories that the organization owns. |
| Billing manager | Organization billing managers can view and edit billing information. |
| Security managers | Organization security managers can manage security alerts and settings across your organization. They can also read permissions for all repositories in the organization. |
| Outside collaborator | Outside collaborators, such as a consultant or temporary employee, can access one or more organization repositories. They aren't explicit members of the organization. |

In addition to these levels, you can also set default permissions for all members of your organization:

For improved management and security, you might also consider giving default read permissions to all members of your organization and adjusting their access to repositories on a case\-by\-case basis. If you have a relatively small organization with a low number of users, a low number of repositories, or a combination of the two, this level of restriction might be unnecessary. If you trust everyone with pushing changes to any repository, you might prefer to give all members write permissions by default.

### Enterprise permission levels

Recall from earlier that enterprise accounts are collections of organizations. By extension, each individual user account that is a member of an organization is also a member of the enterprise. You can control various settings related to authentication from this higher level.

There are three levels of permission at the enterprise level:

| **Permission level** | **Description** |
| --- | --- |
| Owner | Enterprise owners have complete control over the enterprise and can take every action, including:  \- Managing administrators.  \- Adding and removing organizations to and from the enterprise.  \- Managing enterprise settings.  \- Enforcing policies across organizations.  \- Managing billing settings. |
| Member | Enterprise members have the same set of abilities as organization members. |
| Billing manager | Enterprise billing managers can only view and edit your enterprise's billing information and add or remove other billing managers. |
| Guest collaborator | Can be granted access to repositories or organizations, but has limited access by default (Enterprise Managed Users only) |

In addition to these three levels, you can also set a policy of default repository permissions across all your organizations:

For improved management and security, you can give default read permissions to all members of your enterprise and adjust their access to repositories on a case\-by\-case basis. In a smaller enterprise, such as one with a single, relatively small organization, you might prefer to trust all members with write permissions by default.

To further streamline enterprise\-scale access control:

* **Nested Teams:** Enterprise accounts can use nested team structures to reflect departmental hierarchies. A parent team’s permissions cascade down to child teams, simplifying complex access management.
* **Automation \& Auditing:** You can use GitHub’s API or GitHub Actions to automate team creation and permission assignments, and audit access via organization or enterprise audit logs.

### Enterprise Permissions and Policies via Ruleset

This section covers how to manage enterprise permissions and policies through rulesets. We'll explore best practices for structuring organizations, setting default permissions, synchronizing teams via Active Directory (AD), automating multi\-org scripting, and aligning policies with your company’s trust and control positions.

#### Weighing the pros and cons of deploying a single versus multiple organizations

When structuring your enterprise, one of the key decisions is whether to use a single organization or multiple organizations. Each approach has unique benefits and trade\-offs.

##### Single Organization

| Pros | Cons |
| --- | --- |
| **Simplified Management:** Centralized control of permissions and policies. | **Limited Flexibility:** One\-size\-fits\-all policies might not suit all teams. |
| **Consistency:** Uniform application of rules and streamlined collaboration. | **Security Risks:** A single breach could impact the entire organization. |
| **Resource Sharing:** Easier asset sharing across teams. | **Scalability Issues:** Managing permissions can become complex as the organization grows. |
| **Cost Efficiency:** Reduced overhead in administrative tooling and licensing. |  |

##### Multiple Organizations

| Pros | Cons |
| --- | --- |
| **Tailored Policies:** Customize permissions to fit the specific needs of each team. | **Increased Complexity:** More organizations mean more administrative overhead. |
| **Enhanced Isolation:** Limits the impact of a security breach to a single organization. | **Redundancy:** Potential duplication of settings and management efforts. |
| **Decentralized Administration:** Teams can manage their own policies and permissions. | **Inter\-Org Collaboration:** May require extra tools or processes for cross\-organization projects. |

#### Setting default read versus default write across organizations

Deciding on the default permission level is critical to balancing security and collaboration within your enterprise.

##### Default Read vs Default Write

| Default Read | Default Write |
| --- | --- |
| **Enhanced Security:** Minimizes the risk of unintended modifications. | **Improved Collaboration:** Empowers users to contribute and modify content directly. |
| **Control:** Easier to audit and monitor changes. | **Efficiency:** Reduces bottlenecks in content creation and updates. |
| **Best For:** Environments where the majority of users only need to view resources. | **Risks:** Increases the chance of accidental changes or misconfigurations if not carefully managed. |

**Recommendation:**  

Use a default read permission model and grant write access selectively, ensuring adherence to the principle of least privilege.

#### Team synchronization through Active Directory (AD)

Using Active Directory (AD) for team synchronization makes user management and access control easier and more efficient.

##### Why use AD sync?

* **Single source of truth:** Keeps user identities consistent across your organization.
* **Automated access management:** Streamlines onboarding, offboarding, and role updates.
* **Seamless role alignment:** Ensures AD groups match enterprise roles and permissions.

##### Things to consider before implementing

* **Role mapping:** Clearly define how AD groups align with your organization's roles.
* **Sync frequency:** Set a schedule that balances performance and security.
* **Compliance \& auditing:** Log all changes to meet compliance requirements.

By planning ahead, you can ensure a smooth integration that keeps your organization secure and well\-organized.

#### Maintainability: scripting for multiple organizations and access rights

As your enterprise scales, automating the management of permissions across multiple organizations is essential for maintainability.

##### Key Practices

This section highlights key practices for scripting and automation to manage permissions consistently and securely as your enterprise grows. Following these practices helps streamline administration, minimize manual errors, and maintain strong governance.

* **Modularity:** Develop scripts in modular components to handle different organizations with minimal changes.
* **Reusability:** Create reusable functions or modules to perform common permission tasks.
* **Testing:** Thoroughly test scripts in a controlled environment before deployment.
* **Logging:** Implement detailed logging to track changes and facilitate troubleshooting.
* **Version Control:** Use version control systems (like Git) to manage script revisions and collaborate with team members.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/_

## Fuentes
- [Introduction to GitHub administration](https://learn.microsoft.com/en-us/training/modules/github-introduction-administration/?WT.mc_id=api_CatalogApi)
