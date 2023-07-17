from django.shortcuts import render,HttpResponse
# Create your views here.

def generate(request):
    return HttpResponse("This is the Generator Page")