from flask import Flask, render_template
from flask.ext.cors import CORS, cross_origin
import os
import requests
import json
import signal
import time
import socket
import sys
from ec2_metadata import ec2_metadata
import boto3
#import urllib


class GracefulKiller:
  signals = {
    signal.SIGINT: 'SIGINT',
    signal.SIGTERM: 'SIGTERM'
  }

  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    #cam_img = urllib.urlopen("http://localhost:80/").read()
    #cam_img.write("Received {} signal")
    print("\nReceived {} signal".format(self.signals[signum]))
    if self.signals[signum] == 'SIGTERM':
      print("Looks like it's a Spot Interruption. Let's wrap up the processing within next 30 sec ...")

    
    
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

 
@app.route('/')
@cross_origin()
def index():
    
    #return render_template("index.html")
    response = ""
    
    response +="<head> <title>Spot Game Day</title> </head>"
  
    response += "<h2>I am a Simple Containerized Web App Running with below Attributes </h2> <hr/>"
    #hostname = socket.gethostname()    
    #IPAddr = socket.gethostbyname(hostname)   
    #response += "<li>My Host Name is: {}</li>".format(hostname)    
    #response += "<li>My IP        is: {}</li>".format(IPAddr)      
    
    #URL = "curl -s http://localhost:51678/v1/metadata"
    #metadata = requests.get(URL)
    #response += "<li>My ECS metadata is: {}</li>".format(metadata)
    
    
    #URL = "http://169.254.169.254/latest/meta-data/instance-id"
    try:
      #instanceId = requests.get(URL)
      #response += "<li>My instanceId is: {}</li>".format(str(instanceId))
      instanceId = ec2_metadata.instance_id
      response += "<li>My instance_id = {}</li>".format(instanceId)
      lifecycle = getInstanceLifecycle(instanceId)      
      response += "<li>My Instance lifecycle = {}</li>".format(lifecycle)      
      response += "<li>My instance_type = {}</li>".format(ec2_metadata.instance_type)      
      response += "<li>My private_ipv4 = {}</li>".format(ec2_metadata.private_ipv4)  
      response += "<li>My public_ipv4 = {}</li>".format(ec2_metadata.public_ipv4)       
      response += "<li>My availability_zone = {}</li>".format(ec2_metadata.availability_zone)      
      response += "<li>My Region = {}</li>".format(ec2_metadata.region)      
      response += "<li>My ami_launch_index = {}</li>".format(ec2_metadata.ami_launch_index)      
 
      networks = ec2_metadata.network_interfaces
      for nw in networks:
        response += "<li>My subnet_id = {}</li>".format(ec2_metadata.network_interfaces[nw].subnet_id)
        response += "<li>My vpc_id = {}</li>".format(ec2_metadata.network_interfaces[nw].vpc_id)
        
      URL = "http://localhost:51678/v1/metadata"
      ecs = requests.get(URL).json()
      
      response += "<li>My ECS Cluster Name = {}</li>".format(ecs['Cluster'])     
      
      URL = "http://localhost:51678/v1/tasks"
      task_list = requests.get(URL).json()
      
      num = 1
      for task in task_list['Tasks']:
        if task['KnownStatus'] =="RUNNING":
          response += "<li>Task number {} and Task Id = {}</li>".format(num, task['Arn'])
          response += "<li>Task number {} and Task Family:Version = {}:{}</li>".format(num, task['Family'], task['Version'])
          num = num + 1
          
          con=1
          for container in task['Containers']:
            response += "<li>Container number {} and DockerId = {}</li>".format(con, container['DockerId'])
            response += "<li>Container number {} and Name = {}</li>".format(con, container['Name'])     
            con = con + 1

    except:
      response += "<li>Oops !!! There seems to be an error to access my instance  metadata = {}</li>".format(sys.exc_info()[0])
      
    #response += "<li>My InstanceId is: {}</li>".format(json.dumps(metadata.text, indent=4, sort_keys=True))


    #for env_var in os.environ:
    #    response += "<li>{}: {}</li>".format(env_var, os.environ.get(env_var))

    #if 'AWS_EXECUTION_ENV' in os.environ:
    #    response += "<h2>Execution Environment: {}</h2> <hr/>".format(os.environ.get('AWS_EXECUTION_ENV'))
    #else:
    #    response += "<h2>Execution Environment: {}</h2> <hr/>".format('LOCAL')

    #if 'ECS_CONTAINER_METADATA_URI' in os.environ:
    #    metadata_uri = os.environ.get('ECS_CONTAINER_METADATA_URI')
    #    metadata = requests.get(metadata_uri)
    #    response += "<h2>Metadata</h2 <hr/> {}".format(json.dumps(metadata.text, indent=4, sort_keys=True))

    return response

def getInstanceLifecycle(instanceId):
  ec2client = boto3.client('ec2', region_name=ec2_metadata.region)
  describeInstance = ec2client.describe_instances(InstanceIds=[instanceId])
  instanceData=describeInstance['Reservations'][0]['Instances'][0]
  if 'InstanceLifecycle' in instanceData.keys():
    return instanceData['InstanceLifecycle']
  else:
    return "Ondemand"


if __name__ == '__main__':
    killer = GracefulKiller()
    print("Starting A Simple Web Service ...")
    app.run(port=80,host='0.0.0.0')

    #while not killer.kill_now:
    #  time.sleep(1)