from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from . import conversation as cn
import sys
import js2py
import pprint
import json

# Create your views here.

def home(request):
    # js = """
    # function evaluate(){
    # if("geolocation" in navigator){
    #   navigator.geolocation.getCurrentPosition(function(position) {
    #     const Http = new XMLHttpRequest();
    #     const url='http://dev.virtualearth.net/REST/v1/Locations/' + position.coords.latitude + ','+ position.coords.longitude + '?key=AoTJ0es6QeGwvVw9Fb4LCrAhUtdt6ZeDN-eWENSWR8ddNEWPWQ0pTvsA1HZ1ktJj';
    #     Http.open("GET", url);
    #     Http.send();
    #     Http.onreadystatechange=(e)=>{
    #     console.log(Http.responseText)
    #     }
    #   });
    # }
    # else{
    #   console.log("NOOOOO")
    # }
    # }
    # """.replace("console.log", "return")
    # result = js2py.eval_js(js)
    # print(result.value)

    return render(request, 'bot/index.html')

def get_response(request):
    query = request.POST['query']

    response = cn.chatDriver(query)

    # try:
    #     response = cn.main(query)
    # except:
    #     response = "Sorry, I can't process right now!"

    return JsonResponse(response, safe=False)