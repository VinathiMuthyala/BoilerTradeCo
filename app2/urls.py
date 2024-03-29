from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('addproduct/', views.add_product, name = "add_product"),
    path('new/', views.new, name = "new"),
    path('addlisting/', views.add_listing, name = "add_listing"),
    path('editproduct/', views.editproduct, name = 'editproduct'),
    path('<int:pk>/', views.detail, name = 'detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)