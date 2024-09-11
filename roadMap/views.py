from django.shortcuts import render, redirect
from admin.openAIManager import openAIManager
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from accounts.models import User, Person
import json

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

def __getInterest(interest):
    relations = {
        "natural_sciences": "Natural Sciences",
        "mathematics_statistics": "Mathematics and Statistics",
        "engineering_technology": "Engineering and Technology",
        "medical_health_sciences": "Medical and Health Sciences",
        "social_sciences": "Social Sciences",
        "humanities": "Humanities",
        "arts_design": "Arts and Design",
        "business_management": "Business and Management",
        "law_legal_studies": "Law and Legal Studies",
        "education": "Education",
        "computer_science_information_systems": "Computer Science and Information Systems",
        "environmental_agricultural_sciences": "Environmental and Agricultural Sciences",
        "communication_media": "Communication and Media",
        "interdisciplinary_studies": "Interdisciplinary Studies"
    }
    return relations[interest]

@login_required
def interestForm(request):
    return render(request, 'interestForm.html')

def roadmapGenerator(request):
    if request.method == 'POST':
        form = RoadmapCharacteristics(request.POST)
        if form.is_valid():
            interest = form.cleaned_data['interest']
            objective = form.cleaned_data['objective']
            salary = form.cleaned_data['salary']
            bot = openAIManager()
            roadmap = bot.generateRoadmap(objective=objective, salary=salary) #JSON with detailed roadmap.
            user = User.objects.get(username=request.user)
            person = Person.objects.get(user=user.id)
            roadmapInstance = createDBRoadmap(roadmap, interest, person, objective)
            createDBCheckpoints(roadmap, roadmapInstance)


            return redirect(f'displayRoadmap/{roadmapInstance.id}')
        else:
            return render(request, 'interestForm.html', {"message": "Some provided data are not valid."})
    else:
        return render(request, 'interestForm.html')
    
def displayRoadmap(request, roadmapId, stepNumber=0):
    roadmap = Roadmap.objects.get(id=roadmapId).content
    checkpoints = __getCheckpointsStatus(roadmapId)
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
    
def createDBRoadmap(roadmapJSON, interest, person, objective):
    mainGoal = objective
    content = roadmapJSON
    completionPercentage = 0
    interest = __getInterest(interest)
    interest = Interest.objects.get(name=interest)
    numberOfLikes = 0
    roadmap = Roadmap(mainGoal=mainGoal, content=content, completionPercentage=completionPercentage, interest=interest , numberOfLikes=numberOfLikes, user=person)
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
    return render(request, 'base.html')