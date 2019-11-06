## 2-Launching-EC2-Spot-Instances
   
  This is a automated version of the EC2 Spot workshop Launching EC2 Spot Instances https://ec2spotworkshops.com/launching_ec2_spot_instances.html
  
   

## Deploy the cloud formation template to create the Infrastructure Infra 

Please find the CF yaml at  https://ec2spotworkshops.com/launching_ec2_spot_instances.html

### Create the Launch Template Instances 

aws ec2 create-launch-template --region $DEFAULT_REGION --launch-template-name $LAUNCH_TEMPLATE_NAME --version-description LAUNCH_TEMPLATE_VERSION --launch-template-data "{\"NetworkInterfaces\":[{\"DeviceIndex\":0,\"SubnetId\":\"$DEFAULT_SUBNET\"}],\"ImageId\":\"$AMI_ID\",\"InstanceType\":\"$INSTANCE_TYPE\",\"TagSpecifications\":[{\"ResourceType\":\"instance\",\"Tags\":[{\"Key\":\"Name\",\"Value\":\"$LAUNCH_TEMPLATE_NAME\"}]}]}" | jq -r '.LaunchTemplate.LaunchTemplateId'



### Create the Spot Instances using Auto scaling Group

aws autoscaling create-auto-scaling-group --cli-input-json file://$ASG_TEMPLATE_TEMP_FILE

### Create the Spot Instances using Run Instances API

aws ec2 run-instances --launch-template LaunchTemplateName=$LAUNCH_TEMPLATE_NAME,Version=$LAUNCH_TEMPLATE_VERSION --instance-market-options MarketType=spot
 
 
### Create the Spot Instances using Spot Fleet using Instance Specifications

 aws ec2 request-spot-fleet --spot-fleet-request-config file://$SPOTFLEET_TEMPLATE_INSTANCESPECS_TEMP_FILE|jq -r '.SpotFleetRequestId'

### Create the Spot Instances using Spot Fleet using the Launch Template

aws ec2 request-spot-fleet --spot-fleet-request-config file://$SPOTFLEET_TEMPLATE_LAUNCHTEMPLATE_TEMP_FILE|jq -r '.SpotFleetRequestId'


### Workshop Cleanup


