# Configure web app settings

> Curso: Implement Azure App Service web apps (wwl-create-azure-app-service-web-apps) · Seccion: Implement Azure App Service web apps
> Duracion estimada: 30 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

In App Service, app settings are variables passed as environment variables to the application code.

### Learning objectives

After completing this module, you'll be able to:

* Create application settings that are bound to deployment slots.
* Explain the options for installing SSL/TLS certificates for your app.
* Enable diagnostic logging for your app to aid in monitoring and debugging.
* Create virtual app to directory mappings.

---

## Configure application settings

In App Service, app settings are variables passed as environment variables to the application code. For Linux apps and custom containers, App Service passes app settings to the container using the `--env` flag to set the environment variable in the container. In either case, they're injected into your app environment at app startup. When you add, remove, or edit app settings, App Service triggers an app restart.

For ASP.NET and ASP.NET Core developers, setting app settings in App Service is like setting them in `<appSettings>` in *Web.config* or *appsettings.json*, but the values in App Service override the ones in *Web.config* or *appsettings.json*. You can keep development settings (for example, local MySQL password) in *Web.config* or *appsettings.json* and production secrets (for example, Azure MySQL database password) safely in App Service. The same code uses your development settings when you debug locally, and it uses your production secrets when deployed to Azure.

App settings are always encrypted when stored (encrypted\-at\-rest). App settings names can only contain letters, numbers (0\-9\), periods ("."), and underscores ("\_")
Special characters in the value of an App Setting must be escaped as needed by the target OS.

Application settings can be accessed by navigating to your app's management page and selecting **Environment variables \> Application settings**.

### Adding and editing settings

To add a new app setting, select **\+ Add**. If you're using deployment slots, you can specify if your setting is swappable or not. In the dialog, you can stick the setting to the current slot.

When finished, select **Apply**. Don't forget to select **Apply** back in the **Environment variables** page.

Note

In a default Linux app service or a custom Linux container, any nested JSON key structure in the app setting name like `ApplicationInsights:InstrumentationKey` needs to be configured in App Service as `ApplicationInsights__InstrumentationKey` for the key name. In other words, replace any `:` with `__` (double underscore). Any periods in the app setting name are replaced with a `_` (single underscore).

#### Editing application settings in bulk

To add or edit app settings in bulk, select the **Advanced edit** button. When finished, select **OK**. Don't forget to select Apply back in the Environment variables page. App settings have the following JSON formatting:

```
[
  {
    "name": "<key-1>",
    "value": "<value-1>",
    "slotSetting": false
  },
  {
    "name": "<key-2>",
    "value": "<value-2>",
    "slotSetting": false
  },
  ...
]

```

### Configure connection strings

For ASP.NET and ASP.NET Core developers, setting connection strings in App Service are like setting them in `<connectionStrings>` in *Web.config*, but the values you set in App Service override the ones in *Web.config*. For other language stacks, it's better to use app settings instead, because connection strings require special formatting in the variable keys in order to access the values.

Tip

There's one case where you may want to use connection strings instead of app settings for non\-.NET languages: certain Azure database types are backed up along with the app *only* if you configure a connection string for the database in your App Service app.

Adding and editing connection strings follow the same principles as other app settings and they can also be tied to deployment slots. An example of connection strings in JSON formatting that you would use for bulk adding or editing:

```
[
  {
    "name": "name-1",
    "value": "conn-string-1",
    "type": "SQLServer",
    "slotSetting": false
  },
  {
    "name": "name-2",
    "value": "conn-string-2",
    "type": "PostgreSQL",
    "slotSetting": false
  },
  ...
]

```

Note

.NET apps targeting PostgreSQL should set the connection string to **Custom** as work around for a known issue in .NET `EnvironmentVariablesConfigurationProvider`.

At runtime, connection strings are available as environment variables, prefixed with the following connection types:

