from django.shortcuts import render
from django.contrib.auth import authenticate, login, models, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
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
        # Check if user existed
        if user is not None:
            # user existed
            if user.is_authenticated:
                # log user in
                login(request, user)
                data = {'first_name': user.first_name, 'last_name': user.last_name}
                print(request.session.session_key)
                return HttpResponse(json.dumps(data))
            else:
                # can't login due to constraint
                return HttpResponse("error 1")

        else:
            # user not existed
            return HttpResponse("Invalid username or password")

def todo(request):
    pass


@csrf_exempt
def signOut(request):
    # user = request.POST
    # user = User.objects.get(first_name=user)
    # [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
    # user.is_active = False
    print(request.session.session_key)
    logout(request)
    return HttpResponse("logout")


@csrf_exempt
def get_Session(request):

    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())

    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    print(uid_list)

    userItem = dict()
    i = 1
    for items in uid_list:
        userItem["user" + str(i)] = models.User.objects.get(id__in=items).get_full_name()
        i += 1
    print(userItem)
    # Query all logged in users based on id list
    return HttpResponse(json.dumps(userItem))

    def addTodo(request):
        if request.method == 'POST':
            data = json.dumps(request.POST)
            data = json.loads(data)
            user = data.get("user")
            taskd = data.get("taskDescription")
            responseJsons = {}
            if user is not None and taskd is not None:
                tdlist=TodoList(user=user,taskDescription=taskd)
                tdlist.save()

            return HttpResponse("todo added")



