# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0009_auto_20141208_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfilmodel',
            name='chave_ativacao',
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='active',
            field=models.BooleanField(default=True, help_text='Designates whether this token should be treated as active.Unselect this instead of deleting tokens.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 14, 38, 24, 668000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 8, 14, 38, 24, 668000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
