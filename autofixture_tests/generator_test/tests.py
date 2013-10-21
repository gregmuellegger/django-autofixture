import os
from django import forms
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


class EmailForm(forms.Form):
    email = forms.EmailField()


class EmailGeneratorTests(TestCase):
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


class WeightedGeneratorTests(TestCase):
    def test_simple_weights(self):
        results = {"Red": 0, "Blue": 0}
        choices = [(generators.StaticGenerator("Red"), 50), 
                   (generators.StaticGenerator("Blue"), 50)]
        generate = generators.WeightedGenerator(choices)
        
        for i in xrange(1000):
            results[generate()] += 1

        MARGIN = 0.025

        self.assertTrue(0.5 - MARGIN < results["Red"]/1000.0 < 0.5 + MARGIN)
        self.assertTrue(0.5 - MARGIN < results["Blue"]/1000.0 < 0.5 + MARGIN)

    def test_complex_weights(self):
        results = {"frosh": 0, "soph": 0, "jr": 0, "sr": 0}
        choices = [(generators.StaticGenerator("frosh"), 35), 
                   (generators.StaticGenerator("soph"), 20),
                   (generators.StaticGenerator("jr"), 30),
                   (generators.StaticGenerator("sr"), 15)]
        generate = generators.WeightedGenerator(choices)
        
        for i in xrange(1000):
            results[generate()] += 1

        MARGIN = 0.025

        self.assertTrue(0.35 - MARGIN < results["frosh"]/1000.0 < 0.35 + MARGIN)
        self.assertTrue(0.20 - MARGIN < results["soph"]/1000.0 < 0.20 + MARGIN)
        self.assertTrue(0.30 - MARGIN < results["jr"]/1000.0 < 0.30 + MARGIN)
        self.assertTrue(0.15 - MARGIN < results["sr"]/1000.0 < 0.15 + MARGIN)


