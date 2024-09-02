from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm

from .models import *

# Create your views here.
def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})