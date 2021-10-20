from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *

def home(request):
    try:
        user = User.objects.filter(is_staff=False)
        follow = Follow.objects.filter(given_user=request.user, status="requested")
        # follow = Follow.objects.filter(given_user=request.user, status="requested")
        follow_count = Follow.objects.filter(given_user=request.user, status="accepted").count()

        context = {
            'users': user,
            'followers': follow,
            'follow_count': follow_count,
        }
    except:
        context = {
            'users': user,
            'follow_count': 0,
        }
    return render(request, 'home.html', context)

    
def login(request):
    if request.method == 'GET':
        print("---", request.session.has_key)
        return render(request,'login.html')   

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST['password']
        
        try:
            usr = User.objects.get(username=username)
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

        try:
            follow = Follow.objects.get(requested_user=request.user, given_user=id)
            follow_count = Follow.objects.filter(given_user=request.user, status="accepted").count()
        except Follow.DoesNotExist:
            follow = None
            follow_count = 0

        context = {
            'user': user,
            'images': images,
            'form': form,
            'follow': follow,
            'follow_count': follow_count,
        }

    if request.method == 'POST':
        
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

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
    if Follow.objects.filter(requested_user=request.user, given_user=id):
        follow = Follow.objects.get(requested_user=request.user, given_user=id)
        follow.status = "requested"
        follow.save()
    else:
        follow = Follow()
        follow.requested_user = request.user
        follow.given_user = User.objects.get(id=id)
        follow.status = "requested"
        follow.save()
    return redirect('profile_view', id)

def unfollow(request, id):
    if Follow.objects.filter(requested_user=request.user, given_user=id):
        follow = Follow.objects.get(requested_user=request.user, given_user=id)
        follow.status = "rejected"
        follow.save()
    return redirect('profile_view', id)

def accept_follow_request(request, id):
    follow = Follow.objects.get(requested_user=id, given_user=request.user)
    follow.status = "accepted"
    follow.save()
    return redirect('home')

def reject_follow_request(request, id):
    follow = Follow.objects.get(requested_user=id, given_user=request.user)
    follow.status = "rejected"
    follow.save()
    return redirect('home')
