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

]
