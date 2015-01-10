# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainAcad', '0005_auto_20150110_1303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagemmodel',
            old_name='thumbnail_profile',
            new_name='thumbnail_perfil',
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 10, 16, 44, 22, 245000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
