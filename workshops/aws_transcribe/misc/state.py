from flask import Flask, render_template
from flask.ext.cors import CORS, cross_origin
import os
import requests
import json
import time
import sys
import boto3
import datetime
import tzlocal
import base64
from bson import json_util

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ec2client = boto3.client('ec2', region_name='us-east-1')
ec2resource = boto3.resource('ec2')
dbclient = boto3.client('dynamodb')
dynamodbresource = boto3.resource('dynamodb')
subnetIdToAZMappings = {
  'subnet-0c07359b41da1e17c': 'us-east-1a',
  'subnet-01e89d5cc1b12f515': 'us-east-1b',
}

subnetIdList = ['subnet-0c07359b41da1e17c', 'subnet-01e89d5cc1b12f515']

@app.route('/')
@cross_origin()
def index():

  response = ""
  response +="<head> <title>Spot Game Day</title> </head>"
  response += "<h2>I am a Simple Web App Running with below Attributes </h2> <hr/>"

  try:
    URL = "http://169.254.169.254/latest/meta-data/spot/termination-time"
    SpotInt = requests.get(URL)
    if SpotInt.status_code == 200:
      response += "<h1>This Spot Instance Got Interruption and Termination Date is {} </h1> <hr/>".format(SpotInt.text)


    URL = "http://169.254.169.254/latest/dynamic/instance-identity/document"
    InstanceData = requests.get(URL).json()

    instanceId = InstanceData['instanceId']
    response += "<li>My instance_id = {}</li>".format(instanceId)
    lifecycle = getInstanceLifecycle(instanceId, InstanceData['region'])
    response += "<li>My Instance lifecycle = {}</li>".format(lifecycle)
    response += "<li>My instance_type = {}</li>".format(InstanceData['instanceType'])
    response += "<li>My Intance private_ipv4 = {}</li>".format(InstanceData['privateIp'])
    response += "<li>My availability_zone = {}</li>".format(InstanceData['availabilityZone'])
    response += "<li>My Region = {}</li>".format(InstanceData['region'])

    publicIp = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4")
    response += "<li>My instance_type public_ipv4 = {}</li>".format(publicIp.text)
    AMIIndexId = requests.get("http://169.254.169.254/latest/meta-data/ami-launch-index")
    response += "<li>My ami_launch_index = {}</li>".format(AMIIndexId.text)

    AMIId = requests.get("http://169.254.169.254/latest/meta-data/ami-id")
    response += "<li>My ami_launch_index = {}</li>".format(AMIId.text)

    MacId = requests.get("http://169.254.169.254/latest/meta-data/mac")
    Mac = MacId.text

    URL = "http://169.254.169.254/latest/meta-data/network/interfaces/macs/" + str(MacId.text) + "/subnet-id"
    SubnetId = requests.get(URL)
    response += "<li>My subnet_id = {}</li>".format(SubnetId.text)

    URL = "http://169.254.169.254/latest/meta-data/network/interfaces/macs/" + str(MacId.text) + "/vpc-id"
    VPCId = requests.get(URL)
    response += "<li>My vpc_id = {}</li>".format(VPCId.text)


  except Exception as inst:
    response += "<li>Oops !!! Failed to access my instance  metadata with error = {}</li>".format(inst)

  return response
def getInstanceLifecycle(x, y):
  return x+y


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

