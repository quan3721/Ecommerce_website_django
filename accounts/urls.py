from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'), # url register page
    path('login/', views.login, name='login'), # url login page
    path('logout/', views.logout, name='logout'), # url login page
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), # url actiave page
    
    path('daskboard/', views.daskboard, name='daskboard'), # url daskboard page
    path('', views.daskboard, name='daskboard'), # url daskboard page
    
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'), # url forgot Password page
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'), # url forgot Password validate page
    path('resetPassword/', views.resetPassword, name='resetPassword'), # url Password reset page
    
    path('my_orders/', views.my_orders, name='my_orders'), # url path for my orders in DashBoard
    path('edit_profile/', views.edit_profile, name='edit_profile'), # url path for edit profile in DashBoard
    path('change_password/', views.change_password, name='change_password'), # url path for change password in DashBoard
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'), # url path for order detail page in DashBoard


]
