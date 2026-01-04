from django.urls import path
from .views import home,privacyPolicy

urlpatterns = [
    path('', home),
    path('privacy-policy', privacyPolicy),
]
