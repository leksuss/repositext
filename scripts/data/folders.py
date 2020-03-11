#!/usr/bin/env python

import os
import sys

import django
import script_utils

sys.path.append('.')

os.environ['DJANGO_SETTINGS_MODULE'] = script_utils.get_project_settings()

django.setup()

from django.contrib.auth.models import User  # noqa E402
from repositext.settings import SYS_ROOT_FOLDER_NAME # noqa E402
from apps.repo.models import Folder  # noqa E402

ADD_TEST_FOLDERS = True

admin_user = User.objects.get(username='admin')

init_folders = [
    {
        'name': SYS_ROOT_FOLDER_NAME,
        'description': 'System root folder.',
        'owner': admin_user,
    },
]

root_folders = [
    {
        'name': 'Home',
        'description': 'System home folder for users.',
        'owner': admin_user,
        'parent': SYS_ROOT_FOLDER_NAME,
    },
]

class FolderLoader:

    def _get_root_folder(self) -> Folder:
        return Folder.objects.get(name=SYS_ROOT_FOLDER_NAME)

    def add_init_folders(self) -> None:
        for each in init_folders:
            folder = Folder()
            for k, v in each.items():
                setattr(folder, k, v)
            folder.save()

    def add_test_folders(self, amount:int=4) -> None:
        for each in enumerate(range(amount), 1):
            folder = Folder()
            folder.name = f'TestFolder-{each[0]}'
            folder.description = f'Test Folder #{each[0]}'
            folder.owner = admin_user
            folder.parent = self._get_root_folder()
            folder.save()

    def add_root_folders(self) -> None:
        for each in root_folders:
            folder = Folder()
            folder.name = each['name']
            folder.description = each['description']
            folder.owner = each['owner']
            folder.parent = Folder.objects.get(name=each['parent'])
            folder.save()

    def run(self) -> None:
        print('  Adding system and example folders ...')
        self.add_init_folders()
        self.add_root_folders()

        if ADD_TEST_FOLDERS:
            self.add_test_folders()
            
        print('  Done.')


if __name__ == '__main__':
    folder_loader = FolderLoader()
    folder_loader.run()
