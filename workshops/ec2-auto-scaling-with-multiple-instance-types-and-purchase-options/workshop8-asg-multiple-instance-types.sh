#!/bin/bash +x

echo "Hello World from EC2 Spot Team..."
#Global Defaults
REGION=us-east-1

#Workshop8 asg-multiple-instance-types Configurations settings

CF_STACK_FILE=ec2-auto-scaling-with-multiple-instance-types-and-purchase-options.yaml
CF_STACK_NAME=CFS-8-ASG-InstanceTypesDiverse-Spot-OD

aws cloudformation create-stack --stack-name $CF_STACK_NAME --template-body file://$CF_STACK_FILE --capabilities CAPABILITY_IAM --region $REGION

