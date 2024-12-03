from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, FileResponse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from app.forms import *
from django.urls import reverse_lazy
from typing import Dict, Any
from django.contrib import messages
from app.utils.deco import *
from adrf.views import APIView, AsyncRequest
from rest_framework.response import Response
from rest_framework import status
from app.serializers import *

async def redirect_back(request):
    return redirect(request.META.get('HTTP_REFERER'))