def createSnapshot(volumes_dict):

  successful_snapshots = dict()
  for snapshot in volumes_dict:
    try:
      print("Creating snapshot for {} with volumeId={}".format(snapshot, volumes_dict[snapshot]))
      response = ec2client.create_snapshot(
        Description= snapshot,
        VolumeId= volumes_dict[snapshot],
        DryRun= False
      )
      print("response={}".format(str(response)))
      # response is a dictionary containing ResponseMetadata and SnapshotId
      status_code = response['ResponseMetadata']['HTTPStatusCode']
      snapshot_id = response['SnapshotId']
      # check if status_code was 200 or not to ensure the snapshot was created successfully
      if status_code == 200:
        successful_snapshots[snapshot] = snapshot_id

    except Exception as e:
      exception_message = "There was error in creating snapshot " + snapshot + " with volume id "+volumes_dict[snapshot]+" and error is: \n" \
                          + str(e)
  return successful_snapshots

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
    print(json.dumps(response, indent=2, default=json_util.default))
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    AMIId = response['ImageId']
    if status_code == 200:
      print("Created AMIId for snapshotId={} successfully".format(snapshotId))


  except Exception as e:
    exception_message = "There was error in creating AMI for snapshotId " + snapshotId +" and error is: \n" \
                        + str(e)
    print("exception_message={}".format(exception_message))


  return AMIId

def wait_ec2_complate(instance_id):

  print("waiting for the InstanceId={} to be ready".format(instance_id))
  iter = 1
  status = False
  while True:
    iter += 1
    time.sleep(15)
    rsp = ec2client.describe_instance_status(
      InstanceIds=[str(instance_id)],
      IncludeAllInstances=True
    )
    # double check 2/2 status
    instance_status = rsp['InstanceStatuses'][0]['InstanceStatus']['Status']
    system_status = rsp['InstanceStatuses'][0]['SystemStatus']['Status']
    print("iter={} Instance status is {} System status is {}".format(iter, str(instance_status), str(system_status)))
    if str(instance_status) == 'ok' and str(system_status) == 'ok':
      status = True
      break

    if iter >= 30:
      break
  return status


