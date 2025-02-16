from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

def registerPage(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'register.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Incorrect username or password.") # Add error to the form
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')