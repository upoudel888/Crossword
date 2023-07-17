from django.shortcuts import render,HttpResponse
# Create your views here.

def solve(request):
    return HttpResponse("This is the Solver Page")