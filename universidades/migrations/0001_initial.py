# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CursoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'curso',
                'verbose_name_plural': 'cursos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UniversidadeModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sigla', models.CharField(max_length=10)),
                ('nome', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'universidade',
                'verbose_name_plural': 'universidades',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cursomodel',
            name='universidade',
            field=models.ForeignKey(to='universidades.UniversidadeModel'),
            preserve_default=True,
        ),
    ]
