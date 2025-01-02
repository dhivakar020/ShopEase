from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .models import User
from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.conf import settings
import jwt

@api_view(['POST'])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # Create the user

        # Generate JWT token upon signup
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'User created successfully!',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        print(f"Email: {email}, Password: {password}")
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)  # Email is treated as username here
        if user:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login successful!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role,
                #'redirect_url': role_redirect_url,
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProfileView(APIView):
    def get(self, request):
        # Extract the token from the request headers
        token = request.headers.get("Authorization", "").split("Bearer ")[-1]

        if not token:
            return Response({"error": "Token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode the JWT to get the user ID
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the user object
        user = get_object_or_404(User, id=user_id)

        # Serialize and return the user profile data
        profile_data = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "is_active": user.is_active,
        }

        return Response({"profile": profile_data}, status=status.HTTP_200_OK)