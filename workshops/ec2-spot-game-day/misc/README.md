# aws_ec2_spot
This repository contains all the code related to EC2 Spot

https://aws.amazon.com/blogs/machine-learning/train-deep-learning-models-on-gpus-using-amazon-ec2-spot-instances/

Shell commands

aws ec2 run-instances \
    --image-id ami-0027dfad6168539c7 \
    --security-group-ids <SECURITY_GROUP_ID> \
    --count 1 \
    --instance-type m4.xlarge \
    --key-name <KEYPAIR_NAME> \
    --subnet-id <SUBNET_ID> \
    --query "Instances[0].InstanceId"
    

aws ec2 create-volume \
    --size 100 \
    --region <AWS_REGION> \
    --availability-zone <INSTANCE_AZ> \
    --volume-type gp2 \
    --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=DL-datasets-checkpoints}]' 

aws ec2 attach-volume \
    --volume-id vol-<your_volume_id> \
    --instance-id i-<your_instance_id> \
    --device /dev/sdf
        
        
sudo mkdir /dltraining
sudo mkfs -t xfs /dev/xvdf
sudo mount /dev/xvdf /dltraining
sudo chown -R ubuntu: /dltraining/
cd /dltraining
mkdir datasets
mkdir checkpoints        


aws ec2 terminate-instances \
    --instance-ids i-<your_instance_id> \
    --output text
    

sudo mkdir -p /rootvolume/test1
sudo su
echo  "this is a test for root volume " > /rootvolume/test1/file1.txt


sudo mkdir /volume1
sudo mkfs -t xfs /dev/xvdb
sudo mount /dev/xvdb /volume1
sudo chown -R ec2-user: /volume1/
mkdir -p /volume1/test1
echo  "this is a test for volume1" > /volume1/test1/file1.txt


sudo mkdir /volume2
sudo mkfs -t xfs /dev/xvdc
sudo mount /dev/xvdc /volume2
sudo chown -R ec2-user: /volume2/
mkdir -p /volume2/test2
echo  "this is a test for volume2" > /volume2/test2/file2.txt


i-026bb75f4bdd1e53a

vol-07770c367e2baa282  root
ami-02dd77165c07f3843
vol-07a00fdd16a96dc3f vol1  snap-0fc8c2a86174ad86a

vol-06aa4fed8807d0fcb  vol2 snap-06c7304a47f9953f1



m = open("o", "r").read()



with open('o') as f:
  data = json.load(f)
print(data)
  
print(json.dumps(data, indent=2))

print(json.dumps(data['Instances'][0], indent=2))  



if new instance launched
  create 2 and 3 volumes
  
if spot interruption

   create snapshot from volume
   create an AMI for root from snapshot
   if same AZ
	   attach additiional volumes
   else
       create snapshots
	   create volume
	   attach
	   delete volume
	   
       
   create AMI takes time
   delete the volumes
   launch new AMI from this instance
   
import boto3
ec2client = boto3.client('ec2', region_name='us-east-1')
instanceId = 'i-02994c99e6a6c052c'
describeInstance = ec2client.describe_instances(InstanceIds=[instanceId])
print(json.dumps(describeInstance, indent=2, default=json_util.default))

       
periodic   
s1 s2 s3

create an AMI





print(json.dumps(m))
  '"Instances": [
    {
      "LaunchTemplateAndOverrides": {
        "LaunchTemplateSpecification": {
          "LaunchTemplateId": "lt-0e10e9c8156945055",
          "Version": "1"
        },
        "Overrides": {
          "InstanceType": "m4.large",
          "SubnetId": "subnet-01e89d5cc1b12f515",
          "WeightedCapacity": 1.0
        }
      },
      "Lifecycle": "spot",
      "InstanceIds": [
        "i-03af99d353d07c0a3"
      ],
      "InstanceType": "m4.large"
    }
  ]'
  
  
10.0.0.187

import base64

10.0.0.146

data = open("sample.txt", "r").read()
encoded = base64.b64encode(data)
message = "Python is fun"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)


base64_message = 'UHl0aG9uIGlzIGZ1bg=='


base64_bytes = x.encode('utf-8')
message_bytes = base64.b64decode(base64_bytes)
message = message_bytes.decode('utf-8')

print(message)
