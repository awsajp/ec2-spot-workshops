from flask import Flask, render_template
from flask.ext.cors import CORS, cross_origin
import os
import requests
import json
import time
import sys
import boto3

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():

    response = ""
    response +="<head> <title>Spot Game Day</title> </head>"
    response += "<h2>I am a Simple Web App Running with below Attributes </h2> <hr/>"

    try:
        URL = "http://169.254.169.254/latest/meta-data/spot/termination-time"
        SpotInt = requests.get(URL)
        if SpotInt.status_code == 200:
            response += "<h1>This Spot Instance Got Interruption and Termination Date is {} </h1> <hr/>".format(SpotInt.text)


        URL = "http://169.254.169.254/latest/dynamic/instance-identity/document"
        InstanceData = requests.get(URL).json()

        instanceId = InstanceData['instanceId']
        response += "<li>My instance_id = {}</li>".format(instanceId)
        lifecycle = getInstanceLifecycle(instanceId, InstanceData['region'])
        response += "<li>My Instance lifecycle = {}</li>".format(lifecycle)
        response += "<li>My instance_type = {}</li>".format(InstanceData['instanceType'])
        response += "<li>My Intance private_ipv4 = {}</li>".format(InstanceData['privateIp'])
        response += "<li>My availability_zone = {}</li>".format(InstanceData['availabilityZone'])
        response += "<li>My Region = {}</li>".format(InstanceData['region'])

        publicIp = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4")
        response += "<li>My instance_type public_ipv4 = {}</li>".format(publicIp.text)
        AMIIndexId = requests.get("http://169.254.169.254/latest/meta-data/ami-launch-index")
        response += "<li>My ami_launch_index = {}</li>".format(AMIIndexId.text)

        AMIId = requests.get("http://169.254.169.254/latest/meta-data/ami-id")
        response += "<li>My ami_launch_index = {}</li>".format(AMIId.text)

        MacId = requests.get("http://169.254.169.254/latest/meta-data/mac")
        Mac = MacId.text

        URL = "http://169.254.169.254/latest/meta-data/network/interfaces/macs/" + str(MacId.text) + "/subnet-id"
        SubnetId = requests.get(URL)
        response += "<li>My subnet_id = {}</li>".format(SubnetId.text)

        URL = "http://169.254.169.254/latest/meta-data/network/interfaces/macs/" + str(MacId.text) + "/vpc-id"
        VPCId = requests.get(URL)
        response += "<li>My vpc_id = {}</li>".format(VPCId.text)


    except Exception as inst:
        response += "<li>Oops !!! Failed to access my instance  metadata with error = {}</li>".format(inst)

    return response

def getInstanceLifecycle(instanceId, region):
    ec2client = boto3.client('ec2', region_name=region)
    describeInstance = ec2client.describe_instances(InstanceIds=[instanceId])
    instanceData=describeInstance['Reservations'][0]['Instances'][0]
    if 'InstanceLifecycle' in instanceData.keys():
        return instanceData['InstanceLifecycle']
    else:
        return "Ondemand"

if __name__ == '__main__':
    print("Starting A Simple Web Service ...")
    app.run(port=80,host='0.0.0.0')




