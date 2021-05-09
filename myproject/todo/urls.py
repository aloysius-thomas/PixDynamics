from django.urls import path

from todo.views import todo_registration
from todo.views import todo_delete
from todo.views import login_view
from todo.views import logout_request
from todo.views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('todo/', todo_registration, name='todo_registration'),
    path('todo_delete/<int:id>/', todo_delete, name='todo_delete'),
    path('accounts/login/', login_view, name='login_view'),
    path('logout/', logout_request, name='login_view'),
]
