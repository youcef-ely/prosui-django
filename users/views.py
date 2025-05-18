from . import forms
from django.shortcuts import render
from django.contrib.auth import login, authenticate # import des fonctions login et authenticate


def login_page(request):
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
                login(request, user)
                message = f'Hello, {user.username}! You are Logged In.'
            else:
                message = 'Username or password are incorrect.'
    return render(
        request, 'users/login.html', context={'form': form, 'message': message})