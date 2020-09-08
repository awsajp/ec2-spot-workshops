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




CWTEventRule=os.getenv('CWT_EVENT_RULE_NAME')

UseExistingCluster=os.getenv('USE_EXISTING_CLUSTER')
ExistingClusterInstanceTag=os.getenv('EXISTING_CLUSTER_INSTANCE_TAG')
vpcId=os.getenv('VPC_ID')
subnetIdsString=os.getenv('SUBNET_IDs_LIST')
ExistingLaunchTemplateId=os.getenv('EXISTING_LAUNCHTEMPLATE_ID')
ExistingLaunchTemplateVersion=os.getenv('EXISTING_LAUNCHTEMPLATE_VERSION')
InstanceProfile=os.getenv('EXISTING_INSTANCE_PROFILE')
NumberOfEBSVolumes=int(os.getenv('NUMBER_OF_EBS_VOLUMES'))
EBSVolumeDeviceNames=os.getenv('EBS_VOLUME_DEVICE_NAMES')
EBSVolumeDeviceSizes=os.getenv('EBS_VOLUME_DEVICE_SIZES')
EBSVolumeMountPaths=os.getenv('EBS_VOLUME_MOUNT_PATHS')
RootEBSAMIId=os.getenv('ROOT_EBS_AMI_ID')
BaseInstanceType=os.getenv('BASE_INSTANCE_TYPE')
InstanceTypes=os.getenv('INSTANCE_TYPES_LIST')
KeyPairName=os.getenv('KEY_PAIR_NAME')
RetainPrivateIP = os.getenv('RETAINPRIVATEIP')
OnDemandTargetCapacity=int(os.getenv('ONDEMANDTARGETCAPACITY'))
SpotTargetCapacity=int(os.getenv('SPOTTARGETCAPACITY'))
TotalTargetCapacity=int(os.getenv('TOTALTARGETCAPACITY'))
TargetGroupArn = os.getenv('TARGET_GROUP_ARN')


InstancesTableName=os.getenv('DYNAMODB_INSTANCEID_TABLE_NAME')
StatusIndexName=os.getenv('DYNAMODB_GSI_ST')
CFNStackName=os.getenv('CFN_STACK_NAME')
awsRegion=os.getenv('AWSREGION')


launchTemplateName=CFNStackName


#NumberOfEBSVolumes=int(NumberOfEBSVolumes)
EBSVolumeDeviceNamesList=EBSVolumeDeviceNames.split(',')
EBSVolumeDeviceSizesList=EBSVolumeDeviceSizes.split(',')
EBSVolumeMountPathsList=EBSVolumeMountPaths.split(',')
TagKeyValues = ExistingClusterInstanceTag.split('=')
TagKey   = TagKeyValues[0]
TagValue = TagKeyValues[1]


ec2client = boto3.client('ec2', region_name=awsRegion)
ec2resource = boto3.resource('ec2')
elbv2client = boto3.client('elbv2')
dbclient = boto3.client('dynamodb')
dynamodbresource = boto3.resource('dynamodb')
cwtclient = boto3.client('events')

pprint("InstancesTableName={}".format(InstancesTableName))
InstanceTable = dynamodbresource.Table(InstancesTableName)

lambdaclient = boto3.client('lambda')


def createSnapshotFromVolumeId(snapshotDescription, volumeId):

    try:
        pprint("Creating snapshot for volumeId={}...".format(volumeId))
        response = ec2client.create_snapshot(
            Description= snapshotDescription,
            VolumeId = volumeId,
            DryRun= False
        )
        print("response={}".format(str(response)))
        status_code = response['ResponseMetadata']['HTTPStatusCode']

        if status_code == 200:
            print("Creating snapshot for volumeId={} successfully".format(volumeId))
            snapshotId = response['SnapshotId']
            state = "SNAPSHOT_CREATE_SUCCESS"
            return state, snapshotId
        else:
            state = "SNAPSHOT_CREATE_FAILURE"
            return state, str(response)

    except Exception as e:
        pprint("createSnapshotFromVolumeId error in creating snapshot with message = {}".format(str(e)))
        state = "SNAPSHOT_CREATE_FAILURE"
        return state, str(e)

    return snapshotId

