from django.contrib import admin
from .models import Profile,Post,Like,Friendship,Comment,Notification,Message

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Friendship)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Message)



