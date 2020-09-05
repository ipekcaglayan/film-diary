from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def login_view(request):
    form = AuthenticationForm(data=request.POST)
    signup_form = UserCreationForm()
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form, 'signup_form': signup_form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect("home")
