from django.shortcuts import render

def home(request):
    return render(request, "home/home.html")

def mobile(request):
    return render(request, "mobile/mobile.html")

