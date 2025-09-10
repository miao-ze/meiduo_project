from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'index_test（miao）.html')