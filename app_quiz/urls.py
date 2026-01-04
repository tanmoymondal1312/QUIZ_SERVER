from django.urls import path
from .views import check_app_update, get_quiz
from .views_developer import import_quizzes

urlpatterns = [
    path('api/get-quiz', get_quiz),
    path('api/import-quizzes', import_quizzes),
    path('check-update', check_app_update, name="check_app_update"),

]
