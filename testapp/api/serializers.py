from django.core.cache import cache
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .constants import (
    CACHE_TTL,
    CONFIRMATION_CODE_LENGTH_LIMIT as CODE_LIMIT,
    INVITE_CODE_LENGTH_LIMIT as INVITE_LIMIT)
from .utils import get_random_uuid4_str, get_unique_invite_code
from .validators import validate_code, validate_number, validate_referal
from users.models import User


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    confirmation_code = serializers.CharField(read_only=True)

    def validate_phone_number(self, number):
        validate_number(number)
        return number

    def create_code(self):
        phone_number = self.validated_data.get('phone_number')
        confirmation_code = get_random_uuid4_str(CODE_LIMIT)
        cache.set(phone_number, confirmation_code, CACHE_TTL)
        self.validated_data['confirmation_code'] = confirmation_code


class ConfirmNumberSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(write_only=True,
                                              max_length=CODE_LIMIT)
    referal_code = serializers.CharField(write_only=True,
                                         max_length=INVITE_LIMIT,
                                         required=False)

    def validate(self, attrs):
        code, number = attrs.get('confirmation_code'), attrs.get('phone_number'
                                                                 )
        validate_number(number)
        validate_code(code, number)
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmation_code')
        code = validated_data.pop('referal_code', None)
        if code:
            validate_referal(code)
            validated_data['referal'] = User.objects.get(invite_code=code)
        validated_data['invite_code'] = get_unique_invite_code()
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ('phone_number', 'confirmation_code', 'referal_code')


class UserSerializer(serializers.ModelSerializer):
    invitees = serializers.SerializerMethodField()

    @extend_schema_field(list[str])
    def get_invitees(self, instance):
        return [person.phone_number for person in instance.invitees.all()]

    class Meta:
        model = User
        fields = ('phone_number', 'invitees')


class UserSelfSerializer(UserSerializer):

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('invite_code',)


class UserUpdateSerializer(UserSerializer):
    referal_code = serializers.CharField(write_only=True,
                                         max_length=INVITE_LIMIT)

    def update(self, instance, validated_data):
        code = validated_data.pop('referal_code')
        if code:
            validate_referal(code, instance)
            validated_data['referal'] = User.objects.get(invite_code=code)
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = UserSelfSerializer.Meta.fields + ('referal_code',)
        read_only_fields = ('phone_number', 'invitees', 'invite_code')
