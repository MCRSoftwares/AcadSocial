# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 13, 20, 48, 46, 211000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 12, 20, 48, 46, 211000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
