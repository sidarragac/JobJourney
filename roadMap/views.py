from django.shortcuts import render
from admin.openAIManager import openAIManager
from forms import *
import json

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
            return render(request, 'roadmap.html', {'roadmap': roadmap})
            # f = open("./roadMap/roadmap.json")
            # roadmap = json.loads(f.read())
            # return render(request, 'roadmap.html', {'roadmap': roadmap})
        else:
            return render(request, 'interestForm.html', {"message": "Some provided data are not valid."})
    else:
        return render(request, 'interestForm.html')