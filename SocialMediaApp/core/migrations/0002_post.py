# Generated by Django 4.1.2 on 2022-10-18 13:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='post_images')),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('caption', models.TextField(blank=True)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
    ]
