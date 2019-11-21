#!/bin/bash 

echo "Hello World from EC2 Spot Team..."
#Global Defaults
DEFAULT_REGION=us-east-1
#SECONDARY_PRIVATE_IP="172.31.81.24"
MAC=$(curl -s http://169.254.169.254/latest/meta-data/mac)
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
INTERFACE_ID=$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/interface-id)
echo "MAC=$MAC"
echo "INSTANCE_ID=$INSTANCE_ID"
echo "INTERFACE_ID=$INTERFACE_ID"
PRIVATE_IPS=$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/local-ipv4s)
AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
aws configure set default.region ${AWS_REGION}
echo "PRIVATE_IPS=$PRIVATE_IPS"
#IFS=$'\n' 
#read -r -a array <<< "$PRIVATE_IPS"
array=($PRIVATE_IPS)

mkdir -p /jp

#yum install -y amazon-efs-utils

sudo mount -t efs -o tls fs-2b2540aa:/ /jp
#echo "172.31.81.24" > /jp/spot_instance_status.txt
#echo "" > /jp/spot_instance_status.txt

echo "ls=$(ls /jp)"
SECONDARY_PRIVATE_IP="$(cat /jp/spot_instance_status.txt)"
echo "SECONDARY_PRIVATE_IP from EFS is $SECONDARY_PRIVATE_IP"


echo "Numner of Private IPs for the Instance Id are ${#array[@]}"

if [ "${#array[@]}" == "1" ]; then
   echo "Instance $INSTANCE_ID contains only one IP i.e. Primary IP addr ${array[0]}"
   
   if [[ -z $SECONDARY_PRIVATE_IP ]]; then
     echo "SECONDARY_PRIVATE_IP is Empty. Looks like I am launching for the first time. Let me assign a secondary ip add to myself..."
     aws ec2 assign-private-ip-addresses --network-interface-id $INTERFACE_ID --secondary-private-ip-address-count 1
     service network restart
     sleep 5
     PRIVATE_IPS=$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/local-ipv4s)
     array=($PRIVATE_IPS)
     echo "The Primary IP is ${array[0]} Secondary IP is ${array[1]} So storing this Secondary Ip to EFS..."
     SECONDARY_PRIVATE_IP="${array[1]}"
     echo $SECONDARY_PRIVATE_IP > /jp/spot_instance_status.txt
     SECONDARY_PRIVATE_IP="$(cat /jp/spot_instance_status.txt)"
     echo "SECONDARY_PRIVATE_IP stored into the EFS is $SECONDARY_PRIVATE_IP"
  else
     echo "SECONDARY_PRIVATE_IP $SECONDARY_PRIVATE_IP already exists in EFS. So let me assign this IP to myself."
     aws ec2 assign-private-ip-addresses --network-interface-id $INTERFACE_ID --private-ip-addresses $SECONDARY_PRIVATE_IP
     service network restart
  fi
  
else
   echo "Instance already contains both Primary IP ${array[0]} and Secondary IP ${array[1]} So storing Secondary Ip to EFS..."
   SECONDARY_PRIVATE_IP="${array[1]}"
   echo $SECONDARY_PRIVATE_IP > /jp/spot_instance_status.txt
   SECONDARY_PRIVATE_IP="$(cat /jp/spot_instance_status.txt)"
   echo "SECONDARY_PRIVATE_IP  stored into the EFS is $SECONDARY_PRIVATE_IP"

fi

