import os
import requests
import json
import time
import sys
import boto3
import datetime
import base64
import urllib
from pprint import pprint

ec2client = boto3.client('ec2', region_name='us-east-1')
ec2resource = boto3.resource('ec2')
dbclient = boto3.client('dynamodb')
dynamodbresource = boto3.resource('dynamodb')
transcribe = boto3.client('transcribe')

def checkTranscribeJobs(job_name):
  while True:
      status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
      if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
      print("Not ready yet...")
      time.sleep(10)
  pprint(status)
  if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    response = urllib.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    data = json.loads(response.read())
    text = data['results']['transcripts'][0]['transcript']
    print(text)  
    
  

def scheduleTranscribeJobs(s3bucketname, file):

  
  job_name = "job1"
  #job_uri = "https://"+s3bucketname+"/"+file
  job_uri='https://s3bucketaudio.s3.amazonaws.com/ContainerSummit+-+Containers+on+Spot.mp3'
  transcribe.start_transcription_job( 
         TranscriptionJobName=job_name,    
         Media={'MediaFileUri': job_uri},    
         MediaFormat='mp3',    
         LanguageCode='en-US')
         
  while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)    
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
      break    
    print("Not ready yet...")    
    time.sleep(5)
    
  pprint(status)
  
  
  
  
  
if __name__ == '__main__':
  print("Starting the Transcribe workload ...")
  #s3://s3bucketaudio/ContainerSummit+-+Containers+on+Spot.mp3
  #s3bucketname = "s3bucketaudio"
  #file = "ContainerSummit+-+Containers+on+Spot.mp3"
  #scheduleTranscribeJobs(s3bucketname, file)
  
  job_name='autiototext'
  checkTranscribeJobs(job_name)
  
  



