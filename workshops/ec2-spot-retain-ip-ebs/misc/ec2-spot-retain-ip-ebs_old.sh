#!/bin/bash 

echo "Hello World from EC2 Spot Team..."


yum update -y
yum -y install jq amazon-efs-utils


#Global Settings
EFS_FS_ID=fs-2b2540aa
EFS_MOUNT_POINT=/jp
SPOT_IP_STATUS_FILE=spot_ip_status.txt
SPOT_VOLUME_STATUS_FILE=spot_volume_status.txt
SPOT_STATE_FILE=spot_state.txt
SPOT_INSTANCE_STATUS_FILE=spot_instance_status.txt


#EBS Settings

EBS_TYPE=gp2
EBS_SIZE=8
EBS_DEV=/dev/xvdb

#SECONDARY_PRIVATE_IP="172.31.81.24"
MAC=$(curl -s http://169.254.169.254/latest/meta-data/mac)
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
AWS_AVAIALABILITY_ZONE=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.availabilityZone')
AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
INTERFACE_ID=$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/interface-id)
AMI_ID=$(curl -s http://169.254.169.254/latest/meta-data/ami-launch-index)


if [ $AMI_ID == "0" ]; then
    MY_NAME="MASTER"
else
    MY_NAME="SLAVE_"$AMI_ID
fi

echo "MY_NAME=$MY_NAME"

echo "MAC=$MAC"
echo "INSTANCE_ID=$INSTANCE_ID"
echo "INTERFACE_ID=$INTERFACE_ID"


mkdir -p $EFS_MOUNT_POINT
sudo mount -t efs -o tls $EFS_FS_ID:/ $EFS_MOUNT_POINT


if [ ! -f $EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE ]; then
    echo "File $EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE does not exist. Hence creating..."
    touch $EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE
fi

if [ ! -f $EFS_MOUNT_POINT/$SPOT_INSTANCE_STATUS_FILE ]; then
    echo "File $EFS_MOUNT_POINT/$SPOT_INSTANCE_STATUS_FILE does not exist. Hence creating..."
    touch $EFS_MOUNT_POINT/$SPOT_INSTANCE_STATUS_FILE
fi

if [ ! -f $EFS_MOUNT_POINT/$SPOT_VOLUME_STATUS_FILE ]; then
    echo "File $EFS_MOUNT_POINT/$SPOT_VOLUME_STATUS_FILE does not exist. Hence creating..."
    touch $EFS_MOUNT_POINT/$SPOT_VOLUME_STATUS_FILE
fi


VOLUME_IDS=$(aws ec2 describe-volumes --region $AWS_REGION  --filters Name=attachment.instance-id,Values=$INSTANCE_ID | jq -r '.Volumes[].VolumeId')

echo "VOLUME_IDS=$VOLUME_IDS"
volume_array=($VOLUME_IDS)
ROOT_VOLUME_ID="${volume_array[0]}"

echo "Numner of VolumeIds for the Instance Id $INSTANCE_ID are ${#volume_array[@]}"

VOLUME_IDS_STATUS="$(cat $EFS_MOUNT_POINT/$SPOT_VOLUME_STATUS_FILE)"
echo "Initial VOLUME_IDS_STATUS read from EFS is $VOLUME_IDS_STATUS"

function get_available_volume_or_ip()
{
    
    if [[ $1 == "IP" ]]; then
        input="$EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE"
    fi
    
    if [[ $1 == "VOLUME" ]]; then
        input="$EFS_MOUNT_POINT/$SPOT_VOLUME_STATUS_FILE"
    fi

    
    while IFS= read -r line
    do
      #echo "line=$line"
      
      fields=$(echo $line | tr "=" "\n")
      
      arr=($fields)
      if [[ "${arr[1]}" == "AVAILABLE" ]]; then
         echo "${arr[0]}"
         break
      fi
    done < "$input"
}


if [ "${#volume_array[@]}" == "1" ]; then
   echo "Instance $INSTANCE_ID contains only one volume i.e. root EBS Volume ${volume_array[0]}"
   SECONDARY_VOLUME_ID=$(get_available_volume_or_ip "VOLUME")
   echo "SECONDARY_VOLUME from EFS is $SECONDARY_VOLUME_ID"
   
   if [[ -z $SECONDARY_VOLUME_ID ]]; then
     echo "SECONDARY_VOLUME_ID is Empty. Looks like I am launching for the first time. Let me create a new volume and attach it to myself..."
     
     SECONDARY_VOLUME_ID=$(aws ec2 create-volume --volume-type $EBS_TYPE  --size $EBS_SIZE   --availability-zone $AWS_AVAIALABILITY_ZONE | jq -r '.VolumeId')
     echo "SECONDARY_VOLUME_ID=$SECONDARY_VOLUME_ID"
     aws ec2 wait volume-available  --volume-ids $SECONDARY_VOLUME_ID
        
     aws ec2 attach-volume --volume-id $SECONDARY_VOLUME_ID --instance-id $INSTANCE_ID --device $EBS_DEV
     sleep 15
     mkfs -t xfs $EBS_DEV

     echo "The root volume is $ROOT_VOLUME_ID Secondary volume is $SECONDARY_VOLUME_ID So storing this Secondary Volume to EFS..."
     echo "$SECONDARY_VOLUME_ID=IN_USE" >> $EFS_MOUNT_POINT/$SPOT_VOLUME_STATUS_FILE

  else
     echo "SECONDARY_VOLUME_ID $SECONDARY_VOLUME_ID  exists in EFS. So let me attach to this Volume and change volume status in EFS."
     sleep 10
     aws ec2 attach-volume --volume-id $SECONDARY_VOLUME_ID --instance-id $INSTANCE_ID --device $EBS_DEV
     sleep 15
     sed -i "s/$SECONDARY_VOLUME_ID=AVAILABLE/$SECONDARY_VOLUME_ID=IN_USE/g" $EFS_MOUNT_POINT/$SPOT_VOLUME_STATUS_FILE
  fi
else
   SECONDARY_VOLUME_ID="${volume_array[1]}"
   echo "Instance already contains two EBS ROOT_VOLUME_ID: $ROOT_VOLUME_ID and Secondary Volume: $SECONDARY_VOLUME_ID So storing Secondary Volume Id to EFS..."
   echo "$SECONDARY_VOLUME_ID=IN_USE" >> $EFS_MOUNT_POINT/$SPOT_VOLUME_STATUS_FILE
fi

SECONDARY_VOLUME_ID_STATUS="$(cat $EFS_MOUNT_POINT/$SPOT_VOLUME_STATUS_FILE)"
echo "Final SECONDARY_VOLUME_ID_STATUS stored into the EFS is $SECONDARY_VOLUME_ID_STATUS"


PRIVATE_IPS=$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/local-ipv4s)
echo "PRIVATE_IPS=$PRIVATE_IPS"
array=($PRIVATE_IPS)
PRIMARY_PRIVATE_IP="${array[0]}"
echo "Numner of Private IPs for the Instance Id are ${#array[@]}"


