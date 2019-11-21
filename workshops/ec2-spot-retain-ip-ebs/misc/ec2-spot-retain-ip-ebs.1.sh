#!/bin/bash 

echo "Hello World from EC2 Spot Team..."
#Global Defaults
DEFAULT_REGION=us-east-1
SECONDARY_PRIVATE_IP=""
MAC=$(curl http://169.254.169.254/latest/meta-data/mac)
echo "MAC=$MAC"
PRIVATE_IPS=$(curl http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/local-ipv4s)
echo "PRIVATE_IPS=$PRIVATE_IPS"
#IFS=$'\n' 
#read -r -a array <<< "$PRIVATE_IPS"
array=($PRIVATE_IPS)

echo "Numner of Private IPs for the Instance Id are ${#array[@]}"

if [ "${#array[@]}" == "1" ]; then
   echo "Instance contains only one IP i.e. Primary IP addr ${array[0]}"
else
   echo "Instance contains both Primary IP ${array[0]} and Secondary IP ${array[1]}"
   SECONDARY_PRIVATE_IP="${array[1]}"
   echo "SECONDARY_PRIVATE_IP=$SECONDARY_PRIVATE_IP"
fi


echo "${array[0]}"
echo "${array[1]}"

for index in "${!array[@]}"
do
    echo "$index ${array[index]}"
done


#for IP in "${PRIVATE_IPS[@]}"; do
#echo "IP=$IP"
#done
