from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
from roadMap.models import Interest, UserInterest

# Create your views here.
def loginView(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def logoutAccount(request):
    logout(request)
    return redirect('home')

def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.isCompany:
                companyName = request.POST.get('companyName')
                Company.objects.create(user=user, companyName=companyName)
            else:
                dateOfBirth = request.POST.get('dateOfBirth')
                Person.objects.create(user=user, dateOfBirth=dateOfBirth)
            login(request, user)
            return redirect('interestSelection')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def interestSelectionView(request):
    if request.method == 'POST':
        interests = []
        for i in range(3):
            interest = request.POST.get(f'interest{i+1}')
            if interest:
                interests.append(interest)
        user = request.user
        for interest in interests:
            if not UserInterest.objects.filter(user=user, interest=Interest.objects.get(id=interest)).exists():
                UserInterest.objects.create(user=user, interest=Interest.objects.get(id=interest))
        return redirect('home')
    return render(request, 'interestSelection.html', {'interests': Interest.objects.all()})