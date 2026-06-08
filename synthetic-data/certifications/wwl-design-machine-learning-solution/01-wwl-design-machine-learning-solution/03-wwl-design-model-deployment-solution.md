# Design a model deployment solution

> Curso: Design a machine learning solution (wwl-design-machine-learning-solution) · Seccion: Design a machine learning solution
> Duracion estimada: 27 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

As a data scientist, you want to train a machine learning model that helps others. Whether you're training a model to help your colleagues be more productive or to improve the user experience for your customers.

To ensure that your model is used by your target audience, you need to deploy your model to an endpoint. The endpoint can be integrated into a service or application to serve the users of the model. You should design a solution for deploying the model that best meets the needs of the users and takes into account the requirements of the model being deployed.

You'll learn how to design a model deployment solution and how the requirements of the deployed model can affect the way you train a model.

### Learning objectives

In this module, you'll learn how to:

* Understand how a model will be consumed.
* Decide whether to deploy your model to a real\-time or batch endpoint.

---

## Understand how model will be consumed

Imagine you're a data scientist and you train machine learning models. You typically follow six steps to plan, train, deploy, and monitor the model:

1. **Define the problem**: Decide on what the model should predict and when it's successful.
2. **Get the data**: Find data sources and get access.
3. **Prepare the data**: Explore the data. Clean and transform the data based on the model's requirements.
4. **Train the model**: Choose an algorithm and hyperparameter values based on trial and error.
5. **Integrate the model**: Deploy the model to an endpoint to generate predictions.
6. **Monitor the model**: Track the model's performance.

Note

The diagram is a simplified representation of the machine learning process. Typically, the process is iterative and continuous. For example, when monitoring the model you may decide to go back and retrain the model.

You should plan how you **integrate the model**, as it may affect how you train the model or what training data you use. To integrate the model, you need to deploy a model to an **endpoint**. You can deploy a model to an endpoint for either **real\-time or batch predictions**.

### Deploy a model to an endpoint

When you train a model, the goal is often to integrate the model into an application.

To easily integrate a model into an application, you can use **endpoints**. Simply put, an endpoint can be a web address that an application can call to get a message back.

With Azure Machine Learning, you can deploy your model to an endpoint. Then you can integrate the endpoint into your own application and call the model to get the predictions in the application where you want to visualize them.

When you deploy a model to an endpoint, you have two options:

* Get **real\-time** predictions
* Get **batch** predictions

#### Get real\-time predictions

If you want the model to score any new data as it comes in, you need predictions in real\-time.

Real\-time predictions are often needed when a model is used by an application such as a mobile app or a website.

Imagine you have a website that contains your product catalog:

1. A customer selects a product on your website, such as a shirt.
2. Based on the customer's selection, the model recommends other items from the product catalog immediately. The website displays the model's recommendations.

A customer can select a product in the web shop at any time. You want the model to find the recommendations almost immediately. The time it takes for the web page to load and display the shirt details is the time it should take to get the recommendations or predictions. Then, when the shirt is displayed, the recommendations can also be displayed.

#### Get batch predictions

If you want the model to score new data in batches, and save the results as a file or in a database, you need batch predictions.

For example, you can train a model that predicts orange juice sales for each future week. By predicting orange juice sales, you can ensure that supply is sufficient to meet expected demand.

Imagine you're visualizing all historical sales data in a report. You'll want to include the predicted sales in the same report.

Although orange juice is sold throughout the day, you only want to calculate the forecast once a week. You can collect the sales data throughout the week and call the model only when you have the sales data of a whole week. A collection of data points is referred to as a batch.

---

## Decide on real\-time or batch deployment

When you deploy a model to an endpoint to integrate with an application, you can choose to design it for real\-time or batch predictions.

The type of predictions you need depends on how you want to use the model's predictions

To decide whether to design a real\-time or batch deployment solution, you need to consider the following questions:

* How often should predictions be generated?
* How soon are the results needed?
* Should predictions be generated individually or in batches?
* How much compute power is needed to execute the model?

### Identify the necessary frequency of scoring

A common scenario is that you're using a model to score new data. Before you can get predictions in real\-time or in batch, you must first collect the new data.

There are various ways to generate or collect data. New data can also be collected at different time intervals.

For example, you can collect temperature data from an Internet of Things (IoT) device every minute. You can get transactional data every time a customer buys a product from your web shop. Or you can extract financial data from a database every three months.

Generally, there are two types of use cases:

1. You need the model to score the new data as soon as it comes in.
2. You can schedule or trigger the model to score the new data that you've collected over time.

Whether you want real\-time or batch predictions *doesn't necessarily depend on how often new data is collected*. Instead, it depends on how often and how quickly you need the predictions to be generated.

If you need the model's predictions immediately when new data is collected, you need real\-time predictions. If the model's predictions are only consumed at certain times, you need batch predictions.

### Decide on the number of predictions

