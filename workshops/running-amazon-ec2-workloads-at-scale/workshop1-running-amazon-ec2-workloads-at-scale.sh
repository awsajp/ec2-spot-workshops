#!/bin/bash -x

echo "Hello World from EC2 Spot Team..."
#Global Defaults
DEFAULT_REGION=us-east-1
SLEEP=5
LAUNCH_TEMPLATE_NAME=runningAmazonEC2WorkloadsAtScaleNew_lt
LAUNCH_TEMPLATE_VERSION=1
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

CFS_STACK_OP_CODEDEPLOYSERVICEROLE_KEY=codeDeployServiceRole
CFS_STACK_OP_CODEDEPLOYSERVICEROLE_VALUE=$(aws cloudformation describe-stacks --stack-name $CFS_STACK_NAME | jq -r ".Stacks[].Outputs[]| select(.OutputKey==\"$CFS_STACK_OP_CODEDEPLOYSERVICEROLE_KEY\")|.OutputValue")
echo "CFS_STACK_OP_CODEDEPLOYSERVICEROLE_VALUE=$CFS_STACK_OP_CODEDEPLOYSERVICEROLE_VALUE"


#CFS_STACK_OP_SNSTOPIC_KEY=snsTopic
#CFS_STACK_OP_SNSTOPIC_VALUE=$(aws cloudformation describe-stacks --stack-name $CFS_STACK_NAME | jq -r ".Stacks[].Outputs[]| select(.OutputKey==\"$CFS_STACK_OP_CODEDEPLOYSERVICEROLE_KEY\")|.OutputValue")
#echo "CFS_STACK_OP_CODEDEPLOYSERVICEROLE_VALUE=$CFS_STACK_OP_CODEDEPLOYSERVICEROLE_VALUE"

export AMI_ID=$(aws ec2 describe-images --owners amazon --filters 'Name=name,Values=amzn2-ami-hvm-2.0.????????-x86_64-gp2' 'Name=state,Values=available' --output json | jq -r '.Images |   sort_by(.CreationDate) | last(.[]).ImageId')
echo "Amazon AMI_ID is $AMI_ID"
sed -i "s/%ami-id%/$AMI_ID/g" launch-template-data.json
sed -i "s/%UserData%/$(cat user-data.txt | base64 --wrap=0)/g" launch-template-data.json



declare -a CFK_STACK_OP_KEYS_LIST=("instanceProfile"  "codeDeployServiceRole" "snsTopic" 
                                    "cloud9Environment" "fileSystem" "eventRule" 
                                    "lambdaFunction" "codeDeployBucket" "dbSubnetGroup"
                                    "instanceSecurityGroup" "dbSecurityGroup" "loadBalancerSecurityGroup"
                                    "publicSubnet2" "publicSubnet1" "awsRegionId" "vpc" )

for CFK_STACK_OP_KEY in "${CFK_STACK_OP_KEYS_LIST[@]}"; do
#echo "CFK_STACK_OP_KEY=$CFK_STACK_OP_KEY"
CFK_STACK_OP_VALUE=$(aws cloudformation describe-stacks --stack-name $CFS_STACK_NAME | jq -r ".Stacks[].Outputs[]| select(.OutputKey==\"$CFK_STACK_OP_KEY\")|.OutputValue")
echo "$CFK_STACK_OP_KEY=$CFK_STACK_OP_VALUE"
#sed -i "s/%$CFK_STACK_OP_KEY%/$CFK_STACK_OP_VALUE/g" user-data.txt
#sed -i "s/%$CFK_STACK_OP_KEY%/$CFK_STACK_OP_VALUE/g" launch-template-data.json
sed -i.bak -e "s#%$CFK_STACK_OP_KEY%#$CFK_STACK_OP_VALUE#g"  user-data.txt
sed -i.bak -e "s#%$CFK_STACK_OP_KEY%#$CFK_STACK_OP_VALUE#g"  launch-template-data.json
sed -i.bak -e "s#%$CFK_STACK_OP_KEY%#$CFK_STACK_OP_VALUE#g"  rds.json


done

#aws ec2 create-launch-template --launch-template-name runningAmazonEC2WorkloadsAtScale --version-description dev --launch-template-data file://launch-template-data.json

#LAUCH_TEMPLATE_ID=$(aws ec2 create-launch-template --launch-template-name $LAUNCH_TEMPLATE_NAME --version-description LAUNCH_TEMPLATE_VERSION --launch-template-data file://launch-template-data.json | jq -r '.LaunchTemplate.LaunchTemplateId')
#LAUCH_TEMPLATE_ID=lt-046437183d3b6bf53
#echo "Amazon LAUCH_TEMPLATE_ID is $LAUCH_TEMPLATE_ID"

RDS_ID=$(aws rds create-db-instance --cli-input-json file://rds.json)
echo "Amazon RDS_ID is $RDS_ID"

