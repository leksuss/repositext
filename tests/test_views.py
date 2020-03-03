#!/usr/bin/env python

from django.test import Client, TestCase
from tests.common import get_root_folder


class IndexTestCase(TestCase):
    def setUp(self):
        self.root_folder = get_root_folder()

    def test_get(self):
        client = Client()
        response = client.get('/docweb/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Dashboard' in response.content)


class RepositoryTestCase(TestCase):
    def setUp(self):
        self.root_folder = get_root_folder()

    def test_get(self):
        client = Client()
        response = client.get(f'/docweb/repository/folder/{self.root_folder.name}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'System root folder' in response.content)

