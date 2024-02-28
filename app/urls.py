from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.viewprofile, name ="profile"),
    path('', views.index, name ="index"),
    path('home/', views.home, name = "home"),
    path('signup/', views.signup, name = "signup"),
    path('signin/', views.signin, name = "signin"),
    path('profile/', views.viewprofile, name = "profile"),
    path('settings/', views.settings, name="settings"),
]