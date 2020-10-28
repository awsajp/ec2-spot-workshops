## EC2 Spot OD Fallback Strategy for EKS

For detailed Architecture diagram, please refer to EC2-Spot-OD-Fallback-Strategy.pptx

In this workshop, you will deploy the following:

### Step0 : Clone the Repo 
```bash
git clone https://github.com/jalawala/ec2-spot-workshops.git
cd /home/ec2-user/environment/ec2-spot-workshops/workshops/ec2-spot-od-failover strategies/eks
```

### Step1 : Deploy Priority Expander 
```bash
kubectl apply -f cluster-autoscaler-priority-expander.yaml
```

### Step2 : Deploy Spot and OnDemand Node Groups

```bash
eksctl create nodegroup -f spot_nodegroups.yml
```

### Step3 : Configure Spot ASG to simulate no capacity 
There are two ways to do this
1. configure lowest price
2. select some rare / high demand instances which may not be available for spot

### Step4: Deploy Cluster Autoscaler 
 
```bash
eksctl create nodegroup -f spot_nodegroups.yml
```

### Step5 : Watch the CA logs in a different terminal
 
```bash
kubectl logs -f deployment/cluster-autoscaler -n kube-system 2>&1 | tee spot_od.txt
```

### Step6 : Deploy Application
 
```bash
kubectl apply -f monte-carlo-pi-service.yml 
```
 
### Step7 : Watch CA logs 

you can filter logs with this regular expression in the nodepad++

(priority expander)|(Final scale-up plan)|(Setting asg)|(is unschedulable)|(Upcoming)|(is not ready for scaleup)|(auto_scaling_groups)

CA selects SPOT ASG as it is highest priority configured in the config map
```bash
Line 16713: I1028 16:01:40.579485       1 priority.go:167] priority expander: eksctl-eks-spot-demo-nodegroup-SPOT-NodeGroup-CTS7Q22CLVPT chosen as the highest available
```
 
CA selects sets desired capacity to 1 in SPOT ASG to scale at T1=**16:01:40.579582**
```bash
Line 16718: I1028 16:01:40.579582       1 auto_scaling_groups.go:221] Setting asg eksctl-eks-spot-demo-nodegroup-SPOT-NodeGroup-CTS7Q22CLVPT size to 1
```

CA checks SPOT ASG fo every 1 min to check node is provisioned
```bash
Line 16816: I1028 16:02:51.138867       1 auto_scaling_groups.go:407] Instance group eksctl-eks-spot-demo-nodegroup-SPOT-NodeGroup-CTS7Q22CLVPT has only 0 instances created while requested count is 1. Creating placeholder instance with ID i-placeholder-eksctl-eks-spot-demo-nodegroup-SPOT-NodeGroup-CTS7Q22CLVPT-0.
```


CA decides that SPOT ASG cannot provision nodes at T2=**16:06:41.903608**
So T2-T1 = 5min which is same as --max-node-provision-time=5m0s
```bash
Line 17205: W1028 16:06:41.903608       1 scale_up.go:325] Node group eksctl-eks-spot-demo-nodegroup-SPOT-NodeGroup-CTS7Q22CLVPT is not ready for scaleup - backoff
```


CA resets the desired capacity back to 0 in SPOT ASG
```bash
Line 17221: I1028 16:06:52.118816       1 auto_scaling_groups.go:221] Setting asg eksctl-eks-spot-demo-nodegroup-SPOT-NodeGroup-CTS7Q22CLVPT size to 0
```

CA selects OnDemand ASG as it is next highest priority configured in the config map
```bash
	Line 17237: I1028 16:07:02.356812       1 priority.go:167] priority expander: eksctl-eks-spot-demo-nodegroup-OnDemand-NodeGroup-1WBT5PP03OQ4J chosen as the highest available
```

CA sets desired capacity in OnDemand ASG for scale up
```bash
Line 17242: I1028 16:07:02.357006       1 auto_scaling_groups.go:221] Setting asg eksctl-eks-spot-demo-nodegroup-OnDemand-NodeGroup-1WBT5PP03OQ4J size to 2
```

So that means Spot to OnDemand failover is happening !!!
