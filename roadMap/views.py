from django.shortcuts import render
from admin.openAIManager import openAIManager
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import asyncio
import json

def interestForm(request):
    return render(request, 'interestForm.html')

def roadmapGenerator(request):
    if request.method == 'POST':
        form = RoadmapCharacteristics(request.POST)
        if form.is_valid():
            # interest = form.cleaned_data['interest']
            # objective = form.cleaned_data['objective']
            # salary = form.cleaned_data['salary']
            # bot = openAIManager()
            # roadmap = bot.generateRoadmap(objective=objective, salary=salary) #JSON with detailed roadmap.

            # instanciar un obj del modelo roadmap

            f = open("./roadMap/roadmap.json")
            roadmap = json.loads(f.read())

            return render(request, 'roadmap.html', {'roadmap': roadmap, 'roadmapID': 1})
        else:
            return render(request, 'interestForm.html', {"message": "Some provided data are not valid."})
    else:
        return render(request, 'interestForm.html')
    
async def __updateCheckpointStatus(checkpoint, roadmap, status):
    Checkpoint.objects.filter(numberOfCheckpoint=checkpoint, idRoadmap=roadmap).update(completed=status)

@login_required
def checkpointUpdate(request):

    return render(request, 'completedCheckpoint.html')