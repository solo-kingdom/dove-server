# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-05 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0026_bookremark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookremark',
            name='content',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='评语'),
        ),
    ]
