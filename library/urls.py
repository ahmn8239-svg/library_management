"""
URL configuration for library project.
"""
from django.contrib import admin
from django.urls import path, include
# from . import views # old home view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    
  
    path('', include('core.urls', namespace='core')),
    
    path('accounts/', include('django.contrib.auth.urls')),
]
