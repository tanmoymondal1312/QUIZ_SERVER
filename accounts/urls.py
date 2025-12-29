from django.urls import path
from .views import signup, login
from .views_data_sender import get_user_level,get_quiz_perfomance,uquiz_seen,update_user_mcq_solved_mcq_completed

urlpatterns = [
    path('api/signup', signup),
    path('api/login', login),

    path('api/get-user-level', get_user_level),
    path('api/get-quiz-performance', get_quiz_perfomance),
    path('api/put-mark-as-seen', uquiz_seen),
    path('api/update-mcq-states', update_user_mcq_solved_mcq_completed),

]
