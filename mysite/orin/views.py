from django.shortcuts import render


def index(request):
    return render(request, 'orin/index.html')

def about(request):
    return render(request, 'orin/about.html')