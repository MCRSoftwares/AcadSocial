# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0007_auto_20141208_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenmodel',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 8, 10, 13, 57, 13000), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
