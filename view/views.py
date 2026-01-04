from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')


def privacyPolicy(request):
    return render(request, 'privacy_policy.html')
