import json
import os
import eesdk
import boto3
#
# # ENV VARs - these are set via the Master CloudFormation template:
# API_BASE = os.environ['EE_API_BASE']
# API_TOKEN = os.environ['EE_API_TOKEN']
# EVENT_ID = os.environ['EE_EVENT_ID']
# MODULE_ID = os.environ['EE_MODULE_ID']
# REGION = os.environ['EVENT_REGION']
#
# __author__ = "ssengott@"
# #input lambda to create inputs, outputs for teams on module deployment into team account
# def lambda_handler(event, context):
#
#     print("GD: i/p lambda.")
#     print(event)
#
#     sns_event = event['Records'][0]['Sns']['MessageAttributes']['event']['Value']
#     sns_payload = json.loads(event['Records'][0]['Sns']['Message'])
#
#     print("GD: parsed sns_event: " + sns_event)
#     print("GD: sns_payload message: " + str(sns_payload))
#     print("GD: MODULE_ID="+MODULE_ID)
#     print("GD: API_BASE="+API_BASE)
#     #print("GD: API_TOKEN="+API_TOKEN)
#     print("GD: EVENT_ID="+EVENT_ID)
#     print("GD: REGION="+REGION)
#
#     #create input for each team for capturing and creating checkpoint
#     if sns_event == "eventengine:MODULE_DEPLOYED":
#         print("GD: module deployed event")
#         TODO error handling
#         sdk = eesdk.EESDK(API_BASE, API_TOKEN, EVENT_ID, MODULE_ID)
#         teams = sdk.get_all_teams()
#         # Iterate through all teams
#         for team in teams:
#             team_id = team['team-id']
#             print("GD: Creating output and input for team:"+team_id)
#             sdk.post_output(team_id, "gd_output_eks_config_message", "Your first task: ",
#                             "Apply SPOT best practices for given EKS Cluster")
#             #create input to get confirmation from user for spot configuration
#             sdk.post_input(team_id, "gd_input_eks_configured", "Have you configured spot best practices for the use case explained?",
#                            description="Provide YES as answer to mark task completion and to score points.")
#



def deploy_team_template_cfn():
    ACCESS_KEY_ID = ''
    SECRET_ACCESS_KEY = '+/Zoi6r5'
    SESSION_TOKEN = 'g=='
    DEFAULT_REGION='us-east-1'

#use team account ops role credentials
    aws_session = boto3.Session(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        aws_session_token=SESSION_TOKEN,
        region_name=DEFAULT_REGION
    )

    cfn_client = aws_session.client('cloudformation')
    cfn_response = cfn_client.create_stack(
        StackName='EKS-spot-gd-cfn-stack',
        TemplateURL='https://s3.amazonaws.com/ee-assets-prod-us-east-1/modules/a2bac93dd4344c1bad0477278f15d800/v1/team-template-eks.yaml',
        TimeoutInMinutes=45,
        Capabilities=[
            'CAPABILITY_IAM','CAPABILITY_NAMED_IAM',
        ]
    )

    print("CFN response:" + str(cfn_response))

deploy_team_template_cfn()