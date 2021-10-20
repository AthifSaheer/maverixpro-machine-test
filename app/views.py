from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import *

def home(request):
    user = User.objects.all()
    follow = Follow.objects.filter(following_user=request.user, accepted=False, rejected=False)
    print("follow--", follow)
    context = {
        'users': user,
        'followers': follow,
    }
    return render(request, 'home.html', context)

    
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

@login_required(login_url='login')
def profile_view(request, id):
    if request.method == 'GET':
        user = User.objects.get(id=id)
        images = UploadImage.objects.filter(user=id)
        form = UploadImageForm()

        context = {
            'user': user,
            'images': images,
            'form': form,
        }

    if request.method == 'POST':
        
        form = UploadImageForm(request.POST, request.FILES)
        print("-------------------------form--------", form)
        if form.is_valid():
            print("-------------------------valid--------")
            form.save()
            # return redirect('profile_view', id)
            
        # image = request.POST.get('image')
        upld_img = UploadImage.objects.all().order_by('-id').first()
        upld_img.user = request.user
        upld_img.save()
        
        user = User.objects.get(id=id)
        images = UploadImage.objects.filter(user=id)
        form = UploadImageForm()

        context = {
            'user': user,
            'images': images,
            'form': form,
        }

    return render(request, 'profile_view.html', context)
    

def follow(request, id):
    follow = Follow()
    follow.which_user = request.user
    follow.following_user = User.objects.get(id=id)
    follow.save()
    return redirect('profile_view', id)

def accept_follow_request(request, id):
    follow = Follow.objects.filter(which_user=id)
    follow.accepted = True
    follow.save()
    return redirect('home')