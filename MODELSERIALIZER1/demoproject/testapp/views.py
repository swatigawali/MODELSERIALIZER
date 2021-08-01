from functools import partial
from django.shortcuts import render
from django.views.generic import View
import io
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.serializers import Serializer
from .models import Task
from .serializers import Taskserializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@method_decorator(csrf_exempt,name="dispatch")
class TaskCBV(View):
    def get(self,request,*args,**kwargs):
        json_data = request.body
        stream =io.BytesIO(json_data)
        data=JSONParser().parse(stream)
        id=data.get("id",None)
        if id is not None:
            tsk=Task.objects.get(id=id)
            serializer=Taskserializer(tsk)
            json_data=JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type="application/json")
        qs=Task.objects.all()
        serializer=Taskserializer(qs,many=True)
        json_data=JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type="application/json")
    
    def post(self,request,*args,**kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        data=JSONParser().parse(stream)
        serializer=Taskserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            msg={"msg":"Resource created successfully"}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data,content_type="application/json")
       
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type="application/json")

    def put(self,request,*args,**kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        data=JSONParser().parse(stream)
        id=data.get("id")
        tsk=Task.objects.get(id=id)
        serializer=Taskserializer(tsk,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            msg={"msg":"Resource Update successfylly"}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data,content_type="application/json")
        json_data=JSONRenderer.render(serializer.errors)
        return HttpResponse(json_data,content_type="application/json")

    def delete(self,request,*args,**kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        data=JSONParser().parse(stream)
        id=data.get('id',None)
        if id is not None:
            tsk=Task.objects.get(id=id)
            tsk.delete()
            msg={'msg':"Resource deleted successfully"}
            json_data=JSONRenderer().render(msg)
            return HttpResponse(json_data,content_type="application/json")
        msg={'msg':"Please Enter Valid ID"}
        json_data=JSONRenderer().render(msg)
        return HttpResponse(json_data,content_type="application/json")
        



        









