from django.contrib import admin
from django.urls import path
from .views import index, detail, login, sign_up, blog, like, my_profile, add_new_blog

urlpatterns = [
    path('', index),
    path('detail/', detail, name="detail"),
    path('login/', login, name="login"),
    path('signup/', sign_up, name="sign_up"),
    path('myprofile/', my_profile, name="myprofile"),
    path('myprofile/addblog', add_new_blog, name="newblog"),
    path('detail/<str:pk>', blog, name="blog"),
    path('detail/<str:pk>/like', like, name="like"),
]