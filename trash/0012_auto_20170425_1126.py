# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_auto_20170425_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
