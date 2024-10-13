from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics, name='analytics'),
    path('explore', views.explore, name='explore'),
    path('<int:roadmapID>/like', views.likeRoadmap, name='like'),
]
