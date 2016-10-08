'''import main Flask. This starts when run.py calls from app import app'''
import os
from flask import Flask
from flask_compress import Compress
from flask_assets import Bundle, Environment
from flask_caching import Cache

from app.assets import css_assets, js_assets
from app.assets import css_chm, js_chm
from app.logger import logger

# Config
app = Flask(__name__)
flask_config = os.environ['FLASK_CONFIG']
logger.info('** FLASK_CONFIG: {}'.format(flask_config))
app.config.from_object('app.config.{}'.format(flask_config))

Compress(app)
cache = Cache(app)
logger.info('** CACHE_TYPE: {}'.format(os.environ['CACHE_TYPE']))
if bool(os.getenv('CACHE_CLEAR', False)):
    cache.clear_cache()
    logger.info('** Cached cleared [CLEAR_CACHE] True')

# ASSETS
assets = Environment(app)
assets.debug = bool(int(os.getenv('ASSETS_DEBUG', False)))
assets.register('css_assets', css_assets)
assets.register('js_assets', js_assets)
assets.register('css_chm', css_chm)
assets.register('js_chm', js_chm)
logger.debug('ASSETS DEBUG: {}'.format(assets.debug))

from app import views, seo_response, errors
from app import assets
