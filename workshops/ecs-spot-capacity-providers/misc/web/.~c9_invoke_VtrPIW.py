from flask import Flask
from flask.ext.cors import CORS, cross_origin
import os
import requests
import json
import signal
import time
import socket
import sys
from ec2_metadata import ec2_metadata



class GracefulKiller:
  kill_now = False
  signals = {
    signal.SIGINT: 'SIGINT',
    signal.SIGTERM: 'SIGTERM'
  }

  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    print("\nReceived {} signal".format(self.signals[signum]))
    print("Cleaning up resources. End of the program")
    self.kill_now = True
    
    
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
    
    response = ""
    
    response +="<head> <title>Spot Game Day</title> </head>"
  
    response += "<h2>I am a Simple Web ServRunning with below Attributes </h2> <hr/>"
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
      response += "<li>My instance_id is: {}</li>".format(ec2_metadata.instance_id)
      response += "<li>My availability_zone is: {}</li>".format(ec2_metadata.availability_zone)      
      response += "<li>My ami_launch_index is: {}</li>".format(ec2_metadata.ami_launch_index)      
      response += "<li>My instance_type is: {}</li>".format(ec2_metadata.instance_type)      
      response += "<li>My private_ipv4 is: {}</li>".format(ec2_metadata.private_ipv4)  
      response += "<li>My public_ipv4 is: {}</li>".format(ec2_metadata.public_ipv4)  
      response += "<li>My Region is: {}</li>".format(ec2_metadata.region)      
      
      networks = ec2_metadata.network_interfaces
      for nw in networks:
        response += "<li>My subnet_id is: {}</li>".format(ec2_metadata.network_interfaces[nw].subnet_id)
        response += "<li>My vpc_id is: {}</li>".format(ec2_metadata.network_interfaces[nw].vpc_id)
        
      URL = "http://localhost:51678/v1/metadata"
      ecs = requests.get(URL).json()
      
      response += "<li>My ECS Cluster Name is: {}</li>".format(ecs['Cluster'])     
      
      URL = "http://localhost:51678/v1/tasks"
      task_list = requests.get(URL).json()
      
      num = 1
      for task in task_list['Tasks']:
        if task['KnownStatus'] =="RUNNING":
          response += "<li>Task number {} and Task Id is : {}</li>".format(num, task['Arn'])
          response += "<li>Task number {} and Task Family is : {}</li>".format(num, task['Family'])     
          response += "<li>Task number {} and Task Version is : {}</li>".format(num, task['Version'])     
          num = num + 1
          con=1
          for container in task['Containers']:
            response += "   <li>Container number {} and DockerId is : {}</li>".format(con, container['DockerId'])
            response += "   <li>Container number {} and Name is : {}</li>".format(con, container['Name'])     
            con = con + 1

    except:
      response += "<li>There is an error to access the metadata : {}</li>".format(sys.exc_info()[0])
      
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

if __name__ == '__main__':
    killer = GracefulKiller()
    print("Running ...")
    app.run(port=80,host='0.0.0.0')

    #while not killer.kill_now:
    #  time.sleep(1)