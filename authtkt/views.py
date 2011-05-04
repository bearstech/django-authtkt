# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django import shortcuts

def index(request):

    return shortcuts.render_to_response('authtkt/index.html')
