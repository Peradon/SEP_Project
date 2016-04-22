from django.shortcuts import render
from django.contrib.auth import authenticate, login, models
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

# Create your views here.


@csrf_exempt
def authen(request):  # Authentication
    if request.method == 'POST':
        # Receive data from client
        data = json.dumps(request.POST)
        data = json.loads(data)

        # Assign to variable
        username = data.get('username')
        password = data.get('password')

        # use authenticate from Django, which is return a user object
        user = authenticate(username=username, password=password)
        print(user)

        # Check if user existed
        if user is not None:
            # user existed
            if user.is_active:
                # log user in
                login(request, user)
                return HttpResponse(username + " login")
            else:
                # can't login due to constraint
                return HttpResponse("Account disable")

        else:
            # user not existed
            return HttpResponse("Invalid username or password")


@csrf_exempt
def register(request):  # Register new user
    if request.method == 'POST':
        # Receive data from client
        data = json.dumps(request.POST)
        data = json.loads(data)

        # Check if username already in use
        numOfUser = models.User.objects.filter(username=data.get("username")).count()
        if numOfUser > 0:
            return HttpResponse("Username already in use")

        # if username already existed, the rest of function is unreachable
        # Assign to variable
        username = data.get('username')
        password = data.get('password')
        firstName = data.get('first_name')
        lastName = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')

        # create user and save
        user = models.User.objects.create_user(username=username, email=email, password=password,
                                               first_name=firstName, last_name=lastName)
        user.save()
        return HttpResponse("Complete")
