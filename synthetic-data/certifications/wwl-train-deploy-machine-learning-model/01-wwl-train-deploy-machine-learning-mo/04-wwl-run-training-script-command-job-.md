# Run a training script as a command job in Azure Machine Learning

> Curso: Train and manage a machine learning model with Azure Machine Learning (wwl-train-deploy-machine-learning-model) · Seccion: Train and manage a machine learning model with Azure Machine Learning
> Duracion estimada: 37 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

A common challenge when developing machine learning models is to prepare for production scenarios. When you write code to process data and train models, you want the code to be scalable, repeatable, and ready for automation.

Though notebooks are ideal for experimentation and development, scripts are a better fit for production workloads. In Azure Machine Learning, you can run a script as a **command job**. When you submit a command job, you can configure various parameters like the input data and the compute environment. Azure Machine Learning also helps you track your work when working with command jobs to make it easier to compare workloads.

You'll learn how to run a script as a command job using the Python software development kit (SDK) v2 for Azure Machine Learning.

### Learning objectives

In this module, you'll learn how to:

* Convert a notebook to a script.
* Test scripts in a terminal.
* Run a script as a command job.
* Use parameters in a command job.

---

## Convert a notebook to a script

When you've used notebooks for experimentation and development, you'll first need to convert a notebook to a script. Alternatively, you might choose to skip using notebooks and work only with scripts. Either way, there are some recommendations when creating scripts to have production\-ready code.

Scripts are ideal for testing and automation in your production environment. To create a production\-ready script, you'll need to:

* Remove nonessential code.
* Refactor your code into functions.
* Test your script in the terminal.

### Remove all nonessential code

The main benefit of using notebooks is being able to quickly explore your data. For example, you can use `print()` and `df.describe()` statements to explore your data and variables. When you create a script that will be used for automation, you want to avoid including code written for exploratory purposes.

The first thing you therefore need to do to convert your code to production code is to remove the nonessential code. Especially when you'll run the code regularly, you want to avoid executing anything nonessential to reduce cost and compute time.

### Refactor your code into functions

When using code in business processes, you want the code to be easy to read so that anyone can maintain it. One common approach to make code easier to read and test is to use functions.

For example, you might have used the following example code in a notebook to read and split the data:

```
## read and visualize the data
print("Reading data...")
df = pd.read_csv('diabetes.csv')
df.head()

## split data
print("Splitting data...")
X, y = df[['Pregnancies','PlasmaGlucose','DiastolicBloodPressure','TricepsThickness','SerumInsulin','BMI','DiabetesPedigree','Age']].values, df['Diabetic'].values

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

```

As functions also allow you to test parts of your code, you might prefer to create *multiple smaller functions*, rather than one large function. If you want to test a part of your code, you can choose to only test a small part and avoid running more code than necessary.

You can refactor the code shown in the example into two functions:

* Read the data
* Split the data

An example of refactored code might be the following:

```
def main(csv_file):
    # read data
    df = get_data(csv_file)

    # split data
    X_train, X_test, y_train, y_test = split_data(df)

## function that reads the data
def get_data(path):
    df = pd.read_csv(path)
    
    return df

## function that splits the data
def split_data(df):
    X, y = df[['Pregnancies','PlasmaGlucose','DiastolicBloodPressure','TricepsThickness',
    'SerumInsulin','BMI','DiabetesPedigree','Age']].values, df['Diabetic'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

    return X_train, X_test, y_train, y_test

```

Note

You may have noticed that nonessential code was also omitted in the refactored code. You may choose to use `print` statements in production code if you'll review the script's output and you want to ensure all code ran as expected. However, when you know you're not going to review the output of a script in a terminal, it's best to remove any code that has no purpose.

### Test your script

Before using scripts in production environments, for example by integrating them with automation pipelines, you'll want to test whether the scripts work as expected.

One simple way to test your script, is to run the script in a terminal. Within the Azure Machine Learning workspace, you can quickly run a script in the terminal of the compute instance.

When you open a script in the **Notebooks** page of the Azure Machine Learning studio, you can choose to **save and run the script in the terminal**.

Alternatively, you can navigate directly to the terminal of the compute instance. Navigate to the **Compute** page and select the **Terminal** of the compute instance you want to use. You can use the following command to run a Python script named `train.py`:

```
python train.py

```

