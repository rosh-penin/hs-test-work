from django.db import models


class User(models.Model):
    """Кастомная модель пользователей. Не наследуется от AbstractUser."""
    phone_number = models.CharField('Телефонный номер', max_length=16,
                                    unique=True)
    invite_code = models.CharField('Код для приглашений', max_length=6,
                                   unique=True)
    referal = models.ForeignKey(
        'self',
        models.SET_NULL,
        related_name='invitees',
        blank=True,
        null=True
    )
    is_active = True

    class Meta:
        ordering = ('-phone_number',)

    def __str__(self):
        return self.phone_number

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
