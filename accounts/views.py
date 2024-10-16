from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from roadMap.models import Interest, UserInterest, Roadmap, LikeRoadmap

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
            print(form)
            context = {
                'form': form,
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'dateOfBirth': request.POST.get('dateOfBirth'),
                'companyName': request.POST.get('companyName'),
                'isCompany': request.POST.get('isCompany')
            }
            return render(request, 'register.html', context=context)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'isCompany': False})

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

@login_required
def profile(request):
    user = User.objects.get(username=request.user)
    if user.isCompany:
        company = Company.objects.get(user=user)
        context = {
            'name': company.companyName,
            'username': user.username,
            'city' : user.city,
            'isCompany': True
        }
    else:
        person = Person.objects.get(user=user)
        roadmaps = list(Roadmap.objects.filter(user=person))
        likedRoadmaps = list(LikeRoadmap.objects.filter(user=person))
        likedRoadmaps = [roadmap.roadmap for roadmap in likedRoadmaps]
        context = {
            'name': user.first_name + ' ' + user.last_name,
            'username': user.username,
            'roadmaps': roadmaps,
            'likedRoadmaps': likedRoadmaps,
            'city': user.city,
            'isCompany': False
        }
    return render(request, 'userProfile.html', context=context)
