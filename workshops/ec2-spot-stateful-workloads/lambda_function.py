import boto3
from boto3.dynamodb.conditions import Key
import os
import json
import decimal
from random import seed
from random import random
import threading
from pprint import pprint
import time
import sys
import datetime
import base64
#from bson import json_util


InstancesTableName=os.getenv('DYNAMODB_INSTANCEID_TABLE_NAME')
StatusIndexName=os.getenv('DYNAMODB_GSI_ST')

ec2client = boto3.client('ec2', region_name='us-east-1')
ec2resource = boto3.resource('ec2')
dbclient = boto3.client('dynamodb')
dynamodbresource = boto3.resource('dynamodb')
InstanceTable = dynamodbresource.Table(InstancesTableName)

subnetIdToAZMappings = {
  'subnet-0c07359b41da1e17c': 'us-east-1a',
  'subnet-01e89d5cc1b12f515': 'us-east-1b',
}

AZtoSubnetIdMappings = {
  'us-east-1a' : 'subnet-0c07359b41da1e17c' ,
  'us-east-1b' : 'subnet-01e89d5cc1b12f515' ,
}

def createSnapshotFromVolumeId(snapshotDescription, volumeId):

  try:
    print("Creating snapshot for volumeId={}...".format(volumeId))
    response = ec2client.create_snapshot(
      Description= snapshotDescription,
      VolumeId = volumeId,
      DryRun= False
    )
    print("response={}".format(str(response)))
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    snapshotId = response['SnapshotId']
    if status_code == 200:
      print("Creating snapshot for volumeId={} successfully".format(volumeId))

  except Exception as e:
    exception_message = "There was error in creating snapshot " + snapshotId + " with volume id "+ volumeId+" and error is: \n" \
                        + str(e)
    print("exception_message={}".format(exception_message))

  return snapshotId

