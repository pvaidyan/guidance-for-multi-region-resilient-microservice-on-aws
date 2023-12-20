#!/bin/bash
set -eo pipefail
ARTIFACT_BUCKET=$(cat bucket-name.txt)


# aws cloudformation create-stack \
#     --stack-name cr-dr-role  --region us-east-1  \
#     --template-body file://crdr-roles.yaml --capabilities CAPABILITY_NAMED_IAM

# aws cloudformation create-stack \
#     --stack-name cr-dr-ssm-automation  --region us-east-1  \
#     --template-body file://cross-region-orders-db-ssm.yaml --capabilities CAPABILITY_NAMED_IAM

aws cloudformation package --template-file restore-reconcile-orders-ssm.yaml --region us-west-2 --s3-bucket $ARTIFACT_BUCKET --output-template-file out.yaml
aws cloudformation deploy --template-file out.yaml --stack-name reconciliation-lambda --region us-west-2 --capabilities CAPABILITY_NAMED_IAM
