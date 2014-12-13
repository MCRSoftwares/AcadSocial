# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0002_auto_20141213_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilmodel',
            name='amizades',
            field=models.ManyToManyField(to='contas.PerfilModel'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 14, 14, 51, 16, 861000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 14, 51, 16, 861000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
