from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def home(request):
    context = {
        'items': ['one', 'two', 'three'],
    }
    return render(request, 'accounts/home.html', context=context)

