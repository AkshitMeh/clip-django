from django.test import TestCase, Client
from django.urls import reverse
from .models import Paste
from django.utils import timezone
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile

class PasteModelTest(TestCase):
    def test_create_text_paste(self):
        paste = Paste.objects.create(
            content_type='text',
            text_content='Hello, world!',
            code='1234',
            expires_at=timezone.now() + timedelta(days=1)
        )
        self.assertEqual(paste.text_content, 'Hello, world!')
        self.assertEqual(paste.content_type, 'text')

    def test_expired_paste(self):
        paste = Paste.objects.create(
            content_type='text',
            text_content='Expired',
            code='5678',
            expires_at=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(paste.expires_at < timezone.now())

    def test_create_file_paste(self):
        file = SimpleUploadedFile('test.txt', b'file content')
        paste = Paste.objects.create(
            content_type='file',
            file_content=file,
            code='9999',
            expires_at=timezone.now() + timedelta(days=1)
        )
        self.assertTrue(paste.file_content.name.endswith('.txt'))

class PasteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.text_paste = Paste.objects.create(
            content_type='text',
            text_content='View test',
            code='abcd',
            expires_at=timezone.now() + timedelta(days=1)
        )

    def test_home_view_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_display_text_paste(self):
        response = self.client.get(reverse('display_paste', kwargs={'code': self.text_paste.code}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View test')

    def test_display_expired_paste(self):
        expired = Paste.objects.create(
            content_type='text',
            text_content='Expired',
            code='exp1',
            expires_at=timezone.now() - timedelta(days=1)
        )
        response = self.client.get(reverse('display_paste', kwargs={'code': expired.code}))
        self.assertNotEqual(response.status_code, 200)

    def test_file_download(self):
        file = SimpleUploadedFile('download.txt', b'download content')
        file_paste = Paste.objects.create(
            content_type='file',
            file_content=file,
            code='file1',
            expires_at=timezone.now() + timedelta(days=1)
        )
        response = self.client.get(reverse('download_file', kwargs={'code': file_paste.code}))
        self.assertEqual(response.status_code, 200)
        content_disp = response.get('Content-Disposition')
        self.assertIn('.txt', content_disp)
