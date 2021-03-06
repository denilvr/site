# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-12 03:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('deptID', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('deptName', models.CharField(max_length=100)),
                ('dateCreated', models.DateField(null=True, verbose_name='date created')),
                ('dateUpdated', models.DateField(null=True, verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('empID', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('empUniqueID', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('joiningDate', models.DateField(null=True, verbose_name='date published')),
                ('designation', models.CharField(blank=True, max_length=50)),
                ('dateCreated', models.DateField(blank=True, null=True, verbose_name='date created')),
                ('dateUpdated', models.DateField(blank=True, null=True, verbose_name='date updated')),
                ('manager', models.CharField(max_length=40)),
                ('managerID', models.CharField(max_length=10)),
                ('is_hr', models.BooleanField(default=False)),
                ('gender', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permanentAddress', models.CharField(max_length=300)),
                ('presentAddress', models.CharField(max_length=300)),
                ('dateCreated', models.DateField(null=True, verbose_name='date created')),
                ('dateUpdated', models.DateField(null=True, verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeaveLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(verbose_name='leave date')),
                ('leaveType', models.CharField(max_length=20)),
                ('dateCreated', models.DateField(null=True, verbose_name='date created')),
                ('dateUpdated', models.DateField(null=True, verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeaveTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestID', models.CharField(max_length=10)),
                ('leave', models.CharField(default='', max_length=30)),
                ('startDate', models.DateTimeField(null=True, verbose_name='date published')),
                ('endDate', models.DateTimeField(verbose_name='date published')),
                ('duration', models.FloatField(default=0)),
                ('status', models.BooleanField(default=0)),
                ('messageReceived', models.TextField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dateCreated', models.DateField(null=True, verbose_name='date created')),
                ('dateUpdated', models.DateField(null=True, verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='IsEmployeeHR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_hr', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('leaveID', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('leaveName', models.CharField(max_length=30)),
                ('totalSanctioned', models.IntegerField()),
                ('dateCreated', models.DateField(null=True, verbose_name='date created')),
                ('dateUpdated', models.DateField(null=True, verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('phoneID', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('phoneType', models.CharField(max_length=20)),
                ('phoneNumber', models.IntegerField(null=True)),
                ('dateCreated', models.DateField(null=True, verbose_name='date created')),
                ('dateUpdated', models.DateField(null=True, verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('projectID', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('projectName', models.CharField(default=None, max_length=30, null=True)),
                ('startDate', models.DateField(null=True, verbose_name='date published')),
                ('endDate', models.DateField(null=True, verbose_name='date published')),
                ('dateCreated', models.DateField(null=True, verbose_name='date created')),
                ('dateUpdated', models.DateField(null=True, verbose_name='date updated')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeaveMaster',
            fields=[
                ('empID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='leave.Employee')),
                ('work_from_home_availed', models.FloatField(default=0)),
                ('casualLeavesLeft', models.FloatField(default=0)),
                ('sickLeavesLeft', models.FloatField(default=0)),
                ('annualLeavesLeft', models.FloatField(default=0)),
                ('flexiLeavesLeft', models.FloatField(default=0)),
                ('maternityLeavesLeft', models.IntegerField(default=0)),
                ('financialYear', models.CharField(max_length=10)),
                ('dateCreated', models.DateField(null=True, verbose_name='date created')),
                ('dateUpdated', models.DateField(null=True, verbose_name='date updated')),
            ],
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='empID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='leave.Employee'),
        ),
        migrations.AddField(
            model_name='isemployeehr',
            name='empID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='leave.Employee'),
        ),
        migrations.AddField(
            model_name='employeeproject',
            name='empID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.Employee'),
        ),
        migrations.AddField(
            model_name='employeeproject',
            name='projectID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.Project'),
        ),
        migrations.AddField(
            model_name='employeeleavetransaction',
            name='empID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.Employee'),
        ),
        migrations.AddField(
            model_name='employeeleavelog',
            name='empID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.Employee'),
        ),
        migrations.AddField(
            model_name='employeeaddress',
            name='empID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='leave.Employee'),
        ),
        migrations.AddField(
            model_name='employee',
            name='address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leave.EmployeeAddress'),
        ),
        migrations.AddField(
            model_name='employee',
            name='phoneNumber',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leave.PhoneNumber'),
        ),
    ]
