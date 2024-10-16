from django.urls import path
from . import views

urlpatterns = [
    path('', views.interestForm, name='interestForm'),
    path('roadmapGenerator', views.roadmapGenerator, name='roadmapGenerator'),
    path('checkpointUpdate', views.checkpointUpdate, name='checkpointUpdate'),
    path('displayRoadmap/<int:roadmapId>', views.displayRoadmap, name='displayRoadmap'),
    path('displayRoadmap/<int:roadmapId>/<int:stepNumber>', views.displayRoadmap, name='displayRoadmap'),
    path('displayRoadmap/<int:roadmapID>/like', views.likeRoadmap, name='like'),
]
