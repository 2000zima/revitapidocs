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
                #    'js/jquery.min.js',    #  loaded by CDN
                #    'js/jquery.cookie.js', #  loaded by CDN
                #    'js/bootstrap.js',     #  loaded by CDN
                   'js/typed.js',
                   'js/handlebars-v4.0.5.js',
                   'js/treeview.js',
                   'js/main.js',
                   'js/urlhelper.js',
                   'js/ajaxHelper.js',
                   'js/apiTreeview.js',
                   'js/apiSearch.js',
                   'js/navHelper.js',
                   'js/index.js',
                #    'js/apiInsights.js',

                   filters='rjsmin',
                   output='packed/packed.js'
                  )

# js_chm = Bundle('scripts/overrides.js',
#                 # 'scripts/EventUtilities.js',
#                 # 'scripts/SplitScreen.js',
#                 # 'scripts/Dropdown.js',
#                 # 'scripts/script_manifold.js',
#                 # 'scripts/script_feedBack.js',
#                 # 'scripts/CheckboxMenu.js',
#                 # 'scripts/CommonUtilities.js',
#                 filters='rjsmin',
#                 output=join('packed/chm_packed.jss')
#                 )
