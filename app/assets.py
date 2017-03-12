import os
from flask_assets import Bundle

join = os.path.join

scss = Bundle(
              'css/main.scss',
              'css/chm_content.scss',
              filters='libsass', output='packed/sass.css',
              depends='**/*.scss'
             )

css_assets = Bundle(scss,
                    # 'css/overrides.css',
                    'css/treeview.css',
                    filters='cssmin',
                    output='packed/packed.css'
                    )

js_assets = Bundle(
                #    'js/jquery.min.js',    #  loaded by CDN, use this when dev no internet
                #    'js/jquery.cookie.js', #  loaded by CDN
                #    'js/bootstrap.js',     #  loaded by CDN
                   'js/typed.js',
                   'js/navHelper.js',
                   'js/urlhelper.js',
                   'js/ajaxHelper.js',
                   'js/main.js',
                   'js/index.js',
                   filters='rjsmin',
                   output='packed/js_packed.js'
                  )

js_api_assets = Bundle(
                   'js/handlebars-v4.0.5.js',
                   'js/treeview.js',
                   'js/apiTreeview.js',
                   'js/apiSearch.js',
                #    'js/apiInsights.js',
                   filters='rjsmin',
                   output='packed/api_packed.js'
                  )
