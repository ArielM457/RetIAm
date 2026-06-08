# Introduction to GitHub

> Curso: GitHub fundamentals - Administration basics and product features Part 1 of 2 (github-github-administration-products-1) · Seccion: GitHub fundamentals - Administration basics and product features Part 1 of 2
> Duracion estimada: 105 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Components of the GitHub flow

In this unit, we're reviewing the following components of the GitHub flow:

* Branches
* Commits
* Pull Requests
* The GitHub Flow
* Git flow

### Components of GitHub Flow

Before we get into GitHub\-specific workflows, it's helpful to understand that GitHub Flow builds directly on Git’s foundational concepts.

Git provides tools to track and manage changes in your code over time. GitHub builds on this by making it easier to use those tools with features like branches, commits, pull requests, and visual interfaces for collaboration. Let’s start by looking at how these concepts work in GitHub.

### What are branches

In the last section, we created a new file and a new branch in your repository.

Branches are an essential part of the GitHub experience. They let you make changes without affecting the default branch.

Your branch is a safe place to experiment with new features or fixes. If you make a mistake, you can revert your changes or push more changes to fix the mistake. Your changes won't update on the default branch until you merge your branch.

Note

Alternatively, you can create a new branch and check it out by using git in a terminal. The command would be
`git checkout -b newBranchName`

### What are commits

In the previous unit, you added a new file into the repository by pushing a commit. Let’s briefly review what commits are.

A **commit** is a change to one or more files on a branch. Each commit is tracked by a unique ID, timestamp, and contributor, regardless of whether it's made via the command line or directly in GitHub's web interface. Commits provide a clear audit trail for anyone reviewing the history of a file or linked item, such as an issue or pull request.

> You can create a commit using Git in your terminal with:
> 
> 
> 
> ```
> git commit -m "Add a helpful commit message"
> 
> ```

Within a git repository, a file can exist in several valid states as it goes through the version control process. The primary states for a file in a Git repository are **Untracked** and **Tracked**.

**Untracked:** An initial state of a file when it isn't yet part of the Git repository. Git is unaware of its existence.

**Tracked:** A tracked file is one that Git is actively monitoring. It can be in one of the following substates:

* **Unmodified:** The file is tracked, but it hasn't been modified since the last commit.
* **Modified:** The file has been changed since the last commit, but these changes aren't yet staged for the next commit.
* **Staged:** The file has been modified, and the changes have been added to the staging area (also known as the index). These changes are ready to be committed.
* **Committed:** The file is in the repository's database. It represents the latest committed version of the file.

These states help your team understand the status of each file and where it is in the version control process.

### What are pull requests?

A **pull request** is the mechanism used to signal that the commits from one branch are ready to be merged into another branch.

The team member submitting the **pull request** asks one or more reviewers to verify the code and approve the merge. These reviewers have the opportunity to comment on changes, add their own, or use the pull request itself for further discussion.

GitHub also supports *Draft Pull Requests*, which let you open a pull request that's not yet ready for review.

Once the changes have been approved (if required), the pull request's source branch (the compare branch) is merged into the base branch.

Now that you’ve seen how branches, commits, and pull requests work, let’s walk through how they come together in GitHub Flow.

### The GitHub flow

The GitHub flow is a simple workflow that helps you safely make and share changes. It’s great for trying out ideas and collaborating with your team using branches, pull requests, and merges.

Note

GitHub flow is one of several popular workflows. Others include Git flow and trunk\-based development.

Now that we know the basics of GitHub we can walk through the GitHub flow and its components.

1. Start by creating a branch so your changes, features, or fixes don’t affect the main branch.
2. Next, make your updates in the branch. If your workflow supports it, you can deploy changes from this branch to test them before merging.
3. Now, open a pull request to invite feedback and begin a review.
4. Then, review the comments and make any necessary updates based on your team’s feedback.
5. Finally, once you’re confident in your changes, get approval and merge the pull request into the main branch.
6. After that, delete the branch to keep your repository clean and avoid using outdated branches.

### Git flow

While GitHub Flow is a lightweight workflow designed for continuous delivery, **Git flow** is a more structured branching model often used in release\-driven environments. Git flow has been around longer than GitHub Flow, and you may still see the term **`master`** used instead of **`main`** as the default branch.

