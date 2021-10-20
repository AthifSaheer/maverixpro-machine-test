# from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),


    path('profile/view/<int:id>/', views.profile_view, name='profile_view'),
    
    path('follow/<int:id>/', views.follow, name='follow'),
    path('unfollow/<int:id>/', views.unfollow, name='unfollow'),
    path('accept/follow/request/<int:id>/', views.accept_follow_request, name='accept_follow_request'),
    path('reject/follow/request/<int:id>/', views.reject_follow_request, name='reject_follow_request'),
]
