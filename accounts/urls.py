from django.urls import path
from .views import signup, login

urlpatterns = [
    path('api/signup', signup),
    path('api/login', login),
]
