from django.shortcuts import render

# Create your views here.

def home(request):
    context = {
        "items": ["one", "two", "three"],
    }
    return render(request, "bookings/home.html", context)