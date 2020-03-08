#!/bin/bash 

echo "Creating the Infrastructure for ECS_Cluster_Auto_Scaling workshop ..."


yum update -y
yum -y install jq amazon-efs-utils


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
CFS_STACK_NAME=Quick-Start-VPC
CFS_STACK_FILE=aws-vpc.template

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

#aws s3 mb s3://emrtestjan26

#aws s3 ls s3://emrtestjp/results/
 
#CFS_STACK_ID=$(aws cloudformation create-stack --stack-name $CFS_STACK_NAME  --template-body file://$CFS_STACK_FILE --capabilities CAPABILITY_IAM --region $AWS_REGION|jq -r '.StackId')
#echo "Created the stack $CFS_STACK_NAME with Stack Id $CFS_STACK_ID. Please wait till the status is COMPLETE"

#aws cloudformation wait stack-create-complete --stack-name $CFS_STACK_NAME --no-paginate



#aws emr create-cluster --termination-protected --applications Name=Hadoop Name=Ganglia Name=Spark --tags 'Name=EMRTransient Cluuste' --ec2-attributes '{"KeyName":"awsajp_keypair","InstanceProfile":"EMR_EC2_DefaultRole","SubnetId":"subnet-cb26e686","EmrManagedSlaveSecurityGroup":"sg-0e09fda629dfe10e7","EmrManagedMasterSecurityGroup":"sg-0db19bdf51f475fa6"}' --release-label emr-5.29.0 --log-uri 's3n://aws-logs-000474600478-us-east-1/elasticmapreduce/' --steps '[{"Args":["spark-submit","--deploy-mode","cluster","--executor-memory","18G","--executor-cores","4","s3://emrtestjp/script.py","s3://emrtestjp/results1"],"Type":"CUSTOM_JAR","ActionOnFailure":"CONTINUE","Jar":"command-runner.jar","Properties":"","Name":"Spark application"}]' --instance-fleets '[{"InstanceFleetType":"MASTER","TargetOnDemandCapacity":1,"TargetSpotCapacity":0,"LaunchSpecifications":{"SpotSpecification":{"TimeoutDurationMinutes":60,"TimeoutAction":"TERMINATE_CLUSTER"}},"InstanceTypeConfigs":[{"WeightedCapacity":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":1}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"c4.large"},{"WeightedCapacity":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":1}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"m4.large"}],"Name":"Master - 1"},{"InstanceFleetType":"CORE","TargetOnDemandCapacity":4,"TargetSpotCapacity":0,"LaunchSpecifications":{"SpotSpecification":{"TimeoutDurationMinutes":60,"TimeoutAction":"TERMINATE_CLUSTER"}},"InstanceTypeConfigs":[{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5a.xlarge"},{"WeightedCapacity":4,"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5d.xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.xlarge"}],"Name":"Core - 2"},{"InstanceFleetType":"TASK","TargetOnDemandCapacity":40,"TargetSpotCapacity":0,"LaunchSpecifications":{"SpotSpecification":{"TimeoutDurationMinutes":60,"TimeoutAction":"TERMINATE_CLUSTER"}},"InstanceTypeConfigs":[{"WeightedCapacity":8,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":4}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.2xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.xlarge"},{"WeightedCapacity":8,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":4}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.2xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.xlarge"},{"WeightedCapacity":4,"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"i3.xlarge"}],"Name":"Task - 3"}]' --ebs-root-volume-size 10 --service-role EMR_DefaultRole --enable-debugging --name 'My cluster 2' --scale-down-behavior TERMINATE_AT_TASK_COMPLETION --region us-east-1

#aws emr create-cluster --termination-protected --applications Name=Hadoop Name=Spark Name=Ganglia --tags 'Name=EMR OD Cluster 1'  --release-label emr-5.29.0 --log-uri 's3n://aws-logs-000474600478-us-east-1/elasticmapreduce/'  --ec2-attributes '{"KeyName":"awsajp_keypair","InstanceProfile":"EMR_EC2_DefaultRole"}' --instance-fleets '[{"InstanceFleetType":"MASTER","TargetOnDemandCapacity":1,"TargetSpotCapacity":0,"InstanceTypeConfigs":[{"WeightedCapacity":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5a.xlarge"},{"WeightedCapacity":1,"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5d.xlarge"},{"WeightedCapacity":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.xlarge"},{"WeightedCapacity":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.xlarge"}],"Name":"Master - 1"},{"InstanceFleetType":"CORE","TargetOnDemandCapacity":4,"TargetSpotCapacity":4,"InstanceTypeConfigs":[{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5a.xlarge"},{"WeightedCapacity":4,"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5d.xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.xlarge"}],"Name":"Core - 2"},{"InstanceFleetType":"TASK","TargetOnDemandCapacity":0,"TargetSpotCapacity":40,"InstanceTypeConfigs":[{"WeightedCapacity":8,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":4}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.2xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.xlarge"},{"WeightedCapacity":8,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":4}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.2xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.xlarge"},{"WeightedCapacity":4,"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"i3.xlarge"}],"Name":"Task - 3"}]' --ebs-root-volume-size 10 --service-role EMR_DefaultRole --enable-debugging --name 'My cluster 4' --scale-down-behavior TERMINATE_AT_TASK_COMPLETION --region us-east-1