* SQLServer: `SQLCONNSTR_`
* MySQL: `MYSQLCONNSTR_`
* SQLAzure: `SQLAZURECONNSTR_`
* Custom: `CUSTOMCONNSTR_`
* PostgreSQL: `POSTGRESQLCONNSTR_`
* Notification Hub: `NOTIFICATIONHUBCONNSTR_`
* Service Bus: `SERVICEBUSCONNSTR_`
* Event Hub: `EVENTHUBCONNSTR_`
* Document DB: `DOCDBCONNSTR_`
* Redis Cache: `REDISCACHECONNSTR_`

For example, a MySQL connection string named *connectionstring1* can be accessed as the environment variable `MYSQLCONNSTR_connectionString1`.

### Configure environment variables for custom containers

Your custom container might use environment variables that need to be supplied externally. You can pass them in via the Cloud Shell. In Bash:

```
az webapp config appsettings set --resource-group <group-name> --name <app-name> --settings key1=value1 key2=value2

```

In PowerShell:

```
Set-AzWebApp -ResourceGroupName <group-name> -Name <app-name> -AppSettings @{"DB_HOST"="myownserver.mysql.database.azure.com"}

```

When your app runs, the App Service app settings are injected into the process as environment variables automatically. You can verify container environment variables with the URL `https://<app-name>.scm.azurewebsites.net/Env`.

---

## Configure general settings

In the **Configuration \> General settings** section you can configure some common settings for your app. Some settings require you to scale up to higher pricing tiers.

A list of the currently available settings:

* **Stack settings**: The software stack to run the app, including the language and SDK versions. For Linux apps and custom container apps, you can also set an optional start\-up command or file.
* **Platform settings**: Lets you configure settings for the hosting platform, including:

	+ **Platform bitness**: 32\-bit or 64\-bit. For Windows apps only.
	+ **FTP state**: Allow only FTPS or disable FTP altogether.
	+ **HTTP version**: Set to **2\.0** to enable support for HTTPS/2 protocol.
	
	
	
	Note
	
	
	Most modern browsers support HTTP/2 protocol over TLS only, while nonencrypted traffic continues to use HTTP/1\.1\. To ensure that client browsers connect to your app with HTTP/2, secure your custom DNS name.
	+ **Web sockets**: For ASP.NET SignalR or socket.io, for example.
	+ **Always On**: Keeps the app loaded even when there's no traffic. When **Always On** isn't turned on (default), the app is unloaded after 20 minutes without any incoming requests. The unloaded app can cause high latency for new requests because of its warm\-up time. When **Always On** is turned on, the front\-end load balancer sends a GET request to the application root every five minutes. The continuous ping prevents the app from being unloaded.
	
	
	Always On is required for continuous WebJobs or for WebJobs that are triggered using a CRON expression.
	+ **ARR affinity**: In a multi\-instance deployment, ensure that the client is routed to the same instance for the life of the session. You can set this option to **Off** for stateless applications.
	+ **HTTPS Only**: When enabled, all HTTP traffic is redirected to HTTPS.
	+ **Minimum TLS version**: Select the minimum TLS encryption version required by your app.
* **Debugging**: Enable remote debugging for ASP.NET, ASP.NET Core, or Node.js apps. This option turns off automatically after 48 hours.
* **Incoming client certificates**: Require client certificates in mutual authentication. TLS mutual authentication is used to restrict access to your app by enabling different types of authentication for it.

---

## Configure path mappings

In the **Configuration \> Path mappings** section you can configure handler mappings, and virtual application and directory mappings. The **Path mappings** page displays different options based on the OS type.

### Windows apps (uncontainerized)

For Windows apps, you can customize the IIS handler mappings and virtual applications and directories.

Handler mappings let you add custom script processors to handle requests for specific file extensions. To add a custom handler, select **New handler mapping**. Configure the handler as follows:

