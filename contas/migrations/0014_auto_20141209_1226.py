# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0013_auto_20141209_0959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuariomodel',
            name='host',
        ),
        migrations.RemoveField(
            model_name='usuariomodel',
            name='perfil_link',
        ),
        migrations.AddField(
            model_name='perfilmodel',
            name='perfil_link',
            field=models.CharField(default='ufpe', unique=True, max_length=128, verbose_name='profile link'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_expiracao',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 10, 15, 26, 1, 44000, tzinfo=utc), verbose_name='expiration date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tokenmodel',
            name='data_request',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 15, 26, 1, 44000, tzinfo=utc), verbose_name='request date'),
            preserve_default=True,
        ),
    ]
