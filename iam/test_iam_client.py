import unittest
from unittest.mock import patch

import boto3
from moto import mock_aws

from iam.iam_client import IAMClient


class TestIAMClient(unittest.TestCase):

    @mock_aws
    def test_get_roles_with_prefix(self):
        ### SETUP ###

        # Create a mock IAM client
        iam_client = boto3.client('iam', region_name='us-east-1')

        # Create mock roles
        iam_client.create_role(
            RoleName='test-role-1',
            AssumeRolePolicyDocument='{}'
        )
        iam_client.create_role(
            RoleName='job-role-2',
            AssumeRolePolicyDocument='{}'
        )
        iam_client.create_role(
            RoleName='test-role-3',
            AssumeRolePolicyDocument='{}'
        )

        # Initialize the IAMClient class
        my_iam_client = IAMClient()

        ### WHEN ###

        # Test get_roles with a prefix that matches "job-role"
        roles_with_prefix = my_iam_client.get_roles(prefix='job-')

        ### THEN ###

        # Assert only one role is returned that starts with 'job-'
        self.assertEqual(len(roles_with_prefix), 1)
        self.assertEqual(roles_with_prefix[0]['RoleName'], 'job-role-2')

    @mock_aws
    def test_get_roles_without_prefix(self):
        ### SETUP ###

        # Create a mock IAM client
        iam_client = boto3.client('iam', region_name='us-east-1')

        # Create mock roles
        iam_client.create_role(
            RoleName='test-role-1',
            AssumeRolePolicyDocument='{}'
        )
        iam_client.create_role(
            RoleName='job-role-2',
            AssumeRolePolicyDocument='{}'
        )
        iam_client.create_role(
            RoleName='test-role-3',
            AssumeRolePolicyDocument='{}'
        )

        # Initialize the IAMClient class
        my_iam_client = IAMClient()

        ### WHEN ###

        # Test get_roles without any prefix
        all_roles = my_iam_client.get_roles()

        ### THEN ###

        # Assert all roles are returned (3 in total)
        self.assertEqual(len(all_roles), 3)

    @mock_aws
    def test_get_roles_empty(self):
        ### SETUP ###

        # Initialize the IAMClient class without creating any roles
        my_iam_client = IAMClient()

        ### WHEN ###

        # Test get_roles with no roles created
        roles = my_iam_client.get_roles()

        ### THEN ###

        # Assert no roles are returned
        self.assertEqual(len(roles), 0)

    @mock_aws
    @patch('boto3.client')
    def test_check_role_permissions_allowed(self, mock_boto3_client):
        ### SETUP ###
        mock_iam_client = mock_boto3_client.return_value
        mock_iam_client.simulate_principal_policy.return_value = {
            'EvaluationResults': [
                {'EvalActionName': 'rds:DescribeDBInstances', 'EvalDecision': 'allowed'},
                {'EvalActionName': 'rds:StartDBInstance', 'EvalDecision': 'allowed'}
            ]
        }

        # Initialize the IAMClient class
        my_iam_client = IAMClient()

        ### WHEN ###

        # Test check_role_permissions with allowed actions
        allowed_actions = my_iam_client.check_role_permissions(
            role_arn='arn:aws:iam::123456789012:role/test-role',
            actions=['rds:DescribeDBInstances', 'rds:StartDBInstance', 'rds:StopDBInstance', 'rds:DeleteDBInstance'],
            resource_arn='arn:aws:rds:us-east-1:123456789012:db:test-db'
        )

        ### THEN ###

        # Assert allowed actions are returned
        self.assertEqual(allowed_actions, ['rds:DescribeDBInstances', 'rds:StartDBInstance'])


if __name__ == '__main__':
    unittest.main()