* **Extension**: The file extension you want to handle, such as \**.php* or *handler.fcgi*.
* **Script processor**: The absolute path of the script processor. Requests to files that match the file extension are processed by the script processor. Use the path `D:\home\site\wwwroot` to refer to your app's root directory.
* **Arguments**: Optional command\-line arguments for the script processor.

Each app has the default root path (`/`) mapped to `D:\home\site\wwwroot`, where your code is deployed by default. If your app root is in a different folder, or if your repository has more than one application, you can edit or add virtual applications and directories.

You can configure virtual applications and directories by specifying each virtual directory and its corresponding physical path relative to the website root (`D:\home`). To mark a virtual directory as a web application, clear the **Directory** check box.

### Linux and containerized apps

You can add custom storage for your containerized app. Containerized apps include all Linux apps and also the Windows and Linux custom containers running on App Service. Select **New Azure Storage Mount** and configure your custom storage as follows:

* **Name**: The display name.
* **Configuration options**: **Basic** or **Advanced**. Select **Basic** if the storage account isn't using service endpoints, private endpoints, or Azure Key Vault. Otherwise, select **Advanced**.
* **Storage accounts**: The storage account with the container you want.
* **Storage type**: **Azure Blobs** or **Azure Files**. Windows container apps only support Azure Files. Azure Blobs only supports read\-only access.
* **Storage container**: For basic configuration, the container you want.
* **Share name**: For advanced configuration, the file share name.
* **Access key**: For advanced configuration, the access key.
* **Mount path**: The absolute path in your container to mount the custom storage.
* **Deployment slot setting**: When checked, the storage mount settings also apply to deployment slots.

---

## Enable diagnostic logging

There are built\-in diagnostics to assist with debugging an App Service app. In this lesson, you learn how to enable diagnostic logging and add instrumentation to your application, and how to access the information logged by Azure.

The following table shows the types of logging, the platforms supported, and where the logs can be stored and located for accessing the information.

| Type | Platform | Location | Description |
| --- | --- | --- | --- |
| Application logging | Windows, Linux | App Service file system and/or Azure Storage blobs | Logs messages generated by your application code. The messages are generated by the web framework you choose, or from your application code directly using the standard logging pattern of your language. Each message is assigned one of the following categories: **Critical**, **Error**, **Warning**, **Info**, **Debug**, and **Trace**. |
| Web server logging | Windows | App Service file system or Azure Storage blobs | Raw HTTP request data in the W3C extended log file format. Each log message includes data like the HTTP method, resource URI, client IP, client port, user agent, response code, and so on. |
| Detailed error messages | Windows | App Service file system | Copies of the *.html* error pages that would otherwise be sent to the client browser. For security reasons, detailed error pages shouldn't be sent to clients in production, but App Service can save the error page each time an application error occurs that has HTTP code 400 or greater. |
| Failed request tracing | Windows | App Service file system | Detailed tracing information on failed requests, including a trace of the IIS components used to process the request and the time taken in each component. One folder is generated for each failed request, which contains the XML log file, and the XSL stylesheet to view the log file with. |
| Deployment logging | Windows, Linux | App Service file system | Helps determine why a deployment failed. Deployment logging happens automatically and there are no configurable settings for deployment logging. |

### Enable application logging (Windows)

1. To enable application logging for Windows apps in the Azure portal, navigate to your app and select **Monitoring** \> **App Service logs**.
2. Select **On** for either **Application Logging (Filesystem)** or **Application Logging (Blob)**, or both. The **Filesystem** option is for temporary debugging purposes, and turns itself off in 12 hours. The **Blob** option is for long\-term logging, and needs a blob storage container to write logs to.

Note

If you regenerate your storage account's access keys, you must reset the respective logging configuration to use the updated access keys. To do this turn the logging feature off and then on again.
3. You can also set the **Level** of details included in the log as shown in the following table.

