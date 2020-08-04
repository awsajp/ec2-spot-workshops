## EC2 Spot GameDay  Module2 - ec2-spot-gameday-module2-eks.yaml

### Step1 :  Deploy the CFN stack ec2-spot-gameday-module2-eks.yaml in us-east-1
 The CFN stack creates the following resources
 ##### VPC with 10 subnets (5 private subnets and 5 public subnets in us-east-1)
 ##### EKS Cluster with all 10 subnets
 ##### EC2 Launch Template with below labels and taints
     ###### OnDemand Instances Labels: --node-labels=lifecycle=OnDemand,intent=control-apps
     ###### Ec2Spot Instances Labels:  --node-labels=lifecycle=Ec2Spot,intent=apps
     ###### Ec2Spot Instances Taints:  --node-labels=spotInstance=true:PreferNoSchedule     
 ##### Node Groups for size large (2vCPU, 8GB) i.e. 1:4 ratio
    ###### OnDemandNodeGroup1 with min=0, desired=1, max=10
    ###### Ec2SpotNodeGroup1 with min=0, desired=1, max=10
 ##### Node Groups for size xlarge (4vCPU, 16GB) i.e. 1:4 ratio
    ###### OnDemandNodeGroup2 with min=0, desired=1, max=10
    ###### Ec2SpotNodeGroup2  with min=0, desired=1, max=10
    
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

Plese replace with your AWS ACCONT ID and EKS Cluster Name

aws eks --region us-east-1 update-kubeconfig --name Ec2SpotEKS

Add the following configuration for aws-iam-authenticator to ~/.kube/config

users:
- name: arn:aws:eks:us-east-1:<AWS_ACOOUNT_ID>:cluster/<EKS_CLUSTER_NAME>
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      args:
      - "token"
      - "-i"
      - <EKS_CLUSTER_NAME>
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
    - rolearn: arn:aws:iam::<AWS_ACOOUNT_ID>:role/<EKS_CLUSTER_NAME>-NodeInstanceRole
      username: system:node:{{EC2PrivateDNSName}}
      groups:
        - system:bootstrappers
        - system:nodes
        
        
     
 kubectl apply -f aws-auth-cm.yaml
 
 ### Step5 : Install helm, metric server and kube-opos-view tool
 
 curl -sSL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
 
 helm version --short
 
 
 helm repo add stable https://kubernetes-charts.storage.googleapis.com/
 helm repo update
 
 helm search repo stable
 
 helm completion bash >> ~/.bash_completion
 . /etc/profile.d/bash_completion.sh
 . ~/.bash_completion
 source <(helm completion bash)
 
 
 kubectl create namespace metrics
 helm install metrics-server \
     stable/metrics-server \
     --version 2.10.0 \
     --namespace metrics

kubectl get apiservice v1beta1.metrics.k8s.io -o yaml


helm install kube-ops-view \
stable/kube-ops-view \
--set service.type=LoadBalancer \
--set nodeSelector.intent=control-apps \
--set rbac.create=True

helm list

kubectl get svc kube-ops-view | tail -n 1 | awk '{ print "Kube-ops-view URL = http://"$4 }'


helm repo add eks https://aws.github.io/eks-charts
helm install aws-node-termination-handler \
             --namespace kube-system \
             eks/aws-node-termination-handler


kubectl get daemonsets --all-namespaces


### Step5 : How to simulate spot interruption and test your apps against the interruptions

##### Deploy the CFN stack ec2-spot-gameday-module2-eks-spotfleet.yaml. Enter the EKS Stack name in parameters section

##### Check the if the spot node from the spot fleet joins the EKS cluster. Ex: ip-10-0-5-15.ec2.internal below

![Alt text](docs/2.png?raw=true "Diagram")

##### Check the if node termination handler is running on this spot node from the spot fleet

![Alt text](docs/1.png?raw=true "Diagram")

##### Label the spot node from the spot fleet, uniquley to deploy our application ONLY on this node

jp:~/environment $ kubectl label nodes ip-10-0-5-15.ec2.internal   spotsa=jp


node/ip-10-0-5-15.ec2.internal labeled

##### Check if this spot node has the right labels and taints applied 
![Alt text](docs/5.png?raw=true "Diagram")

##### Ensure that the application uses node selector to use this label 
![Alt text](docs/12.png?raw=true "Diagram")

##### Deploy the sample app nginx.yaml 
jp:~/environment $ kubectl apply -f nginx.yaml

 
deployment.apps/nginx-no-split created

##### Check the sample app is deployed only this spot node
![Alt text](docs/6.png?raw=true "Diagram")


##### Open a new terminal and check the nodes status
![Alt text](docs/2.png?raw=true "Diagram")

##### Get the node termination handler daemonset pod running on this spot node
![Alt text](docs/1.png?raw=true "Diagram")

##### Open a new terminal and keep watching the logs from node termination handler on this spot node
![Alt text](docs/3.png?raw=true "Diagram")

##### Change the target capacity from 1 to 0 on the spot fleet in AWS console
![Alt text](docs/7.png?raw=true "Diagram")

##### Check the node status changed from Ready to Ready,ScheduledDisabled
![Alt text](docs/8.png?raw=true "Diagram")

##### Check the node termination handler logs on spot node for spot interruptions 
![Alt text](docs/10.png?raw=true "Diagram")

##### See that pods is now in the pendig state as it is evicted due to spot interruptions 
![Alt text](docs/11.png?raw=true "Diagram")