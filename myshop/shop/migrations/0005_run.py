# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_dataview_dataset'),
    ]

    operations = [
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('formula', models.CharField(max_length=200)),
                ('test_dv', models.ForeignKey(related_name='test_runs', to='shop.DataView')),
                ('train_dv', models.ForeignKey(related_name='train_runs', to='shop.DataView')),
            ],
        ),
    ]
