# Generated by Django 3.1.7 on 2021-03-31 10:48

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_name', models.CharField(default=None, max_length=100)),
                ('isactive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('profile_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('phone_id', models.IntegerField(unique=True)),
                ('email', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='images/')),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('added_date', models.DateTimeField(default=datetime.datetime.now)),
                ('last_modified_date', models.DateTimeField(default=datetime.datetime.now)),
                ('account_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.account')),
            ],
        ),
    ]
