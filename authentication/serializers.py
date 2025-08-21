from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import User, UserProfile


# --------------------------------------------------------------------------------------------------------------
# user profile serializer class 
# --------------------------------------------------------------------------------------------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'address', 'date_of_birth']


# --------------------------------------------------------------------------------------------------------------
# User serializer class 
# --------------------------------------------------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'role', 'phone', 'department', 'is_active', 'created_at', 'profile']
        read_only_fields = ['id', 'created_at']
  
        
# --------------------------------------------------------------------------------------------------------------
# Updating user profile
# --------------------------------------------------------------------------------------------------------------        
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'address', 'date_of_birth']
        extra_kwargs = {
            'bio': {'required': False},
            'avatar': {'required': False},
            'address': {'required': False},
            'date_of_birth': {'required': False},
        }
        
 # --------------------------------------------------------------------------------------------------------------
# Creating new User
# --------------------------------------------------------------------------------------------------------------  
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True)

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Username already taken")]
    )
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Phone number already in use")]
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'confirm_password', 'role', 'phone', 'department'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


# --------------------------------------------------------------------------------------------------------------
# To update user details
# --------------------------------------------------------------------------------------------------------------
class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileUpdateSerializer(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'department', 'is_active', 'role', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super().update(instance, validated_data)

        if profile_data:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return user

# --------------------------------------------------------------------------------------------------------------
# Logout serializer
# --------------------------------------------------------------------------------------------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('Account is deactivated')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')

        return attrs