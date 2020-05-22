## EC2 Spot GameDay

In this workshop, you will deploy the following:

### Step1 :  Create an EC2 Key Pair   
aws ec2 create-key-pair --key-name SpotGameDay | jq -r '.KeyMaterial' > SpotGameDay.pem

### Step2 : Create the CFN Stack
aws cloudformation create-stack --stack-name SpotGameDay --template-body file://ec2-spot-gameday.yaml --capabilities CAPABILITY_IAM --region $AWS_REGION

