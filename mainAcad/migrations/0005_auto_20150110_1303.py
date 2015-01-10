# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainAcad', '0004_auto_20150109_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemmodel',
            name='thumbnail',
            field=models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagemmodel',
            name='thumbnail_home',
            field=models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='imagemmodel',
            name='thumbnail_profile',
            field=models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagemmodel',
            name='data_envio',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 10, 16, 3, 52, 730000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
