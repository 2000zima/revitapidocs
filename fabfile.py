import os
from configparser import ConfigParser

from fabric.api import local


def run_tests():
    local("python -m unittest tests.tests -b -v")


def run(env_name='dev'):
    """
    >>> fab run
    >>> fab run:staging
    >>> fab run:production
    """
    load_config(env_name)
    local("python run.py")


def load_config(env_name):
    """
    >>> fab run
    >>> fab run:staging
    >>> fab run:production
    """
    config = ConfigParser()
    config.read('.env')

    env = dict(config['default'])
    env.update(dict(config[env_name]))

    os.environ.update(env)
    print('Enviroment Set: [.env:{}]'.format(env_name))


def push(remote_name):
    local("git push {}".format(remote_name))


def rebuild_assets():
    os.environ.update({'FLASK_APP': 'app/__init__.py'})
    local('flask assets clean')
    local('flask assets build')


def upload_assets():
    local("python upload-s3-assets.py")


def deploy_staging():
    run_tests()
    load_config('staging')
    rebuild_assets()
    upload_assets()
    push('staging')


def deploy_production():
    run_tests()
    load_config('production')
    rebuild_assets()
    upload_assets()
    push('heroku')
    push('origin')
