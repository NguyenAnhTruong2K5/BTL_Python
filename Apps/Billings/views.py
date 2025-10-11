from django.http import HttpResponse

def index(request):
    return HttpResponse("Billing App OK")