# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainAcad', '0002_auto_20150105_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 9, 1, 5, 25, 17000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
