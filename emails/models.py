from django.db import models


class Email(models.Model):
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
    files = models.JSONField(
        default=list,
        verbose_name='Прикрепленные файлы'
    )
