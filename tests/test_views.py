#!/usr/bin/env python

from django.core.files import File
from django.core.files.base import ContentFile
from django.shortcuts import reverse
from django.test import Client, TestCase
from repositext.settings import SYS_ROOT_FOLDER_NAME
from tests.common import (
    get_root_folder, get_test_user, get_home_folder,
    TEST_USER, add_test_user
)
from apps.repo.models import Document, Folder


class IndexTestCase(TestCase):
    def setUp(self):
        self.root_folder = get_root_folder()

    def test_get(self):
        client = Client()
        client.login(username='admin', password='admin')
        response = client.get('/docweb/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Dashboard' in response.content)


class RepositoryTestCase(TestCase):
    def setUp(self):
        self.root_folder = get_root_folder()
        add_test_user()

    def test_get(self):
        client = Client()
        client.login(
            username=TEST_USER['username'],password=TEST_USER['password']
        )
        response = client.get(
            reverse('repo-view', args=[self.root_folder.id]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Current Folder:' in response.content)


class UserHomeTestCase(TestCase):
    def setUp(self):
        self.home_folder = get_home_folder()

    def test_get(self):
        username = TEST_USER['username']
        password = TEST_USER['password']
        client = Client()
        client.login(
            username='username',
            password='password',
        )
        response = client.get('/docweb/', follow=True)
        response = client.post(
            '/docweb/login/',
            {
                'username': username,
                'password': password,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Home folder for ' in response.content)


class AddDocumentTestCase(TestCase):
    def setUp(self):
        self.home_folder = get_home_folder()

    def test_post(self):
        client = Client()
        client.login(username='admin', password='admin')
        with open('test-documents/TestDocument1.docx', 'rb') as fp:
            response = client.post(
                reverse(
                    'add-document-view',
                    args=[self.home_folder.id, ]
                ),
                data = {
                    'name': 'TestDocument1.docx',
                    'description': 'Test Document',
                    'content_file': fp,
                },
                follow=True
            )
        self.assertEqual(response.status_code, 200)
        document = Document.objects.get(name='TestDocument1.docx')
        self.assertEqual(document.name, 'TestDocument1.docx')


class AddFolderTestCase(TestCase):
    def setUp(self):
        self.home_folder = get_home_folder()

    def test_post(self):
        client = Client()
        client.login(username='admin', password='admin')
        response = client.post(
            reverse(
                'repo-view',
                args=[self.home_folder.id, ]
            ),
            data = {
                'name': 'Test Folder1',
                'description': 'This is test folder #1',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        folder = Folder.objects.get(name='Test Folder1')
        self.assertEqual(folder.name, 'Test Folder1')
