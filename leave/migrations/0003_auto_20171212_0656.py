# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-12 06:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_auto_20171212_0633'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeleavemaster',
            old_name='flexiLeavesLeft',
            new_name='earnLeavesLeft',
        ),
    ]
