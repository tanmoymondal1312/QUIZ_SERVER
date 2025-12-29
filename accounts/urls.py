from django.urls import path
from .views import signup, login
from .views_data_sender import get_user_level,get_quiz_perfomance

urlpatterns = [
    path('api/signup', signup),
    path('api/login', login),

    path('api/get-user-level', get_user_level),
    path('api/get-quiz-performance', get_quiz_perfomance),

]
