# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universidades', '0003_auto_20150118_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='universidademodel',
            name='sigla_campus',
            field=models.CharField(default='UFPERecife', max_length=148),
            preserve_default=False,
        ),
    ]
