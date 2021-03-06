# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-10 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_controller_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='controller',
            name='default_value',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='controller',
            name='max',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='controller',
            name='min',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='controller',
            name='step',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
