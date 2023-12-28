from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

# Create your models here.


User = get_user_model()

# Create your models here.
class Profile(models.Model):
    profileID = models.AutoField(primary_key=True )
    user = models.ForeignKey(User, on_delete=models.CASCADE) #user entity pk (1 to 1 association)
    
    # profile information:
    firstName = models.CharField(max_length=100,null=True)
    lastName = models.CharField(max_length=100,null=True)
    phoneNumber = models.IntegerField(null=True)
    birthDate = models.DateField(null=True)
    gender = models.CharField(max_length=6 ,choices = {('M' , 'Male' ), ('F' , 'Female')},null=True)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)    

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    # post id:
    postID = models.UUIDField(primary_key = True,default=uuid.uuid4 )
    # user pk (1 to many association)
    user = models.ForeignKey(User,  on_delete=models.CASCADE , related_name = "posts")
    # post info
    image = models.ImageField(upload_to='post_images')
    created = models.DateTimeField(default=datetime.now)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f""

class Like(models.Model):
    likeID = models.AutoField(primary_key=True ,default = None)
    postID = models.ForeignKey(Post,  on_delete=models.CASCADE ,default=uuid.uuid4 ,related_name = "likes")
    likeDate = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,  on_delete=models.CASCADE,default=0)

    def __str__(self):
        return self.user.username

class Friendship(models.Model):
    friendshipID = models.AutoField(primary_key = True )
    creator = models.ForeignKey(User, related_name="friendship_creator_set", on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name="friend_set", on_delete=models.CASCADE)
    class Meta:
        constraints = [
            # Ensure that each pair of users can only be friends once
            models.UniqueConstraint(fields=['creator', 'friend'], name='unique_friendships'),
        ]

# Extend the User model
User.add_to_class('friends', models.ManyToManyField('self', through=Friendship, symmetrical=False))

class Comment(models.Model):
    commentID = models.AutoField(primary_key = True)
    commentContent = models.CharField(null=True, max_length=500)
    postID = models.ForeignKey(Post,  on_delete=models.CASCADE , related_name = "comments")
    userID = models.ForeignKey(User, on_delete=models.CASCADE ,related_name = "comments")
    created = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    notificationID = models.AutoField(primary_key = True) 
    userID = models.ForeignKey(User, on_delete=models.CASCADE , related_name ="notifications")
    notificationContent = models.CharField(null=True, max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,null=True , choices = [('R','Read') , ('U', 'Unread') , ('A' , 'Archived')])
    type = models.CharField(max_length=10,null=True , choices = [('F','Friend Request') , ('L', 'Like') , ('C' , 'Comment') ,('S' , 'System')])
    is_accepted = models.BooleanField(default = False) #specific for the Friend request notifs


class Message(models.Model):
    messageID = models.AutoField(primary_key = True) 
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    messageContent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.content}"
    class Meta:
        constraints = [
            # Ensure that each pair of users can only be friends once
            models.UniqueConstraint(fields=['sender', 'receiver'], name='unique_messaging'),
        ]

# Extend the User model
User.add_to_class('messages', models.ManyToManyField('self', through=Message, symmetrical=False ,related_name="history"))
