from django.shortcuts import render, HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from . import conversation as cn
# Create your views here.

def home(request):
    return render(request, 'bot/index.html')

def get_response(request):
    query = request.POST['query']
    print(query)
    # self.query.delete(0)

    response = cn.resp(query)
    print(response)
    return HttpResponse("updated")
