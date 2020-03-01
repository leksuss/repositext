# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'repositext',
        'USER': 'repositext',
        'PASSWORD': 'admin',
        'PORT': '5432',
    }
}
