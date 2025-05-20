import pretty_errors

from . import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout



def login_page(request):
    """
    User login view. Authenticates the user and redirects to the appropriate page.
    If it's the first login, redirects to complete the profile.
    """
    form = forms.LoginForm()
    message = ''
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)  # <- You forgot to log in the user
                if user.first_login:  # No need to compare with '== True'
                    return redirect('complete_profile')
                return redirect('home')
            else:
                message = 'Username or password are incorrect.'
    return render(request, 'users/login.html', context={'form': form, 'message': message})


@login_required
def home(request):
    """
    Home page view. Only accessible if the user is authenticated.
    """
    return render(request, 'users/home.html')


def logout_user(request):
    """
    Log out the user and redirect to the login page.
    """
    logout(request)
    return redirect('login')


@login_required
def complete_profile(request):
    """
    View to complete the user profile if it's the first login.
    """
    user = request.user
    form = forms.CompleteProfileForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            # Update user info
            form.save(commit=False)
            user.first_login = False

            # Password change logic
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password or confirm_password:
                if new_password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return render(request, 'users/complete_profile.html', {'form': form})
                if user.check_password(new_password):
                    messages.warning(request, "New password must be different from the current one.")
                    return render(request, 'users/complete_profile.html', {'form': form})
                user.set_password(new_password)
                update_session_auth_hash(request, user)

            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('home')

    return render(request, 'users/complete_profile.html', {'form': form})


@login_required
def my_profile(request):
    return render(request, 'users/my_profile.html')