def createAMIfromSnapshot(snapshotId):


    try:
        print("Creating AMIId for snapshotId={}...".format(snapshotId))
        response = ec2client.register_image(
            Architecture='x86_64',
            BlockDeviceMappings=[
                {
                    'DeviceName': EBSVolumeDeviceNamesList[0],
                    'Ebs': {
                        'DeleteOnTermination': False,
                        'SnapshotId': snapshotId,
                        'VolumeSize': int(EBSVolumeDeviceSizesList[0]),
                        'VolumeType': 'gp2'
                    }
                }
            ],
            Description='Description for Root Volume',
            RootDeviceName=EBSVolumeDeviceNamesList[0],
            Name="RootVolume-"+snapshotId
        )
        #print(json.dumps(response, indent=2, default=json_util.default))
        #print(json.dumps(response, indent=2))
        status_code = response['ResponseMetadata']['HTTPStatusCode']

        if status_code == 200:
            print("Created AMIId={} for snapshotId={} successfully".format(AMIId, snapshotId))
            AMIId = response['ImageId']
            state = "AMI_CREATE_SUCCESS"
            return state, AMIId
        else:
            state = "AMI_CREATE_FAILURE"
            return state, str(response)

    except Exception as e:
        pprint("createAMIfromSnapshot error in creating AMI with message = {}".format(str(e)))
        state = "AMI_CREATE_FAILURE"
        return state, str(e)


def createLaunchTemplate():

    try:
        #response = ec2client.delete_launch_template(
        #    LaunchTemplateName=launchTemplateName
        #)

        #pprint("type={}".format(type(NumberOfEBSVolumes)))

        pprint("createLaunchTemplate Creating the launchTemplate")
        InputFile = "user-data.txt"
        OutputFile = "/tmp/OutputFile.txt"

        with open(InputFile, "rt") as fin:
            with open(OutputFile, "wt") as fout:
                for line in fin:
                    line = line.replace('EBS_VOLUM2_MOUNT_PATH', EBSVolumeMountPathsList[1])
                    line = line.replace('EBS_VOLUM3_MOUNT_PATH', EBSVolumeMountPathsList[2])
                    fout.write(line)

        fin.close()
        fout.close()
        message = open(OutputFile, "r").read()
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        BlockDeviceMappings=[]

        for EBSVolume in range(0, NumberOfEBSVolumes):

            pprint("EBSVolume={} EBSVolumeDeviceName={} EBSVolumeDeviceSize={} EBSVolumeMountPath={}".format(EBSVolume, EBSVolumeDeviceNamesList[EBSVolume], EBSVolumeDeviceSizesList[EBSVolume], EBSVolumeMountPathsList[EBSVolume]))

            BlockDeviceMappings.append( {
                'DeviceName': EBSVolumeDeviceNamesList[EBSVolume],
                'Ebs': {
                    'DeleteOnTermination': False,
                    'VolumeSize': int(EBSVolumeDeviceSizesList[EBSVolume]),
                    'VolumeType': 'gp2'
                }
            })

        #pprint("BlockDeviceMappings={} launchTemplateName={}".format(BlockDeviceMappings, launchTemplateName))

        response = ec2client.create_launch_template(
            LaunchTemplateName=launchTemplateName,
            VersionDescription='1',
            LaunchTemplateData={
                'EbsOptimized': True,
                'IamInstanceProfile': { 'Arn': InstanceProfile, },
                'BlockDeviceMappings': BlockDeviceMappings,
                'ImageId': RootEBSAMIId,
                'InstanceType': BaseInstanceType,
                'KeyName': KeyPairName,
                'Monitoring': { 'Enabled': True },
                'UserData': base64_message,
                'TagSpecifications': [
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': launchTemplateName
                            },
                            {
                                'Key': TagKey,
                                'Value': TagValue
                            },
                        ]
                    },
                ]
            }
        )

        #print(json.dumps(response, indent=2, default=json_util.default))
        #print("response={}".format((str(response))))

        launchTemplateId = response['LaunchTemplate']['LaunchTemplateId']
        pprint("createLaunchTemplate completed successfully. launchTemplateId={}".format(launchTemplateId))
        state = "LT_CREATE_SUCCESS"
        return state, launchTemplateId

    except Exception as e:
        pprint("createLaunchTemplate error in creating LT with message = {}".format(str(e)))
        state = "LT_CREATE_FAILURE"
        return state, str(e)


