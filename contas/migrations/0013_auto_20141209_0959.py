# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0012_auto_20141208_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariomodel',
            name='host',
            field=models.CharField(default='ufpe', max_length=64, verbose_name='university host'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='active',
            field=models.BooleanField(default=True, help_text='Designates whether this token should be treated as active. An inactive token is a token that expired before being used. Unselect this instead of deleting tokens.', verbose_name='active'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 12, 59, 0, 683000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 12, 59, 0, 683000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='valid',
            field=models.BooleanField(default=True, help_text='Designates whether this token should be treated as valid. An invalid token cannot be accessed. Unselect this instead of deleting tokens.', verbose_name='valid'),
            preserve_default=True,
        ),
    ]