def getEC2Atrributes(InstanceId):

  data=("NA", "NA", "NA", "NA")

  try:
    print("getEC2Atrributes: Reading the Insrance Attributes for InstanceId..".format(InstanceId))
    describeInstance = ec2client.describe_instances(InstanceIds=[InstanceId])
    #print(json.dumps(describeInstance, indent=2))
    #print(json.dumps(describeInstance, indent=2, default=json_util.default))
    ImageId = describeInstance['Reservations'][0]['Instances'][0]['ImageId']
    InstanceType = describeInstance['Reservations'][0]['Instances'][0]['InstanceType']
    IP = describeInstance['Reservations'][0]['Instances'][0]['PrivateIpAddress']
    subnetId = describeInstance['Reservations'][0]['Instances'][0]['SubnetId']
    AZ = subnetIdToAZMappings [ subnetId]
    rootvolume = describeInstance['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
    volume1 = describeInstance['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][1]['Ebs']['VolumeId']
    volume2 = describeInstance['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][2]['Ebs']['VolumeId']
    volumeIds = rootvolume +','+volume1+','+volume2
    return (ImageId, InstanceType, AZ, volumeIds, IP)



  except Exception as e:
    exception_message = "There was error in creating EC2 attributes for InstanceId " + InstanceId +" and error is: \n" \
                        + str(e)
    print("exception_message={}".format(exception_message))


  return data


def createAMIfromSnapshot(snapshotId):

  AMIId="NA"

  try:
    print("Creating AMIId for snapshotId={}...".format(snapshotId))
    response = ec2client.register_image(
      Architecture='x86_64',
      BlockDeviceMappings=[
        {
          'DeviceName': '/dev/xvda',
          'Ebs': {
            'DeleteOnTermination': False,
            'SnapshotId': snapshotId,
            'VolumeSize': 8,
            'VolumeType': 'gp2'
          }
        }
      ],
      Description='Description for Root Volume',
      RootDeviceName='/dev/xvda',
      Name="RootVolume-"+snapshotId
    )
    #print(json.dumps(response, indent=2, default=json_util.default))
    #print(json.dumps(response, indent=2))
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    AMIId = response['ImageId']
    if status_code == 200:
      print("Created AMIId={} for snapshotId={} successfully".format(AMIId, snapshotId))


  except Exception as e:
    exception_message = "There was error in creating AMI for snapshotId " + snapshotId +" and error is: \n" \
                        + str(e)
    print("exception_message={}".format(exception_message))


  return AMIId

def createLaunchTemplateVersion(launchTemplateId, launchTemplateVersion, ImageId, snapshotId1, snapshotId2, IP):

  response = ec2client.create_launch_template_version(
    LaunchTemplateId=launchTemplateId,
    SourceVersion=launchTemplateVersion,
    VersionDescription='V2',
    LaunchTemplateData={
      'BlockDeviceMappings': [
        {
          'DeviceName': '/dev/xvda',
          'Ebs': {
            'DeleteOnTermination': False,
            'VolumeSize': 8,
            'VolumeType': 'gp2'
          }
        },
        {
          'DeviceName': '/dev/xvdb',
          'Ebs': {
            'DeleteOnTermination': False,
            'VolumeSize': 8,
            'SnapshotId': snapshotId1,
            'VolumeType': 'gp2'
          }
        },
        {
          'DeviceName': '/dev/xvdc',
          'Ebs': {
            'DeleteOnTermination': False,
            'VolumeSize': 8,
            'SnapshotId': snapshotId2,
            'VolumeType': 'gp2'
          }
        },
      ],
      'NetworkInterfaces': [
        {
          'DeviceIndex': 0,
          'PrivateIpAddresses': [
            {
              'Primary': True,
              'PrivateIpAddress': IP
            },
          ]
        },
      ],
      'ImageId': ImageId
    }
  )

def createEC2Fleet(launchTemplateId, launchTemplateVersion, SubnetId):
  response = ec2client.create_fleet(
    SpotOptions={
      'AllocationStrategy': 'capacity-optimized',
      'InstanceInterruptionBehavior': 'terminate'
    },
    OnDemandOptions={
      'AllocationStrategy': 'prioritized'
    },
    LaunchTemplateConfigs=[
      {
        'LaunchTemplateSpecification': {
          'LaunchTemplateId': launchTemplateId,
          'Version': launchTemplateVersion
        },
        'Overrides': [
          {
            "InstanceType": "m4.large",
            "SubnetId": SubnetId,
            "WeightedCapacity": 1
          },
          {
            "InstanceType": "m5.large",
            "SubnetId": SubnetId,
            "WeightedCapacity": 1
          },
          {
            "InstanceType": "c4.large",
            "SubnetId": SubnetId,
            "WeightedCapacity": 1
          },

          {
            "InstanceType": "c5.large",
            "SubnetId": SubnetId,
            "WeightedCapacity": 1
          },
          {
            "InstanceType": "r4.large",
            "SubnetId": SubnetId,
            "WeightedCapacity": 1
          },
          {
            "InstanceType": "r5.large",
            "SubnetId": SubnetId,
            "WeightedCapacity": 1
          },
          {
            "InstanceType": "t3a.large",
            "SubnetId": SubnetId,
            "WeightedCapacity": 1
          },
          {
            "InstanceType": "t3.large",
            "SubnetId": SubnetId,
            "WeightedCapacity": 1
          },
          {
            "InstanceType": "t2.large",
            "SubnetId": SubnetId,
            "WeightedCapacity": 1
          },
          {
            "InstanceType": "m5a.large",
            "SubnetId": SubnetId,
            "WeightedCapacity": 1
          }
        ]
      },
    ],
    TargetCapacitySpecification={
      'TotalTargetCapacity': 1,
      'OnDemandTargetCapacity': 0,
      'SpotTargetCapacity': 1,
      'DefaultTargetCapacityType': 'spot'
    },
    Type='instant',
    TagSpecifications=[
      {
        'ResourceType': 'instance',
        'Tags': [
          {
            'Key': 'Name',
            'Value': 'ec2-fleet-stateful'
          },
        ]
      },
    ]
  )
  #print(json.dumps(response, indent=2))
  #print(json.dumps(response, indent=2, default=json_util.default))

  FleetId = response['FleetId']
  Errors = response['Errors']
  print("FleetId={} Errors={}".format(FleetId, Errors))
  InstanceType = response['Instances'][0]['LaunchTemplateAndOverrides']['Overrides']['InstanceType']
  InstanceId = response['Instances'][0]['InstanceIds'][0]
  subnetId = response['Instances'][0]['LaunchTemplateAndOverrides']['Overrides']['SubnetId']
  print("InstanceType={} subnetId={}".format(InstanceType,subnetId))
  return InstanceId


def lambda_handler(event, context):
  # TODO implement

  InstanceId = event['detail']['instance-id']
  #return {
  #    'statusCode': 200,
  #    'body': json.dumps("Complered processing of the termination of the InstanceId={}".format(InstanceId))
  #}


  if event["detail-type"] == "EC2 Instance State-change Notification":

    print("Received EC2 Instance State-change Notification InstanceId={}...".format(InstanceId))

    try:
      response = InstanceTable.get_item(Key={'InstanceId': InstanceId})
    except ClientError as e:
      print(e.response['Error']['Message'])

    #pprint(response, sort_dicts=False)
    volumeIds = response['Item']['VolumeIds']
    IP = response['Item']['IP']
    AZ = response['Item']['AZ']


    print("volumeIds={} IP={} AZ={}".format(volumeIds, IP, AZ))
    volumeIdList = volumeIds.split(',')
    print("volumeIdList={}".format(volumeIdList))
    snapshotIdList = []

    for index, volumeId in enumerate(volumeIdList):
      print("volumeId={}".format(volumeId))
      snapshotId=createSnapshotFromVolumeId("volume"+str(index), volumeId)
      snapshotIdList.append(snapshotId)

    snapshotIds = ','.join(snapshotIdList)
    print("Waiting for the snapshotIdList={} snapshotIds={} to be completed".format(snapshotIdList, snapshotIds))

    waiter = ec2client.get_waiter('snapshot_completed')
    waiter.wait(SnapshotIds=snapshotIdList)

    AMIId = createAMIfromSnapshot(snapshotIdList[0])
    waiter = ec2client.get_waiter('image_available')
    waiter.wait(ImageIds=[AMIId])
    launchTemplateId='lt-03ca5a44acf2af90a'
    launchTemplateVersion = '14'
    createLaunchTemplateVersion(launchTemplateId, launchTemplateVersion, AMIId, snapshotIdList[1], snapshotIdList[2], IP)
    launchTemplateVersion = '$Latest'
    subnetId = AZtoSubnetIdMappings[AZ]
    print("createEC2Fleet with launchTemplateId={} launchTemplateVersion={} subnetId={}".format(launchTemplateId, launchTemplateVersion, subnetId))
    NewInstanceId = createEC2Fleet(launchTemplateId, launchTemplateVersion, subnetId)
    waiter = ec2client.get_waiter('system_status_ok')
    waiter.wait(InstanceIds=[NewInstanceId])
    #response = ec2client.delete_launch_template_versions(
    #    LaunchTemplateId=launchTemplateId,
    #    Versions=[
    #        '2',
    #    ]
    #)
    (ImageId, InstanceType, AZ, volumeIds, IP) = getEC2Atrributes(NewInstanceId)
    table = dynamodbresource.Table('InstancesTable')
    print("Adding NewInstanceId={} details to the dynamodb".format(InstanceId))
    response = table.put_item(
      Item={
        'InstanceId': NewInstanceId,
        'ST': 'USED',
        'VolumeIds': volumeIds,
        'SnapshotIds': 'NA',
        'IP': IP,
        'AZ': AZ,
        'ImageId' : ImageId,
        'Lifecycle' : 'SPOT',
        'InstanceType' : InstanceType
      }
    )
    print("Updating the InstanceId={} details to the dynamodb".format(InstanceId))
    table.update_item(
      Key={
        'InstanceId': InstanceId
      },
      UpdateExpression='SET ST = :val1, SnapshotIds = :val2',
      ExpressionAttributeValues={
        ':val1': 'FREE',
        ':val2': snapshotIds
      }
    )


  return {
    'statusCode': 200,
    'body': json.dumps("Complered processing of the termination of the InstanceId={}".format(InstanceId))
  }
