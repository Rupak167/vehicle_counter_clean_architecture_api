from django.views import View
from django.shortcuts import render

class Index(View):
    @staticmethod
    def get(request):
        return render(request, "public/index.html")