| Level | Included categories |
| --- | --- |
| **Disabled** | None |
| **Error** | Error, Critical |
| **Warning** | Warning, Error, Critical |
| **Information** | Info, Warning, Error, Critical |
| **Verbose** | Trace, Debug, Info, Warning, Error, Critical (all categories) |
4. When finished, select **Save**.

### Enable application logging (Linux/Container)

1. In **App Service logs** set the **Application logging** option to **File System**.
2. In **Quota (MB)**, specify the disk quota for the application logs. In **Retention Period (Days)**, set the number of days the logs should be retained.
3. When finished, select **Save**.

### Enable web server logging

1. For **Web server logging**, select **Storage** to store logs on blob storage, or **File System** to store logs on the App Service file system.
2. In **Retention Period (Days)**, set the number of days the logs should be retained.
3. When finished, select **Save**.

### Add log messages in code

In your application code, you use the usual logging facilities to send log messages to the application logs. For example:

* ASP.NET applications can use the `System.Diagnostics.Trace` class to log information to the application diagnostics log. For example:

```
System.Diagnostics.Trace.TraceError("If you're seeing this, something bad happened");

```

ASP.NET Core includes the Azure App Service logging provider. Enable it when configuring logging, for example:

```
builder.Logging.AddAzureWebAppDiagnostics();

```
* Python applications should use [OpenTelemetry with Azure Monitor](/en-us/azure/azure-monitor/app/opentelemetry-enable) to send logs to the application diagnostics log.

### Send logs to Azure Monitor

You can forward platform and application logs to Azure Monitor destinations via Diagnostic Settings.

