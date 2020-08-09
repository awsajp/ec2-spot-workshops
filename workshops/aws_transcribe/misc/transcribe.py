import os
import requests
import json
import time
import sys
import boto3
import datetime
import base64
import urllib.request
from pprint import pprint

ec2client = boto3.client('ec2', region_name='us-east-1')
ec2resource = boto3.resource('ec2')
dbclient = boto3.client('dynamodb')
dynamodbresource = boto3.resource('dynamodb')
transcribe = boto3.client('transcribe')
s3client = boto3.client('s3')
dynamodbtablename='TranscribeJobs'
table = dynamodbresource.Table(dynamodbtablename)


def checkTranscribeJobs(job_name):
  while True:
      status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
      if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
      print("Not ready yet...")
      time.sleep(10)
  pprint(status)
  if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    data = json.loads(response.read())
    pprint (data)
    #text = data['results']['transcripts'][0]['transcript']
    #print(text)  
    

def startTranscribeJobs(s3bucketname):
  response = s3client.list_objects(
      Bucket=s3bucketname
  )
  pprint(response)
  print("These are files in the S3 Bucket:{}".format(s3bucketname))
  for obj in response['Contents']:
    job_name=obj['Key']
    #pprint(obj['Key'])
    #job_uri='https://s3bucketaudio.s3.amazonaws.com/ContainerSummit+-+Containers+on+Spot.mp3'
    job_uri='https://' + s3bucketname + '.s3.amazonaws.com/' + job_name
    scheduleTranscribeJobs(job_name, job_uri)
    
  for obj in response['Contents']:
    job_name=obj['Key']
    waitforTranscribeJobs(job_name)

        
  #print("below are list of transciption jobs")
  #response = transcribe.list_transcription_jobs(
  #    JobNameContains='job'
  #)
  #pprint(response)  
  
  

def scheduleTranscribeJobs(job_name, job_uri):

  print("scheduleTranscribeJobs job_name={} job_uri={}".format(job_name, job_uri))
  
  try:
    
    response = transcribe.start_transcription_job( 
           TranscriptionJobName=job_name,    
           Media={'MediaFileUri': job_uri},    
           MediaFormat='mp3',    
           LanguageCode='en-US')
    pprint(response)
    
    
    print("Adding job_name={} details to the dynamodb".format(job_name))
    resp = table.put_item(
      Item={
        'JobName': job_name,
        'ST': response['TranscriptionJob']['TranscriptionJobStatus'],
        'LanguageCode': response['TranscriptionJob']['LanguageCode'],
        'MediaFormat': response['TranscriptionJob']['MediaFormat'],
        'MediaFileUri': response['TranscriptionJob']['Media']['MediaFileUri'],
        'transcript': ""
      }
    )
  except Exception as e:
    #exception_message = "There was error in start_transcription_job \n" + job_name + str(e)
    print("exception_message={}".format(str(e)))
  
  
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

    
  #pprint(status)

def createDynamoTable(dynamodbtablename):

  response = dbclient.create_table(
    AttributeDefinitions=[
      {
        'AttributeName': 'JobName',
        'AttributeType': 'S'
      },
      {
        'AttributeName': 'ST',
        'AttributeType': 'S'
      },

    ],
    TableName=dynamodbtablename,
    KeySchema=[
      {
        'AttributeName': 'JobName',
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
        'Value': dynamodbtablename
      },
    ]
  )

  pprint(response)
  #print(json.dumps(response, indent=2, default=json_util.default))
  

  
if __name__ == '__main__':
  print("Starting the Transcribe workload ...")
  
  #createDynamoTable(dynamodbtablename)
  
  #s3://s3bucketaudio/ContainerSummit+-+Containers+on+Spot.mp3
  s3bucketname = "s3bucketaudio"
  #scheduleTranscribeJobs(s3bucketname, file)
  #startTranscribeJobs(s3bucketname)
  job_name='job4'
  job_uri = 'https://s3bucketaudio.s3.amazonaws.com/IntroducingAWSCloudMapandAWSAppMesh.mp3'
  
  startTranscribeJobs(s3bucketname)
  #scheduleTranscribeJobs(job_name, job_uri)
  #waitforTranscribeJobs(job_name)

  #checkTranscribeJobs(job_name)
  #job_name='autiototext'
  #checkTranscribeJobs(job_name)
  #transcribeS3bucket(s3bucketname)
  
  



