import os
from app.logger import logger


class Config(object):
    DEBUG = False
    TESTING = False
    STAGING = False
    PRODUCTION = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATEDIR = os.path.join(BASEDIR, 'templates')
    SEND_FILE_MAX_AGE_DEFAULT = 604800  # 60*60*24*7 = 1 Week
    CACHE_TYPE = 'simple'
    CACHE_REDIS_URL = os.getenv('REDIS_URL', None)
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


class Production(Config):
    CACHE_TYPE = 'redis'
    PRODUCTION = True
    SECRET_KEY = os.getenv('SECRET_KEY', None)


class Staging(Config):
    DEBUG = True
    STAGING = True
    SECRET_KEY = os.getenv('SECRET_KEY', None)

class Development(Config):
    DEBUG = True
    SECRET_KEY = 'SuperSecretKey'


class Testing(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'SuperSecretKey'


#  ENV CONFIG VARS
#   REQUIRED:
#       SECRET_KEY
#       GITHUB_TOKEN
#   FLASK_CONFIG
#       Production  :  If One, No Debug, and env Key
#       Staging  :  1 Same as Production, disable Bots and GA
#   DEBUG:
#        ASSETS_DEBUG = [0/1] Debug for Webassets
#        LOG_LEVEL = [ INFO/DEBUG.ERROR ]
