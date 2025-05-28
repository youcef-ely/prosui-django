import pretty_errors
from . import forms
from .models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm
from django.contrib.auth import get_user_model





def login_page(request):
    """
    User login view. Authenticates the user and redirects to the appropriate page.
    If it's the first login, redirects to complete the profile.
    """
    form = forms.LoginForm()
    message = ''
    User = get_user_model()

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                message = "No user found with this email address."
            else:
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    if user.first_login:
                        return redirect('complete_profile')
                    return redirect('home')
                else:
                    message = "Incorrect password."

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
    if request.method == "POST":
        form = forms.CompleteProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            request.user.first_login = False
            request.user.save(update_fields=['first_login'])
            return redirect('home')
    else:
        form = forms.CompleteProfileForm(instance=request.user)  

    return render(request, "users/complete_profile.html", {"form": form})




@login_required
def my_profile(request):
    return render(request, 'users/my_profile.html')



@login_required
def my_team(request):
    """
    View to display the user's team.
    """
    user = request.user
    if user.role == 'supervisor':
        # Fetch the team members for the supervisor
        team_members = CustomUser.objects.filter(supervisor=user)
        
    else:
        # If not a supervisor, redirect or show an error
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')

    return render(request, 'users/my_team.html', {'team_members': team_members})


@login_required
def update_profile(request):
    """
    View to update the user's profile.
    """
    if request.method == 'POST':
        form = forms.UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Profile updated successfully.")
            return redirect('my_profile')
    else:
        form = forms.UpdateProfileForm(instance=request.user)

    return render(request, 'users/update_profile.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('password_change_done')


@login_required
def member_details(request, pk):
    member = CustomUser.objects.get(pk=pk)
    return render(request, 'users/member_details.html', {'member': member})