import boto3
from boto3.dynamodb.conditions import Key
import os
import json
import decimal
import time
from random import seed
from random import random
import threading


HostsTableName=os.getenv('DYNAMODB_HOST_TABLE_NAME')
InstancesTableName=os.getenv('DYNAMODB_INSTANCEID_TABLE_NAME')
StatusIndexName=os.getenv('DYNAMODB_GSI_ST')
InstanceIndexName=os.getenv('DYNAMODB_GSI_InstanceId')
DC1InstanceId=os.getenv('DC1_INSTANCE_ID')

dynamodb = boto3.resource('dynamodb')
HostsTable = dynamodb.Table(HostsTableName)
InstanceTable = dynamodb.Table(InstancesTableName)
client = boto3.client('ssm')

def lambda_handler(event, context):

  instanceId = event['detail']['instance-id']

  print("instanceId={} HostsTableName={}, InstancesTableName={}, StatusIndexName={}, InstanceIndexName={} DC1InstanceId={}".format(instanceId, HostsTableName,InstancesTableName, StatusIndexName, InstanceIndexName, DC1InstanceId))


  if event["detail-type"] == "EC2 Spot Instance Interruption Warning":
    print("Received EC2 Spot Instance Interruption Warning for instanceId={}...".format(instanceId))

    # Get the host name for this interrupted spot instance.
    resp = HostsTable.query(
      IndexName=InstanceIndexName,
      KeyConditionExpression=Key('InstanceId').eq(instanceId),
    )

    if resp['Count'] >=1 :

      interruptedHostId = resp['Items'][0]["Host"]
      interruptedHostName = resp['Items'][0]["HostName"]
      L=interruptedHostName.split('-')
      interruptedHostNewName=L[0]+"-"+str(int(L[1])+1)

      HostsTable.update_item(
        Key={
          'Host': interruptedHostId
        },
        UpdateExpression='SET ST = :val1, InstanceId = :val2, HostName = :val3',
        ExpressionAttributeValues={
          ':val1': 'FREE',
          ':val2': "Empty",
          ':val3': interruptedHostNewName
        }
      )


      print("interruptedHostId={} interruptedHostName={} interruptedHostNewName={}".format(interruptedHostId, interruptedHostName, interruptedHostNewName))

      print("Sending an interruption message to all the users for the hostname={} with nstanceId={}".format(interruptedHostName, instanceId))
      document = 'AWS-RunPowerShellScript'
      c="C:\\windows\\system32\\msg.exe * Hello,  This desktop will be shutdown in 120 seconds. Please save your work immediately. You will lose unsaved work, when this desktop is shutdown.  A new desktop will be made available to you to login into shortly. Your new Desktop host name is " + str(interruptedHostNewName)
      params= { "commands": [c] }
      send_command_to_the_instance(instanceId, document, params )


      #   detach EBS volume

      #(available, nextFreeInstance) = get_next_available_resource("instance", instanceId)

      available=True
      nextFreeInstance = "i-0cc24c8b57c3ab098"

      # check if there is at least one instance available in the buffer pool
      if available :

        print("Assigning  nextFreeInstance={} to interruptedHostNewName ID={} in HostsTableName={} for interruptedHostId={} ".format(nextFreeInstance, interruptedHostNewName, HostsTableName, interruptedHostId))
        wait_ec2_complate(nextFreeInstance)
        print("calling add_instance_to_domain with nextFreeInstance = {} to interruptedHostNewName ID = {}".format(nextFreeInstance, interruptedHostNewName))
        add_instance_to_domain(nextFreeInstance, interruptedHostNewName)


        print("Assigning  nextFreeInstance={} to interruptedHostNewName ID={} in HostsTableName={} for interruptedHostId={} ".format(nextFreeInstance, interruptedHostNewName, HostsTableName, interruptedHostId))
        HostsTable.update_item(
          Key={
            'Host': interruptedHostId
          },
          UpdateExpression='SET ST = :val1, InstanceId = :val2, HostName = :val3',
          ExpressionAttributeValues={
            ':val1': 'ASSIGNED',
            ':val2': nextFreeInstance,
            ':val3': interruptedHostNewName
          }
        )

      else:
        # There is no instance available in the pool. So change the status of the instance from ASSIGNED to FREE

        print("Assigning FREE status to  interruptedHostName={} HostsTableName={} since there are no free instances in the buffer pool".format(interruptedHostName, HostsTableName))
        HostsTable.update_item(
          Key={
            'Host': interruptedHostId
          },
          UpdateExpression='SET ST = :val1, HostName = :val2',
          ExpressionAttributeValues={
            ':val1': 'FREE',
            ':val2': interruptedHostNewName
          }
        )

      remove_instance_to_domain(instanceId, interruptedHostName)

    else:
      print("Removing instanceId={} to buffer pool in InstancesTableName={} since it is interrupted and NOT assigned to any Host".format(instanceId, InstancesTableName))

      response = InstanceTable.delete_item(
        Key={
          'InstanceId': instanceId
        }
      )


  elif event["detail-type"] == "EC2 Spot Instance Request Fulfillment":
    print("Received EC2 Spot Instance Request Fulfillment... for instanceId={}".format(instanceId))

    # Check if any Host is FREE and need to be assignedE
    (available, freeHostName) = get_next_available_resource("host", instanceId)

    # check if there is at least one Host which is FREE

    if available :

      wait_ec2_complate(instanceId)
      print("Calling add_instance_to_domain with freeHostName = {} to Instance ID = {}".format(freeHostName, instanceId))
      add_instance_to_domain(instanceId, freeHostName)

    else:

      #Add the instance to the buffer pool
      print("Adding instanceId={} to buffer pool in InstancesTableName={}".format(instanceId, InstancesTableName))
      response = InstanceTable.put_item(
        Item={
          'InstanceId': instanceId,
          'ST': 'FREE',
          'IP': '5.5.5.5'
        }
      )


