"""
URL configuration for Ecommerce_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views # import views module
from django.conf.urls.static import static # import static
from django.conf import settings # import settings


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')), # fake url admin
    path("securelogin/", admin.site.urls),
    path('', views.home, name='home'), # path url for home page
    
    # store url #
    path('store/', include('store.urls')),
    
    # cart url #
    path('cart/', include('carts.urls')),
    
    # account url #
    path('accounts/', include('accounts.urls')),
    
    # Order #
    path('orders/', include('orders.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # add media path 
