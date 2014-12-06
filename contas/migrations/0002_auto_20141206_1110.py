# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariomodel',
            name='perfil_link',
            field=models.CharField(max_length=200, verbose_name='profile link'),
            preserve_default=True,
        ),
    ]
