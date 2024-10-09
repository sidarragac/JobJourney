from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from accounts.models import User, Person, Company
from roadMap.models import Roadmap, Interest, UserInterest
from admin.charts import usersPerInterest, ageRangesPerInterest #Charts
from copy import deepcopy


def __companyAnalytics(companyId, companyCity=None):
    """
    Company analytics: Charts with valuable information about user's roadmaps.
    Charts:
    1. Number of users that have the same interest as the company in the same city.
    2. Age range of users that have the same interest as the company in the same city as follows:
        Age < 18, 18 <= Age < 25, 25 <= Age < 35, 35 <= Age < 45, 45 <= Age < 55, Age >= 55.
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
    

    if not companyCity:
        companyCity = User.objects.get(id=companyId).city

    companyInterests = set(UserInterest.objects.select_related('interest').filter(user=companyId).values_list('interest__name', flat=True))
    relatedUsers = User.objects.filter(city=companyCity).exclude(isCompany=True)

    chartOneData, chartTwoData = collectData(companyInterests, relatedUsers)
    colors = dict(Interest.objects.all().values_list('name', 'color', flat=True))

    return usersPerInterest(chartOneData, colors), ageRangesPerInterest(chartTwoData, colors)
    
        

def __suggestedRoadmaps(userId):
    #Suggested roadmaps based on person's interests.
    userInterests = UserInterest.objects.filter(user=userId)
    suggestedRoadmaps = {}
    for userInterest in userInterests:
        roadmaps = list(Roadmap.objects.select_related('user').filter(interest=userInterest.interest_id).exclude(user=userId))
        interest = Interest.objects.get(id=userInterest.interest_id).name
        if roadmaps:
            suggestedRoadmaps[interest] = roadmaps
        else:
            suggestedRoadmaps[interest] = None

    return suggestedRoadmaps

@login_required
def analytics(request):
    user = User.objects.get(username=request.user) #Username is unique as well.
    if user.isCompany:
        company = Company.objects.get(user=user.id)
        chartOne, chartTwo = __companyAnalytics(user.id)
        suggestedRoadmaps = __suggestedRoadmaps(user.id)
        context = {
            'chartOne': chartOne,
            'chartTwo': chartTwo,
            'suggestedRoadmaps': suggestedRoadmaps,
            'name': company.companyName,
            'city': user.city
        }
        return render(request, 'companyAnalytics.html', context=context)
    else:
        suggestedRoadmaps = __suggestedRoadmaps(user.id)
        context = {
            'suggestedRoadmaps': suggestedRoadmaps,
            'name': user.first_name + ' ' + user.last_name,
        }
        return render(request, 'personAnalytics.html', context=context)