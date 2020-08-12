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
from botocore.exceptions import ClientError
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


def scheduleTranscribeJobs(job_name, job_uri):

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
    
    state = response['TranscriptionJob']['TranscriptionJobStatus']
    print("scheduleTranscribeJobs Updating job_name={} state={} to dynamodbtablename".format(job_name, state))
    table.update_item(
      Key={
        'JobName': job_name
      },
      UpdateExpression='SET ST = :val1',
      ExpressionAttributeValues={
        ':val1': state
      }
    )
  except Exception as e:
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
  Sender = "AWS Interview Analytics System <jalawala@amazon.com>"
  
  # Replace recipient@example.com with a "To" address. If your account 
  # is still in the sandbox, this address must be verified.
  Recipient = ['jalawala@amazon.com']
  sendEmail(Sender, Recipient, job_name, state, transcript)  


def sendEmail(Sender, Recipient, job_name, State, Transcript):
  # Replace sender@example.com with your "From" address.
  # This address must be verified with Amazon SES.

  
  # Specify a configuration set. If you do not want to use a configuration
  # set, comment the following variable, and the 
  # ConfigurationSetName=CONFIGURATION_SET argument below.
  #CONFIGURATION_SET = "ConfigSet"
  
  # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
  AWS_REGION = "us-east-1"
  
  # The subject line for the email.
  SUBJECT = "Transcibe Job ({}) Status: {}".format(job_name, State)
  
  # The email body for recipients with non-HTML email clients.
  BODY_TEXT = "AWS Interview Transcription Job \r\n" + str(Transcript)
              
              
  # The HTML body of the email.
  BODY_HTML = "<html><head></head> <body>  <h1>AWS Interview Transcription Job Output</h1> <p>{}</p></body></html>".format(str(Transcript))

  # The character encoding for the email.
  CHARSET = "UTF-8"
  
  # Create a new SES resource and specify a region.
  client = boto3.client('ses',region_name=AWS_REGION)
  
  # Try to send the email.
  try:
      #Provide the contents of the email.
      response = client.send_email(
          Destination={
              'ToAddresses': Recipient,
          },
          Message={
              'Body': {
                  'Html': {
                      'Charset': CHARSET,
                      'Data': BODY_HTML,
                  },
                  'Text': {
                      'Charset': CHARSET,
                      'Data': BODY_TEXT,
                  },
              },
              'Subject': {
                  'Charset': CHARSET,
                  'Data': SUBJECT,
              },
          },
          Source=Sender,
          # If you are not using a configuration set, comment or delete the
          # following line
          #ConfigurationSetName=CONFIGURATION_SET,
      )
  # Display an error if something goes wrong.	
  except ClientError as e:
      print(e.response['Error']['Message'])
  else:
      print("Email sent! Message ID:"),
      print(response['MessageId'])
      
      

def handleS3ObjectUploadEvent(event):

  print("handleS3ObjectUploadEvent for event={}".format(event))
  time.sleep(10)
  #if event['Records'][0]['eventName'] == 'ObjectCreated:Put':
  objectName = event['Records'][0]['s3']['object']['key']
  objectSize = event['Records'][0]['s3']['object']['size']
  s3bucketname = event['Records'][0]['s3']['bucket']['name']
  job_uri='https://' + s3bucketname + '.s3.amazonaws.com/' + objectName
  job_name = objectName.replace('+', '')
  print("Adding job_name={} details to the dynamodb".format(job_name))
  job_nam_split = job_name.split('.')
  MediaFormat = job_nam_split[-1]
  LanguageCode = 'en-US'
    
  resp = table.put_item(
    Item={
      'JobName': job_name,
      'ST': 'NA',
      'LanguageCode': LanguageCode,
      'MediaFormat': MediaFormat,
      'MediaFileUri': job_uri,
      "objectSize" : objectSize,
      'transcript': "NA"
    }
  )  
  scheduleTranscribeJobs(job_name, job_uri)
  waitforTranscribeJobs(job_name)
      

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
    job_name = event['detail']['TranscriptionJobName']
    waitforTranscribeJobs(job_name)
    
    return {
      'statusCode': 200,
      'body': json.dumps("Complered processing of the termination of the event={}".format(event))
    }
