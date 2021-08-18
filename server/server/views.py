import json
from passlib.hash import pbkdf2_sha256
from database.UsersTest import *


@csrf_exempt
def login(request):
    if request.method == 'POST':
        if (request.body):
            data = json.loads(request.body)
            user = data["username"]
            password = data["password"]

            # TODO: look for it in the database
            found = find_user(user, password)
            if found == 1:
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
            found, added = insert_user(user, password)
            if found:
                return JsonResponse({'alreadyExists': True, 'isAuthenticated': False})
            elif not added:
                return JsonResponse({'alreadyExists': False, 'isAuthenticated': False})
            else:  # not found and added
                return JsonResponse({'username': user, 'isAuthenticated': True})
    else:
        return HttpResponse("404: Route not available")


# TODO: remove or add for debug mode
def id(request, key_id):
    if request.method == 'GET':
        # TODO: display user from database/more information or something
        return HttpResponse("Hello I am user {}".format(key_id))
    else:
        return HttpResponse("404: Route not available")


def getBotInfoWithID(request, bot_id):
    if request.method == 'GET':
        key = 1 #database call here
        return JsonResponse({'alpacaKey': key})
    else:
        return HttpResponse("404: Route not available")
    
def getBotInfo(request):
    if request.method == 'GET':
        keys = [] #database call here
        return JsonResponse({'alpacaKeys': keys})
    else:
        return HttpResponse("404: Route not available")

def runTests(request):