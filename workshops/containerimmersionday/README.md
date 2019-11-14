## ContainerImmersionDay - Lab 1 : Getting Started with Docker and ECR Lab
   

   

### 1. Setting up the VPC 


### 2. Setting up the IAM user and roles



### 3. Launching the Cluster


### 4. Launching the Workstation

$ ssh -i cert.pem ec2-user@[public DNS]
$ sudo yum update -y
$ sudo yum install -y docker
$ sudo service docker start

$ sudo usermod -a -G docker ec2-user
$ docker info

 
### 5. Prepping the Docker images

$ curl -O https://s3-us-west-2.amazonaws.com/apn-bootcamps/microservice-ecs-2017/ecs-lab-code-20170524.tar.gz

$ tar -xvf ecs-lab-code-20170524.tar.gz
$ cd <path/to/project>/aws-microservices-ecs-bootcamp-v2/web
$ docker build -t ecs-lab/web .
$ docker images
$ docker run -d -p 3000:3000 ecs-lab/web
$ docker ps 
$ curl localhost:3000/web
$ cd ../api 
$ docker build -t ecs-lab/api .
$ docker images
$ docker run -d -p 8000:8000 ecs-lab/api
$ curl localhost:8000/api



### 6. Creating container registries with ECR


### 7. Configuring the AWS CLI

$ aws configure
$ aws configure
AWS Access Key ID: <leave empty> 
AWS Secret Access Key: <leave empty> 
Default region name [us-east-1]: us-east-1
Default output format [json]: <leave empty> 

$ aws ecr get-login
aws ecr get-login --region us-east-1

### 8. Pushing our tested images to ECR

$ docker tag ecs-lab/web:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/ecs-lab-web:latest
$ docker push <account_id>.dkr.ecr.us-east-1.amazonaws.com/ecs-lab-web:latest

$ docker tag ecs-lab/api:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/ecs-lab-api:latest
$ docker push <account_id>.dkr.ecr.us-east-1.amazonaws.com/ecs-lab-api:latest



## ContainerImmersionDay - Lab 2 : Getting Started with ECS



### 9. Creating the ALB

### 10. Creating the Task Definitions

### 11. Creating the Services

### 12. Testing our service deployments from the console and the ALB

### 13. More in-depth logging with CloudWatch

### 14. Cleanup