def provisionEC2Instances(launchTemplateId, count):
  #launchTemplateId =  createLaunchTemplate()
  #launchTemplateId =  createLaunchTemplate()
  #launchTemplateId =  'lt-0665cda51a915dd48'
  launchTemplateVersion = '1'
  InstanceIdList = []
  AZCount = len (subnetIdToAZMappings)
  for val in range(0, count):
    SubnetId = subnetIdList [ val % AZCount]
    InstanceId = createEC2Fleet(launchTemplateId, launchTemplateVersion, SubnetId)
    print("Adding InstanceId={} to the list at Index {}".format(InstanceId, val))
    InstanceIdList.append(InstanceId)

  for val in range(0, count):
    InstanceId = InstanceIdList[val]
    wait_ec2_complate(InstanceId)
    describeInstance = ec2client.describe_instances(InstanceIds=[InstanceId])
    print(json.dumps(describeInstance, indent=2, default=json_util.default))
    ImageId = describeInstance['Reservations'][0]['Instances'][0]['ImageId']
    InstanceType = describeInstance['Reservations'][0]['Instances'][0]['InstanceType']
    IP = describeInstance['Reservations'][0]['Instances'][0]['PrivateIpAddress']
    subnetId = describeInstance['Reservations'][0]['Instances'][0]['SubnetId']
    AZ = subnetIdToAZMappings [ subnetId]
    rootvolume = describeInstance['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
    volume1 = describeInstance['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][1]['Ebs']['VolumeId']
    volume2 = describeInstance['Reservations'][0]['Instances'][0]['BlockDeviceMappings'][2]['Ebs']['VolumeId']
    volumeIds = rootvolume +','+volume1+','+volume2
    table = dynamodbresource.Table('InstancesTable')
    print("Adding InstanceId={} details to the dynamodb".format(InstanceId))
    response = table.put_item(
      Item={
        'InstanceId': InstanceId,
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

    #(instanceType, InstanceId, subnetId) = createEC2Fleet(launchTemplateId, '9')
    #createEC2Instance(InstanceId, subnetId)

def replaceEC2Instance(count):
  #launchTemplateId =  createLaunchTemplate()
  launchTemplateId =  createLaunchTemplate()
  #launchTemplateId =  'lt-002559cf14f8e7b64'
  launchTemplateVersion = '1'
  ImageId = 'ami-02dd77165c07f3843'
  snapshotId1 = 'snap-0fc8c2a86174ad86a'
  snapshotId2 = 'snap-06c7304a47f9953f1'
  IP = '10.0.1.171'
  createLaunchTemplateVersion(launchTemplateId, launchTemplateVersion, ImageId, snapshotId1, snapshotId2, IP)

  launchTemplateVersion = str(int(launchTemplateVersion) + 1)
  subnetId ='NA'
  for val in range(0, count):

    InstanceId = createEC2Fleet(launchTemplateId, launchTemplateVersion, subnetId)
    #(instanceType, InstanceId, subnetId) = createEC2Fleet(launchTemplateId, '9')
    #createEC2Instance(InstanceId, subnetId)


def createEC2Instance(instanceType, subnetId):
  response = ec2client.run_instances(
    BlockDeviceMappings=[
      {
        'DeviceName': '/dev/xvda',
        'VirtualName': 'RootVolume',
        'Ebs': {
          'DeleteOnTermination': False,
          'VolumeSize': 8,
          'VolumeType': 'gp2'
        }
      },
      {
        'DeviceName': '/dev/xvdb',
        'VirtualName': 'vol1',
        'Ebs': {
          'DeleteOnTermination': False,
          'SnapshotId': 'snap-0fc8c2a86174ad86a',
          'VolumeSize': 16,
          'VolumeType': 'gp2'
        }
      },
      {
        'DeviceName': '/dev/xvdc',
        'VirtualName': 'vol2',
        'Ebs': {
          'DeleteOnTermination': False,
          'SnapshotId': 'snap-06c7304a47f9953f1',
          'VolumeSize': 32,
          'VolumeType': 'gp2'
        }
      }

    ],
    ImageId='ami-02dd77165c07f3843',
    InstanceType=instanceType,
    KeyName='awsajp_keypair',
    #PrivateIpAddress='10.0.0.146',
    MaxCount=1,
    MinCount=1,
    Monitoring={
      'Enabled': True
    },
    SecurityGroupIds=[
      'sg-032472680d0862c98',
    ],
    SubnetId=subnetId,
    TagSpecifications=[
      {
        'ResourceType': 'instance',
        'Tags': [
          {
            'Key': 'Name',
            'Value': 'StatefulEC2'
          },
        ]
      },
    ]

  )
  print("response={}".format((str(response))))

def attachEBSVolumetoEC2Instance(instanceId, volumeId, deviceName):
  instance = ec2resource.Instance(instanceId)
  response = instance.attach_volume(
    Device=deviceName,
    VolumeId=volumeId
  )
  #result = ec2client.attach_volume(volumeId, instanceId, "/dev/xvdb")
  #print("Attach Volume Result: {}".format(result))

def createLaunchTemplate():

  message = open("user-data.txt", "r").read()
  message_bytes = message.encode('ascii')
  base64_bytes = base64.b64encode(message_bytes)
  base64_message = base64_bytes.decode('ascii')

  response = ec2client.create_launch_template(
    LaunchTemplateName='ec2-fleet-lt-stateful-demo2',
    VersionDescription='V1',
    LaunchTemplateData={
      'EbsOptimized': True,
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
            'VolumeSize': 16,
            'VolumeType': 'gp2'
          }
        },
        {
          'DeviceName': '/dev/xvdc',
          'Ebs': {
            'DeleteOnTermination': False,
            'VolumeSize': 32,
            'VolumeType': 'gp2'
          }
        },
      ],

      'ImageId': 'ami-0323c3dd2da7fb37d',
      'InstanceType': 't3.large',
      'KeyName': 'awsajp_keypair',
      'Monitoring': {
        'Enabled': True
      },
      'UserData': base64_message,
      'TagSpecifications': [
        {
          'ResourceType': 'instance',
          'Tags': [
            {
              'Key': 'Name',
              'Value': 'ec2-fleet-lt-stateful-demo'
            },
          ]
        },
      ]
    }
  )

  print(json.dumps(response, indent=2, default=json_util.default))
  #print("response={}".format((str(response))))

  return response['LaunchTemplate']['LaunchTemplateId']

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
            'VolumeSize': 16,
            'SnapshotId': snapshotId1,
            'VolumeType': 'gp2'
          }
        },
        {
          'DeviceName': '/dev/xvdc',
          'Ebs': {
            'DeleteOnTermination': False,
            'VolumeSize': 32,
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
  print(json.dumps(response, indent=2, default=json_util.default))
  FleetId = response['FleetId']
  InstanceType = response['Instances'][0]['LaunchTemplateAndOverrides']['Overrides']['InstanceType']
  InstanceId = response['Instances'][0]['InstanceIds'][0]
  subnetId = response['Instances'][0]['LaunchTemplateAndOverrides']['Overrides']['SubnetId']
  print("InstanceType={} subnetId={}".format(InstanceType,subnetId))
  return InstanceId


  #print("response={}".format((str(response))))
def createDynamoTable():

  response = dbclient.create_table(
    AttributeDefinitions=[
      {
        'AttributeName': 'InstanceId',
        'AttributeType': 'S'
      },
      {
        'AttributeName': 'ST',
        'AttributeType': 'S'
      },

    ],
    TableName='InstancesTable',
    KeySchema=[
      {
        'AttributeName': 'InstanceId',
        'KeyType': 'HASH'
      },
    ],
    GlobalSecondaryIndexes=[
      {
        'IndexName': 'ST-Global-Index',
        'KeySchema': [
          {
            'AttributeName': 'ST',
            'KeyType': 'HASH'
          },
        ],
        'Projection': {
          'ProjectionType': 'ALL'
        },
        'ProvisionedThroughput': {
          'ReadCapacityUnits': 10,
          'WriteCapacityUnits': 10
        }
      },
    ],
    BillingMode='PROVISIONED',
    ProvisionedThroughput={
      'ReadCapacityUnits': 10,
      'WriteCapacityUnits': 10
    },
    Tags=[
      {
        'Key': 'Name',
        'Value': 'InstancesTable'
      },
    ]
  )

  print(json.dumps(response, indent=2, default=json_util.default))

def putItemsinDBTable():
  table = dynamodbresource.Table('InstancesTable')
  response = table.put_item(
    Item={
      'InstanceId': 'i-03af99d353d07c0a3',
      'ST': 'FREE',
      'VolumeIds': 'vol-1,vol-2,vol-3',
      'SnapshotIds': 'sp-1,sp-2,sp-3',
      'IP': '1.1.1.1',
      'subnetId': 'subnet-01e89d5cc1b12f515'
    }
  )
  print(json.dumps(response, indent=2, default=json_util.default))

if __name__ == '__main__':
  print("Starting the Statefull workload ...")

  volumes_dict= {
    'rootvolume' : 'vol-07770c367e2baa282'
  }

  #snapshotId = createSnapshot(volumes_dict)
  #print("snapshotId={}".format(snapshotId))
  #snapshotId = createSnapshot(volumes_dict)
  #print("snapshotId={}".format(snapshotId))

  #snapshotId='snap-0f96d940d7cc0d3af'
  #AMIId = createAMIfromSnapshot(snapshotId)

  #createDynamoTable()
  #putItemsinDBTable()
  #launchTemplateId=createLaunchTemplate()
  launchTemplateId = 'lt-03ca5a44acf2af90a'
  #print("launchTemplateId={}".format(launchTemplateId))
  #launchTemplateId=()
  provisionEC2Instances(launchTemplateId, 2)
  #response = ec2client.delete_launch_template_versions(
  #    LaunchTemplateId=launchTemplateId,
  #    Versions=[
  #        '2',
  #    ]
  #)

  #launchTemplateId='lt-033517d1a06af3611'
  #createEC2Fleet(launchTemplateId)
  #(instanceType, InstanceId, subnetId) = createEC2Fleet(launchTemplateId)
  #createLaunchTemplate()
  #createEC2Instance(instanceType, )
  #volumeId="vol-06aa4fed8807d0fcb"
  #instanceId="i-0bb7cb4b4cdab0267"
  #deviceName="/dev/xvdc"
  #attachEBSVolumetoEC2Instance(instanceId, volumeId, deviceName)
  #res = {'test': "test1"}
  #response={'Groups': [], 'Instances': [{'AmiLaunchIndex': 0, 'ImageId': 'ami-0323c3dd2da7fb37d', 'InstanceId': 'i-026bb75f4bdd1e53a', 'InstanceType': 't2.medium', 'KeyName': 'awsajp_keypair', 'LaunchTime': datetime.datetime(2020, 6, 23, 6, 42, 40, tzinfo=tzlocal()), 'Monitoring': {'State': 'pending'}, 'Placement': {'AvailabilityZone': 'us-east-1a', 'GroupName': '', 'Tenancy': 'default'}, 'PrivateDnsName': 'ip-10-0-0-202.ec2.internal', 'PrivateIpAddress': '10.0.0.202', 'ProductCodes': [], 'PublicDnsName': '', 'State': {'Code': 0, 'Name': 'pending'}, 'StateTransitionReason': '', 'SubnetId': 'subnet-0c07359b41da1e17c', 'VpcId': 'vpc-0b2cfd7b526d5b41a', 'Architecture': 'x86_64', 'BlockDeviceMappings': [], 'ClientToken': '', 'EbsOptimized': False, 'Hypervisor': 'xen', 'NetworkInterfaces': [{'Attachment': {'AttachTime': datetime.datetime(2020, 6, 23, 6, 42, 40, tzinfo=tzlocal()), 'AttachmentId': 'eni-attach-0083e6761e3c33f6d', 'DeleteOnTermination': True, 'DeviceIndex': 0, 'Status': 'attaching'}, 'Description': '', 'Groups': [{'GroupName': 'default', 'GroupId': 'sg-032472680d0862c98'}], 'Ipv6Addresses': [], 'MacAddress': '02:34:3b:09:03:d5', 'NetworkInterfaceId': 'eni-0945de3e545137047', 'OwnerId': '000474600478', 'PrivateDnsName': 'ip-10-0-0-202.ec2.internal', 'PrivateIpAddress': '10.0.0.202', 'PrivateIpAddresses': [{'Primary': True, 'PrivateDnsName': 'ip-10-0-0-202.ec2.internal', 'PrivateIpAddress': '10.0.0.202'}], 'SourceDestCheck': True, 'Status': 'in-use', 'SubnetId': 'subnet-0c07359b41da1e17c', 'VpcId': 'vpc-0b2cfd7b526d5b41a', 'InterfaceType': 'interface'}], 'RootDeviceName': '/dev/xvda', 'RootDeviceType': 'ebs', 'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-032472680d0862c98'}], 'SourceDestCheck': True, 'StateReason': {'Code': 'pending', 'Message': 'pending'}, 'Tags': [{'Key': 'Name', 'Value': 'StatefulEC2'}], 'VirtualizationType': 'hvm', 'CpuOptions': {'CoreCount': 2, 'ThreadsPerCore': 1}, 'CapacityReservationSpecification': {'CapacityReservationPreference': 'open'}, 'MetadataOptions': {'State': 'pending', 'HttpTokens': 'optional', 'HttpPutResponseHopLimit': 1, 'HttpEndpoint': 'enabled'}}], 'OwnerId': '000474600478', 'ReservationId': 'r-0fcc0499bd20dac5c', 'ResponseMetadata': {'RequestId': 'db6a396b-85d9-4ce3-a141-356d9619f48f', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'db6a396b-85d9-4ce3-a141-356d9619f48f', 'content-type': 'text/xml;charset=UTF-8', 'content-length': '4918', 'vary': 'accept-encoding', 'date': 'Tue, 23 Jun 2020 06:42:40 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}

  #print(response['Instances'])
  #print(response)
  #json_string = json.loads(str(response))
  #print(json_string)
  #with open("test") as metrics_file:
  #   metrics = json.load(metrics_file)

  #print("json_string={}".format(json_string))
  #print(type(metrics))
  #print(metrics['Instances'])




