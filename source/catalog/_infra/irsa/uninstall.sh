aws iam detach-role-policy --role-name catalog-rds-access-role --policy-arn arn:aws:iam::810913173032:policy/catalog-rds-access-policy
aws iam delete-policy --policy-arn arn:aws:iam::810913173032:policy/catalog-rds-access-policy
aws iam delete-role --role-name catalog-rds-access-role