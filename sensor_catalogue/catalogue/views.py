from django.shortcuts import render
from django.http import HttpResponse


def homeview(request):
    return HttpResponse(
      "<br>"
      "<h1>SCORE Sensor Catalogue</h1>"
      "<h2>We are updating the web app at this moment...</h2> ")