def createLaunchTemplateVersion(launchTemplateId, launchTemplateVersion, ImageId, subnetIdsList, IP):

    try:
        NetworkInterfaces=[]

        if IP is not None:
            PrivateIpAddresses=[]
            PrivateIpAddresses.append({'Primary': True,  'PrivateIpAddress': IP})
            NetworkInterfaces.append( { 'DeviceIndex': 0,  'PrivateIpAddresses': PrivateIpAddresses  }  )
            pprint("NetworkInterfaces={}".format(NetworkInterfaces))

        BlockDeviceMappings=[]

        BlockDeviceMappings.append( {
            'DeviceName': EBSVolumeDeviceNamesList[0],
            'Ebs': {
                'DeleteOnTermination': False,
                'VolumeType': 'gp2'
            }
        })

        for EBSVolume in range(1, NumberOfEBSVolumes):
            BlockDeviceMappings.append( {
                'DeviceName': EBSVolumeDeviceNamesList[EBSVolume],
                'Ebs': {
                    'DeleteOnTermination': False,
                    'SnapshotId': snapshotIdList[EBSVolume],
                    'VolumeType': 'gp2'
                }
            })

        pprint("createLaunchTemplateVersion BlockDeviceMappings={} launchTemplateId={} launchTemplateVersion={}".format(BlockDeviceMappings, launchTemplateId, launchTemplateVersion))

        response = ec2client.create_launch_template_version(
            LaunchTemplateId=launchTemplateId,
            SourceVersion=launchTemplateVersion,
            VersionDescription='v2',
            LaunchTemplateData={
                'BlockDeviceMappings':BlockDeviceMappings,
                'NetworkInterfaces': NetworkInterfaces,
                'ImageId': ImageId
            }
        )

        launchTemplateVersion = response['LaunchTemplateVersion']['VersionNumber']
        pprint("createLaunchTemplateVersion created new launchTemplateVersion={}".format(launchTemplateVersion))
        state = "LT_VERSION_CREATE_SUCCESS"
        return state, launchTemplateVersion

    except Exception as e:
        pprint("createLaunchTemplateVersion error in creating launchtemplate version = {}".format(str(e)))
        state = "LT_VERSION_CREATE_FAILURE"
        return state, str(e)





def createEC2Fleet(launchTemplateId, launchTemplateVersion,SubnetId,TotalTargetCapacity,OnDemandTargetCapacity,SpotTargetCapacity):

    try:
        pprint("createEC2Fleet starting launchTemplateId={} launchTemplateVersion={} SubnetId={} TotalTargetCapacity={} OnDemandTargetCapacity={} SpotTargetCapacity={}".format(launchTemplateId, launchTemplateVersion, SubnetId, TotalTargetCapacity, OnDemandTargetCapacity, SpotTargetCapacity))
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
            Type='instant'
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

        response = ec2client.describe_fleets(FleetIds=[FleetId])
        #print("updateInstanceStatusInDynamoDB  response={}".format(str(response)))
        ActivityStatus = response['Fleets'][0]['ActivityStatus']
        Errors = response['Fleets'][0]['Errors']

        if Errors != []:
            pprint("createEC2Fleet error in launching EC2 instances with the message {}".format(str(e)))
            state = "FLEET_CREATE_FAILURE"
            return state, str(e)

        FleetState = response['Fleets'][0]['FleetState']
        FulfilledCapacity = response['Fleets'][0]['FulfilledCapacity']
        FulfilledOnDemandCapacity = response['Fleets'][0]['FulfilledOnDemandCapacity']
        InstanceList = response['Fleets'][0]['Instances']
        pprint("EC2FleetId={} ActivityStatus={} Errors={} FulfilledCapacity={} InstanceList={}".format(FleetId, ActivityStatus, Errors, FulfilledCapacity, InstanceList))

        for instanceData in InstanceList:

            Lifecycle = instanceData['Lifecycle']
            InstanceIds = instanceData['InstanceIds']
            waiter = ec2client.get_waiter('system_status_ok')
            pprint("Waiting for the InstanceId={} state to become running".format(InstanceIds))
            waiter.wait(InstanceIds=InstanceIds)
            describeInstance = ec2client.describe_instances(InstanceIds=InstanceIds)
            pprint(describeInstance)
            #print(json.dumps(describeInstance, indent=2, default=json_util.default))
            InstancesDescription = describeInstance['Reservations'][0]['Instances']
            updateInstanceDataInDynamoDB(Lifecycle, InstancesDescription)

            #return FleetId
        #state = "INSTANCE_CREATE_FAILURE"

        pprint("createEC2Fleet created EC2 fleet={} successfully and updated the instance state in the dynamodb".format(FleetId))
        state = "FLEET_CREATE_SUCCESS"
        return state, str(e)

    except Exception as e:
        pprint("createEC2Fleet error in creating the EC2 Fleet with message={}".format(str(e)))
        state = "FLEET_CREATE_FAILURE"
        return state, str(e)


