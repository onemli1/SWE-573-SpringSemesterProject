# Generated by Django 4.0.4 on 2022-05-21 16:31

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='last name')),
                ('profile_image', models.ImageField(blank=True, default=account.models.get_default_profile_image, max_length=255, null=True, upload_to=account.models.get_profile_image_filepath)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
