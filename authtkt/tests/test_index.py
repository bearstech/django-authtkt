# -*- coding: utf-8 -*-
from authtkt.tests.functionnal import *

class TestIndex(UserWebTest):

    def test_setcookie(self):
        resp = self.app.get('/admin/', user=self.login)
        cookies = resp.headers.getall('Set-Cookie')
        self.assertEqual(len([c for c in cookies if 'auth_tkt="' in c]), 1)


    def test_logout(self):
        resp = self.app.get('/admin/logout/', user=self.login)
        cookies = resp.headers.getall('Set-Cookie')
        self.assertEqual(len([c for c in cookies if 'auth_tkt="INVALID"' in c]), 1)

    def test_forget(self):
        resp = self.app.get('/authtkt/', user=self.login)
        cookies = resp.headers.getall('Set-Cookie')
        self.assertEqual(len([c for c in cookies if 'auth_tkt="INVALID"' in c]), 1)