EMR_CLUSTER_TYPE=LONG_RUNNING

      if [[ $EMR_CLUSTER_TYPE == "LONG_RUNNING" ]]; then
            CLUSTER_NAME="EMR LONG RUNNING CLUSTER"
      elif [[ $EMR_CLUSTER_TYPE == "DATA_DRIVEN" ]]; then
            CLUSTER_NAME="EMR DATA DRIVEN CLUSTER"
      else
            CLUSTER_NAME="EMR TRANSIENT OR APP TEST CLUSTER"
      fi
      
      
EMR_CLUSTER_ID=j-1JPWSFJ830DN8
      
if [[ "1" == "2" ]]; then
EMR_CLUSTER_ID=$(aws emr create-cluster --termination-protected   \
  --applications Name=Hadoop Name=Spark Name=Ganglia \
  --tags 'Name=EMR OD Cluster 1'  --release-label emr-5.29.0 \
  --log-uri 's3n://aws-logs-000474600478-us-east-1/elasticmapreduce/'  \
  --ec2-attributes '{"KeyName":"awsajp_keypair","InstanceProfile":"EMR_EC2_DefaultRole"}' \
  --instance-fleets '[{"InstanceFleetType":"MASTER","TargetOnDemandCapacity":1,"TargetSpotCapacity":0,"InstanceTypeConfigs":[{"WeightedCapacity":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5a.xlarge"},{"WeightedCapacity":1,"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5d.xlarge"},{"WeightedCapacity":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.xlarge"},{"WeightedCapacity":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.xlarge"}],"Name":"Master - 1"},{"InstanceFleetType":"CORE","TargetOnDemandCapacity":4,"TargetSpotCapacity":4,"InstanceTypeConfigs":[{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5a.xlarge"},{"WeightedCapacity":4,"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5d.xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.xlarge"}],"Name":"Core - 2"},{"InstanceFleetType":"TASK","TargetOnDemandCapacity":0,"TargetSpotCapacity":40,"InstanceTypeConfigs":[{"WeightedCapacity":8,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":4}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.2xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.xlarge"},{"WeightedCapacity":8,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":4}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r4.2xlarge"},{"WeightedCapacity":4,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"r5.xlarge"},{"WeightedCapacity":4,"BidPriceAsPercentageOfOnDemandPrice":100,"InstanceType":"i3.xlarge"}],"Name":"Task - 3"}]'  \
  --ebs-root-volume-size 10 --service-role EMR_DefaultRole \
  --enable-debugging --name "$CLUSTER_NAME" \
  --scale-down-behavior TERMINATE_AT_TASK_COMPLETION --region us-east-1 | jq -r '.ClusterId')
  
echo "Created the EMR_CLUSTER_ID $EMR_CLUSTER_ID. Please wait till the status is RUNNING"



aws emr wait cluster-running --cluster-id $EMR_CLUSTER_ID

EMR_STEP_ID=$(aws emr add-steps --cluster-id $EMR_CLUSTER_ID \
--steps '[{"Args":["spark-submit","--deploy-mode","cluster","--executor-memory","18G","--executor-cores","4","s3://emrtestjp/script.py","s3://emrtestjp/results1/"],"Type":"CUSTOM_JAR","ActionOnFailure":"CONTINUE","Jar":"command-runner.jar","Properties":"","Name":"Spark application"}]'| jq -r '.StepIds[0]')
echo "Created the EMR_STEP_ID $EMR_STEP_ID. Please wait till the status is COMPLETED"


aws emr wait step-complete --cluster-id $EMR_CLUSTER_ID --step-id $EMR_STEP_ID

EMR_STEP_ID=$(aws emr add-steps --cluster-id $EMR_CLUSTER_ID \
--steps '[{"Args":["spark-submit","--deploy-mode","cluster","--executor-memory","18G","--executor-cores","4","s3://emrtestjp/script.py","s3://emrtestjp/results1/"],"Type":"CUSTOM_JAR","ActionOnFailure":"CONTINUE","Jar":"command-runner.jar","Properties":"","Name":"Spark application"}]'| jq -r '.StepIds[0]')
echo "Created the EMR_STEP_ID $EMR_STEP_ID. Please wait till the status is COMPLETED"

