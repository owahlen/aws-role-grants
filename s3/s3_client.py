import boto3
from botocore.exceptions import ClientError


def get_s3_actions():
    return [
        's3:ListBucket',
        's3:DeleteBucket',
        's3:GetObject',
        's3:PutObject',
        's3:DeleteObject',
    ]


def get_bucket_arn(bucket_name):
    return f"arn:aws:s3:::{bucket_name}"


def get_bucket_tags(self, bucket_name):
    """Retrieve tags for a specific S3 bucket."""
    try:
        tags_response = self.s3_client.get_bucket_tagging(Bucket=bucket_name)
        tags = {tag['Key']: tag['Value'] for tag in tags_response['TagSet']}
    except ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchTagSet':
            raise e
        tags = {}
    return tags


class S3Client:
    def __init__(self, **kwargs):
        self.s3_client = boto3.client('s3', **kwargs)

    def get_s3_buckets(self):
        """Retrieve all S3 buckets along with their tags."""
        response = self.s3_client.list_buckets()
        buckets = []

        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            bucket_arn = get_bucket_arn(bucket_name)
            tags = get_bucket_tags(self, bucket_name)

            buckets.append({
                'BucketName': bucket_name,
                'BucketArn': bucket_arn,
                'Tags': tags
            })

        return buckets
