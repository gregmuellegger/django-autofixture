from autofixture_tests.models import ImageModel, dummy_storage
import os
from operator import truediv

from django import forms
from django.conf import settings
from django.utils import timezone
from django.test.utils import override_settings
from PIL import Image

from autofixture import generators, AutoFixture
from . import FileSystemCleanupTestCase


class FilePathTests(FileSystemCleanupTestCase):
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


class DateTimeTests(FileSystemCleanupTestCase):
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


class EmailForm(forms.Form):
    email = forms.EmailField()


class EmailGeneratorTests(FileSystemCleanupTestCase):
    def test_email(self):
        generate = generators.EmailGenerator()
        form = EmailForm({'email': generate()})
        self.assertTrue(form.is_valid())

    def test_email_with_static_domain(self):
        generate = generators.EmailGenerator(static_domain='djangoproject.com')
        email = generate()
        self.assertTrue(email.endswith('djangoproject.com'))
        email = generate()
        self.assertTrue(email.endswith('djangoproject.com'))


class WeightedGeneratorTests(FileSystemCleanupTestCase):
    def test_simple_weights(self):
        results = {"Red": 0, "Blue": 0}
        choices = [(generators.StaticGenerator("Red"), 50),
                   (generators.StaticGenerator("Blue"), 50)]
        generate = generators.WeightedGenerator(choices)

        runs = 10000

        for i in range(runs):
            results[generate()] += 1

        MARGIN = 0.025

        self.assertTrue(0.5 - MARGIN < truediv(results["Red"], runs) < 0.5 + MARGIN)
        self.assertTrue(0.5 - MARGIN < truediv(results["Blue"], runs) < 0.5 + MARGIN)

    def test_complex_weights(self):
        results = {"frosh": 0, "soph": 0, "jr": 0, "sr": 0}
        choices = [(generators.StaticGenerator("frosh"), 35),
                   (generators.StaticGenerator("soph"), 20),
                   (generators.StaticGenerator("jr"), 30),
                   (generators.StaticGenerator("sr"), 15)]
        generate = generators.WeightedGenerator(choices)

        runs = 10000

        for i in range(runs):
            results[generate()] += 1

        MARGIN = 0.025

        self.assertTrue(0.35 - MARGIN < truediv(results["frosh"], runs) < 0.35 + MARGIN, results["frosh"] / 1.0 * runs)
        self.assertTrue(0.20 - MARGIN < truediv(results["soph"], runs) < 0.20 + MARGIN)
        self.assertTrue(0.30 - MARGIN < truediv(results["jr"], runs) < 0.30 + MARGIN)
        self.assertTrue(0.15 - MARGIN < truediv(results["sr"], runs) < 0.15 + MARGIN)


class ImageGeneratorTests(FileSystemCleanupTestCase):
    def test_image_generator(self):
        generate = generators.ImageGenerator()
        media_file = generate()

        file_path = os.path.join(settings.MEDIA_ROOT, media_file)
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, 'rb') as f:
            image = Image.open(f)
            self.assertTrue(image.size in generators.ImageGenerator.default_sizes)

    def test_width_height(self):
        media_file = generators.ImageGenerator(125, 225).generate()
        file_path = os.path.join(settings.MEDIA_ROOT, media_file)
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, 'rb') as f:
            image = Image.open(f)
            self.assertTrue(image.size, (125, 225))

    def test_filenames_dont_clash(self):
        media_file = generators.ImageGenerator(100, 100).generate()
        file_path1 = os.path.join(settings.MEDIA_ROOT, media_file)
        self.assertTrue(os.path.exists(file_path1))

        media_file = generators.ImageGenerator(100, 100).generate()
        file_path2 = os.path.join(settings.MEDIA_ROOT, media_file)
        self.assertTrue(os.path.exists(file_path2))

        self.assertNotEqual(file_path1, file_path2)

    def test_path(self):
        self.cleanup_dirs.append('mycustompath/withdirs')

        media_file = generators.ImageGenerator(path='mycustompath/withdirs').generate()
        file_path = os.path.join(settings.MEDIA_ROOT, media_file)
        self.assertTrue(os.path.exists(file_path))

        self.assertTrue(media_file.startswith('mycustompath/withdirs/'))
        self.assertTrue('_autofixture' not in media_file)

    def test_storage(self):
        """Storage is handled properly if defined on a field"""
        o = AutoFixture(ImageModel).create_one()

        self.assertTrue(dummy_storage.exists(o.imgfield.name))
