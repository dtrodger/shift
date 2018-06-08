from flask import current_app

from api.apps.ponos.middleware.worker import PonosWorker


def cli_worker_ponos(app_config, action, pid):
    """
    CLI command function for starting Ponos worker daemon.

    Arguments:
        app_config (str): Flask application configuration
        action (str): daemon behavior
        pid (str): daemon process id
    """

    # Validate configuration.
    configs = ('develop', 'test', 'stage', 'prod')

    if app_config not in configs:
        raise AttributeError('Invalid worker Flask app configuration. Options include {}'.format(configs))

    try:
        # Initialize worker.
        gaia_worker = PonosWorker(app_config, pid)

        # Command worker.
        if action == 'start':
            gaia_worker.start()
        elif action == 'stop':
            gaia_worker.stop()
        elif action == 'restart':
            gaia_worker.restart()

        print('Ponos worker {} successful'.format(action))

    except Exception as e:
        current_app.logger.error('Ponos Worker - {}'.format(e.message))
        print('Ponos worker error. Check application logs for more information.')
