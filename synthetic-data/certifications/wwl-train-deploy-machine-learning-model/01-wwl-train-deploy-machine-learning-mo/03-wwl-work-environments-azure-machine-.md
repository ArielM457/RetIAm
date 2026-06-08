# Work with environments in Azure Machine Learning

> Curso: Train and manage a machine learning model with Azure Machine Learning (wwl-train-deploy-machine-learning-model) · Seccion: Train and manage a machine learning model with Azure Machine Learning
> Duracion estimada: 42 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

As a data scientist, you want to write code that works in any development environment. Whether you're using local or cloud compute, the code should successfully execute to train a machine learning model for example.

To run code, you need to ensure necessary packages, libraries, and dependencies are installed on the compute you use to run the code. In Azure Machine Learning, **environments** list and store the necessary packages that you can reuse across compute targets.

Note

In this module, we refer to Azure Machine Learning's interpretation of environments. Note that the term environments is also used to describe other technical concepts. For example, in DevOps, environments refer to the collection of resources used for a specific phase in the application deployment, like the development or production environment. [Learn more about continuous deployment for machine learning.](/en-us/training/modules/continuous-deployment-for-machine-learning/?azure-portal=true)

---

## Understand environments

In an enterprise machine learning solution, where experiments may be run in various compute contexts, it can be important to be aware of the environments in which your experiment code is running. You can use Azure Machine Learning **environments** to create environments and specify runtime configuration for an experiment.

When you create an Azure Machine Learning workspace, **curated** environments are automatically created and made available to you. Alternatively, you can create and manage your own **custom** environments and register them in the workspace. Creating and registering custom environments makes it possible to define consistent, reusable runtime contexts for your experiments \- regardless of where the experiment script is run.

### What is an environment in Azure Machine Learning?

Python code runs in the context of a *virtual environment* that defines the version of the Python runtime to be used as well as the installed packages available to the code. In most Python installations, packages are installed and managed in environments using `conda` or `pip`.

To improve portability, you usually create environments in Docker containers that are in turn hosted on compute targets, such as your development computer, virtual machines, or clusters in the cloud.

Azure Machine Learning builds environment definitions into Docker images and conda environments. When you use an environment, Azure Machine Learning builds the environment on the **Azure Container registry** associated with the workspace.

Tip

When you create an Azure Machine Learning workspace, you can choose whether to use an existing Azure Container registry, or whether to let the workspace create a new registry for you when needed.

To view all available environments within the Azure Machine Learning workspace, you can list the environments in the studio, using the Azure CLI, or the Python SDK.

For example, to list the environments using the Python SDK:

```
envs = ml_client.environments.list()
for env in envs:
    print(env.name)

```

To review the details of a specific environment, you can retrieve an environment by its registered name:

```
env = ml_client.environments.get(name="my-environment", version="1")
print(env)

```

---

## Explore and use curated environments

**Curated environments** are prebuilt environments for the most common machine learning workloads, available in your workspace by default.

Curated environments use the prefix **AzureML\-** and are designed to provide for scripts that use popular machine learning frameworks and tooling.

For example, there are curated environments for when you want to run a script that trains a regression, clustering, or classification model with Scikit\-Learn.

To explore a curated environment, you can view it in the studio, using the Azure CLI, or the Python SDK.

The following command allows you to retrieve the description and tags of a curated environment with the Python SDK:

```
env = ml_client.environments.get("AzureML-sklearn-0.24-ubuntu18.04-py37-cpu", version=44)
print(env. description, env.tags)

```

### Use a curated environment

Most commonly, you use environments when you want to run a script as a (**command**) **job**.

To specify which environment you want to use to run your script, you reference an environment by its name and version.

For example, the following code shows how to configure a command job with the Python SDK, which uses a curated environment including Scikit\-Learn:

```
from azure.ai.ml import command

## configure job
job = command(
    code="./src",
    command="python train.py",
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    compute="aml-cluster",
    display_name="train-with-curated-environment",
    experiment_name="train-with-curated-environment"
)

## submit job
returned_job = ml_client.create_or_update(job)

```

### Test and troubleshoot a curated environment

As curated environments allow for faster deployment time, it's a best practice to first explore whether one of the pre\-created curated environments can be used to run your code.

You can verify that a curated environment includes all necessary packages by reviewing its details. Then, you can test by using the environment to run the script.

If an environment doesn't include all necessary packages to run your code, your job fails.

When a job fails, you can review the detailed error logs in the **Outputs \+ logs** tab of your job in the Azure Machine Learning studio.

