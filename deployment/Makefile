# Change these for your environment
ENV="-dev0"
PRIMARY_REGION=us-east-1
STANDBY_REGION=us-west-2
####

####
AWS_ACCOUNT_ID := $(shell aws sts get-caller-identity --output text|awk '{print $$1}')
AWS_PAGER:=''
.DEFAULT_GOAL := test-creds
MAKE=/usr/bin/make
DOCKER_BUILDKIT=0
COMPOSE_DOCKER_CLI_BUILD=0
####
deploy: deploy-ecs
deploy-apprunner: test-creds primary_infrastructure standby_infrastructure build-catalog primary_apps standby_apps
deploy-ecs: test-creds create-peer primary_infrastructure primary_ecs standby_infrastructure standby_ecs global_routing canaries
deploy-ecs-primary: test-creds primary_infrastructure primary_ecs

create-peer:
	@aws cloudformation deploy --template ./regionalVpc.yaml --region ${PRIMARY_REGION} \
	--stack-name baseVpc${ENV} --capabilities CAPABILITY_IAM --parameter-overrides Env=${ENV}
	@aws cloudformation deploy --template ./regionalVpc.yaml --region ${STANDBY_REGION} \
	--stack-name baseVpc${ENV} --capabilities CAPABILITY_IAM --parameter-overrides Env=${ENV}

build-catalog-primary: primary_infrastructure
	@cd ../source/catalog/; docker build -t catalog${ENV} .
	(aws ecr get-login-password --region $(PRIMARY_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(PRIMARY_REGION).amazonaws.com)
	docker tag catalog${ENV}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${PRIMARY_REGION}.amazonaws.com/catalog${ENV}:latest
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${PRIMARY_REGION}.amazonaws.com/catalog${ENV}:latest

build-catalog-standby: standby_infrastructure
	@cd ../source/catalog/; docker build -t catalog${ENV} .
	(aws ecr get-login-password --region $(STANDBY_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(STANDBY_REGION).amazonaws.com)
	docker tag catalog${ENV}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${STANDBY_REGION}.amazonaws.com/catalog${ENV}:latest
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${STANDBY_REGION}.amazonaws.com/catalog${ENV}:latest

primary_infrastructure: create-peer
	@aws cloudformation deploy --template ./regionalBaseInfra.yaml --region ${PRIMARY_REGION} \
	--stack-name baseInfra${ENV} --capabilities CAPABILITY_IAM --parameter-overrides Env=${ENV}

primary_apps: primary_infrastructure build-catalog-primary
	@aws cloudformation deploy --template ./appRunner.yaml --region ${PRIMARY_REGION} \
	--stack-name apps${ENV} --capabilities CAPABILITY_IAM --parameter-overrides Env=${ENV}

primary_ecs: create-peer primary_infrastructure build-catalog-primary
	@aws cloudformation deploy --template ./ecs.yaml --region ${PRIMARY_REGION} \
	--stack-name apps${ENV} --capabilities CAPABILITY_IAM --parameter-overrides Env=${ENV}

standby_infrastructure: create-peer
	@aws cloudformation deploy --template ./regionalBaseInfra.yaml --region ${STANDBY_REGION} \
	--stack-name baseInfra${ENV} --capabilities CAPABILITY_IAM --parameter-overrides Env=${ENV}

standby_apps: standby_infrastructure build-catalog-standby
	@aws cloudformation deploy --template ./appRunner.yaml --region ${STANDBY_REGION} \
	--stack-name apps${ENV} --capabilities CAPABILITY_IAM --parameter-overrides Env=${ENV}

standby_ecs: create-peer standby_infrastructure build-catalog-standby
	@aws cloudformation deploy --template ./ecs.yaml --region ${STANDBY_REGION} \
	--stack-name apps${ENV} --capabilities CAPABILITY_IAM --parameter-overrides Env=${ENV}

global_routing:
	@aws cloudformation deploy --region ${PRIMARY_REGION} --template ./globalRouting.yaml \
	--stack-name gr${ENV} --parameter-overrides DomainName=demo${ENV}.io Env=${ENV} 
canaries: global_routing
	@aws cloudformation deploy --region ${PRIMARY_REGION} --template ./canaries.yaml \
	--stack-name canaries${ENV} --parameter-overrides Env=${ENV} --capabilities CAPABILITY_IAM 
	@aws cloudformation deploy --region ${STANDBY_REGION} --template ./canaries.yaml \
	--stack-name canaries${ENV} --parameter-overrides Env=${ENV} --capabilities CAPABILITY_IAM 
clean:
	@echo "To remove all stacks deployed by this solution, run 'make destroy-all'"

test-creds:
	@echo "Current AWS session:"
	@aws sts get-caller-identity

destroy-all: destroy-peer destroy-apps
	@echo "Removing all cloudformation stacks!!!"

destroy-ecr:
	@aws ecr delete-repository --force --repository-name catalog${ENV} --region $(PRIMARY_REGION) --no-cli-pager
	@aws ecr delete-repository --force --repository-name catalog${ENV} --region $(STANDBY_REGION) --no-cli-pager

destroy-global_routing:
	@aws cloudformation delete-stack --stack-name gr${ENV} --region ${PRIMARY_REGION}
	@aws cloudformation wait stack-delete-complete --stack-name gr${ENV} --region ${PRIMARY_REGION}
	
destroy-peer: destroy-peer_primary destroy-peer_standby 

destroy-peer_standby: 
	@aws cloudformation delete-stack --stack-name baseVpc${ENV} --region ${STANDBY_REGION}
	@aws cloudformation wait stack-delete-complete --stack-name baseVpc${ENV} --region ${STANDBY_REGION}

destroy-peer_primary: destroy-peer_standby
	@aws cloudformation delete-stack --stack-name baseVpc${ENV} --region ${PRIMARY_REGION}
	@aws cloudformation wait stack-delete-complete --stack-name baseVpc${ENV} --region ${PRIMARY_REGION}

destroy-apps: destroy-infra 
	@aws cloudformation delete-stack --stack-name canaries${ENV} --region ${PRIMARY_REGION}
	@aws cloudformation wait stack-delete-complete --stack-name canaries${ENV} --region ${PRIMARY_REGION}
	@aws cloudformation delete-stack --stack-name canaries${ENV} --region ${STANDBY_REGION}
	@aws cloudformation wait stack-delete-complete --stack-name canaries${ENV} --region ${STANDBY_REGION}

	@aws cloudformation delete-stack --stack-name apps${ENV} --region ${PRIMARY_REGION}
	@aws cloudformation wait stack-delete-complete --stack-name apps${ENV} --region ${PRIMARY_REGION}
	@aws cloudformation delete-stack --stack-name apps${ENV} --region ${STANDBY_REGION}
	@aws cloudformation wait stack-delete-complete --stack-name apps${ENV} --region ${STANDBY_REGION}

destroy-infra: destroy-ecr destroy-peer
	@aws cloudformation delete-stack --stack-name baseInfra${ENV} --region ${STANDBY_REGION}
	@aws cloudformation wait stack-delete-complete --stack-name baseInfra${ENV} --region ${STANDBY_REGION}
	@aws cloudformation delete-stack --stack-name baseInfra${ENV} --region ${PRIMARY_REGION}
	@aws cloudformation wait stack-delete-complete --stack-name baseInfra${ENV} --region ${PRIMARY_REGION}