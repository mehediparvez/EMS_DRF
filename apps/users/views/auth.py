from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from apps.users.serializers.user_serializer import UserSerializer, UserDetailSerializer, LoginSerializer

User = get_user_model()


class SetRefreshCookieView(APIView):
    """
    Sets an HttpOnly cookie with the refresh token.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        expiry_date = datetime.now() + settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME', timedelta(days=7))
        
        response = Response({"detail": "Refresh token cookie set"})
        
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Strict',
            expires=expiry_date,
            path='/',
        )
        
        return response


class ClearRefreshCookieView(APIView):
    """
    Clears the HttpOnly refresh token cookie.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        response = Response({"detail": "Refresh token cookie cleared"})
        response.delete_cookie('refresh_token', path='/')
        return response


class SignUpView(generics.CreateAPIView):
    """
    View for user registration
    Endpoint: POST /api/auth/signup/
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
        Create a new user account
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    """ 
    User Login View
    Endpoint: POST /api/auth/login/
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = User.objects.filter(email=email).first()

        if user and check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    Logout View - Blacklist the refresh token
    Endpoint: POST /api/auth/logout/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
                
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating user profile
    Endpoint: GET /api/auth/profile/
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user