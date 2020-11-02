#!/bin/bash 

# Install Test Pods 

kubectl create namespace rbac-test
kubectl create deploy nginx --image=nginx -n rbac-test


kubectl get all -n rbac-test


#Create a User 

aws iam create-user --user-name rbac-user
aws iam create-access-key --user-name rbac-user | tee /tmp/create_output.json


cat << EoF > rbacuser_creds.sh
export AWS_SECRET_ACCESS_KEY=$(jq -r .AccessKey.SecretAccessKey /tmp/create_output.json)
export AWS_ACCESS_KEY_ID=$(jq -r .AccessKey.AccessKeyId /tmp/create_output.json)
EoF


# Map an IAM User to K8s 



kubectl get configmap -n kube-system aws-auth -o yaml > aws-auth.yaml


cat << EoF >> aws-auth.yaml
data:
  mapUsers: |
    - userarn: arn:aws:iam::${ACCOUNT_ID}:user/rbac-user
      username: rbac-user
EoF


kubectl apply -f aws-auth.yaml


# Test the new user 

. rbacuser_creds.sh

# Create the Role and Binding
kubectl apply -f rbacuser-role.yaml
kubectl apply -f rbacuser-role-binding.yaml


kubectl get pods -n kube-system


# Cleanup 

unset AWS_SECRET_ACCESS_KEY
unset AWS_ACCESS_KEY_ID
kubectl delete namespace rbac-test
rm rbacuser_creds.sh
rm rbacuser-role.yaml
rm rbacuser-role-binding.yaml
aws iam delete-access-key --user-name=rbac-user --access-key-id=$(jq -r .AccessKey.AccessKeyId /tmp/create_output.json)
aws iam delete-user --user-name rbac-user
rm /tmp/create_output.json


kubectl apply -f aws-auth.yaml
rm aws-auth.yaml

