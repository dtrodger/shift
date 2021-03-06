import ast
import logging
import os
import sys
import threading
import time

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(basepath)

from api.apps.utilities.middleware.queue.daemon import Daemon
from api.apps import create_app
from api.apps.ponos.middleware.db import PonosDB
from api.apps.ponos.middleware.queue import PonosQueue


class PonosWorker(Daemon):
    """
    API for Ponos worker to process queued jobs.
    """

    def __init__(self, app_config, *args, **kwargs):
        Daemon.__init__(self, *args, **kwargs)
        self.app_config = app_config

    def run(self, *args, **kwargs):
        # Run single thread
        timer_thread = threading.Thread(target=self.execute, args=[self.app_config])
        timer_thread.start()

    def stop(self):
        Daemon.stop(self)

    def execute(self, app_config):
        app = create_app(app_config)

        with app.app_context():
            try:
                ponos_db = PonosDB()
                ponos_q = PonosQueue()
                while True:
                    self.work_jobs(ponos_db, ponos_q, app.logger)
                    time.sleep(1)
            except Exception as e:
                app.logger.error('PonosWorker - {}'.format(e.message))

    def work_jobs(self, ponos_db, ponos_q, logger):
        """
        Pulls Redis cache id from SQS, gets Redis record, deserialize record, saves record into Mongo database.
        """
        # Get jobs from queue.
        # TODO - Rethink architecture. Attempting to pull jobs from an empty queue every seconds is not efficient.
        jobs = ponos_q.get_jobs()

        for job in jobs:

            # Ensure Redis record returned
            if job[0]:
                json_api_resource = ast.literal_eval(job[0])

                # Get job type
                job_type = ponos_q.get_job_type(job)

                # Call DB API job type method with cache data.

                shift = getattr(ponos_db, '{}_job'.format(job_type))(json_api_resource)

                # Delete job.
                sqs_message = job[1]
                cache_id = job[2]
                deleted = ponos_q.safe_delete_shift(shift, sqs_message, cache_id)

                if deleted:
                    logger.info('PonosWorker - Create Shift {}'.format(shift.shift_id))

                if not deleted:
                    logger.error('PonosWorker - failed job {}'.format(job[2]))
                    # TODO - handle failed jobs.
