from django.db.models import CASCADE, OneToOneField
from rest_framework.authtoken.models import Token as TokenExample
from rest_framework.authentication import TokenAuthentication as TknAuthExample

from .models import User


class Token(TokenExample):
    user = OneToOneField(
        User,
        CASCADE,
        related_name='auth_token',
        verbose_name='User'
    )


class TokenAuthentication(TknAuthExample):
    model = Token
