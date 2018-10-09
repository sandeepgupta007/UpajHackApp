from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from . import conversation as cn
# Create your views here.

def home(request):
    return render(request, 'bot/index.html')

def get_response(request):
    chat = request.POST['query']
    response = cn.main(chat)
    return HttpResponse(response)
