# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_auto_20170427_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookauthor',
            name='sex',
            field=models.CharField(choices=[('MALE', '男'), ('FEMALE', '女'), ('OTHER', '其他'), ('SECRET', '保密')], default='SECRET', max_length=8),
        ),
    ]
