import boto3
import json
import urllib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


AWSREGION = 'us-east-1'
sesClient = boto3.client('ses',region_name=AWSREGION)

dynamodbresource = boto3.resource('dynamodb')
tabletranscribeStatus = dynamodbresource.Table('transcribeStatus')
tableinterviewanalysis = dynamodbresource.Table('interview_analysis')

def updateStatus(username,filename,status):
  dynamodbresource = boto3.resource('dynamodb')
  table = dynamodbresource.Table('interview_analysis')
  
  table.update_item(
    Key={
       
        'filename': filename
    },
    UpdateExpression='SET job_status = :val1',
    ExpressionAttributeValues={
        ':val1': status
    }
  )

def updateTranscribeStatus(jobname,state,transcript):
  dynamodbresource = boto3.resource('dynamodb')
  table = dynamodbresource.Table('transcribeStatus')
  
  table.update_item(
    Key={
       
        'jobname': jobname
    },
     UpdateExpression='SET ST = :val1, transcript = :val2',
    ExpressionAttributeValues={
      ':val1': state,
      ':val2': transcript,
    }
  )


def getJobDetails(jobname):
  client = boto3.client('transcribe')
  response = client.get_transcription_job(
    TranscriptionJobName= jobname
    )
  print(response)
  jobstatus = response['TranscriptionJob']["TranscriptionJobStatus"]
  mediauri = response['TranscriptionJob']["Media"]["MediaFileUri"]
  filename = mediauri.split("/")[-1]
  userid = mediauri.split("/")[-2]
  print(filename)
  print(userid)
  status = ""
  if jobstatus == "COMPLETED":
    print("{} successfully completed".format(jobname))
    status = "Transcribe job completed"

  
  if jobstatus == "FAILED":
    print("{} failed !!!".format(jobname))
    status = "Transcribe job failed"
    
  updateStatus(userid,filename,status)
  data = urllib.request.urlopen(response['TranscriptionJob']['Transcript']['TranscriptFileUri'])
  data = json.loads(data.read())
  transcript = data['results']['transcripts'][0]['transcript']
  updateTranscribeStatus(jobname,jobstatus,transcript)
  
  TranscriptAttachmentFile = jobname +'.txt'
  TranscriptFile='/tmp/'+ jobname+'.txt'
  
  file = open(TranscriptFile, 'a')
  file.write(transcript)
  file.close()
  
  Sender = "AWS Interview Analytics System <jalawala@amazon.com>"
  
  # Replace recipient@example.com with a "To" address. If your account 
  # is still in the sandbox, this address must be verified.
  #Recipient = ['jalawala@amazon.com']
  Recipient = getRecepientEmailId(jobname)
  #sendEmail(Sender, Recipient, job_name, state, transcript)
  sendEmailAsAttachment(Sender, Recipient, jobname, status, TranscriptFile, TranscriptAttachmentFile)
  
  
  return transcript

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
  
def getRecepientEmailId(jobname):
  

  print("jobname={}".format(jobname))
  try:
      response = tabletranscribeStatus.get_item(Key={'jobname': jobname})
  except ClientError as e:
      print(e.response['Error']['Message'])

  if 'Item' in response.keys():
    MediaFileUri = response['Item']['MediaFileUri']  
    print("MediaFileUri={}".format(MediaFileUri))
    filenameparts = MediaFileUri.split('/')
    filename = filenameparts[-1]
    print("filename={}".format(filename))
    
    
  try:
      response = tableinterviewanalysis.get_item(Key={'filename': filename})
  except ClientError as e:
      print(e.response['Error']['Message'])  
  
  print("response={}".format(response))    
  if 'Item' in response.keys():
    email = response['Item']['email'] 
    print("email={}".format(email))
    return [email]
  
def handler(event, context):
  print('received event: {}'.format(event))
  
  #below if is just for testing purpose. we can remove later
  if 'RequestType' in event.keys(): 
    if event['RequestType'] == "transcribeevent":
      print("Handling transcribeevent={}".format(event)) 
      jobname=event['jobname']
      Recipient = getRecepientEmailId(jobname)
      print("Recipient={}".format(Recipient))
      return {
        'message': 'Hello from your new Amplify Python lambda!'
      }
      
  
  jobname = event["detail"]["TranscriptionJobName"]
  jobstatus = event["detail"]["TranscriptionJobStatus"]
  response = getJobDetails(jobname)

    
    
  
  return {
    'message': 'Hello from your new Amplify Python lambda!'
  }
