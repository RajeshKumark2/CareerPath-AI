from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer
import random
import string
from datetime import timedelta
from django.utils import timezone

class UserViewSet(viewsets.ModelViewSet):
    """
    User registration, login, and profile management
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'register']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Register a new user
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create user profile
            UserProfile.objects.create(user=user, phone=request.data.get('phone'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def verify_phone(self, request):
        """
        Verify phone OTP
        """
        otp = request.data.get('otp')
        user_profile = request.user.profile
        
        # Verify OTP logic here
        user_profile.phone_verified = True
        user_profile.save()
        
        return Response({'message': 'Phone verified successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def verify_email(self, request):
        """
        Verify email OTP
        """
        otp = request.data.get('otp')
        user_profile = request.user.profile
        
        # Verify OTP logic here
        user_profile.email_verified = True
        user_profile.save()
        
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """
        Get user profile
        """
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """
        Update user profile
        """
        user_profile = request.user.profile
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
