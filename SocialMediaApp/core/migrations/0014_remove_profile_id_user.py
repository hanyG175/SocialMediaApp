# Generated by Django 4.2.8 on 2023-12-26 00:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_profile_id_profile_profileid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id_user',
        ),
    ]
