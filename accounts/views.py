import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserData

@api_view(['POST'])
def signup(request):
    data = request.data  # JSON input
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=email).exists():
        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
    UserData.objects.create(user=user) 
    token = Token.objects.create(user=user)

    return Response({"token": token.key, "name": name}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return Response({"error": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "name": user.first_name}, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_user_full_data(request):
    token_key = request.data.get('token')

    if not token_key:
        return Response(
            {"error": "token is required"},
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

    profile = user.profile  # UserData via related_name

    failed_to_solve = profile.mcq_completed - profile.mcq_solved
    joined_at = user.date_joined.strftime("%d %b %Y") 

    return Response(
        {
            "name": user.first_name,
            "email": user.email,
            "joined_at": joined_at,
            "level": profile.level,
            "mcq_solved": profile.mcq_solved,
            "failed_to_solve": failed_to_solve,
        },
        status=status.HTTP_200_OK
    )