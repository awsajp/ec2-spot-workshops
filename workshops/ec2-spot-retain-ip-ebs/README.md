## EC2 Spot Workshop #10 : ec2-spot-retain-ip-ebs

The purpose of this workshop is to show to how to retain both EBS and private ips of the spot instances.

In this workshop, you will deploy the following:

    Creare an EFS storage
      - all spot instances maintain one state file in EFS to store secondary ip and EBS volume
      - SPOT_STATE_FILE - contains state (running or interruption) of spot instances
    Create Lauch Template with user data
    Create a Spot fleet of N (say 2 for testing) instances. One of the instance named MASTER and remaining are named as SLAVE_#N 
        - each instance runs a web server. Web Server runs from the secondary EBS volume and prints secondary ip and EBS volume id
        - when instance is launched for the first time, it allocates an secondary private ip and EBS volume
          and store them in EFS and set the state to IN_USE
        - it installs the spot interruption handler.  
        - when sinstance is interrupted, interruption handler detaches EBS volume and changes the state in EFS to AVAILABLE
        - when instances ls launched again, it checks if there is IP/EBS exists with state AVAILABLE
          if it finds, it ssiigns the secondary private ip and EBS to itself and changes the state
          
    Create a Spot fleet of N (say 2 for testing) instances
    Test the spot interruption by reducing the target capacity and increase it again after instance is terminated
    You can see that secondary private ip/EBS is always SAME for the instances across the spot terminations
    


    
### Step1 :  Create the EFS and Initial State files to store the persistance data/state for spot instances
 
### Step2 : Create a Launch Template

### Step3 : Create a Spot Fleet

### Step4 : Test retentikion of the Private IPs 

### Stpe5:  Cleanup