SECONDARY_PRIVATE_IPS_STATUS="$(cat $EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE)"
echo "Initial SECONDARY_PRIVATE_IPS_STATUS read from EFS is $SECONDARY_PRIVATE_IPS_STATUS"


if [ "${#array[@]}" == "1" ]; then
   echo "Instance $INSTANCE_ID contains only one IP i.e. Primary IP addr ${array[0]}"
   SECONDARY_PRIVATE_IP=$(get_available_volume_or_ip "IP")
   echo "SECONDARY_PRIVATE_IP from EFS is $SECONDARY_PRIVATE_IP"
   
   if [[ -z $SECONDARY_PRIVATE_IP ]]; then
     echo "SECONDARY_PRIVATE_IP is Empty. Looks like I am launching for the first time. Let me assign a secondary ip add to myself..."
     aws ec2 assign-private-ip-addresses --network-interface-id $INTERFACE_ID --secondary-private-ip-address-count 1
     service network restart
     sleep 10
     PRIVATE_IPS=$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/local-ipv4s)
     array=($PRIVATE_IPS)
     SECONDARY_PRIVATE_IP="${array[1]}"
     echo "The Primary IP is ${array[0]} Secondary IP is ${array[1]} So storing this Secondary Ip to EFS..."
     echo "$SECONDARY_PRIVATE_IP=IN_USE" >> $EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE
  else
     echo "SECONDARY_PRIVATE_IP $SECONDARY_PRIVATE_IP already exists in EFS. So let me assign this IP to myself and change status in EFS"
     sleep 45
     aws ec2 assign-private-ip-addresses --network-interface-id $INTERFACE_ID --private-ip-addresses $SECONDARY_PRIVATE_IP
     service network restart
     sed -i "s/$SECONDARY_PRIVATE_IP=AVAILABLE/$SECONDARY_PRIVATE_IP=IN_USE/g" $EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE
  fi
  
