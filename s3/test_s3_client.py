import unittest

import boto3
from moto import mock_aws

from s3.s3_client import S3Client


class TestS3Client(unittest.TestCase):

    @mock_aws
    def test_get_s3_buckets(self):
        ### SETUP ###

        # Initialize a boto3 RDS client within the mock context
        client = boto3.client('s3')

        # Create a mocked RDS instance
        client.create_bucket(Bucket='test-bucket-1', CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'})
        client.create_bucket(Bucket='test-bucket-2', CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'})

        # Create a tag for the RDS instance
        client.put_bucket_tagging(
            Bucket='test-bucket-2',
            Tagging={
                'TagSet': [
                    {'Key': 'Env', 'Value': 'Prod'},
                    {'Key': 'Owner', 'Value': 'TeamA'}
                ]
            }
        )

        # Initialize the RDSClient
        rds_client = S3Client()

        ### WHEN ###

        # Call the method
        buckets = rds_client.get_s3_buckets()

        ### THEN ###
        sorted_buckets = sorted(buckets, key=lambda x: x['BucketName'])
        expected_buckets = [
            {
                'BucketName': 'test-bucket-1',
                'BucketArn': 'arn:aws:s3:::test-bucket-1',
                'Tags': {}
            },
            {
                'BucketName': 'test-bucket-2',
                'BucketArn': 'arn:aws:s3:::test-bucket-2',
                'Tags': {'Env': 'Prod', 'Owner': 'TeamA'}
            }
        ]

        # Assert that the returned value matches the expected output
        self.assertEqual(sorted_buckets, expected_buckets)


if __name__ == '__main__':
    unittest.main()
