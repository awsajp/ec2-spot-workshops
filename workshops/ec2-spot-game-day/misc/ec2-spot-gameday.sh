#!/bin/bash 

echo "Creating the Infrastructure for EC2 SpotGameDay"

aws ec2 create-key-pair --key-name SpotGameDay | jq -r '.KeyMaterial' > SpotGameDay.pem

aws cloudformation create-stack --stack-name SpotGameDay --template-body file://ec2-spot-gameday.yaml --capabilities CAPABILITY_IAM --region $AWS_REGION