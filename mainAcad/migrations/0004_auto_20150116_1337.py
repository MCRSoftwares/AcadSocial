# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainAcad', '0003_auto_20150116_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='amigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 16, 37, 25, 354000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 16, 37, 25, 354000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
