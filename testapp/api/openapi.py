from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.serializers import CharField


token_return = extend_schema(
    responses={
        200: inline_serializer(
            'Токен выдан успешно',
            fields={
                'token': CharField()
            }
        )
    }
)
