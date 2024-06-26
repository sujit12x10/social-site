from django.urls import path, include
from account import views

urlpatterns = [
    path('logut/', views.custom_logout, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    # path('edit/', views.edit, name='edit_profile'),
]