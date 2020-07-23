### Stateful Workloads on EC2 Spot

#### Step1:  Create S3 Bucket and upload the lambda_function.zip file to the S3 Bucket and use it during the CFN creation
zip lambda_function.zip lambda_function.py cfnresponse.py

#### Step2 :  Create the Cloud Formation Stack using ec2-spot-stateful-ec2fleet.yaml
 It creates the following resources
 
 ##### VPC with 3 public and 3 private subnets
 ##### Application Load Balance and Target Group
 ##### EC2 Launch Template bootstrapping a pythn flask based web app
 ##### EC2 Fleet with 4 instances (2 on-demand and 2 spot instances)
 ##### Dynamo DB Table
 ##### Lambda function to provision initial instances and also for restoring the state/EBS volumes
 ##### Cloud Watch event to handle node termination
 
  ![Alt text](EC2 Spot for Stateful Workloads.png?raw=true "Diagram")
  
  The solution provides the following features
  ##### EC2 Fleet API with Spot best practices
  ##### configure Spot Instance diversification via CFN Template
  ##### configure Total, spot and on-demand target capacity via CFN Template
  ##### Enable/Disable Retain of Private IP via CFN Template. That means replacement spot can be launched either in same or different AZ
  ##### Configure Root EBS, Additional Volume1 and Additional Volume2 sizes via CFN template
  ##### Simple Python Flask based Web app showing the state of 3 EBS volumes 
  ##### Application Load Balancer to access the Web Application
  ##### Configure Root EBS, Additional Volume1 and Additional Volume2 sizes via CFN template
  
  
 
  
  
#### Step3 :  Check out all the resources created by CFN Stack

#### Step4 :  Run the ALB DNS Name in the browser to check if the web application is up and running

#### Step5 :  Test the workshop by terminating one of the 4 instances created by the CFN

#### Step6 :  Run the ALB DNS Name in the browser again to check if 3 EBS Volumes are restored back in the replacement spot instance
