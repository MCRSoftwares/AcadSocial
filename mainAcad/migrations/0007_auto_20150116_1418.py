# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainAcad', '0006_auto_20150116_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 17, 18, 10, 821000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conviteamigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 17, 18, 10, 821000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 17, 18, 10, 820000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
