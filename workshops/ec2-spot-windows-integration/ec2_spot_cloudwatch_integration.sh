#!/bin/bash 

echo "Creating the Infrastructure for ec2-spot-cwt-od-fallback workshop ..."


#yum update -y
#yum -y install jq amazon-efs-utils


#Global Defaults
WORKSHOP_NAME=ec2-spot-cwt-od-fallback
LAUNCH_TEMPLATE_NAME=$WORKSHOP_NAME-LT
ASG1_NAME_SPOT=$WORKSHOP_NAME-asg1-spot
ASG2_NAME_OD=$WORKSHOP_NAME-asg2-od

ASG3_NAME_SPOT=$WORKSHOP_NAME-asg3-spot
ASG4_NAME_OD=$WORKSHOP_NAME-asg4-od


LAUNCH_TEMPLATE_VERSION=1
IAM_INSTANT_PROFILE_ARN=arn:aws:iam::000474600478:instance-profile/ecsInstanceRole
SECURITY_GROUP=sg-4f3f0d1e



#EBS Settings

EBS_TYPE=gp2
EBS_SIZE=8
EBS_DEV=/dev/xvdb

#SECONDARY_PRIVATE_IP="172.31.81.24"
MAC=$(curl -s http://169.254.169.254/latest/meta-data/mac)
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
AWS_AVAIALABILITY_ZONE=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.availabilityZone')
AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
INTERFACE_ID=$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/interface-id)

