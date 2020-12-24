
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
instanceTableName=os.getenv('DYNAMODB_INSTANCE_TABLE')

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
dynamodbInstanceTable = dynamodbresource.Table(instanceTableName)


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

def getClientandEbsId(instance_id):

  resp = dynamodbTable.query(
    IndexName=instanceIndexName,
    KeyConditionExpression=Key('instanceId').eq(instance_id),
  )

  print("resp={}".format(resp))

  if resp['Count'] >=1 :

    ebsId = resp['Items'][0]["ebsId"]
    clientId = resp['Items'][0]["clientId"]
    CurrentAZId = resp['Items'][0]["AZ"]
    serviceNames = resp['Items'][0]["serviceNames"]

    print("getClientandEbsId updating clientId={} with ebsId={} with instance_id={} to FREE".format(clientId, ebsId, instance_id))

    dynamodbTable.update_item(
      Key={
        'clientId': clientId
      },
      UpdateExpression='SET ST = :val1',
      ExpressionAttributeValues={
        ':val1': 'FREE'
      }
    )
    return (clientId, ebsId, CurrentAZId, serviceNames)

  else:
    message = "FAILURE: instance_id {} DOES NOT exist in DynamoDB".format(instance_id)
    returnFromLambda(message)

def handletallyworkloadbootstrap():

  resp = dynamodbTable.query(
    IndexName=statusIndexName,
    KeyConditionExpression=Key('ST').eq('FREE'),
  )

  #print("resp={}".format(resp))

  #for item in resp['Items']:
  for i, item in enumerate(resp['Items']):

    ebsId = resp['Items'][i]["ebsId"]
    clientId = resp['Items'][i]["clientId"]
    serviceNames = resp['Items'][i]["serviceNames"]
    CurrentAZId  = resp['Items'][i]["AZ"]
    print("clientId={} ebsId={} CurrentAZId={} serviceNames={}".format(clientId, ebsId, CurrentAZId, serviceNames))
    (NewInstanceId, NewAZId) = getReplacementInstanceId()
    if CurrentAZId == NewAZId:
      attachEbsVolume(clientId, ebsId, NewInstanceId)
      deployServices(clientId, NewInstanceId, CurrentAZId, ebsId, serviceNames)
    else:
      SnapshotId = createSnapshotFromVolumeId("volumeId-"+ebsId, ebsId)
      NewvolumeId = createVolumeIdFromSnapshot(SnapshotId, NewAZId)
      attachEbsVolume(clientId, NewvolumeId, NewInstanceId)
      deployServices(clientId, NewInstanceId, NewAZId, NewvolumeId, serviceNames)





def getReplacementInstanceId():

  NewInstanceId='NA'
  NewAZId='NA'

  sleepTime = 10

  for i in range(0, 60):

    print("getReplacementInstanceId checking for NewInstanceId at iteration i={}".format(i))
    resp = dynamodbInstanceTable.query(
      IndexName=statusIndexName,
      KeyConditionExpression=Key('ST').eq('FREE'),
    )

    #print("resp={}".format(resp))

    if resp['Count'] >=1 :

      NewInstanceId = resp['Items'][0]["instanceId"]
      NewAZId = resp['Items'][0]["AZ"]

      print("getReplacementInstanceId updating NewInstanceId={} NewAZId={} with ST to USED at iteration i={}".format(NewInstanceId, NewAZId, i))

      dynamodbInstanceTable.update_item(
        Key={
          'instanceId': NewInstanceId
        },
        UpdateExpression='SET ST = :val1',
        ExpressionAttributeValues={
          ':val1': 'USED'
        }
      )

      break


    else:
      print("getReplacementInstanceId sleeping for {} sec at iteration i={}".format(sleepTime, i))
      time.sleep(sleepTime)

  return (NewInstanceId, NewAZId)


def attachEbsVolume(clientId, ebsId, NewInstanceId):

  device = '/dev/sdf'

  print("attachEbsVolume waiting for ebsId {} to be in available to attach to NewInstanceId={} for customer {}".format( ebsId, NewInstanceId, clientId))
  ec2client.get_waiter('volume_available').wait( VolumeIds=[ebsId], DryRun=False )

  print("attaching ebsId={} to NewInstanceId={} at device={} for the customer {} at device={}".format(ebsId, NewInstanceId, device, clientId, device))
  response= ec2client.attach_volume(
    Device=device,
    InstanceId=NewInstanceId,
    VolumeId=ebsId,
    DryRun=False
  )
  #print("response={}".format(response))

  ec2client.get_waiter('volume_in_use').wait( VolumeIds=[ebsId],   DryRun=False  )

  waiter = ec2client.get_waiter('system_status_ok')
  print("Waiting for the NewInstanceId={} state to become running".format(NewInstanceId))
  waiter.wait(InstanceIds=[NewInstanceId])

  print("Sending ssm command to the instance_id={}".format(NewInstanceId))
  response = ssmclient.send_command(
    InstanceIds=[NewInstanceId],
    DocumentName="AWS-RunShellScript",
    Parameters={'commands': ['sudo mount /dev/sdf /data']}, )

  print("Deleting the NewInstanceId={} from dynamodb InstanceTable".format(NewInstanceId))
  response = dynamodbInstanceTable.delete_item( Key={ 'instanceId': NewInstanceId  }  )


