from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from accounts.models import User, Person, Company
from roadMap.models import Roadmap, Interest, UserInterest, LikeRoadmap
from admin.charts import usersPerInterest, ageRangesPerInterest, roadmapCompletionPercentage #Charts
from admin.openAIManager import openAIManager
from copy import deepcopy
import numpy as np

def __analyticsCharts(companyId, companyCity):
    """
    Company analytics: Charts with valuable information about user's roadmaps.
    Charts:
    1. Number of users that have the same interest as the company in the same city.
    2. Age range of users that have the same interest as the company in the same city as follows:
        Age < 18, 18 <= Age < 25, 25 <= Age < 35, 35 <= Age < 45, 45 <= Age < 55, Age >= 55.
    3. Completion percentage of roadmaps based on company's interests and selected city.
    -- Suggested roadmaps based on company's interests.
    """
    def calculateAge(userId):
        today = date.today() #Today's date.
        person = Person.objects.get(user=userId)
        if not person.dateOfBirth:
            return None
        dob = person.dateOfBirth
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            return '18-'
        elif age < 25:
            return '18-24'
        elif age < 35:
            return '25-34'
        elif age < 45:
            return '35-44'
        elif age < 55:
            return '45-54'
        else:
            return '55+'

    def collectData(companyInterests, relatedUsers):
        chartOneData = {} #Dict with the number of users that have the same interest as the company.
        chartTwoData = {} #Dict with the number of users per age range that have the same interest as the company.
        ranges = {
            '18-': 0,
            '18-24': 0,
            '25-34': 0,
            '35-44': 0,
            '45-54': 0,
            '55+': 0
        }
        for user in relatedUsers:
            userInterests = set(UserInterest.objects.select_related('interest').filter(user=user.id).values_list('interest__name', flat=True))
            commonInterests = companyInterests.intersection(userInterests)
            age = calculateAge(user.id)
            if not age:
                continue
            for interest in commonInterests:
                #Chart 1:
                if interest in chartOneData:
                    chartOneData[interest] += 1
                else:
                    chartOneData[interest] = 1

                #Chart 2:
                if interest in chartTwoData:
                    chartTwoData[interest][age] += 1
                else:
                    chartTwoData[interest] = deepcopy(ranges)
                    chartTwoData[interest][age] += 1


        return chartOneData, chartTwoData

    companyInterests = set(UserInterest.objects.select_related('interest').filter(user=companyId).values_list('interest__name', flat=True))
    relatedUsers = User.objects.filter(city=companyCity).exclude(isCompany=True)

    chartOneData, chartTwoData = collectData(companyInterests, relatedUsers)
    colors = dict(Interest.objects.all().values_list('name', 'color'))

    return usersPerInterest(chartOneData, colors), ageRangesPerInterest(chartTwoData, colors)     

def __roadmapsStatistics(userId, city):
    
    def completionPercentageChart():
        colors = dict(Interest.objects.all().values_list('name', 'color'))
        return roadmapCompletionPercentage(roadmapCompletion, colors)
    
    userInterests = UserInterest.objects.filter(user=userId)
    roadmapCompletion = {}
    completionPercentage = {}
    suggestedRoadmaps = []
    for userInterest in userInterests:
        roadmaps = Roadmap.objects.filter(interest=userInterest.interest_id, user__user__city=city).order_by('-completionPercentage')
        if not roadmaps:
            roadmapCompletion[userInterest.interest.name] = []
            completionPercentage[userInterest.interest] = 0
            continue
        percentages = [roadmap.completionPercentage for roadmap in roadmaps]
        roadmapCompletion[userInterest.interest.name] = percentages
        completionPercentage[userInterest.interest] = (sum(percentages) / len(percentages)) if percentages else 0
        suggestedRoadmaps.extend(list(roadmaps)[0:6 if len(roadmaps) > 6 else len(roadmaps)])
    return completionPercentage, suggestedRoadmaps, completionPercentageChart()

def __suggestedRoadmaps(userId):
    #Suggested roadmaps based on person's interests.
    userInterests = UserInterest.objects.filter(user=userId)
    suggestedRoadmaps = []
    for userInterest in userInterests:
        roadmaps = list(Roadmap.objects.select_related('user').filter(interest=userInterest.interest_id).exclude(user=userId))
        if roadmaps:
            suggestedRoadmaps.extend(roadmaps)
    return suggestedRoadmaps

