from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Record(models.Model):
    amount = models.IntegerField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='records'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True
    )
    created = models.DateTimeField("Дата публикации", auto_now_add=True)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'[{self.category}: {self.amount} руб.]'
