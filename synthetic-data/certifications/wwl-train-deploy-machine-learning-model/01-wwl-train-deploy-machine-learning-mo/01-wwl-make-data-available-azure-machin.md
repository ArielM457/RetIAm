# Make data available in Azure Machine Learning

> Curso: Train and manage a machine learning model with Azure Machine Learning (wwl-train-deploy-machine-learning-model) · Seccion: Train and manage a machine learning model with Azure Machine Learning
> Duracion estimada: 39 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Data is a fundamental element in any machine learning workload. You need data to train a model and you create data when using a model to generate predictions.

To work with data in Azure Machine Learning, you can access data by using **Uniform Resource Identifiers** (**URIs**). When you work with a data source or a specific file or folder repeatedly, you can create **datastores** and **data assets** within the Azure Machine Learning workspace. Datastores and data assets allow you to securely store the connection information to your data.

In this module, you learn how to create and use URIs, datastores, and data assets in Azure Machine Learning.

---

## Understand URIs

You can store data on your local device, or somewhere in the cloud. Wherever you store your data, you want to access the data when training machine learning models. To find and access data in Azure Machine Learning, you can use **Uniform Resource Identifiers** (**URIs**).

### Understand URIs

A URI references the location of your data. For Azure Machine Learning to connect to your data, you need to prefix the URI with the appropriate protocol. There are three common protocols when working with data in the context of Azure Machine Learning:

* `http(s)`: Use for data stores publicly or privately in an Azure Blob Storage or publicly available http(s) location.
* `abfs(s)`: Use for data stores in an Azure Data Lake Storage Gen 2\.
* `azureml`: Use for data stored in a datastore.

For example, you may create an Azure Blob Storage in Azure. To store data, you create a container named `training-data`. Within the container, you create a folder `datastore-path`. Within the folder, you store the CSV file `diabetes.csv`.

When you want to access the data from the Azure Machine Learning workspace, you can use the path to the folder or file directly. When you want to connect to the folder or file directly, you can use the `http(s)` protocol. If the container is set to private, you'll need to provide some kind of authentication to get access to the data, like a Shared Access Signature (SAS).

When you create a datastore in Azure Machine Learning, you'll store the connection and authentication information in the workspace. Then, to access the data in the container, you can use the `azureml` protocol.

Tip

A datastore is a reference to an existing storage account on Azure. Therefore, when you refer to data stored in a datastore, you may be referring to data being stored in an Azure Blob Storage or Azure Data Lake Storage. When you refer to the datastore however, you won't need to authenticate as the connection information stored with the datastore will be used by Azure Machine Learning.

It's considered a best practice to avoid any sensitive data in your code, like authentication information. Therefore, whenever possible, you should work with datastores and data assets in Azure Machine Learning. However, during experimentation in notebooks, you may want to connect directly to a storage location to avoid unnecessary overhead.

---

## Create a datastore

In Azure Machine Learning, **datastores** are abstractions for cloud data sources. They encapsulate the information needed to connect to data sources, and securely store this connection information so that you don’t have to code it in your scripts.

The benefits of using datastores are:

* Provides easy\-to\-use URIs to your data storage.
* Facilitates data discovery within Azure Machine Learning.
* Securely stores connection information, without exposing secrets and keys to data scientists.

When you create a datastore with an existing storage account on Azure, you have the choice between two different authentication methods:

* **Credential\-based**: Use a *service principal*, *shared access signature* (*SAS*) token or *account key* to authenticate access to your storage account.
* **Identity\-based**: Use your *Microsoft Entra identity* or *managed identity*.

### Understand types of datastores

Azure Machine Learning supports the creation of datastores for multiple kinds of Azure data source, including:

* Azure Blob Storage
* Azure File Share
* Azure Data Lake (Gen 2\)

### Use the built\-in datastores

Every workspace has four built\-in datastores (two connecting to Azure Storage blob containers, and two connecting to Azure Storage file shares), which are used as system storages by Azure Machine Learning.

In most machine learning projects, you need to work with data sources of your own. For example, you can integrate your machine learning solution with data from existing applications or data engineering pipelines.

### Create a datastore

Datastores are attached to workspaces and are used to store connection information to storage services. When you create a datastore, you provide a name that can be used to retrieve the connection information.

Datastores allow you to easily connect to storage services without having to provide all necessary details every time you want to read or write data. It also creates a protective layer if you want users to use the data, but not connect to the underlying storage service directly.

