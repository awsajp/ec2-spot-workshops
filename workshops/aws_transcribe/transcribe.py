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
from botocore.exceptions import ClientError
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


ec2client = boto3.client('ec2', region_name='us-east-1')
ec2resource = boto3.resource('ec2')
dbclient = boto3.client('dynamodb')
dynamodbresource = boto3.resource('dynamodb')
transcribe = boto3.client('transcribe')
s3client = boto3.client('s3')
<<<<<<< HEAD
=======
dynamodbtablename='TranscribeJobs'
table = dynamodbresource.Table(dynamodbtablename)
AWSREGION = "us-east-1"
sesClient = boto3.client('ses',region_name=AWSREGION)

>>>>>>> df697205d6633c658d0f2e9722976b71ab2837de

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
    

def deleteTranscribeJobs(JobNameContains, MaxResults):

        
  print("below are list of transciption jobs")
  response = transcribe.list_transcription_jobs(
      JobNameContains=JobNameContains, 
      MaxResults=MaxResults
  )
  #pprint(response)
  JobSummaries=response['TranscriptionJobSummaries']
  print("Number of Jobs returned is {}".format((len(JobSummaries))))
  
  for job in JobSummaries:
    job_name = job['TranscriptionJobName']
    #pprint(job_name)
    print("Deleting the TranscriptionJobName {}".format(job_name))
    response = transcribe.delete_transcription_job(
        TranscriptionJobName=job_name
    )  
      
  
def deleteObjectsinS3Bucket(s3bucketname, PrefixName):
  #response = s3client.list_objects(
  #    Bucket=s3bucketname
  #)
  #pprint(response)  
  
  s3 = boto3.resource('s3')
  bucket = s3.Bucket(s3bucketname)
  for obj in bucket.objects.filter(Prefix=PrefixName):
      #s3.Object(bucket.name,obj.key).delete()  
      pprint("Deleting the Object={}".format((obj.key)))
      #s3.Object(bucket.name,obj.key).delete()

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
  TranscriptAttachmentFile = job_name +'.txt'
  TranscriptFile='/tmp/'+ TranscriptAttachmentFile
  #ranscriptFile=job_name +'.txt'
  file = open(TranscriptFile, 'a')
  file.write(transcript)
  file.close()
  
  Sender = "AWS Interview Analytics System <jalawala@amazon.com>"
  
  # Replace recipient@example.com with a "To" address. If your account 
  # is still in the sandbox, this address must be verified.
  Recipient = ['jalawala@amazon.com']
  #sendEmail(Sender, Recipient, job_name, state, transcript)
  sendEmailAsAttachment(Sender, Recipient, job_name, state, TranscriptFile, TranscriptAttachmentFile)

    
  #pprint(status)


def sendEmailAsAttachment(Sender, Recipient, job_name, State, TranscriptFile, TranscriptAttachmentFile):
  # Replace sender@example.com with your "From" address.
  # This address must be verified with Amazon SES.

  print("sendEmailAsAttachment Sender={} Recipient={} job_name={} State={} TranscriptFile={}".format(Sender, Recipient, job_name, State, TranscriptFile))
  SUBJECT = "Transcibe Job ({}) Status: {}".format(job_name, State)
  
  # The email body for recipients with non-HTML email clients.
  BODY_TEXT = "AWS Interview Transcription Job Output Attached"

  message = MIMEMultipart()
  message['Subject'] = SUBJECT
  message['From'] = Sender
  message['To'] = ', '.join(Recipient)# message body
  part = MIMEText(BODY_TEXT, 'html')
  message.attach(part)# attachment
  attachment_string=None
  if attachment_string:   # if bytestring available
      part = MIMEApplication(str.encode('attachment_string'))
  else:    # if file provided
      part = MIMEApplication(open(TranscriptFile, 'r').read())
  part.add_header('Content-Disposition', 'attachment', filename=TranscriptAttachmentFile)
  message.attach(part)
  
  response = sesClient.send_raw_email(
      Source=message['From'],
      Destinations=Recipient,
      RawMessage={
          'Data': message.as_string()
      }
  )


      
        
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
  #job_name='job4'
  #job_uri = 'https://s3bucketaudio.s3.amazonaws.com/IntroducingAWSCloudMapandAWSAppMesh.mp3'
  
  #startTranscribeJobs(s3bucketname)
  #job_name ='GettingstartedwithservicemeshAWSAppMesh.mp4'
  #waitforTranscribeJobs(job_name)
  #scheduleTranscribeJobs(job_name, job_uri)
  #waitforTranscribeJobs(job_name)

  #checkTranscribeJobs(job_name)
  #job_name='autiototext'
  #checkTranscribeJobs(job_name)
  #transcribeS3bucket(s3bucketname)
  
  JobNameContains='mp4'
  MaxResults=5
  #deleteTranscribeJobs(JobNameContains, MaxResults)
  s3bucketname='unicorngym-unicorngymsrecordings'
  PrefixName=''
  deleteObjectsinS3Bucket(s3bucketname, PrefixName)
  
  s3Srcbucketname='unicorngym-unicorngymsrecordings'
  PrefixName=''
  s3Dstbucketname='unicorngym-unicorngymsrecordings'
  deleteObjectsinS3Bucket(s3bucketname, PrefixName)  
  



