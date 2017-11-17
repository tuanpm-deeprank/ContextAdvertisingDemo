# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.shortcuts import redirect

def index(request):
    if request.method == 'POST':
        es = Elasticsearch([{'host':'10.12.11.161', 'port':9200}])

        username = request.POST['username']
        password = request.POST['password']

        search = es.search(index="adserver", doc_type="users", body={"query":{"match":{'username':username}}})
        print search['hits']['total']
        exist = search['hits']['total']
        print exist        
        return redirect("signad")
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        es = Elasticsearch([{'host':'10.12.11.161', 'port':9200}])

        username = request.POST['username']
        password = request.POST['password']
        
        search = es.search(index="adserver", doc_type="users", body={"query":{"match":{'username':username}}})
        print search['hits']['total']
        exist = search['hits']['total']
        if exist != 0:
            success = es.index(index = "adserver", doc_type="user", body= {"username":username, "password":password})
        return redirect('index')
    return render(request, 'signup.html')

def signad(request):
    if request.method == 'POST' and request.FILES['imagead']:
        es = Elasticsearch([{'host':'10.12.11.161', 'port':9200}])

        imagead = request.FILES['imagead']
        #print imagead
        fs = FileSystemStorage()
        filename = fs.save(imagead.name, imagead)
        #print filename
        uploaded_file_url = fs.url(filename)
        #print uploaded_file_url

        adname = request.POST['namead']
        catead = request.POST['catead']

        success = es.index(index = "adserver", doc_type="adimage", body= {"adname":adname, "catead":catead, "imagead":uploaded_file_url})

        return HttpResponse('ok')
    return render(request, 'signad.html')