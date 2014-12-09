# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0002_auto_20141206_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='SenhaResetModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=40, verbose_name='token', blank=True)),
                ('data_expiracao', models.DateField(verbose_name='expiration date')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'senha reset',
                'verbose_name_plural': 'senha resets',
            },
            bases=(models.Model,),
        ),
    ]
