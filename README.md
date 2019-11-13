## Ec2 Spot Workshop - running-amazon-ec2-workloads-at-scale
   
   
 
    An AWS CloudFormation stack, which will include:
        An Amazon Virtual Private Cloud (Amazon VPC) with subnets in two Availability Zones
        An AWS Cloud9 environment
        Supporting IAM policies and roles
        Supporting security groups
        An Amazon EFS file system
        An Amazon S3 bucket to use with AWS CodeDeploy
    An Amazon EC2 launch template
    An Amazon RDS database instance
    An Application Load Balancer (ALB) with a listener and target group
    An Amazon EC2 Auto Scaling group, with:
        A scheduled scaling action
        A dynamic scaling policy
    An AWS CodeDeploy application deployment
    An AWS Systems Manager run command to emulate load on the service



   
   
-- INSERT --                                                 
Collection of workshops to demonstrate best practices in using Amazon EC2 Spot Instances. https://aws.amazon.com/ec2/spot/

Website for this workshops is available at https://ec2spotworkshops.com

## Building the Workshop site

The content of the workshops is built using [hugo](https://gohugo.io/). 

### Local Build
To build the content
 * clone this repository
 * [install hugo](https://gohugo.io/getting-started/installing/)
 * The project uses [hugo learn](https://github.com/matcornic/hugo-theme-learn/) template as a git submodule. To update the content, execute the following code
```bash
pushd themes/learn
git submodule init
git submodule update --checkout --recursive
popd
```
 * Run hugo to generate the site, and point your browser to http://localhost:1313
```bash
hugo serve -D
```

### Containerized Development

The image can also serve as a development enviornment using [docker-compose](https://docs.docker.com/compose/).
The following command will spin up a container exposing the website at [localhost:1313](http://localhost:1313) and mount `config.toml` and the directories `./content`, `./layouts` and `./static`, so that local changes will automatically be picked up by the development container.

```
$ docker-compose up -d  ## To see the logs just drop '-d'
Starting ec2-spot-workshops_hugo_1 ... done
```

## License

This library is licensed under the Amazon Software License.
