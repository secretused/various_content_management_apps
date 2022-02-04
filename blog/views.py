# blog/urls.pyで呼び出される
from django.shortcuts import render
from django.http import HttpResponse


def test(request):
    return HttpResponse("test page")