def get_next_available_resource(name, instanceId):

  retValue = "dummy"
  index = "dummy"
  value1="dumm"
  value2="dummy"
  seed(1)
  if name == "host":
    min=0
    max=60
    table=HostsTable
  else:
    min=0
    max=10
    table=InstanceTable

  value1=min + (random() * (max - min))
  time.sleep(value1)

  resp = table.query(
    IndexName=StatusIndexName,
    KeyConditionExpression=Key('ST').eq('FREE'),
  )

  if resp['Count'] >=1 :
    available = True
    print("The following Hosts are FREE and needs to be assigned:")
    for item in resp['Items']:
      print(item)

    min=0
    max=resp['Count']
    value2=min + (random() * (max - min))
    index=int(value2)



    if name == "host":
      HostId = resp['Items'][index]["Host"]
      freeHostName = resp['Items'][index]["HostName"]

      print("Assigning  instanceId={} to freeHostName ID={} in HostsTableName={} for HostId={} ".format(instanceId, freeHostName, HostsTableName, HostId))
      HostsTable.update_item(
        Key={
          'Host': HostId
        },
        UpdateExpression='SET ST = :val1, InstanceId = :val2',
        ExpressionAttributeValues={
          ':val1': 'ASSIGNED',
          ':val2': instanceId
        }
      )
      retValue = freeHostName
    else:
      nextFreeInstance = resp['Items'][index]["InstanceId"]
      print("Removing nextFreeInstance={} from the buffer pool in InstancesTableName={}".format(nextFreeInstance, InstancesTableName))
      response = InstanceTable.delete_item(
        Key={
          'InstanceId': nextFreeInstance
        }
      )
      retValue = nextFreeInstance

  else:
    available = False

  print("name={} value1={} available={} count={} value2={} index={} retValue={}".format(name, value1,  str(available), resp['Count'],value2, index, retValue))
  return (available, retValue)

