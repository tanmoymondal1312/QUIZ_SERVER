from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')


def privacyPolicy(request):
    return render(request, 'privacy_policy.html')

def Terms(request):
    return render(request, 'terms.html')

def DataSetection(request):
    return render(request, 'data_detection.html')