from django.shortcuts import render, redirect
from .forms import NewUserForm
# Create your views here.
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this


def register_request(request):
    if request.method == "POST":
        # print(request.POST)
        form = NewUserForm(request.POST)
        if form.is_valid():
            print("in if condition")
            user = form.save()
            # login(request, user)  # skip
            return redirect("register")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') # admin
            password = form.cleaned_data.get('password') # admin
            user = authenticate(username=username, password=password) # returns user object
            print(user, user.__dict__)
            if user:
                login(request, user) # database save
                return redirect("home_page")
            else:
                return redirect("login_user")
        else:
            return redirect("login_user")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})

def logout_request(request):
    logout(request)
    return redirect("login_user")

