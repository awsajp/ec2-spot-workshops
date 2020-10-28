## EC2 Spot OD Fallback Strategy for EKS

For detailed Architecture diagram, please refer to EC2-Spot-OD-Fallback-Strategy.pptx

In this workshop, you will deploy the following:

### Step1 : Create a Launch Template 
TBD

Run the following command to substitute the template with actual values from the global variables

```bash
sed -i -e "s#%ASG_NAME%#$ASG_NAME#g"  -e "s#%OD_PERCENTAGE%#$OD_PERCENTAGE#g" -e "s#%PUBLIC_SUBNET_LIST%#$VPCPublicSubnets#g"  asg.json
```

### Step2 : Create a ASG1_SPOT for only Spot instances 
OD_BASE=0
MIN_SIZE=3
MAX_SIZE=6
DESIREDS_SIZE=3
OD_PERCENTAGE=0
### Step3 : Create a ASG2_OD for only OD instances 
OD_BASE=0
MIN_SIZE=0
MAX_SIZE=3
DESIREDS_SIZE=0
OD_PERCENTAGE=100

Both ASG1_SPOT and ASG2_OD are used for Solution #1 using CW Alarms
Create Cloud Watch alarm ASG1_SPOT_CAPACITY_ALARM for ASG1_SPOT if the ASG metric
GroupTotalInstances<3 for 2 data points with period 1 min

Create Cloud Watch alarm ASG1_SPOT_CAPACITY_OK for ASG1_SPOT if the ASG metric
GroupTotalInstances>=3 for 1 data points with period 5 min

if Spot Interruption happens in ASG1_SPOT, ASG1_SPOT_CAPACITY_ALARM triggers and OD instance gets created in ASG2_OD
if Spot Capacity is available in ASG1_SPOT, ASG1_SPOT_CAPACITY_OK triggers and OD instance gets terminated in ASG2_OD

This replacement takes around 5 min as explained in the PPT

### Step4 : Create a Lambda function to handle spot interruption

### Step5 : Create a ASG3_SPOT for only SPOT instances 
OD_BASE=0
MIN_SIZE=3
MAX_SIZE=6
DESIREDS_SIZE=3
OD_PERCENTAGE=0
### Step3 : Create a ASG4_OD for only OD instances 
OD_BASE=0
MIN_SIZE=3
MAX_SIZE=6
DESIREDS_SIZE=3
OD_PERCENTAGE=100

Both ASG3_SPOT and ASG4_OD are used for Solution #2 using CW Events
Create Cloud Watch Event/Rules ASG3_spot-interruption-event and ASG3_spot-Fulfillment-event
and registers a lambda function as the target.


if Spot Interruption happens in ASG3_SPOT, Event "CW Event: EC2 Spot Instance 
Interruption Warning" triggers and Lambda increases the desired capacity in ASG4_OD

if Spot Capacity is available in ASG3_SPOT, Event "EC2 Spot Instance 
Request Fulfillment" triggers and Lambda increases the decreases capacity in ASG4_OD


This replacement takes immediateley min as explained in PPT. 

### Workshop Cleanup
