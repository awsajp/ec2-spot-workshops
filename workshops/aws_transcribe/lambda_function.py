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
import urllib.request
import cfnresponse
#from bson import json_util


#TranscribeJobsStateTable=os.getenv('DYNAMODB_INSTANCEID_TABLE_NAME')
#StatusIndexName=os.getenv('DYNAMODB_GSI_ST')
TranscribeJobsStateTable=os.getenv('DYNAMODB_INSTANCEID_TABLE_NAME')
StatusIndexName=os.getenv('DYNAMODB_GSI_ST')
awsRegion=os.getenv('AWS_REGION')

ec2client = boto3.client('ec2', region_name=awsRegion)
ec2resource = boto3.resource('ec2')
elbv2client = boto3.client('elbv2')
dbclient = boto3.client('dynamodb')
dynamodbresource = boto3.resource('dynamodb')
table = dynamodbresource.Table(TranscribeJobsStateTable)
transcribe = boto3.client('transcribe')


  

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

      TG = os.getenv('TARGET_GROUP_ARN')
      print("Registering the  InstanceId={}  to the TG={}".format(InstanceId, TG))
      registerTargets = elbv2client.register_targets(TargetGroupArn=TG,Targets=[{'Id':InstanceId}])

def scheduleTranscribeJobs(job_name, job_uri, objectSize):

  print("scheduleTranscribeJobs job_name={} job_uri={}".format(job_name, job_uri))
  
  try:
    
    job_nam_split = job_name.split('.')
    MediaFormat = job_nam_split[-1]
    LanguageCode = 'en-US'
    response = transcribe.start_transcription_job( 
           TranscriptionJobName=job_name,    
           Media={'MediaFileUri': job_uri},    
           MediaFormat=MediaFormat,    
           LanguageCode=LanguageCode) 
    pprint(response)
    
    
    print("Adding job_name={} details to the dynamodb".format(job_name))
    resp = table.put_item(
      Item={
        'JobName': job_name,
        'ST': response['TranscriptionJob']['TranscriptionJobStatus'],
        'LanguageCode': response['TranscriptionJob']['LanguageCode'],
        'MediaFormat': response['TranscriptionJob']['MediaFormat'],
        'MediaFileUri': response['TranscriptionJob']['Media']['MediaFileUri'],
        "objectSize" : objectSize,
        'transcript': ""
      }
    )
  except Exception as e:
    #exception_message = "There was error in start_transcription_job \n" + job_name + str(e)
    print("exception_message={}".format(str(e)))
    waitforTranscribeJobs(job_name)
  
def handleTranscribeEvent(event):

  
  job_name = event['detail']['TranscriptionJobName']
  print("handleTranscribeEvent job_name={}".format(job_name))  
  state = event['detail']['TranscriptionJobStatus']
  transcript  = ""
  status = transcribe.get_transcription_job(TranscriptionJobName=job_name)

  if state == 'COMPLETED':
    response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    data = json.loads(response.read())
    transcript = data['results']['transcripts'][0]['transcript']
    
  print("Updating job_name={} state={} to dynamodbtablename".format(job_name, state))
  table.update_item(
    Key={
      'JobName': job_name
    },
    UpdateExpression='SET ST = :val1, transcript = :val2',
    ExpressionAttributeValues={
      ':val1': state,
      ':val2': transcript,
    }
  )
  
  

def handleS3ObjectUploadEvent(event):

  print("handleS3ObjectUploadEvent for event={}".format(event))
  time.sleep(10)
  #if event['Records'][0]['eventName'] == 'ObjectCreated:Put':
  objectName = event['Records'][0]['s3']['object']['key']
  objectSize = event['Records'][0]['s3']['object']['size']
  s3bucketname = event['Records'][0]['s3']['bucket']['name']
  job_uri='https://' + s3bucketname + '.s3.amazonaws.com/' + objectName
  job_name = objectName.replace('+', '')
  scheduleTranscribeJobs(job_name, job_uri, objectSize)
  waitforTranscribeJobs(job_name)
      
def waitforTranscribeJobs(job_name):

  print("waitforTranscribeJobs job_name={}".format(job_name))
  state = "NA"
  transcript  = "NA"
  while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    state = status['TranscriptionJob']['TranscriptionJobStatus']
    if state in ['COMPLETED', 'FAILED']:
      break    
    print("Not ready yet...")    
    time.sleep(10)
  
  if state == 'COMPLETED':
    response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    data = json.loads(response.read())
    transcript = data['results']['transcripts'][0]['transcript']
    #pprint (data)
    
    
  print("waitforTranscribeJobs updating job_name={} state={} to dynamodbtablename".format(job_name, state))
  table.update_item(
    Key={
      'JobName': job_name
    },
    UpdateExpression='SET ST = :val1, transcript = :val2',
    ExpressionAttributeValues={
      ':val1': state,
      ':val2': transcript,
    }
  )
  
  
def lambda_handler(event, context):
  # TODO implement

  if 'RequestType' in event.keys():
    if event['RequestType'] == "Create":
      pprint("Create Event={}".format(event))
    elif event['RequestType'] == "Delete":
      pprint("Delete Event={}".format(event))
    else:
      pprint("Invalid event={}".format(event))


    responseData = {}
    responseData['Data'] = '1'
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData,"CustomResourcePhysicalID")
    return {
      'statusCode': 200,
      'body': json.dumps("Completed processing of the event={}".format(event))
    }
  elif 'Records' in event.keys():
    pprint("S3 event={}".format(event))
    handleS3ObjectUploadEvent(event)    
  elif 'detail-type' in event.keys():
    pprint("Transcribe event={}".format(event))
    handleTranscribeEvent(event)
    


    return {
      'statusCode': 200,
      'body': json.dumps("Complered processing of the termination of the event={}".format(event))
    }
