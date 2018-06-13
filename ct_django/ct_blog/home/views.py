from django.shortcuts import render

def home(request):
    return render(request, "home/home.html")
    #qs = PostModel.objects.all()
