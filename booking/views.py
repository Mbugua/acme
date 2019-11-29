from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    '''
    landing page
    '''
    return render(request, 'index.html')
