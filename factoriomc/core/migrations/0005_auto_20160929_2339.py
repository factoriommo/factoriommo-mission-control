# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160929_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionStat',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.IntegerField()),
                ('server', models.ForeignKey(to='core.Server')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='productionamountstat',
            name='server',
        ),
        migrations.DeleteModel(
            name='ProductionAmountStat',
        ),
    ]
