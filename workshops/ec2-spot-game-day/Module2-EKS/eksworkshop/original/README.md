# Provision Accounts for Container Day labs using Event Engine



## Event Engine

The AWS Event Engine was created to help AWS field teams run Workshops, GameDays, Bootcamps, Immersion Days,
and other events that require hands-on access to AWS accounts.

For introduction and please refer to [onboarding guide](https://w.amazon.com/bin/view/AWS_EventEngine/)

## Create Event engine module and blueprint

### Introduction

A module is a self-contained piece of content that can be consumed by customers. For example, EKS Lab in a
[workshop](http://labs.awscontainerday.com/eks.html). A module can be comprised of a master template, a team
template, a readme, an IAM policy, and any additional artifacts. Once you've defined your module, you can then build a
Blueprint by selecting this, and possibly other modules, together.

In the following section we will look at how you can build a module using existing [template](EE_team_template.yaml). We will then create a blue print to provision accounts using these modules.

> Please make sure to review the template before you proceed. For example, EKS template has the eksctl configuration file embedded in CFN. It uses us-east-1 as default region and Kubernetes v1.16 as default version. You can also add any other configuration supported by eksctl.

### Create a module 

1. Browse to [event engine](https://admin.eventengine.run) and click on Backend -> Module

| **EE Home Page** |
|:--:| 
| ![EE Home Page](images/ee_create_module_or_blueprint.png) | 

***

| **Create Module** |
|:--:| 
| ![Create module](images/ee_create_module.png) | 




2. Specify name, label and description for your module and click create.

| **Module Details** |
|:--:| 
| ![Module Details](images/module_details.png) | 


3. Once a module is created, proceed to customizing your module by using cloudformation template and custom IAM policies.

| **Edit Config** |
|:--:| 
| ![Edit Config](images/ee_config_module.png) | 

4. Start with defining an IAM settings for the users. Use [IAM Policy Statements](EE_IAM.json) and [IAM Trusted Services](EE_IAM_trust_policy.txt)

| **Module IAM Config** |
|:--:| 
| ![Module IAM Config](images/ee_module_iam_config.png) | 

5. Next, update team template. This is used to provision resources used for Lab and click save.

| **Module Team template** |
|:--:| 
| ![Module team template](images/ee_module_team_template.png) | 

> This template will provision - 
> Cloud9 IDE for ECS Labs and EKS Cluster usiing m5.xlarge worker nodes. 
> Cloud9 IDE for ECS Labs and a Fargate Cluster.

| **Save module** |
|:--:| 
| ![Save module](images/save_module.png) | 

### Create a blueprint 


1. Browse to [event engine](https://admin.eventengine.run) and click on Backend -> Blueprint -> Create Blueprint

| **EE Home Page** |
|:--:| 
| ![EE Home Page](images/ee_create_module_or_blueprint.png) | 


2. Provide blueprint Type, Name, description and click Create

| **Create blueprint** |
|:--:| 
| ![Create Blueprint](images/create_blueprint.png) | 


3. Add module(s) to your blueprint and Click save.

| **Add module to blueprint 1/3** |
|:--:| 
| ![Save module](images/add_module_to_blueprint.png) | 

***

| **Add module to blueprint 2/3** |
|:--:| 
| ![Save module](images/add_module_template.png) | 

***

| **Add module to blueprint 3/3** |
|:--:| 
| ![Save module](images/save_blueprint.png) | 

## Provision Accounts 

1. Browse to [event engine](https://admin.eventengine.run) and click on Create Event

2. Select blueprint

| **Add module to blueprint 3/3** |
|:--:| 
| ![Save module](images/create_event_1.png) | 


3. Provide Event Details

| **Add module to blueprint 3/3** |
|:--:| 
| ![Save module](images/create_event_2.png) | 


4. Team and Customer Information

| **Add module to blueprint 3/3** |
|:--:| 
| ![Save module](images/create_event_3.png) | 


5. Initialize and Monitor Event

>It will take a while before accounts are provisioned. Meanwhile you can export account hash and keep them ready to
> be printed or emailed. Check back after a while to make sure all accounts are successfully provisioned.

| **Add module to blueprint 3/3** |
|:--:| 
| ![Save module](images/create_event_4.png) | 

> All status squares should be green. Yellow means provisioning is still in progress, whereas red indicates that account
> wasn’t successfully provisioned.



### Handle transient failures

If an account status is red, you can disable (undeploy) and enable (deploy) module again. This usually helps with any
transient issues during account creation.

| **Manage Account** |
|:--:| 
| ![Troubleshooting Account 1/3](images/manage_account_1.png) | 

***

| **Undeploy module** |
|:--:| 
| ![Troubleshooting Account 2/3](images/manage_account_2.png) | 

***

| **Deploy module** |
|:--:| 
| ![Troubleshooting Account 3/3](images/manage_account_3.png) | 

***


### Export account details

| **Export accounts details** |
|:--:| 
| ![Export accounts details](images/export_account.png) | 

***

### Terminate Event

> Always remember to terminate event on completion.

| **Terminate Event** |
|:--:| 
| ![Terminate Event](images/terminate_event.png) | 