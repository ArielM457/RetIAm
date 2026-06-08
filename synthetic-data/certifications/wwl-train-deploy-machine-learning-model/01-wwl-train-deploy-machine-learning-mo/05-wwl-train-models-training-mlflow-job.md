# Track model training with MLflow in jobs

> Curso: Train and manage a machine learning model with Azure Machine Learning (wwl-train-deploy-machine-learning-model) · Seccion: Train and manage a machine learning model with Azure Machine Learning
> Duracion estimada: 34 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Scripts are ideal when you want to run machine learning workloads in production environments. Imagine you're a data scientist who has developed a machine learning model to predict diabetes. The model is performing as expected and you created a training script. The script is used to retrain the model every month when new data has been collected.

You'll want to monitor the model's performance over time. You want to understand whether the new data every month benefits the model. Next to tracking models that are trained in notebooks, you can also use **MLflow** to track models in scripts.

**MLflow** is an open\-source platform that helps you to track model metrics and artifacts across platforms and is integrated with Azure Machine Learning.

When you use MLflow together with Azure Machine Learning, you can run training scripts locally or in the cloud. You can review model metrics and artifacts in the Azure Machine Learning workspace to compare runs and decide on next steps.

### Learning objectives

In this module, you learn how to:

* Use MLflow when you run a script as a job.
* Review metrics, parameters, artifacts, and models from a run.

---

## Track metrics with MLflow

When you train a model with a script, you can include MLflow in the scripts to track any parameters, metrics, and artifacts. When you run the script as a job in Azure Machine Learning, you're able to review all input parameters and outputs for each run.

### Understand MLflow

MLflow is an open\-source platform, designed to manage the complete machine learning lifecycle. As it's open source, it can be used when training models on different platforms. Here, we explore how we can integrate MLflow with Azure Machine Learning jobs.

There are two options to track machine learning jobs with MLflow:

* Enable autologging using `mlflow.autolog()`
* Use logging functions to track custom metrics using `mlflow.log_*`

Before you can use either of these options, you need to set up the environment to use MLflow.

### Include MLflow in the environment

To use MLflow during training job, the `mlflow` and `azureml-mlflow` pip packages need to be installed on the compute executing the script. Therefore, you need to include these two packages in the environment. You can create an environment by referring to a YAML file that describes the Conda environment. As part of the Conda environment, you can include these two packages.

For example, in this custom environment `mlflow` and `azureml-mlflow` are installed using pip:

```
name: mlflow-env
channels:
  - conda-forge
dependencies:
  - python=3.8
  - pip
  - pip:
    - numpy
    - pandas
    - scikit-learn
    - matplotlib
    - mlflow
    - azureml-mlflow

```

Once the environment is defined and registered, make sure to refer to it when submitting a job.

### Enable autologging

When working with one of the common libraries for machine learning, you can enable autologging in MLflow. Autologging logs parameters, metrics, and model artifacts without anyone needing to specify what needs to be logged.

Autologging is supported for the following libraries:

* Scikit\-learn
* TensorFlow and Keras
* XGBoost
* LightGBM
* Spark
* Fastai
* Pytorch

To enable autologging, add the following code to your training script:

```
import mlflow

mlflow.autolog()

```

### Log metrics with MLflow

In your training script, you can decide whatever custom metric you want to log with MLflow.

Depending on the type of value you want to log, use the MLflow command to store the metric with the experiment run:

* `mlflow.log_param()`: Log single key\-value parameter. Use this function for an input parameter you want to log.
* `mlflow.log_metric()`: Log single key\-value metric. Value must be a number. Use this function for any output you want to store with the run.
* `mlflow.log_artifact()`: Log a file. Use this function for any plot you want to log, save as image file first.

To add MLflow to an existing training script, you can add the following code:

```
import mlflow

reg_rate = 0.1
mlflow.log_param("Regularization rate", reg_rate)

```

Tip

