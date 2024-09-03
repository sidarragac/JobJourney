from django.shortcuts import render, redirect
from admin.openAIManager import openAIManager
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
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

            return redirect(f'displayRoadmap/{1}')
        else:
            return render(request, 'interestForm.html', {"message": "Some provided data are not valid."})
    else:
        return render(request, 'interestForm.html')
    
def displayRoadmap(request, roadmapId):
    roadmapObj = Roadmap.objects.get(id=roadmapId)
    roadmap = roadmapObj.content

    return render(request, 'roadmap.html', {'roadmap': roadmap, 'roadmapId': roadmapId})

def __updateCheckpointStatus(checkpoint, roadmap):
    print("Checkpoint: ", checkpoint)
    print("Roadmap: ", roadmap)
    chkpt = Checkpoint.objects.get(numberOfCheckpoint=checkpoint, idRoadmap=roadmap)
    print(chkpt)
    chkpt.completed = not chkpt.completed #Negate the value. If completed and unmarked => completed = False and vice versa.
    chkpt.save()

@login_required
def checkpointUpdate(request):
    if request.method == 'POST':
        roadmapId = request.POST.get('roadmapId')
        checkpoint = request.POST.get('checkpoint')
        __updateCheckpointStatus(checkpoint, roadmapId)
        return redirect(f'displayRoadmap/{roadmapId}')