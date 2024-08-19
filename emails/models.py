from django.db import models


class Email(models.Model):
    """Модель письма"""
    name = models.CharField(
        max_length=255,
        verbose_name='Тема'
    )
    received_date = models.DateTimeField(
        verbose_name='Дата получения'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
