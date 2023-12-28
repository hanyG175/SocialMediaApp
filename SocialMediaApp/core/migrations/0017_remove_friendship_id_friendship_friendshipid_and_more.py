# Generated by Django 4.2.8 on 2023-12-27 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0016_remove_post_likes_alter_like_postid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendship',
            name='id',
        ),
        migrations.AddField(
            model_name='friendship',
            name='friendshipID',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=6, null=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notificationID', models.IntegerField(primary_key=True, serialize=False)),
                ('notificationContent', models.CharField(max_length=500, null=True)),
                ('received', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('R', 'Read'), ('U', 'Unread'), ('A', 'Archived')], max_length=10, null=True)),
                ('type', models.CharField(choices=[('F', 'Friend Request'), ('L', 'Like'), ('C', 'Comment'), ('S', 'System')], max_length=10, null=True)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('messageID', models.IntegerField(primary_key=True, serialize=False)),
                ('messageContent', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentID', models.IntegerField(primary_key=True, serialize=False)),
                ('commentContent', models.CharField(max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('postID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.post')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='message',
            constraint=models.UniqueConstraint(fields=('sender', 'receiver'), name='unique_messaging'),
        ),
    ]