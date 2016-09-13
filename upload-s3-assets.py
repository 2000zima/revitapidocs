import flask_s3
from app import app
print('Uploading...')
flask_s3.create_all(app)
print('Done.')