#### Create a datastore for an Azure Blob Storage container

You can create a datastore through the graphical user interface, the Azure command\-line interface (CLI), or the Python software development kit (SDK).

Depending on the storage service you want to connect to, there are different options for Azure Machine Learning to authenticate.

For example, when you want to create a datastore to connect to an Azure Blob Storage container, you can use an account key:

```
blob_datastore = AzureBlobDatastore(
    			name = "blob_example",
    			description = "Datastore pointing to a blob container",
    			account_name = "mytestblobstore",
    			container_name = "data-container",
    			credentials = AccountKeyConfiguration(
        			account_key="XXXxxxXXXxXXXXxxXXX"
    			),
)
ml_client.create_or_update(blob_datastore)

```

Alternatively, you can create a datastore to connect to an Azure Blob Storage container by using a SAS token to authenticate:

```
blob_datastore = AzureBlobDatastore(
name="blob_sas_example",
description="Datastore pointing to a blob container",
account_name="mytestblobstore",
container_name="data-container",
credentials=SasTokenConfiguration(
sas_token="?xx=XXXX-XX-XX&xx=xxxx&xxx=xxx&xx=xxxxxxxxxxx&xx=XXXX-XX-XXXXX:XX:XXX&xx=XXXX-XX-XXXXX:XX:XXX&xxx=xxxxx&xxx=XXxXXXxxxxxXXXXXXXxXxxxXXXXXxxXXXXXxXXXXxXXXxXXxXX"
),
)
ml_client.create_or_update(blob_datastore)

```

Tip

Learn more about [how to create datastores to connect to other types of cloud storage solutions](/en-us/azure/machine-learning/how-to-datastore?azure-portal=true).

---

## Create a data asset

As a data scientist, you want to focus on training machine learning models. Though you need access to data as input for a machine learning model, you don't want to worry about *how* to get access. To simplify getting access to the data you want to work with, you can use **data assets**.

### Understand data assets

In Azure Machine Learning, data assets are references to where the data is stored, how to get access, and any other relevant metadata. You can create data assets to get access to data in datastores, Azure storage services, public URLs, or data stored on your local device.

The benefits of using data assets are:

* You can **share and reuse data** with other members of the team such that they don't need to remember file locations.
* You can **seamlessly access data** during model training (on any supported compute type) without worrying about connection strings or data paths.
* You can **version** the metadata of the data asset.

There are three main types of data assets you can use:

* **URI file**: Points to a specific file.
* **URI folder**: Points to a folder.
* **MLTable**: Points to a folder or file, and includes a schema to read as tabular data.

Note

**URI** stands for **Uniform Resource Identifier** and stands for a storage location on your local computer, Azure Blob or Data Lake Storage, publicly available https location, or even an attached datastore.

### When to use data assets

Data assets are most useful when executing machine learning tasks as Azure Machine Learning jobs. As a job, you can run a Python script that takes inputs and generates outputs. A data asset can be parsed as both an input or output of an Azure Machine Learning job.

Let’s take a look at each of the types of data assets, how to create them, and how to use the data asset in a job.

### Create a URI file data asset

A URI file data asset points to a specific file. Azure Machine Learning only stores the path to the file, which means you can point to any type of file. When you use the data asset, you specify how you want to read the data, which depends on the type of data you're connecting to.

The supported paths you can use when creating a URI file data asset are:

* Local: `./<path>`
* Azure Blob Storage: `wasbs://<account_name>.blob.core.windows.net/<container_name>/<folder>/<file>`
* Azure Data Lake Storage (Gen 2\): `abfss://<file_system>@<account_name>.dfs.core.windows.net/<folder>/<file>`
* Datastore: `azureml://datastores/<datastore_name>/paths/<folder>/<file>`

Important

When you create a data asset and point to a file or folder stored on your local device, a copy of the file or folder will be uploaded to the default datastore `workspaceblobstore`. You can find the file or folder in the `LocalUpload` folder. By uploading a copy, you'll still be able to access the data from the Azure Machine Learning workspace, even when the local device on which the data is stored is unavailable.

To create a URI file data asset, you can use the following code:

```
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

my_path = '<supported-path>'

my_data = Data(
    path=my_path,
    type=AssetTypes.URI_FILE,
    description="<description>",
    name="<name>",
    version="<version>"
)

ml_client.data.create_or_update(my_data)

```

