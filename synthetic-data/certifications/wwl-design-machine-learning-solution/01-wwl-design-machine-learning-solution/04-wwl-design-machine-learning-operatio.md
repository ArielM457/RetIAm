# Design a machine learning operations solution

> Curso: Design a machine learning solution (wwl-design-machine-learning-solution) · Seccion: Design a machine learning solution
> Duracion estimada: 36 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Imagine you trained a model. The next step is to operationalize the model and to make sure whoever needs the predictions can consume them.

**Machine Learning operations** or **MLOps** help you to scale your model from a proof of concept or pilot project to production. A model in production is ready for large\-scale deployment and is retrained and redeployed when necessary.

Implementing MLOps helps you to make your machine learning workloads robust and reproducible.

You'll learn about a typical MLOps architecture and what you need to consider to bring a model to production.

### Learning objectives

In this module, you will:

* Explore an MLOps architecture.
* Design for monitoring.
* Design for retraining.

---

## Explore an MLOps architecture

As a data scientist, you want to train the best machine learning model. To implement the model, you want to deploy it to an endpoint and integrate it with an application.

Over time, you may want to retrain the model. For example, you can retrain the model when you have more training data.

In general, once you've trained a machine learning model, you want to get the model ready for enterprise\-scale. To prepare the model and operationalize it, you want to:

* Convert the model training to a **robust** and **reproducible** pipeline.
* Test the code and the model in a **development** environment.
* Deploy the model in a **production** environment.
* **Automate** the end\-to\-end process.

### Set up environments for development and production

Within MLOps, similarly to DevOps, an **environment** refers to a collection of resources. These resources are used to deploy an application, or with machine learning projects, to deploy a model.

Note

In this module, we refer to the DevOps interpretation of environments. Note that Azure Machine Learning also uses the term environments to describe a collection of Python packages needed to run a script. These two concepts of environments are independent from each other.

How many environments you work with, depends on your organization. Commonly, there are at least two environments: *development* or *dev* and *production* or *prod*. Plus, you can add environments in between like a staging or *pre\-production* (*pre\-prod*) environment.

A typical approach is to:

* Experiment with model training in the *development* environment.
* Move the best model to the *staging* or *pre\-prod* environment to deploy and test the model.
* Finally release the model to the *production* environment to deploy the model so that end\-users can consume it.

#### Organize Azure Machine Learning environments

When you implement MLOps, and work with machine learning models at a large scale, it's a best practice to work with separate environments for different stages.

Imagine your team uses a dev, pre\-prod, and prod environment. Not everyone on your team should get access to all environments. Data scientists may only work within the dev environment with non\-production data, while machine learning engineers work on deploying the model in the pre\-prod and prod environment with production data.

Having separate environments makes it easier to control access to resources. Each environment can then be associated with a separate Azure Machine Learning workspace.

Within Azure, you use role\-based access control (RBAC) to give colleagues the right level of access to the subset of resources they need to work with.

Alternatively, you can use only one Azure Machine Learning workspace. When you use one workspace for development and production, you have a smaller Azure footprint and less management overhead. However, RBAC applies to both dev and prod environments, which may mean that you're giving people too little or too much access to resources.

Tip

Learn more about [best practices to organize Azure Machine Learning resources](/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/ai-machine-learning-resource-organization).

### Design an MLOps architecture

Bringing a model to production means you need to scale your solution and work together with other teams. Together with other data scientists, data engineers and an infrastructure team, you may decide on using the following approach:

* Store all data in an Azure Blob storage, managed by the data engineer.
* The infrastructure team creates all necessary Azure resources, like the Azure Machine Learning workspace.
* Data scientists focus on what they do best: developing and training the model (inner loop).
* Machine learning engineers deploy the trained models (outer loop).

As a result, your MLOps architecture includes the following parts:

1. **Setup**: Create all necessary Azure resources for the solution.
2. **Model development (inner loop)**: Explore and process the data to train and evaluate the model.
3. **Continuous integration**: Package and register the model.
4. **Model deployment (outer loop)**: Deploy the model.
5. **Continuous deployment**: Test the model and promote to production environment.
6. **Monitoring**: Monitor model and endpoint performance.

When you're working with larger teams, you're not expected to be responsible of all parts of the MLOps architecture as a data scientist. To prepare your model for MLOps however, you should think about how to design for monitoring and retraining.

---

## Design for monitoring

As part of a machine learning operations (MLOps) architecture, you should think about how to monitor your machine learning solution.

**Monitoring** is beneficial in any MLOps environment. You'll want to monitor the *model*, the *data*, and the *infrastructure* to collect metrics that help you decide on any necessary next steps.

### Monitor the model

Most commonly, you want to monitor the performance of your model. During development, you use MLflow to train and track your machine learning models. Depending on the model you train, there are different metrics you can use to evaluate whether the model is performing as expected.

To monitor a model in production, you can use the trained model to generate predictions on a small subset of new incoming data. By generating the performance metrics on that test data, you're able to verify whether the model is still achieving its goal.

Additionally, you may also want to monitor for any responsible artificial intelligence (AI) issues. For example, whether the model is making fair predictions.

Before you can monitor a model, it's important to decide which performance metrics you want to monitor and what the benchmark for each metric should be. When should you be alerted that the model isn't accurate anymore?