def createSnapshotFromVolumeId(snapshotDescription, volumeId):

  try:
    print("createSnapshotFromVolumeId waiting for volumeId {} to be in available".format( volumeId))
    ec2client.get_waiter('volume_available').wait( VolumeIds=[volumeId], DryRun=False )

    print("createSnapshotFromVolumeId : starting for volumeId={}".format(volumeId))
    response = ec2client.create_snapshot( Description= snapshotDescription, VolumeId = volumeId )
    status_code = response['ResponseMetadata']['HTTPStatusCode']

    if status_code == 200:
      snapshotId = response['SnapshotId']
      print("createSnapshotFromVolumeId created and waiting for snapshotId={} for volumeId={} to be completed".format(snapshotId, volumeId))
      waiter = ec2client.get_waiter('snapshot_completed')
      waiter.wait(SnapshotIds=[snapshotId])
      return snapshotId
    else:
      message = "FAILURE: createSnapshotFromVolumeId failed for volumeId={}".format(volumeId)
      returnFromLambda(message)

  except Exception as e:
    message = "FAILURE: createSnapshotFromVolumeId failed with {} for volumeId={}".format(str(e), volumeId)
    returnFromLambda(message)


def createVolumeIdFromSnapshot(SnapshotId, AvailabilityZoneId):

  try:
    print("createVolumeIdFromSnapshot starting for SnapshotId={}".format(SnapshotId))
    response = ec2client.create_volume(SnapshotId=SnapshotId, AvailabilityZone=AvailabilityZoneId)
    #print(response)
    status_code = response['ResponseMetadata']['HTTPStatusCode']

    if status_code == 200:
      VolumeId = response['VolumeId']
      print("createVolumeIdFromSnapshot created VolumeId={} in AvailabilityZone {} for SnapshotId={}".format(VolumeId, AvailabilityZoneId, SnapshotId))
      return VolumeId
    else:
      message = "FAILURE: createVolumeIdFromSnapshot failed for SnapshotId={}".format(SnapshotId)
      returnFromLambda(message)

  except Exception as e:
    message = "FAILURE: createVolumeIdFromSnapshot failed with {} for SnapshotId={}".format(str(e), SnapshotId)
    returnFromLambda(message)



def deployServices(clientId, NewInstanceId, AZId, VolumeId, serviceNames):

  fil = 'ec2InstanceId == ' + NewInstanceId
  response = ecsclient.list_container_instances(
    cluster=clusterName,
    filter=fil,
    nextToken='',
    maxResults=10,
    status='ACTIVE'
  )
  #print(response)
  containerInstanceId = response['containerInstanceArns'][0]
  print("deployServices containerInstanceId={}".format(containerInstanceId))


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

  dynamodbTable.update_item(
    Key={
      'clientId': clientId
    },
    UpdateExpression='SET ST = :val1, instanceId = :val2, AZ = :val3, ebsId = :val4',
    ExpressionAttributeValues={
      ':val1': 'USED',
      ':val2': NewInstanceId,
      ':val3': AZId,
      ':val4': VolumeId
    }
  )

  serviceNamesList = serviceNames.split(',')

  for serviceName in serviceNamesList:
    print("deployServices deploying the service {}".format(serviceName))
    response = ecsclient.update_service(
      cluster=clusterName,
      service=serviceName,
      forceNewDeployment=True
    )



def returnFromLambda(message):

  return {
    'statusCode': 200,
    'body': json.dumps("Completed processing with message={}".format(message))
  }



