# -*- coding: utf-8 -*-
from authtkt.tests.functionnal import *

class TestIndex(WebTest):

    def test_index(self):
        resp = self.app.get(reverse('authtkt_index'))
        resp.mustcontain('authtkt')

