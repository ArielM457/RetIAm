# Explain threat hunting concepts in Microsoft Sentinel

> Curso: Perform threat hunting in Microsoft Sentinel (wwl-sc-200-perform-threat-hunting-azure-sentinel) · Seccion: Perform threat hunting in Microsoft Sentinel
> Duracion estimada: 23 min

## Objetivos
- (pendiente de expansion por agente)

## Contenido
## Introduction

Microsoft Sentinel provides the tools to perform Threat Hunting. Before starting the hunt, it's crucial to understand the Threat Hunting process.

You're a Security Operations Analyst working at a company that implemented Microsoft Sentinel. You want to mature your Security Operations team to proactively hunt for malicious activity in your environment.

You suggest to management to create a threat hunting team. You must explain to management the benefit, processes, and tasks of a threat hunting team. You'll demonstrate how to develop a quality hypothesis for hunting.

After completing this module, you'll be able to:

* Describe threat hunting concepts for use with Microsoft Sentinel
* Define a threat hunting hypothesis for use in Microsoft Sentinel

### Prerequisites

Basic knowledge of operational concepts such as monitoring, logging, and alerting

---

## Develop a hypothesis

Hunting starts with a Hypothesis. The idea of what we are going to hunt. Getting this right is critical because it drives our focuses on what we are going to do. What makes a good Hypothesis?

There are many factors, but here are the key ones:

**Keep it achievable**. Don't perform a hunt where you know you have no hope of finding results. It could be that you don't have the data available, or have insufficient knowledge about the threat to understand how to find it.

**Keep the scope narrow**. Avoid broad a hypothesis such as "I'm going to hunt for strange log\-ons." Such a hypothesis fails to define what the results could mean.

**Keep it time\-bound**. Are you looking for any sign\-ins since the beginning of your logs? Are you looking for last week? The last day? The time\-bounded also is used in documentation. You'll want Threat Hunting to be a continual process. If you don't time\-bound your hunts, there's a chance that you'll end up just repeating the same hunt on the same dataset. You'll be able to say, "I did this hunt, at this time, covering this period." With this documented, your team members will know what period was hunted for with this Hypothesis.

**Keep it useful and efficient**. You want to target threats that maybe you don't have adequate coverage for in your detections. These might be things that you know that you've previously missed or that you haven't detected. A good SOC team typically has a good idea about where their coverage is good and where it may be weaker and needs improvement. You also want to make sure it relates to realistic threats. There's no point in hunting for an advanced threat that targets an industry you're not in or a platform you aren't using.

**Keep it related to the threat model that you are defending against**. Otherwise, you may spend much time threat hunting for things that you'll never find and which aren't a threat.

Don't start your Threat Hunting journey going after the most advanced threats. Start with the basics and incrementally mature your organization's Threat Hunting capabilities. Start with a simple Hunt Hypothesis. An example hypothesis could be that we have Threat Intel that a Threat Actor, has automated attacks that use the cmd.exe process.

Another Hypothesis could be; We want to check for the last day in which accounts have run cmd.exe, but that have not run cmd.exe during the past week.

---

_Fuente oficial: https://learn.microsoft.com/en-us/training/modules/what-is-threat-hunting-azure-sentinel/_

## Fuentes
- [Explain threat hunting concepts in Microsoft Sentinel](https://learn.microsoft.com/en-us/training/modules/what-is-threat-hunting-azure-sentinel/?WT.mc_id=api_CatalogApi)
