# CORE VIEW  MODULE

from django.shortcuts import render

def index(request):
    return render(request, 'core/frontend/home.html')