def updateInstanceDataInDynamoDB(Lifecycle, InstancesDescription):

    pprint("updateInstanceDataInDynamoDB starting Lifecycle={}".format(Lifecycle))

    try:

        for InstanceData in InstancesDescription:

            InstanceId = InstanceData['InstanceId']
            ImageId = InstanceData['ImageId']
            InstanceType = InstanceData['InstanceType']
            IP = InstanceData['PrivateIpAddress']
            SubnetId = InstanceData['SubnetId']
            #Lifecycle ='on-demand'
            AZ = InstanceData['Placement']['AvailabilityZone']
            volumeIdList =[]
            for EBSVolume in InstanceData['BlockDeviceMappings']:
                volumeIdList.append(EBSVolume['Ebs']['VolumeId'])

            volumeIds=','.join(volumeIdList)
            pprint("volumeIds={}".format(volumeIds))
            #table = dynamodbresource.Table(InstanceTable)
            pprint("Adding InstanceId={} details to the dynamodb".format(InstanceId))
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

            if UseExistingCluster == "NO" and TargetGroupArn != "INVALID":
                pprint("Registering the  InstanceId={}  to the TG={}".format(InstanceId, TargetGroupArn))
                registerTargets = elbv2client.register_targets(TargetGroupArn=TargetGroupArn,Targets=[{'Id':InstanceId}])

        pprint("updateInstanceDataInDynamoDB ended successfully for Lifecycle={}".format(Lifecycle))
        state = "UPDATE_DB_FAILURE"
        return state, str(e)
    except Exception as e:
        pprint("updateInstanceDataInDynamoDB failed with error={}".format(str(e)))
        state = "UPDATE_DB_FAILURE"
        return state, str(e)


def updateInstanceIdInDynamoDB(InstanceId):
    pprint("Running updateInstanceIdInDynamoDB for InstanceId={}".format(InstanceId))
    InstanceIds = [InstanceId]
    for InstanceId in InstanceIds:
        pprint("Waiting for the InstanceId={} state to become running".format(InstanceId))
        waiter = ec2client.get_waiter('system_status_ok')
        waiter.wait(InstanceIds=[InstanceId])
        describeInstance = ec2client.describe_instances(InstanceIds=[InstanceId])
        #print(json.dumps(describeInstance, indent=2, default=json_util.default))
        InstanceData = describeInstance['Reservations'][0]['Instances'][0]
        ImageId = InstanceData['ImageId']
        InstanceType = InstanceData['InstanceType']
        IP = InstanceData['PrivateIpAddress']
        SubnetId = InstanceData['SubnetId']
        Lifecycle ='on-demand'
        AZ = InstanceData['Placement']['AvailabilityZone']
        volumeIds=""
        for EBSVolume in InstanceData['BlockDeviceMappings']:
            volumeIds=volumeIds+','+EBSVolume['Ebs']['VolumeId']


        #rootvolume = InstanceData['BlockDeviceMappings'][0]['Ebs']['VolumeId']
        #volume1    = InstanceData['BlockDeviceMappings'][1]['Ebs']['VolumeId']
        #volume2    = InstanceData['BlockDeviceMappings'][2]['Ebs']['VolumeId']
        #volumeIds = rootvolume +','+volume1+','+volume2
        pprint("volumeIds={}".format(volumeIds))
        #table = dynamodbresource.Table(InstanceTable)
        pprint("Adding InstanceId={} details to the dynamodb".format(InstanceId))
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

