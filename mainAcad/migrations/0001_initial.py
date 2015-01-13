# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0002_auto_20150112_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagemModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagem', models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens', verbose_name='Image')),
                ('thumbnail_perfil', models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail')),
                ('thumbnail_home', models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail')),
                ('thumbnail', models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail')),
                ('data_envio', models.DateTimeField(default=datetime.datetime(2015, 1, 12, 20, 48, 46, 233000, tzinfo=utc))),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this image should be treated as active. Unselect this instead of deleting images.')),
                ('is_profile_image', models.BooleanField(default=False, help_text='Designates whether this image should be treated as a profile picture. Unselect this instead of deleting the profile image.')),
                ('perfil', models.ForeignKey(to='contas.PerfilModel')),
            ],
            options={
                'verbose_name': 'imagem',
                'verbose_name_plural': 'imagens',
            },
            bases=(models.Model,),
        ),
    ]
