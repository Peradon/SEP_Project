from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

# Create your views here.


def index(request):
    return HttpResponse("Receive")


@csrf_exempt
def authen(request):
    if request.method == 'POST':
        data = json.dumps(request.POST)
        print(data)
        data = json.loads(data)
        print(data.get("username"))
        #username = request.POST.get['username']
        #password = request.POST.get['password']
        #print(type(data))
        #print(data+"\n")
        #print(data["username"])
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                #login(request, user)
                return HttpResponse(username + " login")
            else:
                return HttpResponse("Account disable")

        else:
            return HttpResponse("Invalid username or password")