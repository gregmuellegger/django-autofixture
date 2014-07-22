import os
import shutil

from django.conf import settings
from django.test import TestCase


class FileSystemCleanupTestCase(TestCase):
    def setUp(self):
        self.cleanup_dirs = ['_autofixture']

    def tearDown(self):
        for path in self.cleanup_dirs:
            img_folder = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.exists(img_folder):
                shutil.rmtree(img_folder)
