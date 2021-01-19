# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-06 02:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0030_auto_20170606_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='books',
            field=models.ManyToManyField(blank=True, null=True, to='book.Book'),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='book.BookTag'),
        ),
    ]
