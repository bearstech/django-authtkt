# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import simplejson
from authtkt.auth_tkt import AuthTktCookiePlugin
import logging

log = logging.getLogger(__name__)

def resolve(module):
    if module:
        module, meth = module.split(':')
        mod = __import__(module, {}, {}, [])
        return getattr(mod, meth)
    def empty(user):
        return user
    return empty

class AuthTktMiddleware(object):

    plugin = AuthTktCookiePlugin(settings.SECRET_KEY, **getattr(settings, 'AUTHTKT_OPTIONS', {}))
    callback = staticmethod(resolve(getattr(settings, 'AUTHTKT_CALLBACK', None)))
    cookie_type = {'domain': 1, 'subdomain':2}.get(getattr(settings, 'AUTHTKT_DOMAIN', 0), 0)

    def process_request(self, request):
        identity = self.plugin.identify(request.environ.copy())
        if identity and 'repoze.who.plugins.auth_tkt.userid' in identity:
            user_id = identity['repoze.who.plugins.auth_tkt.userid']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = User(id=user_id)
                self.callback(user)
                user.save()
            user.backend='django.contrib.auth.backends.ModelBackend'
            login(request, user)
            request.user = user

    def process_response(self, request, response):
        try:
            id = request.user.id
            is_anon = request.user.is_anonymous()
        except AttributeError:
            id = None
            is_anon = True
        if is_anon and self.plugin.cookie_name not in request.COOKIES:
            cookies = self.plugin.forget(request.environ, {})
            header, value = cookies[self.cookie_type]
            response[header] = value
        if not is_anon and self.plugin.cookie_name not in request.COOKIES:
            identity = {
                    'repoze.who.userid': request.user.id,
                    }
            cookies = self.plugin.remember(request.environ, identity)
            header, value = cookies[self.cookie_type]
            response[header] = value
        return response



