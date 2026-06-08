# Create and explore the Responsible AI dashboard for a model in Azure Machine Learning

> Curso: Manage and review models in Azure Machine Learning (wwl-manage-review-models-azure-machine-learning) · Seccion: Manage and review models in Azure Machine Learning
> Duracion estimada: 42 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

When you train a machine learning model, you may experiment with multiple models to find the one that best fits your data. To compare and evaluate models, you can review relevant performance metrics. Next to the performance metrics, you should also review whether your models conform to **responsible Artificial Intelligence (AI)** principles. Responsible AI is an approach to developing, assessing, and deploying models in a safe, trustworthy, and ethical way.

To help you with implementing responsible AI, Azure Machine Learning offers the **Responsible AI dashboard**. You can create and customize the Responsible AI dashboard to explore your data and model.

---

## Understand Responsible AI

As a data scientist, you may train a machine learning model to predict whether someone is able to pay back a loan, or whether a candidate is suitable for a job vacancy. As models are often used when making decisions, it's important that the models are unbiased and transparent.

Whatever you use a model for, you should consider the **Responsible Artificial Intelligence** (**Responsible AI**) principles. Depending on the use case, you may focus on specific principles. Nevertheless, it's a best practice to consider all principles to ensure you're addressing any issues the model may have.

Microsoft has listed six Responsible AI principles:

* **Fairness**: Ensure your model provides equitable outcomes by testing for and mitigating harmful bias across groups.
* **Reliability \& Safety**: Build, test, and monitor your model so it performs consistently, handles edge cases, and prevents unsafe behavior.
* **Privacy \& Security**: Protect user data through minimal collection, strong safeguards, and responsible data\-handling practices.
* **Inclusiveness**: Design and evaluate systems so people of diverse abilities, backgrounds, and contexts can use them effectively.
* **Transparency**: Communicate clearly how your model works, what data it uses, and how its outputs should be interpreted.
* **Accountability**: Assign human oversight and responsibility so decisions influenced by AI remain traceable and governed.

Tip

Learn about the [Responsible AI Standard](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2022/06/Microsoft-Responsible-AI-Standard-v2-General-Requirements-3.pdf) for building AI systems according to the six key principles.

---

## Create the Responsible AI dashboard

To help you implement the **Responsible Artificial Intelligence** (**Responsible AI**) principles in Azure Machine Learning, you can create the **Responsible AI dashboard**.

The Responsible AI dashboard allows you to pick and choose insights you need, to evaluate whether your model is safe, trustworthy, and ethical.

Azure Machine Learning has built\-in **components** that can generate Responsible AI insights for you. The insights are then gathered in an interactive dashboard for you to explore. You can also generate a scorecard as PDF to easily share the insights with your colleagues to evaluate your models.

### Create a Responsible AI dashboard

To create a Responsible AI (RAI) dashboard, you need to create a **pipeline** by using the built\-in components. The pipeline should:

1. Start with the `RAI Insights dashboard constructor`.
2. Include one of the **RAI tool components**.
3. End with `Gather RAI Insights dashboard` to collect all insights into one dashboard.
4. *Optionally* you can also add the `Gather RAI Insights score card` at the end of your pipeline.

### Explore the Responsible AI components

The available tool components and the insights you can use are:

* `Add Explanation to RAI Insights dashboard`: Interpret models by generating explanations. Explanations show how much features influence the prediction.
* `Add Causal to RAI Insights dashboard`: Use historical data to view the causal effects of features on outcomes.
* `Add Counterfactuals to RAI Insights dashboard`: Explore how a change in input would change the model's output.
* `Add Error Analysis to RAI Insights dashboard`: Explore the distribution of your data and identify erroneous subgroups of data.

### Build and run the pipeline to create the Responsible AI dashboard

To create the Responsible AI dashboard, you build a pipeline with the components you selected. When you run the pipeline, a Responsible dashboard (and scorecard) is generated and associated with your model.

After you've trained and registered a model in the Azure Machine Learning workspace, you can create the Responsible AI dashboard in three ways:

* Using the Command Line Interface (CLI) extension for Azure Machine Learning.
* Using the Python Software Development Kit (SDK).
* Using the Azure Machine Learning studio for a no\-code experience.

#### Using the Python SDK to build and run the pipeline

To generate a Responsible AI dashboard, you need to:

* Register the training and test datasets as MLtable data assets.
* Register the model.
* Retrieve the built\-in components you want to use.
* Build the pipeline.
* Run the pipeline.

If you want to build the pipeline using the Python SDK, you first have to retrieve the components you want to use.

You should start the pipeline with the `RAI Insights dashboard constructor` component:

```
rai_constructor_component = ml_client_registry.components.get(
    name="microsoft_azureml_rai_tabular_insight_constructor", label="latest"
)

```

Then, you can add any of the available insights, like the explanations, by retrieving the `Add Explanation to RAI Insights dashboard component`:

```
rai_explanation_component = ml_client_registry.components.get(
    name="microsoft_azureml_rai_tabular_explanation", label="latest"
)

```

Note

The parameters and expected inputs vary across components. [Explore the component for the specific insights](/en-us/azure/machine-learning/how-to-responsible-ai-insights-sdk-cli?view=azureml-api-2&tabs=python?azure-portal=true) you want to add to your dashboard to find which inputs you need to specify.

And finally, your pipeline should end with a `Gather RAI Insights dashboard` component:

```
rai_gather_component = ml_client_registry.components.get(
    name="microsoft_azureml_rai_tabular_insight_gather", label="latest"
)

```

Once you have the components, you can build the pipeline:

