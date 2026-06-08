# Work with compute targets in Azure Machine Learning

> Curso: Train and manage a machine learning model with Azure Machine Learning (wwl-train-deploy-machine-learning-model) · Seccion: Train and manage a machine learning model with Azure Machine Learning
> Duracion estimada: 37 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

As a data scientist, you can train machine learning models on your local device. For large\-scale projects, a single local device can limit you to efficiently train machine learning models. When you use cloud compute for machine learning workloads, you're ready to scale your work when needed.

In Azure Machine Learning, you can use various types of managed cloud computes. By using any of the compute options in the Azure Machine Learning workspace, you can save time on managing compute.

Whether you're working in notebooks during experimentation, or need to run scripts for production, Azure Machine Learning compute helps you run your workloads at scale.

---

## Choose the appropriate compute target

In Azure Machine Learning, *compute targets* are physical or virtual computers on which jobs are run.

### Understand the available types of compute

Azure Machine Learning supports multiple types of compute for experimentation, training, and deployment. By having multiple types of compute, you can select the most appropriate type of compute target for your needs.

* **Compute instance**: Behaves similarly to a virtual machine and is primarily used to run notebooks. It's ideal for *experimentation*.
* **Compute clusters**: Multi\-node clusters of virtual machines that automatically scale up or down to meet demand. A cost\-effective way to run scripts that need to process large volumes of data. Clusters also allow you to use parallel processing to distribute the workload and reduce the time it takes to run a script.
* **Kubernetes clusters**: Cluster based on Kubernetes technology, giving you more control over how the compute is configured and managed. You can attach your self\-managed Azure Kubernetes (AKS) cluster for cloud compute, or an Arc Kubernetes cluster for on\-premises workloads.
* **Attached compute**: Allows you to attach existing compute like Azure virtual machines or Azure Databricks clusters to your workspace.
* **Serverless compute**: A fully managed, on\-demand compute you can use for training jobs.

Note

Azure Machine Learning offers you the option to create and manage your own compute or to use compute that is fully managed by Azure Machine Learning.

### When to use which type of compute?

In general, there are some best practices that you can follow when working with compute targets. To understand how to choose the appropriate type of compute, several examples are provided. Remember that which type of compute you use always depends on your specific situation.

#### Choose a compute target for experimentation

Imagine you're a data scientist and you're asked to develop a new machine learning model. You likely have a small subset of the training data with which you can experiment.

During experimentation and development, you prefer working in a Jupyter notebook. A notebook experience benefits most from a compute that is continuously running.

Many data scientists are familiar with running notebooks on their local device. A cloud alternative managed by Azure Machine Learning is a *compute instance*. Alternatively, you can also opt for *Spark serverless compute* to run Spark code in notebooks, if you want to make use of Spark's distributed compute power.

#### Choose a compute target for production

After experimentation, you can train your models by running Python scripts to prepare for production. Scripts will be easier to automate and schedule for when you want to retrain your model continuously over time. You can run scripts as (pipeline) jobs.

When moving to production, you want the compute target to be ready to handle large volumes of data. The more data you use, the better the machine learning model is likely to be.

When training models with scripts, you want an on\-demand compute target. A *compute cluster* automatically scales up when the script(s) need to be executed, and scales down when the script finishes executing. If you want an alternative that you don't have to create and manage, you can use Azure Machine Learning's *serverless compute*.

#### Choose a compute target for deployment

The type of compute you need when using your model to generate predictions depends on whether you want batch or real\-time predictions.

For batch predictions, you can run a pipeline job in Azure Machine Learning. Compute targets like compute clusters and Azure Machine Learning's serverless compute are ideal for pipeline jobs as they're on\-demand and scalable.

When you want real\-time predictions, you need a type of compute that is running continuously. Real\-time deployments therefore benefit from more lightweight (and thus more cost\-efficient) compute. Containers are ideal for real\-time deployments. When you deploy your model to a managed online endpoint, Azure Machine Learning creates and manages containers for you to run your model. Alternatively, you can attach Kubernetes clusters to manage the necessary compute to generate real\-time predictions.

---

## Create and use a compute instance

When you want to execute code in notebooks, you can choose to use a **compute instance** managed by Azure Machine Learning. You can create a compute instance in the Azure Machine Learning studio, using the Azure command\-line interface (CLI), or the Python software development kit (SDK).

### Create a compute instance with the Python SDK

To create a compute instance with the Python SDK, you can use the following code:

```
from azure.ai.ml.entities import ComputeInstance

ci_basic_name = "basic-ci-12345"
ci_basic = ComputeInstance(
    name=ci_basic_name, 
    size="STANDARD_DS3_v2"
)
ml_client.begin_create_or_update(ci_basic).result()

```

To understand which parameters the `ComputeInstance` class expects, you can review the [reference documentation](/en-us/python/api/azure-ai-ml/azure.ai.ml.entities.computeinstance?azure-portal=true).

Note

Compute instances need to have a unique name across an Azure region (for example within west europe). If the name already exists, an error message will tell you to try again with another name.

Alternatively, you can also create a compute instance by using a script. With a script, you ensure that any necessary packages, tools, or software is automatically installed on the compute and you can clone any repositories to the compute instance. When you need to create compute instances for multiple users, using a script allows you to create a consistent development environment for everyone.

Tip

