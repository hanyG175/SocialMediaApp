from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile , Post ,Like , FollowerCount
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='signin')
def index(request):
    
    
    context = {
        'posts' : Post.objects.all() ,
        
        'profiles' : Profile.objects.all()
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
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
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
            return  redirect('/')

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
        bio = request.POST['bio']
        location = request.POST['location']
        if request.FILES.get('image') != None:   
            user_prof.profileimg = request.FILES.get('image')
            
        user_prof.bio = bio
        user_prof.location = location
        user_prof.save()
        return redirect('settings')
    
    return render(request,"setting.html" , {'user_prof' : user_prof})
    
@login_required(login_url='signin') 
def upload(request):
    if request.method == 'POST':
        
        user = request.user.username
        image = request.FILES.get('image_upload')    
        caption = request.POST['caption']
        new_post = Post.objects.create(user = user,image = image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin') 
def like(request):
    un = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = Like.objects.filter(post_id = post_id,username=un).first()
    if like_filter == None:
        new_like = Like.objects.create(post_id = post_id,username=un)
        new_like.save()
        post.likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.likes -= 1
        post.save()
        return redirect('/')

@login_required(login_url='signin') 
def profile(request , pk):
   
    user_obj = User.objects.get(username = pk)
    user_prof = Profile.objects.get(user=user_obj)
    no_posts = len(Post.objects.filter(user= pk))
    no_followers = len(FollowerCount.objects.filter(user=pk))
    context={
        'user_prof' : user_prof ,
        'user_obj' : user_obj, 
        'posts' : Post.objects.filter(user= pk),
        'no_posts':no_posts,
        'no_followers': no_followers
        }
    
    return render(request , 'profile.html',context)
    
@login_required(login_url='signin') 
def follow(request):
    if request.method == 'POST':
        username = request.user.username
        follower_name = request.POST['follow']
        f_obj = FollowrCount(follower = follower_name , user = username)
        return redirect('profile/<str:pk>')
    else :
        return redirect('profile/<str:pk>')   
        
    
    