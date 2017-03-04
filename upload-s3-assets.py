import flask_s3
from app import app

import logging
logger = logging.getLogger('flask_s3')
logger.setLevel(logging.DEBUG)

# TODO: Implement API Clear, maybe CLI

print('Uploading Assets to S3 Bucket...')
bucket_name = app.config['FLASKS3_BUCKET_NAME']

if input('Bucket is [{}]. Confirm? [y]'.format(bucket_name)) == 'y':
    flask_s3.create_all(app)
    print('Done.')
else:
    print('Canceled')
