from api.apps.ponos.middleware.worker import PonosWorker


def cli_worker_ponos(action, app_config):
    """
    CLI command function for starting Ponos worker daemon.

    Arguments:
         action (str): daemon behavior
    """

    # Validate configuration.
    configs = ('develop', 'test', 'stage', 'prod')

    if app_config not in configs:
        raise AttributeError('Invalid worker Flask app configuration. Options include {}'.format(configs))

    # Initialize worker.
    gaia_worker = PonosWorker(app_config, '/tmp/ponosdaemon.pid')

    # Command worker.
    if action == 'start':
        gaia_worker.start()
    elif action == 'stop':
        gaia_worker.stop()
    elif action == 'restart':
        gaia_worker.restart()
