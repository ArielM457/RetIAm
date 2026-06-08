# Get started with machine learning in Azure

> Curso: Design a machine learning solution (wwl-design-machine-learning-solution) · Seccion: Design a machine learning solution
> Duracion estimada: 66 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Thoughtfully designed machine learning solutions form the foundation of today's AI applications. From predictive analytics to personalized recommendations and beyond, machine learning solutions support the latest technological advances in society by using existing data to produce new insights.

Data scientists make decisions to tackle machine learning problems in different ways. The decisions they make affect the cost, speed, quality, and longevity of the solution.

In this module, you learn how to design an end\-to\-end machine learning solution with Microsoft Azure that can be used in an enterprise setting. Using the following six steps as a framework, we explore how to plan, train, deploy, and monitor machine learning solutions.

1. **Define the problem**: Decide on what the model should predict and when it's successful.
2. **Get the data**: Find data sources and get access.
3. **Prepare the data**: Explore the data. Clean and transform the data based on the model's requirements.
4. **Train the model**: Choose an algorithm and hyperparameter values based on trial and error.
5. **Integrate the model**: Deploy the model to an endpoint to generate predictions.
6. **Monitor the model**: Track the model's performance.

Note

The diagram is a simplified representation of the machine learning process. Typically, the process is iterative and continuous. For example, when monitoring the model you may decide to go back and retrain the model.

Next, let's look at how we can get started on a machine learning solution by defining the problem.

---

## Define the problem

Starting with the first step, you want to **define the problem** the model should solve, by understanding:

* What the model’s output should be.
* What type of machine learning task you use.
* What criteria make a model successful.

Depending on the data you have and the expected output of the model, you can identify the machine learning task. The task determines which types of algorithms you can use to **train the model**.

Some common machine learning tasks are:

1. **Classification**: Predict a categorical value.
2. **Regression**: Predict a numerical value.
3. **Time\-series forecasting**: Predict future numerical values based on time\-series data.
4. **Computer vision**: Classify images or detect objects in images.
5. **Natural language processing** (**NLP**): Extract insights from text.

To train a model, you have a set of algorithms that you can use, depending on the task you want to perform. To evaluate the model, you can calculate performance metrics such as accuracy or precision. The metrics available also depend on the task your model needs to perform and help you to decide whether a model is successful in its task.

### Explore an example

Consider a scenario where you want to determine if patients have diabetes. The problem you're trying to solve and the type of data available determines the machine learning task you choose. In this case, the available data are other health data points from patients. We can represent the output we want as *categorical* information that either the patient has diabetes or doesn't have diabetes. Thus, the machine learning task is *classification*.

Understanding the entire process before you start gives you an opportunity to map out the decisions you need to make to design a successful machine learning solution. Following, is a diagram showing one way to approach the problem of identifying diabetes in a patient. In the diagram, the data is prepped, split, and trained using specific algorithms. Afterward, the model is evaluated for quality.

1. **Load data**: Import and inspect the dataset.
2. **Preprocess data**: Normalize and clean for consistency.
3. **Split data**: Separate into training and test sets.
4. **Choose model**: Select and configure an algorithm.
5. **Train model**: Learn patterns from the training data.
6. **Score model**: Generate predictions on test data.
7. **Evaluate**: Calculate performance metrics.

Training a machine learning model is often an iterative process, where you go through each of these steps multiple times to find the best performing model. Next, let's examine the data preparation process for developing a machine learning solution.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/design-machine-learning-model-training-solution/_

## Fuentes
- [Get started with machine learning in Azure](https://learn.microsoft.com/en-us/training/modules/design-machine-learning-model-training-solution/?WT.mc_id=api_CatalogApi)
