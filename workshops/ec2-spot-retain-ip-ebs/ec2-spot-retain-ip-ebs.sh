#!/bin/bash 

echo "Hello World from EC2 Spot Team..."
#Global Defaults
DEFAULT_REGION=us-east-1
SECONDARY_PRIVATE_IP="172.31.81.24"
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

echo "Numner of Private IPs for the Instance Id are ${#array[@]}"

if [ "${#array[@]}" == "1" ]; then
   echo "Instance contains only one IP i.e. Primary IP addr ${array[0]}"
   aws ec2 assign-private-ip-addresses --network-interface-id $INTERFACE_ID --private-ip-addresses $SECONDARY_PRIVATE_IP
   
else
   echo "Instance contains both Primary IP ${array[0]} and Secondary IP ${array[1]}"
   SECONDARY_PRIVATE_IP="${array[1]}"
   echo "SECONDARY_PRIVATE_IP=$SECONDARY_PRIVATE_IP"
fi

