import json

from api.apps.extensions.amazon_aws import (
    sns_connection,
    sqs_connection,
    RawMessage
)
from flask import current_app

from api.apps.extensions import redis_cache


class Queue(object):
    """
    API for queue CRUD operations. Meant to be inherited by microservice queue class.
    Note that this class is designed to handle management of a SQS q and SNS topic.
    """
    def __init__(self, sns_topic, sns_q):
        # Get Flask application configuration.
        self.config = current_app.config
        self.redis_cache = redis_cache.get_api()

        # Initialize SQS Client and set other relevant attributes.
        self.sqsconn = sqs_connection(self.config)
        self.queue = self.sqsconn.get_queue(sns_q)

        # Initialize SNS Client
        self.snsconn = sns_connection(self.config)
        self.sns_topic = sns_topic
        self.sns_message = RawMessage

    def create_job(self, cache_id, job_type, cache_attrs):
        """
        Adds serialized record to Redis. Publishes messages to SNS containing serialized records uuid. SQS queue
        subscribed SNS topic will receive message attributes.

        Arguments:
             cache_id (str): Redis cache id
             job_type (str): Job meta data about for worker processes
             cache_attrs (dict)

        Return:
            (True) if successful, (False) if failed
        """

        try:
            # Set cache attributes to Redis.
            self.redis_cache.set(cache_id, cache_attrs)

        except Exception as e:
            # TODO - catch more specific errors. Implement better solution than returning False for failed redis sets.
            current_app.logger.error('Redis - {}'.format(e.message))

            return False

        try:
            data = json.dumps(dict(cache_id=cache_id, event_type=job_type))
            message = dict(default='', sqs=data)

            # Publish message to SNS.
            self.snsconn.publish(target_arn=self.sns_topic, message=json.dumps(message), message_structure='json')

        except Exception as e:
            # TODO - catch more specific errors. Implement better solution than returning False for failed SNS publish.
            current_app.logger.error('SNS - {}'.format(e.message))

            return False

        return True

    def _read_queue(self):
        """
        Reads and returns RawMessages from SQS queue.

        Return:
            (list): SQS RawMessages if successful (False) if not successful
        """
        try:
            current_app.logger.info(self.queue)
            self.queue.set_message_class(self.sns_message)
            messages = self.sqsconn.receive_message(self.queue, number_messages=10, wait_time_seconds=6,
                                                visibility_timeout=12)
        except Exception as e:
            current_app.logger.error('SQS - {}'.format(e.message))
            return False

        return messages

    def safe_delete_job(self, record, record_id, message, cache_id):
        """
        Deletes job from SQS and Redis if worker process created db record from job.

        Return:
            (True) if job successful, (False) if job not successful
        """

        # Ensure record created from job has id.
        if getattr(record, record_id):
            self.queue.delete_message(message)
            self.redis_cache.delete(cache_id)
            return True
        else:
            return False

    def get_jobs(self):
        """
        Requests SQS Messages. Uses Message content to get record from Redis. Returns all Message associated Redis
        records.

        Arguments:
            job_type (str): SQS queue related job.
        Return:
            (list): Redis records.
        """
        messages = self._read_queue()

        jobs = list()

        if messages:
            for message in messages:
                message_content = json.loads(json.loads(message.get_body())['Message'])
                cache_id = message_content['cache_id']
                cache_record = self.redis_cache.get(cache_id)
                jobs.append([cache_record, message, cache_id])

        return jobs

    def clear_cache(self):
        """
        Delete all keys in the current Redis database.

        Return:
            (True)
        """
        return self.redis_cache.flushdb()

    def clear_queue(self):
        """
        Clears SQS Queue

        Return:
            (True)
        """
        return self.queue.clear()

    @staticmethod
    def get_job_type(job):
        """
        Gets job type from job.

        Arguments:
            job (list): message returned from _read_queue

        Return:
            job_type (str) if valid job, else (False)
        """
        try:
            job_type = job[2].split('::')[1]
        except Exception as e:
            current_app.logger.error('Job - {}'.format(e.message))

            return False

        return job_type
