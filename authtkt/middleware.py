# -*- coding: utf-8 -*-
from django.contrib.auth import login
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.conf import settings
from authtkt.auth_tkt import AuthTktCookiePlugin
import logging

log = logging.getLogger(__name__)

USE_SESSION = getattr(settings, 'AUTHTKT_USE_SESSION',
                  'django.contrib.sessions.middleware.SessionMiddleware' in \
                                                settings.MIDDLEWARE_CLASSES)


def resolve(module):
    if module:
        module, meth = module.split(':')
        mod = __import__(module, {}, {}, [])
        return getattr(mod, meth)

    def empty(user):
        return user
    return empty

LOGOUT_URL = '/logout'


class AuthTktMiddleware(object):

    plugin = AuthTktCookiePlugin(settings.SECRET_KEY,
                                 **getattr(settings, 'AUTHTKT_OPTIONS', {}))
    callback = staticmethod(resolve(getattr(settings,
                                            'AUTHTKT_CALLBACK', None)))
    cookie_type = {'domain': 1, 'subdomain': 2}.get(
                            getattr(settings, 'AUTHTKT_DOMAIN', 0), 0)

    def identify(self, request, response):
        identity = {
                'repoze.who.userid': request.user.id,
                }
        cookies = self.plugin.remember(request.environ, identity)
        header, value = cookies[self.cookie_type]
        response[header] = value
        request.environ['authtkt.processed'] = True

    def forget(self, request, response):
        cookies = self.plugin.forget(request.environ, {})
        header, value = cookies[self.cookie_type]
        response[header] = value
        request.environ['authtkt.processed'] = True

    def process_request(self, request):
        request.user = AnonymousUser()
        identity = self.plugin.identify(request.environ.copy())
        if identity and 'repoze.who.plugins.auth_tkt.userid' in identity:
            user_id = identity['repoze.who.plugins.auth_tkt.userid']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = User(id=user_id)
                self.callback(user)
                user.save()
            request.user = user
            if USE_SESSION:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
        request.environ['authtkt.identify'] = self.identify
        request.environ['authtkt.forget'] = self.forget

    def process_response(self, request, response):
        if request.environ.get('authtkt.processed', False) is not True:
            try:
                is_anon = request.user.is_anonymous()
            except AttributeError:
                is_anon = True
            if LOGOUT_URL in request.META['PATH_INFO']:
                self.forget(request, response)
            elif not is_anon and \
                 self.plugin.cookie_name not in request.COOKIES:
                self.identify(request, response)
        return response
