from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, FileResponse
from django.views.generic import CreateView, UpdateView
from app.forms import *
from django.urls import reverse_lazy
from typing import Dict, Any
from adrf.views import APIView, AsyncRequest
from rest_framework.response import Response
from rest_framework import status
from app.serializers import *
from asgiref.sync import sync_to_async


async def redirect_back(request):
    return redirect(request.META.get('HTTP_REFERER'))