from django.urls import path
from .views import get_quiz
from .views_developer import import_quizzes

urlpatterns = [
    path('api/get-quiz', get_quiz),
    path('api/import-quizzes', import_quizzes),
]
