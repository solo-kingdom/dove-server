# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0032_auto_20170606_0704'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='douban_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='summary',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
