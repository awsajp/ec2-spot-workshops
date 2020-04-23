#!/bin/bash 

echo "Creating the Infrastructure for ECS_Cluster_Auto_Scaling workshop ..."


yum update -y
yum -y install jq

export ACCOUNT_ID=$(aws sts get-caller-identity  --output text --query Account)
export AWS_REGION=$(curl -s  169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
echo "export  ACCOUNT_ID=${ACCOUNT_ID}" >> ~/.bash_profile
echo "export  AWS_REGION=${AWS_REGION}" >> ~/.bash_profile
aws configure set default.region ${AWS_REGION}
aws configure get default.region


aws ecs create-cluster \
--cluster-name EcsSpotWorkshopCluster \
--capacity-providers FARGATE FARGATE_SPOT \
--region $AWS_REGION \
--default-capacity-provider-strategy capacityProvider=FARGATE,base=1,weight=1 

#Create ECS Tasks for FARGATE Capacity Providers
aws ecs register-task-definition --cli-input-json file://webapp-fargate-task.json

#Get the list of public subnets created from Quick-Start-VPC
aws ec2 describe-subnets --filters "Name=tag:aws:cloudformation:stack-name,Values=Quick-Start-VPC" | jq -r '.Subnets[].SubnetId'
#subnet-07a877ee28959daa3
#subnet-015fc3e06f653980a
#subnet-003ef0ebc04c89b2d

# Assign the subnet list to a variable
export PUBLIC_SUBNET_LIST="subnet-07a877ee28959daa3,subnet-015fc3e06f653980a,subnet-003ef0ebc04c89b2d"

#Get the VPC Id for Quick-Start-VPC
export VPC_ID=$(aws ec2 describe-vpcs --filters "Name=tag:aws:cloudformation:stack-name,Values=Quick-Start-VPC" | jq -r '.Vpcs[0].VpcId')
echo "Quick Start VPC ID is $VPC_ID"

#Get the default Security Group created from the Quick-Start-VPC
export SECURITY_GROUP=$( aws ec2 describe-security-groups --filters "Name=vpc-id,Values=$VPC_ID" | jq -r '.SecurityGroups[0].GroupId')
echo "Default Security group is $SECURITY_GROUP"

# Deploy ECS Service only on the FARGATE Capacity Provider
aws ecs create-service \
     --capacity-provider-strategy capacityProvider=FARGATE,weight=1 \
     --cluster EcsSpotWorkshopCluster \
     --service-name webapp-fargate-service-fargate \
     --task-definition webapp-fargate-task:1 \
     --desired-count 2\
     --region us-east-2\
     --network-configuration "awsvpcConfiguration={subnets=[$PUBLIC_SUBNET_LIST],securityGroups=[$SECURITY_GROUP],assignPublicIp="ENABLED"}" 
          
# Deploy ECS Service only on the FARGATE_SPOT Capacity Provider
aws ecs create-service \
     --capacity-provider-strategy capacityProvider=FARGATE_SPOT,weight=1 \
     --cluster EcsSpotWorkshopCluster \
     --service-name webapp-fargate-service-fargate-spot \
     --task-definition webapp-fargate-task:1 \
     --desired-count 2 \
     --region us-east-2 \
     --network-configuration "awsvpcConfiguration={subnets=[$PUBLIC_SUBNET_LIST],securityGroups=[$SECURITY_GROUP],assignPublicIp="ENABLED"}" 
          
# Deploy ECS Service  on both FARGATE and FARGATE_SPOT Capacity Providers                   
aws ecs create-service \
     --capacity-provider-strategy capacityProvider=FARGATE,weight=3 capacityProvider=FARGATE_SPOT,weight=1 \
     --cluster EcsSpotWorkshopCluster \
     --service-name webapp-fargate-service-fargate-mix \
     --task-definition webapp-fargate-task:1  \
     --desired-count 4\
     --region us-east-2 \
     --network-configuration "awsvpcConfiguration={subnets=[$PUBLIC_SUBNET_LIST],securityGroups=[$SECURITY_GROUP],assignPublicIp="ENABLED"}" 
          
#Create an EC2 launch template          
cp templates/user-data.txt .
cp templates/launch-template-data.json .       
                              
# Go to AWS IAM console and copy the ARN for the instance-profile 
export IAM_INSTANT_PROFILE_ARN="arn:aws:iam::000474600478:instance-profile/ecslabinstanceprofile"
export AMI_ID=$(aws ssm get-parameters --names  /aws/service/ecs/optimized-ami/amazon-linux-2/recommended | jq -r 'last(.Parameters[]).Value' | jq -r '.image_id')
echo "Latest  ECS Optimized Amazon AMI_ID is $AMI_ID"


sed -i -e "s#%instanceProfile%#$IAM_INSTANT_PROFILE_ARN#g"  -e "s#%instanceSecurityGroup%#$SECURITY_GROUP#g"  -e "s#%ami-id%#$AMI_ID#g"  -e "s#%UserData%#$(cat user-data.txt |  base64 --wrap=0)#g" launch-template-data.json

LAUCH_TEMPLATE_ID=$(aws ec2 create-launch-template  --launch-template-name ecs-spot-workshop-lt  --version-description 1  --launch-template-data file://launch-template-data.json | jq -r '.LaunchTemplate.LaunchTemplateId')
echo "Amazon  LAUCH_TEMPLATE_ID is $LAUCH_TEMPLATE_ID"

aws ec2 describe-launch-template-versions  --launch-template-name ecs-spot-workshop-lt

#Creating an Auto Scaling Group (ASG) with EC2 On-Demand Instances
cp templates/asg.json .

export SERVICE_ROLE_ARN="arn:aws:iam::000474600478:role/aws-service-role/autoscaling.amazonaws.com/AWSServiceRoleForAutoScaling_ec2"
export ASG_NAME=ecs-spot-workshop-asg-od
export OD_PERCENTAGE=100 # Note that ASG will have 100% On-Demand, 0% Spot

sed -i -e "s#%ASG_NAME%#$ASG_NAME#g"   -e "s#%OD_PERCENTAGE%#$OD_PERCENTAGE#g"  -e "s#%PUBLIC_SUBNET_LIST%#$PUBLIC_SUBNET_LIST#g"  -e "s#%SERVICE_ROLE_ARN%#$SERVICE_ROLE_ARN#g"  asg.json

aws autoscaling  create-auto-scaling-group --cli-input-json file://asg.json
ASG_ARN=$(aws autoscaling  describe-auto-scaling-groups --auto-scaling-group-name $ASG_NAME| jq -r '.AutoScalingGroups[0].AutoScalingGroupARN')
echo "$ASG_NAME  ARN=$ASG_ARN"
 
#Creating a Capacity Provider using ASG with EC2 On-demand instances.
cp -Rfp templates/ecs-capacityprovider.json .

export CAPACITY_PROVIDER_NAME=od-capacity_provider
sed -i -e "s#%CAPACITY_PROVIDER_NAME%#$CAPACITY_PROVIDER_NAME#g"  -e "s#%ASG_ARN%#$ASG_ARN#g"  ecs-capacityprovider.json

CAPACITY_PROVIDER_ARN=$(aws ecs create-capacity-provider  --cli-input-json file://ecs-capacityprovider.json | jq -r '.capacityProvider.capacityProviderArn')
echo "$OD_CAPACITY_PROVIDER_NAME  ARN=$CAPACITY_PROVIDER_ARN"

#Creating an Auto Scaling Group (ASG) with EC2 Spot Instances
cp templates/asg.json .

export ASG_NAME=ecs-spot-workshop-asg-spot
export OD_PERCENTAGE=0 # Note that ASG will have 0% On-Demand, 100% Spot

sed -i -e "s#%ASG_NAME%#$ASG_NAME#g"   -e "s#%OD_PERCENTAGE%#$OD_PERCENTAGE#g"  -e "s#%PUBLIC_SUBNET_LIST%#$PUBLIC_SUBNET_LIST#g"  -e "s#%SERVICE_ROLE_ARN%#$SERVICE_ROLE_ARN#g"  asg.json
aws autoscaling create-auto-scaling-group --cli-input-json  file://asg.json
ASG_ARN=$(aws autoscaling  describe-auto-scaling-groups --auto-scaling-group-name $ASG_NAME | jq -r '.AutoScalingGroups[0].AutoScalingGroupARN')
echo "$ASG_NAME  ARN=$ASG_ARN"


#Creating a Capacity Provider using ASG with EC2 Spot instances.

cp -Rfp templates/ecs-capacityprovider.json .
export CAPACITY_PROVIDER_NAME=ec2spot-capacity_provider
sed -i -e "s#%CAPACITY_PROVIDER_NAME%#$CAPACITY_PROVIDER_NAME#g"  -e "s#%ASG_ARN%#$ASG_ARN#g"  ecs-capacityprovider.json


CAPACITY_PROVIDER_ARN=$(aws ecs create-capacity-provider  --cli-input-json file://ecs-capacityprovider.json | jq -r '.capacityProvider.capacityProviderArn')
echo "$SPOT_CAPACITY_PROVIDER_NAME  ARN=$CAPACITY_PROVIDER_ARN"


#Update ECS Cluster with Auto Scaling Capacity Providers
aws ecs put-cluster-capacity-providers   \
        --cluster EcsSpotWorkshopCluster  \
        --capacity-providers FARGATE FARGATE_SPOT od-capacity_provider ec2spot-capacity_provider  \
         --default-capacity-provider-strategy capacityProvider=od-capacity_provider,base=1,weight=1   \
         --region $AWS_REGION


#Create ECS Tasks for EC2 Capacity Providers
aws ecs register-task-definition --cli-input-json file://webapp-ec2-task.json

# Deploy ECS Service only on the EC2 On-demand autoscaling Capacity Provider
aws ecs create-service \
     --capacity-provider-strategy capacityProvider=od-capacity_provider,weight=1 \
     --cluster EcsSpotWorkshopCluster \
     --service-name webapp-ec2-service-od\
     --task-definition webapp-ec2-task:1 \
     --desired-count 2\
     --region $AWS_REGION

     
# Deploy ECS Service only on the EC2 Spot autoscaling Capacity Provider
aws ecs create-service \
     --capacity-provider-strategy capacityProvider=$SPOT_CAPACITY_PROVIDER_NAME,weight=1 \
     --cluster EcsSpotWorkshopCluster \
     --service-name webapp-ec2-service-spot \
     --task-definition webapp-ec2-task:1 \
     --desired-count 2 \
     --region $AWS_REGION 

# Deploy ECS Service  on both EC2 demand and Spot  autoscaling Capacity Providers
aws ecs create-service \
     --capacity-provider-strategy capacityProvider=webapp-ec2-service-od,weight=1 \
                                  capacityProvider=webapp-ec2-service-spot,weight=3 \
     --cluster EcsSpotWorkshopCluster \
     --service-name webapp-ec2-service-mix \
     --task-definition webapp-ec2-task:1 \
     --desired-count 6 \
     --region $AWS_REGION
     
     