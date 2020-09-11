### Stateful Workloads on EC2 Spot

#### Step1:  Create S3 Bucket and upload the lambda_function.zip file to the S3 Bucket and use it during the CFN creation
 zip lambda_function.zip lambda_function.py cfnresponse.py user-data.txt

#### Step2 :  Deploy the Solution using the CFN stack ec2-spot-stateful-ec2fleet.yaml
The solution works in 2 modes.  1). Use an Existing Cluster   2) Create a new Cluster from the scratch
##### Step2a :  Common Cluster Configuration
 This is a common configuration needed for both options

          - UseExistingCluster
          - RetainPrivateIP
          - ClusterInstanceTag
          - NumberOfEBSVolumes
          - EBSVolumeDeviceNames
          - EBSVolumeDeviceSizes
          - EBSVolumeMountPaths
          - KeyPairName
          - InstanceTypes
          - NodeServiceStartCommand
          
CFN stack creates the following both modes
          
 ###### Dynamo DB Table
 ###### Lambda function to provision initial instances and also for restoring the state/EBS volumes
 ###### Cloud Watch event to handle node termination          

##### Step2b :  Existing Cluster Configuration
This is needed if UseExistingCluster==YES

          - ExistingVPCId
          - ExistingSubnetIdsList
          - ExistingLaunchTemplateId
          - ExistingLaunchTemplateVersion
          - ExistingInstanceProfile
 
##### Step2c :  New Cluster (Simple Python Web App) ) Configuration
This is needed if UseExistingCluster==NO
          
          - RootEBSAMIId
          - BaseInstanceType
          - sourceCidr
          - TotalTargetCapacity
          - OnDemandTargetCapacity
          - SpotTargetCapacity       
             
In this mode the CFN stack creates the following resources
 
 ###### VPC with 2 public and 2 private subnets
 ###### Application Load Balance and Target Group
 ###### EC2 Launch Template bootstrapping a python flask based web app
 ###### EC2 Fleet with 2 instances (1 on-demand and 1 spot instances)

 
  ![Alt text](diagram.png?raw=true "Diagram")
  
  The solution provides the following features
  ###### EC2 Fleet API with Spot best practices
  ###### configure Spot Instance diversification via CFN Template
  ###### configure Total, spot and on-demand target capacity via CFN Template
  ###### Enable/Disable Retain of Private IP via CFN Template. That means replacement spot can be launched either in same or different AZ
  ###### Configure Root EBS, Additional Volume1 and Additional Volume2 sizes via CFN template
  ###### Simple Python Flask based Web app showing the state of 3 EBS volumes 
  ###### Application Load Balancer to access the Web Application
  ###### Configure Root EBS, Additional Volume1 and Additional Volume2 sizes via CFN template
  
 
#### Step3 :  Check out all the resources created by CFN Stack and ensure that DynamoDB is updated with all the state

#### Step4 :  Terminate one of the EC2 Instances and see that replacement comes back
