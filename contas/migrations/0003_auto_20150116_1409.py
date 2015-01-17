# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0002_auto_20150112_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 17, 17, 9, 28, 984000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 17, 9, 28, 984000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
