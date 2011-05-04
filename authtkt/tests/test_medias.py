# -*- coding: utf-8 -*-
import os
from unittest import TestCase
from django.conf import settings

class TestMedias(TestCase):

    def test_readme(self):
        filename = os.path.join(settings.MEDIA_ROOT, 'authtkt', 'README.txt')
        assert os.path.isfile(filename), filename

