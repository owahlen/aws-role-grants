# aws-role-grants
Script to retrieves allowed actions on AWS resource based on IAM roles.

## Requirements
* [AWS CLI](https://aws.amazon.com/cli/)
  installed and authenticated to an AWS profile 
  (e.g. using [GSTS](https://github.com/ruimarinho/gsts)) that has the permissions to retrieve details on
  resources (RDS, S3, KMS) and that has permission to simulate IAM roles on these resources.
* Python 3

## Usage
Install the required Python packages:
```bash
$ pip install -r requirements.txt
```
Call the script:
```bash
$ python aws_role_grants.py
```

## Results
The script produces the Excel file `role_grants.xlsx` with the following columns:
* `service`: The AWS service that was analyzed (e.g. `kms`, `rds`, `s3`)
* `resource`: The name of the resource within this service that was analyzed (e.g. the DB name for RDS)
* `role`: The IAM role that was analyzed (e.g. `job-role-administrator`)
* `allowed_actions`: The actions that are allowed on the resource for the role (e.g. `rds:dbconnect`)
* `description`: Further description of the resource (e.g. the description of the KMS key or the ARN of the RDS DB)

## Limitations
* In its current version the script only analyzes roles whose name starts with `job-role`.
* Only the following services are supported: KMS, RDS, S3
* Only a subset of actions that are possible on the resources of these services are analyzed.
* For RDS, it is only analyzed that the role can connect to the DB but not as which user.
