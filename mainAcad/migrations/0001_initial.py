# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0002_auto_20150118_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmigoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 18, 16, 16, 34, 530000, tzinfo=utc))),
                ('ativo', models.BooleanField(default=True)),
                ('amigo', models.ForeignKey(related_name='amigo', to='contas.PerfilModel')),
                ('perfil', models.ForeignKey(related_name='perfil', to='contas.PerfilModel')),
            ],
            options={
                'verbose_name': 'amigo',
                'verbose_name_plural': 'amigos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConviteAmigoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_criacao', models.DateTimeField(default=datetime.datetime(2015, 1, 18, 16, 16, 34, 531000, tzinfo=utc))),
                ('ativo', models.BooleanField(default=True)),
                ('amigo', models.ForeignKey(related_name='amigo_convite', to='contas.PerfilModel')),
                ('perfil', models.ForeignKey(related_name='perfil_convite', to='contas.PerfilModel')),
            ],
            options={
                'verbose_name': 'convite (Amigo)',
                'verbose_name_plural': 'convites (Amigo)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImagemModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagem', models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens', verbose_name='Image')),
                ('thumbnail_perfil', models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail')),
                ('thumbnail_home', models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail')),
                ('thumbnail', models.ImageField(default=b'imagens/perfil/default.jpg', upload_to=b'imagens/thumbnails/', verbose_name='Thumbnail')),
                ('data_envio', models.DateTimeField(default=datetime.datetime(2015, 1, 18, 16, 16, 34, 529000, tzinfo=utc))),
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
