from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import User, UserProfile
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer, LoginSerializer
)
from .permissions import IsAdmin, IsManager, IsOwnerOrAdmin


# --------------------------------------------------------------------------------------------------------------
#Register Functionlity
# --------------------------------------------------------------------------------------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


# --------------------------------------------------------------------------------------------------------------
#Login Functionlity
# --------------------------------------------------------------------------------------------------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


# --------------------------------------------------------------------------------------------------------------
# Display user list (access only admin and manager)
# Admin can view all users (other admin, manager and employee)
# --------------------------------------------------------------------------------------------------------------
class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return User.objects.all()
        elif user.role == 'manager':
            # Managers can only see employees
            return User.objects.filter(role='employee')
        return User.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    def perform_create(self, serializer):
        # Only admins can create users
        if self.request.user.role != 'admin':
            raise permissions.PermissionDenied("Only admins can create users")
        user = serializer.save()


# --------------------------------------------------------------------------------------------------------------
# Display user details
# --------------------------------------------------------------------------------------------------------------
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def perform_destroy(self, instance):
        if instance == self.request.user:
            raise permissions.PermissionDenied("Cannot delete your own account")
        instance.delete()


# --------------------------------------------------------------------------------------------------------------
# Display Profile 
# --------------------------------------------------------------------------------------------------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer


# --------------------------------------------------------------------------------------------------------------
# Logout Functionalitu
# --------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({
            "message": "Successfully logged out"
        }, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({
            "error": "Invalid token"
        }, status=status.HTTP_400_BAD_REQUEST)
