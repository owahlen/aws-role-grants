import unittest

import boto3
from moto import mock_aws

from kms.kms_client import KMSClient


class TestKMSClient(unittest.TestCase):

    @mock_aws
    def test_get_kms_keys(self):
        ### SETUP ###

        # Initialize a boto3 KMS client within the mock context
        client = boto3.client('kms')

        # Create fake KMS keys
        kms_key_1 = client.create_key(
            Description='Test key 1',
            Tags=[{'TagKey': 'Environment', 'TagValue': 'Development'}])
        kms_key_2 = client.create_key(
            Description='Test key 2'
        )

        # Initialize the RDSClient
        kms_client = KMSClient()

        ### WHEN ###

        # Call the method
        kms_keys = kms_client.get_kms_keys()

        ### THEN ###
        # Assert that we have 2 KMS keys
        self.assertEqual(len(kms_keys), 2)

        # Check that the first key has the correct tags
        key_1 = kms_keys[0]
        self.assertEqual(key_1['KeyId'], kms_key_1['KeyMetadata']['KeyId'])
        self.assertIn('arn:aws:kms', key_1['KeyArn'])
        self.assertEqual(key_1['Tags'], [{'TagKey': 'Environment', 'TagValue': 'Development'}])

        # Check that the second key has the correct tags
        key_2 = kms_keys[1]
        self.assertEqual(key_2['KeyId'], kms_key_2['KeyMetadata']['KeyId'])
        self.assertIn('arn:aws:kms', key_2['KeyArn'])
        self.assertEqual(key_2['Tags'], [])

if __name__ == '__main__':
    unittest.main()