cp -Rfp templates/*.json .
cp -Rfp templates/*.txt .

export AMI_ID=$(aws ec2 describe-images --owners amazon --filters 'Name=name,Values=amzn2-ami-hvm-2.0.????????-x86_64-gp2' 'Name=state,Values=available' --output json | jq -r '.Images | sort_by(.CreationDate) | last(.[]).ImageId')
echo "Latest ECS Optimized Amazon AMI_ID is $AMI_ID"

sed -i.bak -e "s#%instanceProfile%#$IAM_INSTANT_PROFILE_ARN#g"  launch-template-data.json
sed -i.bak -e "s#%instanceSecurityGroup%#$SECURITY_GROUP#g"  launch-template-data.json
sed -i.bak -e "s#%workshopName%#$WORKSHOP_NAME#g"  launch-template-data.json
sed -i.bak  -e "s#%ami-id%#$AMI_ID#g" -e "s#%UserData%#$(cat user-data.txt | base64 --wrap=0)#g" launch-template-data.json


#LAUCH_TEMPLATE_ID=$(aws ec2 create-launch-template --launch-template-name $LAUNCH_TEMPLATE_NAME --version-description $LAUNCH_TEMPLATE_VERSION --launch-template-data file://launch-template-data.json | jq -r '.LaunchTemplate.LaunchTemplateId')
LAUCH_TEMPLATE_ID=lt-04fb033ec5a075f22
echo "Amazon LAUCH_TEMPLATE_ID is $LAUCH_TEMPLATE_ID"

ASG_NAME=$ASG1_NAME_SPOT
OD_BASE=0
OD_PERCENTAGE=0
MIN_SIZE=3
MAX_SIZE=6
DESIREDS_SIZE=3
PUBLIC_SUBNET_LIST="subnet-764d7d11,subnet-a2c2fd8c,subnet-cb26e686,subnet-7acbf626,subnet-93d490ad,subnet-313ad03f"
INSTANCE_TYPE_1=m4.large
INSTANCE_TYPE_2=c4.large
INSTANCE_TYPE_3=r4.large
INSTANCE_TYPE_4=m5.large
INSTANCE_TYPE_5=c5.large
INSTANCE_TYPE_6=r5.large
SERVICE_ROLE_ARN="arn:aws:iam::000474600478:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling"

sed -i.bak -e "s#%ASG_NAME%#$ASG_NAME#g"  asg.json
sed -i.bak -e "s#%LAUNCH_TEMPLATE_NAME%#$LAUNCH_TEMPLATE_NAME#g"  asg.json
sed -i.bak -e "s#%LAUNCH_TEMPLATE_VERSION%#$LAUNCH_TEMPLATE_VERSION#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_1%#$INSTANCE_TYPE_1#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_2%#$INSTANCE_TYPE_2#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_3%#$INSTANCE_TYPE_3#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_4%#$INSTANCE_TYPE_4#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_5%#$INSTANCE_TYPE_5#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_6%#$INSTANCE_TYPE_6#g"  asg.json
sed -i.bak -e "s#%OD_BASE%#$OD_BASE#g"  asg.json
sed -i.bak -e "s#%OD_PERCENTAGE%#$OD_PERCENTAGE#g"  asg.json
sed -i.bak -e "s#%MIN_SIZE%#$MIN_SIZE#g"  asg.json
sed -i.bak -e "s#%MAX_SIZE%#$MAX_SIZE#g"  asg.json
sed -i.bak -e "s#%DESIREDS_SIZE%#$DESIREDS_SIZE#g"  asg.json
sed -i.bak -e "s#%OD_BASE%#$OD_BASE#g"  asg.json
sed -i.bak -e "s#%PUBLIC_SUBNET_LIST%#$PUBLIC_SUBNET_LIST#g"  asg.json
sed -i.bak -e "s#%SERVICE_ROLE_ARN%#$SERVICE_ROLE_ARN#g"  asg.json

aws autoscaling create-auto-scaling-group --cli-input-json file://asg.json
ASG_ARN=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name $ASG_NAME | jq -r '.AutoScalingGroups[0].AutoScalingGroupARN')
echo "$ASG1_NAME_SPOT ARN=$ASG_ARN"

aws autoscaling enable-metrics-collection --auto-scaling-group-name $ASG1_NAME_SPOT --granularity "1Minute"


cp -Rfp templates/asg.json .

ASG_NAME=$ASG2_NAME_OD
OD_BASE=0
OD_PERCENTAGE=100
MIN_SIZE=0
MAX_SIZE=3
DESIREDS_SIZE=0

sed -i.bak -e "s#%ASG_NAME%#$ASG_NAME#g"  asg.json
sed -i.bak -e "s#%LAUNCH_TEMPLATE_NAME%#$LAUNCH_TEMPLATE_NAME#g"  asg.json
sed -i.bak -e "s#%LAUNCH_TEMPLATE_VERSION%#$LAUNCH_TEMPLATE_VERSION#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_1%#$INSTANCE_TYPE_1#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_2%#$INSTANCE_TYPE_2#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_3%#$INSTANCE_TYPE_3#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_4%#$INSTANCE_TYPE_4#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_5%#$INSTANCE_TYPE_5#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_6%#$INSTANCE_TYPE_6#g"  asg.json
sed -i.bak -e "s#%OD_BASE%#$OD_BASE#g"  asg.json
sed -i.bak -e "s#%OD_PERCENTAGE%#$OD_PERCENTAGE#g"  asg.json
sed -i.bak -e "s#%MIN_SIZE%#$MIN_SIZE#g"  asg.json
sed -i.bak -e "s#%MAX_SIZE%#$MAX_SIZE#g"  asg.json
sed -i.bak -e "s#%DESIREDS_SIZE%#$DESIREDS_SIZE#g"  asg.json
sed -i.bak -e "s#%OD_BASE%#$OD_BASE#g"  asg.json
sed -i.bak -e "s#%PUBLIC_SUBNET_LIST%#$PUBLIC_SUBNET_LIST#g"  asg.json
sed -i.bak -e "s#%SERVICE_ROLE_ARN%#$SERVICE_ROLE_ARN#g"  asg.json

aws autoscaling create-auto-scaling-group --cli-input-json file://asg.json
ASG_ARN=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name $ASG_NAME | jq -r '.AutoScalingGroups[0].AutoScalingGroupARN')
echo "$ASG2_NAME_OD ARN=$ASG_ARN"

aws autoscaling enable-metrics-collection --auto-scaling-group-name $ASG2_NAME_OD --granularity "1Minute"

ASG2_OD_SCALE_OUT_POLICY=$(aws autoscaling put-scaling-policy --policy-name $ASG2_NAME_OD-Scale-Out-Policy \
--auto-scaling-group-name $ASG2_NAME_OD --scaling-adjustment +1 \
--adjustment-type ChangeInCapacity | jq -r '.PolicyARN')

aws cloudwatch put-metric-alarm --alarm-name ASG1_SPOT_CAPACITY_ALARM \
    --alarm-description "Spot Capacity Insufficient Alarm for $ASG1_NAME_SPOT" \
    --metric-name GroupTotalInstances --namespace AWS/AutoScaling --statistic Average \
    --period 60 --threshold 3 --comparison-operator LessThanThreshold \
    --dimensions "Name=AutoScalingGroupName,Value=$ASG1_NAME_SPOT" --evaluation-periods 2 \
    --alarm-actions $ASG2_OD_SCALE_OUT_POLICY
    

ASG2_OD_SCALE_IN_POLICY=$(aws autoscaling put-scaling-policy --policy-name $ASG2_NAME_OD-Scale-In-Policy \
--auto-scaling-group-name $ASG2_NAME_OD --scaling-adjustment -1 \
--adjustment-type ChangeInCapacity | jq -r '.PolicyARN')


aws cloudwatch put-metric-alarm --alarm-name ASG1_SPOT_CAPACITY_OK \
    --alarm-description "Spot Capacity OK Alarm for $ASG1_NAME_SPOT" \
    --metric-name GroupTotalInstances --namespace AWS/AutoScaling --statistic Average \
    --period 300 --threshold 3 --comparison-operator GreaterThanOrEqualToThreshold \
    --dimensions "Name=AutoScalingGroupName,Value=$ASG1_NAME_SPOT" --evaluation-periods 1 \
    --alarm-actions $ASG2_OD_SCALE_IN_POLICY
    
    
cp -Rfp templates/asg.json .

ASG_NAME=$ASG3_NAME_SPOT
OD_BASE=0
OD_PERCENTAGE=0
MIN_SIZE=3
MAX_SIZE=6
DESIREDS_SIZE=3

sed -i.bak -e "s#%ASG_NAME%#$ASG_NAME#g"  asg.json
sed -i.bak -e "s#%LAUNCH_TEMPLATE_NAME%#$LAUNCH_TEMPLATE_NAME#g"  asg.json
sed -i.bak -e "s#%LAUNCH_TEMPLATE_VERSION%#$LAUNCH_TEMPLATE_VERSION#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_1%#$INSTANCE_TYPE_1#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_2%#$INSTANCE_TYPE_2#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_3%#$INSTANCE_TYPE_3#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_4%#$INSTANCE_TYPE_4#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_5%#$INSTANCE_TYPE_5#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_6%#$INSTANCE_TYPE_6#g"  asg.json
sed -i.bak -e "s#%OD_BASE%#$OD_BASE#g"  asg.json
sed -i.bak -e "s#%OD_PERCENTAGE%#$OD_PERCENTAGE#g"  asg.json
sed -i.bak -e "s#%MIN_SIZE%#$MIN_SIZE#g"  asg.json
sed -i.bak -e "s#%MAX_SIZE%#$MAX_SIZE#g"  asg.json
sed -i.bak -e "s#%DESIREDS_SIZE%#$DESIREDS_SIZE#g"  asg.json
sed -i.bak -e "s#%OD_BASE%#$OD_BASE#g"  asg.json
sed -i.bak -e "s#%PUBLIC_SUBNET_LIST%#$PUBLIC_SUBNET_LIST#g"  asg.json
sed -i.bak -e "s#%SERVICE_ROLE_ARN%#$SERVICE_ROLE_ARN#g"  asg.json

aws autoscaling create-auto-scaling-group --cli-input-json file://asg.json
ASG_ARN=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name $ASG_NAME | jq -r '.AutoScalingGroups[0].AutoScalingGroupARN')
echo "$ASG3_NAME_SPOT ARN=$ASG_ARN"

aws autoscaling enable-metrics-collection --auto-scaling-group-name $ASG3_NAME_SPOT --granularity "1Minute"


cp -Rfp templates/asg.json .
ASG_NAME=$ASG4_NAME_OD
OD_BASE=0
OD_PERCENTAGE=100
MIN_SIZE=3
MAX_SIZE=6
DESIREDS_SIZE=3

sed -i.bak -e "s#%ASG_NAME%#$ASG_NAME#g"  asg.json
sed -i.bak -e "s#%LAUNCH_TEMPLATE_NAME%#$LAUNCH_TEMPLATE_NAME#g"  asg.json
sed -i.bak -e "s#%LAUNCH_TEMPLATE_VERSION%#$LAUNCH_TEMPLATE_VERSION#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_1%#$INSTANCE_TYPE_1#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_2%#$INSTANCE_TYPE_2#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_3%#$INSTANCE_TYPE_3#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_4%#$INSTANCE_TYPE_4#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_5%#$INSTANCE_TYPE_5#g"  asg.json
sed -i.bak -e "s#%INSTANCE_TYPE_6%#$INSTANCE_TYPE_6#g"  asg.json
sed -i.bak -e "s#%OD_BASE%#$OD_BASE#g"  asg.json
sed -i.bak -e "s#%OD_PERCENTAGE%#$OD_PERCENTAGE#g"  asg.json
sed -i.bak -e "s#%MIN_SIZE%#$MIN_SIZE#g"  asg.json
sed -i.bak -e "s#%MAX_SIZE%#$MAX_SIZE#g"  asg.json
sed -i.bak -e "s#%DESIREDS_SIZE%#$DESIREDS_SIZE#g"  asg.json
sed -i.bak -e "s#%OD_BASE%#$OD_BASE#g"  asg.json
sed -i.bak -e "s#%PUBLIC_SUBNET_LIST%#$PUBLIC_SUBNET_LIST#g"  asg.json
sed -i.bak -e "s#%SERVICE_ROLE_ARN%#$SERVICE_ROLE_ARN#g"  asg.json

aws autoscaling create-auto-scaling-group --cli-input-json file://asg.json
ASG_ARN=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name $ASG_NAME | jq -r '.AutoScalingGroups[0].AutoScalingGroupARN')
echo "$ASG4_NAME_OD ARN=$ASG_ARN"

aws autoscaling enable-metrics-collection --auto-scaling-group-name $ASG4_NAME_OD --granularity "1Minute"

zip function.zip lambda_function.py

LAMBDA_ARN=$(aws lambda create-function \
    --function-name ASG3_Spot_Interruption_Handler \
    --runtime python3.8 \
    --zip-file fileb://function.zip \
    --handler lambda_function.handler \
    --environment Variables={ASG_NAME=$ASG4_NAME_OD} \
    --role  arn:aws:iam::000474600478:role/service-role/execute_my_lambda|jq -r '.FunctionArn')
    
aws events put-rule \
--name ASG3_spot-interruption-event \
--event-pattern \
'{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "EC2 Spot Instance Interruption Warning"
  ]
}'


aws events put-targets --rule ASG3_spot-interruption-event --targets "Id"="1","Arn"="$LAMBDA_ARN"

aws events put-rule \
--name ASG3_spot-Fulfillment-event \
--event-pattern \
'{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "EC2 Spot Instance Request Fulfillment"
  ]
}'

aws events put-targets --rule ASG3_spot-Fulfillment-event --targets "Id"="1","Arn"="$LAMBDA_ARN"


aws events put-rule \
--name EC2_Launch_Terminate_Events \
--event-pattern \
'{
  "source": [
    "aws.autoscaling"
  ],
  "detail-type": [
    "EC2 Instance Launch Successful",
    "EC2 Instance Terminate Successful"
  ],
  "detail": {
    "AutoScalingGroupName": [
      "ec2-spot-cwt-od-fallback-asg1-spot",
      "ec2-spot-cwt-od-fallback-asg2-od",
      "ec2-spot-cwt-od-fallback-asg3-spot",
      "ec2-spot-cwt-od-fallback-asg4-od"
    ]
  }
}'

aws events put-targets --rule EC2_Launch_Terminate_Events --targets "Id"="1","Arn"="arn:aws:sns:us-east-1:000474600478:awsajp_notification"



