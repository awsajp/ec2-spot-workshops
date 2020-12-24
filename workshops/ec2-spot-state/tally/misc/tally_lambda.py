
from botocore.exceptions import ClientError
import logging, os
import boto3
from boto3.dynamodb.conditions import Key
import os
import json
import decimal
import time
from random import seed
from random import random
import threading



logger = logging.getLogger()
logger.setLevel(logging.INFO)

customerTableName=os.getenv('DYNAMODB_TABLE_NAME')
statusIndexName=os.getenv('DYNAMODB_GSI_NAME')
instanceIndexName=os.getenv('DYNAMODB_INSTANCE_INDEX')
clusterName = os.getenv('ECS_CLUSTER')


# API Clients
ec2client = boto3.client('ec2')
asgclient = boto3.client('autoscaling')
ssmclient = boto3.client('ssm')
dbclient = boto3.client('dynamodb')
dynamodbresource = boto3.resource('dynamodb')
ecsclient = boto3.client('ecs')
dynamodbTable = dynamodbresource.Table(customerTableName)




def get_asg_name(instance_id):
  # Describe tags for the instance that will be interrupted
  try:
    describe_tags_response = ec2client.describe_instances(InstanceIds=[instance_id])
    instance_tags = describe_tags_response['Reservations'][0]['Instances'][0]['Tags']
  except ClientError as e:
    error_message = "Unable to describe tags for instance id: {id}. ".format(id=instance_id)
    logger.error( error_message + e.response['Error']['Message'])
    # Instance does not exist or cannot be described
    raise e

  interruption_handling_properties = {
    'controller-type': '',
    'controller-id': '',
    'managed': False }

  for tag in instance_tags:
    if tag['Key'] == 'aws:autoscaling:groupName':
      asg_name = tag['Value']
      return asg_name

  return "no_asg_found"

def detach_instance_from_asg(instance_id):
  try:
    # detach instance from ASG and launch replacement instance
    as_group_name=get_asg_name(instance_id)
    response = asgclient.detach_instances(
      InstanceIds=[instance_id],
      AutoScalingGroupName=as_group_name,
      ShouldDecrementDesiredCapacity=False)
    logger.info(response['Activities'][0]['Cause'])
  except ClientError as e:
    error_message = "Unable to detach instance {id} from AutoScaling Group {asg_name}. ".format(
      id=instance_id,asg_name=as_group_name)
    logger.error( error_message + e.response['Error']['Message'])
    raise e

def handler(event, context):


  print("event={}".format(event))
  exit()

  if event['detail-type'] == "EC2 Instance-terminate Lifecycle Action":
    instance_id = event['detail']['EC2InstanceId']
    logger.info("Handling EC2 Instance-terminate Lifecycle Action for instance {id}. Sleeping for 300 sec".format(id=instance_id))

    time.sleep(10)

    response = asgclient.complete_lifecycle_action(
      AutoScalingGroupName=event['detail']['AutoScalingGroupName'],
      LifecycleActionResult='CONTINUE',
      LifecycleActionToken=event['detail']['LifecycleActionToken'],
      LifecycleHookName=event['detail']['LifecycleHookName'],
    )


    exit()

  elif event['detail-type'] == "EC2 Instance Rebalance Recommendation":
    instance_id = event['detail']['instance-id']
    logger.info("Handling EC2 Instance Rebalance Recommendation for instance {id}".format(id=instance_id))

    exit()

  elif event['detail-type'] == "EC2 Spot Instance Interruption Warning":
    instance_id = event['detail']['instance-id']
    logger.info("Handling spot instance interruption notification for instance {id}".format(id=instance_id))

    exit()

    resp = dynamodbTable.query(
      IndexName=instanceIndexName,
      KeyConditionExpression=Key('instanceId').eq(instance_id),
    )

    print("resp={}".format(resp))

    if resp['Count'] >=1 :

      ebsId = resp['Items'][0]["ebsId"]
      clientId = resp['Items'][0]["clientId"]

      dynamodbTable.update_item(
        Key={
          'clientId': clientId
        },
        UpdateExpression='SET ST = :val1',
        ExpressionAttributeValues={
          ':val1': 'FREE'
        }
      )

    detach_instance_from_asg(instance_id)


  #elif event['detail-type'] == "EC2 Spot Instance Request Fulfillment":
  elif event['detail-type'] == "ECS_FORCE_DEPLOYMENT":
    response = ecsclient.update_service(
      cluster='demo',
      service='c1-user1',
      forceNewDeployment=True
    )
  elif event['detail-type'] == "EC2 Instance Launch Successful":
    instance_id = event['detail']['EC2InstanceId']
    logger.info("Handling EC2 Instance Launch Successful for instance {id}".format(id=instance_id))
    #logger.info("Handling spot instance Request Fulfillment notification for instance {id}".format(id=instance_id))

    resp = dynamodbTable.query(
      IndexName=statusIndexName,
      KeyConditionExpression=Key('ST').eq('FREE'),
    )

    print("resp={}".format(resp))

    if resp['Count'] >=1 :

      ebsId = resp['Items'][0]["ebsId"]
      clientId = resp['Items'][0]["clientId"]
      device = '/dev/sdf'

      print("instance_id {} is waiting for ebsId {} to be in available state for customer {}".format(instance_id, ebsId, clientId))
      ec2client.get_waiter('volume_available').wait(
        VolumeIds=[ebsId],
        DryRun=False
      )


      print("attaching ebsId={} to instance_id={} at device={} for the customer {}".format(ebsId, instance_id, device, clientId))
      response= ec2client.attach_volume(
        Device=device,
        InstanceId=instance_id,
        VolumeId=ebsId,
        DryRun=False
      )
      print("response={}".format(response))

      ec2client.get_waiter('volume_in_use').wait(
        VolumeIds=[ebsId],
        DryRun=False
      )

      waiter = ec2client.get_waiter('system_status_ok')
      print("Waiting for the instance_id={} state to become running".format(instance_id))
      waiter.wait(InstanceIds=[instance_id])

      print("Sending ssm command to the instance_id={}".format(instance_id))
      response = ssmclient.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': ['sudo mount /dev/sdf /data']}, )


      #fil = 'ec2InstanceId == i-029c502bbead6919b'
      fil = 'ec2InstanceId == ' + instance_id
      response = ecsclient.list_container_instances(
        cluster=clusterName,
        filter=fil,
        nextToken='',
        maxResults=10,
        status='ACTIVE'
      )
      print(response)
      containerInstanceId = response['containerInstanceArns'][0]
      print(containerInstanceId)

      response = ecsclient.put_attributes(
        cluster=clusterName,
        attributes=[
          {
            'name': 'lifecycle',
            'value': clientId,
            'targetType': 'container-instance',
            'targetId': containerInstanceId
          },
        ]
      )



      print("Updating the dynamodb table for the customer id {} with instance_id={}".format(clientId, instance_id))

      dynamodbTable.update_item(
        Key={
          'clientId': clientId
        },
        UpdateExpression='SET ST = :val1, instanceId = :val2',
        ExpressionAttributeValues={
          ':val1': 'USED',
          ':val2': instance_id
        }
      )






