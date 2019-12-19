import boto3
import json
def handler(event, context):
  print("This is test code1")
  print("event={} context={}".format(str(event), str(context)))
  
  client = boto3.client('autoscaling')
  
  response = client.describe_auto_scaling_groups(
    AutoScalingGroupNames=[
        'asg_cwt_od2',
    ]
)

  print("This is test code2")
  print("ASG={}".format(str(response)))
  print("This is test code3")
  print(response['AutoScalingGroups'])
  print("This is test code4")
  print(response['AutoScalingGroups'][0])
  print(response['AutoScalingGroups'][0]['AutoScalingGroupName'])
  DesiredCapacity=response['AutoScalingGroups'][0]['DesiredCapacity']
  DesiredCapacity += 1


  print("DesiredCapacity={}".format(DesiredCapacity))
  response = client.set_desired_capacity(
    AutoScalingGroupName='asg_cwt_od2',
    DesiredCapacity=DesiredCapacity,
    HonorCooldown=True
  )
  print(response)
  #print(response['AutoScalingGroups'][0]['DesiredCapacity'])
  
  #json_string = json.loads(str(response))
  
 # print("response={}".format(str(json_string)))

  return