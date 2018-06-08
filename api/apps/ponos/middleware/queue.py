import json
from uuid import uuid4
from flask import current_app

from api.apps.utilities.middleware.queue.queue import Queue


class PonosQueue(Queue):
    """
    API for Ponos service queue CRUD operations.
    """

    def __init__(self):
        # Call parent class __init__ with microservice specific SNS topic and SQS queue.
        super(PonosQueue, self).__init__(current_app.config['SQS_PONOS_Q_TOPIC'], current_app.config['SQS_PONOS_Q'])

    def _add_job(self, job_type, cache_attrs):
        """
        Create unique id for job, add serialized record to cache and cache record id to queue.
        Purposefully private. To ensure valid job types, implement new add_*_job method that
        calls _add_job(*, cache_attrs).

        Arguments:
             job_type (str): Job meta data about for worker processes
             cache_attrs (dict): Data to be stored in cache

        Return:
            job_uid (str): ID of record added to cache
        """

        # Create unique id for job
        job_uid = 'ponos::{0}::{1}'.format(job_type, str(uuid4().int))
        self.create_job(job_uid, job_type, cache_attrs)

        return job_uid

    def add_create_shift_job(self, cache_attrs=None):
        """
        Adds create shift job.

        Arguments:
            cache_attrs (dict): Data to be stored in cache

        Return:
            job_uid (str): ID of record added to cache
        """
        job_uid = self._add_job('create_shift', cache_attrs)

        return job_uid

    def safe_delete_shift(self, shift, message, cache_id):
        return self.safe_delete_job(shift, 'shift_id', message, cache_id)
