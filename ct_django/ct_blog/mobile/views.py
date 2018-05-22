from django.shortcuts import render
from .models import MobileModel

def list(request):
    ct = MobileModel.objects.all()
    return render(request, 'mobile/mobile.html', {"ct":ct})