For a complete overview of how to use MLflow Tracking, read the [MLflow documentation](https://www.mlflow.org/docs/latest/tracking.html).

### Submit the job

Finally, you need to submit the training script as a job in Azure Machine Learning. When you use MLflow in a training script and run it as a job, all tracked parameters, metrics, and artifacts are stored with the job run.

You configure the job as usual. You only need to make sure that the environment you refer to in the job includes the necessary packages, and the script describes which metrics you want to log.

---

## View metrics and evaluate models

After you've trained and tracked models with MLflow in Azure Machine Learning, you can explore the metrics and evaluate your models.

* Review metrics in the Azure Machine Learning studio.
* Retrieve runs and metrics with MLflow.

Note

Azure Machine Learning uses the concept of jobs when you run a script. Multiple job runs in Azure Machine Learning can be grouped within one experiment. MLflow uses a similar syntax where each script is a run, which is part of an experiment.

### View the metrics in the Azure Machine Learning studio

When your job is completed, you can review the logged parameters, metrics, and artifacts in the Azure Machine Learning studio.

When you review job runs in the Azure Machine Learning studio, you'll explore a job run's metrics, which is part of an experiment.

To view the metrics through an intuitive user interface, you can:

1. Open the Studio by navigating to <https://ml.azure.com>.
2. Find your experiment run and open it to view its details.
3. In the **Details** tab, all logged parameters are shown under **Params**.
4. Select the **Metrics** tab and select the metric you want to explore.
5. Any plots that are logged as artifacts can be found under **Images**.
6. The model assets that can be used to register and deploy the model are stored in the **models** folder under **Outputs \+ logs**.

Tip

Read the documentation to learn more on [how to track models with MLflow](/en-us/azure/machine-learning/how-to-use-mlflow).

### Retrieve metrics with MLflow in a notebook

When you run a training script as a job in Azure Machine Learning, and track your model training with MLflow, you can query the runs in a notebook by using MLflow. Using MLflow in a notebook gives you more control over which runs you want to retrieve to compare.

When using MLflow to query your runs, you'll refer to experiments and runs.

#### Search all the experiments

You can get all the active experiments in the workspace using MLFlow:

```
experiments = mlflow.search_experiments(max_results=2)
for exp in experiments:
    print(exp.name)

```

If you want to retrieve archived experiments too, then include the option `ViewType.ALL`:

```
from mlflow.entities import ViewType

experiments = mlflow.search_experiments(view_type=ViewType.ALL)
for exp in experiments:
    print(exp.name)

```

To retrieve a specific experiment, you can run:

```
exp = mlflow.get_experiment_by_name(experiment_name)
print(exp)

```

Tip

Explore the documentation on how to [search experiments with MLflow](https://mlflow.org/docs/latest/search-experiments.html?azure-portal=true)

#### Retrieve runs

MLflow allows you to search for runs inside of any experiment. You need either the experiment ID or the experiment name.

For example, when you want to retrieve the metrics of a specific run:

```
mlflow.search_runs(exp.experiment_id)

```

You can search runs across multiple experiments if necessary. Searching across experiments may be useful in case you want to compare runs of the same model when it's being logged in different experiments (by different people or different project iterations).

You can use `search_all_experiments=True` if you want to search across all the experiments in the workspace.

By default, experiments are ordered descending by `start_time`, which is the time the experiment was queued in Azure Machine Learning. However, you can change this default by using the parameter `order_by`.

For example, if you want to sort by start time and only show the last two results:

```
mlflow.search_runs(exp.experiment_id, order_by=["start_time DESC"], max_results=2)

```

You can also look for a run with a specific combination in the hyperparameters:

```
mlflow.search_runs(
    exp.experiment_id, filter_string="params.num_boost_round='100'", max_results=2
)

```

Tip

Explore the documentation on how to [search runs with MLflow](https://mlflow.org/docs/latest/search-runs.html?azure-portal=true)

---

## Exercise \- Use MLflow to track training jobs

Now, it's your chance to explore how to track models with MLflow in scripts.

In this exercise, you learn how to:

* Train and track a model with custom logging.
* Train and track a model with autologging.

### Instructions

Launch the exercise and follow the instructions.

---

## Summary

In this module, you've learned how to:

* Use MLflow when you run a script as a job.
* Review metrics, parameters, artifacts, and models from a run.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/train-models-training-mlflow-jobs/_

## Fuentes
- [Track model training with MLflow in jobs](https://learn.microsoft.com/en-us/training/modules/train-models-training-mlflow-jobs/?WT.mc_id=api_CatalogApi)
