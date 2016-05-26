# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_dataset'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('parameters', models.CharField(max_length=500)),
                ('row_range', models.CharField(max_length=200)),
            ],
        ),
    ]
