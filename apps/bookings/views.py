from django.shortcuts import render

# Create your views here.

def home(request):
    context = {
        "items": ["one", "two", "three"],
    }
    return render(request, "bookings/home.html", context)

def enrepreneur_page(request):
    return render(request, "bookings/entrepreneur-floor-panel.html")