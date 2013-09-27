import os
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django.test.utils import override_settings
from autofixture import generators


class FilePathTests(TestCase):
    def test_media_path_generator(self):
        generate = generators.MediaFilePathGenerator(recursive=True)
        for i in range(10):
            path = generate()
            self.assertTrue(len(path) > 0)
            self.assertFalse(path.startswith('/'))
            media_path = os.path.join(settings.MEDIA_ROOT, path)
            self.assertTrue(os.path.exists(media_path))
            self.assertTrue(os.path.isfile(media_path))

    def test_media_path_generator_in_subdirectory(self):
        generate = generators.MediaFilePathGenerator(path='textfiles')
        for i in range(10):
            path = generate()
            self.assertTrue(path.startswith('textfiles/'))
            self.assertTrue(path.endswith('.txt'))


class DateTimeTests(TestCase):
    @override_settings(USE_TZ=True)
    def test_is_datetime_timezone_aware(self):
        generate = generators.DateTimeGenerator()
        date_time = generate()
        self.assertTrue(timezone.is_aware(date_time))

    @override_settings(USE_TZ=False)
    def test_is_datetime_timezone_not_aware(self):
        generate = generators.DateTimeGenerator()
        date_time = generate()
        self.assertFalse(timezone.is_aware(date_time))
