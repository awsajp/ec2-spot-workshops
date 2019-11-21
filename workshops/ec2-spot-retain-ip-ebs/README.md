## EC2 Spot Workshop #10 : ec2-spot-retain-ip-ebs

The purpose of this workshop is to show to how to retain both EBS and private ips of the spot instances.

In this workshop, you will deploy the following:

    Creare an EFS storage
      - all spot instances maintain below two states in EFS
      - SPOT_INSTANCE_STATUS_FILE - contains state (running or interruption) of spot instances
      - SPOT_IP_STATUS_FILE contauns secondary private ip of the spot instances
    Create Lauch Template with user data
        - each instance runs a web server
        - when instance is launched for the first time, it allocates an secondary private ip
        - when instance is interrupted, it saves secondary private ip into EFS
        - when instances ls launched again, it checks for available secondary ip in EFS
          if it finds, it ssiigns the secondary private ip
        - it installs the spot interruption handler to save private ip into the EFS state
          
    Create a Spot fleet of N (say 2 for testing) instances
    Web server prints primary and secondary private ips
    Test the spot interruption by reducing the target capacity and increase it again after instance is terminated
    You can see that secondary private ip is always SAME for the instances across the spot terminations
    


    
### Step1 :  Create the EFS and Initial State files to store the persistance data/state for spot instances
 
### Step2 : Create a Launch Template

### Step3 : Create a Spot Fleet

### Step4 : Test retentikion of the Private IPs 

### Stpe5:  Cleanup

