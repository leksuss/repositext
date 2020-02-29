import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UuidPrimaryKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Timestamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Folder(UuidPrimaryKey, Timestamped):
    name = models.CharField('Name', max_length=255)
    parent = models.ForeignKey(
        'Folder', on_delete=models.CASCADE,
        null=True, blank=True
    )
    description = models.TextField('Description', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DocumentVersion(UuidPrimaryKey, Timestamped):
    version = models.CharField('Version', max_length=11)
    content_file = models.FileField(
        'Content File', upload_to='content/%Y/%m/%d/'
    )
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'Document', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Document Version'
        verbose_name_plural = 'Document Versions'

    def __str__(self):
        return f'{self.parent.name}:{self.version}'


class Document(UuidPrimaryKey, Timestamped):
    name = models.CharField('Name', max_length=255)
    parent = models.ForeignKey(
        'Folder', on_delete=models.CASCADE
    )
    description = models.TextField('Description', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    versions = models.ManyToManyField(
        DocumentVersion, blank=True
    )

    def newest_version(self):
        return self.versions.filter().order_by('-created')

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField('Name', max_length=50, unique=True)
    address = models.CharField('Address', max_length=50)
    city = models.CharField('City', max_length=50)
    state = models.CharField('State or Province', max_length=30)
    country = models.CharField('Country', max_length=2)
    postal_code = models.CharField('Zip or Postal Code', max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField('Description', null=True, blank=True)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    skype = models.CharField('Skype', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_names = 'User Profiles'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