When you parse the URI file data asset as input in an Azure Machine Learning job, you first need to read the data before you can work with it.

Imagine you create a Python script you want to run as a job, and you set the value of the input parameter `input_data` to be the URI file data asset (which points to a CSV file). You can read the data by including the following code in your Python script:

```
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input_data", type=str)
args = parser.parse_args()

df = pd.read_csv(args.input_data)
print(df.head(10))

```

If your URI file data asset points to a different type of file, you need to use the appropriate Python code to read the data. For example, if instead of CSV files, you're working with JSON files, you'd use `pd.read_json()` instead.

### Create a URI folder data asset

A URI folder data asset points to a specific folder. It works similar to a URI file data asset and supports the same paths.

To create a URI folder data asset with the Python SDK, you can use the following code:

```
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

my_path = '<supported-path>'

my_data = Data(
    path=my_path,
    type=AssetTypes.URI_FOLDER,
    description="<description>",
    name="<name>",
    version='<version>'
)

ml_client.data.create_or_update(my_data)

```

When you parse the URI folder data asset as input in an Azure Machine Learning job, you first need to read the data before you can work with it.

Imagine you create a Python script you want to run as a job, and you set the value of the input parameter `input_data` to be the URI folder data asset (which points to multiple CSV files). You can read all CSV files in the folder and concatenate them, which you can do by including the following code in your Python script:

```
import argparse
import glob
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input_data", type=str)
args = parser.parse_args()

data_path = args.input_data
all_files = glob.glob(data_path + "/*.csv")
df = pd.concat((pd.read_csv(f) for f in all_files), sort=False)

```

Depending on the type of data you're working with, the code you use to read the files can change.

### Create a MLTable data asset

A MLTable data asset allows you to point to tabular data. When you create a MLTable data asset, you specify the schema definition to read the data. As the schema is already defined and stored with the data asset, you don't have to specify how to read the data when you use it.

Therefore, you want to use a MLTable data asset when the schema of your data is complex or changes frequently. Instead of changing how to read the data in every script that uses the data, you only have to change it in the data asset itself.

When you define the schema when creating a MLTable data asset, you can also choose to only specify a subset of the data.

For certain features in Azure Machine Learning, like Automated Machine Learning, you need to use a MLTable data asset, as Azure Machine Learning needs to know how to read the data.

To define the schema, you can include a **MLTable file** in the same folder as the data you want to read. The MLTable file includes the path pointing to the data you want to read, and how to read the data:

```
type: mltable

paths:
  - pattern: ./*.txt
transformations:
  - read_delimited:
      delimiter: ','
      encoding: ascii
      header: all_files_same_headers

```

Tip

Learn more on [how to create the MLTable file and which transformations you can include](/en-us/azure/machine-learning/reference-yaml-mltable?azure-portal=true).

To create a MLTable data asset with the Python SDK, you can use the following code:

```
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

my_path = '<path-including-mltable-file>'

my_data = Data(
    path=my_path,
    type=AssetTypes.MLTABLE,
    description="<description>",
    name="<name>",
    version='<version>'
)

ml_client.data.create_or_update(my_data)

```

When you parse a MLTable data asset as input to a Python script you want to run as an Azure Machine Learning job, you can include the following code to read the data:

```
import argparse
import mltable
import pandas

parser = argparse.ArgumentParser()
parser.add_argument("--input_data", type=str)
args = parser.parse_args()

tbl = mltable.load(args.input_data)
df = tbl.to_pandas_dataframe()

print(df.head(10))

```

A common approach is to convert the tabular data to a Pandas data frame. However, you can also convert the data to a Spark data frame if that suits your workload better.

---

## Exercise \- Make data available in Azure Machine Learning

Now, it's your chance to explore how to work with data.

In this exercise, you learn how to:

* Explore the default datastores.
* Create a datastore.
* Create data assets.

### Instructions

Launch the exercise and follow the instructions.

---

## Summary

In this module, you've learned how to:

* Access data by using URIs.
* Connect to cloud data sources with datastores.
* Use data asset to access specific files or folders.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/make-data-available-azure-machine-learning/_

## Fuentes
- [Make data available in Azure Machine Learning](https://learn.microsoft.com/en-us/training/modules/make-data-available-azure-machine-learning/?WT.mc_id=api_CatalogApi)
