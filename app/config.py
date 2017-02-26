import os
from app.utils.logger import logger


class Config(object):
    DEBUG = False
    TESTING = False
    STAGING = False
    PRODUCTION = False
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATEDIR = os.path.join(BASEDIR, 'templates')

    SEND_FILE_MAX_AGE_DEFAULT = 604800  # 60*60*24*7 = 1 Week
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')  # simple, redis
    CACHE_CLEAR = False

    GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
    CONSTRUCTOR_IO_AUTOCOMPLETE_KEY = os.environ['CONSTRUCTOR_IO_AUTOCOMPLETE_KEY']
    CONSTRUCTOR_IO_API_TOKEN = os.environ['CONSTRUCTOR_IO_API_TOKEN']

    FLASKS3_USE_CACHE_CONTROL = True
    FLASKS3_HEADERS = {'Cache-Control': 'max-age={}'.format(SEND_FILE_MAX_AGE_DEFAULT)}

    FLASKS3_ONLY_MODIFIED = False
    FLASKS3_GZIP = True

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    JSONIFY_PRETTYPRINT_REGULAR = False

    AVAILABLE_APIS = ['2015', '2016', '2017', '2017.1']
    API_DOCS_NAME = 'api_docs'
    API_DOCS_PATH = os.path.join(TEMPLATEDIR, API_DOCS_NAME)


class Production(Config):
    PRODUCTION = True
    ASSETS_DEBUG = bool(int(os.getenv('ASSETS_DEBUG', False)))
    FLASKS3_ACTIVE = FLASK_ASSETS_USE_S3 = bool(int(os.getenv('FLASKS3_ACTIVE', True)))
    FLASKS3_ACTIVE = FLASKS3_ACTIVE
    SECRET_KEY = os.environ['SECRET_KEY']
    FLASKS3_BUCKET_NAME = 'revitapidocs'


class Staging(Config):
    STAGING = True
    CACHE_CLEAR = bool(int(os.getenv('CACHE_CLEAR', 0)))
    ASSETS_DEBUG = bool(int(os.getenv('ASSETS_DEBUG', False)))
    FLASKS3_ACTIVE = FLASK_ASSETS_USE_S3 = bool(int(os.getenv('FLASKS3_ACTIVE', True)))
    DEBUG = False
    FLASKS3_BUCKET_NAME = 'revitapidocs-staging'
    SECRET_KEY = os.environ['SECRET_KEY']

class Development(Config):
    CACHE_CLEAR = True
    DEBUG = True
    SECRET_KEY = 'SuperSecretKey'
    ASSETS_DEBUG = bool(int(os.getenv('ASSETS_DEBUG', False)))
    FLASKS3_ACTIVE = bool(int(os.getenv('FLASKS3_ACTIVE', 0)))
    FLASK_ASSETS_USE_S3 = FLASKS3_ACTIVE
    FLASKS3_BUCKET_NAME = 'fake-bucket'

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


class Testing(Development):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'SuperSecretKey'
