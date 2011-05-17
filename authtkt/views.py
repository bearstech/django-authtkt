# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django import shortcuts

def index(request):
    response = shortcuts.render_to_response('authtkt/index.html')
    request.environ['authtkt.forget'](request, response)
    return response
