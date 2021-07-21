from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
import requests 
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from ratelimit.decorators import ratelimit


def home(request):
    return HttpResponse("home page")

@ratelimit(key='ip', rate='5/m')
@api_view(['POST', 'GET'])
def index(request):
    title=""
    if request.method=='POST':
        print("helo worldd")
        title=request.POST['title']
        url = "https://api.stackexchange.com/2.3/search/advanced?&order=desc&sort=activity&q="+title+"&body="+title+"&title="+title+"&site=stackoverflow"

        data = requests.get(url)
        response = data.json()
        items = response['items']
        
        if len(items) == 0:
            context = {
                "error": "Not found"
            }
            return render(request, 'stackapp/index.html', context)
        
        context = {
            "items": items,
            "title": title
        }
        # return Response({"data": context})
        return render(request, 'stackapp/index.html', context)
    else:
        print("not found")
        context ={
            "error": "Data not found"
        }
        return render(request, 'stackapp/index.html', context)