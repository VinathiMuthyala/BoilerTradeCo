from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from .views import UserProfileUpdateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name ="index"),
    path('authentication/', views.email_auth, name = "email_auth"),
    path('home/', views.home, name = "home"),
    path('signup/', views.signup, name = "signup"),
    path('signin/', views.signin, name = "signin"),
    path('profile/', views.viewprofile, name = "profile"),
    path('deleteaccount/', views.delete_account, name='deleteaccount'),
    path('settings/', views.settings, name="settings"),
    path('emailreport/', views.emailreport, name = 'emailreport'),
    path('generatepdf/', views.get_pdf, name='generatepdf'),
    path('logout', views.signout, name='logout'),
    path('submit_rating/', views.submit_rating, name='submit_rating'),
    path('rate_edit/', views.rate_edit, name='rate_edit'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="authentication/reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="authentication/reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/reset.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authentication/reset_password_complete.html"), name="password_reset_complete"),
    #path('email_auth/', views.email_auth, name = "email_auth"),
    path('emailseller/', views.emailseller, name = 'emailseller'),
    # path('editproduct/', views.editproduct, name = 'editproduct'),
    # path('filter-products-by-price/', views.filter_products_by_price, name='filter_products_by_price'),
    #path('rate-seller/', views.rate_seller, name='rate_seller'),
    path('rate-seller/<str:seller_email>/', views.rate_seller, name='rate_seller'),
    path('edit-seller/<str:seller_email>/', views.edit_seller, name='edit_seller'),
    path('delete-rating/<str:seller_email>/', views.delete_rating, name='delete_rating'),
    path('update-notifications/', views.update_notifications, name='update_notifications'),

]