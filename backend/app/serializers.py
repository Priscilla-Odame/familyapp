from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        max_length=68,
        min_length=6,
        write_only=True
        )

    class Meta:
        model = User
        fields = ['firstname', 'surname', 'maidenname', 'phone', 'email', 'password']

    def validate(self, attrs):
        firstname = attrs.get('firstname', '')
        surname = attrs.get('surname', '')
        maidenname = attrs.get('maidenname', '')
        phone = attrs.get('phone', '')
        email = attrs.get('email', '')

        if firstname is None:
            serializers.ValidationError('The first name field is required')
        if surname is None:
            serializers.ValidationError('The surname field is required')
        if maidenname is None:
            serializers.ValidationError('The maiden name is required')
        if email is None:
            serializers.ValidationError('The email field is required')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=225, min_length=3)
    username = serializers.CharField(
        max_length=225,
        min_length=3,
        read_only=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        max_length=225,
        min_length=3,
        write_only=True)
    tokens = serializers.CharField(max_length=68, min_length=3, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'tokens')

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid Credential. Try again')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
