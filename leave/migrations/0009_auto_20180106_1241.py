# Generated by Django 2.0.1 on 2018-01-06 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leave', '0008_custommodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='custommodel',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='custommodel',
            name='messageReceived',
        ),
        migrations.RemoveField(
            model_name='custommodel',
            name='requestID',
        ),
        migrations.RemoveField(
            model_name='custommodel',
            name='status',
        ),
        migrations.RemoveField(
            model_name='employeeleavetransaction',
            name='requestID',
        ),
        migrations.AddField(
            model_name='employee',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='custommodel',
            name='endDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='custommodel',
            name='startDate',
            field=models.DateTimeField(null=True),
        ),
    ]