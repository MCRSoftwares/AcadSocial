# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0005_auto_20141208_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 8, 9, 54, 51, 740000), verbose_name='request date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(verbose_name='expiration date'),
            preserve_default=True,
        ),
    ]
