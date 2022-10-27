from django.contrib import admin
from django.urls import path 
from . import views
urlpatterns = [
    path('' , views.index , name ='index'),
    path('settings/' , views.settings, name ='settings'),
    path("upload/" , views.upload , name='upload'),
    path('signup/', views.signup , name='signup'),
    path('signin/', views.signin , name='signin'),
    path('logout/',views.signout,name="signout"),
    path('like/' , views.like,name='like'),
    path('profile/<str:pk>' , views.profile , name='profile'),
    path('follow' , views.follow , name='follow'),
    
]
