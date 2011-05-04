# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from webtest import Form
from authtkt import models

__all__ = ('WebTest', 'UserWebTest', 'models', 'reverse')

class UserWebTest(WebTest):

    login = 'user1'
    extra_environ = {'REMOTE_USER': login}

    def setUp(self):
        super(UserWebTest, self).setUp()
        models.User.objects.create_user(self.login, '%s@example.com' % self.login)


