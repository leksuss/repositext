#!/usr/bin/env python

import os
import sys

import django

sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'repositext.settings'
django.setup()

from django.contrib.auth.models import User  # noqa E402
from apps.repo.models import Organization  # noqa E402

ADD_TEST_FOLDERS = True

admin_user = User.objects.get(username='admin')

organization_list = [
    {
        'name': 'ACME Software',
        'address': '9999 Shiprock Ave',
        'city': 'Scenic Desert',
        'state': 'AZ',
        'country': 'US',
        'postal_code': '44444-2233',
        'owner': admin_user,
    }
]


if __name__ == '__main__':
    for org in organization_list:
        organization = Organization()
        for k, v in org.items():
            setattr(organization, k, v)
        organization.save()
