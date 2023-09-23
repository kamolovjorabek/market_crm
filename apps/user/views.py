from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegisterForm
# Create your views here.


def custom_login(request):
    if request.method == 'POST':
        user = authenticate(
            phone=request.POST.get('phone'),
            password=request.POST.get('password')
        )
        if not user:
            messages.error(request, 'No such user exists!')
            return redirect('custom_login')
        login(request, user)
        role = user.role
        if role == 'director':
            return redirect("dashboard")
        if role == 'shop':
            return redirect("shop")
    return render(request, 'login.html')


def custom_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('custom_login')
    return render(request, 'register.html')