Learn more about [how to customize the compute instance with a script](/en-us/azure/machine-learning/how-to-customize-compute-instance?azure-portal=true).

#### Assign a compute instance to a user

As a data scientist, you can attach a compute instance to notebooks to run cells within the notebook. To be allowed to work with the compute instance, it needs to be assigned to you as a user.

A compute instance can only be assigned to *one* user, as the compute instance can't handle parallel workloads. When you create a new compute instance, you can assign it to someone else if you have the appropriate permissions.

#### Minimize compute time

When you're actively working on code in a notebook, you want your compute instance to be running. When you're not executing any code, you want your compute instance to be stopped to save on costs.

When a compute instance is assigned to you, you can start and stop a compute instance whenever you need. You can also add a schedule to the compute instance to start or stop at set times. Additionally, you can configure a compute to automatically shut down when it has been idle for a set amount of time.

By scheduling your compute instance to stop at the end of every day, you avoid unnecessary costs if you forget to stop a compute instance.

### Use a compute instance

To use a compute instance, you need an application that can host notebooks. The easiest option to work with the compute instance is through the integrated notebooks experience in the Azure Machine Learning studio.

You can prefer to work with Visual Studio Code for easier source control of your code. If you want to edit and run code in Visual Studio Code, you can attach a compute instance to run notebook cells remotely.

Tip

Learn more about [how to create and manage an Azure Machine Learning compute instance](/en-us/azure/machine-learning/how-to-create-manage-compute-instance?azure-portal=true).

---

## Create and use a compute cluster

After experimentation and development, you want your code to be production\-ready. When you run code in production environments, it's better to use scripts instead of notebooks. When you run a script, you want to use a compute target that is scalable.

Within Azure Machine Learning, **compute clusters** are ideal for running scripts. You can create a compute cluster in the Azure Machine Learning studio, using the Azure command\-line interface (CLI), or the Python software development kit (SDK).

### Create a compute cluster with the Python SDK

To create a compute cluster with the Python SDK, you can use the following code:

```
from azure.ai.ml.entities import AmlCompute

cluster_basic = AmlCompute(
    name="cpu-cluster",
    type="amlcompute",
    size="STANDARD_DS3_v2",
    location="westus",
    min_instances=0,
    max_instances=2,
    idle_time_before_scale_down=120,
    tier="low_priority",
)
ml_client.begin_create_or_update(cluster_basic).result()

```

To understand which parameters the `AmlCompute` class expects, you can review the [reference documentation](/en-us/python/api/azure-ai-ml/azure.ai.ml.entities.amlcompute?azure-portal=true).

When you create a compute cluster, there are three main parameters you need to consider:

* `size`: Specifies the *virtual machine type* of each node within the compute cluster. Based on the [sizes for virtual machines in Azure](/en-us/azure/virtual-machines/sizes?azure-portal=true). Next to size, you can also specify whether you want to use CPUs or GPUs.
* `max_instances`: Specifies the *maximum number of nodes* your compute cluster can scale out to. The number of parallel workloads your compute cluster can handle is analogous to the number of nodes your cluster can scale to.
* `tier`: Specifies whether your virtual machines are *low priority* or *dedicated*. Setting to low priority can lower costs as you're not guaranteed availability.

### Use a compute cluster

There are three main scenarios in which you can use a compute cluster:

* Running a pipeline job you built in the Designer.
* Running an Automated Machine Learning job.
* Running a script as a job.

In each of these scenarios, a compute cluster is ideal as a compute cluster automatically scales up when a job is submitted, and automatically shut down when a job is completed.

A compute cluster also allows you to train multiple models in parallel, which is a common practice when using Automated Machine Learning.

You can run a Designer pipeline job and an Automated Machine Learning job through the Azure Machine Learning studio. When you submit the job through the studio, you can set the compute target to the compute cluster you created.

When you prefer a code\-first approach, you can set the compute target to your compute cluster by using the Python SDK.

For example, when you run a script as a command job, you can set the compute target to your compute cluster with the following code:

```
from azure.ai.ml import command

## configure job
job = command(
    code="./src",
    command="python diabetes-training.py",
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    compute="cpu-cluster",
    display_name="train-with-cluster",
    experiment_name="diabetes-training"
    )

## submit job
returned_job = ml_client.create_or_update(job)
aml_url = returned_job.studio_url
print("Monitor your job at", aml_url)

```

After submitting a job that uses a compute cluster, the compute cluster scales out to one or more nodes. Resizing takes a few minutes, and your job starts running once the necessary nodes are provisioned. When a job's status is *preparing*, the compute cluster is being prepared. When the status is *running*, the compute cluster is ready, and the job is running.

---

## Exercise \- Work with compute resources

Now, it's your chance to explore how to work with compute resources in Azure Machine Learning.

In this exercise, you learn how to:

* Create and use a compute instance.
* Create and use a compute cluster.

### Instructions

Launch the exercise and follow the instructions.

---

## Summary

In this module, you've learned how to:

* Choose the appropriate compute target.
* Create and use a compute instance.
* Create and use a compute cluster.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/work-compute-resources-azure-machine-learning/_

## Fuentes
- [Work with compute targets in Azure Machine Learning](https://learn.microsoft.com/en-us/training/modules/work-compute-resources-azure-machine-learning/?WT.mc_id=api_CatalogApi)
