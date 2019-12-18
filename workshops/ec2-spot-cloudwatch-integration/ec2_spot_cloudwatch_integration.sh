#!/bin/bash 

echo "Creating the Infrastructure for ECS_Cluster_Auto_Scaling workshop ..."


#yum update -y
#yum -y install jq amazon-efs-utils


#Global Defaults
WORKSHOP_NAME=ecs-fargate-cluster-autoscale
LAUNCH_TEMPLATE_NAME=ecs-fargate-cluster-autoscale-LT
ASG_NAME_OD=ecs-fargate-cluster-autoscale-asg-od
ASG_NAME_SPOT=ecs-fargate-cluster-autoscale-asg-spot
OD_CAPACITY_PROVIDER_NAME=od-capacity_provider_3
SPOT_CAPACITY_PROVIDER_NAME=spot-capacity_provider_3

ECS_FARGATE_CLLUSTER_NAME=EcsFargateCluster
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

aws configure set default.region ${AWS_REGION}

cp -Rfp templates/*.json .
cp -Rfp templates/*.txt .

#The following example specifies the AWS/EC2 namespace to view all the metrics for Amazon EC2.
aws cloudwatch list-metrics --namespace AWS/EC2 | jq -r '.[][].MetricName' | wc -l

#To list all the available metrics for a specified resource
#The following example specifies the AWS/EC2 namespace and the InstanceId dimension to view the
#results for the specified instance only.

aws cloudwatch list-metrics --namespace AWS/EC2 --dimensions \
                              Name=InstanceId,Value=i-0913b928725f6a665 \
                              | jq -r '.[][].MetricName' | wc -l
                              
# To list a metric for all resources
#The following example specifies the AWS/EC2 namespace and a metric name to view the results for the
#specified metric only.                          

#aws cloudwatch list-metrics --namespace AWS/EC2 --metric-name CPUUtilization

#To get average CPU utilization across your EC2 instances using the AWS CLI

aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization \
--dimensions Name=InstanceId,Value=i-0913b928725f6a665 --statistics Maximum \
--start-time 2019-12-16T12:51:00 --end-time 2019-12-17T12:51:00 --period 360

#To get DiskWriteBytes for the instances in an Auto Scaling group using the AWS CLI

aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name DiskWriteBytes
--dimensions Name=AutoScalingGroupName,Value=ecs-fargate-cluster-autoscale-asg-od --statistics "Sum" "SampleCount" \
--start-time 2016-10-16T23:18:00 --end-time 2016-10-18T23:18:00 --period 360


aws cloudwatch list-metrics --namespace "AWS/AutoScaling"

exit 0

export AMI_ID=$(aws ec2 describe-images --owners amazon --filters 'Name=name,Values=amzn2-ami-ecs-hvm-2.0.????????-x86_64-ebs' 'Name=state,Values=available' --output json | jq -r '.Images |   sort_by(.CreationDate) | last(.[]).ImageId')
echo "Latest ECS Optimized Amazon AMI_ID is $AMI_ID"

sed -i.bak -e "s#ECS_FARGATE_CLLUSTER_NAME#$ECS_FARGATE_CLLUSTER_NAME#g"  user-data.txt
sed -i.bak -e "s#%instanceProfile%#$IAM_INSTANT_PROFILE_ARN#g"  launch-template-data.json
sed -i.bak -e "s#%instanceSecurityGroup%#$SECURITY_GROUP#g"  launch-template-data.json
sed -i.bak -e "s#%workshopName%#$WORKSHOP_NAME#g"  launch-template-data.json
sed -i.bak  -e "s#%ami-id%#$AMI_ID#g" -e "s#%UserData%#$(cat user-data.txt | base64 --wrap=0)#g" launch-template-data.json


LAUCH_TEMPLATE_ID=$(aws ec2 create-launch-template --launch-template-name $LAUNCH_TEMPLATE_NAME --version-description $LAUNCH_TEMPLATE_VERSION --launch-template-data file://launch-template-data.json | jq -r '.LaunchTemplate.LaunchTemplateId')
#LAUCH_TEMPLATE_ID=lt-07fdb20138ddf466c
echo "Amazon LAUCH_TEMPLATE_ID is $LAUCH_TEMPLATE_ID"

ASG_NAME=$ASG_NAME_OD
OD_BASE=0
OD_PERCENTAGE=100
MIN_SIZE=0
MAX_SIZE=10
DESIREDS_SIZE=0
PUBLIC_SUBNET_LIST="subnet-764d7d11,subnet-a2c2fd8c,subnet-cb26e686,subnet-7acbf626,subnet-93d490ad,subnet-313ad03f"
INSTANCE_TYPE_1=c4.large
INSTANCE_TYPE_2=c5.large
INSTANCE_TYPE_3=m4.large
INSTANCE_TYPE_4=m5.large
INSTANCE_TYPE_5=r4.large
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
ASG_ARN=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name $ASG_NAME_OD | jq -r '.AutoScalingGroups[0].AutoScalingGroupARN')
echo "$ASG_NAME_OD ARN=$ASG_ARN"

TARGET_CAPACITY=100
CAPACITY_PROVIDER_NAME=$OD_CAPACITY_PROVIDER_NAME
sed -i.bak -e "s#%CAPACITY_PROVIDER_NAME%#$CAPACITY_PROVIDER_NAME#g"  ecs-capacityprovider.json
sed -i.bak -e "s#%ASG_ARN%#$ASG_ARN#g"  ecs-capacityprovider.json
sed -i.bak -e "s#%MAX_SIZE%#$MAX_SIZE#g"  ecs-capacityprovider.json
sed -i.bak -e "s#%TARGET_CAPACITY%#$TARGET_CAPACITY#g"  ecs-capacityprovider.json

CAPACITY_PROVIDER_ARN=$(aws ecs create-capacity-provider --cli-input-json file://ecs-capacityprovider.json | jq -r '.capacityProvider.capacityProviderArn')
echo "$OD_CAPACITY_PROVIDER_NAME ARN=$CAPACITY_PROVIDER_ARN"



