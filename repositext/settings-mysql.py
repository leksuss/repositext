# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'repositext',
        'USER': 'repositext',
        'PASSWORD': 'admin',
        'PORT': '3306',
    }
}
