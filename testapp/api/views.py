from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from .openapi import token_return
from .permissions import IsSelfUserOrReadOnly
from .serializers import (ConfirmNumberSerializer, PhoneNumberSerializer,
                          UserSelfSerializer, UserSerializer,
                          UserUpdateSerializer)
from users.authentication import Token
from users.models import User
from .validators import validate_code


class AuthViewset(GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'number':
            return PhoneNumberSerializer
        return ConfirmNumberSerializer

    @action(['POST'], detail=False)
    def number(self, request, *args, **kwargs):
        """Отдает пользователю код подтверждения телефона."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        serializer.create_code()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def _create_token(self, user):
        token, status = Token.objects.get_or_create(user=user)
        return token

    @token_return
    @action(['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        """
        Экшен проверяет есть ли пользователь в базе данных.
        Если есть - получает для него токен.
        Если нет - создает пользователя и получает токен.
        Плюс проверка кода подтверждения, полученного в экшене number.
        """
        number = request.data.get('phone_number')
        if User.objects.filter(phone_number=number).exists():
            code = request.data.get('confirmation_code')
            validate_code(code, number)
            user = User.objects.get(phone_number=number)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        token = self._create_token(user)
        return Response({'token': token.key}, status=HTTP_201_CREATED)


class UsersViewset(GenericViewSet, ListModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    permission_classes = [IsSelfUserOrReadOnly]
    serializer_class = UserSerializer
    lookup_field = 'phone_number'
    http_method_names = ['get', 'patch']

    def get_serializer_class(self):
        if self.action == 'me':
            return UserSelfSerializer
        if self.action == 'partial_update':
            return UserUpdateSerializer
        return UserSerializer

    @action(['GET'], detail=False)
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