END=10

for i in $(seq 1 $END); do
    echo $i; 
    sleep 5
    STEP_STATUS=$(aws emr describe-step --cluster-id $EMR_CLUSTER_ID --step-id $EMR_STEP_ID | jq -r '.Step.Status.State')
    if [[ $STEP_STATUS == "RUNNING" ]]; then
        sleep 5
        INSTANCE_ID_LIST=$(aws emr list-instances --cluster-id $EMR_CLUSTER_ID --instance-fleet-type TASK --instance-states RUNNING | jq -r '.Instances[].Ec2InstanceId')
        echo "INSTANCE_ID_LIST=$INSTANCE_ID_LIST"
        Instance_id_array=($INSTANCE_ID_LIST)
        aws ec2 terminate-instances --instance-ids ${Instance_id_array[0]}
        aws ec2 terminate-instances --instance-ids ${Instance_id_array[1]}
        aws ec2 terminate-instances --instance-ids ${Instance_id_array[2]}
        
    fi
    
done

aws emr wait step-complete --cluster-id $EMR_CLUSTER_ID --step-id $EMR_STEP_ID

fi

EMR_STEP_ID=$(aws emr add-steps --cluster-id $EMR_CLUSTER_ID \
--steps '[{"Args":["spark-submit","--deploy-mode","cluster","--executor-memory","18G","--executor-cores","4","s3://emrtestjp/script.py","s3://emrtestjp/results1/"],"Type":"CUSTOM_JAR","ActionOnFailure":"CONTINUE","Jar":"command-runner.jar","Properties":"","Name":"Spark application"}]' | jq -r '.StepIds[0]')
echo "Created the EMR_STEP_ID $EMR_STEP_ID. Please wait till the status is COMPLETED"

END=10

for i in $(seq 1 $END); do
    sleep 5
    STEP_STATUS=$(aws emr describe-step --cluster-id $EMR_CLUSTER_ID --step-id $EMR_STEP_ID | jq -r '.Step.Status.State')

    if [[ $STEP_STATUS == "RUNNING" ]]; then
        sleep 5
        
        INSTANCE_ID_LIST=$(aws emr list-instances --cluster-id $EMR_CLUSTER_ID --instance-fleet-type TASK --instance-states RUNNING | jq -r '.Instances[].Ec2InstanceId')
        echo "INSTANCE_ID_LIST=$INSTANCE_ID_LIST"
        Instance_id_array=($INSTANCE_ID_LIST)
        num_of_instances=${#Instance_id_array[*]}
        num_of_instances=$(( num_of_instances/2 ))  
        for i in $(seq 0 $num_of_instances); do 
           aws ec2 terminate-instances --instance-ids ${Instance_id_array[i]}
        done
        
        X=$( aws emr list-instance-fleets --cluster-id j-1JPWSFJ830DN8 | jq -r '.InstanceFleets[]')
        INSTANCE_FLEET_TYPES=$(echo $X | jq -r '.InstanceFleetType')
        echo "INSTANCE_FLEET_TYPES=$INSTANCE_FLEET_TYPES"
        INSTANCE_FLEET_TYPES_ARRAY=($INSTANCE_FLEET_TYPES)
        
        INSTANCE_FLEET_IDS=$(echo $X | jq -r '.Id')
        echo "INSTANCE_FLEET_IDS=$INSTANCE_FLEET_IDS"
        INSTANCE_FLEET_IDS_ARRAY=($INSTANCE_FLEET_IDS)

        END=2
        
        for i in $(seq 1 $END); do
            echo $i; 
            if [[ "${INSTANCE_FLEET_TYPES_ARRAY[i]}" == "TASK" ]]; then
                TASK_FLEET_ID="${INSTANCE_FLEET_IDS_ARRAY[i]}"
            fi
        done
        echo "TASK_FLEET_ID=$TASK_FLEET_ID"
         
        aws emr modify-instance-fleet --cluster-id $EMR_CLUSTER_ID --instance-fleet InstanceFleetId=$TASK_FLEET_ID,TargetOnDemandCapacity=0,TargetSpotCapacity=20
    fi
    
done

aws emr wait step-complete --cluster-id $EMR_CLUSTER_ID --step-id $EMR_STEP_ID

aws emr modify-instance-fleet --cluster-id $EMR_CLUSTER_ID --instance-fleet InstanceFleetId=$TASK_FLEET_ID,TargetOnDemandCapacity=0,TargetSpotCapacity=40
