import os
import shutil

from django.conf import settings
from django.test import TestCase

# Create your tests here.


class BaseTestClass(TestCase):
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
