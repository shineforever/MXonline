# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-02 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecomments',
            name='comments',
            field=models.CharField(default='', max_length=200, verbose_name='\u7528\u6237\u8bc4\u8bba'),
        ),
    ]
