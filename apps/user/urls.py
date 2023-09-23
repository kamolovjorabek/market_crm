from django.urls import path
from .views import custom_login, custom_register
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', custom_login, name='custom_login'),
    path('register/', custom_register, name='custom_register')
]
