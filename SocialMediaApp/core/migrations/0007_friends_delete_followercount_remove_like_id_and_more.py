# Generated by Django 5.0 on 2023-12-25 01:49

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_followercount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
       
        migrations.AddField(
            model_name='like',
            name='likeDate',
            field=models.DateField(default=None, verbose_name=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='like',
            name='likeID',
            field=models.IntegerField(default=None, primary_key=True, serialize=False),
        ),
    
        migrations.AddField(
            model_name='friends',
            name='followed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='core.profile'),
        ),
        migrations.AddField(
            model_name='friends',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followings', to='core.profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(through='core.Friends', to='core.profile'),
        ),
    ]
