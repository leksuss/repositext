#!/usr/bin/env python

import os
import sys

import django
import script_utils

sys.path.append('.')

os.environ['DJANGO_SETTINGS_MODULE'] = script_utils.get_project_settings()

django.setup()

from django.contrib.auth.models import User  # noqa E402
from django.core.files import File
from django.core.files.base import ContentFile
from repositext.settings import SYS_ROOT_FOLDER_NAME
from apps.repo.models import Document, Folder, DocumentVersion  # noqa E402

ADD_TEST_DOCUMENTS = True

admin_user = User.objects.get(username='admin')
root_folder = Folder.objects.get(name=SYS_ROOT_FOLDER_NAME)
default_doc_version = '0.1.0'

documents = [
    {
        'path_to_file': 'test-documents/TestDocument1.docx',
        'name': 'Test Document 1.docx',
        'parent': Folder.objects.get(name='TestFolder-1', parent=root_folder),
        'description': 'A test docx document',
        'owner': admin_user,
    },
    {
        'path_to_file': 'test-documents/TestDocument2.docx',
        'name': 'Test Document 2.docx',
        'parent': Folder.objects.get(name='TestFolder-1', parent=root_folder),
        'description': 'A test docx document',
        'owner': admin_user,
    },
    {
        'path_to_file': 'test-documents/TestDocument3.docx',
        'name': 'Test Document 3.docx',
        'parent': Folder.objects.get(name='TestFolder-2', parent=root_folder),
        'description': 'A test docx document',
        'owner': admin_user,
    },
    {
        'path_to_file': 'test-documents/TestDocument4.docx',
        'name': 'Test Document 4.docx',
        'parent': Folder.objects.get(name='TestFolder-3', parent=root_folder),
        'description': 'A test docx document',
        'owner': admin_user,
    },
    {
        'path_to_file': 'test-documents/TestDocument5.docx',
        'name': 'Test Document 5.docx',
        'parent': Folder.objects.get(name='TestFolder-4', parent=root_folder),
        'description': 'A test docx document',
        'owner': admin_user,
    },
    {
        'path_to_file': 'test-documents/TestDocument1.docx',
        'name': 'Test Document 1.docx',
        'parent': root_folder,
        'description': 'A test docx document',
        'owner': admin_user,
    },
    {
        'path_to_file': 'test-documents/TestDocument2.docx',
        'name': 'Test Document 2.docx',
        'parent': root_folder,
        'description': 'A test docx document',
        'owner': admin_user,
    },
]


if __name__ == '__main__':
    print('  Adding test documents ...')
    if ADD_TEST_DOCUMENTS:
        for doc in documents:
            document = Document()
            document.name = doc['name']
            document.parent = doc['parent']
            document.description = doc['description']
            document.owner = doc['owner']
            document.save()

            f = open(doc['path_to_file'], 'rb')

            doc_ver = DocumentVersion()
            doc_ver.version = default_doc_version
            doc_ver.parent = document
            doc_ver.content_file = File(f)
            doc_ver.save()
            document.versions.add(doc_ver)
            document.save()
    print('  Done.')
