from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        # user = User.objects.get(email=user_data['email'])
        # token = RefreshToken.for_user(user).access_token
        return Response({'user': user_data})


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = User.objects.filter(email=user_data['email'])
        serialized = UserSerializer(user, many=True)
        data = {
            'details': serializer.data,
            'user_info': {
                'firstname': serialized.data[0]['firstname'],
                'surname': serialized.data[0]['surname'],
                'phone': serialized.data[0]['phone'],
            }
        }

        return Response({'data': data})
