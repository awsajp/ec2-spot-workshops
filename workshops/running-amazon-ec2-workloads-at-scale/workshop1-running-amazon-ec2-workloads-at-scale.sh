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
sed -i.bak -e "s#%$CFK_STACK_OP_KEY%#$CFK_STACK_OP_VALUE#g"  application-load-balancer.json
sed -i.bak -e "s#%$CFK_STACK_OP_KEY%#$CFK_STACK_OP_VALUE#g"  target-group.json
sed -i.bak -e "s#%$CFK_STACK_OP_KEY%#$CFK_STACK_OP_VALUE#g"  asg.json


done

#aws ec2 create-launch-template --launch-template-name runningAmazonEC2WorkloadsAtScale --version-description dev --launch-template-data file://launch-template-data.json

#LAUCH_TEMPLATE_ID=$(aws ec2 create-launch-template --launch-template-name $LAUNCH_TEMPLATE_NAME --version-description LAUNCH_TEMPLATE_VERSION --launch-template-data file://launch-template-data.json | jq -r '.LaunchTemplate.LaunchTemplateId')
#LAUCH_TEMPLATE_ID=lt-046437183d3b6bf53
#echo "Amazon LAUCH_TEMPLATE_ID is $LAUCH_TEMPLATE_ID"

#RDS_ID=$(aws rds create-db-instance --cli-input-json file://rds.json|jq -r '.DBInstance.DBInstanceIdentifier')
#echo "Amazon RDS_ID is $RDS_ID"

#aws rds wait  db-instance-available --db-instance-identifier $$RDS_ID


aws elbv2 create-load-balancer --cli-input-json file://application-load-balancer.json
alb_arn=$(aws elbv2 describe-load-balancers --names runningAmazonEC2WorkloadsAtScale --query LoadBalancers[].LoadBalancerArn --output text)
aws elbv2 create-target-group --cli-input-json file://target-group.json
tg_arn=$(aws elbv2 describe-target-groups --names runningAmazonEC2WorkloadsAtScale --query TargetGroups[].TargetGroupArn --output text)

sed -i.bak -e "s#%TargetGroupArn%#$tg_arn#g" modify-target-group.json
aws elbv2 modify-target-group-attributes --cli-input-json file://modify-target-group.json

sed -i.bak -e "s#%LoadBalancerArn%#$alb_arn#g" -e "s#%TargetGroupArn%#$tg_arn#g" listener.json

aws elbv2 create-listener --cli-input-json file://listener.json

aws autoscaling create-auto-scaling-group --cli-input-json file://asg.json