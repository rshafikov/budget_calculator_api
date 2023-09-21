from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('user', 'user'),
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default='user',
        max_length=9,
    )
    currency = models.CharField(max_length=5, default='RUB')
    tg_id = models.CharField(max_length=15, default='')

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return f'{self.username}'


class Category(models.Model):
    category_name = models.CharField(max_length=30, blank=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='categories',
    )

    def __str__(self):
        return f'{self.category_name}'


class Record(models.Model):
    amount = models.FloatField()
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='records'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=False,
        related_name='records'
    )
    created = models.DateTimeField("Дата публикации", default=timezone.now)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.category}: {self.amount} {self.user.currency}'
