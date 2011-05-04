# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import simplejson
from authtkt.auth_tkt import AuthTktCookiePlugin

def resolve(module):
    if module:
        module, meth = module.split(':')
        meth = __import__(module, meth, [])
        return meth
    def empty(user):
        return user
    return empty

class AuthTktMiddleware(object):

    plugin = AuthTktCookiePlugin(settings.SECRET_KEY, **getattr(settings, 'AUTHTKT_OPTIONS', {}))
    callback = resolve(getattr(settings, 'AUTHTKT_CALLBACK', None))
    cookie_type = {'domain': 1, 'subdomain':2}.get(getattr(settings, 'AUTHTKT_DOMAIN', 0), 0)

    def process_request(self, request):
        identity = self.plugin.identify(request.environ.copy())
        import pdb;pdb.set_trace()
        if identity and 'repoze.who.plugins.auth_tkt.userid' in identity:
            user_id = identity['repoze.who.plugins.auth_tkt.userid']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = User(id=id)
                callback(user)
                user.save()
            request.user = user

    def process_response(self, request, response):
        if request.user.is_anonymous() and self.plugin.cookie_name not in request.COOKIES:
            cookies = plugin.forget(environ, {})
            header, value = cookies[self.cookie_type]
            response[header] = value
        if not request.user.is_anonymous() and self.plugin.cookie_name not in request.COOKIES:
            user = request.user
            identity = {
                    'repoze.who.userid': user.id,
                    }
            cookies = self.plugin.remember(request.environ, identity)
            header, value = cookies[self.cookie_type]
            response[header] = value
        return response



