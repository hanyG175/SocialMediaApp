# Generated by Django 4.2.8 on 2023-12-27 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_friendship_id_friendship_friendshipid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profileID',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
