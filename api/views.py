from django.shortcuts import render, redirect
from django.http import HttpResponse


def save(request):
    return HttpResponse('save method')