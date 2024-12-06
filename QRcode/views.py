from django.shortcuts import render

def home(request):
    return render(request, 'QRcode/home.html')
