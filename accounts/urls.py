from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('logout/', views.logoutAccount, name='logout'),
    path('interestSelection/', views.interestSelectionView, name='interestSelection'),
    path('profile/', views.profile, name='profile'),
]