import os
from app.logger import logger


class Config(object):
    DEBUG = False
    TESTING = False
    STAGING = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATEDIR = os.path.join(BASEDIR, 'templates')
    SEND_FILE_MAX_AGE_DEFAULT = 604800  # 60*60*24*7 = 1 Week
    # GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

    GITHUB_TOKEN = '94e9d489cc282b34a41c9ea89a3c0f396fb42f58'
    # GITHUB_TOKEN = '94e9d489cc282b34a41c9ea89a3c0f396fb42f58zzzzz'

class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY', None)


class StagingConfig(Config):
    STAGING = True
    SECRET_KEY = os.getenv('SECRET_KEY', None)


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = '*)(EFUELKH!@#(&!_@&UQPasdasdj!(@&$_EFSDPFJSLK!@!@#1231)))'


is_production = bool(int(os.getenv('PRODUCTION', 0)))
logger.info('PRODUCTION={}'.format(is_production))

is_staging = bool(int(os.getenv('STAGING', 0)))
logger.info('STAGING={}'.format(is_staging))

if is_staging:
    logger.info('STAGING IS ON - HEROKU')
    config = StagingConfig
elif is_production:
    logger.info('PRODUCTION CONFIG - HEROKU')
    config = ProductionConfig
else:
    logger.info('DEVELOPMENT CONFIG')
    config = DevelopmentConfig
