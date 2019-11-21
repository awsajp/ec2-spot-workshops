#!/bin/bash 

yum -y install jq amazon-efs-utils

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
SPOT_IP_STATUS_FILE=spot_ip_status.txt
SPOT_INSTANCE_STATUS_FILE=spot_instance_status.txt

if [ ! -f /jp/$SPOT_IP_STATUS_FILE ]; then
    echo "File /jp/$SPOT_IP_STATUS_FILE does not exist. Hence creating..."
    touch /jp/$SPOT_IP_STATUS_FILE
fi

if [ ! -f /jp/$SPOT_INSTANCE_STATUS_FILE ]; then
    echo "File /jp/$SPOT_INSTANCE_STATUS_FILE does not exist. Hence creating..."
    touch /jp/$SPOT_INSTANCE_STATUS_FILE
fi


sudo mount -t efs -o tls fs-2b2540aa:/ /jp

function get_available_secondary_ip()
{
  
    input="/jp/$SPOT_IP_STATUS_FILE"
    while IFS= read -r line
    do
      #echo "line=$line"
      
      mails=$(echo $line | tr "=" "\n")
      arr=($mails)
      if [[ "${arr[1]}" == "AVAILABLE" ]]; then
         echo "${arr[0]}"
         break
      fi
    
      #for addr in $mails
      #do
       #   echo "addr=$addr"
      #done
    
    done < "$input"
}

#SECONDARY_PRIVATE_IP=$(get_available_secondary_ip)   # or result=`myfunc`
#echo "result=$SECONDARY_PRIVATE_IP"

#sed -i "s/$SECONDARY_PRIVATE_IP=AVAILABLE/$SECONDARY_PRIVATE_IP=IN_USE/g" /jp/$SPOT_IP_STATUS_FILE

#echo "172.31.81.24" > /jp/$SPOT_IP_STATUS_FILE
#echo "" > /jp/$SPOT_IP_STATUS_FILE


#echo "ls=$(ls /jp)"
SECONDARY_PRIVATE_IPS_STATUS="$(cat /jp/$SPOT_IP_STATUS_FILE)"
echo "SECONDARY_PRIVATE_IPS_STATUS stored into the EFS is $SECONDARY_PRIVATE_IPS_STATUS"

echo "Numner of Private IPs for the Instance Id are ${#array[@]}"

if [ "${#array[@]}" == "1" ]; then
   echo "Instance $INSTANCE_ID contains only one IP i.e. Primary IP addr ${array[0]}"
   SECONDARY_PRIVATE_IP=$(get_available_secondary_ip)
   echo "SECONDARY_PRIVATE_IP from EFS is $SECONDARY_PRIVATE_IP"
   
   if [[ -z $SECONDARY_PRIVATE_IP ]]; then
     echo "SECONDARY_PRIVATE_IP is Empty. Looks like I am launching for the first time. Let me assign a secondary ip add to myself..."
     aws ec2 assign-private-ip-addresses --network-interface-id $INTERFACE_ID --secondary-private-ip-address-count 1
     service network restart
     sleep 5
     PRIVATE_IPS=$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/local-ipv4s)
     array=($PRIVATE_IPS)
     SECONDARY_PRIVATE_IP="${array[1]}"
     echo "The Primary IP is ${array[0]} Secondary IP is ${array[1]} So storing this Secondary Ip to EFS..."
     echo "$SECONDARY_PRIVATE_IP=IN_USE" >> /jp/$SPOT_IP_STATUS_FILE
     
     SECONDARY_PRIVATE_IPS_STATUS="$(cat /jp/$SPOT_IP_STATUS_FILE)"
     echo "SECONDARY_PRIVATE_IPS_STATUS stored into the EFS is $SECONDARY_PRIVATE_IPS_STATUS"
  else
     echo "SECONDARY_PRIVATE_IP $SECONDARY_PRIVATE_IP already exists in EFS. So let me assign this IP to myself."
     aws ec2 assign-private-ip-addresses --network-interface-id $INTERFACE_ID --private-ip-addresses $SECONDARY_PRIVATE_IP
     service network restart
     sed -i "s/$SECONDARY_PRIVATE_IP=AVAILABLE/$SECONDARY_PRIVATE_IP=IN_USE/g" /jp/$SPOT_IP_STATUS_FILE
     SECONDARY_PRIVATE_IPS_STATUS="$(cat /jp/$SPOT_IP_STATUS_FILE)"
     echo "SECONDARY_PRIVATE_IPS_STATUS stored into the EFS is $SECONDARY_PRIVATE_IPS_STATUS"
     
  fi
  
else
   echo "Instance already contains both Primary IP ${array[0]} and Secondary IP ${array[1]} So storing Secondary Ip to EFS..."
   SECONDARY_PRIVATE_IP="${array[1]}"
   echo "$SECONDARY_PRIVATE_IP=IN_USE" >> /jp/$SPOT_IP_STATUS_FILE
   SECONDARY_PRIVATE_IPS_STATUS="$(cat /jp/$SPOT_IP_STATUS_FILE)"
   echo "SECONDARY_PRIVATE_IPS_STATUS stored into the EFS is $SECONDARY_PRIVATE_IPS_STATUS"

fi


cat <<EOF > /usr/local/bin/spot-instance-termination-notice-handler.sh
#!/bin/bash
while sleep 5; do
 INSTANCE_ID=\$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
if [ -z \$(curl -Isf http://169.254.169.254/latest/meta-data/spot/termination-time)]; then
   echo "\$INSTANCE_ID is running fine at \$(date)" >> /jp/$SPOT_INSTANCE_STATUS_FILE
   /bin/false
else
   echo "\$INSTANCE_ID is got spot interruption at \$(date)" >> /jp/$SPOT_INSTANCE_STATUS_FILE
   MAC=\$(curl -s http://169.254.169.254/latest/meta-data/mac)
   PRIVATE_IPS=\$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/\$MAC/local-ipv4s)
   array=(\$PRIVATE_IPS)
   SECONDARY_PRIVATE_IP="\${array[1]}"
   sed -i "s/\$SECONDARY_PRIVATE_IP=IN_USE/\$SECONDARY_PRIVATE_IP=AVAILABLE/g" /jp/$SPOT_IP_STATUS_FILE
   SECONDARY_PRIVATE_IPS_STATUS="\$(cat /jp/$SPOT_IP_STATUS_FILE)"
   echo "SECONDARY_PRIVATE_IPS_STATUS stored into the EFS is \$SECONDARY_PRIVATE_IPS_STATUS"
   
fi
done
EOF
chmod +x /usr/local/bin/spot-instance-termination-notice-handler.sh
/usr/local/bin/spot-instance-termination-notice-handler.sh &



