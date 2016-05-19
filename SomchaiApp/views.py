from django.shortcuts import render
from django.contrib.auth import authenticate, login, models, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import TodoList, UserModel, ChatRoom, MeetingRoom, Reservation
import json
import re


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
def deleteChat(request):
    # get user model from cookie
    sessions = Session.objects.get(session_key=request.COOKIES["sessionid"])
    user = User.objects.get(id__in=sessions.get_decoded()["_auth_user_id"])
    userModel = UserModel.objects.get(user=user)
    num = ChatRoom.objects.filter(owner=userModel).count()
    if(num != 0):
        chatRoom = ChatRoom.objects.filter(owner=userModel)
        chatRoom.delete()


@csrf_exempt
def signOut(request):
    # user = request.POST
    # user = User.objects.get(first_name=user)
    # [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
    # user.is_active = False
    deleteChat(request)
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
        allTask["work"+str(i)] = item.get_description()
        i += 1

    # dumps add return
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
        # get user model from cookie
        sessions = Session.objects.get(session_key=request.COOKIES["sessionid"])
        user = User.objects.get(id__in=sessions.get_decoded()["_auth_user_id"])
        userModel = UserModel.objects.get(user=user)

        data = json.dumps(request.POST)
        data = json.loads(data)
        print(data)

        # get data
        roomIPin = data.get("roomIP")
        roomPortin = data.get("roomPort")
        roomNamein = data.get("roomName")

        # create instance
        g = ChatRoom(chatIP=roomIPin, chatPort=roomPortin, chatName=roomNamein, owner=userModel)
        # save
        g.save()

        return HttpResponse("Done")


@csrf_exempt
def getChatRoom(request):
    if request.method == "GET":
        if ChatRoom.objects.all().count() != 0:
            c = ChatRoom.objects.all()
            allChat = dict()
            i = 1
            for item in c:
                single = dict()
                single["chatName"] = item.get_room_name()
                single["chatIP"] = item.get_room_ip()
                single["chatPort"] = item.get_room_port()
                single["owner"] = item.get_user().get_fullname()
                allChat["room" + str(i)] = single
                i += 1

            return HttpResponse(json.dumps(allChat))

        else:
            return HttpResponse("no room")




@csrf_exempt
def getRoom(request):
    room = MeetingRoom.objects.all()

    allRoom = dict()

    # add Task in to dict
    i = 1
    for item in room:
        allRoom["room"+str(i)] = item.get_room()
        i += 1

    # dumps add return
    return HttpResponse(json.dumps(allRoom))


@csrf_exempt
def makeReserve(request):
    if request.method == 'POST':
        # get user model from cookie
        sessions = Session.objects.get(session_key=request.COOKIES["sessionid"])
        user = User.objects.get(id__in=sessions.get_decoded()["_auth_user_id"])
        userModel = UserModel.objects.get(user=user)

        # receive
        data = json.dumps(request.POST)
        data = json.loads(data)

        # get data
        topicin = data.get("topic")
        roomStart = data.get("roomStart")
        roomEnd = data.get("roomEnd")
        roomin = data.get("room")

        # query on the same day
        startList = roomStart.split(" ")
        date = startList[0]
        date = date.split("-")
        obj = Reservation.objects.filter(start__year=date[0], start__month=date[1], start__day=date[2], room=roomin)
        print(obj)

        for i in obj:
            if(i.get_start() < roomStart and roomStart > i.get_end() or i.get_start() < roomEnd and roomEnd > i.get_end()):
                return HttpResponse("Overlapped")


        # get room instance
        r = MeetingRoom.objects.get(roomName=roomin)

        r = Reservation(topic=topicin, start=roomStart, end=roomEnd, room=r, owner=userModel)
        r.save()

        return HttpResponse("Done")


@csrf_exempt
def deleteReserve(request):
    if request.method == "POST":
        data = json.dumps(request.POST)
        data = json.loads(data)
        print(data)
        topic = data.get("topic")
        startT = data.get("time")
        s = startT.split(" - ")
        start = s[0]
        end = s[1]

        obj = Reservation.objects.get(topic=topic, start=start, end=end)
        obj.delete()

        return HttpResponse("Complete")



@csrf_exempt
def getReserve(request):
    r = Reservation.objects.all()

    allReserve = dict()

    # add Task in to dict
    i = 1
    for item in r:
        single = dict()
        single["topic"] = item.get_topic()
        single["time"] = item.get_time()
        single["room"] = item.get_room()
        single["owner"] = item.get_owner()
        allReserve["reserve"+str(i)] = single
        i += 1

    return HttpResponse(json.dumps(allReserve))


@csrf_exempt
def getProfile(request):
    # get user model from cookie
    sessions = Session.objects.get(session_key=request.COOKIES["sessionid"])
    user = User.objects.get(id__in=sessions.get_decoded()["_auth_user_id"])
    # create profile dict
    profile = dict()
    profile["fullName"] = user.get_full_name()
    profile["email"] = user.email

    # get userModel
    userModel = UserModel.objects.get(user=user)
    profile["department"] = userModel.get_department()
    profile["position"] = userModel.get_position()
    profile["phone"] = userModel.get_phone()

    return HttpResponse(json.dumps(profile))





