from django.shortcuts import render, redirect, HttpResponse
from admin.openAIManager import openAIManager
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from accounts.models import User, Person
import json
import numpy as np

def __updateCheckpointStatus(checkpoint, roadmap):
    chkpt = Checkpoint.objects.get(numberOfCheckpoint=checkpoint, roadmap=roadmap)
    chkpt.completed = not chkpt.completed #Negate the value. If completed and unmarked => completed = False and vice versa.
    chkpt.save()

def __getCheckpointsStatus(roadmapId):
    query = Checkpoint.objects.filter(roadmap=roadmapId).values('numberOfCheckpoint', 'completed')
    checkpoints = {}
    for checkpoint in query:
        checkpoints[checkpoint['numberOfCheckpoint']] = checkpoint['completed']

    return checkpoints

@login_required
def interestForm(request):
    user = User.objects.get(username=request.user)
    if user.isCompany:
        return render(request, 'accessDenied.html')
    else:
        return render(request, 'interestForm.html', {'interests': Interest.objects.all()})

@login_required
def roadmapGenerator(request):
    if request.method == 'POST':
        form = RoadmapCharacteristics(request.POST)
        if form.is_valid():
            interest = form.cleaned_data['interest']
            interest = Interest.objects.get(id=interest).name
            objective = form.cleaned_data['objective']
            salary = form.cleaned_data['salary']
            openAI = openAIManager()
            roadmap = openAI.generateRoadmap(objective=objective, salary=salary) #JSON with detailed roadmap.
            embedding = np.array(openAI.embedObjective(objective)).tobytes()
            user = User.objects.get(username=request.user)
            person = Person.objects.get(user=user.id)
            roadmapInstance = createDBRoadmap(roadmap, interest, person, objective, embedding)
            createDBCheckpoints(roadmap, roadmapInstance)
            return redirect(f'displayRoadmap/{roadmapInstance.id}')
        else:
            return render(request, 'interestForm.html', {'interests': Interest.objects.all(), "error": "Please select an interest and write an objective"})
    else:
        return render(request, 'interestForm.html', {'interests': Interest.objects.all()})

def percentageCompletion(roadmapId):
    checkpoints = Checkpoint.objects.filter(roadmap=roadmapId, completed=True)
    completedCheckpoints = len(checkpoints)
    percentage = int((completedCheckpoints/15)*100)
    Roadmap.objects.filter(id=roadmapId).update(completionPercentage=percentage)
    return percentage

@login_required   
def displayRoadmap(request, roadmapId, stepNumber=0):
    roadmap = Roadmap.objects.get(id=roadmapId)
    completionPercentage = percentageCompletion(roadmapId)
    user = User.objects.get(username=request.user)
    editable = True
    if user.id != roadmap.user.user_id:
        editable = False
    checkpoints = __getCheckpointsStatus(roadmapId)
    context = {
        'completionPercentage': completionPercentage,
        'roadmap': roadmap.content, 
        'roadmapId': roadmapId,
        'stepNumber': stepNumber, 
        'checkpoints': json.dumps(checkpoints),
        'editable': editable
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
    
def createDBRoadmap(roadmapJSON, interest, person, objective, embedding):
    mainGoal = objective
    content = roadmapJSON
    completionPercentage = 0
    interest = Interest.objects.get(name=interest)
    numberOfLikes = 0
    roadmap = Roadmap(mainGoal=mainGoal, content=content, completionPercentage=completionPercentage, interest=interest , numberOfLikes=numberOfLikes, user=person, embedding=embedding)
    roadmap.save()
    return roadmap

def createDBCheckpoints(roadmapJSON, roadmap):
    steps = roadmapJSON['steps']
    counter = 1
    for step in steps:
        checkpoints = step['remarkablePoints']
        for _ in checkpoints:
            checkpoint = Checkpoint(numberOfCheckpoint=counter, roadmap=roadmap, completed=False)
            checkpoint.save()
            counter += 1

def home(request):
    return render(request, 'home.html')