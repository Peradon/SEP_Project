from django.shortcuts import render
from django.contrib.auth import authenticate, login, models, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import TodoList, UserModel, ChatRoom
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


# get all user
@csrf_exempt
def get_User(request):
    # get user from db
    allUser = User.objects.filter(is_superuser=False)

    # create dict for json
    name_list = dict()
    i = 1
    for user in allUser:
        name_list["user" + str(i)] = user.get_full_name()
        i += 1

    print(name_list)
    return HttpResponse(json.dumps(name_list))


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


@csrf_exempt
def addTodo(request):
    if request.method == 'POST':
        data = json.dumps(request.POST)
        data = json.loads(data)

        # get full name
        fullName = data.get("user")

        # split full name
        fullName = fullName.split()

        # assign first and last name to variable
        first = fullName[0]
        last = fullName[1]
        print(User.objects.get(first_name=first, last_name=last))

        # get UserModel
        user = UserModel.objects.get(user=User.objects.get(first_name=first, last_name=last))
        taskd = data.get("taskDescription")
        responseJsons = {}
        if user is not None and taskd is not None:
            tdlist = TodoList(user=user, taskDescription=taskd)
            tdlist.save()
            return HttpResponse("todo added")


@csrf_exempt
def getTodo(request):
    # get user model from cookie
    sessions = Session.objects.get(session_key=request.COOKIES["sessionid"])
    user = User.objects.get(id__in=sessions.get_decoded()["_auth_user_id"])
    userModel = UserModel.objects.get(user=user)

    # get to do list of that user
    todoList = TodoList.objects.filter(user=userModel)
    allTask = dict()

    # add Task in to dict
    i = 1
    for item in todoList:
        print(i)
        allTask["work"+str(i)] = item.get_description()
        i += 1

    # dumps add return
    print(allTask)
    return HttpResponse(json.dumps(allTask))


@csrf_exempt
def deleteTodo(request):
    if request.method == 'POST':
        data = json.dumps(request.POST)
        data = json.loads(data)

        # get data
        des = data.get("des")

        # find that todolist
        t = TodoList.objects.filter(taskDescription=des)

        # delete it
        t.delete()
        return HttpResponse("Done")


@csrf_exempt
def createChat(request):
    if request.method == 'POST':
        data = json.dumps(request.POST)
        data = json.loads(data)

        # get data
        roomIPin = data.get("roomIP")
        roomPortin = data.get("roomPort")
        roomNamein = data.get("roomName")

        # create instance
        g = ChatRoom(roomIP=roomIPin, roomPort=roomPortin, roomName=roomNamein)
        # save
        g.save()

        return HttpResponse("Done")


