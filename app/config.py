import os
from app.logger import logger


class Config(object):
    DEBUG = False
    TESTING = False
    STAGING = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATEDIR = os.path.join(BASEDIR, 'templates')
    DEFAULT_CACHE_EXP = 604800
    SEND_FILE_MAX_AGE_DEFAULT = DEFAULT_CACHE_EXP  # 60*60*24*7 = 1 Week
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    CACHE_TYPE = 'simple'

    FLASKS3_BUCKET_NAME = 'revitapidocs'
    FLASKS3_HEADERS = {'Cache-Control': 'max-age='.format(DEFAULT_CACHE_EXP)}
    FLASKS3_ONLY_MODIFIED = True
    FLASKS3_GZIP = True
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


class ProductionConfig(Config):
    PRODUCTION = True
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
    logger.info('*** STAGING IS ON - HEROKU')
    config = StagingConfig
elif is_production:
    logger.info('*** PRODUCTION CONFIG - HEROKU')
    config = ProductionConfig
else:
    logger.info('*** DEVELOPMENT CONFIG')
    config = DevelopmentConfig


#  ENV CONFIG VARS
#   REQUIRED:
#       SECRET_KEY
#       GITHUB_TOKEN
#   Mode
#       PRODUCTION = [1]  :  If One, No Debug, and env Key
#       STAGING = [1]  :  1 Same as Production, disable Bots and GA
#   DEBUG:
#        ASSETS_DEBUG = [0/1] Debug for Webassets
#        LOG_LEVEL = [ INFO/DEBUG.ERROR ]
