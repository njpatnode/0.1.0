# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_controller'),
    ]

    operations = [
        migrations.AddField(
            model_name='panel',
            name='result_function',
            field=models.CharField(default='histogram', max_length=200),
            preserve_default=False,
        ),
    ]
