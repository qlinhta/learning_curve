from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms


def login(request):
    return render(request, 'learningcurveapp/login.html')