def handler(event, context):


  if event['detail-type'] == "EC2 Instance Rebalance Recommendation":
    instance_id = event['detail']['instance-id']
    logger.info("Handling EC2 Instance Rebalance Recommendation for instance {id}".format(id=instance_id))
  if event['detail-type'] == "EC2 Instance Terminate Successful":
    instance_id = event['detail']['EC2InstanceId']
    logger.info("Handling EC2 Instance Terminate Successful for instance {id}".format(id=instance_id))
  if event['detail-type'] == "EC2 Instance-terminate Lifecycle Action":
    instance_id = event['detail']['EC2InstanceId']
    logger.info("Handling EC2 Instance-terminate Lifecycle Action for instance {id}".format(id=instance_id))
  if event['detail-type'] == "EC2 Instance Terminate Unsuccessful":
    instance_id = event['detail']['EC2InstanceId']
    logger.info("Handling EC2 Instance Terminate Unsuccessful for instance {id}".format(id=instance_id))
  elif event['detail-type'] == "EC2 Spot Instance Interruption Warning":
    instance_id = event['detail']['instance-id']
    logger.info("Handling spot instance interruption notification for instance {id}".format(id=instance_id))

    (clientId, ebsId, CurrentAZId, serviceNames) =  getClientandEbsId(instance_id)
    print("clientId={} ebsId={} CurrentAZId={} serviceNames={}".format(clientId, ebsId, CurrentAZId, serviceNames))

    (NewInstanceId, NewAZId) = getReplacementInstanceId()

    if CurrentAZId == NewAZId:
      AZId = CurrentAZId
      VolumeId = ebsId
    else:
      AZId = NewAZId
      print("Calling createSnapshotFromVolumeId for volumeId={}".format(ebsId))
      SnapshotId = createSnapshotFromVolumeId("volumeId-"+ebsId, ebsId)
      VolumeId = createVolumeIdFromSnapshot(SnapshotId, NewAZId)

    attachEbsVolume(clientId, VolumeId, NewInstanceId)
    deployServices(clientId, NewInstanceId, AZId, VolumeId, serviceNames)

    if CurrentAZId != NewAZId:
      print("deleting the SnapshotId={} and ebsId={} from AvailabilityZone={} ".format(SnapshotId, ebsId, CurrentAZId))
      response = ec2client.delete_volume(VolumeId=ebsId)
      response = ec2client.delete_snapshot(SnapshotId=SnapshotId)


    #detach_instance_from_asg(instance_id)


  #elif event['detail-type'] == "EC2 Spot Instance Request Fulfillment":
  elif event['detail-type'] == "ECS_FORCE_DEPLOYMENT":
    #response = ecsclient.update_service(
    #    cluster='demo',
    #    service='c1-user1',
    #    forceNewDeployment=True
    #)

    serviceNames = 'c2-user1,c2-user2'
    serviceNamesList = serviceNames.split(',')

    for serviceName in serviceNamesList:
      response = ecsclient.update_service(
        cluster=clusterName,
        service=serviceName,
        forceNewDeployment=True
      )

  elif event['detail-type'] == "TALLY_WORKLOAD_BOOTSTRAPP":
    handletallyworkloadbootstrap()
  elif event['detail-type'] == "TEST_SNAPSHOT":
    volumeId = event['volumeId']
    SnapshotId = 'snap-0e10bd8cfe5ece490'
    AvailabilityZoneId = 'ap-south-1a'
    #SnapshotId = createSnapshotFromVolumeId("volumeId-"+volumeId, volumeId)
    volumeId = createVolumeIdFromSnapshot(SnapshotId, AvailabilityZoneId)

  elif event['detail-type'] == "EC2 Instance Launch Successful":
    instance_id = event['detail']['EC2InstanceId']
    logger.info("Handling EC2 Instance Launch Successful for instance {id}".format(id=instance_id))
    #logger.info("Handling spot instance Request Fulfillment notification for instance {id}".format(id=instance_id))

    describeInstance = ec2client.describe_instances(InstanceIds=[instance_id])
    #print(json.dumps(describeInstance, indent=2, default=json_util.default))
    InstanceData = describeInstance['Reservations'][0]['Instances'][0]
    ImageId = InstanceData['ImageId']
    InstanceType = InstanceData['InstanceType']
    IP = InstanceData['PrivateIpAddress']
    SubnetId = InstanceData['SubnetId']
    AZ = InstanceData['Placement']['AvailabilityZone']


    logger.info("Updating dynamodb with InstanceId={} data InstanceType={} ImageId={} IP={} SubnetId={} AZ={}".format(instance_id, InstanceType, ImageId, IP, SubnetId, AZ))

    response = dynamodbInstanceTable.put_item(
      Item={
        'instanceId': instance_id,
        'ST': 'FREE',
        'IP': IP,
        'AZ': AZ,
        'SubnetId': SubnetId,
        'ImageId' : ImageId,
        'InstanceType' : InstanceType
      }
    )


  message = "SUCCESS"
  returnFromLambda(message)


