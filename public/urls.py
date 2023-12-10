from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import never_cache
from .api import ProcessVideoFile
from django.contrib import admin
from django.urls import path
from .views import Index


app_name = "public"
urlpatterns = [
    path("", never_cache(csrf_exempt(Index.as_view())), name="index"),
    path("process/", never_cache(csrf_exempt(ProcessVideoFile.as_view())), name="process")
]
