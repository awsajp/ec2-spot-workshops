# Tally Solution Architecture on EC2 Spot

## Managing the EKS clusters


To list clusters, use:

```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names C3
```


To create a cluster

```bash
aws autoscaling update-auto-scaling-group --auto-scaling-group-names C3 --mixed-instances-policy update.json

aws autoscaling update-auto-scaling-group --auto-scaling-group-names C3 --mixed-instances-policy update.json
     --network-configuration "awsvpcConfiguration={subnets=[$VPCPublicSubnets],securityGroups=[$SECURITY_GROUP],assignPublicIp="ENABLED"}" 
```

To check the status of the cloud formation stack, use:

```bash
'eksctl utils describe-stacks --region=us-east-1 --cluster=eks-spot-managed-node-groups
```



For more details about a specific cluster group you can use:

```bash
aws eks describe-cluster  --name eksworkshop
```

To list updates in a cluster, use:

```bash
aws eks list-updates --name eksworkshop
```

To describe an update in a cluster, use:

```bash
aws eks describe-update --name eksworkshop --update-id c9997d32-f29a-470a-bc80-616ced04cae6
```



## Managing the managed node groups

To select suitable instance types, you can use the ec2-instance-selector tool:

```bash
ec2-instance-selector --vcpus=4 --memory=16 --cpu-architecture=x86_64 --gpus=0 --burst-support=false
```

To see create the spot managed node groups, you can use:

```bash
eksctl create nodegroup --cluster eks-spot-managed-node-groups --instance-types m5.xlarge,m4.xlarge,m5a.xlarge,m5d.xlarge,m5n.xlarge,m5ad.xlarge,m5dn.xlarge --managed --spot --name spot-4vcpu-16gb --asg-access --nodes-max 20
```

You can run the following command to list the nodes labled with SPOT

```bash
kubectl get nodes --selector=eks.amazonaws.com/capacityType=SPOT
```

Apply the cluster autoscaler manifest file from the official GitHub repository to your cluster.

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
```


Open the cluster autoscaler deployment for editing:

```bash
kubectl edit deployment cluster-autoscaler -n kube-system
```





Find the line with --node-group-auto-discovery and modify <YOUR CLUSTER NAME> to the right cluster name. In this example, eks-spot-managed-node-groups

Lastly, check that cluster autoscaler started successfully by looking at the logs:
```bash
kubectl -n kube-system logs -f deployment.apps/cluster-autoscaler
```

Lastly, check that cluster autoscaler started successfully by looking at the logs:
```bash
kubectl -n kube-system logs -f deployment.apps/cluster-autoscaler
```


Apply the manifest file to the cluster:

```bash
kubectl apply -f nginx-spot-demo.yaml
```

Get the list of nodes based on the label
```bash
kubectl get no -l eks.amazonaws.com/capacityType=SPOT
```

Run kubectl describe to check what pods those nodes have running.

```bash
kubectl describe node <one of the nodes from the output of the previous command>
```

Scale the NGINX deployment and confirm that cluster autoscaler increases the size of the managed node group running Spot Instances
```bash
kubectl scale deployment nginx-spot-demo --replicas=20
```

You can also check the cluster autoscaler logs to confirm it identified the pending pods, and have chosen an Auto Scaling group to scale out

```bash
kubectl logs deployment/cluster-autoscaler -n kube-system --tail 500 | grep scale_up
```

For more details about a specific managed node group you can use:


```bash
 aws eks describe-nodegroup --cluster-name eksworkshop --nodegroup-name SpotMNG
```

Add a new label to the node


```bash
 aws eks  update-nodegroup-config --cluster-name eksworkshop --nodegroup-name <value>
[--labels <value>]
[--scaling-config <value>]
[--client-request-token <value>]
[--cli-input-json <value>]
[--generate-cli-skeleton <value>]

```

## Cleanup the resources 


To list clusters, use:

```bash
kubectl delete deployment nginx-spot-demo

eksctl delete nodegroup on-demand-4vcpu-16gb --cluster eks-spot-managed-node-groups

eksctl delete nodegroup spot-4vcpu-16gb --cluster eks-spot-managed-node-groups

eksctl delete cluster eks-spot-managed-node-groups
```
