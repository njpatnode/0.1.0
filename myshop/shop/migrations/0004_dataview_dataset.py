# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_dataview'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataview',
            name='dataset',
            field=models.ForeignKey(related_name='dataviews', default=1, to='shop.DataSet'),
            preserve_default=False,
        ),
    ]
