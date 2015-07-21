# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(default=b'', max_length=255, blank=True)),
                ('message', models.TextField()),
                ('level', models.IntegerField(choices=[(10, b'DEBUG'), (20, b'INFO'), (25, b'SUCCESS'), (30, b'WARNING'), (40, b'ERROR'), (110, b'PERSISTENT DEBUG'), (120, b'PERSISTENT INFO'), (125, b'PERSISTENT SUCCESS'), (130, b'PERSISTENT WARNING'), (140, b'PERSISTENT ERROR')])),
                ('extra_tags', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('read', models.BooleanField(default=False)),
                ('expires', models.DateTimeField(null=True, blank=True)),
                ('close_timeout', models.IntegerField(null=True, blank=True)),
                ('from_user', models.ForeignKey(related_name='from_user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
