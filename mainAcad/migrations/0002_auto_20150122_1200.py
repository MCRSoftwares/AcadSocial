# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainAcad', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conviteamigomodel',
            name='id',
        ),
        migrations.AddField(
            model_name='conviteamigomodel',
            name='cid',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='amigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 15, 0, 12, 794000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conviteamigomodel',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 15, 0, 12, 795000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 22, 15, 0, 12, 793000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
