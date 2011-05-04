# -*- coding: utf-8 -*-
import os

try:
    from pluggableapp import PluggableApp
except ImportError:
    # pluggableapp is not installed
    pass


def pluggableapp(**kw):
    app = PluggableApp('authtkt', distribution='django-authtkt', **kw)
    app.append_app('authtkt')
    app.register_pattern('', r'^authtkt/', 'authtkt.urls')
    app.register_media(__file__)
    app.insert_templates(__file__)
    # app.initialize_settings(MYAPP_KEY='myappvalue', MYAPP_OTHER='other')
    return app

