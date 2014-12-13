# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0004_auto_20141213_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfilmodel',
            name='contatos',
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 14, 14, 59, 53, 71000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 14, 59, 53, 71000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
