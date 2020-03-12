#!/usr/bin/env python

import os

import django

try:    
    from local import project_settings as project_settings
    os.environ['DJANGO_SETTINGS_MODULE'] = project_settings
except ModuleNotFoundError:
    project_settings = 'repositext.settings'
    os.environ['DJANGO_SETTINGS_MODULE'] = project_settings

django.setup()

from django.contrib.auth.models import User  # noqa E402


if __name__ == '__main__':
    print("  Setting admin user password ...")
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin')
    admin_user.save()
    print("  Done.")

