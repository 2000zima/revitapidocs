import os
import json
import time

ENCODING_READ = 'utf-8-sig'
ENCODING_WRITE = 'utf-8'
IGNORE_ERRORS = False


def open_html(filename, directory='.', ignore_errors=IGNORE_ERRORS):
    """ Opens Html. Handles encoding and errors"""
    filepath = os.path.join(directory, filename)
    # with open(filepath, 'r', encoding="utf-16-sig") as fp:
    try:
        with open(filepath, 'r', encoding=ENCODING_READ) as fp:
            html_content = fp.read()
    except Exception as errmsg:
        print('File: {}'.format(errmsg))
        print('Error: {}'.format(errmsg))
        if not ignore_errors:
            raise
    else:
        return html_content


def write_html(string, filename, directory='.', ignore_errors=IGNORE_ERRORS):
    """ Writes Html. Handles encoding and errors"""
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    try:
        with open(filepath, 'w', encoding=ENCODING_WRITE) as fp:
            # Enforce Encoding Took care of BOM Caracter
            fp.write(string)
    except Exception as errmsg:
        print('Error writing html: {}'.format(errmsg))
        print('File: {}'.format(errmsg))
        import pdb; pdb.set_trace()
        if not ignore_errors:
            raise
    else:
        return filename


def dump_json(data, filepath, ignore_errors=IGNORE_ERRORS, indent=1, minify=True):
    """ Dumps Data as JSON """
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        with open(filepath, 'w') as fp:
            json.dump(data, fp, indent=indent)
        if minify:
            min_json_out = filepath.replace('.json', '_min.json')
            with open(min_json_out, 'w') as fp:
                json.dump(data, fp, indent=None)

    except Exception as errmsg:
        print('Error: {}'.format(errmsg))
        print('File: {}'.format(filepath))
        if not ignore_errors:
            raise
    else:
        return True


def load_json(filepath):
    """ Load Data as JSON """
    try:
        with open(filepath, 'r') as fp:
            json_data = json.load(fp)
    except Exception as errmsg:
        print('Error: {}'.format(errmsg))
        raise
    else:
        return json_data


class Timer(object):
    "Time and TimeIt Decorator"
    def __init__(self):
        self.start_time = time.time()

    def stop(self):
        end_time = time.time()
        duration = end_time - self.start_time
        return duration

    @staticmethod
    def time_function(name):
        def wrapper(func):
            def wrap(*ags, **kwargs):
                logger.debug('START: {}'.format(name))
                t = Timer()
                rv = func(*ags, **kwargs)
                duration = t.stop()
                logger.debug('Done: {} sec'.format(duration))
                return rv
            return wrap
        return wrapper
