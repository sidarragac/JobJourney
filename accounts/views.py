from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import *
from .models import *
from roadMap.models import Interest, UserInterest, Roadmap, LikeRoadmap
from urllib.parse import urlencode
import requests

def __infoUser__(user):
    instagram = UserSocialMedia.objects.get(socialMedia__name="Instagram",user=user) if UserSocialMedia.objects.filter(socialMedia__name="Instagram",user=user).exists() else None
    facebook = UserSocialMedia.objects.get(socialMedia__name="Facebook",user=user) if UserSocialMedia.objects.filter(socialMedia__name="Facebook",user=user).exists() else None
    linkedin = UserSocialMedia.objects.get(socialMedia__name="LinkedIn",user=user) if UserSocialMedia.objects.filter(socialMedia__name="LinkedIn",user=user).exists() else None
    if user.isCompany:
        company = Company.objects.get(user=user)
        context = {
            'name': company.companyName,
            'username': user.username,
            'city' : user.city,
            'isCompany': True,
            'instagram': instagram.link if instagram else None,
            'facebook': facebook.link if facebook else None,
            'linkedin': linkedin.link if linkedin else None,
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
            'isCompany': False,
            'instagram': instagram.link if instagram else None,
            'facebook': facebook.link if facebook else None,
            'linkedin': linkedin.link if linkedin else None,
        }
    return context

def __getAuthorizationToken__(code):
    tokenURL = 'https://oauth2.googleapis.com/token'

    data = {
        'code': code,
        'client_id': settings.KEYS['GOOGLE_CLIENT_ID'],
        'client_secret': settings.KEYS['GOOGLE_CLIENT_SECRET'],
        'redirect_uri': settings.KEYS['GOOGLE_REDIRECT_URI'],
        'grant_type': 'authorization_code',
    }

    response = requests.post(tokenURL, data=data)
    token = response.json()
    return token['access_token']
    
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
            context = {
                'form': form,
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'dateOfBirth': request.POST.get('dateOfBirth'),
                'companyName': request.POST.get('companyName'),
                'isCompany': request.POST.get('isCompany'),
            }
            return render(request, 'register.html', context=context)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'isCompany': False})

@login_required
def interestSelection(request):
    if request.method == 'GET':
        return render(request, 'interestSelection.html', {'interests': Interest.objects.all()})
    
    interests = []
    user = request.user
    for i in range(3):
        interest = request.POST.get(f'interest{i+1}')
        if interest:
            interests.append(interest)

    for interest in interests:
        if UserInterest.objects.filter(user=user, interest=interest).exists():
            continue
        UserInterest.objects.create(user=user, interest=Interest.objects.get(id=interest))
    
    if UserInterest.objects.filter(user=user).count() != len(interests):
        UserInterest.objects.filter(user=user).exclude(interest__in=interests).delete()

    return redirect('profile')

@login_required
def editInterests(request):
    userInterests = list(UserInterest.objects.filter(user=request.user).values_list('interest', flat=True))
    interests = Interest.objects.all()

    while len(userInterests) < 3:
        userInterests.append(None)

    return render(request, 'editInterestSelection.html', {'interests': interests, 'userInterests': userInterests})

@login_required
def profile(request):
    user = User.objects.get(username=request.user)
    context = __infoUser__(user)
    return render(request, 'userProfile.html', context=context)

@login_required
def editProfile(request):
    user = User.objects.get(username=request.user)
    context = __infoUser__(user)
    if request.method == 'POST':
        # Actualizar la imagen de perfil
        uploaded_image = request.FILES.get('inputFile')
        if uploaded_image:
            if user.image.url != 'images/default-avatar.jpg':
                user.image.delete()
            user.image = uploaded_image  # Asigna la imagen nueva

        # Actualizar o crear el enlace de Instagram
        UserSocialMedia.objects.update_or_create(
            user=user,
            socialMedia=SocialMedia.objects.get(name='Instagram'),
            defaults={'link': request.POST.get('Instagram', '')}
        )
        
        # Actualizar o crear el enlace de Facebook
        UserSocialMedia.objects.update_or_create(
            user=user,
            socialMedia=SocialMedia.objects.get(name='Facebook'),
            defaults={'link': request.POST.get('Facebook', '')}
        )
        
        # Actualizar o crear el enlace de LinkedIn
        UserSocialMedia.objects.update_or_create(
            user=user,
            socialMedia=SocialMedia.objects.get(name='LinkedIn'),
            defaults={'link': request.POST.get('LinkedIn', '')}
        )
        user.save()
        context = __infoUser__(user)
        return redirect('profile')

    return render(request, 'userProfile.html', context=context)

def googleLogin(request):
    params = {
        'client_id': settings.KEYS['GOOGLE_CLIENT_ID'],
        'redirect_uri': settings.KEYS['GOOGLE_REDIRECT_URI'],
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
    }
    url = f'https://accounts.google.com/o/oauth2/auth?{urlencode(params)}'
    return redirect(url)

def callback(request):
    try:
        code = request.GET.get('code')
        token = __getAuthorizationToken__(code)
    except:
        return redirect('register')
    
    userInfoURL = 'https://www.googleapis.com/oauth2/v3/userinfo'
    headers = {'Authorization': f"Bearer {token}"}
    userInfo = requests.get(userInfoURL, headers=headers).json()
    email = userInfo['email']
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        login(request, user)
        return redirect('home')
    else:
        context = {
            'email': email,
            'name': userInfo['name'],
            'firstName': userInfo['given_name'],
            'lastName': userInfo['family_name'],
            'image': userInfo['picture'],
        }
        return render(request, 'completeRegistration.html', context=context)
    
def completeRegistration(request):
    if request.method == 'GET':
        return redirect('register')

    form = GoogleRegisterForm(request.POST)
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
        context = {
            'form': form,
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'dateOfBirth': request.POST.get('dateOfBirth'),
            'companyName': request.POST.get('companyName'),
            'isCompany': request.POST.get('isCompany'),
        }
        return render(request, 'register.html', context=context)