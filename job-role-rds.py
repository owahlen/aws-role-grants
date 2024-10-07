import boto3
import pandas as pd

def get_job_roles():
    """Retrieve all IAM roles that start with 'job-role'."""
    iam_client = boto3.client('iam')
    paginator = iam_client.get_paginator('list_roles')
    job_roles = []

    for page in paginator.paginate():
        for role in page['Roles']:
            if role['RoleName'].startswith('job-role'):
                job_roles.append(role)

    return job_roles

def get_rds_databases():
    """Retrieve all RDS database instances."""
    rds_client = boto3.client('rds')
    db_instances = rds_client.describe_db_instances()
    databases = []

    for db in db_instances['DBInstances']:
        databases.append({
            'DBInstanceIdentifier': db['DBInstanceIdentifier'],
            'DBInstanceArn': db['DBInstanceArn']
        })

    return databases

def check_role_permissions_on_rds(role_arn, db_arn):
    """Check if the IAM role has permissions on the RDS instance."""
    iam_sim_client = boto3.client('iam')
    actions = [
        'rds:DescribeDBInstances',
        'rds:StartDBInstance',
        'rds:StopDBInstance',
        'rds:DeleteDBInstance'
    ]

    response = iam_sim_client.simulate_principal_policy(
        PolicySourceArn=role_arn,
        ActionNames=actions,
        ResourceArns=[db_arn]
    )

    allowed_actions = []
    for result in response['EvaluationResults']:
        if result['EvalDecision'] == 'allowed':
            allowed_actions.append(result['EvalActionName'])

    return allowed_actions

def main():
    # Step 1: Get all roles that start with 'job-role'
    job_roles = get_job_roles()

    # Step 2: Get all RDS databases
    databases = get_rds_databases()

    # Prepare data for pandas DataFrame
    results = []

    # Step 3: Check if any roles have permissions on these databases
    for role in job_roles:
        role_arn = role['Arn']
        role_name = role['RoleName']

        for db in databases:
            db_arn = db['DBInstanceArn']
            db_identifier = db['DBInstanceIdentifier']
            print("Evaluating role {} on database {}".format(role_name, db_identifier))
            allowed_actions = check_role_permissions_on_rds(role_arn, db_arn)

            if allowed_actions:
                results.append({
                    'role': role_name,
                    'db_identifier': db_identifier,
                    'allowed_actions': ', '.join(allowed_actions)
                })

    # Step 4: Convert results to a pandas DataFrame and print the table
    df = pd.DataFrame(results, columns=['role', 'db_identifier', 'allowed_actions'])
    if df.empty:
        print("No roles with permissions found on the RDS databases.")
    else:
        # Configure pandas to display the entire DataFrame without truncation
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        print(df)

if __name__ == '__main__':
    main()
