from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt 
def login(request):
    if request.method == 'POST':
        if (request.body):
            data = json.loads(request.body)
            user = data["username"]
            password = data["password"]
        #TODO: store it
        return HttpResponse("Recieved")
    else:
        return HttpResponse("404: Route not available")


def id(request, key_id):
    if request.method == 'GET':
        return HttpResponse("Hello I am user {}".format(key_id))
    else:
        return HttpResponse("404: Route not available")