def updateInstanceStatusInDynamoDB(EC2FleetId):

    pprint("Running updateInstanceStatusInDynamoDB for EC2FleetId={}".format(EC2FleetId))
    response = ec2client.describe_fleets(FleetIds=[EC2FleetId])
    pprint("updateInstanceStatusInDynamoDB  response={}".format(str(response)))
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

            #TG = os.getenv('TARGET_GROUP_ARN')
            #print("Registering the  InstanceId={}  to the TG={}".format(InstanceId, TG))
            #registerTargets = elbv2client.register_targets(TargetGroupArn=TG,Targets=[{'Id':InstanceId}])



def handleNodeTermination(InstanceId):

    try:
        print("handleNodeTermination for InstanceId={}".format(InstanceId))
        response = InstanceTable.get_item(Key={'InstanceId': InstanceId})

        if 'Item' in response.keys():

            volumeIds = response['Item']['VolumeIds']
            IP = response['Item']['IP']
            AZ = response['Item']['AZ']
            SubnetId = response['Item']['SubnetId']

            print("volumeIds={} IP={} AZ={} SubnetId={}".format(volumeIds, IP, AZ, SubnetId))
            volumeIdList = volumeIds.split(',')
            print("volumeIdList={}".format(volumeIdList))
            snapshotIdList = []
            #snapshotIdList = ['snap-0dc28ed9b1f9340b2', 'snap-0205816f16095d95d', 'snap-0618f90e026b30562']


            for index, volumeId in enumerate(volumeIdList):
                print("volumeId={}".format(volumeId))
                state, snapshotId=createSnapshotFromVolumeId("volume"+str(index), volumeId)
                if "SUCCESS" in state:
                    snapshotIdList.append(snapshotId)
                else:
                    message = snapshotId
                    pprint("handleNodeTermination:createSnapshotFromVolumeId failed with message={}".format(message))
                    state = "TERMINATION_HANLDER_FAILURE"
                    return state, message

            snapshotIds = ','.join(snapshotIdList)
            print("Waiting for the snapshotIdList={} snapshotIds={} to be completed".format(snapshotIdList, snapshotIds))

            time.sleep(30)
            waiter = ec2client.get_waiter('snapshot_completed')
            waiter.wait(SnapshotIds=snapshotIdList)

            state, AMIId = createAMIfromSnapshot(snapshotIdList[0])
            if "SUCCESS" in state:
                waiter = ec2client.get_waiter('image_available')
                waiter.wait(ImageIds=[AMIId])
            else:
                message = AMIId
                pprint("handleNodeTermination:createAMIfromSnapshot failed with message={}".format(message))
                state = "TERMINATION_HANLDER_FAILURE"
                return state, message

                #launchTemplateId='lt-03ca5a44acf2af90a'

            if RetainPrivateIP == "NO":
                SubnetId=subnetIdsString
                IP =  None

            launchTemplateVersion = '1'
            response = InstanceTable.get_item(Key={'InstanceId': 'launchTemplateData'})

            if 'Item' in response.keys():
                launchTemplateId = response['Item']['LaunchTemplateId']
            else:
                message = "launchTemplateData Doesn't Exist in DynamoDB"
                pprint("handleNodeTermination failed with message={}".format(message))
                state = "TERMINATION_HANLDER_FAILURE"
                return state, message


            print("Creating a new LaunchTemplate Version with launchTemplateId={}  IP={} RetainPrivateIP={} to be completed".format(launchTemplateId, IP, RetainPrivateIP))
            state, launchTemplateVersion = createLaunchTemplateVersion(launchTemplateId, launchTemplateVersion, AMIId, snapshotIdList, IP)
            if "SUCCESS" in state:
                launchTemplateVersion = '$Latest'
            else:
                message = launchTemplateVersion
                pprint("handleNodeTermination:createLaunchTemplateVersion failed with message={}".format(message))
                state = "TERMINATION_HANLDER_FAILURE"
                return state, message

                #EC2FleetId = createEC2Fleet(launchTemplateId, launchTemplateVersion, subnetId)

            OnDemandTargetCapacity=1
            SpotTargetCapacity=0
            TotalTargetCapacity=1


            pprint("createEC2Fleet with launchTemplateId={} launchTemplateVersion={} SubnetId={}".format(launchTemplateId, launchTemplateVersion, SubnetId))
            state, EC2FleetId = createEC2Fleet(launchTemplateId,launchTemplateVersion,SubnetId,TotalTargetCapacity,OnDemandTargetCapacity,SpotTargetCapacity)
            if "SUCCESS" in state:
                for volumeId in volumeIdList:
                    print("Deleting the volumeId={}".format(volumeId))
                    response = ec2client.delete_volume( VolumeId=volumeId )

                print("Deleting the Old InstanceId={} from dynamodb".format(InstanceId))
                response = InstanceTable.delete_item( Key={ 'InstanceId': InstanceId  }  )
            else:
                message = launchTemplateVersion
                pprint("handleNodeTermination:createLaunchTemplateVersion failed with message={}".format(message))
                state = "TERMINATION_HANLDER_FAILURE"
                return state, message

                #updateInstanceStatusInDynamoDB(EC2FleetId)

            #print("Deregistering the AMI={} to be completed".format(AMIId))
            #response = ec2client.deregister_image(
            #  ImageId=AMIId
            #)

            #for snapshotId in snapshotIdList:
            #  print("Deleting the snapshotId={} to be completed".format(snapshotId))
            #  response = ec2client.delete_snapshot(
            #    SnapshotId=snapshotId
            #  )

            pprint("handleNodeTermination completed successfully for InstanceId={}".format(InstanceId))
            state = "TERMINATION_HANLDER_SUCCESS"
            message = "SUCCESS"
            return state, message

        else:
            message = "InstanceId Doesn't Exist in DynamoDB"
            print("handleNodeTermination failed with message={}".format(message))
            state = "TERMINATION_HANLDER_FAILURE"
            return state, message

    except Exception as e:
        pprint("handleNodeTermination failed for InstanceId={} with error={}".format(InstanceId, str(e)))
        state = "TERMINATION_HANLDER_FAILURE"
        return state, str(e)

