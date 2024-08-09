from django.shortcuts import render
from admin.openAIManager import openAIManager

def home(request):
    return render(request, 'index.html')

def roadmapGenerator(request):
    bot = openAIManager()
    bot.generateRoadmap("software engineeer", "software engineer at google", 100000)
    # if request.method == 'POST':
    #     return render(request, 'roadmapGenerator.html')
    return render(request, 'index.html')