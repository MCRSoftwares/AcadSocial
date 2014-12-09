# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0010_auto_20141208_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenmodel',
            name='active',
            field=models.BooleanField(default=True, help_text='Designates whether this token should be treated as active. Unselect this instead of deleting tokens.', verbose_name='active'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 14, 51, 26, 32000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 8, 14, 51, 26, 32000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariomodel',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
            preserve_default=True,
        ),
    ]
