from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.

from django.http import HttpResponse
import requests 
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from ratelimit.decorators import ratelimit



def home(request):
    return HttpResponse("home page")

# @api_view(('POST',))
@ratelimit(key='ip', rate='5/m')
@api_view(['POST', 'GET'])
# @ratelimit(key='ip', rate='5/m')
def index(request):
    title=""
    if request.method=='POST':
        print("helo worldd")
        title=request.POST['title']
        url = "https://api.stackexchange.com/2.3/search/advanced?&order=desc&sort=activity&q="+title+"&body="+title+"&title="+title+"&site=stackoverflow"
        # url = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&title="+title+"&site=stackoverflow"
        print(url)
        data = requests.get(url)
        response = data.json()
        items = response['items']

       
        # paginator = Paginator(items, 5)
        # page_number = request.GET.get('page')
        # print('page number', Paginator, page_number)
        # try:
        #     page_obj = paginator.get_page(page_number)  # returns the desired page object
        # except PageNotAnInteger:
        #     # if page_number is not an integer then assign the first page
        #     page_obj = paginator.page(1)
        # except EmptyPage:
        #     # if page is empty then return last page
        #     page_obj = paginator.page(paginator.num_pages)

        
        if len(items) == 0:
            context = {
                "error": "Not found"
            }
            return render(request, 'stackapp/index.html', context)
        
        context = {
            "items": items,
            "title": title
        }
            
        print(context)
            # context = {"error": ['data not found']}
        # return Response({"data": context})
        return render(request, 'stackapp/index.html', context)
    else:
        print("not found")
        context ={
            "error": "Data not found"
        }
        return render(request, 'stackapp/index.html', context)