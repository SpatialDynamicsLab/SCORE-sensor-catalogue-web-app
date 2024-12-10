from django.shortcuts import render
import requests


def map_view(request, sensor_id=None):
    context = {}
    if sensor_id:
        context['sensor_id'] = sensor_id
    return render(request, "observations/map/map.html", context)


def official_sensors_view(request, sensor_id=None):
    return render(request, "observations/sta_official_sensors/index.html")