def createSnapshots(InstanceId):

    print("createSnapshots for InstanceId={}".format(InstanceId))

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
        #snapshotIdList = ['snap-0fc6d23769bedf5ff', 'snap-0987320f1d5c08daa', 'snap-02d91eb0f597dc8bc']
        #time.sleep(45)

        for index, volumeId in enumerate(volumeIdList):
            print("volumeId={}".format(volumeId))
            snapshotId=createSnapshotFromVolumeId("volume"+str(index), volumeId)
            snapshotIdList.append(snapshotId)

        print("snapshotIdList={}".format(snapshotIdList))

def updateExistingClusterinDynamoDB(ExistingClusterInstanceTag):
    try:
        pprint("ExistingClusterInstanceTag={}".format(ExistingClusterInstanceTag))
        #TagKeyValues = ExistingClusterInstanceTag.split('=')
        #key = TagKeyValues[0]
        #value = TagKeyValues[1]
        pprint("TagKey={} TagValue={}".format(TagKey, TagValue))
        response = ec2client.describe_instances(Filters=[{'Name': 'tag:'+TagKey,'Values':[TagValue]}])
        #pprint(response)
        InstancesDescription= response['Reservations'][0]['Instances']
        pprint("number of instances={}".format(len(InstancesDescription)))
        Lifecycle = 'on-demand'
        state, message = updateInstanceDataInDynamoDB(Lifecycle, InstancesDescription)
        if "SUCCESS" in state:
            pprint("updateInstanceDataInDynamoDB completed successfully with message={}".format(message))
            state = "CLUSTER_HANLDER_SUCCESS"
        else:
            pprint("updateInstanceDataInDynamoDB completed successfully with message={}".format(message))
            state = "CLUSTER_HANLDER_FAILURE"
            return state, message

    except Exception as e:
        pprint("updateExistingClusterinDynamoDB failed with message={}".format(str(e)))
        state = "CLUSTER_HANLDER_FAILURE"
        return state, str(e)

