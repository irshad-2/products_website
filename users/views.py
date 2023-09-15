from django.http.response import HttpResponseRedirect
from django.shortcuts import render, reverse,redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages



# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)

                return HttpResponseRedirect("/")

        context = {
            "title": "Login",
            "error": True,
            "message": "Invalid username or password"
        }
        return render(request, "users/login.html", context)
    else:
        context = {
            "title": "Login",

        }
        return render(request, "users/login.html", context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("web:index"))

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST["repassword"]
        if password == repassword:
            User.objects.create_user(username=username, password=password, is_staff=False, email=email)
            messages.success(request, "Account created successfully")
            return redirect('users:login')
        else:
            context = {"message": "passwords do not match"}
            return render(request, "users/signup.html", context)

    return render(request, "users/signup.html")