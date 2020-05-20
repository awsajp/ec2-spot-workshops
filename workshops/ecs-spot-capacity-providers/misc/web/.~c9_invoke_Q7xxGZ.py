from flask import Flask
import os
import requests
import json
import signal
import time
import socket

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
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/')
def index():
    
    response = ""
    
    response +="<head> <title>Spot Game Day</title> </head>"
  
    response += "<h2>I am a Simple Web Running with below Attributes </h2> <hr/>"
    hostname = socket.gethostname()    
    IPAddr = socket.gethostbyname(hostname)   
    response += "<li>My Host Name is: {}</li>".format(hostname)    
    response += "<li>My IP        is: {}</li>".format(IPAddr)      
    
    URL = "curl -s http://localhost:51678/v1/metadata"
    metadata = requests.get(URL)
    response += "<li>My ECS metadata is: {}</li>".format(metadata)
    
    
    URL = "http://169.254.169.254/latest/meta-data/instance-id"
    instanceId = requests.get(URL)
    response += "<li>My InstanceId is: {}</li>".format(instanceId)
      
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
    app.run(debug=False,host='0.0.0.0', port=80)

    #while not killer.kill_now:
    #  time.sleep(1)











































































































