def CleanupClusterResources():


    try:



        #response = cwtclient.enable_rule(
        #    Name=CWTEventRule
        #)
        #pprint("response={}".format(response))
        key   = "ClusterName"
        value = CFNStackName
        pprint("TagKey={} TagValue={}".format(TagKey, TagValue))
        response = ec2client.describe_instances(Filters=[{'Name': 'tag:'+TagKey,'Values':[TagValue]}, {'Name': 'instance-state-name', 'Values': ['running']} ])
        #pprint(response)
        InstancesDescription=[]
        if response['Reservations'] != []:
            InstancesDescription= response['Reservations'][0]['Instances']
        else:
            pprint("There are no instances to delete.")

        if UseExistingCluster == "NO":
            pprint("Disabling the CWTEventRule={}".format(CWTEventRule))
            response = cwtclient.disable_rule( Name=CWTEventRule   )
            time.sleep(5)

        for InstanceData in InstancesDescription:

            InstanceId = InstanceData['InstanceId']
            print("Deleting the InstanceId={} from dynamodb".format(InstanceId))
            response = InstanceTable.delete_item( Key={ 'InstanceId': InstanceId } )

            if UseExistingCluster == "NO":
                pprint("Terminating the EC2 InstanceId={}".format(InstanceId))
                response = ec2client.terminate_instances( InstanceIds=[ InstanceId ], )

        response = ec2client.describe_launch_templates(LaunchTemplateNames=[launchTemplateName])
        if response['LaunchTemplates'] != []:
            pprint("Deleting the launchTemplateName={}".format(launchTemplateName))
            response = ec2client.delete_launch_template( LaunchTemplateName=launchTemplateName )

        print("Deleting the launchTemplateData from dynamodb")
        response = InstanceTable.delete_item( Key={ 'InstanceId': 'launchTemplateData' } )

    except Exception as e:
        pprint("CleanupClusterResources failed with message={}".format(str(e)))
        state = "CLEANUP_HANLDER_FAILURE"
        return state, str(e)

