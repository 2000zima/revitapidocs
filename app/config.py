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
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')  # simple, redis
    #CACHE_REDIS_URL = os.environ['REDIS_URL']

    GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
    CONSTRUCTOR_IO_AUTOCOMPLETE_KEY = os.environ['CONSTRUCTOR_IO_AUTOCOMPLETE_KEY']
    CONSTRUCTOR_IO_API_TOKEN = os.environ['CONSTRUCTOR_IO_API_TOKEN']

    FLASKS3_USE_CACHE_CONTROL = True
    FLASKS3_BUCKET_NAME = 'revitapidocs'
    FLASKS3_HEADERS = {'Cache-Control': 'max-age={}'.format(SEND_FILE_MAX_AGE_DEFAULT)}

    FLASKS3_ONLY_MODIFIED = True
    FLASKS3_GZIP = True
    FLASKS3_ACTIVE = bool(int(os.getenv('FLASKS3_ACTIVE', 1)))
    FLASK_ASSETS_USE_S3 = FLASKS3_ACTIVE

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    AVAILABLE_APIS = ['2015', '2016', '2017']
    JSONIFY_PRETTYPRINT_REGULAR = False


class Production(Config):
    PRODUCTION = True
    SECRET_KEY = os.environ['SECRET_KEY']


class Staging(Config):
    DEBUG = False
    STAGING = True
    SECRET_KEY = os.environ['SECRET_KEY']


class Development(Config):
    DEBUG = True
    SECRET_KEY = 'SuperSecretKey'
    FLASKS3_ACTIVE = bool(int(os.getenv('FLASKS3_ACTIVE', 0)))
    FLASK_ASSETS_USE_S3 = FLASKS3_ACTIVE

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    DEBUG_TB_PANELS = (
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        # 'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
    )


class Testing(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'SuperSecretKey'
