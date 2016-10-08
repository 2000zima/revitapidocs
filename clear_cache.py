import os
from flask_caching import Cache

from app import app, logger

cache = Cache()

flask_config = os.environ['FLASK_CONFIG']
logger.info('** FLASK_CONFIG: {}'.format(flask_config))
app.config.from_object('app.config.{}'.format(flask_config))


def main():
    cache = Cache(app)

    with app.app_context():
        cache.clear()
        print('Cache Cleared.')

if __name__ == '__main__':
    main()
