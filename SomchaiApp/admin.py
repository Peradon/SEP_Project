from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.UserModel)
admin.site.register(models.TodoList)
admin.site.register(models.Reservation)
admin.site.register(models.MeetingRoom)