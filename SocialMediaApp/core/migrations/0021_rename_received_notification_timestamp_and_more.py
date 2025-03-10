# Generated by Django 4.2.8 on 2023-12-28 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_like_likedate_alter_profile_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='received',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='notification',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
