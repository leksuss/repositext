#!/usr/bin/env python

import os
import sys

import django

sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'repositext.settings'
django.setup()

from django.contrib.auth.models import User  # noqa E402
from apps.repo.models import UserProfile  # noqa E402

ADD_TEST_FOLDERS = True

admin_user = User.objects.get(username='admin')

user_list = [
    {
        'username': 'harlin',
        'password': 's3cr3tpassw0rd',
        'email': 'harlin@acme.org',
        'bio': 'Worker among workers',
        'location': 'Scenic Desert, AZ USA',
        'birth_date': '1969-05-22',
        'skype': 'scenicdesert_tours',
    },
]


if __name__ == '__main__':
    for u in user_list:
        user = User()
        user.username = u['username']
        user.set_password(u['password'])
        user.email = u['email']
        user.save()
        user.userprofile.bio = u['bio']
        user.userprofile.location = u['location']
        user.userprofile.birth_date = u['birth_date']
        user.userprofile.skype = u['skype']
        user.save()
