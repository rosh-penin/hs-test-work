import re

from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from users.models import User


def validate_number(number: str):
    """
    Проверяет телефонный номер.
    Номер должен начинаться либо с +7, либо с 8.
    Длина должна быть не больше 16 знаков.
    """
    rule = re.compile(r'^(\+7|8)\d{1,14}$')
    if not rule.fullmatch(number):
        raise ValidationError('Введен неправильный номер телефона.')


def validate_code(code, number):
    """Проверяет код подтверждения."""
    cached_code = cache.get(number)
    if code != cached_code:
        raise ValidationError('Код подтверждения не подходит.')


def validate_referal(code, instance=None):
    if instance and instance.referal:
        raise ValidationError('Реферальный код уже введен.')
    if not User.objects.filter(invite_code=code).exists():
        raise ValidationError('Неверный реферальный код.')
