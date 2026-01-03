import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Quiz, QuizCategory


@api_view(['POST'])
def get_quiz(request):
    data = request.data

    token_key = data.get('token')
    category_slug = data.get('category')   # slug OR "daily_challenge"
    limit = data.get('limit')

    if not token_key or not category_slug or not limit:
        return Response(
            {"error": "token, category and limit are required"},
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

    # ============================
    # 🎯 DAILY CHALLENGE LOGIC
    # ============================
    if category_slug == "daily_challenge":

        quizzes = (
            Quiz.objects
            .exclude(seen_by=user)
            .order_by('?')[:15]   # random 15 from all categories
        )

        if not quizzes.exists():
            return Response(
                {"message": "No new daily challenge quizzes available"},
                status=status.HTTP_200_OK
            )

        quiz_data = []
        for quiz in quizzes:
            quiz_data.append({
                "id": quiz.id,
                "question": quiz.question,
                "optA": quiz.optA,
                "optB": quiz.optB,
                "optC": quiz.optC,
                "optD": quiz.optD,
                "correct_ans": quiz.correct_ans
            })

        return Response(
            {
                "user": user.username,
                "category": "daily_challenge",
                "total": len(quiz_data),
                "quizzes": quiz_data
            },
            status=status.HTTP_200_OK
        )

    # ============================
    # 📚 NORMAL CATEGORY LOGIC
    # ============================
    try:
        category = QuizCategory.objects.get(slug=category_slug)
    except QuizCategory.DoesNotExist:
        return Response(
            {"error": "Category not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    quizzes = (
        Quiz.objects
        .filter(category=category)
        .exclude(seen_by=user)
        .order_by('id')[:int(limit)]
    )

    if not quizzes.exists():
        return Response(
            {"message": "No new quizzes available for this category"},
            status=status.HTTP_200_OK
        )

    quiz_data = []
    for quiz in quizzes:
        quiz_data.append({
            "id": quiz.id,
            "question": quiz.question,
            "optA": quiz.optA,
            "optB": quiz.optB,
            "optC": quiz.optC,
            "optD": quiz.optD,
            "correct_ans": quiz.correct_ans
        })

    return Response(
        {
            "user": user.username,
            "category": category.slug,
            "total": len(quiz_data),
            "quizzes": quiz_data
        },
        status=status.HTTP_200_OK
    )
