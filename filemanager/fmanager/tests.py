from django.test import TestCase
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage


class TestStaticFiles(TestCase):
    def test_images(self):
        abs_path = finders.find('fmanager.css')
        self.assertTrue(staticfiles_storage.exists(abs_path))
