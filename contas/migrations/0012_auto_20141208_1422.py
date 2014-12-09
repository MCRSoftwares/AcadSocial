# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0011_auto_20141208_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokenmodel',
            name='valid',
            field=models.BooleanField(default=True, help_text='Designates whether this token should be treated as valid. A invalid token cannot be accessed.', verbose_name='valid'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 17, 22, 50, 816000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 8, 17, 22, 50, 816000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
