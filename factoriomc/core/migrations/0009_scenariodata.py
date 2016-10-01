# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20161001_0149'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScenarioData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('server', models.ForeignKey(blank=True, to='core.Server', null=True)),
            ],
        ),
    ]