* In the Azure portal, open your app and select **Monitoring** \> **Diagnostic settings**, then add a diagnostic setting to send logs to a Log Analytics workspace, Storage account, or Event Hubs.
* Common categories include **AppServiceHTTPLogs** (web server logs) and **AppServiceConsoleLogs** (stdout/stderr). For details, see [Supported resource logs for Microsoft.Web](/en-us/azure/app-service/monitor-app-service-reference#supported-resource-logs-for-microsoftweb).

### Stream logs

Before you stream logs in real time, enable the log type that you want. Any information written to files ending in .txt, .log, or .htm that are stored in the `/home/LogFiles` directory (Windows: `D:\home\LogFiles`) is streamed by App Service.

Note

Some types of logging buffer write to the log file, which can result in out of order events in the stream. For example, an application log entry that occurs when a user visits a page may be displayed in the stream before the corresponding HTTP log entry for the page request.

* Azure portal \- To stream logs in the Azure portal, navigate to your app and select **Log stream**.
* Azure CLI \- To stream logs live in Cloud Shell, use the following command (note: Cloud Shell may not work for some Linux\-based plans; use the local CLI if needed):

```
az webapp log tail --name appname --resource-group myResourceGroup

```

To filter specific log types, such as HTTP or application logs, use the `--provider` parameter, for example:

```
az webapp log tail --name appname --resource-group myResourceGroup --provider http

```
* Local console \- To stream logs in the local console, install Azure CLI and sign in to your account. Once signed in, follow the instructions shown for Azure CLI.

### Access log files

If you configure the Azure Storage blobs option for a log type, you need a client tool that works with Azure Storage.

For logs stored in the App Service file system, the easiest way is to download the ZIP file in the browser at:

* Linux/container apps: `https://<app-name>.scm.azurewebsites.net/api/logs/docker/zip`
* Windows apps: `https://<app-name>.scm.azurewebsites.net/api/logs/zip`

Note

The `api/dump` endpoint downloads a full diagnostic dump, not just logs. Use `api/logs/zip` to download only log files.

For Linux/container apps, the ZIP file contains console output logs for both the docker host and the docker container. For a scaled\-out app, the ZIP file contains one set of logs for each instance. In the App Service file system, these log files are the contents of the */home/LogFiles* directory.

---

## Configure security certificates

Azure App Service has tools that let you create, upload, or import a private certificate or a public certificate into App Service.

A certificate uploaded into an app is stored in a deployment unit that is bound to the app service plan's resource group and region combination (internally called a *webspace*). The certificate is accessible to other apps in the same resource group and region combination.

The table below details the options you have for adding certificates in App Service:

| Option | Description |
| --- | --- |
| Create a free App Service managed certificate | A private certificate that's free of charge and easy to use if you just need to secure your custom domain in App Service. |
| Purchase an App Service certificate | A private certificate managed by Azure. It combines the simplicity of automated certificate management and the flexibility of renewal and export options. |
| Import a certificate from Key Vault | Useful if you use Azure Key Vault to manage your certificates. |
| Upload a private certificate | If you already have a private certificate from a third\-party provider, you can upload it. |
| Upload a public certificate | Public certificates aren't used to secure custom domains, but you can load them into your code if you need them to access remote resources. |

### Private certificate requirements

The free **App Service managed certificate** and the **App Service certificate** already satisfy the requirements of App Service. If you want to use a private certificate in App Service, your certificate must meet the following requirements:

* Exported as a password\-protected PFX file, encrypted using triple DES.
* Contains private key at least 2,048 bits long.
* Contains all intermediate certificates and the root certificate in the certificate chain.

To secure a custom domain in a TLS binding, the certificate has other requirements:

* Contains an Extended Key Usage for server authentication (OID \= 1\.3\.6\.1\.5\.5\.7\.3\.1\)
* Signed by a trusted certificate authority

### Creating a free managed certificate

To create custom TLS/SSL bindings or enable client certificates for your App Service app, your App Service plan must be in the **Basic**, **Standard**, **Premium**, or **Isolated** tier.

The free App Service managed certificate is a turn\-key solution for securing your custom DNS name in App Service. It's a TLS/SSL server certificate fully managed by App Service and renewed continuously and automatically in six\-month increments, 45 days before expiration. You create the certificate and bind it to a custom domain, and let App Service do the rest.

Important

Before you create a free managed certificate, make sure you meet the prerequisites for your app. Free certificates are issued by DigiCert. For some domains, you must explicitly allow DigiCert as a certificate issuer by creating a CAA domain record with the value: `0 issue digicert.com`. Azure fully manages the certificates on your behalf, so any aspect of the managed certificate, including the root issuer, can change at any time. These changes are outside your control. Make sure to avoid hard dependencies and "pinning" practice certificates to the managed certificate or any part of the certificate hierarchy.

The free certificate comes with the following limitations:

* Doesn't support wildcard certificates.
* Doesn't support usage as a client certificate by using certificate thumbprint, which is planned for deprecation and removal.
* Doesn't support private DNS.
* Isn't exportable.
* Isn't supported in an App Service Environment (ASE).
* Only supports alphanumeric characters, dashes (\-), and periods (.).
* Only custom domains of length up to 64 characters are supported.

### Import an App Service Certificate

If you purchase an App Service Certificate from Azure, Azure manages the following tasks:

* Takes care of the purchase process from certificate provider.
* Performs domain verification of the certificate.
* Maintains the certificate in Azure Key Vault.
* Manages certificate renewal.
* Synchronize the certificate automatically with the imported copies in App Service apps.

If you already have a working App Service certificate, you can:

* Import the certificate into App Service.
* Manage the certificate, such as renew, rekey, and export it.

Note

App Service Certificates aren't supported in Azure National Clouds at this time.

---

## Summary

In this module, you learned how to:

* Create application settings that are bound to deployment slots.
* Explain the options for installing SSL/TLS certificates for your app.
* Enable diagnostic logging for your app to aid in monitoring and debugging.
* Create virtual app to directory mappings.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/configure-web-app-settings/_

## Fuentes
- [Configure web app settings](https://learn.microsoft.com/en-us/training/modules/configure-web-app-settings/?WT.mc_id=api_CatalogApi)
