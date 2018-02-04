from django.shortcuts import render

from django.http import HttpResponse # Added by JNR 18.01.2018

def index(request):
    return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>") # Added 18.01.2018

def about(request):
    return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>") # Added 18.01.18
