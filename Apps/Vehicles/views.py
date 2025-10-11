from django.http import HttpResponse

def index(request):
    return HttpResponse("Vehicles App OK")