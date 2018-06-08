from boto import (
    sns,
    sqs
)
from boto.sqs.message import RawMessage


def sns_connection(config):
    """
    Initialize Boto SNS Client from FLask application configuration.

    Arguments:
        config (flask.config.Config)

    Return:
        sns_con (boto.sqs.connection.SNSConnection)
    """
    sns_con = sns.connect_to_region(config['AWS_REGION'], aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                                    aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])

    return sns_con


def sqs_connection(config):
    """
        Initialize Boto SQS Client from FLask application configuration.

        Arguments:
            config (flask.config.Config)

        Return:
            sns_con (boto.sqs.connection.SQSConnection)
        """
    sqs_con = sqs.connect_to_region(config['AWS_REGION'], aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
                                    aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'])

    return sqs_con


# Restrict module imports to exclude sns and sqs
__all__ = ['RawMessage', 'sqs_connection', 'sns_connection']
