# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 05:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_run'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataview',
            old_name='row_range',
            new_name='row_range_high',
        ),
        migrations.AddField(
            model_name='dataview',
            name='row_range_low',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