```
from azure.ai.ml import Input, dsl
from azure.ai.ml.constants import AssetTypes

@dsl.pipeline(
    compute="aml-cluster",
    experiment_name="Create RAI Dashboard",
)
def rai_decision_pipeline(
    target_column_name, train_data, test_data
):
    # Initiate the RAIInsights
    create_rai_job = rai_constructor_component(
        title="RAI dashboard diabetes",
        task_type="classification",
        model_info=expected_model_id,
        model_input=Input(type=AssetTypes.MLFLOW_MODEL, path=azureml_model_id),
        train_dataset=train_data,
        test_dataset=test_data,
        target_column_name="Predictions",
    )
    create_rai_job.set_limits(timeout=30)

    # Add explanations
    explanation_job = rai_explanation_component(
        rai_insights_dashboard=create_rai_job.outputs.rai_insights_dashboard,
        comment="add explanation", 
    )
    explanation_job.set_limits(timeout=10)

    # Combine everything
    rai_gather_job = rai_gather_component(
        constructor=create_rai_job.outputs.rai_insights_dashboard,
        insight=explanation_job.outputs.explanation,
    )
    rai_gather_job.set_limits(timeout=10)

    rai_gather_job.outputs.dashboard.mode = "upload"

    return {
        "dashboard": rai_gather_job.outputs.dashboard,
    }

```

### Exploring the Responsible AI dashboard

After building the pipeline, you need to run it to generate the Responsible AI dashboard. When the pipeline successfully completed, you can select to **view** the Responsible AI dashboard from the pipeline overview.

Alternatively, you can find the Responsible AI dashboard in the **Responsible AI** tab of the registered model.

---

## Evaluate the Responsible AI dashboard

When your Responsible AI dashboard is generated, you can explore its contents in the Azure Machine Learning studio to evaluate your model.

When you open the Responsible AI dashboard, the studio tries to automatically connect it to a compute instance. The compute instance provides the necessary compute for interactive exploration within the dashboard.

The output of each component you added to the pipeline is reflected in the dashboard. Depending on the components you selected, you can find the following insights in your Responsible AI dashboard:

* Error analysis
* Explanations
* Counterfactuals
* Causal analysis

Let's explore what we can review for each of these insights.

#### Explore error analysis

A model is expected to make false predictions, or errors. With the error analysis feature in the Responsible AI dashboard, you can review and understand how errors are distributed in your dataset. For example, are there specific subgroups, or cohorts, in your dataset for which the model makes more false predictions?

When you include error analysis, there are two types of visuals you can explore in the Responsible AI dashboard:

* **Error tree map**: Allows you to explore which combination of subgroups results in the model making more false predictions.

* **Error heat map**: Presents a grid overview of a model's errors over the scale of one or two features.

#### Explore explanations

Whenever you use a model for decision\-making, you want to understand how a model reaches a certain prediction. Whenever you've trained a model that is too complex to understand, you can run *model explainers* to calculate the **feature importance**. In other words, you want to understand how each of the input features influences the model's prediction.

There are [various statistical techniques](/en-us/azure/machine-learning/how-to-machine-learning-interpretability?view=azureml-api-2#supported-model-interpretability-techniques) you can use as model explainers. Most commonly, the **mimic** explainer trains a simple interpretable model on the same data and task. As a result, you can explore two types of feature importance:

* **Aggregate feature importance**: Shows how each feature in the test data influences the model's predictions *overall*.

* **Individual feature importance**: Shows how each feature impacts an *individual* prediction.

#### Explore counterfactuals

Explanations can give you insights into the relative importance of features on the model's predictions. Sometimes, you may want to take it a step further and understand whether the model's predictions would change if the input would be different. To explore how the model's output would change based on a change in the input, you can use **counterfactuals**.

You can choose to explore counterfactuals *what\-if* examples by selecting a data point and the desired model's prediction for that point. When you create a what\-if counterfactual, the dashboard opens a panel to help you understand which input would result in the desired prediction.

#### Explore causal analysis

Explanations and counterfactuals help you to understand the model's predictions and the effects of features on the predictions. Though model interpretability may already be a goal by itself, you may also need more information to help you improve decision\-making.

**Causal analysis** uses statistical techniques to estimate the average effect of a feature on a desired prediction. It analyzes how certain interventions or treatments may result in a better outcome, across a population or for a specific individual.

There are three available tabs in the Responsible AI dashboard when including causal analysis:

* **Aggregate causal effects**: Shows the average causal effects for predefined treatment features (the features you want to change to optimize the model's predictions).
* **Individual causal effects**: Shows individual data points and allows you to change the treatment features to explore their influence on the prediction.
* **Treatment policy**: Shows which parts of your data points benefit most from a treatment.

---

## Exercise \- Explore the Responsible AI dashboard

Now it's your chance to work with the Responsible AI dashboard in Azure Machine Learning for yourself.

In this exercise, learn how to:

* Create a pipeline with the Python SDK v2 to create a Responsible AI dashboard.
* Explore the results of the dashboard in the Azure Machine Learning studio.

### Instructions

Launch the exercise and follow the instructions.

---

## Summary

In this module, you've learned how to:

* Understand Azure Machine Learning's built\-in components for responsible AI.
* Create a Responsible AI dashboard.
* Explore a Responsible AI dashboard.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/manage-compare-models-azure-machine-learning/_

## Fuentes
- [Create and explore the Responsible AI dashboard for a model in Azure Machine Learning](https://learn.microsoft.com/en-us/training/modules/manage-compare-models-azure-machine-learning/?WT.mc_id=api_CatalogApi)
