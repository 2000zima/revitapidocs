from flask import render_template, request
from app import app
from app.logger import logger


@app.errorhandler(503)
@app.errorhandler(500)
@app.errorhandler(404)
def server_error(error):
    name = getattr(error, 'name', 'UNKNOWN')
    code = getattr(error, 'code', 0)
    description = getattr(error, 'description', None) or \
                  getattr(error, 'msg', 'UNKNOWN')

    error = {'name':name, 'code': code, 'description': description}
    logger.error('ERROR: {}|{}'.format(code, name))
    logger.error('ERROR AT: {}'.format(request.path))
    return render_template('error.html', error=error), int(code)
