from logger.log import log

from rds.rds_client import get_rds_actions


def evaluate(databases, job_roles, iam_client):
    results = []
    for index, database in enumerate(databases):
        db_instance_arn = database['DBInstanceArn']
        rds_db_arn = _get_rds_db_arn(database)
        db_identifier = database['DBInstanceIdentifier']
        db_tags = database['Tags']

        log.info("Analyzing database '{}' ({}/{})".format(db_identifier, index + 1, len(databases)))

        for role in job_roles:
            role_arn = role['Arn']
            role_name = role['RoleName']
            log.debug("Analyzing role '{}' on '{}'".format(role_name, db_identifier))
            allowed_actions = iam_client.check_role_permissions(role_arn, ['rds-db:connect'], rds_db_arn, db_tags)
            allowed_actions.extend(
                iam_client.check_role_permissions(role_arn, get_rds_actions(), db_instance_arn, db_tags))

            if allowed_actions:
                log.debug("Allowed actions of role on database: '{}'".format(allowed_actions))
                results.append({
                    'service': 'rds',
                    'resource': db_identifier,
                    'role': role_name,
                    'allowed_actions': ', '.join(allowed_actions),
                    'description': db_instance_arn
                })

    return results


def _get_rds_db_arn(database):
    db_instance_arn = database['DBInstanceArn']
    db_resource_id = database['DBResourceID']
    db_instance_arn_parts = db_instance_arn.split(':')
    region = db_instance_arn_parts[3]
    account_id = db_instance_arn_parts[4]
    resource_type = db_instance_arn_parts[5]
    assert resource_type == 'db', f"Invalid RDS instance ARN: {db_instance_arn}"
    return f"arn:aws:rds-db:{region}:{account_id}:dbuser:{db_resource_id}/*"
