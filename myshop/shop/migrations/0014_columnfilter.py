# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 01:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20160607_0139'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColumnFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=50)),
                ('field_choices', models.TextField()),
                ('current_selection', models.TextField()),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='column_filters', to='shop.Analysis')),
            ],
        ),
    ]
