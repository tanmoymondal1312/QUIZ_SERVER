from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token



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