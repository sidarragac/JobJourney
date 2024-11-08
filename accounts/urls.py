from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('logout/', views.logoutAccount, name='logout'),
    path('interestSelection/', views.interestSelection, name='interestSelection'),
    path('interestSelection/edit', views.editInterests, name='editInterests'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.editProfile, name='editProfile'),
    path('oauth/', views.googleLogin, name='oauth'),
    path('oauth/complete/', views.completeRegistration, name='completeRegistration'),
    path('oauth/callback/', views.callback, name='callback'),
]