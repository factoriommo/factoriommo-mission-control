# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumptionStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('event', models.CharField(choices=[('player_joined', 'Player Joined'), ('player_left', 'Player Left'), ('rocket_launched', 'Rocket Launched')], max_length=255)),
                ('data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ingame_name', models.CharField(max_length=255)),
                ('last_seen', models.DateTimeField()),
                ('times_joined', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductionStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(null=True, max_length=255, blank=True)),
                ('ip', models.CharField(max_length=32)),
                ('daemon_port', models.IntegerField()),
                ('player_limit', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='productionstat',
            name='server',
            field=models.ForeignKey(to='core.Server'),
        ),
        migrations.AddField(
            model_name='player',
            name='on_server',
            field=models.ForeignKey(null=True, blank=True, to='core.Server'),
        ),
        migrations.AddField(
            model_name='event',
            name='server',
            field=models.ForeignKey(to='core.Server'),
        ),
        migrations.AddField(
            model_name='consumptionstat',
            name='server',
            field=models.ForeignKey(to='core.Server'),
        ),
    ]
