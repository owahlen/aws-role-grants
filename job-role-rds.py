import boto3
import pandas as pd

from iam.iam_client import IAMClient
from rds.rds_client import RDSClient, get_rds_actions


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


def evaluate_roles_on_databases(databases, job_roles, iam_client):
    results = []
    for database in databases:
        db_arn = database['DBInstanceArn']
        db_identifier = database['DBInstanceIdentifier']
        db_tags = database['Tags']

        for role in job_roles:
            role_arn = role['Arn']
            role_name = role['RoleName']
            print("Evaluating allowed actions on database '{}' for role '{}':".format(db_identifier, role_name))
            allowed_actions = iam_client.check_role_permissions(role_arn, get_rds_actions(), db_arn, db_tags)

            if allowed_actions:
                print("-> '{}'".format(allowed_actions))
                results.append({
                    'db_identifier': db_identifier,
                    'role': role_name,
                    'allowed_actions': ', '.join(allowed_actions)
                })
    return results


def display_results(results):
    """Convert results to a pandas DataFrame and print the table."""
    df = pd.DataFrame(results, columns=['db_identifier', 'role', 'allowed_actions'])
    if df.empty:
        print("No roles with permissions found on the RDS databases.")
    else:
        # Configure pandas to display the entire DataFrame without truncation
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.show_dimensions', False)
        print(df)


def main():
    # Step 1: Initialize the RDS and IAM clients
    rds_client = RDSClient()
    iam_client = IAMClient()

    # Step 2: Retrieve all RDS databases and job roles
    databases = rds_client.get_rds_databases()
    job_roles = iam_client.get_roles(prefix='job-role')

    # Step 3: Check if any roles have permissions on these databases
    results = evaluate_roles_on_databases(databases, job_roles, iam_client)

    # Step 4: Convert results to a pandas DataFrame and print the table
    display_results(results)


if __name__ == '__main__':
    main()
