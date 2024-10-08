import logging

from evaluation import database_roles
from logger.log import log

import pandas as pd

from iam.iam_client import IAMClient
from rds.rds_client import RDSClient



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
        print(df)


def main():
    log.setLevel(level=logging.INFO)

    # Step 1: Initialize the RDS and IAM clients
    rds_client = RDSClient()
    iam_client = IAMClient()

    # Step 2: Retrieve all RDS databases and job roles
    databases = rds_client.get_rds_databases()
    job_roles = iam_client.get_roles(prefix='job-role')

    # Step 3: Check if any roles have permissions on these databases
    results = database_roles.evaluate(databases, job_roles, iam_client)

    # Step 4: Convert results to a pandas DataFrame and print the table
    display_results(results)


if __name__ == '__main__':
    main()
