from django.shortcuts import render
from admin.openAIManager import openAIManager

def interestForm(request):
    return render(request, 'interestForm.html')

def roadmapGenerator(request):
    if request.method == 'POST':
        interest = request.POST.get('interest')
        objective = request.POST.get('objective')
        salary = request.POST.get('salary')
        bot = openAIManager()
        roadmap = bot.generateRoadmap(objective=objective, salary=salary) #JSON with detailed roadmap.
        return render(request, 'roadmap.html', {'roadmap': roadmap})
    else:
        return render(request, 'interestForm.html')