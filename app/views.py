from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def home(request):
    return render(request, 'home.html')

    
def login(request):
    if request.method == 'GET':
        print("---", request.session.has_key)
        return render(request,'login.html')   

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # hashed_pwrod = make_password(password, "")
        try:
            usr = User.objects.get(username=username)
            # if hashed_pwrod == usr.password:
            #     print("pwrd success----", usr.password)
            # else:
            #     print("pwrd error----", usr.password)
            #     print("pwrd error----", hashed_pwrod)
            auth_login(request, usr)
            return redirect('home')
        except User.DoesNotExist:
            error = 'Invalid creditials ! !'
            return render(request, 'login.html', {'error':error})

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        if password == password_confirmation:
            print("user succesfully created")
            user = User.objects.create(username=username, email=email, password=password)
            auth_login(request, user)
            return redirect('home')
        else:
            pwrd_error = "password did not match"
            return render(request, 'register.html', {'pword_error': pwrd_error})

    return render(request, 'register.html')


def logout(request):
    auth_logout(request)
    return redirect('login')

def profile_view(request, id):
    return render(request, 'profile_view.html')
    