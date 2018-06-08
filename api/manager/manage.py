#!/usr/bin/env python
import os

import click

from api.apps import create_app
from api.apps.extensions import sqldb
from api.apps.extensions import mongodb
from api.apps.ponos.utilities.mock_data import mock_shift_data, drop_ponos_collections
from api.apps.ponos.utilities.tests_cli import (
    cli_test_ponos_endpoints,
    cli_test_ponos_middleware,
    cli_test_ponos_models,
    cli_test_ponos
)
from api.apps.ponos.utilities.worker_cli import cli_worker_ponos
from api.apps.utilities.test_cli import cli_test_app_config


# Initialize Flask object.
app = create_app(os.getenv('SHIFTGIG_FLASK_CONFIG') or 'develop')


# Shell context.
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=sqldb, mongo=mongodb)


# Unit tests.
@app.cli.command()
def test_ponos_models():
    """Test Ponos models"""
    cli_test_ponos_models()


@app.cli.command()
def test_ponos_endpoints():
    """Test Ponos endpoints"""
    cli_test_ponos_endpoints()


@app.cli.command()
def test_ponos_middleware():
    """Test Ponos middleware"""
    cli_test_ponos_middleware()


@app.cli.command()
def test_ponos():
    """Test Ponos"""
    cli_test_ponos()


@app.cli.command()
def test_app_config():
    """Test application configuration"""
    cli_test_app_config()


@app.cli.command()
def test_all():
    """Test entire app"""
    cli_test_app_config()
    cli_test_ponos()


# Database operations.
@app.cli.command()
def db_bootstrap():
    """Save mock data to Mogno"""
    mock_shift_data()


@app.cli.command()
def db_clear():
    """Deletes from Mongo"""
    drop_ponos_collections()


# Ponos worker.
@app.cli.command()
@click.option('--app-config', default='develop', help='Application configuration context', required=False)
@click.option('--action', default='start', help='Daemon execution options', required=False)
@click.option('--pid', default='/tmp/ponosdaemon.pid', help='Daemon execution options', required=False)
def worker_ponos(action, app_config, pid):
    """Ponos worker manager"""
    cli_worker_ponos(app_config, action, pid)
