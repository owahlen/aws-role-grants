from logger.log import log

from kms.kms_client import get_kms_actions


def evaluate(kms_keys, job_roles, iam_client):
    results = []
    for index, kms_key in enumerate(kms_keys):
        key_id = kms_key['KeyId']
        key_arn = kms_key['KeyArn']
        key_tags = kms_key['Tags']
        key_description = kms_key['Description']

        log.info("Analyzing KMS key '{}': {} ({}/{})".format(key_id, key_description, index + 1, len(kms_keys)))

        for role in job_roles:
            role_arn = role['Arn']
            role_name = role['RoleName']
            log.debug("Analyzing role '{}' on '{}'".format(role_name, key_id))
            allowed_actions = iam_client.check_role_permissions(role_arn, get_kms_actions(), key_arn, key_tags)

            if allowed_actions:
                log.debug("Allowed actions of role on KMS key: '{}'".format(allowed_actions))
                results.append({
                    'service': 'kms',
                    'resource': key_id,
                    'role': role_name,
                    'allowed_actions': ', '.join(allowed_actions),
                    'description': key_description
                })

    return results
