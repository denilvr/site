# Generated by Django 2.0.1 on 2018-01-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0007_logincredentials'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomModel',
            fields=[
                ('requestID', models.CharField(max_length=10)),
                ('empID', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('leave', models.CharField(default='', max_length=30)),
                ('startDate', models.DateTimeField(null=True, verbose_name='date published')),
                ('endDate', models.DateTimeField(verbose_name='date published')),
                ('duration', models.FloatField(default=0)),
                ('status', models.BooleanField(default=0)),
                ('messageReceived', models.TextField(max_length=100, null=True)),
            ],
        ),
    ]
