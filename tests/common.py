from django.contrib.auth.models import User
from repositext.settings import SYS_ROOT_FOLDER_NAME
from apps.repo.models import Folder


def set_admin_user():
    admin_user = User()
    admin_user.username = 'admin'
    admin_user.email = 'admin@localhost'
    admin_user.set_password('admin')
    admin_user.save()


def get_admin_user():
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        set_admin_user()
        admin_user = User.objects.get(username='admin')
    return admin_user
    

def add_root_folder():
    root_folder = Folder()
    root_folder.name = SYS_ROOT_FOLDER_NAME
    root_folder.description = 'System root folder'
    root_folder.owner = get_admin_user()
    root_folder.save()

def get_root_folder(create=False):
    if create:
        root_folder = Folder.objects.get(name=SYS_ROOT_FOLDER_NAME)
    try:
        root_folder = Folder.objects.get(name=SYS_ROOT_FOLDER_NAME)
    except Folder.DoesNotExist:
        add_root_folder()
        root_folder = Folder.objects.get(name=SYS_ROOT_FOLDER_NAME)
    return root_folder


TEST_USER = {
    'username': 'testuser',
    'email': 'testuser@localhost',
    'password': 'testsecret',
}


def add_test_user():
    test_user = User()
    test_user.username = TEST_USER['username']
    test_user.email = TEST_USER['email']
    test_user.set_password(TEST_USER['password'])
    test_user.save()


def get_test_user(create=False):
    if create:
        add_test_user()
    test_user = User.objects.get(username=TEST_USER['username'])
    return test_user


def get_home_folder():
    test_user = get_test_user(create=True)
    home_folder = Folder()
    home_folder.name = 'Home'
    home_folder.description = 'System home folder for users'
    home_folder.owner = User.objects.get(
        username=get_admin_user().username
    )
    home_folder.parent = get_root_folder()
    home_folder.save()
    return home_folder