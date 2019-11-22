#!/bin/bash 

echo "Hello World from EC2 Spot Team..."


yum update -y
yum -y install jq amazon-efs-utils

#Global Settings
EFS_FS_ID=fs-2b2540aa
EFS_MOUNT_POINT=/jp
SPOT_IP_STATUS_FILE=spot_ip_status.txt
SPOT_VOLUME_STATUS_FILE=spot_volume_status.txt
SPOT_INSTANCE_STATUS_FILE=spot_instance_status.txt


#EBS Settings

EBS_TYPE=gp2
EBS_SIZE=8
EBS_DEV=/dev/xvdb

AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
MAC=$(curl -s http://169.254.169.254/latest/meta-data/mac)
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
INTERFACE_ID=$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/interface-id)
echo "MAC=$MAC"
echo "INSTANCE_ID=$INSTANCE_ID"
echo "INTERFACE_ID=$INTERFACE_ID"

sudo mount -t efs -o tls $EFS_FS_ID:/ $EFS_MOUNT_POINT


service httpd stop
umount /var/www/
rm -rf /var/www/
yum -y remove httpd

VOLUME_IDS=$(aws ec2 describe-volumes --region $AWS_REGION  --filters Name=attachment.instance-id,Values=$INSTANCE_ID | jq -r '.Volumes[].VolumeId')
volume_array=($VOLUME_IDS)
echo "VOLUME_IDS=$VOLUME_IDS  ${#volume_array[@]}"
if [ "${#volume_array[@]}" != "1" ]; then
   SECONDARY_VOLUME_ID="${volume_array[1]}"
   aws ec2 detach-volume --volume-id $SECONDARY_VOLUME_ID
   sed -i "s/\$SECONDARY_VOLUME_ID=IN_USE/\$SECONDARY_VOLUME_ID=AVAILABLE/g" \$EFS_MOUNT_POINT/\$SPOT_VOLUME_STATUS_FILE
fi

PRIVATE_IPS=$(curl -s http://169.254.169.254/latest/meta-data/network/interfaces/macs/$MAC/local-ipv4s)
array=($PRIVATE_IPS)

if [ "${#array[@]}" != "1" ]; then
   SECONDARY_PRIVATE_IP="${array[1]}"
   aws ec2 unassign-private-ip-addresses --network-interface-id $INTERFACE_ID --private-ip-addresses $SECONDARY_PRIVATE_IP
   sed -i "s/\$SECONDARY_PRIVATE_IP=IN_USE/\$SECONDARY_PRIVATE_IP=AVAILABLE/g" $EFS_MOUNT_POINT/$SPOT_IP_STATUS_FILE
fi





