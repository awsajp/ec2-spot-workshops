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
import cfnresponse
#from bson import json_util


#InstancesTableName=os.getenv('DYNAMODB_INSTANCEID_TABLE_NAME')
#StatusIndexName=os.getenv('DYNAMODB_GSI_ST')
InstancesTableName=os.getenv('DYNAMODB_INSTANCEID_TABLE_NAME')
StatusIndexName=os.getenv('DYNAMODB_GSI_ST')
RootEBSVolumeSize=os.getenv('ROOT_EBS_VOLUME_SIZE')
launchTemplateId=os.getenv('LAUNCH_TEMPLATE_ID')
InstanceTypes=os.getenv('INSTANCE_TYPES_LIST')
subnetIdsString=os.getenv('SUBNET_IDs_LIST')





ec2client = boto3.client('ec2', region_name='us-east-1')
ec2resource = boto3.resource('ec2')
dbclient = boto3.client('dynamodb')
dynamodbresource = boto3.resource('dynamodb')
InstanceTable = dynamodbresource.Table(InstancesTableName)


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
            'VolumeSize': int(RootEBSVolumeSize),
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
            'VolumeType': 'gp2'
          }
        },
        {
          'DeviceName': '/dev/xvdb',
          'Ebs': {
            'DeleteOnTermination': False,
            'SnapshotId': snapshotId1,
            'VolumeType': 'gp2'
          }
        },
        {
          'DeviceName': '/dev/xvdc',
          'Ebs': {
            'DeleteOnTermination': False,
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

def createEC2Fleet(launchTemplateVersion,SubnetId,TotalTargetCapacity,OnDemandTargetCapacity,SpotTargetCapacity):

  Overrides=[]
  InstanceTypesList= InstanceTypes.split(',')
  subnetIdsList = SubnetId.split(',')

  for InstanceId in InstanceTypesList:
    for subnetId in subnetIdsList:
      Overrides.append({'InstanceType':InstanceId,
                        'SubnetId': subnetId,
                        'WeightedCapacity': 1
                        })

  pprint("Overrides={}".format(Overrides))

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
        'Overrides': Overrides
      },
    ],
    TargetCapacitySpecification={
      'TotalTargetCapacity': TotalTargetCapacity,
      'OnDemandTargetCapacity': OnDemandTargetCapacity,
      'SpotTargetCapacity': SpotTargetCapacity,
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
  #Errors = response['Errors']
  #print("FleetId={} Errors={}".format(FleetId, Errors))
  #InstanceType = response['Instances'][0]['LaunchTemplateAndOverrides']['Overrides']['InstanceType']
  #InstanceId = response['Instances'][0]['InstanceIds'][0]
  #subnetId = response['Instances'][0]['LaunchTemplateAndOverrides']['Overrides']['SubnetId']
  #print("InstanceType={} subnetId={}".format(InstanceType,subnetId))
  return FleetId

def updateInstanceStatusInDynamoDB(EC2FleetId):

  print("Running updateInstanceStatusInDynamoDB for EC2FleetId={}".format(EC2FleetId))
  response = ec2client.describe_fleets(FleetIds=[EC2FleetId])
  ActivityStatus = response['Fleets'][0]['ActivityStatus']
  Errors = response['Fleets'][0]['Errors']
  FleetState = response['Fleets'][0]['FleetState']
  FulfilledCapacity = response['Fleets'][0]['FulfilledCapacity']
  FulfilledOnDemandCapacity = response['Fleets'][0]['FulfilledOnDemandCapacity']
  InstanceList = response['Fleets'][0]['Instances']
  #LegnthOfInstanceList =  len(InstanceList)
  for instanceData in InstanceList:
    Lifecycle = instanceData['Lifecycle']
    InstanceIds = instanceData['InstanceIds']
    for InstanceId in InstanceIds:
      print("Waiting for the InstanceId={} state to become running".format(InstanceId))
      waiter = ec2client.get_waiter('system_status_ok')
      waiter.wait(InstanceIds=[InstanceId])
      describeInstance = ec2client.describe_instances(InstanceIds=[InstanceId])
      #print(json.dumps(describeInstance, indent=2, default=json_util.default))
      InstanceData = describeInstance['Reservations'][0]['Instances'][0]
      ImageId = InstanceData['ImageId']
      InstanceType = InstanceData['InstanceType']
      IP = InstanceData['PrivateIpAddress']
      SubnetId = InstanceData['SubnetId']
      AZ = InstanceData['Placement']['AvailabilityZone']
      rootvolume = InstanceData['BlockDeviceMappings'][0]['Ebs']['VolumeId']
      volume1    = InstanceData['BlockDeviceMappings'][1]['Ebs']['VolumeId']
      volume2    = InstanceData['BlockDeviceMappings'][2]['Ebs']['VolumeId']
      volumeIds = rootvolume +','+volume1+','+volume2
      #table = dynamodbresource.Table(InstanceTable)
      print("Adding InstanceId={} details to the dynamodb".format(InstanceId))
      response = InstanceTable.put_item(
        Item={
          'InstanceId': InstanceId,
          'ST': 'USED',
          'VolumeIds': volumeIds,
          'SnapshotIds': 'NA',
          'IP': IP,
          'AZ': AZ,
          'SubnetId': SubnetId,
          'ImageId' : ImageId,
          'Lifecycle' : Lifecycle,
          'InstanceType' : InstanceType
        }
      )


def handleNodeTermination(InstanceId):

  print("handleNodeTermination for InstanceId={}".format(InstanceId))

  try:
    response = InstanceTable.get_item(Key={'InstanceId': InstanceId})
  except ClientError as e:
    print(e.response['Error']['Message'])

  if 'Item' in response.keys():

    volumeIds = response['Item']['VolumeIds']
    IP = response['Item']['IP']
    AZ = response['Item']['AZ']
    SubnetId = response['Item']['SubnetId']

    print("volumeIds={} IP={} AZ={} SubnetId={}".format(volumeIds, IP, AZ, SubnetId))
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

    #launchTemplateId='lt-03ca5a44acf2af90a'
    launchTemplateVersion = '1'
    createLaunchTemplateVersion(launchTemplateId, launchTemplateVersion, AMIId, snapshotIdList[1], snapshotIdList[2], IP)
    launchTemplateVersion = '$Latest'


    #EC2FleetId = createEC2Fleet(launchTemplateId, launchTemplateVersion, subnetId)

    OnDemandTargetCapacity=0
    SpotTargetCapacity=1
    TotalTargetCapacity=1
    RetainPrivateIP = os.getenv('RETAINPRIVATEIP')
    if RetainPrivateIP == "NO":
      SubnetId=subnetIdsString

    print("createEC2Fleet with launchTemplateId={} launchTemplateVersion={} SubnetId={}".format(launchTemplateId, launchTemplateVersion, SubnetId))
    EC2FleetId = createEC2Fleet(launchTemplateVersion,SubnetId,TotalTargetCapacity,OnDemandTargetCapacity,SpotTargetCapacity)

    updateInstanceStatusInDynamoDB(EC2FleetId)

    print("Deregistering the AMI={} to be completed".format(AMIId))
    response = ec2client.deregister_image(
      ImageId=AMIId
    )

    for snapshotId in snapshotIdList:
      print("Deleting the snapshotId={} to be completed".format(snapshotId))
      response = ec2client.delete_snapshot(
        SnapshotId=snapshotId
      )

    for volumeId in volumeIdList:
      print("Deleting the volumeId={} to be completed".format(volumeId))
      response = ec2client.delete_volume(
        VolumeId=volumeId
      )

    print("Terminating InstanceId={} state in the dynamodb".format(InstanceId))
    try:
      response = InstanceTable.delete_item(
        Key={
          'InstanceId': InstanceId
        }
      )
    except Exception as e:
      print(e.response['Error']['Message'])

  else:
    print("InstanceId={} does not exist in the Dynamodb Table={}. Hence Skipping the processing".format(InstanceId, InstancesTableName))

def lambda_handler(event, context):
  # TODO implement

  if 'RequestType' in event.keys():
    if event['RequestType'] == "Create":
      #EC2FleetId=os.getenv('EC2_FLEET_ID')
      OnDemandTargetCapacity=int(os.getenv('ONDEMANDTARGETCAPACITY'))
      SpotTargetCapacity=int(os.getenv('SPOTTARGETCAPACITY'))
      TotalTargetCapacity=int(os.getenv('TOTALTARGETCAPACITY'))
      launchTemplateVersion = '1'
      SubnetId=os.getenv('SUBNET_IDs_LIST')
      EC2FleetId = createEC2Fleet(launchTemplateVersion,SubnetId,TotalTargetCapacity,OnDemandTargetCapacity,SpotTargetCapacity)
      updateInstanceStatusInDynamoDB(EC2FleetId)
    elif event['RequestType'] == "Delete":

      scan = InstanceTable.scan()
      with InstanceTable.batch_writer() as batch:
        for each in scan['Items']:
          InstanceId = each['InstanceId']
          print("Deleting the InstanceId={} from Dynamodb table={}".format(InstanceId, InstancesTableName))
          batch.delete_item(
            Key={
              'InstanceId': InstanceId
            }
          )

          time.sleep(5)
          try:
            print("Terminating the  InstanceId={}".format(InstanceId))
            response = ec2client.terminate_instances(
              InstanceIds=[
                InstanceId
              ]
            )
          except Exception as e:
            print(e.response['Error']['Message'])

    else:
      print("CFN event RequestType={} is NOT handled currently".format(event['RequestType']))


    responseData = {}
    responseData['Data'] = '1'
    #cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData,"CustomResourcePhysicalID")
    return {
      'statusCode': 200,
      'body': json.dumps("Completed processing of the event={}".format(event))
    }
  else:
    InstanceId = event['detail']['instance-id']
    print("Received EC2 Instance State-change Notification InstanceId={}...".format(InstanceId))
    handleNodeTermination(InstanceId)

    return {
      'statusCode': 200,
      'body': json.dumps("Complered processing of the termination of the InstanceId={}".format(InstanceId))
    }
