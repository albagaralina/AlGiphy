from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('send_email/', views.send_email, name='send_email'),
    path('success/', views.success, name='success'),  # Add success URL
    path('error/', views.error, name='error'),        # Add error URL
]
