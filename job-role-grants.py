import logging

from evaluation import database_roles, bucket_roles
from logger.log import log

import pandas as pd

from iam.iam_client import IAMClient
from rds.rds_client import RDSClient
from s3.s3_client import S3Client


def display_results(results):
    """Convert results to a pandas DataFrame and print the table."""
    df = pd.DataFrame(results, columns=['service', 'resource', 'role', 'allowed_actions'])
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

    # Initialize the AWS clients
    iam_client = IAMClient()
    rds_client = RDSClient()
    s3_client = S3Client()

    # Retrieve all AWS resources and job roles
    databases = rds_client.get_rds_databases()
    buckets = s3_client.get_s3_buckets()
    job_roles = iam_client.get_roles(prefix='job-role')

    # Check if any roles has permissions on the resources
    results = database_roles.evaluate(databases, job_roles, iam_client)
    results.extend(bucket_roles.evaluate(buckets, job_roles, iam_client))

    # Convert results to a pandas DataFrame and print the table
    display_results(results)


if __name__ == '__main__':
    main()
