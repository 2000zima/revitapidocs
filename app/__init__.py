'''import main Flask. This starts when run.py calls from app import app'''
import os
from flask import Flask
from flask_compress import Compress
from flask_assets import Bundle, Environment
from flask_caching import Cache
from flask_s3 import FlaskS3
from flask_debugtoolbar import DebugToolbarExtension

from app.assets import css_assets, js_assets
from app.utils.logger import logger

# Config
app = Flask(__name__)
compress = Compress()
flasks3 = FlaskS3()
cache = Cache()
toolbar = DebugToolbarExtension()

flask_config = os.environ['FLASK_CONFIG']
logger.info('** FLASK_CONFIG: {}'.format(flask_config))
app.config.from_object('app.config.{}'.format(flask_config))

compress.init_app(app)
flasks3.init_app(app)
cache.init_app(app)
toolbar.init_app(app)

logger.info('** CACHE_TYPE: {}'.format(os.environ['CACHE_TYPE']))
if bool(int(os.getenv('CACHE_CLEAR', 0))):
    cache.clear()
    logger.info('** Cached cleared [CLEAR_CACHE] True')

# ASSETS
assets = Environment(app)
assets.debug = bool(int(os.getenv('ASSETS_DEBUG', False)))
assets.register('css_assets', css_assets)
assets.register('js_assets', js_assets)
logger.debug('ASSETS DEBUG: {}'.format(assets.debug))

logger.debug('FLASK S3 ACTIVE: {}'.format(app.config['FLASKS3_ACTIVE']))
logger.debug('FLASK S3 ASSETS ACTIVE: {}'.format(app.config['FLASK_ASSETS_USE_S3']))

from app import views, seo_response, errors
from app import assets
