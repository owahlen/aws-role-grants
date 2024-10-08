import logging

from evaluation import database_roles, bucket_roles, kms_roles
from iam.iam_client import IAMClient
from kms.kms_client import KMSClient
from logger.log import log
from output.results import write_results_to_excel
from rds.rds_client import RDSClient
from s3.s3_client import S3Client


def main():
    log.setLevel(level=logging.INFO)

    # Initialize the AWS clients
    iam_client = IAMClient()
    kms_client = KMSClient()
    rds_client = RDSClient()
    s3_client = S3Client()

    # Retrieve all AWS resources and job roles
    kms_keys = kms_client.get_kms_keys()
    databases = rds_client.get_rds_databases()
    buckets = s3_client.get_s3_buckets()
    job_roles = iam_client.get_roles(prefix='job-role')

    # Check if any roles has permissions on the resources
    results = kms_roles.evaluate(kms_keys, job_roles, iam_client)
    results.extend(database_roles.evaluate(databases, job_roles, iam_client))
    results.extend(bucket_roles.evaluate(buckets, job_roles, iam_client))

    # Write results to an Excel file
    write_results_to_excel(results, 'role_grants.xlsx')


if __name__ == '__main__':
    main()
