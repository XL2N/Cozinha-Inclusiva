from django.shortcuts import render

def home_adm(request):
    return render(request, 'administrativo/home.html')

def dashboard(request):
    return render(request, 'administrativo/dashboard.html')