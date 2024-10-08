import boto3


def get_kms_actions():
    return [
        'kms:Encrypt',
        'kms:Decrypt',
        'kms:ReEncryptFrom',
        'kms:ReEncryptTo',
        'kms:GenerateDataKey',
        'kms:DescribeKey',
        'kms:CreateKey'
    ]


class KMSClient:
    def __init__(self, **kwargs):
        self.kms_client = boto3.client('kms', **kwargs)

    def get_kms_keys(self):
        """Retrieve all KMS keys along with their tags."""
        paginator = self.kms_client.get_paginator('list_keys')
        kms_keys = []
        for page in paginator.paginate():
            for key in page['Keys']:
                key_id = key['KeyId']
                # Retrieve key details
                key_metadata = self.kms_client.describe_key(KeyId=key_id)['KeyMetadata']
                key_arn = key_metadata['Arn']
                key_description = key_metadata['Description']

                # Get the tags for the key
                # todo: the admin role does not have permission to list the tags of the key
                #tags_response = self.kms_client.list_resource_tags(KeyId=key_arn)
                #tags = tags_response.get('Tags', [])
                tags = None

                # Append the key and its tags to the list
                kms_keys.append({
                    'KeyId': key_id,
                    'KeyArn': key_arn,
                    'Description': key_description,
                    'Tags': tags
                })
        return kms_keys
