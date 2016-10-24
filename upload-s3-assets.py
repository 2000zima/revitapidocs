import flask_s3
from app import app

import logging
logger = logging.getLogger('flask_s3')
logger.setLevel(logging.DEBUG)

print('Uploading Assets to S3 Bucket...')
flask_s3.create_all(app)

print('Done.')
