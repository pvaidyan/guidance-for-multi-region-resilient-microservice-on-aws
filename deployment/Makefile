# Prerequisites:
# - kubectl
# - awscli


ENV="-dev"
PRIMARY_REGION=us-east-1
STANDBY_REGION=us-west-2
EKSCLUSTERVERSION=1.27

.DEFAULT_GOAL := test-creds
MAKE=/usr/bin/make

build:

deploy: test-creds primary_infrastructure secondary_infrastructure

primary_infrastructure:
	@aws cloudformation deploy --template ./regionalBaseInfra.yaml --region ${PRIMARY_REGION} \
	--stack-name baseInfra${ENV} --capabilities CAPABILITY_IAM --parameter-overrides Env=${ENV}
standby_infrastructure:

clean:
	@echo "To remove all stacks deployed by this solution, run 'make destroy-all'"

test-creds:
	@echo "Current AWS session:"
	@aws sts get-caller-identity

destroy-all:
	@echo "Removing all cloudformation stacks!!!"
	@aws cloudformation delete-stack --stack-name baseInfra${ENV} --region ${PRIMARY_REGION}
	@aws cloudformation wait stack-delete-complete --stack-name baseInfra${ENV} --region ${PRIMARY_REGION}