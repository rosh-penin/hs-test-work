from rest_framework.permissions import IsAuthenticated


class IsSelfUserOrReadOnly(IsAuthenticated):
    """
    Наследуется от класса IsAuthenticated.
    Добавляет проверку для получения объекта.
    Подходит только для изменения данных пользователя.
    """
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and
                request.user.phone_number == obj.phone_number)