A common error message that indicates your environment is incomplete, is `ModuleNotFoundError`. The module that isn't found is listed in the error message. By reviewing the error message, you can update the environment to include the libraries to ensure the necessary packages are installed on the compute target before running the code.

When you need to specify other necessary packages, you can use a curated environment as reference for your own custom environments by modifying the Dockerfiles that back these curated environments.

---

## Create and use custom environments

When you need to create your own environment in Azure Machine Learning to list all necessary packages, libraries, and dependencies to run your scripts, you can create **custom environments**.

You can define an environment from a Docker image, a Docker build context, and a conda specification with Docker image.

### Create a custom environment from a Docker image

The easiest approach is likely to be to create an environment from a Docker image. Docker images can be hosted in a public registry like [Docker Hub](https://hub.docker.com/?azure-portal=true) or privately stored in an Azure Container registry.

Many open\-source frameworks are encapsulated in public images to be found on Docker Hub. For example, you can find a public Docker image that contains all necessary packages to train a deep learning model with [PyTorch](https://hub.docker.com/r/pytorch/pytorch?azure-portal=true).

To create an environment from a Docker image, you can use the Python SDK:

```
from azure.ai.ml.entities import Environment

env_docker_image = Environment(
    image="pytorch/pytorch:latest",
    name="public-docker-image-example",
    description="Environment created from a public Docker image.",
)
ml_client.environments.create_or_update(env_docker_image)

```

You can also use the Azure Machine Learning base images to create an environment (which are similar to the images used by curated environments):

```
from azure.ai.ml.entities import Environment

env_docker_image = Environment(
    image="mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04",
    name="aml-docker-image-example",
    description="Environment created from a Azure ML Docker image.",
)
ml_client.environments.create_or_update(env_docker_image)

```

### Create a custom environment with a conda specification file

Though Docker images contain all necessary packages when working with a specific framework, it may be that you need to include other packages to run your code.

For example, you may want to train a model with PyTorch, and track the model with MLflow.

When you need to include other packages or libraries in your environment, you can add a conda specification file to a Docker image when creating the environment.

A conda specification file is a YAML file, which lists the packages that need to be installed using `conda` or `pip`. Such a YAML file may look like:

```
name: basic-env-cpu
channels:
  - conda-forge
dependencies:
  - python=3.7
  - scikit-learn
  - pandas
  - numpy
  - matplotlib

```

Tip

Review the conda documentation on how to [create an environment manually](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually?azure-portal=true) for information on the standard format for conda files.

To create an environment from a base Docker image and a conda specification file, you can use the following code:

```
from azure.ai.ml.entities import Environment

env_docker_conda = Environment(
    image="mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04",
    conda_file="./conda-env.yml",
    name="docker-image-plus-conda-example",
    description="Environment created from a Docker image plus Conda environment.",
)
ml_client.environments.create_or_update(env_docker_conda)

```

Note

Since all curated environments are prefixed with **AzureML\-**, you can't create an environment with the same prefix.

### Use an environment

Most commonly, you use environments when you want to run a script as a (**command**) **job**.

To specify which environment you want to use to run your script, you reference an environment using the `<curated-environment-name>:<version>` or `<curated-environment-name>@latest` syntax.

For example, the following code shows how to configure a command job with the Python SDK, which uses a curated environment including Scikit\-Learn:

```
from azure.ai.ml import command

## configure job
job = command(
    code="./src",
    command="python train.py",
    environment="docker-image-plus-conda-example:1",
    compute="aml-cluster",
    display_name="train-custom-env",
    experiment_name="train-custom-env"
)

## submit job
returned_job = ml_client.create_or_update(job)

```

When you submit the job, the environment is built. The first time you use an environment, it can take 10\-15 minutes to build the environment. You can review the logs of the environment build in the logs of the job.

When Azure Machine Learning builds a new environment, it's added to the list of custom environments in the workspace. The image of the environment is hosted in the Azure Container registry associated to the workspace. Whenever you use the same environment for another job (and another script), the environment is ready to go and doesn't need to be build again.

---

## Exercise \- Work with environments

Now, it's your chance to explore how to work with environments in Azure Machine Learning.

In this exercise, you learn how to:

* Create a custom environment.
* Use environments when running Azure Machine Learning jobs.

### Instructions

Launch the exercise and follow the instructions.

---

## Summary

In this module, you've learned how to:

* Understand environments in Azure Machine Learning.
* Explore and use curated environments.
* Create and use custom environments.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/work-environments-azure-machine-learning/_

## Fuentes
- [Work with environments in Azure Machine Learning](https://learn.microsoft.com/en-us/training/modules/work-environments-azure-machine-learning/?WT.mc_id=api_CatalogApi)