def __filteredRoadmaps(objective, interest, userId):
    def findSimilarObjectives(objective, interest=None):
        if interest:
            roadmaps = list(Roadmap.objects.filter(interest=interest).exclude(user=userId))
        else:
            roadmaps = list(Roadmap.objects.all().exclude(user=userId))
        
        if not roadmaps:
            return None

        openAI = openAIManager()
        embeddedObjective = openAI.embedObjective(objective)
        cosineSimilarity = lambda a, b: np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        #Find nearest roadmap objectives.
        distances = [cosineSimilarity(embeddedObjective, list(np.frombuffer(roadmap.embedding))) for roadmap in roadmaps]
        sortedDistanceIndex = np.argsort(distances)[::-1]

        #Save and return the best matches only:
        filteredRoadmaps = []
        i = 0
        if distances[sortedDistanceIndex[i]] == 1.0: #if exists an exact match.
            #Take only the exact matches.
            while distances[sortedDistanceIndex[i]] == 1.0 and i < len(sortedDistanceIndex):
                filteredRoadmaps.append(roadmaps[sortedDistanceIndex[i]])
                i += 1
        elif distances[sortedDistanceIndex[i]] > 0.0: #if exists a good match.
            #Take the 9 best matches.
            while i < 9 and i < len(sortedDistanceIndex) and distances[sortedDistanceIndex[i]] > 0.0:
                filteredRoadmaps.append(roadmaps[sortedDistanceIndex[i]])
                i += 1
        else:
            #No good matches found (distance <= 0.0 are not related.) 
            return None
        
        return filteredRoadmaps



    filteredRoadmaps = []
    searchTerm = ""
    if not objective:
        #Only interest was provided.
        filteredRoadmaps = list(Roadmap.objects.filter(interest=int(interest)).exclude(user=userId))
        searchTerm = Interest.objects.get(id=interest).name
    elif not interest:
        #Only objective was provided.
        filteredRoadmaps = findSimilarObjectives(objective)
        searchTerm = objective
    else:
        #Both objective and interest were provided.
        filteredRoadmaps = findSimilarObjectives(objective, interest)
        searchTerm = Interest.objects.get(id=interest).name + " with " + objective
    return (searchTerm, filteredRoadmaps)

@login_required
def analytics(request): #Only for companies.
    user = User.objects.get(username=request.user) #Username is unique as well.
    if not user.isCompany:
        return redirect('home')
    
    if request.method == 'POST':
        pass
    else:
        company = Company.objects.get(user=user.id)
        chartOne, chartTwo = __analyticsCharts(user.id, user.city)
        roadmapCompletion, suggestedRoadmaps, chartThree = __roadmapsStatistics(user.id, user.city)
        context = {
            'userInterests': chartOne,
            'userAgeInterest': chartTwo,
            'completionPercentage': chartThree,
            'suggestedRoadmaps': suggestedRoadmaps,
            'roadmapCompletion': roadmapCompletion,
            'name': company.companyName,
            'city': user.city
        }
        return render(request, 'analytics.html', context=context)
        
@login_required
def explore(request):
    user = User.objects.get(username=request.user) #Username is unique as well.
    interests = dict(Interest.objects.all().values_list('id', 'name'))
    if request.method == 'POST':
        objective = request.POST.get('objective')
        interest = request.POST.get('interest')
        searchTerm, filteredRoadmaps = __filteredRoadmaps(objective, interest, user.id)
        likedRoadmaps = list(LikeRoadmap.objects.filter(user=user.id, roadmap__in=filteredRoadmaps))
        likedRoadmaps = [roadmap.roadmap for roadmap in likedRoadmaps]
        context = {
            'searchTerm': searchTerm,
            'filteredRoadmaps': filteredRoadmaps,
            'interests': interests,
            'filtered': True,
            'likedRoadmaps': likedRoadmaps
        }
        return render(request, 'explore.html', context=context)
    else:
        suggestedRoadmaps = __suggestedRoadmaps(user.id)
        likedRoadmaps = list(LikeRoadmap.objects.filter(user=user.id, roadmap__in=suggestedRoadmaps))
        likedRoadmaps = [roadmap.roadmap for roadmap in likedRoadmaps]
        context = {
            'suggestedRoadmaps': suggestedRoadmaps,
            'interests': interests,
            'filtered': False,
            'likedRoadmaps': likedRoadmaps
        }
        return render(request, 'explore.html', context=context)