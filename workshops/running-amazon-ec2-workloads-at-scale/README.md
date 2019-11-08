## EC2 Spot Workshop #1 : running-amazon-ec2-workloads-at-scale

In this workshop, you will deploy the following:

    An AWS CloudFormation stack, which will include:
        An Amazon Virtual Private Cloud (Amazon VPC) with subnets in two Availability Zones
        An AWS Cloud9 environment
        Supporting IAM policies and roles
        Supporting security groups
        An Amazon EFS file system
        An Amazon S3 bucket to use with AWS CodeDeploy
    An Amazon RDS database instance
    An Amazon EC2 launch template
    An Application Load Balancer (ALB) with a listener and target group
    An Amazon EC2 Auto Scaling group, with:
        A scheduled scaling action
        A dynamic scaling policy
    An AWS CodeDeploy application deployment
    An AWS Systems Manager run command to emulate load on the service



  This is a automated version of the EC2 Spot workshop Launching EC2 Spot Instances https://ec2spotworkshops.com/launching_ec2_spot_instances.html
  
   

### Step1 :  Deploy the cloud formation template to create the Infrastructure  

aws cloudformation create-stack --stack-name $CFS_STACK_NAME  --template-body file://$CFS_STACK_FILE --capabilities CAPABILITY_IAM --region $DEFAULT_REGION|jq -r '.StackId'

### Step2 : Create an Amazon RDS database instance
aws rds create-db-instance --cli-input-json file://rds.json|jq -r '.DBInstance.DBInstanceIdentifier'

### Step3 : Create the Launch Template Instances 

aws ec2 create-launch-template --launch-template-name $LAUNCH_TEMPLATE_NAME --version-description LAUNCH_TEMPLATE_VERSION --launch-template-data file://launch-template-data.json | jq -r '.LaunchTemplate.LaunchTemplateId'

### Step4 : Create the Application Load Balancer and Target Group

aws elbv2 create-load-balancer --cli-input-json file://application-load-balancer.json
aws elbv2 create-target-group --cli-input-json file://target-group.json

### Step5 : Create the Auto Scaling Group
aws autoscaling create-auto-scaling-group --cli-input-json file://asg.json

### Step6 : An AWS CodeDeploy application deployment

git clone https://github.com/phanan/koel.git
    
cd koel && git checkout v3.7.2
cp -avr ../codedeploy/* .
aws deploy create-application --application-name koelApp

aws deploy push --application-name koelApp --s3-location s3://$code_deploy_bucket/koelApp.zip --no-ignore-hidden-files
cd ..
aws deploy create-deployment-group --cli-input-json file://deployment-group.json
aws deploy create-deployment --cli-input-json file://deployment.json

### Step7 : Run AWS Systems Manager run command to emulate load on the service
aws ssm send-command --cli-input-json file://ssm-stress.json


### Workshop Cleanup
Delete all the resources created above. This section is TBD
