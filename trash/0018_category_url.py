# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-13 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0017_auto_20170428_0519'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='url',
            field=models.CharField(default='', max_length=200),
        ),
    ]
