# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0003_senharesetmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=128)),
                ('token', models.CharField(max_length=40, verbose_name='token', blank=True)),
                ('data_expiracao', models.DateField(verbose_name='expiration date')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'token',
                'verbose_name_plural': 'tokens',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='senharesetmodel',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='SenhaResetModel',
        ),
    ]
