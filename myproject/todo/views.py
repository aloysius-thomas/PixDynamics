from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from todo.forms import TodoRegistrationForm, NewUserForm
from todo.models import Todomodel, LogHistory
from django.contrib.auth.forms import AuthenticationForm
import requests

mobile_regex = RegexValidator(regex=r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[6789]\d{9}|(\d[ -]?){10}\d$')


# Create your views here.

def convert_to_string(err):
    err = err
    msg = ""
    for key, val in err.items():
        msg += "'" + key + "' " + val[0] + ","
        break

    return msg


@login_required
def todo_registration(request):
    if request.method == "POST":

        form = TodoRegistrationForm(request.POST)
        if not form.is_valid:
            messages.info(request, convert_to_string(form.errors))
        form.save()

    form = TodoRegistrationForm
    query = Todomodel.objects.all().order_by('-id')
    return render(request=request,
                  template_name="todo.html",
                  context={"form": form, 'query': query})


@login_required
def todo_delete(request, id):
    todo = get_object_or_404(Todomodel, id=id)

    todo.delete()

    return redirect("/todo/")


def login_view(request):
    if request.method == 'POST':

        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/todo/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="login.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/accounts/login/")


@receiver(post_save, sender=Todomodel)
def logTodCreate(sender, instance, **kwargs):
    LogHistory(action='Creation', todo=instance.id).save()


@receiver(pre_delete, sender=Todomodel, dispatch_uid='todo_delete_signal')
def logTodoDelete(sender, instance, using, **kwargs):
    print('instance', instance)
    print('instance', sender)
    LogHistory(action='Deletion', todo=instance.id).save()


def register(request):
    if request.method == "POST":

        form = NewUserForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            login(request, user)
            last = {
                "email": email,
                "username": username,
                "password": password1
            }
            r = requests.get('http://127.0.0.1:8000/auth/users/', data=last)
            print("respone === >", r)
            return redirect("/auth/users/")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request=request,
                          template_name="register.html",
                          context={"form": form})
    form = NewUserForm

    return render(request=request,
                  template_name="register.html",
                  context={"form": form})
