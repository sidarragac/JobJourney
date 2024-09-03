from django.shortcuts import render, redirect
from admin.openAIManager import openAIManager
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import json

def __updateCheckpointStatus(checkpoint, roadmap):
    chkpt = Checkpoint.objects.get(numberOfCheckpoint=checkpoint, idRoadmap=roadmap)
    chkpt.completed = not chkpt.completed #Negate the value. If completed and unmarked => completed = False and vice versa.
    chkpt.save()

def __getCheckpointsStatus(roadmapId):
    query = Checkpoint.objects.filter(idRoadmap=roadmapId).values('numberOfCheckpoint', 'completed')
    checkpoints = {}
    for checkpoint in query:
        checkpoints[checkpoint['numberOfCheckpoint']] = checkpoint['completed']

    return checkpoints

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
    
def displayRoadmap(request, roadmapId, stepNumber=0):
    roadmap = Roadmap.objects.get(id=roadmapId).content
    checkpoints = __getCheckpointsStatus(roadmapId)
    print(roadmap)
    print(checkpoints)
    context = {
        'roadmap': roadmap, 
        'roadmapId': roadmapId, 
        stepNumber: stepNumber,
        'checkpoints': json.dumps(checkpoints)
    }
    return render(request, 'roadmap.html', context)



@login_required
def checkpointUpdate(request):
    if request.method == 'POST':
        roadmapId = int(request.POST.get('roadmapId'))
        checkpoint = int(request.POST.get('checkpoint'))
        stepNumber = int(request.POST.get('stepNumber'))
        __updateCheckpointStatus(checkpoint, roadmapId)
        return redirect(f'displayRoadmap/{roadmapId}/{stepNumber}')