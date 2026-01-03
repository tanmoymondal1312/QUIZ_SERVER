from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from app_quiz.models import Quiz
from .models import UserData



@api_view(['POST'])
def get_user_level(request):
    data = request.data
    token_key = data.get('token')

    # 🔐 Verify token
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return Response(
            {"error": "Invalid or expired token"},
            status=status.HTTP_401_UNAUTHORIZED
        )


    level = user.profile.level 

    return Response({"level": level}, status=status.HTTP_200_OK)

@api_view(['POST'])
def get_quiz_perfomance(request):
    data = request.data
    token_key = data.get('token')

    # 🔐 Verify token
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return Response(
            {"error": "Invalid or expired token"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    mcq_solved = user.profile.mcq_solved
    mcq_completed = user.profile.mcq_completed

    return Response({"mcq_solved": mcq_solved, "mcq_completed": mcq_completed}, status=status.HTTP_200_OK)





@api_view(['POST'])
def uquiz_seen(request):
    token_key = request.data.get('token')
    quiz_id = request.data.get('quiz_id')

    if not token_key or not quiz_id:
        return Response(
            {"error": "token and quiz_id are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔐 Verify token
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return Response(
            {"error": "Invalid or expired token"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # 🎯 Get quiz
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response(
            {"error": "Quiz not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # 👀 Mark as seen (idempotent)
    already_seen = quiz.seen_by.filter(id=user.id).exists()
    if not already_seen:
        quiz.seen_by.add(user)

    return Response(
        {
            "message": "Quiz marked as seen",
        },
        status=status.HTTP_200_OK
    )



@api_view(['POST'])
def update_user_mcq_solved_mcq_completed(request):
    token_key = request.data.get('token')
    quiz_id = request.data.get('quiz_id')
    mcq_solved = request.data.get('mcq_solved')  # boolean expected

    if token_key is None or quiz_id is None or mcq_solved is None:
        return Response(
            {"error": "token, quiz_id and mcq_solved are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔐 Verify token
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return Response(
            {"error": "Invalid or expired token"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # 🎯 Get quiz
    try:
        quiz = Quiz.objects.get(id=quiz_id)
    except Quiz.DoesNotExist:
        return Response(
            {"error": "Quiz not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # 📊 Get user data
    try:
        user_data = user.profile
    except UserData.DoesNotExist:
        return Response(
            {"error": "UserData not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # ✅ Update mcq_completed (always)
    user_data.mcq_completed += 1

    # ✅ Update mcq_solved (only if true)
    if mcq_solved is True:
        user_data.mcq_solved += 1

    user_data.save()

    return Response(
        {
            "message": "User MCQ states updated successfully",
        },
        status=status.HTTP_200_OK
    )




@api_view(['POST'])
def leaderboard(request):
    token_key = request.data.get('token')

    # 🔐 Verify token
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
    except Token.DoesNotExist:
        return Response(
            {"error": "Invalid or expired token"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # 🏆 Top 50 users by mcq_solved
    top_users_qs = (
        UserData.objects
        .select_related('user')
        .order_by('-mcq_solved', 'user__id')[:50]
    )

    leaderboard_data = []
    for index, u in enumerate(top_users_qs, start=1):
        leaderboard_data.append({
            "rank": index,
            "id": u.user.id,
            "name": u.user.first_name,
            "mcq_solved": u.mcq_solved
        })

    # 📍 Current user rank
    user_mcq_solved = user.profile.mcq_solved

    user_rank = (
        UserData.objects
        .filter(mcq_solved__gt=user_mcq_solved)
        .count() + 1
    )

    return Response(
        {
            "leaderboard": leaderboard_data,
            "user_rank": user_rank,
            "user_mcq_solved": user_mcq_solved
        },
        status=status.HTTP_200_OK
    )