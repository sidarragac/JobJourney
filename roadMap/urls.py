from django.urls import path
from . import views

urlpatterns = [
    path('', views.interestForm, name='interestForm'),
    path('roadmapGenerator', views.roadmapGenerator, name='roadmapGenerator'),
    path('checkpointUpdate', views.checkpointUpdate, name='checkpointUpdate'),
]
