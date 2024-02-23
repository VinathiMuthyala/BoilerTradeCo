from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.viewprofile, name ="profile"),
    path('signup/', views.signup, name = "signup"),
    path('signin/', views.signin, name = "signin"),
    path('signout/', views.signin, name = "signout"),
    path('profile/', views.viewprofile, name = "profile"),
    path('settings/', views.settings, name="settings"),
]