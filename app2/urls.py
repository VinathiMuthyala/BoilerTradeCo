from django.urls import path, include
from . import views

urlpatterns = [
    path('addproduct/', views.add_product, name = "add_product")
]