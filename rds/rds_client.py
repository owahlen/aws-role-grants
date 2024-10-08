import boto3


def get_rds_actions():
    return [
        'rds:DescribeDBInstances',
        'rds:StartDBInstance',
        'rds:StopDBInstance',
        'rds:DeleteDBInstance'
    ]


class RDSClient:
    def __init__(self, **kwargs):
        self.rds_client = boto3.client('rds', **kwargs)

    def get_rds_databases(self):
        """Retrieve all RDS database instances along with their tags."""
        db_instances = self.rds_client.describe_db_instances()
        databases = []

        for db in db_instances['DBInstances']:
            db_arn = db['DBInstanceArn']
            tags_response = self.rds_client.list_tags_for_resource(ResourceName=db_arn)
            tags = {tag['Key']: tag['Value'] for tag in tags_response['TagList']}

            databases.append({
                'DBInstanceIdentifier': db['DBInstanceIdentifier'],
                'DBInstanceArn': db_arn,
                'DBResourceID': db['DbiResourceId'],
                'Tags': tags
            })

        return databases
