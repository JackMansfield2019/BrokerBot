from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from passlib.hash import pbkdf2_sha256
from server.database.UsersTest import *


@csrf_exempt
def login(request):
    if request.method == 'POST':
        if (request.body):
            data = json.loads(request.body)
            user = data["username"]
            password = data["password"]

            # TODO: look for it in the database
            found = find_user(user, password)
            # As a note, in order to do the encryption you must call pbkdf2_sha256.verify(password, foundPassword)
            # where foundPassword is the password for the username that you find in the database
            # No decrption or rehashing, just using the library's verify function
            if len(found) != 0:
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
            # found = False
            # added = False
            hashedPassword = pbkdf2_sha256.hash(password)
            # TODO: look for user and try to add (use hashedPassword for add instead of plain password)
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
