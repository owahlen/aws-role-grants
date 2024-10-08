import unittest

import boto3
from moto import mock_aws

from rds.rds_client import RDSClient


class TestRDSClient(unittest.TestCase):

    @mock_aws
    def test_get_rds_databases(self):
        ### SETUP ###

        # Initialize a boto3 RDS client within the mock context
        client = boto3.client('rds')

        # Create a fake RDS instance
        create_db_response = client.create_db_instance(
            DBInstanceIdentifier='test-db',
            MasterUsername='admin',
            MasterUserPassword='password',
            DBInstanceClass='db.t2.micro',
            Engine='postgres',
            AllocatedStorage=20,
        )
        db_arn = create_db_response['DBInstance']['DBInstanceArn']

        # Create a tag for the RDS instance
        client.add_tags_to_resource(
            ResourceName=db_arn,
            Tags=[
                {'Key': 'Team', 'Value': 'Test Team'}
            ]
        )

        # Initialize the RDSClient
        rds_client = RDSClient()

        ### WHEN ###

        # Call the method
        databases = rds_client.get_rds_databases()

        ### THEN ###

        # Assert the results
        self.assertEqual(len(databases), 1)
        self.assertEqual(databases[0]['DBInstanceIdentifier'], 'test-db')
        self.assertEqual(databases[0]['DBInstanceArn'], db_arn)
        self.assertEqual(databases[0]['Tags'], {'Team': 'Test Team'})


if __name__ == '__main__':
    unittest.main()