Outputs of `print` statements will show in the terminal. Any possible errors will also appear in the terminal.

---

## Run a script as a command job

When you have a script that train a machine learning model, you can run it as a command job in Azure Machine Learning.

### Configure and submit a command job

To run a script as a command job, you'll need to configure and submit the job.

To configure a command job with the Python SDK (v2\), you'll use the `command` function. To run a script, you'll need to specify values for the following parameters:

* `code`: The folder that includes the script to run.
* `command`: Specifies which file to run.
* `environment`: The necessary packages to be installed on the compute before running the command.
* `compute`: The compute to use to run the command.
* `display_name`: The name of the individual job.
* `experiment_name`: The name of the experiment the job belongs to.

Tip

Learn more about [the `command` function and all possible parameters](/en-us/python/api/azure-ai-ml/azure.ai.ml?azure-portal=true) in the reference documentation for the Python SDK (v2\).

You can configure a command job to run a file named `train.py`, on the compute cluster named `aml-cluster` with the following code:

```
from azure.ai.ml import command

## configure job
job = command(
    code="./src",
    command="python train.py",
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    compute="aml-cluster",
    display_name="train-model",
    experiment_name="train-classification-model"
    )

```

When your job is configured, you can submit it, which will initiate the job and run the script:

```
## submit job
returned_job = ml_client.create_or_update(job)

```

You can monitor and review the job in the Azure Machine Learning studio. All jobs with the same experiment name will be grouped under the same experiment. You can find an individual job using the specified display name.

All inputs and outputs of a command job are tracked. You can review which command you specified, which compute was used, and which environment was used to run the script on the specified compute.

---

## Use parameters in a command job

You can increase the flexibility of your scripts by using parameters. For example, you might have created a script that trains a machine learning model. You can use the same script to train a model on different datasets, or using various hyperparameter values.

### Working with script arguments

To use parameters in a script, you must use a library such as `argparse` to read arguments passed to the script and assign them to variables.

For example, the following script reads an arguments named `training_data`, which specifies the path to the training data.

```
## import libraries
import argparse
import pandas as pd
from sklearn.linear_model import LogisticRegression

def main(args):
    # read data
    df = get_data(args.training_data)

## function that reads the data
def get_data(path):
    df = pd.read_csv(path)
    
    return df

def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str)

    # parse args
    args = parser.parse_args()

    # return args
    return args

## run script
if __name__ == "__main__":

    # parse args
    args = parse_args()

    # run main function
    main(args)

```

Any parameters you expect should be defined in the script. In the script, you can specify what type of value you expect for each parameter and whether you want to set a default value.

### Passing arguments to a script

To pass parameter values to a script, you need to provide the argument value in the command.

For example, if you would pass a parameter value when running a script in a terminal, you would use the following command:

```
python train.py --training_data diabetes.csv

```

In the example, `diabetes.csv` is a local file. Alternatively, you could specify the path to a data asset created in the Azure Machine Learning workspace.

Similarly, when you want to pass a parameter value to a script you want to run as a command job, you'll specify the values in the command:

```
from azure.ai.ml import command

## configure job
job = command(
    code="./src",
    command="python train.py --training_data diabetes.csv",
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    compute="aml-cluster",
    display_name="train-model",
    experiment_name="train-classification-model"
    )

```

After submitting a command job, you can review the input and output parameters you specified.

---

## Exercise \- Run a training script as a command job

Now, it's your chance to run a script as a command job in Azure Machine Learning.

In this exercise, you will:

* Convert a notebook to a script.
* Test the script in the terminal.
* Run a script as a command job.
* Use parameters when running a script.

### Instructions

Follow these instructions to complete the exercise:

1. View the exercise repo at [https://microsoftlearning.github.io/mslearn\-azure\-ml/](https://microsoftlearning.github.io/mslearn-azure-ml?azure-portal=true).
2. Complete the **Run a training script as a command job in Azure Machine Learning** exercise.

---

## Summary

In this module, you've learned how to:

* Convert a notebook to a script.
* Test scripts in a terminal.
* Run a script as a command job.
* Use parameters in a command job.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/run-training-script-command-job-azure-machine-learning/_

## Fuentes
- [Run a training script as a command job in Azure Machine Learning](https://learn.microsoft.com/en-us/training/modules/run-training-script-command-job-azure-machine-learning/?WT.mc_id=api_CatalogApi)
