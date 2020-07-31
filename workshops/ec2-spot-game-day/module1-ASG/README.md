## EC2 Spot GameDay  Module1 - ec2-spot-gameday.yaml

In this workshop, you will deploy the following:

### Step1 :  Create an EC2 Key Pair   
aws ec2 create-key-pair --key-name SpotGameDay | jq -r '.KeyMaterial' > SpotGameDay.pem

### Step2 : Create the CFN Stack
aws cloudformation create-stack --stack-name SpotGameDay --template-body file://ec2-spot-gameday.yaml --capabilities CAPABILITY_IAM --region $AWS_REGION

## EC2 Spot GameDay  Module2 - ec2-spot-gameday-module2-eks.yaml

### Step1 :  Deploy the CFN styack ec2-spot-gameday-module2-eks.yaml in us-east-1

### Step2 : Create a Cloud9 Environment
install the following tools

export KUBECTL_VERSION=v1.15.10
sudo curl --silent --location -o /usr/local/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl
sudo chmod +x /usr/local/bin/kubectl

sudo yum -y install jq gettext

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
. ~/.bash_profile

run aws configure  and set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY of the
user which is used to create the EKS cluster

Or if any IAM role is assumed while creating the EKS cluster, use the same role to 
assign it to the EC2 instance of the Cloud9 environment.

curl -o aws-iam-authenticator https://amazon-eks.s3.us-west-2.amazonaws.com/1.15.10/2020-02-22/bin/linux/amd64/aws-iam-authenticator
chmod +x ./aws-iam-authenticator
mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$PATH:$HOME/bin


### Step3 : Configure eksctl tool for the accessing the EKS cluster
aws eks --region us-east-1 update-kubeconfig --name Ec2SpotEKS

Add the following configuration for aws-iam-authenticator to ~/.kube/config

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN5RENDQWJDZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJd01EWXlPVEUwTWpNeU5sb1hEVE13TURZeU56RTBNak15Tmxvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTGlaCi9qRkZyUlFvSmYxZDRUdXlMRjBIeTVwelQraDRjVlJmTHZ1a1YxZ0pma3VOQzBNaTdWY0xFQWU4b3kyTjV5STAKRFVvVHIrUEFFcDN4cUNyNEp4anFkbkJVSWNicTkyOXIyRnRQOHlMYjFZQXFvcEU0QWVQVXJ3c0gzZVFkVDIrWApUd2prcnpmR1Z1RmNkZlE1a216bGlBaFBJVlpQaVYxMDBJdlcxbnhIT2xVTERkWDVrVHJjUUtYNjR3TzlKVlpCCitrNTdoNWgya29MaVM0YThubU0rSWJDd2V6UVN1cUgva0x2U2FSWkNvbzBZVjYrd0xOYnQ2Sm1XUHRXbVNUaHcKVTllazZXa0ZDNTkwT2hEWldSenEwYjIrRVBBbFZtM3JodGszUXZrQmtRQ3ZtVGoveXE4eXRsL1puU3pEejF5bQp4TDllVlFvSnk0UWZwZ0JXYlZzQ0F3RUFBYU1qTUNFd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFJQU1maVZJdlVMTDZMd2ZaMlBxU3V6T2Z3eGUKZ2tXQTJsUjAwOVFnV3ozWTluQ2pxM0FLMDNrRjJ4MVphOElTczcwcDdzRXNUeGI4cVpJRzMvR0gycUJTcnFzSwpCTnFNRnNXOFFxUDZmem9weDlRTndZTURiQmNTOEVjbWd5OVVkdVY3S091OGZHNkVmQ2t0Z09ieDcyMVhUejZJCk1hVW5QM3FlUjVpSzI1MHVKTjdQK1IxRENacXl0enBFUlc2bGdEb0l4YVJZV0dlbmJIMDZoRHM4Z3pqbTJ0dE8KVGdYdUs0ZFVhMlcra01CQXlQaEdZZ0pRMGJCbEpaWjVlOFBxSzVSSWtIOU9DU0NKSURHa3NITVhaOUk0MTkwUQp0UG1jb3FRbU9HMGNrcVdmaXFlQzZkRkhqT0VmcG5iTVVzRks1ZHZPUE9tcWFsdXR3dUtmb0ZEcEpQcz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
    server: https://BB76CAE95CAD48A0E62E7036E112DBB7.gr7.us-east-1.eks.amazonaws.com
  name: arn:aws:eks:us-east-1:000474600478:cluster/Ec2SpotEKS
contexts:
- context:
    cluster: arn:aws:eks:us-east-1:000474600478:cluster/Ec2SpotEKS
    user: arn:aws:eks:us-east-1:000474600478:cluster/Ec2SpotEKS
  name: arn:aws:eks:us-east-1:000474600478:cluster/Ec2SpotEKS
current-context: arn:aws:eks:us-east-1:000474600478:cluster/Ec2SpotEKS
kind: Config
preferences: {}
users:
- name: arn:aws:eks:us-east-1:000474600478:cluster/Ec2SpotEKS
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      args:
      - "token"
      - "-i"
      - Ec2SpotEKS
      command: aws-iam-authenticator
      

### Step4 : Configure aws-auth-cm.yaml to allow worker nodes to join the cluster    
      
test kubectl get nodes

curl -o aws-auth-cm.yaml https://amazon-eks.s3.us-west-2.amazonaws.com/cloudformation/2020-06-10/aws-auth-cm.yaml

get the NodeInstanceRole ARN from IAM and update it in the aws-auth-cm.yaml

apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
    - rolearn: arn:aws:iam::000474600478:role/Ec2SpotEKS-NodeInstanceRole
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
        
        
      

 kubectl apply -f aws-auth-cm.yaml