### Monitor the data

You typically train a machine learning model using a historical dataset that is representative of the new data that your model receives when deployed. However, over time there may be trends that change the profile of the data, making your model less accurate.

For example, suppose a model is trained to predict the expected gas mileage of an automobile based on the number of cylinders, engine size, weight, and other features. Over time, as car manufacturing and engine technologies advance, the typical fuel\-efficiency of vehicles might improve dramatically; making the model's predictions trained on older data less accurate.

This change in data profiles between current and the training data is known as data drift, and it can be a significant issue for predictive models used in production. It's therefore important to be able to monitor data drift over time, and retrain models as required to maintain predictive accuracy.

### Monitor the infrastructure

Next to monitoring the model and data, you should also monitor the infrastructure to minimize cost and optimize performance.

Throughout the machine learning lifecycle, you use compute to train and deploy models. With machine learning projects in the cloud, compute may be one of your biggest expenses. You therefore want to monitor whether you are efficiently using your compute.

For example, you can monitor the compute utilization of your compute during training and during deployment. By reviewing compute utilization, you know whether you can scale down your provisioned compute, or whether you need to scale out to avoid capacity constraints.

Tip

Learn more about [monitoring the Azure Machine Learning workspace and its resources](/en-us/azure/machine-learning/monitor-azure-machine-learning?azure-portal=true).

---

## Design for retraining

When preparing your model for production in a machine learning operations (MLOps) solution, you need to design for retraining.

Generally, there are two approaches to when you want to retrain a model:

* Based on a **schedule**: when you know you always need the latest version of the model, you can decide to retrain your model every week, or every month, based on a schedule.
* Based on **metrics**: if you only want to retrain your model when necessary, you can monitor the model's performance and data drift to decide when you need to retrain the model.

In either case, you need to design for retraining. To easily retrain your model, you should prepare your code for automation.

### Prepare your code

Ideally, you should train models with **scripts** instead of notebooks. Scripts are better suited for automation. You can add **parameters** to a script and change input parameters like the training data or hyperparameter values. When you parameterize your scripts, you can easily retrain the model on new data if needed.

Another important thing to prepare your code is to host the code in a central repository. A repository refers to a location where all relevant files to a project are stored. With machine learning projects, Git\-based repositories are ideal to achieve **source control**.

When you apply source control to your project, you can easily collaborate on a project. You can assign someone to improve the model by updating the code. You'll be able to see past changes, and you can review changes before they're committed to the main repository.

### Automate your code

When you want to automatically execute your code, you can configure Azure Machine Learning jobs to run scripts. In Azure Machine Learning, you can create and schedule pipelines to run scripts too.

If you want scripts to run based on a trigger or event happening outside of Azure Machine Learning, you may want to trigger the Azure Machine Learning job from another tool.

Two tools that are commonly used in MLOps projects are Azure DevOps and GitHub (Actions). Both tools allow you to create automation pipelines and can trigger Azure Machine Learning pipelines.

As a data scientist, you may prefer to work with the Azure Machine Learning Python SDK. However, when working with tools like Azure DevOps and GitHub, you may prefer to configure the necessary resources and jobs with the Azure Machine Learning CLI extension instead. The Azure CLI is designed for automating tasks and may be easier to use with Azure DevOps and GitHub.

Tip

If you want to learn more about MLOps, explore the [introduction to machine learning operations (MLOps)](/en-us/training/paths/introduction-machine-learn-operations/?azure-portal=true) or try to build your first [MLOps automation pipeline with GitHub Actions](/en-us/training/paths/build-first-machine-operations-workflow/?azure-portal=true)

---

## Knowledge check

Note

To complete this exercise, read the case study. At the end, you'll be asked to give advice by answering the knowledge check questions.

Welcome to Proseware! You've been hired as the *lead data scientist* to help us design a machine learning deployment solution.

### Understand the problem

At Proseware, we're developing a **mobile application** that helps doctors diagnose diseases in patients faster. A doctor can enter the patient's medical data into the app to get a diagnosis for the patient.

Our first planned feature is that the app tells the doctor *whether the patient should be further screened or treated for diabetes*.

We have already collected data that correlates with diabetes, such as the number of pregnancies, age, and body mass index (BMI). We also have a team of data scientists working on training a model that can classify whether a patient is likely to have diabetes.

We need your help deciding how to design for bringing the model to production.

We're looking forward to your advice on **how to design the machine learning operations (MLOps) solution**!

### Consider the requirements

* **Consider the environments**. Currently, we're working in a small team and you're the only data scientist involved. We want to see whether this project is successful before actually scaling up and getting a large team involved.
* **Consider the model**. As the model is used to help doctors, accuracy is important to us. The model should only be in use when we know it's performing as expected.
* **Consider the data**. We're starting small and will mostly use the deployed model to test our application. The data the deployed model generates predictions on shouldn't be used to retrain the model as it may be biased.

---

## Summary

In this module, you've learned how to:

* Explore an MLOps architecture.
* Design for monitoring.
* Design for retraining.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/design-machine-learning-operations-solution/_

## Fuentes
- [Design a machine learning operations solution](https://learn.microsoft.com/en-us/training/modules/design-machine-learning-operations-solution/?WT.mc_id=api_CatalogApi)
