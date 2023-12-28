from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile , Post ,Like , Friendship,Notification
from django.contrib.auth.decorators import login_required
from itertools import chain
import random 
from channels.generic.websocket import AsyncWebsocketConsumer
import json
# Create your views here.

@login_required(login_url='signin')
def index(request):
    
    user_obj = User.objects.get(id = request.user.id)
    user_prof = Profile.objects.get(user=user_obj)

    user_following = [User.objects.get(username=username.friend) for username in user_obj.friendship_creator_set.all()]
    print( user_obj.friend_set.all())
    feed = [Post.objects.filter(user=usernames) for usernames in user_following]
    
    feed_list = list(chain(*feed))  + list(user_obj.posts.all())
    
    post_likes = [ (post , post.likes.count() ,list(Profile.objects.get(user=User.objects.get(username = liker)) for liker in post.likes.all())  ) for post in feed_list]
    
    all_users = list(User.objects.all())
    #list od all users except current user:
    all_users.remove(list(User.objects.filter(username = request.user.username))[0])
    
    #list of people already followed:
    #list of user not followed:
    user_suggestions = [x for x in list(all_users) if (x not in user_following)]

    print(user_suggestions)
    profile_suggestions = [Profile.objects.filter(user = x.id) for x in user_suggestions]

    random.shuffle(profile_suggestions)
    suggestions = list(chain(*profile_suggestions))
    print(suggestions)

    notifications = list(Notification.objects.filter(userID=request.user, status = 'U' ,is_accepted=False))
    context = {
        'posts' : post_likes ,
        'profileimg' : Profile.objects.get(user = User.objects.get(username = request.user.username)).profileimg,
        'profiles' : Profile.objects.all(),
        'suggestions':suggestions[:3],
        'user_prof': user_prof,
        'notifications': notifications[:3],
    }
    
    return HttpResponse(render(request , 'index.html' , context ))

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
        
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                #log user in and redirect to settings page:
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                #create a Profile object for the new user:
                new_profile = Profile.objects.create(user=user_login)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Passwords Not Matching')
            return redirect('signup')
  
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        
        if user is not None :
            auth.login(request,user)
            profile_exists = Profile.objects.filter(user=user.id).first()
            if profile_exists is not None:
                return  redirect('/')
            return redirect('settings')

        else:
            messages.info(request, 'Credentials Invalid : User Not Found!')
            return redirect('signin')
            
    else:        
        return render(request,"signin.html") 

@login_required(login_url='signin')
def signout(request):
    auth.logout(request)
    return redirect('signin')  

@login_required(login_url='signin')
def settings(request):        
    user_prof = Profile.objects.get(user  = request.user)
    if request.method == 'POST':
        firstname= request.POST['firstname']
        lastname= request.POST['lastname']
        gender= request.POST['gender']
        birthDate= request.POST['birthdate']
        phoneNumber = request.POST['phoneNumber']
        bio = request.POST['bio']
        location = request.POST['location']
        if request.FILES.get('image') != None:   
            user_prof.profileimg = request.FILES.get('image')
        user_prof.firstName =request.user.first_name = firstname
        user_prof.lastName =request.user.last_name = lastname
        user_prof.gender = gender
        if birthDate != "":
            user_prof.birthDate = birthDate
        user_prof.phoneNumber = phoneNumber
        user_prof.bio = bio
        user_prof.location = location
        user_prof.save()
        return redirect('settings')
    
    return render(request,"setting.html" , {'user_prof' : user_prof})
    
@login_required(login_url='signin') 
def upload(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')    
        caption = request.POST['caption']
        new_post = Post.objects.create(user = user,image = image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin') 
def like(request):
    un = request.user
    post_id = request.GET.get('post_id')
    post = Post.objects.get(postID=post_id)
    like_filter = Like.objects.filter(postID= post,user=un).first()
    if like_filter == None:
        new_like = Like.objects.create(postID = post,user=un)
        new_like.save()

        note = Notification.objects.create(userID=post.user , notificationContent=f"{un} has liked your post",type='L' , status='U')
        note.save()

        return redirect('/')
    else:
        like_filter.delete()
        post.save()
        return redirect('/')

@login_required(login_url='signin') 
def profile(request , pk):
    user_obj = User.objects.get(id = pk)
    user_prof = Profile.objects.get(user=user_obj.id)
    no_posts = len(Post.objects.filter(user= pk))
    no_followers = len(user_obj.friend_set.all())
    no_following = 0
    
    follower_exist = Friendship.objects.filter(friend=request.user.id,creator=pk).first()
    button_text = "UnFollow" if follower_exist else "Follow"
    
    context={
        'user_prof' : user_prof ,
        'user_obj' : user_obj, 
        'posts' : Post.objects.filter(user= pk),
        'no_posts':no_posts,
        'button_text': button_text,
        'no_followers': no_followers,
        'no_following': no_following,
        
        }
    
    return HttpResponse(render(request , 'profile.html',context))

@login_required(login_url='signin') 

def mark_as_read(request, note_id):
    notification = Notification.objects.get(notificationID=note_id)
    notification.status = 'R'
    notification.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='signin') 
def invite(request):
    if request.method == 'POST':
        friend = request.POST['friend']
        creator = request.POST['creator']
        cr = User.objects.get(username = creator).id
        fr = User.objects.get(username = friend).id
        friend = User.objects.get(username = friend)
        f_obj = Friendship.objects.filter(friend = friend, creator = cr)
        if f_obj.first():
            f_obj.delete()
            return redirect('/profile/' + str(cr))
        else:
            note = Notification.objects.create(userID=friend , notificationContent=f"{creator} has sent you a friend invitation",type='F',status='U')
            note.save()
            if request.META['HTTP_REFERER'] == 'http://127.0.0.1:8000/':
                return redirect('/')
            else:      
                return redirect('/profile/'+str(cr))
    else :
        return redirect('/')   

@login_required
def accept_invitation(request, invitation_id):
    invitation = Notification.objects.get(notificationID=invitation_id)
    invitation.is_accepted = True
    cr = list(invitation.notificationContent.split(" "))[0]
    creator = User.objects.get(username=cr)
    f_obj = Friendship.objects.create(friend = invitation.userID , creator = creator )
    f_obj.save()
    invitation.save()
    mark_as_read(request, invitation_id)
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='signin') 
def search(request):
    
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user=user_object)
   
    if request.method == 'POST':
        user_name = request.POST['username']
        username_objs = User.objects.filter(username__icontains = user_name)
        username_profiles =[ Profile.objects.filter(id_user = user.id) for user in  username_objs]
        l = list(chain(*username_profiles))
    
    
        context = {
            'user_profile' : user_profile,
            'results' : l,
            'username' : request.POST['username']
        }    
        
    return  render(request,"search.html",context)

@login_required(login_url='signin')
def privacy(request):
    
    return HttpResponse(render(request , 'privacy.html' ))
@login_required(login_url="signin")
def testing(request):
    
    return HttpResponse(render(request , 'testing.html' ))





    