def remove_instance_to_domain(instanceId, interruptedHostName):
  #L=args.split(':')
  #instanceId=L[0]
  #interruptedHostName=L[1]

  print("Remove-Computer() called for instanceId={}".format(instanceId))
  document = 'AWS-RunPowerShellScript'
  c="Remove-Computer -Force  -Restart "
  #c="Remove-Computer -Force "
  params= { "commands": [c] }
  send_command_to_the_instance(instanceId, document, params )
  time.sleep (45)

  #remove the computer from the AD
  print("Remove-ADComputer() called for interruptedHostName={} from DC1InstanceId={}".format(interruptedHostName, DC1InstanceId))
  document = 'AWS-RunPowerShellScript'
  c1="Remove-ADComputer -Identity   "+str(interruptedHostName) + "  -confirm:$false "
  c2="Remove-DnsServerResourceRecord -Force -ZoneName example.com -RRType A -Name "  + str(interruptedHostName)
  params= { "commands": [c1, c2] }
  send_command_to_the_instance(DC1InstanceId, document, params )
  #time.sleep (20)

def add_instance_to_domain(instanceId, hostname):

  print("add_instance_to_domain:rename instanceId={} hostname={}".format(instanceId, hostname))

  #assign_hostname_to_instance(instanceId, freeHostName)
  document = 'AWS-RunPowerShellScript'
  #part1= "{ \"commands\": [" + " \"Rename-Computer -NewName   "
  #part2=str(freeHostName) + "  \" ], }"
  #params =  part1 + part2
  c="Rename-Computer -NewName     "+str(hostname)
  params= { "commands": [c] }
  send_command_to_the_instance(instanceId, document, params)

  time.sleep (20)

  # Join the Host to the domain

  #add_instance_to_domain(instanceId)
  print("add_instance_to_domain:domain instanceId={} hostname={}".format(instanceId, hostname))
  document = 'awsconfig_Domain_d-9367157267_example.com'
  params={}
  send_command_to_the_instance(instanceId, document, params )

  time.sleep (20)
  #wait for few seconds to ensure domain join is successful

  # Restart the Host to make the changes effect
  #restart_instance(instanceId)
  print("add_instance_to_domain:restart instanceId={} hostname={}".format(instanceId, hostname))
  document = 'AWS-RunPowerShellScript'
  #params="{ \"commands\": [" + " \"Restart-Computer -Force  \"  " + "   ], }"
  c="Restart-Computer -Force"
  params= { "commands": [c] }
  send_command_to_the_instance(instanceId, document, params )
  time.sleep (20)



def send_command_to_the_instance(instanceId, document, params):

  #print("instanceId={}".format(instanceId))


  client = boto3.client('ssm')
  response = client.send_command(
    Targets=[
      {
        'Key': 'InstanceIds',
        'Values': [
          str(instanceId),
        ]
      },
    ],
    DocumentName=document,
    DocumentVersion='1',
    TimeoutSeconds=300,
    Comment="sending a command command to the PC",
    Parameters=params,
    MaxConcurrency='50',
    MaxErrors='0'
  )
  print("response={}".format(response))

def wait_ec2_complate(instance_id):

  #print("instance_id={}".format(instance_id))
  client = boto3.client('ec2')
  iter = 1
  status = False
  while True:
    iter += 1
    time.sleep(15)
    rsp = client.describe_instance_status(
      InstanceIds=[str(instance_id)],
      IncludeAllInstances=True
    )
    # double check 2/2 status
    instance_status = rsp['InstanceStatuses'][0]['InstanceStatus']['Status']
    system_status = rsp['InstanceStatuses'][0]['SystemStatus']['Status']
    print("iter={} Instance status is {} System status is {}".format(iter, str(instance_status), str(system_status)))
    if str(instance_status) == 'ok' and str(system_status) == 'ok':
      status = True
      break

    if iter >= 30:
      break
  return status