def lambda_handler(event, context):
    # TODO implement

    if 'RequestType' in event.keys():
        if event['RequestType'] == "Create":

            response = cwtclient.enable_rule( Name=CWTEventRule )
            time.sleep(10)

            try:
                response = InstanceTable.get_item(Key={'InstanceId': 'launchTemplateData'})

                if 'Item' in response.keys():
                    launchTemplateId = response['Item']['LaunchTemplateId']
                    launchTemplateVersion = response['Item']['LaunchTemplateVersion']
                    pprint("launchTemplateData found in dynamodb. launchTemplateId={} launchTemplateVersion={}".format(launchTemplateId, launchTemplateVersion))
                else:
                    pprint("ExistingLaunchTemplateId={} ExistingLaunchTemplateVersion={}".format(ExistingLaunchTemplateId, ExistingLaunchTemplateVersion))
                    if ExistingLaunchTemplateId is not None:
                        launchTemplateId = ExistingLaunchTemplateId
                        if ExistingLaunchTemplateVersion is not None:
                            launchTemplateVersion = ExistingLaunchTemplateVersion
                        else:
                            launchTemplateVersion = '1'
                    else:
                        state, launchTemplateId = createLaunchTemplate()
                        if "SUCCESS" in state:
                            launchTemplateVersion = '1'
                        else:
                            message = launchTemplateId
                            pprint("Error occured while processing the event={} with error={}".format(event, launchTemplateId))


                    pprint("Adding launchTemplateId=%d launchTemplateName={} launchTemplateVersion={}".format(launchTemplateName, launchTemplateId, launchTemplateVersion))
                    response = InstanceTable.put_item(
                        Item={
                            'InstanceId': 'launchTemplateData',
                            'launchTemplateName': launchTemplateName,
                            'launchTemplateId': launchTemplateId,
                            'launchTemplateVersion': launchTemplateVersion
                        }
                    )

                if UseExistingCluster == "YES":
                    state, message = updateExistingClusterinDynamoDB(ExistingClusterInstanceTag)
                    if "SUCCESS" in state:
                        launchTemplateVersion = '1'
                    else:
                        pprint("Error occured while processing the event={} with message={}".format(event, message))
                else:

                    #pprint("NumberOfEBSVolumes={}".format(NumberOfEBSVolumes))
                    #response = lambdaclient.update_function_configuration(
                    #  FunctionName='arn:aws:lambda:ap-south-1:140518057739:function:Ec2SpotState-InitFunction',
                    #  Environment={
                    #      'Variables': {
                    #          'LAUNCH_TEMPLATE_ID': 'testValue'
                    #      }
                    #    }
                    #)
                    #pprint(response)
                    #launchTemplateId=os.getenv('LAUNCH_TEMPLATE_ID')
                    #pprint("launchTemplateId={}".format(launchTemplateId))

                    #try:
                    #  response = InstanceTable.get_item(Key={'InstanceId': 'launchTemplateData'})
                    #except ClientError as e:
                    #  print(e.response['Error']['Message'])

                    #if 'Item' in response.keys():

                    #  launchTemplateId = response['Item']['LaunchTemplateId']
                    #else:
                    #  launchTemplateId = createLaunchTemplate()
                    #return {
                    #  'statusCode': 200,
                    #  'body': json.dumps("Completed processing of the event={}".format(event))
                    #}


                    #pprint("vpcId={}".format(vpcId))
                    response = ec2client.describe_security_groups(    Filters=[ { 'Name': 'vpc-id',  'Values': [ vpcId, ] }, { 'Name': 'group-name',  'Values': [ 'default', ] }  ],)
                    #pprint("vpcId={} response={}".format(vpcId, response))
                    securityGroupId= response['SecurityGroups'][0]['GroupId']
                    pprint("Adding ingress rule for prort 80 for securityGroupId={} vpcId={}".format(securityGroupId, vpcId))
                    #data = ec2client.authorize_security_group_ingress(GroupId=securityGroupId,IpPermissions=[{'IpProtocol': 'tcp','FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},])



                    #launchTemplateVersion = '14'
                    #launchTemplateVersion = '1'
                    SubnetId=subnetIdsString
                    state, message = createEC2Fleet(launchTemplateId, launchTemplateVersion,SubnetId,TotalTargetCapacity,OnDemandTargetCapacity,SpotTargetCapacity)
                    if "SUCCESS" in state:
                        ppprint("createEC2Fleet completely successfully with FleetId={}".format(message))
                    else:
                        pprint("Error occured while processing the event={} with message={}".format(event, message))

            except Exception as e:
                pprint("Error occured while processing the event={} error={}. So Cleaning up Resources..".format(event, str(e)))
                CleanupClusterResources()

        elif event['RequestType'] == "Delete":
            CleanupClusterResources()
        elif event['RequestType'] == "Snapshot":
            InstanceId = event['InstanceId']
            createSnapshots(InstanceId)
        elif event['RequestType'] == "Update":
            InstanceId = event['InstanceId']
            updateInstanceIdInDynamoDB(InstanceId)
        else:
            print("CFN event RequestType={} is NOT handled currently".format(event['RequestType']))


        #responseData = {}
        #responseData['Data'] = '1'
        #cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData,"CustomResourcePhysicalID")
    else:
        InstanceId = event['detail']['instance-id']
        print("Received EC2 Instance State-change Notification InstanceId={}...".format(InstanceId))
        handleNodeTermination(InstanceId)

    return {
        'statusCode': 200,
        'body': json.dumps("Complered processing of the termination of the event={}".format(event))
    }