else
   SECONDARY_PRIVATE_IP="${array[1]}"
   echo "Instance already contains both Primary IP $PRIMARY_PRIVATE_IP and Secondary IP $SECONDARY_PRIVATE_IP So storing Secondary Ip to EFS..."
   echo "$SECONDARY_PRIVATE_IP=IN_USE" >> $EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE
fi

    SECONDARY_PRIVATE_IPS_STATUS="$(cat $EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE)"
    echo "Final SECONDARY_PRIVATE_IPS_STATUS stored into the EFS is $SECONDARY_PRIVATE_IPS_STATUS"
    
    mkdir -p /var/www/html/
    mount $EBS_DEV /var/www/
    
    yum -y install httpd
    service httpd start
    chkconfig httpd on

    echo "<html> <body> <h2>Time: $(date) Instance Id: $INSTANCE_ID PRIMARY_PRIVATE_IP: $PRIMARY_PRIVATE_IP SECONDARY_PRIVATE_IP: $SECONDARY_PRIVATE_IP ROOT_VOLUME_ID: $ROOT_VOLUME_ID SECONDARY_VOLUME_ID:$SECONDARY_VOLUME_ID</h2> </body> </html>" >> /var/www/html/index.html

     
cat <<EOF > /usr/local/bin/spot-instance-termination-notice-handler.sh
#!/bin/bash
while sleep 5; do

 INSTANCE_ID=\$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
 AWS_REGION=\$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
 
if [ -z \$(curl -Isf http://169.254.169.254/latest/meta-data/spot/termination-time)]; then
   echo "\$INSTANCE_ID is running fine at \$(date)" >> $EFS_MOUNT_POINT/$SPOT_INSTANCE_STATUS_FILE
   /bin/false
else
   echo "\$INSTANCE_ID is got spot interruption at \$(date)" >> $EFS_MOUNT_POINT/$SPOT_INSTANCE_STATUS_FILE
   
   MAC=\$(curl -s http://169.254.169.254/latest/meta-data/mac)
   PRIVATE_IPS=\$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/\$MAC/local-ipv4s)
   array=(\$PRIVATE_IPS)
   SECONDARY_PRIVATE_IP="\${array[1]}"
   sed -i "s/\$SECONDARY_PRIVATE_IP=IN_USE/\$SECONDARY_PRIVATE_IP=AVAILABLE/g" $EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE

   VOLUME_IDS=\$(aws ec2 describe-volumes --region \$AWS_REGION  --filters Name=attachment.instance-id,Values=\$INSTANCE_ID | jq -r '.Volumes[].VolumeId')
   volume_array=(\$VOLUME_IDS)
   SECONDARY_VOLUME_ID="\${volume_array[1]}"
 
   service httpd stop
   umount /var/www/
   yum -y removed httpd
   rm -rf /var/www/
   aws ec2 detach-volume --volume-id \$SECONDARY_VOLUME_ID
   sed -i "s/\$SECONDARY_VOLUME_ID=IN_USE/\$SECONDARY_VOLUME_ID=AVAILABLE/g" $EFS_MOUNT_POINT/$SPOT_VOLUME_STATUS_FILE
    
   umount $EFS_MOUNT_POINT
   rm -rf $EFS_MOUNT_POINT
   sleep 120
 
  
fi
done
EOF
chmod +x /usr/local/bin/spot-instance-termination-notice-handler.sh
/usr/local/bin/spot-instance-termination-notice-handler.sh &


