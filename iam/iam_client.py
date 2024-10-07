import boto3

class IAMClient:
    def __init__(self, **kwargs):
        self.iam_client = boto3.client('iam', **kwargs)

    def get_roles(self, prefix = None):
        """Retrieve all IAM roles that start with the prefix."""
        paginator = self.iam_client.get_paginator('list_roles')
        job_roles = []

        for page in paginator.paginate():
            for role in page['Roles']:
                role_name = role['RoleName']
                if prefix is None or role_name.startswith(prefix):
                    job_roles.append(role)

        return job_roles

    def check_role_permissions(self, role_arn, actions, resource_arn, tags=None):
        """Check if the IAM role has permissions on the resource."""

        # Add the tags to the simulation context in which the role is evaluated
        context_entries = []
        if tags is not None:
            for key, value in tags.items():
                context_entries.append({
                    'ContextKeyName': f'aws:ResourceTag/{key}',
                    'ContextKeyValues': [value],
                    'ContextKeyType': 'string'
                })

        response = self.iam_client.simulate_principal_policy(
            PolicySourceArn=role_arn,
            ActionNames=actions,
            ResourceArns=[resource_arn],
            ContextEntries=context_entries
        )

        allowed_actions = []
        for result in response['EvaluationResults']:
            if result['EvalDecision'] == 'allowed':
                allowed_actions.append(result['EvalActionName'])

        return allowed_actions
