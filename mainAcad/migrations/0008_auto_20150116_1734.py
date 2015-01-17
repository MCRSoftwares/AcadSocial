# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainAcad', '0007_auto_20150116_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 9, 769000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conviteamigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 9, 769000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 20, 34, 9, 768000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
