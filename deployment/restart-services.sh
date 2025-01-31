#!/bin/bash

# Initialize variables
ENV=""
SERVICES=()

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --env)
            ENV="$2"
            shift 2
            ;;
        --services)
            IFS=',' read -r -a SERVICES <<< "$2"
            shift 2
            ;;
        *)
            echo "Unknown parameter passed: $1"
            echo "Usage: $0 [--env <Env>] --services <Service1,Service2,...>"
            exit 1
            ;;
    esac
done

# Ensure at least one service is provided
if [ "${#SERVICES[@]}" -lt 1 ]; then
  echo "Usage: $0 [--env <Env>] --services <Service1,Service2,...>"
  exit 1
fi

# Function to get the cluster ARN with the specified tag using Resource Groups Tagging API
get_cluster_arn() {
  local tag_value
  if [ -z "$ENV" ]; then
    tag_value="mr-app-ecs-cluster"
  else
    tag_value="mr-app-ecs-cluster${ENV}"
  fi
  local cluster_arn
  cluster_arn=$(aws resourcegroupstaggingapi get-resources \
    --tag-filters Key=Name,Values=$tag_value \
    --resource-type-filters ecs:cluster \
    --query 'ResourceTagMappingList[0].ResourceARN' \
    --output text)
  echo "$cluster_arn"
}

# Function to force a new deployment for a given service
force_new_deployment() {
  local cluster_arn=$1
  local service_name=$2

  aws ecs update-service \
    --cluster "$cluster_arn" \
    --service "$service_name" \
    --force-new-deployment \
    --no-cli-pager

  echo "New deployment forced for service '$service_name' in cluster $cluster_arn."
}

# Get the cluster ARN
CLUSTER_ARN=$(get_cluster_arn)

# Check if the cluster ARN was found
if [ -z "$CLUSTER_ARN" ]; then
  if [ -z "$ENV" ]; then
    echo "Cluster with tag 'Name=mr-app-ecs-cluster' not found."
  else
    echo "Cluster with tag 'Name=mr-app-ecs-cluster${ENV}' not found."
  fi
  exit 1
fi

# Force a new deployment for each service in the list
for service in "${SERVICES[@]}"; do
  force_new_deployment "$CLUSTER_ARN" "$service"
done
