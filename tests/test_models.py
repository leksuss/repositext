from django.contrib.auth.models import User
from django.test import TestCase
from apps.repo.models import Folder

class FolderTest(TestCase):
    def setUp(self):
        self.admin_user = User()
        self.admin_user.username = 'admin'
        self.admin_user.email = 'admin@localhost'
        self.admin_user.set_password('admin')
        self.admin_user.save()

    def test_folder_add(self):
        folder = Folder()
        folder.name = '-ROOT-'
        folder.description = 'The system root folder'
        folder.owner = self.admin_user
        folder.save()

        self.assertTrue(Folder.objects.get(name='-ROOT-'))
        self.assertTrue(Folder.objects.get(description='The system root folder'))
