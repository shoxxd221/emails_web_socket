# Generated by Django 5.1 on 2024-08-19 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Тема')),
                ('received_date', models.DateTimeField(verbose_name='Дата получения')),
                ('text', models.TextField(verbose_name='Текст')),
                ('files', models.JSONField(default=list, verbose_name='Прикрепленные файлы')),
            ],
        ),
    ]
