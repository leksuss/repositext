from django.contrib.auth.models import User
from apps.repo.models import Folder


def get_admin_user():
    admin_user = User()
    admin_user.username = 'admin'
    admin_user.email = 'admin@localhost'
    admin_user.set_password('admin')
    admin_user.save()
    return admin_user


def get_root_folder():
    root_folder = Folder()
    root_folder.name = '-ROOT-'
    root_folder.description = 'System root folder'
    root_folder.owner = get_admin_user()
    root_folder.save()
    return root_folder

