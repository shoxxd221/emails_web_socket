from django.shortcuts import render


def gmail(request):
    return render(request, 'gmail.html')


def mail(request):
    return render(request, 'mail.html')


def yandex(request):
    return render(request, 'yandex.html')
