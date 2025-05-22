from asyncio import exceptions as instance

from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html', {})

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'Contact us.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are now logged in."))
            return redirect('home')
        else:
            messages.success(request, ("An error occurred, please try again."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out."))
    return redirect('home')

def register(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully, please fill out the rest of the information.')
            return redirect('update_info')
        else:
            messages.success(request, 'Oops, something went wrong please try again.')
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_users = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_users)

        if user_form.is_valid():
            user_form.save()

            login(request, current_users)
            messages.success(request, 'User has been updated.')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, 'You are not logged in.')
        return redirect('login')

def update_password(request):
    if request.user.is_authenticated:
        current_users = request.user
        # did they fill the form
        if request.method == "POST":
            form = ChangePasswordForm(current_users, request.POST)
            # is form valid
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password was successfully updated! Please log in again.')
                # login(request, current_users)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_users)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, 'You are not logged in.')
        return redirect('home')
    return render(request, 'update_password.html', {})

def update_info(request):
    if request.user.is_authenticated:
        current_users = UserProfile.objects.get(user__id = request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_users)

        if form.is_valid():
            form.save()

            messages.success(request, "Your info has been updated!!!!")
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.success(request, "You are not logged in.")
        return redirect('home')
