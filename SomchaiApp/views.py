from django.shortcuts import render
from django.contrib.auth import authenticate, login, models
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
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
            if user.is_active:
                # log user in
                login(request, user)
                data = {'first_name': user.first_name, 'last_name': user.last_name}
                return HttpResponse(json.dumps(data))
            else:
                # can't login due to constraint
                return HttpResponse("error 1")

        else:
            # user not existed
            return HttpResponse("error 2")

def todo(request):
    pass


def logout(request):
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



