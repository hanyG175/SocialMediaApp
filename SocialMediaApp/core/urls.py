from django.contrib import admin
from django.urls import path 
from . import views
urlpatterns = [
    path('' , views.index , name ='index'),
    path('settings/' , views.settings, name ='settings'),
    path('settings/privacy',views.privacy , name='privacy'),
    path("upload/" , views.upload , name='upload'),
    path('signup/', views.signup , name='signup'),
    path('signin/', views.signin , name='signin'),
    path('logout/',views.signout,name="signout"),
    path('like/' , views.like,name='like'),
    path('profile/<str:pk>' , views.profile , name='profile'),
    path('invite' , views.invite , name='invite'),
    path('search' , views.search , name='search'),
    path('mark_as_read/<int:note_id>' , views.mark_as_read,name='mark_as_read'),
    path('accept_invitation/<int:invitation_id>' , views.accept_invitation,name='accept_invitation'),

    path('testing' , views.testing , name='testing'),


]
