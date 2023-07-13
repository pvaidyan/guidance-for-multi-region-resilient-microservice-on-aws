

account_id=$1
aws_region=$2
cluster_name=$3
service_account=$4
namespace=$5

policy_name="catalog-rds-access-policy"
role_name="catalog-rds-access-role"

cat >policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rds-db:connect"
      ],
      "Resource": [
        "arn:aws:rds-db:*:*:*:*/*"
      ]
    }
  ]
}
EOF

aws iam create-policy --policy-name "$policy_name" --policy-document file://policy.json

oidc_provider=$(aws eks describe-cluster --name "$cluster_name" --region "$aws_region" --query "cluster.identity.oidc.issuer" --output text | sed -e "s/^https:\/\///")


cat >trust-relationship.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::$account_id:oidc-provider/$oidc_provider"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "$oidc_provider:aud": "sts.amazonaws.com",
          "$oidc_provider:sub": "system:serviceaccount:$namespace:$service_account"
        }
      }
    }
  ]
}
EOF


aws iam create-role --role-name "$role_name" --assume-role-policy-document file://trust-relationship.json --description "Role for accessing catalog database"

aws iam attach-role-policy --role-name "$role_name" --policy-arn=arn:aws:iam::"$account_id":policy/"$policy_name"

kubectl annotate serviceaccount -n "$namespace" "$service_account" eks.amazonaws.com/role-arn=arn:aws:iam::"$account_id":role/$role_name