Another important question to ask yourself is whether you need the predictions to be generated individually or in batches.

A simple way to illustrate the difference between individual and batch predictions is to imagine a table. Suppose you have a table of customer data where each row represents a customer. For each customer, you have some demographic data and behavioral data, such as how many products they've purchased from your web shop and when their last purchase was.

Based on this data, you can predict customer churn: whether a customer will buy from your web shop again or not.

Once you've trained the model, you can decide if you want to generate predictions:

* **Individually**: The model receives a *single row of data* and returns whether or not that individual customer will buy again.
* **Batch**: The model receives *multiple rows of data* in one table and returns whether or not each customer will buy again. The results are collated in a table that contains all predictions.

You can also generate individual or batch predictions when working with files. For example, when working with a computer vision model you may need to score a single image individually, or a collection of images in one batch.

### Consider the cost of compute

In addition to using compute when training a model, you also need compute when deploying a model. Depending on whether you deploy the model to a real\-time or batch endpoint, you'll use different types of compute. To decide whether to deploy your model to a real\-time or batch endpoint, you must consider the cost of each type of compute.

If you need **real\-time predictions**, you need compute that is always available and able to return the results (almost) immediately. **Container** technologies like *Azure Container Instance* (ACI) and *Azure Kubernetes Service* (AKS) are ideal for such scenarios as they provide a lightweight infrastructure for your deployed model.

However, when you deploy a model to a real\-time endpoint and use such container technology, the compute is *always on*. Once a model is deployed, you're continuously paying for the compute as you can't pause, or stop the compute as the model must always be available for immediate predictions.

Alternatively, if you need **batch predictions**, you need compute that can handle a large workload. Ideally, you'd use a **compute cluster** that can score the data in *parallel* batches by using multiple nodes.

When working with compute clusters that can process data in parallel batches, the compute is provisioned by the workspace when the batch scoring is triggered, and scaled down to 0 nodes when there's no new data to process. By letting the workspace scale down an idle compute cluster, you can save significant costs.

### Decide on real\-time or batch deployment

Choosing a deployment strategy for your machine learning models may be challenging, as different factors may influence your decision.

In general, if you need individual predictions immediately when new data is collected, you need real\-time predictions.

If you need the model to score new data when a batch of data is available, you should get batch predictions.

There are scenarios where you expect to need real\-time predictions when batch predictions can be more cost\-effective. Remember that you're continuously paying for compute with real\-time deployments, even when no new predictions are generated.

If you can allow for a 5\-10 minutes delay when needing immediate predictions, you can opt to deploy your model to a batch endpoint. The delay is caused in the time it needs to start the compute cluster after the endpoint is triggered. However, the compute cluster will also stop after the prediction is generated, minimizing costs and potentially being a more cost\-effective solution.

Finally, you also have to consider the required compute for your model to score new data. Simpler models require less cost and time to generate predictions. More complex models may require more compute power and processing time to generate predictions. Therefore, you should consider how you'll deploy your model before deciding on how to train your model.

---

## Module assessment

Note

To complete this exercise, read the case study below. At the end, you'll be asked to give advice by answering the knowledge check questions.

Welcome to Proseware! You've been hired as the *lead data scientist* to help us design a machine learning deployment solution.

### Understand the problem

At Proseware, we're developing a **mobile application** that will help doctors diagnose diseases in patients faster. A doctor can enter the patient's medical data into the app to get a diagnosis on the patient.

Our first planned feature is that the app will tell the doctor *whether the patient should be further screened or treated for diabetes*.

We have already collected data that correlates with diabetes, such as the number of pregnancies, age, and body mass index (BMI). We also have a team of data scientists working on training a model that can classify whether a patient is likely to have diabetes.

We need your help deciding how to deploy the model to integrate it with our mobile application.

We're looking forward to your advice on **how to design the model's deployment solution**!

### Consider the requirements

| Requirement | Description |
| --- | --- |
|  | **Consider the frequency**. The plan is that a doctor enters a patient's information into the app, like their age and BMI. After entering, a doctor can select the `Analyze` button, after which the model should predict whether or not a patient is likely to have diabetes. |
|  | **Consider the compute**. A doctor consultation typically takes less than 10 minutes. If we want doctors to use this app, we need the answers to be returned as quickly as possible. The deployed model should always be available as we don't know when a doctor may use it. |
|  | **Consider the size**. A doctor will only use the app to get a prediction on an individual's situation. There's no need for generating the predictions of multiple patients at once. |

### Propose a solution

### Knowledge check

---

## Summary

In this module, you've learned how to:

* Identify how a model will be consumed.
* Decide whether to deploy your model to a real\-time or batch endpoint.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/design-model-deployment-solution/_

## Fuentes
- [Design a model deployment solution](https://learn.microsoft.com/en-us/training/modules/design-model-deployment-solution/?WT.mc_id=api_CatalogApi)
