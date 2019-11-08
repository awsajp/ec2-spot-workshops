#!/bin/bash -x

echo "Hello World from EC2 Spot Team..."
#Global Defaults
DEFAULT_REGION=us-east-1
SLEEP=5
CFS_STACK_NAME=runningAmazonEC2WorkloadsAtScaleNew
CFS_STACK_FILE=running-amazon-ec2-workloads-at-scale.yaml


#CFS_STACK_ID=$(aws cloudformation create-stack --stack-name $CFS_STACK_NAME  --template-body file://$CFS_STACK_FILE --capabilities CAPABILITY_IAM --region $DEFAULT_REGION|jq -r '.StackId')
#echo "Created the stack $CFS_STACK_NAME with Stack Id $CFS_STACK_ID. Please wait till the status is COMPLETE"

aws cloudformation wait stack-create-complete --stack-name $CFS_STACK_NAME --no-paginate


#CFS_STACK_STATUS=$(aws cloudformation describe-stacks --stack-name $CFS_STACK_NAME | jq -r '.Stacks[].StackStatus')
#echo "Stack $CFS_STACK_NAME status is $CFS_STACK_STATUS"


#while [ $CFS_STACK_STATUS != "CREATE_COMPLETE" ]
#do
#   echo "Stack $CFS_STACK_NAME status is $CFS_STACK_STATUS. Sleeping for $SLEEP seconds..."
#   sleep $SLEEP
#done


CFS_STACK_OP_INSTANCEPROFILE_KEY=instanceProfile
CFS_STACK_OP_INSTANCEPROFILE_VALUE=$(aws cloudformation describe-stacks --stack-name $CFS_STACK_NAME | jq -r ".Stacks[].Outputs[]| select(.OutputKey==\"$CFS_STACK_OP_INSTANCEPROFILE_KEY\")|.OutputValue")

echo "CFS_STACK_OP_INSTANCEPROFILE_VALUE=$CFS_STACK_OP_INSTANCEPROFILE_VALUE"

