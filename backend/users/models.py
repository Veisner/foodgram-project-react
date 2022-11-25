from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'
    ROLES = (
        (ROLE_USER, 'Пользователь'),
        (ROLE_ADMIN, 'Администратор'),
    )
    role = models.CharField(
        choices=ROLES,
        max_length=10,
        verbose_name='Роль пользователя',
        default=ROLE_USER
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )
    password = models.TextField(
        max_length=150,
        verbose_name='Пароль'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.TextField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.TextField(
        max_length=150,
        verbose_name='Фамилия'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
