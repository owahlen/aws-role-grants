from logger.log import log

from s3.s3_client import get_s3_actions


def evaluate(buckets, job_roles, iam_client):
    results = []
    for index, bucket in enumerate(buckets):
        bucket_arn = bucket['BucketArn']
        bucket_name = bucket['BucketName']
        bucket_tags = bucket['Tags']

        log.info("Analyzing S3 bucket '{}' ({}/{})".format(bucket_name, index + 1, len(buckets)))

        for role in job_roles:
            role_arn = role['Arn']
            role_name = role['RoleName']
            log.debug("Analyzing role '{}' on '{}'".format(role_name, bucket_name))
            allowed_actions = iam_client.check_role_permissions(role_arn, get_s3_actions(), bucket_arn, bucket_tags)

            if allowed_actions:
                log.debug("Allowed actions of role on S3 bucket: '{}'".format(allowed_actions))
                results.append({
                    'service': 's3',
                    'resource': bucket_name,
                    'role': role_name,
                    'allowed_actions': ', '.join(allowed_actions),
                    'description': bucket_arn
                })

    return results
