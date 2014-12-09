# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0006_auto_20141208_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokenmodel',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 8, 10, 12, 54, 59000), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
