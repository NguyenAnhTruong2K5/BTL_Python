from django.http import HttpResponse

def index(request):
    return HttpResponse("Accounts App OK")