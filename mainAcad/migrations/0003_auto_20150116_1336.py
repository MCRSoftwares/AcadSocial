# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainAcad', '0002_auto_20150116_1336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amigomodel',
            options={'verbose_name': ('amigo',), 'verbose_name_plural': ('amigos',)},
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 16, 36, 28, 725000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
