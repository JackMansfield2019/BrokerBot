from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt 
def login(request):
    if request.method == 'POST':
        if (request.body):
            data = json.loads(request.body)
            user = data["username"]
            password = data["password"]
            found = False
            #TODO: look for it in the database
            if (found):
                return JsonResponse({'username': user, 'isAuthenticated': True})
        return JsonResponse({'isAuthenticated': False})
    else:
        return HttpResponse("404: Route not available")

def register(request):
    if request.method == 'POST':
        if (request.body):
            data = json.loads(request.body)
            user = data["username"]
            password = data["password"]
        found = False
        added = False
        #TODO: look for user and try to add
        if (found):
            return JsonResponse({'alreadyExists': True, 'isAuthenticated': False})
        elif (not added):
            return JsonResponse({'alreadyExists': False, 'isAuthenticated': False})
        else: #not found and added
            return JsonResponse({'username': user, 'isAuthenticated': True})
    else:
        return HttpResponse("404: Route not available")

def id(request, key_id):
    if request.method == 'GET':
        return HttpResponse("Hello I am user {}".format(key_id))
    else:
        return HttpResponse("404: Route not available")
