# Guidance for a Multi-Region Microservice on AWS

## Getting started

This guidance helps customers design and operate a multi-Region microservice based architecture for an e-commerce platform on AWS using services like Amazon Elastic Container Services, Amazon Aurora Global Tables, Route53 Application Recovery Controller (ARC) and Lambda functions. The solution is deployed across two Regions that can failover and failback from one Region to another in an automated fashion. It leverages Amazon Route 53 Application Recovery Controller to help with the regional failover using AWS Systems Manager document (SSM). AWS Systems Manager (SSM) runbook  toggles the Route53 Application Recovery Controller (ARC) routing control “off” which causes the managed Health Check for the region to enter a “Failed” state. SSM runbook executes Aurora Global Database managed failover which promotes the standby region to the primary for writes. SSM runbook recovers a copy of the old primary database from a snapshot and reconcile the data in the new primary database to the old and generates a missing transaction report. 

## Architecture
WIP

### 1. Operating in the active/active state
WIP

### 2. Cross Region Failover 
WIP


## Pre-requisites

* To deploy this example guidance, you need an AWS account (We suggest using a temporary or a development account to 
  test this guidance), and a user identity with access to the following services:

    * AWS CloudFormation
    * Amazon Virtual Private Cloud (VPC)
    * Amazon Elastic Compute Cloud (EC2)
    * Amazon Elastic Container Services (ECS)
    * Amazon Relational Database Service (RDS)
    * Amazon Aurora Global Database 
    * AWS Identity and Access Management (IAM)
    * AWS Secrets Manager
    * AWS Systems Manager
    * Amazon Route 53
    * AWS Lambda
    * Amazon CloudWatch
    * Amazon Simple Storage Service
* Install the latest version of AWS CLI v2 on your machine, including configuring the CLI for a specific account and region
profile.  Please follow the [AWS CLI setup instructions](https://github.com/aws/aws-cli).  Make sure you have a 
default profile set up; you may need to run `aws configure` if you have never set up the CLI before. 

* Install Python version 3.9 on your machine. Please follow the [Download and Install Python](https://www.python.org/downloads/) instructions.

* Install `make` for your OS if it is not already there.

### Regions

This demonstration by default uses `us-east-1` as the primary region and `us-west-2` as the backup region. These can be changed in the Makefile.

## Deployment

For the purposes of this workshop, we deploy the CloudFormation Templates and SAM Templates via a Makefile. For a production 
workload, you'd want to have an automated deployment pipeline.  As discussed in this 
[article](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/?did=ba_card&trk=ba_card), a multi-region pipeline should follow a staggered deployment schedule to reduce the blast radius of a bad deployment.  
Take particular care with changes that introduce possibly backwards-incompatible changes like schema modifications, and make use of schema versioning.


## Configuration
Before starting deployment process please update the following variables in the `deployment/Makefile`:

**ENV** - It is the unique variable that indicates the environment name. Global resources created, such as S3 buckets, use this name. (ex: -dev)

**PRIMARY_REGION** - The AWS region that will serve as primary for the workload

**STANDBY_REGION** - The AWS region that will serve as standby or failover for the workload

## Deployment Steps

We use make file to automate the deployment commands. The make file is optimized for [AWS Cloud9](https://aws.amazon.com/pm/cloud9/) which is Cloud Integrated Development Environment (IDE) for writing, running, and debugging code. Please go through this [document](https://docs.aws.amazon.com/cloud9/latest/user-guide/tutorial-create-environment.html) to know how to launch a AWS Cloud9 environment in the Primary Region.  

1. Deploy the full solution from the `deployment` folder
    ```shell
    make Makefile deploy
    ```

## Verify the deployment
WIP

## Observability
WIP

## Cleanup

Note: If you have created reconciliation Amazon Aurora Database Clusters and Database Instances in the Standby Region, please delete all those instances before going to the next step.

```
    aws rds delete-db-instance \
    --db-instance-identifier orders-recon-dbinstance-[add-uniqueid-here] \
    --skip-final-snapshot \
    --region us-west-2
```

Once the Database instance is deleted delete the database cluster using 

```
    aws rds delete-db-cluster \
    --db-cluster-identifier orders-recon-dbcluster-[add-uniqueid-here] \
    --skip-final-snapshot \
    --region us-west-2
```

1. Delete all the cloudformation stacks and associated resources from both the Regions, by running the following command from the `deployment` folder
    ```shell 
    make destroy-all
    ```


## Security
See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## License
This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.