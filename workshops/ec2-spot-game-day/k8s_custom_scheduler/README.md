## EC2 Spot EKS Custom Scheduler


### Step0 :  Ensure CA is not running and manually scale ASGs with instances needed for your workload
 kubectl delete -f ~/environment/cluster-autoscaler/cluster_autoscaler.yml 

### Step1 :  Run the customer Scheduler locally on your development machine

Setup the kubeconfig on your machine and ensure basic command like 'kubectl get nodes' work

Ensure to have below lines enabled in Ec2SpotCustomScheduler.py

config.load_kube_config()
#config.load_incluster_config()

chmod +x Ec2SpotCustomScheduler.py
./Ec2SpotCustomScheduler.py

### Step2 :  Run the customer Scheduler in your K8S cluster as a pod - Create an ECR Repo

aws ecr create-repository \
    --repository-name ec2spotcustomscheduler \
    --image-scanning-configuration scanOnPush=true
    
### Step3 :  Build customer Scheduler container and push it to ECR

cd /home/ec2-user/environment/ec2-spot-workshops/workshops/ec2-spot-game-day/k8s_custom_scheduler

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 000474600478.dkr.ecr.us-east-1.amazonaws.com

Ensure to have below lines enabled in Ec2SpotCustomScheduler.py

#config.load_kube_config()
config.load_incluster_config()


docker build --no-cache -t ec2spotcustomscheduler .
docker tag ec2spotcustomscheduler:latest 000474600478.dkr.ecr.us-east-1.amazonaws.com/ec2spotcustomscheduler:latest
docker push 000474600478.dkr.ecr.us-east-1.amazonaws.com/ec2spotcustomscheduler:latest
 
### Step4 :  Build and Deploy the customer Scheduler onto OnDemand Instances
Update the docker image path in Ec2SpotCustomScheduler.yaml. Please note it will be deployed on the OnDemand instances to keep it running all the time.
NOTE: A ServiceAccount with necessary permissions needs to added to below Yaml to access the K8S objects.
kubectl apply  -f Ec2SpotCustomScheduler.yaml 

To run the custom scheduler manually on the devlopment machine
### Step5 :  Create a deployement with the custom scheduling information

Refer to sample file nginx.yaml

Add the below annotation to the deployment object
  annotations:
    Ec2SpotK8SCustomScheduler: 'true'  # This enables the custome scheduling for a deployment
    OnDemandBase: '1'  # number of min pods to be running on OnDemand, similar to ASG
    OnDemandAbovePercentage: '50' # % of pods beyond the base number of OnDemand pods
    SpotASGName: 'Ec2SpotEKS4-Ec2SpotNodegroup1' # NOT NEEDED for now. We can use it later if we want to scale ASG  
    OnDemandASGName: 'Ec2SpotEKS4-ODNodegroup1' # NOT NEEDED for now. We can use it later if we want to scale ASG  
    
    
    Add below to the pod spec 
    schedulerName: "Ec2SpotK8sScheduler"

    kubectl apply -f nginx.yaml
    

### Step6 : Monitor the logs for the custom scheduler
kubectl logs -f ec2spotcustomscheduler-78b6c6c989-bzn5x


### Step7 : Try changing the pod distribution by changing OnDemandBase, OnDemandAbovePercentage and replica

export EDITOR=vim
kubectl edit deploy nginx

check out the custom scheduler logs also check 'kubectl get pods'


### TODO List - Integration with K8S Cluster Autoscaler (CA)

1. K8S CA DOES NOT scale instances for the pods assigned to with custom scheduler. CA takes only default K8S scheduler into account.
2. Even the ASG is scaled manually and place the pods using custom scheduler, CA will terminate these nodes and pods.
3. One option is to use ASG scaling policies(ex: target tracking) instead of CA for scaling cluster

