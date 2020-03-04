#!/usr/bin/env python

from django.shortcuts import reverse
from django.test import Client, TestCase
from tests.common import get_root_folder, get_test_user, get_home_folder, TEST_USER


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

    def test_get(self):
        client = Client()
        response = client.get(f'/docweb/repository/folder/{self.root_folder.name}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'System root folder' in response.content)


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
