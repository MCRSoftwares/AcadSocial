# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0003_auto_20150105_1851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='perfilmodel',
            options={'verbose_name': 'perfil', 'verbose_name_plural': 'perfis'},
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 10, 1, 5, 24, 279000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 9, 1, 5, 24, 279000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='token',
            field=models.CharField(max_length=128, verbose_name='token', blank=True),
            preserve_default=True,
        ),
    ]
