"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard.html')


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Front End Pages
    path("", dashboard_view, name="dashboard"),

    path('login/', TemplateView.as_view(template_name="auth/login.html"), name='login'),
     path('register/', TemplateView.as_view(template_name="auth/register.html"), name='register'),
    
    # API routes (register, login, dashboard, etc.)
    path('api/', include('core.urls')),
    path('api/stores/', include('stores.urls')),
    path("api/marketplace/", include("marketplace.urls")),
    path('api/accounts/', include('accounts.urls')),
   

]
