import boto3
import os


def handler(event, context):
  print("This is test code1")

  print("event={} context={}".format(str(event), str(context)))

  client = boto3.client('autoscaling')
  asg_name=os.getenv('ASG_NAME')
  print("asg_name={}".format(asg_name))
  response = client.describe_auto_scaling_groups(
      AutoScalingGroupNames=[
        asg_name,
      ]
    )
  DesiredCapacity=response['AutoScalingGroups'][0]['DesiredCapacity']
  
  if event["detail-type"] == "EC2 Spot Instance Interruption Warning":
    DesiredCapacity += 1
    print("Received EC2 Spot Instance Interruption Warning. Increasing DesiredCapacity from {} to {}".format(DesiredCapacity-1, DesiredCapacity))
  elif event["detail-type"] == "EC2 Spot Instance Request Fulfillment":
    DesiredCapacity -= 1
    print("Received EC2 Spot Instance Request Fulfillment. Decreasing DesiredCapacity  from {} to {}".format(DesiredCapacity+1, DesiredCapacity))

  response = client.set_desired_capacity(
    AutoScalingGroupName=asg_name,
    DesiredCapacity=DesiredCapacity,
    HonorCooldown=True
  )
  

  return