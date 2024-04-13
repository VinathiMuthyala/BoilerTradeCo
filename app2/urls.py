from django.urls import path, re_path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('addproduct/', views.add_product, name = "add_product"),
    path('newproduct/', views.new, name = "new"),
    path('addlisting/', views.add_listing, name = "add_listing"),
    # path('editproduct/', views.editproduct, name = 'editproduct'),
    path('<int:pk>/', views.detail, name = 'detail'),
    path('<int:pk>/delete/', views.delete, name = 'delete'),
    path('<int:pk>/edit/', views.edit, name = 'edit'),
    path('bookmarks/', views.generate_bookmarks, name = 'bookmarks'),
    path('bookmark/', views.bookmark_product, name='bookmark_product'),
    re_path(r'^category/(?P<category_tag>[\w\s-]+)/$', views.filter_products_by_category, name='filter_products_by_category'),
    re_path(r'^quality/(?P<quality_tag>[\w\s-]+)/$', views.filter_products_by_quality, name='filter_products_by_quality'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)