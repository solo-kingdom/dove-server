# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-13 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0018_category_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='未命名书单', max_length=100)),
                ('summary', models.CharField(max_length=1000, null=True)),
                ('pic', models.CharField(max_length=200, null=True)),
                ('tags', models.ManyToManyField(to='book.BookTag')),
            ],
        ),
    ]
