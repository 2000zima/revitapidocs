import os
from flask_assets import Bundle

join = os.path.join

scss = Bundle(
            #   'css/index.scss',
              'css/main.scss',
              filters='libsass', output='packed/sass.css',
              depends='**/*.scss'
              )

css_assets = Bundle(#'css/yeti.css',
                    # 'css/main.css',
                    scss,
                    'css/overrides.css',
                    'css/treeview.css',
                    filters='cssmin',
                    output='packed/packed.css'
                    )

js_assets = Bundle(
                   'js/jquery.min.js',
                   'js/jquery.cookie.js',
                   'js/bootstrap.js',
                   'js/main.js',
                   'js/treeview.js',
                   'js/typed.js',
                   'js/mustache.js',
                   filters='rjsmin',
                   output='packed/packed.js'
                   )


css_chm = Bundle('styles/Presentation.css',
                 output=join('packed/chm_packed.css')
                 )

js_chm = Bundle('scripts/overrides.js',
                # 'scripts/EventUtilities.js',
                # 'scripts/SplitScreen.js',
                # 'scripts/Dropdown.js',
                # 'scripts/script_manifold.js',
                # 'scripts/script_feedBack.js',
                # 'scripts/CheckboxMenu.js',
                # 'scripts/CommonUtilities.js',
                filters='rjsmin',
                output=join('packed/chm_packed.jss')
                )
