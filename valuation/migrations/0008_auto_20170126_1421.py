# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-26 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0007_auto_20170126_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fair_value',
            name='year',
        ),
        migrations.AlterField(
            model_name='fair_value',
            name='period',
            field=models.CharField(max_length=7, null=True),
        ),
    ]