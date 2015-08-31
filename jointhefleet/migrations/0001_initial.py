# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Killmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('killID', models.IntegerField()),
                ('solarSystemID', models.IntegerField()),
                ('killTime', models.DateTimeField()),
                ('shipTypeID', models.IntegerField()),
                ('characterID', models.IntegerField()),
                ('characterName', models.CharField(max_length=50)),
                ('corporationID', models.IntegerField()),
                ('corporationName', models.CharField(max_length=50)),
                ('allianceID', models.IntegerField(null=True, blank=True)),
                ('allianceName', models.CharField(max_length=50, null=True, blank=True)),
                ('totalValue', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member_id', models.IntegerField()),
                ('member_name', models.CharField(max_length=50)),
                ('member_ship_id', models.IntegerField()),
                ('member_ship_name', models.CharField(max_length=50)),
                ('member_system', models.CharField(max_length=30)),
                ('member_corp_id', models.IntegerField(default=1)),
                ('member_corp_name', models.CharField(default=b'Not Recorded', max_length=50)),
                ('join_time', models.TimeField(help_text=b'Join Time', verbose_name=b'Join Time')),
                ('exit_time', models.TimeField(help_text=b'Exit Time', null=True, verbose_name=b'Exit Time', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text=b'Operation Code', max_length=100)),
                ('date_opd', models.DateTimeField(help_text=b'Start Time', verbose_name=b'date operated')),
                ('date_fin', models.DateTimeField(help_text=b'Finish Time', null=True, verbose_name=b'date finished', blank=True)),
                ('security_code', models.CharField(help_text=b'OP Security Code for join', max_length=32)),
                ('category', models.CharField(default=b'CTA', help_text=b'Operation Category', max_length=3, choices=[(b'Alliance Operation', ((b'ROM', b'Roaming'), (b'CTA', b'CTA'), (b'TRN', b'Training'), (b'ETC', b'Etc.'))), (b'Movingstar Operation', ((b'WRR', b'Mission WRR'), (b'MWF', b'Movingstar Wormhole Fleet')))])),
                ('state', models.CharField(default=b'OPENED', help_text=b'State of this Operation', max_length=6, choices=[(b'OPENED', b'Opened'), (b'CLOSED', b'Closed'), (b'DSITED', b'Distributed')])),
                ('fc_id', models.IntegerField(help_text=b'Charactor ID')),
                ('fc_name', models.CharField(help_text=b'Charactor Name', max_length=50)),
                ('acquired', models.TextField(help_text=b'Acquired Item lists', null=True, blank=True)),
                ('remarks', models.TextField(help_text=b'Remarks', null=True, blank=True)),
                ('killboard', models.TextField(help_text=b'Killboard Links', null=True, blank=True)),
                ('profit', models.IntegerField(default=0, help_text=b'Profit', null=True, blank=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='operation',
            field=models.ForeignKey(to='jointhefleet.Operation'),
        ),
        migrations.AddField(
            model_name='killmail',
            name='operation',
            field=models.ForeignKey(to='jointhefleet.Operation'),
        ),
    ]
