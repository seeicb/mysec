# Generated by Django 2.1.2 on 2019-03-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CIpDomain',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('target_id', models.IntegerField()),
                ('ip', models.CharField(max_length=20)),
                ('domain', models.CharField(max_length=67, unique=True)),
                ('remark', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CTarget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('target_name', models.CharField(max_length=255)),
                ('start_ip', models.CharField(max_length=20)),
                ('end_ip', models.CharField(max_length=20)),
                ('remark', models.CharField(max_length=255)),
                ('uptime', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
