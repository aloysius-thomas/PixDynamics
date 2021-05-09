from django.contrib import admin

# Register your models here.
from todo.models import LogHistory

from todo.models import Todomodel

admin.site.register(Todomodel)
admin.site.register(LogHistory)
