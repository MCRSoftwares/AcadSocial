# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0014_auto_20141209_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariomodel',
            name='full_name',
            field=models.CharField(default=None, max_length=256, verbose_name='full name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 11, 1, 54, 23, 770000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 1, 54, 23, 770000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
