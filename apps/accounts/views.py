import json

from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods


def home(request):
    context = {
        'items': ['one', 'two', 'three'],
    }
    return render(request, 'accounts/home.html', context=context)

def enrepreneur_page(request):
    return render(request, "accounts/entrepreneur-floor-panel.html")