*Image by Vincent Driessen, from ['A successful Git branching model'](https://nvie.com/posts/a-successful-git-branching-model/)*

#### Git flow Branch Types

Git flow uses several long\-lived and temporary branches:

* **master**: Always reflects production\-ready code.
* **develop**: Contains the latest development work for the next release.
* **feature/**\*: Used to create new features; branched from `develop` and merged back when complete.
* **release/**\*: Prepares a new production release from `develop`; allows final testing and minor bug fixes.
* **hotfix/**\*: Used to quickly patch production issues; branched from `master`.

#### How the Git flow Process Works

1. Developers create **feature branches** from `develop` to build new functionality.
2. When it's time for a release, a **release branch** is created from `develop`. This isolates release preparation work so development can continue uninterrupted.
3. Bug fixes can be added to the release branch, but major features should wait for a future release.
4. Once ready, the release branch is merged into `master` and tagged with a version number. GitHub can use these tags to help you generate release notes.
5. The same release branch should be merged back into `develop` to keep it in sync.
6. If a critical production bug arises, a **hotfix branch** is created from `master`. Once fixed, it’s merged into both `master` and `develop`.

#### When to Use Git flow

* Best suited for projects with **scheduled or versioned releases**
* Helpful if you maintain **multiple production versions** (e.g., long\-term support branches)
* Ideal for **slower, more structured development cycles** (e.g., enterprise or regulated environments)
* Considered more "heavyweight" than GitHub Flow due to **additional branch management**

Note

Git flow assumes merge commits for integrating branches. Using rebase or squash merges can interfere with its branch structure and history tracking.

> For many teams using GitHub, GitHub Flow is simpler and faster. But if your team values predictability and needs more release planning, Git flow may be a better fit.

Congratulations! You’ve just walked through the full GitHub Flow—and explored how Git flow offers a structured alternative for release\-driven projects.

Let’s move onto the next section where we’ll cover the differences between issues and discussions.

---

## GitHub is a collaborative platform

Collaboration is at the core of everything GitHub does. We went over repositories in the first unit of the module and learned that repositories help you organize your project and its files. In the last unit, we learned about pull requests, which is a way to keep track of changes made to your project.

In this unit, we're learning about issues and discussions. These are features that contribute to the collaborative nature of the GitHub Enterprise Platform.

### Issues

GitHub Issues are used to track ideas, feedback, tasks, or bugs for work on GitHub. Issues can be created in various ways, so you can choose the most convenient method for your workflow.

This walkthrough covers how to create an issue from a repository. Issues can also be created from:

* An item in a task list.
* A note in a project.
* A comment in an issue or pull request.
* A specific line of code.
* A URL query.

#### Creating an issue from a repository

1. On GitHub.com, navigate to the main page of the repository.
2. Under your repository name, select **Issues**.
3. Select **New issue**. This should open a blank issue field for you to fill.
4. If your repository uses issue templates, you should get a list of issues types, select the one you'd like to use.

If the type of issue you'd like to open isn't included in the available options, select **Blank issue**. If not using templates, skip to Step 5\.

If your repository uses issue forms, you'll see a structured form to fill out instead of a blank issue template. Issue forms allow maintainers to collect specific information in a standardized format.
5. In the **Add a title** field, enter a title for your issue.
6. In the **Add a description** field, type a description of your issue.
7. If you're a project maintainer, you can assign the issue to someone, add it to a project board, associate it with a milestone, or apply a label.
8. When you're finished, select **Submit new issue**.

Use labels, mentions, and reactions to manage collaboration effectively and increase issue visibility. Issue templates help maintain consistent structure and expectations for contributors.

Some conversations may be more appropriate for GitHub Discussions. Use GitHub Discussions to ask and answer questions, share information, make announcements, and conduct or participate in conversations about a project.

In the next section, we’ll review Discussions and how to best utilize the feature.

### Discussions

Discussions are designed for conversations that aren’t necessarily tied to code—such as Q\&A, ideas, or general feedback. They support open, ongoing communication within a shared forum and can be public or private, depending on the repository's visibility.

In this section, you'll learn how to:

* Enabling a discussion in your repository.
* Creating a new discussion and various discussion categories.

Let’s dive into enabling a discussion in your repository.

#### Enabling a discussion in your repository

Repository owners and those with Write access can enable GitHub Discussions for a community on their public and private repositories. The visibility of a discussion inherits visibility from the repository they’re created in.

When you first enable GitHub Discussions, you're prompted to configure a welcome post.

1. On GitHub.com, navigate to the main page of the repository.
2. Under your repository name, select **Settings**.
3. Scroll down to the **Features** section and under **Discussions**, select **Setup discussions**.
4. Under **Start a new discussion**, edit the template to match your community's tone and resources.
5. Select **Start discussion**.

You're now ready to create a new discussion.

#### Create a new discussion

Any authenticated user who can view the repository can create a discussion in that repository. For organization\-level discussions, any user who can view the source repository can also create a discussion.

1. On GitHub.com, navigate to the main page of the repository or organization where you want to start a discussion.
2. Under your repository or organization name, select **Discussions**.
3. On the right side of the page, select **New discussion**.
4. Select a discussion category by choosing **Get started**. All discussions must be placed in a category. Repository maintainers define these categories.

Each discussion category includes a unique name, emoji, and description to clarify its purpose. Categories help maintainers organize how conversations are filed. They're customizable to help distinguish categories that are Q\&A or more open\-ended conversations. The following table shows the default categories for discussions and their purpose.

| **Category** | **Purpose** | **Format** |
| --- | --- | --- |
| 📣 Announcements | Updates and news from project maintainers | Announcement |
| \#️⃣ General | Anything and everything relevant to the project | Open\-ended discussion |
| 💡 Ideas | Ideas to change or improve the project | Open\-ended discussion |
| 🗳️ Polls | Polls with multiple options for the community to vote for and discuss | Polls |
| 🙏 Q\&A | Questions for the community to answer, with a question/answer format | Question and Answer |
| 🙌 Show and tell | Creations, experiments, or tests relevant to the project | Open\-ended discussion |

Repository maintainers can pin important discussions to the top of the Discussions tab for better visibility.

1. Under **Discussion title** enter a title for your discussion, and under **Write** enter the body of your discussion.
2. Select **Start discussion**.

That covers how GitHub supports collaboration through Issues and Discussions. Now let's move to how you can manage notifications, subscribe to threads, and get started with GitHub pages.

#### Marking a comment as an answer

In a Q\&A style discussion, you can mark a comment as the accepted answer to the original question.

1. Navigate to the discussion.
2. Locate the comment that best answers the original question.
3. Select **Mark as answer** below the comment.

The comment will be highlighted, making it easy for others to find the solution quickly. You can also unmark an answer if needed.

#### Reference a discussion in an issue

If a discussion leads to work that needs to be tracked, you can convert the discussion into an issue.

1. Navigate to the discussion you want to convert.
2. Select the **`...`** (three dots) menu at the top\-right of the discussion.
3. Select **Reference in new issue**.
4. Confirm the new issue title and body.

This keeps track of actionable work that originates from community conversations.

#### Pinning a discussion

You can pin important discussions to the top of the Discussions page for better visibility.

1. Navigate to the discussion you want to pin.
2. Select the **`...`** (three dots) menu at the top\-right of the discussion.
3. Select **Pin discussion**.

Pinned discussions are helpful for highlighting announcements, important questions, or ongoing topics the community should notice.

---

## GitHub platform management

Now that you know the basics of the GitHub platform, this section covers platform management topics.

In this unit, we'll cover:

* Managing notifications and subscriptions.
* Subscribing to threads and finding threads where you're mentioned.
* Publicizing your project or organization on GitHub pages.

### Managing notifications and subscriptions

Notifications help you stay up to date on important activity across your repositories and teams. Managing your subscriptions ensures you only get updates for the work that matters most to you.

You can subscribe to notifications for:

* Specific issues, pull requests, or gists
* Repository activity like issues, pull requests, releases, or discussions
* Workflow statuses for repositories using GitHub Actions
* All activity across a repository

You're automatically subscribed when you interact with conversations (commenting, opening an issue, being assigned), but you can also manually manage subscriptions as needed.

If you're no longer interested in receiving updates, you can unsubscribe, unwatch, or customize the types of notifications you receive.

### Subscribing to threads and finding threads where you're mentioned

You can also access detailed notification settings by navigating to your GitHub user settings and choosing 'Notifications' to configure delivery channels such as email, web, and mobile.

If you want to keep an eye on issues or pull requests that mention a specific user, use the search qualifier *mentions:* followed by the username.

To make sure you get updates about a particular thread (like an issue or pull request), you can subscribe to it—even if you weren’t originally part of the conversation.

You can subscribe to a thread by:

* Selecting **Subscribe** on the right\-hand sidebar of an issue, pull request, or discussion.

To find conversations where you're mentioned:

* Use the search qualifier `mentions:<username>` in the GitHub search bar to locate issues and pull requests where you were @mentioned.

This way, you won’t miss any conversations that need your attention.

#### Filter notifications

GitHub allows you to filter notifications using watch settings:

* **Watching**: Receive notifications for all activity.
* **Not watching**: Receive notifications only when you're participating or @mentioned.
* **Ignore**: No notifications at all for a repository.
* **Custom**: Fine\-tune what types of activity (like pull requests, issues, or discussions) trigger notifications.

You can manage watch settings by selecting **Watch** at the top of a repository page.

#### Configure notification settings

You can configure where you receive notifications:

* **Email**: Notifications delivered to your registered email address.
* **Web**: Notifications viewed directly in your GitHub dashboard.
* **Mobile**: Push notifications using the GitHub mobile app.
* **Custom notifications**: Configure specific event types for different channels.

Notification settings are managed under your GitHub account settings in **Notifications**.

### What are GitHub Pages?

Now let’s take a look at GitHub Pages. You can use GitHub Pages to publicize and host a website about yourself, your organization, or your project directly from a repository on GitHub.com.

GitHub Pages is a static site\-hosting service that takes HTML, CSS, and JavaScript files straight from a repository on GitHub. Optionally, you can run the files through a build process and publish a website. You can specify a source branch and folder (e.g., `/docs`) for your Pages site, and GitHub will host the content publicly.

Next, you'll complete a hands\-on activity to reinforce key GitHub skills. In the next exercise, you'll:

* Create a new repository.
* Create a new branch.
* Commit a file.
* Open a pull request.
* And merge a pull request.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/introduction-to-github/_

## Fuentes
- [Introduction to GitHub](https://learn.microsoft.com/en-us/training/modules/introduction-to-github/?WT.mc_id=api_CatalogApi)
