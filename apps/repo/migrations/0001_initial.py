# Generated by Django 3.0.3 on 2020-03-04 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('skype', models.CharField(blank=True, max_length=50, null=True, verbose_name='Skype')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('address', models.CharField(max_length=50, verbose_name='Address')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('state', models.CharField(max_length=30, verbose_name='State or Province')),
                ('country', models.CharField(max_length=2, verbose_name='Country')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Zip or Postal Code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repo.Folder')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentVersion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('version', models.CharField(max_length=11, verbose_name='Version')),
                ('content_file', models.FileField(upload_to='content/%Y/%m/%d/', verbose_name='Content File')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repo.Document')),
            ],
            options={
                'verbose_name': 'Document Version',
                'verbose_name_plural': 'Document Versions',
            },
        ),
        migrations.AddField(
            model_name='document',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repo.Folder'),
        ),
        migrations.AddField(
            model_name='document',
            name='versions',
            field=models.ManyToManyField(blank=True, to='repo.DocumentVersion'),
        ),
    ]
